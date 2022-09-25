import pandas as pd
import numpy as np
import os

# csv 불러오기
concept_mapping_df = pd.read_csv("./csv/subject_metadata.csv")

dependency_list = []
concept_list = []
# SubjectId,Name,ParentId,Level
for i in range(len(concept_mapping_df)):
    if int(concept_mapping_df['SubjectId'][i]) not in concept_list:
        concept_list.append(int(concept_mapping_df['SubjectId'][i]))
    if np.isnan(concept_mapping_df["ParentId"][i]):
        continue
    else:
        dependency_list.append((int(concept_mapping_df['ParentId'][i]), int(concept_mapping_df['SubjectId'][i])))

concept_list.sort()
print(f"concept_n: {len(concept_list)}")

dependency = ""
dependency_list.sort(key=lambda x:x[0])
for dep in dependency_list:
    dependency += f"{concept_list.index(dep[0])}\t{concept_list.index(dep[1])}\n"

if os.path.isfile("./graph/K_Undirected.txt"):
    os.remove("./graph/K_Undirected.txt")
if os.path.isfile("./graph/K_Undirected.txt"):
    os.remove("./graph/K_Directed.txt")

with open('./graph/K_Directed.txt', 'w') as f:
    f.write(dependency)
with open('./graph/K_Undirected.txt', 'w') as f:
    f.write("0\t0\n")