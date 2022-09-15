python test.py --gpu 0 --mode 0 --log KT_1_reduce_shuffle
python test.py --gpu 0 --mode 0 --log KT_edge_1_reduce_shuffle
sleep 5
python test.py --gpu 2 --mode 1 --log KTOT_0.8_1_reduce_shuffle
python test.py --gpu 2 --mode 1 --log KTOT_0.8_edge_1_reduce_shuffle
sleep 5
python test.py --gpu 1 --mode 1 --log KTOT_0.5_1_reduce_shuffle
python test.py --gpu 1 --mode 1 --log KTOT_0.5_edge_1_reduce_shuffle
sleep 5
python test.py --gpu 0 --mode 1 --log KTOT_0.2_1_reduce_shuffle
python test.py --gpu 0 --mode 1 --log KTOT_0.2_edge_1_reduce_shuffle
sleep 5
python test.py --gpu 1 --mode 1 --log KTOT_0.1_1_reduce_shuffle
python test.py --gpu 1 --mode 1 --log KTOT_0.1_edge_1_reduce_shuffle
sleep 5
python test.py --gpu 2 --mode 2 --log OT_1_reduce_shuffle
python test.py --gpu 2 --mode 2 --log OT_edge_1_reduce_shuffle