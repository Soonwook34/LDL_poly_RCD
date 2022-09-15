nohup python -u main.py --student_n 540 --exer_n 598 --knowledge_n 46 --gpu 0 --epoch_n 50 --mode 0 --log KT_1_reduce > result/KT_1_reduce.out &
nohup python -u main.py --student_n 540 --exer_n 598 --knowledge_n 46 --gpu 1 --epoch_n 50 --mode 1 --lamb 0.1 --log KTOT_0.1_1_reduce > result/KTOT_0.1_1_reduce.out &
nohup python -u main.py --student_n 540 --exer_n 598 --knowledge_n 46 --gpu 2 --epoch_n 50 --mode 2 --log OT_1_reduce > result/OT_1_reduce.out &
sleep 10000
nohup python -u main.py --student_n 540 --exer_n 598 --knowledge_n 46 --gpu 0 --epoch_n 50 --mode 1 --lamb 0.2 --log KTOT_0.2_1_reduce > result/KTOT_0.2_1_reduce.out &
nohup python -u main.py --student_n 540 --exer_n 598 --knowledge_n 46 --gpu 1 --epoch_n 50 --mode 1 --lamb 0.5 --log KTOT_0.5_1_reduce > result/KTOT_0.5_1_reduce.out &
nohup python -u main.py --student_n 540 --exer_n 598 --knowledge_n 46 --gpu 2 --epoch_n 50 --mode 1 --lamb 0.8 --log KTOT_0.8_1_reduce > result/KTOT_0.8_1_reduce.out &
sleep 11000
nohup python -u main.py --student_n 540 --exer_n 598 --knowledge_n 46 --gpu 0 --epoch_n 50 --mode 0 --edge_emb --log KT_edge_1_reduce > result/KT_edge_1_reduce.out &
nohup python -u main.py --student_n 540 --exer_n 598 --knowledge_n 46 --gpu 1 --epoch_n 50 --mode 1 --lamb 0.1 --edge_emb --log KTOT_0.1_edge_1_reduce > result/KTOT_0.1_edge_1_reduce.out &
nohup python -u main.py --student_n 540 --exer_n 598 --knowledge_n 46 --gpu 2 --epoch_n 50 --mode 2 --edge_emb --log OT_edge_1_reduce > result/OT_edge_1_reduce.out &
sleep 12000
nohup python -u main.py --student_n 540 --exer_n 598 --knowledge_n 46 --gpu 0 --epoch_n 50 --mode 1 --lamb 0.2 --edge_emb --log KTOT_0.2_edge_1_reduce > result/KTOT_0.2_edge_1_reduce.out &
nohup python -u main.py --student_n 540 --exer_n 598 --knowledge_n 46 --gpu 1 --epoch_n 50 --mode 1 --lamb 0.5 --edge_emb --log KTOT_0.5_edge_1_reduce > result/KTOT_0.5_edge_1_reduce.out &
nohup python -u main.py --student_n 540 --exer_n 598 --knowledge_n 46 --gpu 2 --epoch_n 50 --mode 1 --lamb 0.8 --edge_emb --log KTOT_0.8_edge_1_reduce > result/KTOT_0.8_edge_1_reduce.out &
