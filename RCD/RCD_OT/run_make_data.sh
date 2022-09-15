cd ../data/poly/
python make_log_data_default.py

cd ../../RCD_OT/
cp ../data/poly/log_data.json ../data/poly/log_data_default.json
python divide_data_valid.py
cp ../data/poly/train_set.json ../data/poly/train_set_default.json
cp ../data/poly/valid_set.json ../data/poly/valid_set_default.json
cp ../data/poly/test_set.json ../data/poly/test_set_default.json
python divide_data_valid.py --shuffle
cp ../data/poly/train_set.json ../data/poly/train_set_shuffle.json
cp ../data/poly/valid_set.json ../data/poly/valid_set_shuffle.json
cp ../data/poly/test_set.json ../data/poly/test_set_shuffle.json

cd ../data/poly/
python make_log_data_reduce.py

cd ../../RCD_OT/
cp ../data/poly/log_data.json ../data/poly/log_data_reduce.json
python divide_data_valid.py
cp ../data/poly/train_set.json ../data/poly/train_set_reduce.json
cp ../data/poly/valid_set.json ../data/poly/valid_set_reduce.json
cp ../data/poly/test_set.json ../data/poly/test_set_reduce.json
python divide_data_valid.py --shuffle
cp ../data/poly/train_set.json ../data/poly/train_set_reduce_shuffle.json
cp ../data/poly/valid_set.json ../data/poly/valid_set_reduce_shuffle.json
cp ../data/poly/test_set.json ../data/poly/test_set_reduce_shuffle.json