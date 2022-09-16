import numpy as np
import argparse
import json
import random
from scipy.stats import norm


class GenDataArgParser(argparse.ArgumentParser):
    def __init__(self):
        super(GenDataArgParser, self).__init__()
        self.add_argument('--student_n', type=int, default=4000,
                          help='Number of students')
        self.add_argument('--exercise_n', type=int, default=50,
                          help='Number of exercises')
        self.add_argument('--concept_n', type=int, default=5,
                          help='Number of concepts')
        self.add_argument('--concept_map', type=int, default=1,
                          help='Shape of concept map / 0: line, 1: binary tree')
        self.add_argument('--sample_n', type=int, default=100,
                          help='Number of sampling')
        self.add_argument('--ability_min', type=int, default=0.2,
                          help='Minimum initial answer rate(ability), [0,1)')
        self.add_argument('--name', type=str, default='test',
                          help='Dataset name')
        self.add_argument('--ability_min', type=float, default=0,
                          help="Min vaule of student's ability")
        self.add_argument('--ability_max', type=float, default=5,
                          help="Max vaule of student's ability")
        self.add_argument('--difficulty_min', type=float, default=0,
                          help="Min vaule of exercise's difficulty")
        self.add_argument('--difficulty_max', type=float, default=5,
                          help="Max vaule of exercise's difficulty")
        self.add_argument('--discrimination_min', type=float, default=0.5,
                          help="Min vaule of exercise's discrimination")
        self.add_argument('--discrimination_max', type=float, default=2,
                          help="Max vaule of exercise's discrimination")
        self.add_argument('--pseudo_guessing_min', type=float, default=-0.2,
                          help="Min vaule of exercise's pseudo guessing")
        self.add_argument('--pseudo_guessing_max', type=float, default=0.2,
                          help="Max vaule of exercise's pseudo guessing")


class Student():
    def __init__(self, args, exercise_per_concept):
        # 학생 응답 기록 a[s][e] (right or wrong)
        self.responses = [[0 for e in range(exercise_per_concept)] for c in range(args.concept_n)]
        # 학생 정답 기록, 1[a[s][e] == 1(right)]
        self.answers = [[0 for e in range(exercise_per_concept)] for c in range(args.concept_n)]
        # 학생 concept별 정답률(=능력) 기록, p(c)
        self.abilities = [0 for c in range(args.concept_n)]

    def calc_ability(self, concept):
        self.abilities[concept] = np.mean(self.answers[concept])


class Exercise():
    def __init__(self, args, e, c):
        self.num = e
        self.concept = concept
        self.difficulty = np.random.rand() * (args.difficulty_max - args.difficulty_min) + args.difficulty_min
        self.discrimination = np.random.rand() * (args.discrimination_max - args.discrimination_min) + args.discrimination_min
        self.pseudo_guessing = np.random.rand() * (args.pseudo_guessing_max - args.pseudo_guessing_min) + args.pseudo_guessing_min

    def ICC(self, ability):
        return max((1 - self.pseudo_guessing) / (1 + np.exp(-self.discrimination * (ability - self.difficulty))), 0)


class Concept():
    def __init__(self, args, c):
        self.num = c
        # prerequisite concept of concept c, c_pre
        # 일자 구조
        if args.concept_map == "0":
            self.c_pre = max(c - 1, 0)
        # 이진 트리 구조
        elif args.concept_map == "1":
            self.c_pre = int((c - 1) / 2)
        self.c_pre = int((c - 1) / 2)

    def sample_ability(self, ability_pre, sample_n):
        return norm(ability_pre, 1).rvs(100).mean()


def generate_dataset(args):
    dataset = []
    exercise_per_concept = int(args.exercise_n / args.concept_n)
    students = [Student(args, s, exercise_per_concept) for s in range(args.student_n)]
    exercises = [[Exercise(args, e + exercise_per_concept * c, c) for e in range(exercise_per_concept)] for c in range(args.concept_n)]
    concepts = [Concept(args, c) for c in range(args.concept_n)]

    for s in students:
        s.abilities[0] = random.uniform(args.ability_min, 1)
        for c in concepts:
            s.abilities[c.num] = c.sample_ability(s.abilities[c.c_pre], args.sample_n)
            for e in exercises[c.num]:
                # TODO: generate log
    return dataset


def convert_dataset(dataset):
    log_data = []
    # TODO: convert dataset into json form
    return log_data


if __name__ == '__main__':
    args = GenDataArgParser().parse_args()
    print(str(args))
    dataset = generate_dataset(args)
    log_data = convert_dataset(dataset)
    with open(f"./log_data_{args.name}.json", 'w', encoding='utf8') as output_file:
        json.dump(log_data, output_file, indent=4, ensure_ascii=False)