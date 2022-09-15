import pandas as pd
import json

# csv 불러오기
concept_mapping_df = pd.read_csv("./csv/concept_mapping.csv")
exercise_concept_df = pd.read_csv("./csv/exercise_concept.csv")
student_exercise_df = pd.read_csv("./csv/student_exercise.csv")

# join 연산
join_df = pd.merge(left=student_exercise_df, right=exercise_concept_df, how="inner", on=["test_no", "exercise_no"])
join_df = pd.merge(left=join_df, right=concept_mapping_df, how="inner", on="concept_no")
join_df = join_df[["student_id", "exercise_no", "score", "concept_no", "mapped_concept_no"]]
print(join_df.head())
print(len(join_df))

# 결측값 확인
ori_student_df = student_exercise_df["student_id"].drop_duplicates().dropna(axis=0)
ori_exercise_df = exercise_concept_df["exercise_no"].drop_duplicates().dropna(axis=0)
ori_concept_df = concept_mapping_df["concept_no"].drop_duplicates().dropna(axis=0)
student_df = join_df["student_id"].drop_duplicates().dropna(axis=0)
exercise_df = join_df["exercise_no"].drop_duplicates().dropna(axis=0)
concept_df = join_df["concept_no"].drop_duplicates().dropna(axis=0)
print(f"student {len(student_df)} / {len(ori_student_df)}")
print(f"exercise {len(exercise_df)} / {len(ori_exercise_df)}")
print(f"concept {len(concept_df)} / {len(ori_concept_df)}")

# user_id를 1번부터 할당하기 위한 매핑
student_list = list(student_df.sort_values())
student_id_dict = dict(zip(student_list, range(1, len(student_list)+1)))

# user_id 당 log_num 계산 및 매핑 (푼 exercise 수)
log_num_dict = join_df["student_id"].value_counts().to_dict()

# exer_id를 1번부터 할당하기 위한 매핑
exercise_list = list(exercise_df.sort_values())
exercise_no_dict = dict(zip(exercise_list, range(1, len(exercise_list)+1)))

# exer_id - knowledge_code 매핑
exercise_list = list(exercise_df)
concept_list = []
for exer_id in exercise_list:
    concept_no = int(exercise_concept_df.loc[exercise_concept_df["exercise_no"] == exer_id]["concept_no"].values[0])
    knowledge_code = int(concept_mapping_df.loc[concept_mapping_df["concept_no"] == concept_no]["mapped_concept_no"].values[0])
    concept_list.append(knowledge_code)
concept_no_dict = dict(zip(exercise_list, concept_list))

# 전체 log_data 생성
log_data_dict = {}
for student_id in student_df:
    log_data_dict[student_id] = {"user_id": student_id_dict[student_id], "log_num": log_num_dict[student_id], "logs": []}

# logs 채워넣기
student_id_list = list(join_df["student_id"])
exercise_no_list = list(join_df["exercise_no"])
score_list = list(join_df["score"])
for student_id, exer_id, score in zip(student_id_list, exercise_no_list, score_list):
    log_data_dict[student_id]["logs"].append({"exer_id": exercise_no_dict[exer_id], "score":score , "knowledge_code": [concept_no_dict[exer_id]]})

log_data = list(log_data_dict.values())
log_data = sorted(log_data, key=lambda log: log["user_id"])

# log_data.json에 저장
with open('./log_data.json', 'w', encoding='utf8') as output_file:
    json.dump(log_data, output_file, indent=4, ensure_ascii=False)

print(f"{len(log_data)} logs saved")
