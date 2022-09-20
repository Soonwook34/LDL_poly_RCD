cd ../
cp config_full.txt config.txt
cp ../data/poly/log_data_shuffle.json ../data/poly/log_data.json
cp ../data/poly/train_set_shuffle.json ../data/poly/train_set.json
cp ../data/poly/valid_set_shuffle.json ../data/poly/valid_set.json
cp ../data/poly/test_set_shuffle.json ../data/poly/test_set.json

python build_k_e_graph.py
python build_u_e_graph.py

nohup python -u test.py --gpu 0 --mode 0 --log KT_shuffle > /dev/null &
nohup python -u test.py --gpu 1 --mode 1 --log KTOT_0.1_shuffle > /dev/null &
python -u test.py --gpu 2 --mode 1 --log KTOT_0.2_shuffle
sleep 5

nohup python -u test.py --gpu 0 --mode 1 --log KTOT_0.5_shuffle > /dev/null &
nohup python -u test.py --gpu 1 --mode 1 --log KTOT_0.8_shuffle > /dev/null &
python -u test.py --gpu 2 --mode 2 --log OT_shuffle
sleep 5

nohup python -u test.py --gpu 0 --mode 0 --log KT_edge_0_shuffle > /dev/null &
nohup python -u test.py --gpu 1 --mode 0 --log KT_edge_1_shuffle > /dev/null &
python -u test.py --gpu 2 --mode 0 --log KT_edge_2_shuffle
sleep 5

nohup python -u test.py --gpu 0 --mode 1 --log KTOT_0.1_edge_0_shuffle > /dev/null &
nohup python -u test.py --gpu 1 --mode 1 --log KTOT_0.1_edge_1_shuffle > /dev/null &
python -u test.py --gpu 2 --mode 1 --log KTOT_0.1_edge_2_shuffle
sleep 5

nohup python -u test.py --gpu 0 --mode 1 --log KTOT_0.2_edge_0_shuffle > /dev/null &
nohup python -u test.py --gpu 1 --mode 1 --log KTOT_0.2_edge_1_shuffle > /dev/null &
python -u test.py --gpu 2 --mode 1 --log KTOT_0.2_edge_2_shuffle
sleep 5

nohup python -u test.py --gpu 0 --mode 1 --log KTOT_0.5_edge_0_shuffle > /dev/null &
nohup python -u test.py --gpu 1 --mode 1 --log KTOT_0.5_edge_1_shuffle > /dev/null &
python -u test.py --gpu 2 --mode 1 --log KTOT_0.5_edge_2_shuffle
sleep 5

nohup python -u test.py --gpu 0 --mode 1 --log KTOT_0.8_edge_0_shuffle > /dev/null &
nohup python -u test.py --gpu 1 --mode 1 --log KTOT_0.8_edge_1_shuffle > /dev/null &
python -u test.py --gpu 2 --mode 1 --log KTOT_0.8_edge_2_shuffle
sleep 5

nohup python -u test.py --gpu 0 --mode 2 --log OT_edge_0_shuffle > /dev/null &
nohup python -u test.py --gpu 1 --mode 2 --log OT_edge_1_shuffle > /dev/null &
python -u test.py --gpu 2 --mode 2 --log OT_edge_2_shuffle