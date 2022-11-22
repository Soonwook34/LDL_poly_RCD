import pandas as pd
import json

# csv 불러오기
concept_mapping_df = pd.read_csv("./csv/subject_metadata.csv")
exercise_concept_df = pd.read_csv("./csv/question_metadata_task_3_4.csv")
student_exercise_df = pd.read_csv("./csv/train_task_3_4.csv")

concept_list = []
# SubjectId,Name,ParentId,Level
for i in range(len(concept_mapping_df)):
    concept_list.append(int(concept_mapping_df['SubjectId'][i]))
concept_list = list(set(concept_list))
concept_list.sort()

# QuestionId,SubjectId
exercise_dict = {}
for i in range(len(exercise_concept_df)):
    concepts = list(map(int, exercise_concept_df['SubjectId'][i][1:-1].split(", ")))
    concepts = [concept_list.index(c) + 1 for c in concepts]
    exercise_dict[int(exercise_concept_df['QuestionId'][i])] = concepts
exercise_dict = dict((k, v) for k, v in sorted(exercise_dict.items()))

# QuestionId,UserId,AnswerId,IsCorrect,CorrectAnswer,AnswerValue
exercise_list, student_list = [], []
print(len(student_exercise_df))
for i in range(len(student_exercise_df)):
    exercise_list.append(int(student_exercise_df['QuestionId'][i]))
    student_list.append(int(student_exercise_df['UserId'][i]))
exercise_list = list(set(exercise_list))
student_list = list(set(student_list))
exercise_list.sort()
student_list.sort()
print(exercise_list[-1], len(exercise_list))
print(student_list[-1], len(student_list))

# 전체 log_data 생성
log_data_dict = {}
for student_id in student_list:
    log_data_dict[student_id] = {"user_id": student_list.index(student_id) + 1, "log_num": 0, "logs": []}

# QuestionId,UserId,AnswerId,IsCorrect,CorrectAnswer,AnswerValue
for i in range(len(student_exercise_df)):
    uid = int(student_exercise_df.iloc[i]['UserId'])
    exer_id = int(student_exercise_df.iloc[i]['QuestionId'])
    score = int(student_exercise_df.iloc[i]['IsCorrect'])
    option = int(student_exercise_df.iloc[i]['AnswerValue'])
    log_data_dict[uid]["log_num"] += 1
    log_data_dict[uid]["logs"].append({"exer_id": exercise_list.index(exer_id) + 1, "score":score, "option":option,
                                       "knowledge_code": exercise_dict[exer_id]})

log_data = list(log_data_dict.values())
log_data = sorted(log_data, key=lambda log: log["user_id"])[:2000]     # [:int(len(student_list)/2)]

# log_data.json에 저장
with open('./log_data.json', 'w', encoding='utf8') as output_file:
    json.dump(log_data, output_file, indent=4, ensure_ascii=False)

print(f"{len(log_data)} logs saved")

student_list, exercise_list, concept_list = [], [], []
for logs in log_data:
    student_list.append(logs["user_id"])
    for log in logs["logs"]:
        exercise_list.append(log["exer_id"])
        concept_list += log["knowledge_code"]
student_list = list(set(student_list))
exercise_list = list(set(exercise_list))
concept_list = list(set(concept_list))
student_list.sort()
exercise_list.sort()
concept_list.sort()

# Student 총 2000 (MAX 2000), Exercise 총 948 (MAX 948), Concept 총 86 (MAX 300)
print(f"Student 총 {len(student_list)} (MAX {student_list[-1]}), Exercise 총 {len(exercise_list)} (MAX {exercise_list[-1]}), Concept 총 {len(concept_list)} (MAX {concept_list[-1]})")