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
import time


def train(args, local_map):
    START_TRAIN = time.time()
    print(f"=====train 시작=====\n{time.strftime('%y-%m-%d %H:%M:%S', time.localtime(START_TRAIN + 32400))}")

    data_loader = TrainDataLoader()
    device = torch.device(('cuda:%d' % (args.gpu)) if torch.cuda.is_available() else 'cpu')
    net = Net(args, local_map)
    net = net.to(device)
    # net = torch.nn.DataParallel(net)
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

    # Training
    for epoch in range(args.epoch_n):
        START_EPOCH = time.time()
        START_BATCH = time.time()
        print(f"=====epoch {epoch + 1} 시작=====\n{time.strftime('%y-%m-%d %H:%M:%S', time.localtime(START_EPOCH + 32400))}")

        data_loader.reset()
        running_loss = 0.0
        batch_count = 0
        prev_batch = 0
        while not data_loader.is_end():
            batch_count += 1
            input_stu_ids, input_exer_ids, input_knowledge_embs, labels, options = data_loader.next_batch()
            input_stu_ids, input_exer_ids, input_knowledge_embs, labels, options = input_stu_ids.to(device), input_exer_ids.to(device), input_knowledge_embs.to(device), labels.to(device), options.to(device)

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

            running_loss += loss.item()
            if batch_count % 200 == 199:
                END_BATCH = time.time()
                print(f"=====epoch {epoch + 1}@batch {prev_batch + 1}-{batch_count + 1} 소요 시간=====\n{time.strftime('%H:%M:%S', time.localtime(END_BATCH - START_BATCH))}")
                print(f"loss: {running_loss / 200:.10f}")
                START_BATCH = time.time()
                prev_batch = batch_count
                # print('[%d, %5d] loss: %.3f' % (epoch + 1, batch_count + 1, running_loss / 200))
                running_loss = 0.0
        END_BATCH = time.time()
        print(f"=====epoch {epoch + 1}@batch {prev_batch + 1}-{batch_count + 1} 소요 시간=====\n{time.strftime('%H:%M:%S', time.localtime(END_BATCH - START_BATCH))}")
        print(f"loss: {running_loss / 200:.10f}")

        # Val Test
        if (epoch + 1) % 2 == 0:
            START_TEST = time.time()
            print(f"=====epoch {epoch + 1}@test 시작=====\n{time.strftime('%y-%m-%d %H:%M:%S', time.localtime(START_TEST + 32400))}")
            # test and save current model every epoch
            # save_snapshot(net, f"model/model_{args.log}_epoch{str(epoch + 1)}")
            rmse, auc = predict(args, net, epoch)

            END_TEST = time.time()
            print(f"=====epoch {epoch + 1}@test 종료=====\n{time.strftime('%y-%m-%d %H:%M:%S', time.localtime(END_TEST + 32400))}")
            print(f"=====epoch {epoch + 1}@test 소요 시간=====\n{time.strftime('%H:%M:%S', time.localtime(END_TEST - START_TEST))}")
        END_EPOCH = time.time()
        print(f"=====epoch {epoch + 1} 종료=====\n{time.strftime('%y-%m-%d %H:%M:%S', time.localtime(END_EPOCH + 32400))}")
        print(f"=====epoch {epoch + 1} 소요 시간=====\n{time.strftime('%H:%M:%S', time.localtime(END_EPOCH - START_EPOCH))}")
    END_TRAIN = time.time()
    print(f"=====train 종료=====\n{time.strftime('%y-%m-%d %H:%M:%S', time.localtime(END_TRAIN + 32400))}")
    print(f"=====train 소요 시간=====\n{time.strftime('%d %H:%M:%S', time.localtime(END_TRAIN - START_TRAIN))}")


def predict(args, net, epoch):
    device = torch.device(('cuda:%d' % args.gpu) if torch.cuda.is_available() else 'cpu')
    data_loader = ValTestDataLoader('predict')
    print('predicting model...')
    data_loader.reset()
    net.eval()

    correct_count, exer_count = 0, 0
    batch_count, batch_avg_loss = 0, 0.0
    pred_all, label_all = [], []
    while not data_loader.is_end():
        batch_count += 1
        input_stu_ids, input_exer_ids, input_knowledge_embs, labels, options = data_loader.next_batch()
        input_stu_ids, input_exer_ids, input_knowledge_embs, labels, options = input_stu_ids.to(device), input_exer_ids.to(device), input_knowledge_embs.to(device), labels.to(device), options.to(device)

        # KT / KT+OT / OT
        if args.mode == 0:
            # forward
            output = net.forward(input_stu_ids, input_exer_ids, input_knowledge_embs)
            output_pred = output.view(-1)
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
            # count hit (KT+OT 다 맞아야 정답)
            for i in range(len(labels)):
                if (labels[i] == 1 and output_pred_kt[i] > 0.5) or (labels[i] == 0 and output_pred_kt[i] < 0.5):
                    if options[i] == output_pred_ot[i]:
                        correct_count += 1
            # store pred
            pred_all += output_pred_kt.to(torch.device('cpu')).tolist()
            label_all += labels.to(torch.device('cpu')).tolist()
            pred = output_ot.flatten()
            option = nn.functional.one_hot(options, num_classes=4).flatten()
            pred_all += pred.to(torch.device('cpu')).tolist()
            label_all += option.to(torch.device('cpu')).tolist()
        else:
            # forward
            output = net.forward(input_stu_ids, input_exer_ids, input_knowledge_embs)
            output_pred = torch.argmax(output, dim=1)
            # count hit
            for i in range(len(labels)):
                if options[i] == output_pred[i]:
                    correct_count += 1
            # store pred
            pred = output.flatten()
            label = nn.functional.one_hot(options, num_classes=4).flatten()
            pred_all += pred.to(torch.device('cpu')).tolist()
            label_all += label.to(torch.device('cpu')).tolist()
        exer_count += len(labels)

    pred_all = np.array(pred_all)
    label_all = np.array(label_all)
    # compute accuracy
    accuracy = correct_count / exer_count
    # compute RMSE
    rmse = np.sqrt(np.mean((label_all - pred_all) ** 2))
    # compute AUC
    auc = roc_auc_score(label_all, pred_all)
    print('epoch= %d, accuracy= %f, rmse= %f, auc= %f' % (epoch + 1, accuracy, rmse, auc))
    with open(f'result/RCD_log_{args.log}.txt', 'a', encoding='utf8') as f:
        f.write('epoch= %d, accuracy= %f, rmse= %f, auc= %f\n' % (epoch + 1, accuracy, rmse, auc))

    return rmse, auc


def save_snapshot(model, filename):
    f = open(filename, 'wb')
    torch.save(model.state_dict(), f)
    f.close()


if __name__ == '__main__':
    START_MAIN = time.time()
    print(f"=====main 시작=====\n{time.strftime('%y-%m-%d %H:%M:%S', time.localtime(START_MAIN + 32400))}")

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

    END_MAIN = time.time()
    print(f"=====main 종료=====\n{time.strftime('%y-%m-%d %H:%M:%S', time.localtime(END_MAIN + 32400))}")
    print(f"=====main 소요 시간=====\n{time.strftime('%d %H:%M:%S', time.localtime(END_MAIN - START_MAIN))}")
