import json


def check_stats():
    data_file = "./log_data.json"

    with open(data_file, encoding="utf8") as i_f:
        data = json.load(i_f)

    log_num = []
    score = {0: 0, 1: 0}
    knowledge_num = []
    exercise_list = []
    concept_list = []
    for line in data:
        log_num.append(line["log_num"])
        for log in line["logs"]:
            score[log["score"]] += 1
            knowledge_num.append(len(log["knowledge_code"]))
            exercise_list.append(log["exer_id"])
            concept_list += log["knowledge_code"]

    avg = sum(log_num, 0.0) / len(log_num)
    min_num = min(log_num)
    min_index = log_num.index(min_num)
    max_num = max(log_num)
    max_index = log_num.index(max_num)
    correct_rate = score[1] / (score[0] + score[1]) * 100
    avg_knowledge = sum(knowledge_num, 0.0) / len(knowledge_num)

    print(f"Students: {len(log_num)}\n"
          f"Exercises: {len(set(exercise_list))} / {max(exercise_list)}\n"
          f"Concepts: {len(set(concept_list))} / {max(concept_list)}\n"
          f"Response records: {len(exercise_list)}\n"
          f"Concepts per exercise: {avg_knowledge:.2f}\n"
          f"Response records per student: {avg:.2f}\n"
          f"Min log: {min_num} (user_id {min_index + 1}) / Max log: {max_num} (user_id {max_index + 1})\n"
          f"Correct response rate: {correct_rate:.2f}% ({score[1]}:{score[0]})")

    # print(f"평균 로그: {avg}\n최소 길이 로그: {min_num} (user_id {min_index + 1})\n최대 길이 로그: {max_num} (user_id {max_index + 1})\nConcepts per Exercise: {avg_knowledge:.2f}\n정답 비율: {correct_rate:.2f}% ({score[1]}:{score[0]})")
    # junyi
    # Students: 10000
    # Exercises: 706 / 835
    # Concepts: 706 / 835
    # Response records: 353835
    # Concepts per exercise: 1.00
    # Response records per student: 35.38
    # Min log: 15 (user_id 3) / Max log: 235 (user_id 5140)
    # Correct response rate: 65.17% (230587:123248)
    ##############################
    # ASSIST
    # Students: 2493
    # Exercises: 17671 / 17746
    # Concepts: 123 / 123
    # Response records: 267415
    # Concepts per exercise: 1.19
    # Response records per student: 107.27
    # Min log: 15 (user_id 236) / Max log: 1021 (user_id 281)
    # Correct response rate: 65.77% (175890:91525)
    ##############################
    # poly
    # Students: 540
    # Exercises: 598 / 598
    # Concepts: 28 / 46
    # Response records: 96660
    # Concepts per exercise: 1.00
    # Response records per student: 179.00
    # Min log: 30 (user_id 1) / Max log: 330 (user_id 91)
    # Correct response rate: 83.35% (80570:16090)
    ##############################
    # NeurIPS Edu Chall 2020
    # Students: 4918
    # Exercises: 948 / 948
    # Concepts: 86 / 300
    # Response records: 1382727
    # Concepts per exercise: 4.02
    # Response records per student: 281.16
    # Min log: 50 (user_id 65) / Max log: 827 (user_id 1368)
    # Correct response rate: 53.73% (742983:639744)


if __name__ == '__main__':
    check_stats()
