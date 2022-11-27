cd ..
#cp config_riiid.txt config.txt
#
#python build_k_e_graph.py --dir ../data/riiid/
#python build_u_e_graph.py --dir ../data/riiid/

python -u main.py --student_n 500 --exer_n 976 --knowledge_n 57 --dir ../data/riiid/ --gpu 1 --epoch_n 50 --mode 0 --edge_emb --edge_type 1 --log riiid_KT_edge_1
sleep 10

python -u main.py --student_n 500 --exer_n 976 --knowledge_n 57 --dir ../data/riiid/ --gpu 1 --epoch_n 50 --mode 1 --lamb 0.2 --edge_emb --edge_type 1 --log riiid_KTOT_0.2_edge_1
sleep 10

python -u main.py --student_n 500 --exer_n 976 --knowledge_n 57 --dir ../data/riiid/ --gpu 1 --epoch_n 50 --mode 1 --lamb 0.8 --edge_emb --edge_type 1 --log riiid_KTOT_0.8_edge_1
sleep 10

python -u main.py --student_n 500 --exer_n 976 --knowledge_n 57 --dir ../data/riiid/ --gpu 1 --epoch_n 50 --mode 2 --edge_emb --edge_type 1 --log riiid_OT_edge_1
sleep 10

python -u main.py --student_n 500 --exer_n 976 --knowledge_n 57 --dir ../data/riiid/ --gpu 1 --epoch_n 50 --mode 1 --lamb 0.2 --log riiid_KTOT_0.2
