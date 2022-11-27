cd ..
cp config_riiid.txt config.txt

python build_k_e_graph.py --dir ../data/riiid/
python build_u_e_graph.py --dir ../data/riiid/

nohup python -u test.py --dir ../data/riiid/ --gpu 0 --mode 0 --log riiid_KT_edge_0 > /dev/null &
nohup python -u test.py --dir ../data/riiid/ --gpu 1 --mode 0 --log riiid_KT_edge_1 > /dev/null &
python -u test.py --dir ../data/riiid/ --gpu 2 --mode 0 --log riiid_KT_edge_2
sleep 5

nohup python -u test.py --dir ../data/riiid/ --gpu 0 --mode 1 --log riiid_KTOT_0.2_edge_0 > /dev/null &
nohup python -u test.py --dir ../data/riiid/ --gpu 1 --mode 1 --log riiid_KTOT_0.2_edge_1 > /dev/null &
python -u test.py --dir ../data/riiid/ --gpu 2 --mode 1 --log riiid_KTOT_0.2_edge_2
sleep 5

nohup python -u test.py --dir ../data/riiid/ --gpu 0 --mode 1 --log riiid_KTOT_0.8_edge_0 > /dev/null &
nohup python -u test.py --dir ../data/riiid/ --gpu 1 --mode 1 --log riiid_KTOT_0.8_edge_1 > /dev/null &
python -u test.py --dir ../data/riiid/ --gpu 2 --mode 1 --log riiid_KTOT_0.8_edge_2
sleep 5

nohup python -u test.py --dir ../data/riiid/ --gpu 0 --mode 2 --log riiid_OT_edge_0 > /dev/null &
nohup python -u test.py --dir ../data/riiid/ --gpu 1 --mode 2 --log riiid_OT_edge_1 > /dev/null &
python -u test.py --dir ../data/riiid/ --gpu 2 --mode 2 --log riiid_OT_edge_2
sleep 5

nohup python -u test.py --dir ../data/riiid/ --gpu 0 --mode 0 --log riiid_KT > /dev/null &
nohup python -u test.py --dir ../data/riiid/ --gpu 1 --mode 1 --log riiid_KTOT_0.2 > /dev/null &
python -u test.py --dir ../data/riiid/ --gpu 2 --mode 1 --log riiid_KTOT_0.8
sleep 5

python -u test.py --dir ../data/riiid/ --gpu 0 --mode 2 --log riiid_OT