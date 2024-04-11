import os
import json
import docx
import torch
import logging
import datetime
from torch.nn import Module
from typing import Dict, Tuple, Union, Optional
from transformers import AutoConfig, AutoModel, AutoTokenizer
torch.backends.cudnn.benchmark = True

logging.basicConfig(
    level=logging.INFO,
     format='%(asctime)s %(levelname)-8s %(module)s[line:%(lineno)d]: >> %(message)s',
     datefmt='%Y-%m-%d %H:%M:%S'
     )

DEVICE = "cuda"
DEVICE_ID = "0"
CUDA_DEVICE = f"{DEVICE}:{DEVICE_ID}" if DEVICE_ID else DEVICE


def auto_configure_device_map(num_gpus: int) -> Dict[str, int]:

    num_trans_layers = 28
    per_gpu_layers = 30 / num_gpus

    device_map = {
        'transformer.embedding.word_embeddings': 0,
        'transformer.encoder.final_layernorm': 0,
        'transformer.output_layer': 0,
        'transformer.rotary_pos_emb': 0,
        'lm_head': 0,
        'transformer.prefix_encoder.embedding':0
    }

    used = 2
    gpu_target = 0
    for i in range(num_trans_layers):
        if used >= per_gpu_layers:
            gpu_target += 1
            used = 0
        assert gpu_target < num_gpus
        device_map[f'transformer.encoder.layers.{i}'] = gpu_target
        used += 1

    return device_map


def load_model_on_gpus(checkpoint_path: Union[str, os.PathLike], num_gpus: int = 2,
                       device_map: Optional[Dict[str, int]] = None, **kwargs) -> Module:
    if num_gpus < 2 and device_map is None:
        model = AutoModel.from_pretrained(checkpoint_path,  trust_remote_code=True, **kwargs).half().cuda()

    else:
        from accelerate import dispatch_model


        model = AutoModel.from_pretrained(checkpoint_path,  trust_remote_code=True, **kwargs).half()
        prefix_state_dict = torch.load(os.path.join('/data2/fyj2023/project/ChatGLM2-6B/ptuning/output/gov1000_index_rawData20240319_1748/adgen-chatglm2-6b-32k-pt-128-2e-2/checkpoint-600/', "pytorch_model.bin"))
        new_prefix_state_dict = {}
        for k, v in prefix_state_dict.items():
            if k.startswith("transformer.prefix_encoder."):
                new_prefix_state_dict[k[len("transformer.prefix_encoder."):]] = v
        model.transformer.prefix_encoder.load_state_dict(new_prefix_state_dict)

        # model = model.quantize(4)
        # model = model.cuda()
        # model.transformer.prefix_encoder.float()

        if device_map is None:
            device_map = auto_configure_device_map(num_gpus)

        model = dispatch_model(model, device_map=device_map)

    return model
model_path = "/data2/fyj2023/pretrained_model/chatglm2-6b-32k"
checkpoint_path = "/data2/fyj2023/project/ChatGLM2-6B/ptuning/output/gov1000_index_rawData20240319_1748/adgen-chatglm2-6b-32k-pt-128-2e-2/checkpoint-600"
#checkpoint_path = "/data/xf2022/projects/ChatGLM2-6B/ptuning/output/network_center20230914_2252/adgen-chatglm2-6b-32k-pt-128-1e-2/checkpoint-1350"
# 载入Tokenizer
torch.cuda.set_device(0)
ava_gpu = torch.cuda.current_device()
logging.info(f"gpuInfo:{ava_gpu}")
tokenizer = AutoTokenizer.from_pretrained(model_path, trust_remote_code=True)

# 加载ptuning模型
config = AutoConfig.from_pretrained(model_path, trust_remote_code=True, pre_seq_len=128)
model = AutoModel.from_pretrained(model_path, config=config, trust_remote_code=True)
#model = load_model_on_gpus(model_path, num_gpus=4, config=config)
prefix_state_dict = torch.load(os.path.join(checkpoint_path, "pytorch_model.bin"))
new_prefix_state_dict = {}
for k, v in prefix_state_dict.items():
    if k.startswith("transformer.prefix_encoder."):
        new_prefix_state_dict[k[len("transformer.prefix_encoder."):]] = v
model.transformer.prefix_encoder.load_state_dict(new_prefix_state_dict)




# Comment out the following line if you don't use quantization
model = model.quantize(4)
model = model.cuda(0)
model = model.eval()
#model.cuda(3)

data_list = []
data_path = '/data2/fyj2023/project/ChatGLM2-6B/ptuning/data/government_procurement/data_index/test.json'
with open(data_path, 'r') as fr:
    for line in fr.readlines():
        data = eval(line)
        data_list.append(data)

result_path = '/data2/fyj2023/project/ChatGLM2-6B/ptuning/output/gov1000_index_rawData20240319_1748/result/result_600.txt'
#with open(result_path, 'w', encoding='utf-8') as fw:
#    for i, data in enumerate(data_list):
#        if i % 10 == 0:
#            logging.info(i)
#        response, history = model.chat(tokenizer, data['input'], history=[], temperature=0.05)
#         result_dir= {}
#        result_dir["labels"] = data['output']
#        result_dir["predict"] = str(response)

with open(result_path, 'w', encoding='utf-8') as fw:
    for i, data in enumerate(data_list):
        #if i % 10 == 0:
        logging.info(i)


       # response, history = model.chat(tokenizer, data['input'], history=[], temperature=0.05)
        response, history = model.chat(tokenizer,
                                   data['input'],
                                   history=[],
                                   max_length=2048,
                                   top_p= 0.7,
                                   temperature= 0.95)
        result_dir= {}
        result_dir["labels"] = data['output']
        result_dir["predict"] = str(response)
        fw.write(str(result_dir)+'\n')

logging.info(f"model path:{model_path}")
logging.info(f"checkpoint path:{checkpoint_path}")
logging.info(f"data path:{data_path}")
logging.info(f"result path:{result_path}")


