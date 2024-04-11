import json
import logging
import pandas as pd
import matplotlib.pyplot as plt
logging.basicConfig(
    level=logging.INFO,
     format='%(asctime)s %(levelname)-8s %(module)s[line:%(lineno)d]: >> %(message)s',
     datefmt='%Y-%m-%d %H:%M:%S'
     )
average_f1_values = []
average_f1_values_cp = []
for i in range(1,4):
    relation = {"标准":{"tp":0,"fp":0,"fn":0,"tn":0},"方法":{"tp":0,"fp":0,"fn":0,"tn":0},"服务":{"tp":0,"fp":0,"fn":0,"tn":0},"属性":{"tp":0,"fp":0,"fn":0,"tn":0},"职责":{"tp":0,"fp":0,"fn":0,"tn":0}} 
    f1_score_dict = {"标准":{'f1':0,'p':0,'r':0,'accuracy':0},"方法":{'f1':0,'p':0,'r':0,'accuracy':0},"服务":{'f1':0,'p':0,'r':0,'accuracy':0},"属性":{'f1':0,'p':0,'r':0,'accuracy':0},"职责":{'f1':0,'p':0,'r':0,'accuracy':0}} 
    # False Positive for "relation"
    fn_pr = {}  # False Negative for "pr"

    # 解析 JSON 数据


    # filename = './cl_k'+str(i)+'/os.json'
    filename = './k/'+str(i*2)+'/os.json'
    full_dataset = []
    count=0
    # df = pd.read_json(filename, encoding='utf-8')
    # full_dataset = list(df.loc[0])
    with open(filename, 'r', encoding='utf-8') as f:
        for l in f:
            data=json.loads(l)
            full_dataset.append(data)
    for data in full_dataset:
        if data["relation"]==data["pr"]:
            relation[data["relation"]]["tp"]+=2
            for key in relation.keys():
                if key !=data["relation"]:
                    count+=1
                    relation[key]["tn"]+=1
        else:
            relation[data["pr"]]["fp"]+=1
            relation[data["relation"]]["fn"]+=1

    for field, counts in relation.items():
        tp = counts['tp']
        tn = counts['tn']
        fp = counts['fp']
        fn = counts['fn']

        # Precision
        if tp + fp == 0:
            precision = 0
        else:
            precision = tp / (tp + fp)

        # Recall
        if tp + fn == 0:
            recall = 0
        else:
            recall = tp / (tp + fn)

        # F1 Score
        if precision + recall == 0:
            f1 = 0
        else:
            f1 = 2 * (precision * recall) / (precision + recall)

        # Accuracy
        accuracy = (tp + tn) / (tp + tn + fp + fn)

        # Write to f1_score_dict
        f1_score_dict[field]['f1'] = f1
        f1_score_dict[field]['p'] = precision
        f1_score_dict[field]['r'] = recall
        f1_score_dict[field]['accuracy'] = accuracy
    # logging.info(f'f1_dict{f1_score_dict}')
    total_f1 = 0
    for relation, scores in f1_score_dict.items():
        f1 = scores['f1']
        total_f1 += f1
    average_f1 = total_f1 / len(f1_score_dict)
    average_f1_values_cp.append(average_f1)
    logging.info(f'Average f1 :{average_f1}')
    df = pd.DataFrame.from_dict(f1_score_dict, orient='index')

    # Write DataFrame to Excel
    df.to_excel("./result/k_ch_"+str(i)+"_ge_evaluation.xlsx", index_label='Field')
print('----------------------------------------------')
for i in range(1,7):
    relation = {"标准":{"tp":0,"fp":0,"fn":0,"tn":0},"方法":{"tp":0,"fp":0,"fn":0,"tn":0},"服务":{"tp":0,"fp":0,"fn":0,"tn":0},"属性":{"tp":0,"fp":0,"fn":0,"tn":0},"职责":{"tp":0,"fp":0,"fn":0,"tn":0}} 
    f1_score_dict = {"标准":{'f1':0,'p':0,'r':0,'accuracy':0},"方法":{'f1':0,'p':0,'r':0,'accuracy':0},"服务":{'f1':0,'p':0,'r':0,'accuracy':0},"属性":{'f1':0,'p':0,'r':0,'accuracy':0},"职责":{'f1':0,'p':0,'r':0,'accuracy':0}} 
    # False Positive for "relation"
    fn_pr = {}  # False Negative for "pr"

    # 解析 JSON 数据


    filename = './cl_k'+str(i)+'/os.json'
    # filename = './k/'+str(i*2)+'/os.json'
    full_dataset = []
    count=0
    # df = pd.read_json(filename, encoding='utf-8')
    # full_dataset = list(df.loc[0])
    with open(filename, 'r', encoding='utf-8') as f:
        for l in f:
            data=json.loads(l)
            full_dataset.append(data)
    for data in full_dataset:
        if data["relation"]==data["pr"]:
            relation[data["relation"]]["tp"]+=2
            for key in relation.keys():
                if key !=data["relation"]:
                    count+=1
                    relation[key]["tn"]+=1
        else:
            relation[data["pr"]]["fp"]+=1
            relation[data["relation"]]["fn"]+=1

    for field, counts in relation.items():
        tp = counts['tp']
        tn = counts['tn']
        fp = counts['fp']
        fn = counts['fn']

        # Precision
        if tp + fp == 0:
            precision = 0
        else:
            precision = tp / (tp + fp)

        # Recall
        if tp + fn == 0:
            recall = 0
        else:
            recall = tp / (tp + fn)

        # F1 Score
        if precision + recall == 0:
            f1 = 0
        else:
            f1 = 2 * (precision * recall) / (precision + recall)

        # Accuracy
        accuracy = (tp + tn) / (tp + tn + fp + fn)

        # Write to f1_score_dict
        f1_score_dict[field]['f1'] = f1
        f1_score_dict[field]['p'] = precision
        f1_score_dict[field]['r'] = recall
        f1_score_dict[field]['accuracy'] = accuracy
    # logging.info(f'f1_dict{f1_score_dict}')
    total_f1 = 0
    for relation, scores in f1_score_dict.items():
        f1 = scores['f1']
        total_f1 += f1
    average_f1 = total_f1 / len(f1_score_dict)
    if i%2==0:
        average_f1_values.append(average_f1)
    logging.info(f'Average f1 :{average_f1}')
    df = pd.DataFrame.from_dict(f1_score_dict, orient='index')

    # Write DataFrame to Excel
    df.to_excel("./result/k_ch_"+str(i)+"_evaluation.xlsx", index_label='Field')
# json_data = '{"token": ["Here", "we", "develop", "an", "approach", "for", "1", "distance", "that", "begins", "with", "an", "explicit", "and", "exactly", "distance-preserving", "embedding", "of", "the", "points", "into", "2", "2", "."], "obj_start": 6, "obj_end": 7, "subj_start": 4, "subj_end": 4, "relation": "USED-FOR", "pr": "USED-FOR"}'
# data = json.loads(json_data)

# # 比较 relation 和 pr 字段
# if data['relation'] == 'USED-FOR' and data['pr'] == 'USED-FOR':
#     tp_used_for += 1
# else:
#     if data['relation'] not in fp_relation:
#         fp_relation[data['relation']] = 0
#     fp_relation[data['relation']] += 1
    
#     if data['pr'] not in fn_pr:
#         fn_pr[data['pr']] = 0
#     fn_pr[data['pr']] += 1

# # 计算 Precision、Recall 和 F1 分数
# precision = tp_used_for / (tp_used_for + sum(fp_relation.values()))
# recall = tp_used_for / (tp_used_for + sum(fn_pr.values()))
# f1 = 2 * (precision * recall) / (precision + recall)

# print("Precision:", precision)
# print("Recall:", recall)
# print("F1 Score:", f1)

# 一系列的 average_f1 值
  # 请替换为你实际的数据

# x 轴数据（这里假设 x 轴为数据点的索引）
# average_f1_values.append(0.30933)

# average_f1_values.append(0.27201)
# average_f1_values.append(0.26764)
# print(average_f1_values)
# N_values = range(1, len(average_f1_values) + 1)
# # # 绘制折线图
# plt.plot(N_values, average_f1_values, marker='o', linestyle='-')

# # 设置标题和标签
# plt.title('Average F1 Scores Over k-shot demostrations')
# plt.xlabel('Number of demostrations')
# plt.ylabel('Average F1 Score')

# # 显示图例
# plt.legend(['Average F1'])

# # 显示图形
# # plt.show()
# plt.savefig('./f1-ch.png')


import matplotlib.pyplot as plt

# 定义横坐标和对应的两根折线的纵坐标
x_values = [2, 4, 6]
y_values1 = [3, 6, 9]  # 第一根折线的纵坐标
y_values2 = [2, 4, 8]  # 第二根折线的纵坐标
average_f1_values_full=[0.479,0.4,0.349]
# 绘制折线图
plt.plot(x_values, average_f1_values_cp, marker='^', linestyle='-', label='with 50% generate data')
plt.plot(x_values, average_f1_values_full, marker='s', linestyle='-', label='with 100% generate data')
plt.plot(x_values, average_f1_values, marker='o', linestyle='-', label='no generate data')

# 设置标题和标签
plt.title('Average F1 Scores Over k-shot demostrations With different ration of generate data')
plt.xlabel('Number of demostrations')
plt.ylabel('Average F1 Score')
plt.xticks(x_values)
# 添加图例
plt.legend()

# 显示图形
plt.savefig('./f1_ge.png')
