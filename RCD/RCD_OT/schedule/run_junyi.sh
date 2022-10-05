cd ..
cp config_junyi.txt config.txt
cp ../data/junyi/log_data_ori.json ../data/junyi/log_data.json
cp ../data/junyi/train_set_ori.json ../data/junyi/train_set.json
cp ../data/junyi/valid_set_ori.json ../data/junyi/valid_set.json
cp ../data/junyi/test_set_ori.json ../data/junyi/test_set.json

cp ../data/junyi/graph/K_Directed_ori.txt ../data/junyi/graph/K_Directed.txt
cp ../data/junyi/graph/K_Undirected_ori.txt ../data/junyi/graph/K_Undirected.txt

python build_k_e_graph.py --dir ../data/junyi/
python build_u_e_graph.py --dir ../data/junyi/

nohup python -u main.py --student_n 10000 --exer_n 835 --knowledge_n 835 --dir ../data/junyi/ --gpu 0 --epoch_n 20 --mode 0 --log junyi_full_1 > /dev/null &
nohup python -u main.py --student_n 10000 --exer_n 835 --knowledge_n 835 --dir ../data/junyi/ --gpu 1 --epoch_n 20 --mode 0 --log junyi_full_2 > /dev/null &
nohup python -u main.py --student_n 10000 --exer_n 835 --knowledge_n 835 --dir ../data/junyi/ --gpu 2 --epoch_n 20 --mode 0 --log junyi_full_3 > /dev/null &
sleep 10

cp ../data/junyi/graph/K_Directed_no.txt ../data/junyi/graph/K_Directed.txt
cp ../data/junyi/graph/K_Undirected_no.txt ../data/junyi/graph/K_Undirected.txt

python build_k_e_graph.py --dir ../data/junyi/
python build_u_e_graph.py --dir ../data/junyi/

nohup python -u main.py --student_n 10000 --exer_n 835 --knowledge_n 835 --dir ../data/junyi/ --gpu 0 --epoch_n 20 --mode 0 --log junyi_no_dep_1 > /dev/null &
nohup python -u main.py --student_n 10000 --exer_n 835 --knowledge_n 835 --dir ../data/junyi/ --gpu 1 --epoch_n 20 --mode 0 --log junyi_no_dep_2 > /dev/null &
nohup python -u main.py --student_n 10000 --exer_n 835 --knowledge_n 835 --dir ../data/junyi/ --gpu 2 --epoch_n 20 --mode 0 --log junyi_no_dep_3 > /dev/null &
sleep 10

cp config_junyi_0.txt config.txt
cp ../data/junyi_0/log_data_0.json ../data/junyi_0/log_data.json
cp ../data/junyi_0/train_set_0.json ../data/junyi_0/train_set.json
cp ../data/junyi_0/valid_set_0.json ../data/junyi_0/valid_set.json
cp ../data/junyi_0/test_set_0.json ../data/junyi_0/test_set.json

cp ../data/junyi_0/graph/K_Directed_no.txt ../data/junyi_0/graph/K_Directed.txt
cp ../data/junyi_0/graph/K_Undirected_no.txt ../data/junyi_0/graph/K_Undirected.txt

python build_k_e_graph.py --dir ../data/junyi_0/
python build_u_e_graph.py --dir ../data/junyi_0/

nohup python -u main.py --student_n 10000 --exer_n 835 --knowledge_n 1 --dir ../data/junyi_0/ --gpu 0 --epoch_n 20 --mode 0 --log junyi_no_con_1 > /dev/null &
nohup python -u main.py --student_n 10000 --exer_n 835 --knowledge_n 1 --dir ../data/junyi_0/ --gpu 1 --epoch_n 20 --mode 0 --log junyi_no_con_2 > /dev/null &
nohup python -u main.py --student_n 10000 --exer_n 835 --knowledge_n 1 --dir ../data/junyi_0/ --gpu 2 --epoch_n 20 --mode 0 --log junyi_no_con_3 > /dev/null &
sleep 10