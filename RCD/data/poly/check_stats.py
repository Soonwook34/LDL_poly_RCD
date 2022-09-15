import json


def check_stats():
    data_file = "./log_data.json"

    with open(data_file, encoding="utf8") as i_f:
        data = json.load(i_f)

    log_num = []
    score = {0: 0, 1: 0}
    for line in data:
        log_num.append(line["log_num"])
        for log in line["logs"]:
            score[log["score"]] += 1

    avg = sum(log_num, 0.0) / len(log_num)
    min_num = min(log_num)
    min_index = log_num.index(min_num)
    max_num = max(log_num)
    max_index = log_num.index(max_num)
    correct_rate = score[1] / (score[0] + score[1]) * 100

    print(f"평균 로그: {avg}\n최소 길이 로그: {min_num} (user_id {min_index + 1})\n최대 길이 로그: {max_num} (user_id {max_index + 1})\n정답 비율: {correct_rate:.2f}% ({score[1]}:{score[0]})")
    # junyi
    # 평균 로그: 35.3835
    # 최소 길이 로그: 15 (user_id 3)
    # 최대 길이 로그: 235 (user_id 5140)
    # 정답 비율: 65.17% (230587:123248)
    ##############################
    # ASSIST
    # 평균 로그: 107.26634576815083
    # 최소 길이 로그: 15 (user_id 236)
    # 최대 길이 로그: 1021 (user_id 281)
    # 정답 비율: 65.77% (175890:91525)
    ##############################
    # poly
    # 평균 로그: 179.0
    # 최소 길이 로그: 30 (user_id 1)
    # 최대 길이 로그: 330 (user_id 91)
    # 정답 비율: 83.35% (80570:16090)


if __name__ == '__main__':
    check_stats()
