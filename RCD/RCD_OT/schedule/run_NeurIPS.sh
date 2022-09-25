cd ..
cp config_NeurIPS.txt config.txt

python build_k_e_graph.py --dir ../data/NeurIPS/
python build_u_e_graph.py --dir ../data/NeurIPS/

nohup python -u main.py --student_n 4918 --exer_n 948 --knowledge_n 388 --dir ../data/NeurIPS/ --gpu 0 --epoch_n 50 --mode 0 --log NeurIPSgen1_KT > /dev/null &
nohup python -u main.py --student_n 4918 --exer_n 948 --knowledge_n 388 --dir ../data/NeurIPS/ --gpu 1 --epoch_n 50 --mode 1 --lamb 0.1 --log NeurIPS_KTOT_0.1 > /dev/null &
python -u main.py --student_n 4918 --exer_n 948 --knowledge_n 388 --dir ../data/NeurIPS/ --gpu 2 --epoch_n 50 --mode 1 --lamb 0.2 --log NeurIPS_KTOT_0.2
sleep 10

nohup python -u main.py --student_n 4918 --exer_n 948 --knowledge_n 388 --dir ../data/NeurIPS/ --gpu 0 --epoch_n 50 --mode 1 --lamb 0.5 --log NeurIPS_KTOT_0.5 > /dev/null &
nohup python -u main.py --student_n 4918 --exer_n 948 --knowledge_n 388 --dir ../data/NeurIPS/ --gpu 1 --epoch_n 50 --mode 1 --lamb 0.8 --log NeurIPS_KTOT_0.8 > /dev/null &
python -u main.py --student_n 4918 --exer_n 948 --knowledge_n 388 --dir ../data/NeurIPS/ --gpu 2 --epoch_n 50 --mode 2 --log NeurIPSgen1_OT
sleep 10

nohup python -u main.py --student_n 4918 --exer_n 948 --knowledge_n 388 --dir ../data/NeurIPS/ --gpu 0 --epoch_n 50 --mode 0 --edge_emb --edge_type 0 --log NeurIPS_edge_0 > /dev/null &
nohup python -u main.py --student_n 4918 --exer_n 948 --knowledge_n 388 --dir ../data/NeurIPS/ --gpu 1 --epoch_n 50 --mode 0 --edge_emb --edge_type 1 --log NeurIPS_edge_1 > /dev/null &
python -u main.py --student_n 4918 --exer_n 948 --knowledge_n 388 --dir ../data/NeurIPS/ --gpu 2 --epoch_n 50 --mode 0 --edge_emb --edge_type 2 --log NeurIPS_edge_2
sleep 10

nohup python -u main.py --student_n 4918 --exer_n 948 --knowledge_n 388 --dir ../data/NeurIPS/ --gpu 0 --epoch_n 50 --mode 1 --lamb 0.1 --edge_emb --edge_type 0 --log NeurIPS_KTOT_0.1_edge_0 > /dev/null &
nohup python -u main.py --student_n 4918 --exer_n 948 --knowledge_n 388 --dir ../data/NeurIPS/ --gpu 1 --epoch_n 50 --mode 1 --lamb 0.1 --edge_emb --edge_type 1 --log NeurIPS_KTOT_0.1_edge_1 > /dev/null &
python -u main.py --student_n 4918 --exer_n 948 --knowledge_n 388 --dir ../data/NeurIPS/ --gpu 2 --epoch_n 50 --mode 1 --lamb 0.1 --edge_emb --edge_type 2 --log NeurIPS_KTOT_0.1_edge_2
sleep 10

nohup python -u main.py --student_n 4918 --exer_n 948 --knowledge_n 388 --dir ../data/NeurIPS/ --gpu 0 --epoch_n 50 --mode 1 --lamb 0.2 --edge_emb --edge_type 0 --log NeurIPS_KTOT_0.2_edge_0 > /dev/null &
nohup python -u main.py --student_n 4918 --exer_n 948 --knowledge_n 388 --dir ../data/NeurIPS/ --gpu 1 --epoch_n 50 --mode 1 --lamb 0.2 --edge_emb --edge_type 1 --log NeurIPS_KTOT_0.2_edge_1 > /dev/null &
python -u main.py --student_n 4918 --exer_n 948 --knowledge_n 388 --dir ../data/NeurIPS/ --gpu 2 --epoch_n 50 --mode 1 --lamb 0.2 --edge_emb --edge_type 2 --log NeurIPS_KTOT_0.2_edge_2
sleep 10

nohup python -u main.py --student_n 4918 --exer_n 948 --knowledge_n 388 --dir ../data/NeurIPS/ --gpu 0 --epoch_n 50 --mode 1 --lamb 0.5 --edge_emb --edge_type 0 --log NeurIPS_KTOT_0.5_edge_0 > /dev/null &
nohup python -u main.py --student_n 4918 --exer_n 948 --knowledge_n 388 --dir ../data/NeurIPS/ --gpu 1 --epoch_n 50 --mode 1 --lamb 0.5 --edge_emb --edge_type 1 --log NeurIPS_KTOT_0.5_edge_1 > /dev/null &
python -u main.py --student_n 4918 --exer_n 948 --knowledge_n 388 --dir ../data/NeurIPS/ --gpu 2 --epoch_n 50 --mode 1 --lamb 0.5 --edge_emb --edge_type 2 --log NeurIPS_KTOT_0.5_edge_2
sleep 10

nohup python -u main.py --student_n 4918 --exer_n 948 --knowledge_n 388 --dir ../data/NeurIPS/ --gpu 0 --epoch_n 50 --mode 1 --lamb 0.8 --edge_emb --edge_type 0 --log NeurIPS_KTOT_0.8_edge_0 > /dev/null &
nohup python -u main.py --student_n 4918 --exer_n 948 --knowledge_n 388 --dir ../data/NeurIPS/ --gpu 1 --epoch_n 50 --mode 1 --lamb 0.8 --edge_emb --edge_type 1 --log NeurIPS_KTOT_0.8_edge_1 > /dev/null &
python -u main.py --student_n 4918 --exer_n 948 --knowledge_n 388 --dir ../data/NeurIPS/ --gpu 2 --epoch_n 50 --mode 1 --lamb 0.8 --edge_emb --edge_type 2 --log NeurIPS_KTOT_0.8_edge_2
sleep 10

nohup python -u main.py --student_n 4918 --exer_n 948 --knowledge_n 388 --dir ../data/NeurIPS/ --gpu 0 --epoch_n 50 --mode 2 --edge_emb --edge_type 0 --log NeurIPS_edge_0 > /dev/null &
nohup python -u main.py --student_n 4918 --exer_n 948 --knowledge_n 388 --dir ../data/NeurIPS/ --gpu 1 --epoch_n 50 --mode 2 --edge_emb --edge_type 1 --log NeurIPS_edge_1 > /dev/null &
python -u main.py --student_n 4918 --exer_n 948 --knowledge_n 388 --dir ../data/NeurIPS/ --gpu 2 --epoch_n 50 --mode 2 --edge_emb --edge_type 2 --log NeurIPS_edge_2
