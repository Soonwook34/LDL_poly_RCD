import pandas as pd
import os

##############################
undirected = True
##############################

concept_df = pd.read_csv("./csv/concept_dependency_reduce.csv")

source_list = list(concept_df["source_no"])
target_list = list(concept_df["target_no"])

dependency = ""

for source, target in zip(source_list, target_list):
    dependency += f"{source-1}\t{target-1}\n"

if os.path.isfile("./graph/K_Undirected.txt"):
    os.remove("./graph/K_Undirected.txt")
if os.path.isfile("./graph/K_Undirected.txt"):
    os.remove("./graph/K_Directed.txt")

if undirected:
    with open('./graph/K_Undirected.txt', 'w') as f:
        f.write(dependency)
    with open('./graph/K_Directed.txt', 'w') as f:
        f.write("0\t0\n")
else:
    with open('./graph/K_Directed.txt', 'w') as f:
        f.write(dependency)
    with open('./graph/K_Undirected.txt', 'w') as f:
        f.write("0\t0\n")
