export CUDA_VISIBLE_DEVICES="1,2,3,4"
PRE_SEQ_LEN=128
LR=2e-2
NUM_GPUS=4

nohup torchrun --standalone --nnodes=1 --nproc-per-node=$NUM_GPUS main.py \
    --do_train \
    --train_file /data2/fyj2023/project/ChatGLM2-6B/ptuning/data/government_procurement/data_sci/train.json \
    --validation_file /data2/fyj2023/project/ChatGLM2-6B/ptuning/data/government_procurement/data_sci/dev.json \
    --preprocessing_num_workers 10 \
    --prompt_column input \
    --response_column output \
    --overwrite_cache \
    --model_name_or_path /data2/fyj2023/pretrained_model/chatglm2-6b-32k \
    --ptuning_checkpoint /data2/fyj2023/project/ChatGLM2-6B/ptuning/output/gov1000_3_rawData20230828_1824/adgen-chatglm2-6b-32k-pt-128-2e-2/checkpoint-500 \
    --output_dir output/scire_rawData$(date +%Y%m%d_%H%M)/adgen-chatglm2-6b-32k-pt-$PRE_SEQ_LEN-$LR \
    --overwrite_output_dir \
    --max_source_length 500 \
    --max_target_length 256 \
    --per_device_train_batch_size 1 \
    --per_device_eval_batch_size 1 \
    --gradient_accumulation_steps 16 \
    --predict_with_generate \
    --max_steps 1000 \
    --logging_steps 10 \
    --save_steps 50 \
    --learning_rate $LR \
    --pre_seq_len $PRE_SEQ_LEN \
    --quantization_bit 4 \
    >>./log/$(date +%Y%m%d_%H%M).log 2>&1 &


# 下面给出的文本是政府采购招标项目的公告内容，请从中提取出特定字段，并以json的格式返回，具体的格式如：{项目编号:__, 代理机构:__, 采购方式:__, 采购单位:__, 采购单位联系地址:__, 采购单位联系电话:__, 采购单位联系人姓名:__, 所属地区:__, 总预算:__, 报名开始日期:__, 报名结束日期:__}。请按照以下要求提取字段： 1、只能从原文中提取字段值，没找到的为null； 2、所属地区为项目的地区或采购单位所在地区； 3、报名结束时间是获取采购文件截止时间；

