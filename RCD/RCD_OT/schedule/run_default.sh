cd ..
cp config_full.txt config.txt
cp ../data/poly/log_data_default.json ../data/poly/log_data.json
cp ../data/poly/train_set_default.json ../data/poly/train_set.json
cp ../data/poly/valid_set_default.json ../data/poly/valid_set.json
cp ../data/poly/test_set_default.json ../data/poly/test_set.json

python build_k_e_graph.py
python build_u_e_graph.py

nohup python -u main.py --gpu 0 --epoch_n 50 --mode 0 --log KT > /dev/null &
nohup python -u main.py --gpu 1 --epoch_n 50 --mode 1 --lamb 0.1 --log KTOT_0.1 > /dev/null &
python -u main.py --gpu 2 --epoch_n 50 --mode 1 --lamb 0.2 --log KTOT_0.2
sleep 10

nohup python -u main.py --gpu 0 --epoch_n 50 --mode 1 --lamb 0.5 --log KTOT_0.5 > /dev/null &
nohup python -u main.py --gpu 1 --epoch_n 50 --mode 1 --lamb 0.8 --log KTOT_0.8 > /dev/null &
python -u main.py --gpu 2 --epoch_n 50 --mode 2 --log OT
sleep 10

nohup python -u main.py --gpu 0 --epoch_n 50 --mode 0 --edge_emb --edge_type 0 --log KT_edge_0 > /dev/null &
nohup python -u main.py --gpu 1 --epoch_n 50 --mode 0 --edge_emb --edge_type 1 --log KT_edge_1 > /dev/null &
python -u main.py --gpu 2 --epoch_n 50 --mode 0 --edge_emb --edge_type 2 --log KT_edge_2
sleep 10

nohup python -u main.py --gpu 0 --epoch_n 50 --mode 1 --lamb 0.1 --edge_emb --edge_type 0 --log KTOT_0.1_edge_0 > /dev/null &
nohup python -u main.py --gpu 1 --epoch_n 50 --mode 1 --lamb 0.1 --edge_emb --edge_type 1 --log KTOT_0.1_edge_1 > /dev/null &
python -u main.py --gpu 2 --epoch_n 50 --mode 1 --lamb 0.1 --edge_emb --edge_type 2 --log KTOT_0.1_edge_2
sleep 10

nohup python -u main.py --gpu 0 --epoch_n 50 --mode 1 --lamb 0.2 --edge_emb --edge_type 0 --log KTOT_0.2_edge_0 > /dev/null &
nohup python -u main.py --gpu 1 --epoch_n 50 --mode 1 --lamb 0.2 --edge_emb --edge_type 1 --log KTOT_0.2_edge_1 > /dev/null &
python -u main.py --gpu 2 --epoch_n 50 --mode 1 --lamb 0.2 --edge_emb --edge_type 2 --log KTOT_0.2_edge_2
sleep 10

nohup python -u main.py --gpu 0 --epoch_n 50 --mode 1 --lamb 0.5 --edge_emb --edge_type 0 --log KTOT_0.5_edge_0 > /dev/null &
nohup python -u main.py --gpu 1 --epoch_n 50 --mode 1 --lamb 0.5 --edge_emb --edge_type 1 --log KTOT_0.5_edge_1 > /dev/null &
python -u main.py --gpu 2 --epoch_n 50 --mode 1 --lamb 0.5 --edge_emb --edge_type 2 --log KTOT_0.5_edge_2
sleep 10

nohup python -u main.py --gpu 0 --epoch_n 50 --mode 1 --lamb 0.8 --edge_emb --edge_type 0 --log KTOT_0.8_edge_0 > /dev/null &
nohup python -u main.py --gpu 1 --epoch_n 50 --mode 1 --lamb 0.8 --edge_emb --edge_type 1 --log KTOT_0.8_edge_1 > /dev/null &
python -u main.py --gpu 2 --epoch_n 50 --mode 1 --lamb 0.8 --edge_emb --edge_type 2 --log KTOT_0.8_edge_2
sleep 10

nohup python -u main.py --gpu 0 --epoch_n 50 --mode 2 --edge_emb --edge_type 0 --log OT_edge_0 > /dev/null &
nohup python -u main.py --gpu 1 --epoch_n 50 --mode 2 --edge_emb --edge_type 1 --log OT_edge_1 > /dev/null &
python -u main.py --gpu 2 --epoch_n 50 --mode 2 --edge_emb --edge_type 2 --log OT_edge_2
