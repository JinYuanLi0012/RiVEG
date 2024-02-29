#!/usr/bin/env bash

# The port for communication. Note that if you want to run multiple tasks on the same machine,
# you need to specify different port numbers.
export MASTER_PORT=6081
export PYTHONPATH=$PYTHONPATH:.../OFA/fairseq


user_dir=../../ofa_module
bpe_dir=../../utils/BPE
selected_cols=0,4,2,3


########################## Evaluate##########################
data=../../dataset/refcoco_data/twitter10000REC_addent_test_pred.tsv
path=.../OFA/run_scripts/refcoco/twitter10000REC_large_checkpoints/your checkpoint
result_path=../../results/twitter10000REC/OFAlargeVE_OFAlargeREC_pred
split='refcoco_val'
CUDA_VISIBLE_DEVICES=0 python3 -m torch.distributed.launch --nproc_per_node=1 --use_env --master_port=${MASTER_PORT} ../../evaluate.py \
    ${data} \
    --path=${path} \
    --user-dir=${user_dir} \
    --task=refcoco \
    --batch-size=32 \
    --log-format=simple --log-interval=10 \
    --seed=7 \
    --gen-subset=${split} \
    --results-path=${result_path} \
    --beam=5 \
    --min-len=4 \
    --max-len-a=0 \
    --max-len-b=4 \
    --no-repeat-ngram-size=3 \
    --fp16 \
    --num-workers=0 \
    --model-overrides="{\"data\":\"${data}\",\"bpe_dir\":\"${bpe_dir}\",\"selected_cols\":\"${selected_cols}\"}"
