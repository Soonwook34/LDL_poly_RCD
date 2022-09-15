import pandas as pd

concept_df = pd.read_csv("./csv/concept_mapping.csv")

source_concept = []
source_no = []
source_mapped_no = []
target_concept = []
target_no = []
target_mapped_no = []
with open("./graph/knowledgeGraph.txt", "r") as f:
    for i in f.readlines():
        i = i.replace('\n', '').split('\t')
        source = int(i[0]) + 1
        target = int(i[1]) + 1
        source_mapped_no.append(source)
        target_mapped_no.append(target)
        source_no.append(int(concept_df[concept_df.mapped_concept_no == source].concept_no.iloc[0]))
        target_no.append(int(concept_df[concept_df.mapped_concept_no == target].concept_no.iloc[0]))
        source_concept.append(concept_df[concept_df.mapped_concept_no == source].Skills.iloc[0])
        target_concept.append(concept_df[concept_df.mapped_concept_no == target].Skills.iloc[0])

concept_relation_df = pd.DataFrame({
    "Source 스킬명": source_concept,
    "Source 스킬코드": source_no,
    "Source 스킬코드(학습용)": source_mapped_no,
    "Target 스킬명": target_concept,
    "Target 스킬코드": target_no,
    "Target 스킬코드(학습용)": target_mapped_no,
})

SAVE_PATH = "./csv/concept_relation.csv"
concept_relation_df.to_csv(SAVE_PATH, index=False, encoding="utf-8-sig")
print(f"saved at {SAVE_PATH}")
