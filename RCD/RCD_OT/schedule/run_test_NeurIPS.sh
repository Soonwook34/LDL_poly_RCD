cd ..
cp config_NeurIPS.txt config.txt

python build_k_e_graph.py --dir ../data/NeurIPS/
python build_u_e_graph.py --dir ../data/NeurIPS/

nohup python -u test.py --dir ../data/NeurIPS/ --gpu 0 --mode 0 --log NeurIPS_KT_edge_0 > /dev/null &
nohup python -u test.py --dir ../data/NeurIPS/ --gpu 1 --mode 0 --log NeurIPS_KT_edge_1 > /dev/null &
python -u test.py --dir ../data/NeurIPS/ --gpu 2 --mode 0 --log NeurIPS_KT_edge_2
sleep 5

nohup python -u test.py --dir ../data/NeurIPS/ --gpu 0 --mode 1 --log NeurIPS_KTOT_0.2_edge_0 > /dev/null &
nohup python -u test.py --dir ../data/NeurIPS/ --gpu 1 --mode 1 --log NeurIPS_KTOT_0.2_edge_1 > /dev/null &
python -u test.py --dir ../data/NeurIPS/ --gpu 2 --mode 1 --log NeurIPS_KTOT_0.2_edge_2
sleep 5

nohup python -u test.py --dir ../data/NeurIPS/ --gpu 0 --mode 1 --log NeurIPS_KTOT_0.8_edge_0 > /dev/null &
nohup python -u test.py --dir ../data/NeurIPS/ --gpu 1 --mode 1 --log NeurIPS_KTOT_0.8_edge_1 > /dev/null &
python -u test.py --dir ../data/NeurIPS/ --gpu 2 --mode 1 --log NeurIPS_KTOT_0.8_edge_2
sleep 5

nohup python -u test.py --dir ../data/NeurIPS/ --gpu 0 --mode 2 --log NeurIPS_OT_edge_0 > /dev/null &
nohup python -u test.py --dir ../data/NeurIPS/ --gpu 1 --mode 2 --log NeurIPS_OT_edge_1 > /dev/null &
python -u test.py --dir ../data/NeurIPS/ --gpu 2 --mode 2 --log NeurIPS_OT_edge_2
sleep 5

nohup python -u test.py --dir ../data/NeurIPS/ --gpu 0 --mode 0 --log NeurIPS_KT > /dev/null &
nohup python -u test.py --dir ../data/NeurIPS/ --gpu 1 --mode 1 --log NeurIPS_KTOT_0.2 > /dev/null &
python -u test.py --dir ../data/NeurIPS/ --gpu 2 --mode 1 --log NeurIPS_KTOT_0.8
sleep 5

python -u test.py --dir ../data/NeurIPS/ --gpu 0 --mode 2 --log NeurIPS_OT