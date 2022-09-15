import pandas as pd
import json

s_e_df = pd.read_csv("./csv/student_exercise_OT.csv")

print(s_e_df.head())

s_e_df.loc[s_e_df["score"] == 'Y', "score"] = 1
s_e_df.loc[s_e_df["score"] == 'N', "score"] = 0

s_e_df.to_csv("./csv/student_exercise_OT.csv")