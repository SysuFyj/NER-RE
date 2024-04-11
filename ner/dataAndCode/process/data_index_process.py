import re
import json
import random
import pandas as pd

# 指定切分比例
train_ratio = 0.6  
dev_ratio = 0.2
test_ratio = 0.2

# 读取数据整改后的整个json文件
filename = './data/mod/data_modified.json'
# df = pd.read_json(filename, encoding='utf-8')
# full_dataset = list(df.loc[0])
with open(filename, 'r', encoding='utf-8') as f:
    data_list = json.load(f)

full_dataset = []
for i in range(len(data_list)):
     full_dataset.append(list(data_list[i].values())[0])

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
with open('./mod/data_modified/full_data_md.json', 'w', encoding='utf-8') as f0:
    res_li=[]
    id=0
    for line in full_dataset:
        res={}
        sb=json.dumps(line, ensure_ascii=False)
        # print(line['output'])
        output= json.loads(line['output'])
        # print(output['中标信息'])
        res['output']=output['中标信息']
        info_li=['、采购结果','、中标（成交）信息','、中标信息','、成交信息','、中标(成交)信息','、 评审结果','、评审结果','、\n中标信息','、成交人信息','、评审意见','、招标评审结果','、本项目中标','、 中标结果','、中标结果','、中标情况','、评标结果','、成交人情况','、中标人','、成交情况','、谈判结果','、中标候选人','、入围中标人']
        ch_num=['一','二','三','四','五','六','七','八','九','十','十一']
        flag = False
        input_index=''
        input = line['input']
        res['text']=str(input)
        for item in info_li:
            idx=input.find(item)
            if  idx!=-1:
                if input[idx-1] in ch_num :
                    idx_end=input.find(ch_num[ch_num.index(input[idx-1])+1]+'、')
                    if idx_end!=-1:
                        input_index=input[idx+len(item):idx_end]
                        res['input']=str(input_index)
                        flag=True
                        break
        if not flag:
            id+=1
            print("未成功识别")
            print(input)
        json.dump(res, f0, ensure_ascii=False)
        f0.write('\n')
        res_li.append(res)
    print(id)
# print(res_li[0]['input'])
    

        # json.dump(line, f0, ensure_ascii=False)
        # f0.write('\n')

# with open('./data_modified/train.json', 'w', encoding='utf-8') as f1:
#     for line in train_set:
#         json.dump(line, f1, ensure_ascii=False)
#         f1.write('\n')
    
# with open('./data_modified/dev.json', 'w', encoding='utf-8') as f2:
#     for line in dev_set:
#         json.dump(line, f2, ensure_ascii=False)
#         f2.write('\n')
# with open('./data_modified/test.json', 'w', encoding='utf-8') as f3:
#     for line in test_set:
#         json.dump(line, f3, ensure_ascii=False)
#         f3.write('\n')