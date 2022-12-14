import numpy as np
import argparse
import json
import random
import os
from scipy.stats import norm, bernoulli

from check_stats import check_stats


class GenDataArgParser(argparse.ArgumentParser):
    def __init__(self):
        super(GenDataArgParser, self).__init__()
        self.add_argument('--student_n', type=int, default=100,
                          help='Number of students')
        self.add_argument('--exercise_n', type=int, default=300,
                          help='Number of exercises')
        self.add_argument('--concept_n', type=int, default=6,
                          help='Number of concepts')
        self.add_argument('--concept_map', type=int, default=2,
                          help='Shape of concept map / 0: line, 1: binary tree, 2: 2 lines')
        self.add_argument('--sample_n', type=int, default=100,
                          help='Number of sampling')
        self.add_argument('--name', type=str, default='KSC',
                          help='Dataset name')
        self.add_argument('--ability_min', type=float, default=0,
                          help="Min value of student's initial ability, [0,1)")
        self.add_argument('--ability_max', type=float, default=1,
                          help="Max value of student's initial ability, (args.ability_min, 1]")
        self.add_argument('--difficulty_min', type=float, default=0,
                          help="Min value of exercise's difficulty")
        self.add_argument('--difficulty_max', type=float, default=2,
                          help="Max value of exercise's difficulty")
        self.add_argument('--discrimination_min', type=float, default=0,
                          help="Min value of exercise's discrimination")
        self.add_argument('--discrimination_max', type=float, default=2,
                          help="Max value of exercise's discrimination")
        self.add_argument('--pseudo_guessing_min', type=float, default=0,
                          help="Min value of exercise's pseudo guessing")
        self.add_argument('--pseudo_guessing_max', type=float, default=0.2,
                          help="Max value of exercise's pseudo guessing")


class Student:
    def __init__(self, args, s, exercise_per_concept):
        self.num = s
        # ?????? ?????? ?????? a_s,e (right or wrong)
        self.responses = [[0 for e in range(exercise_per_concept)] for c in range(args.concept_n)]
        # ?????? ?????? ??????, 1[a_{s,e == 1(right)]
        self.answers = [[0 for e in range(exercise_per_concept)] for c in range(args.concept_n)]
        # ?????? concept??? ?????????(=??????) ??????, p(c)
        self.abilities = [0 for c in range(args.concept_n)]

    def calc_ability(self, c):
        self.abilities[c] = np.mean(self.answers[c])


class Exercise:
    def __init__(self, args, e, c):
        self.num = e
        self.c = c
        self.difficulty = np.random.rand() * (args.difficulty_max - args.difficulty_min) + args.difficulty_min
        self.discrimination = np.random.rand() * (args.discrimination_max - args.discrimination_min) + args.discrimination_min
        self.pseudo_guessing = np.random.rand() * (args.pseudo_guessing_max - args.pseudo_guessing_min) + args.pseudo_guessing_min

    def ICC(self, ability):
        ability = ability * 6
        return min(max((1 - self.pseudo_guessing) / (1 + np.exp(-self.discrimination * (ability - self.difficulty))), 0), 1)


class Concept:
    def __init__(self, args, c):
        self.num = c
        self.sample_n = args.sample_n
        # prerequisite concept of concept c, c_pre
        # ?????? ??????
        if args.concept_map == 0:
            self.c_pre = max(c - 1, 0)
        # ?????? ?????? ??????
        elif args.concept_map == 1:
            self.c_pre = int((c - 1) / 2)
        elif args.concept_map == 2:
            self.c_pre = max(c - 1, 0)
            if c == int(args.concept_n / 2):
                self.c_pre = c

    def sample_ability(self, student):
        return min(max(norm(student.abilities[self.c_pre], 0.1).rvs(self.sample_n).mean(), 0), 1)


def generate_dataset(args):
    dataset, dataset_0 = [], []
    exercise_per_concept = int(args.exercise_n / args.concept_n)
    students = [Student(args, s, exercise_per_concept) for s in range(args.student_n)]
    exercises = [[Exercise(args, e, c) for e in range(exercise_per_concept)] for c in range(args.concept_n)]
    concepts = [Concept(args, c) for c in range(args.concept_n)]

    right_rate = []
    for student in students:
        student.abilities[0] = random.uniform(args.ability_min, args.ability_max)
        if args.concept_map == 2:
            student.abilities[int(args.concept_n / 2)] = random.uniform(args.ability_min, args.ability_max)
        logs, logs_0 = [], []
        for concept in concepts:
            p_c = concept.sample_ability(student)
            for exercise in exercises[concept.num]:
                p_e_given_c = exercise.ICC(p_c * student.abilities[concept.c_pre])
                a_se = bernoulli.rvs(p_e_given_c)
                student.responses[concept.num][exercise.num] = a_se
                student.answers[concept.num][exercise.num] = a_se
                logs.append({"exer_id": concept.num * exercise_per_concept + exercise.num + 1, "score": a_se,
                             "p_e": p_e_given_c, "knowledge_code": [concept.num + 1]})
                logs_0.append({"exer_id": concept.num * exercise_per_concept + exercise.num + 1, "score": a_se,
                             "p_e": p_e_given_c, "knowledge_code": [1]})
            student.calc_ability(concept.num)
            # ?????? ?????????
            right_rate.append(student.abilities[concept.num])
        dataset.append(logs)
        dataset_0.append(logs_0)
        print(student.abilities[0], student.abilities[int(args.concept_n / 2)], student.abilities)
    return dataset, dataset_0, sum(right_rate) / len(right_rate)


def convert_dataset(dataset):
    log_data_dict = {}
    for student_id, logs in enumerate(dataset):
        log_data_dict[student_id] = {"user_id": student_id + 1, "log_num": len(logs), "logs": logs}

    log_data = list(log_data_dict.values())
    log_data = sorted(log_data, key=lambda log: log["user_id"])
    return log_data


if __name__ == '__main__':
    args = GenDataArgParser().parse_args()
    print(str(args))

    ability_log = []
    for i in range(1):
        print(f"{i}...")
        dataset, dataset_0, rr = generate_dataset(args)
        ability_log.append(rr)
    print(sum(ability_log) / len(ability_log))

    log_data = convert_dataset(dataset)
    with open(f"./log_data_{args.name}.json", 'w', encoding='utf8') as output_file:
        json.dump(log_data, output_file, indent=4, ensure_ascii=False)
    log_data_0 = convert_dataset(dataset_0)
    with open(f"./log_data_{args.name}_0.json", 'w', encoding='utf8') as output_file:
        json.dump(log_data_0, output_file, indent=4, ensure_ascii=False)

    # K_Directed.txt, K_Undirected.txt
    dependency = ""
    for c in range(args.concept_n):
        if c == 0:
            continue
        if args.concept_map == 0:
            dependency += f"{c - 1}\t{c}\n"
        elif args.concept_map == 1:
            dependency += f"{int((c - 1) / 2)}\t{c}\n"
        elif args.concept_map == 2:
            if c == int(args.concept_n / 2):
                continue
            else:
                dependency += f"{c - 1}\t{c}\n"

    file_name = f'{args.concept_map}_{args.concept_n}'
    if os.path.isfile(f'./graph/K_Undirected_{file_name}.txt'):
        os.remove(f'./graph/K_Undirected_{file_name}.txt')
    if os.path.isfile(f'./graph/K_Directed_{file_name}.txt'):
        os.remove(f'./graph/K_Directed_{file_name}.txt')

    with open(f'./graph/K_Undirected_{file_name}.txt', 'w') as f:
        f.write("0\t0\n")
    with open(f'./graph/K_Directed_{file_name}.txt', 'w') as f:
        f.write(dependency)

    check_stats(f"./log_data_{args.name}.json")
