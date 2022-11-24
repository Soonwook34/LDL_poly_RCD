cd ..
#cp config_NeurIPS.txt config.txt
#
#python build_k_e_graph.py --dir ../data/NeurIPS/
#python build_u_e_graph.py --dir ../data/NeurIPS/
#
#python -u main.py --student_n 500 --exer_n 948 --knowledge_n 300 --dir ../data/NeurIPS/ --gpu 1 --epoch_n 50 --mode 0 --edge_emb --edge_type 1 --log NeurIPS_KT_edge_1
#sleep 10

python -u main.py --student_n 500 --exer_n 948 --knowledge_n 300 --dir ../data/NeurIPS/ --gpu 1 --epoch_n 50 --mode 1 --lamb 0.2 --edge_emb --edge_type 1 --log NeurIPS_KTOT_0.2_edge_1
sleep 10

python -u main.py --student_n 500 --exer_n 948 --knowledge_n 300 --dir ../data/NeurIPS/ --gpu 1 --epoch_n 50 --mode 1 --lamb 0.8 --edge_emb --edge_type 1 --log NeurIPS_KTOT_0.8_edge_1
sleep 10

python -u main.py --student_n 500 --exer_n 948 --knowledge_n 300 --dir ../data/NeurIPS/ --gpu 1 --epoch_n 50 --mode 2 --edge_emb --edge_type 1 --log NeurIPS_OT_edge_1
sleep 10

python -u main.py --student_n 500 --exer_n 948 --knowledge_n 300 --dir ../data/NeurIPS/ --gpu 1 --epoch_n 50 --mode 1 --lamb 0.2 --log NeurIPS_KTOT_0.2