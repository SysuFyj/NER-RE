import re
import json
import random
import pandas as pd

# 指定切分比例
train_ratio = 0.6  
dev_ratio = 0.2
test_ratio = 0.2

# 读取整个json文件
filename = '../data/index/full_data_index.json'

full_dataset = []
# df = pd.read_json(filename, encoding='utf-8')
# full_dataset = list(df.loc[0])
with open(filename, 'r', encoding='utf-8') as f:
    for l in f:
        data=json.loads(l)
        full_dataset.append(data)

# full_dataset = []
# for i in range(len(data_list)):
#      full_dataset.append(list(data_list[i].values())[0])

# 将unicode字符转换为utf-8
def illegal_char(s):
    s = re \
        .compile( \
        u"[^"
        u"\u4e00-\u9fa5"
        u"\u0041-\u005A"
        u"\u0061-\u007A"
        u"\u0030-\u0039"
        u"\u3002\uFF1F\uFF01\uFF0C\u3001\uFF1B\uFF1A\u300C\u300D\u300E\u300F\u2018\u2019\u201C\u201D\uFF08\uFF09\u3014\u3015\u3010\u3011\u2014\u2026\u2013\uFF0E\u300A\u300B\u3008\u3009"
        u"\!\@\#\$\%\^\&\*\(\)\-\=\[\]\{\}\\\|\;\'\:\"\,\.\/\<\>\?\/\*\+"
        u"]+") \
        .sub(' ', s)
    return s

# for ss in full_dataset:
#     text = ss['input']
#     ss['input'] = illegal_char(text)
   

print(full_dataset[0])

# 计算切分后数据集大小 
train_size = int(len(full_dataset) * train_ratio)  
dev_size = int(len(full_dataset) * dev_ratio)

# 随机划分数据集
random.seed(10)
random.shuffle(full_dataset)
train_set = full_dataset[:train_size]
dev_set = full_dataset[train_size:train_size+dev_size] 
test_set = full_dataset[train_size+dev_size:]

print("all data size:", len(full_dataset))
print("train_size:", train_size)
print("dev_size", dev_size)
print("test_size:", len(test_set))

# 写入新的json文件
with open('../data/index/full_data.json', 'w', encoding='utf-8') as f0:
    for line in full_dataset:
        json.dump(line, f0, ensure_ascii=False)
        f0.write('\n')

with open('../data/index/train.json', 'w', encoding='utf-8') as f1:
    for line in train_set:
        json.dump(line, f1, ensure_ascii=False)
        f1.write('\n')
    
with open('../data/index//dev.json', 'w', encoding='utf-8') as f2:
    for line in dev_set:
        json.dump(line, f2, ensure_ascii=False)
        f2.write('\n')
with open('../data/index//test.json', 'w', encoding='utf-8') as f3:
    for line in test_set:
        json.dump(line, f3, ensure_ascii=False)
        f3.write('\n')