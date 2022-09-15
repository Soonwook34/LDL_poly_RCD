import torch
import torch.nn as nn
import torch.optim as optim
import numpy as np
import json
import sys
from sklearn.metrics import roc_auc_score
from data_loader import TrainDataLoader, ValTestDataLoader
from model import Net
from utils import CommonArgParser, construct_local_map
from tqdm import tqdm
import time
from torch.utils.tensorboard import SummaryWriter

def train(args, local_map):
    START_TRAIN = time.time()
    print(f"=====train 시작=====\n{time.strftime('%y-%m-%d %H:%M:%S', time.localtime(START_TRAIN + 32400))}")

    writer = SummaryWriter(log_dir=f"runs/{args.log}")

    data_loader = TrainDataLoader()
    device = torch.device(('cuda:%d' % (args.gpu)) if torch.cuda.is_available() else 'cpu')
    net = Net(args, local_map)
    net = net.to(device)
    # print(net)
    optimizer = optim.Adam(net.parameters(), lr=0.0001)

    # 그래프 테스트
    g = local_map['e_from_u']
    print(g)
    # for option in g.etypes:
    #     print(g.edges[option])

    print('training model...')
    # KT / KT+OT / OT
    if args.mode == 0:
        loss_function = nn.NLLLoss()
    elif args.mode == 1:
        loss_function_kt = nn.NLLLoss()
        loss_function_ot = nn.CrossEntropyLoss()
    else:
        loss_function = nn.CrossEntropyLoss()

    best_val_loss = 100.0
    patience = 0
    # Training
    for epoch in range(args.epoch_n):

        data_loader.reset()
        train_data = []
        while not data_loader.is_end():
            input_stu_ids, input_exer_ids, input_knowledge_embs, labels, options = data_loader.next_batch()
            input_stu_ids, input_exer_ids, input_knowledge_embs, labels, options = input_stu_ids.to(device), input_exer_ids.to(device), input_knowledge_embs.to(device), labels.to(device), options.to(device)
            train_data.append([input_stu_ids, input_exer_ids, input_knowledge_embs, labels, options])

        running_train_loss = 0.0
        exer_count = 0
        with tqdm(train_data, unit="it") as train_bar:
            train_bar.set_description(f"Train {epoch+1}/{args.epoch_n}")
            for data in train_bar:
                input_stu_ids, input_exer_ids, input_knowledge_embs, labels, options = data
                # KT / KT+OT / OT
                optimizer.zero_grad()
                if args.mode == 0:
                    # forward
                    output_1 = net.forward(input_stu_ids, input_exer_ids, input_knowledge_embs)
                    output_0 = torch.ones(output_1.size()).to(device) - output_1
                    output = torch.cat((output_0, output_1), 1)
                    # loss (KT)
                    loss = loss_function(torch.log(output + 1e-10), labels)
                elif args.mode == 1:
                    # forward
                    output_1, output_ot = net.forward(input_stu_ids, input_exer_ids, input_knowledge_embs)
                    output_0 = torch.ones(output_1.size()).to(device) - output_1
                    output_kt = torch.cat((output_0, output_1), 1)
                    # loss (KT+OT)
                    loss_kt = loss_function_kt(torch.log(output_kt + 1e-10), labels)
                    loss_ot = loss_function_ot(output_ot, options)
                    loss = args.lamb * loss_kt + (1 - args.lamb) * loss_ot
                else:
                    # forward
                    output = net.forward(input_stu_ids, input_exer_ids, input_knowledge_embs)
                    # loss (OT)
                    loss = loss_function(output, options)

                loss.backward()
                optimizer.step()
                # weight에 ReLU 적용 (non-negative value로 변경)
                net.apply_clipper()

                exer_count += len(labels)
                running_train_loss += loss.item() * len(labels)
                train_bar.set_postfix(loss=f"{running_train_loss / exer_count:.6f}")
        train_loss = running_train_loss / exer_count

        # Validation
        if (epoch + 1) % 1 == 0:
            accuracy, rmse, auc, val_loss = predict(args, net, epoch)
            # Early Stopping 구현 (Val loss)
            if best_val_loss - val_loss > args.early_stopping:
                patience = 0
            else:
                patience += 1
                if patience >= args.patience_max:
                    print(f"Patience Count reached at {patience}. Early Stopping...")
                    break
                else:
                    print(f"Patience Count updated ({patience}/{args.patience_max}). best_val_loss: {best_val_loss}, curr_val_loss: {val_loss}")
            # Best Model 저장
            if best_val_loss > val_loss:
                torch.save(net, f"model/RCD_{args.log}_best.pt")
                print(f"Best Model Changed at epoch {epoch+1}")
                best_val_loss = val_loss

        # Tensorboard 기록
        writer.add_scalars("Loss", {'train_loss': train_loss, 'valid_loss': val_loss}, epoch + 1)
        if args.mode == 0:
            writer.add_scalars("Metric", {'accuracy_KT': accuracy,
                                          'RMSE_KT': rmse,
                                          'AUC_KT': auc}, epoch + 1)
        elif args.mode == 1:
            writer.add_scalars("Metric", {'accuracy_KT': accuracy[0],
                                          'RMSE_KT': rmse[0],
                                          'AUC_KT': auc[0],
                                          'accuracy_OT': accuracy[1],
                                          'RMSE_OT': rmse[1],
                                          'AUC_OT': auc[1]}, epoch + 1)
        else:
            writer.add_scalars("Metric", {'accuracy_OT': accuracy,
                                          'RMSE_OT': rmse,
                                          'AUC_OT': auc}, epoch + 1)

    writer.close()

    END_TRAIN = time.time()
    print(f"=====train 종료=====\n{time.strftime('%y-%m-%d %H:%M:%S', time.localtime(END_TRAIN + 32400))}")
    print(f"=====train 소요 시간=====\n{time.strftime('%d %H:%M:%S', time.localtime(END_TRAIN - START_TRAIN))}")


def predict(args, net, epoch):
    device = torch.device(('cuda:%d' % args.gpu) if torch.cuda.is_available() else 'cpu')
    data_loader = ValTestDataLoader('validation')
    print('predicting model...')
    data_loader.reset()
    net.eval()

    val_data = []
    while not data_loader.is_end():
        input_stu_ids, input_exer_ids, input_knowledge_embs, labels, options = data_loader.next_batch()
        input_stu_ids, input_exer_ids, input_knowledge_embs, labels, options = input_stu_ids.to(device), input_exer_ids.to(device), input_knowledge_embs.to(device), labels.to(device), options.to(device)
        val_data.append([input_stu_ids, input_exer_ids, input_knowledge_embs, labels, options])

    # KT / KT+OT / OT
    if args.mode == 0:
        loss_function = nn.NLLLoss()
    elif args.mode == 1:
        loss_function_kt = nn.NLLLoss()
        loss_function_ot = nn.CrossEntropyLoss()
    else:
        loss_function = nn.CrossEntropyLoss()

    correct_count, exer_count = 0, 0
    pred_all, label_all = [], []
    running_val_loss = 0.0
    with tqdm(val_data, unit="it") as val_bar:
        val_bar.set_description(f"Valid {epoch+1}/{args.epoch_n}")
        if args.mode == 1:
            pred_all, label_all = [[], []], [[], []]
            correct_count = [0, 0]
        for data in val_bar:
            input_stu_ids, input_exer_ids, input_knowledge_embs, labels, options = data
            # KT / KT+OT / OT
            if args.mode == 0:
                # forward
                output_1 = net.forward(input_stu_ids, input_exer_ids, input_knowledge_embs)
                output_pred = output_1.view(-1)
                # loss (KT)
                output_0 = torch.ones(output_1.size()).to(device) - output_1
                output = torch.cat((output_0, output_1), 1)
                loss = loss_function(torch.log(output + 1e-10), labels)
                # count hit
                for i in range(len(labels)):
                    if (labels[i] == 1 and output_pred[i] > 0.5) or (labels[i] == 0 and output_pred[i] < 0.5):
                        correct_count += 1
                # store pred
                pred_all += output_pred.to(torch.device('cpu')).tolist()
                label_all += labels.to(torch.device('cpu')).tolist()
            elif args.mode == 1:
                # forward
                output_kt, output_ot = net.forward(input_stu_ids, input_exer_ids, input_knowledge_embs)
                output_pred_kt = output_kt.view(-1)
                output_pred_ot = torch.argmax(output_ot, dim=1)
                # loss (KT+OT)
                output_0 = torch.ones(output_kt.size()).to(device) - output_kt
                output_kt = torch.cat((output_0, output_kt), 1)
                loss_kt = loss_function_kt(torch.log(output_kt + 1e-10), labels)
                loss_ot = loss_function_ot(output_ot, options)
                loss = args.lamb * loss_kt + (1 - args.lamb) * loss_ot
                # count hit (KT+OT 다 맞아야 정답)
                for i in range(len(labels)):
                    if (labels[i] == 1 and output_pred_kt[i] > 0.5) or (labels[i] == 0 and output_pred_kt[i] < 0.5):
                        correct_count[0] += 1
                    if options[i] == output_pred_ot[i]:
                        correct_count[1] += 1
                # store pred
                pred_all[0] += output_pred_kt.to(torch.device('cpu')).tolist()
                label_all[0] += labels.to(torch.device('cpu')).tolist()
                pred = output_ot.flatten()
                option = nn.functional.one_hot(options, num_classes=4).flatten()
                pred_all[1] += pred.to(torch.device('cpu')).tolist()
                label_all[1] += option.to(torch.device('cpu')).tolist()
            else:
                # forward
                output = net.forward(input_stu_ids, input_exer_ids, input_knowledge_embs)
                output_pred = torch.argmax(output, dim=1)
                # count hit
                for i in range(len(labels)):
                    if options[i] == output_pred[i]:
                        correct_count += 1
                # loss OT
                loss = loss_function(output, options)
                # store pred
                pred = output.flatten()
                label = nn.functional.one_hot(options, num_classes=4).flatten()
                pred_all += pred.to(torch.device('cpu')).tolist()
                label_all += label.to(torch.device('cpu')).tolist()
            exer_count += len(labels)
            running_val_loss += loss.item() * len(labels)
            if args.mode == 1:
                val_bar.set_postfix(acc_KT=f"{correct_count[0] / exer_count:.6f}", acc_OT=f"{correct_count[1] / exer_count:.6f}", val_loss=f"{running_val_loss / exer_count:.6f}")
            else:
                val_bar.set_postfix(acc=f"{correct_count / exer_count:.6f}", val_loss=f"{running_val_loss / exer_count:.6f}")

    # compute accuracy, RMSE, AUC, valid loss
    if args.mode == 1:
        accuracy, rmse, auc = [0, 0], [0, 0], [0, 0]
        for i in range(2):
            pred_all[i] = np.array(pred_all[i])
            label_all[i] = np.array(label_all[i])
        pred_all = np.array(pred_all, dtype=type(pred_all[0]))
        label_all = np.array(label_all, dtype=type(label_all[0]))
        for i in range(2):
            accuracy[i] = correct_count[i] / exer_count
            rmse[i] = np.sqrt(np.mean((label_all[i] - pred_all[i]) ** 2))
            auc[i] = roc_auc_score(label_all[i], pred_all[i])
        val_loss = running_val_loss / exer_count
        print_str = f"epoch={epoch + 1:2d} / " \
                    f"accuracy_KT={accuracy[0]:.6f}, rmse_KT={rmse[0]:.6f}, auc_KT={auc[0]:.6f} " \
                    f"accuracy_OT={accuracy[1]:.6f}, rmse_OT={rmse[1]:.6f}, auc_OT={auc[1]:.6f}, val_loss={val_loss:.6f}"
    else:
        pred_all = np.array(pred_all)
        label_all = np.array(label_all)
        accuracy = correct_count / exer_count
        rmse = np.sqrt(np.mean((label_all - pred_all) ** 2))
        auc = roc_auc_score(label_all, pred_all)
        val_loss = running_val_loss / exer_count
        print_str = f"epoch={epoch+1:2d} / accuracy={accuracy:.6f}, rmse={rmse:.6f}, auc={auc:.6f}, val_loss={val_loss:.6f}"
    print(print_str)
    with open(f'result/RCD_{args.log}.txt', 'a', encoding='utf8') as f:
        f.write(print_str + '\n')

    return accuracy, rmse, auc, val_loss


def save_snapshot(model, filename):
    f = open(filename, 'wb')
    torch.save(model.state_dict(), f)
    f.close()


if __name__ == '__main__':
    # START_MAIN = time.time()
    # print(f"=====main 시작=====\n{time.strftime('%y-%m-%d %H:%M:%S', time.localtime(START_MAIN + 32400))}")

    # args 정리
    args = CommonArgParser().parse_args()
    notice = ""
    if args.mode == 0:
        notice += "KT loss / "
    elif args.mode == 1:
        notice += f"KT+OT 혼합 loss, lambda={args.lamb} / "
    elif args.mode == 2:
        notice += "OT loss / "
    else:
        print("args.mode 오류 (0, 1, 2)")
        exit()
    if args.edge_emb:
        notice += "Edge Embedding 사용\n"
    else:
        notice += "Edge Embedding 사용 안 함\n"
    notice += str(args)
    print(notice)

    train(args, construct_local_map(args))

    # END_MAIN = time.time()
    # print(f"=====main 종료=====\n{time.strftime('%y-%m-%d %H:%M:%S', time.localtime(END_MAIN + 32400))}")
    # print(f"=====main 소요 시간=====\n{time.strftime('%d %H:%M:%S', time.localtime(END_MAIN - START_MAIN))}")
