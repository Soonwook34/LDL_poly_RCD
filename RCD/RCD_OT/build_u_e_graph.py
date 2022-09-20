import json
import argparse
import random

class UEGraphArgParser(argparse.ArgumentParser):
    def __init__(self):
        super(UEGraphArgParser, self).__init__()
        self.add_argument('--dir', type=str, default="../data/poly/",
                          help='Directory Path')

def build_local_map(args):
    data_file = args.dir + 'train_set.json'
    with open('config.txt') as i_f:
        i_f.readline()
        student_n, exer_n, knowledge_n = list(map(eval, i_f.readline().split(',')))

    # e
    # u
    with open(data_file, encoding='utf8') as i_f:
        data = json.load(i_f)
    u_from_e = ''  # e(src) to k(dst)
    e_from_u = ''  # k(src) to k(dst)
    print(len(data))
    for line in data:
        exer_id = line['exer_id'] - 1
        user_id = line['user_id'] - 1
        # OT: e_from_y에 option 기록
        option = line['option']
        for k in line['knowledge_code']:
            u_from_e += str(exer_id) + '\t' + str(user_id + exer_n) + '\n'
            # e_from_u += str(user_id + exer_n) + '\t' + str(exer_id) + '\n'
            # OT: e_from_u에 option 기록
            e_from_u += str(user_id + exer_n) + '\t' + str(exer_id) + '\t' + str(option) + '\n'
    with open(args.dir + 'graph/u_from_e.txt', 'w') as f:
        f.write(u_from_e)
    with open(args.dir + 'graph/e_from_u.txt', 'w') as f:
        f.write(e_from_u)


if __name__ == '__main__':
    args = UEGraphArgParser().parse_args()
    build_local_map(args)
