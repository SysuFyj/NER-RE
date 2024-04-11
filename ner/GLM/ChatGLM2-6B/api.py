from fastapi import FastAPI, Request
from transformers import AutoTokenizer, AutoModel, AutoConfig
import uvicorn, json, datetime
import torch
import os

DEVICE = "cuda"
DEVICE_ID = "0"
CUDA_DEVICE = f"{DEVICE}:{DEVICE_ID}" if DEVICE_ID else DEVICE


def torch_gc():
    if torch.cuda.is_available():
        with torch.cuda.device(CUDA_DEVICE):
            torch.cuda.empty_cache()
            torch.cuda.ipc_collect()


app = FastAPI()


@app.post("/")
async def create_item(request: Request):
    global model, tokenizer
    json_post_raw = await request.json()
    json_post = json.dumps(json_post_raw)
    json_post_list = json.loads(json_post)
    prompt = json_post_list.get('prompt')
    history = json_post_list.get('history')
    max_length = json_post_list.get('max_length')
    top_p = json_post_list.get('top_p')
    temperature = json_post_list.get('temperature')
    response, history = model.chat(tokenizer,
                                   prompt,
                                   history=history,
                                   max_length=max_length if max_length else 6000,
                                   top_p=top_p if top_p else 0.7,
                                   temperature=temperature if temperature else 0.95)
    now = datetime.datetime.now()
    time = now.strftime("%Y-%m-%d %H:%M:%S")
    answer = {
        "response": response,
        "history": history,
        "status": 200,
        "time": time
    }
    log = "[" + time + "] " + '", prompt:"' + prompt + '", response:"' + repr(response) + '"'
    print(log)
    torch_gc()
    return answer


if __name__ == '__main__':
    model_path = "/data2/fyj2023/pretrained_model/chatglm2-6b-32k"
    #checkpoint_path = "/data2/fyj2023/project/ChatGLM2-6B/ptuning/output/gov1000_dbz_rawData20240306_1638/adgen-chatglm2-6b-32k-pt-128-2e-2/checkpoint-500"
    checkpoint_path = "/data2/fyj2023/project/ChatGLM2-6B/ptuning/output/scire_rawData20240311_2326/adgen-chatglm2-6b-32k-pt-128-2e-2/checkpoint-850"
    tokenizer = AutoTokenizer.from_pretrained(model_path, trust_remote_code=True)
    # model = AutoModel.from_pretrained(model_path, trust_remote_code=True).cuda()
    # 多显卡支持，使用下面两行代替上面一行，将num_gpus改为你实际的显卡数量
    # from utils import load_model_on_gpus
    # model = load_model_on_gpus(model_path, num_gpus=4)

    # 加载ptuning模型
    config = AutoConfig.from_pretrained(model_path, trust_remote_code=True, pre_seq_len=128)
    model = AutoModel.from_pretrained(model_path, config=config, trust_remote_code=True)
    prefix_state_dict = torch.load(os.path.join(checkpoint_path, "pytorch_model.bin"))
    new_prefix_state_dict = {}
    for k, v in prefix_state_dict.items():
        if k.startswith("transformer.prefix_encoder."):
            new_prefix_state_dict[k[len("transformer.prefix_encoder."):]] = v
    model.transformer.prefix_encoder.load_state_dict(new_prefix_state_dict)

    # Comment out the following line if you don't use quantization
    model = model.quantize(4)
    model = model.cuda()

    model.eval()
    uvicorn.run(app, host='0.0.0.0', port=8002, workers=1)
