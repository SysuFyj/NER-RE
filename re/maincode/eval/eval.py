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
for i in range(1,4):
    relation = {"COMPARE":{"tp":0,"fp":0,"fn":0,"tn":0},"CONJUNCTION":{"tp":0,"fp":0,"fn":0,"tn":0},"FEATURE-OF":{"tp":0,"fp":0,"fn":0,"tn":0},"USED-FOR":{"tp":0,"fp":0,"fn":0,"tn":0},"HYPONYM-OF":{"tp":0,"fp":0,"fn":0,"tn":0},"EVALUATE-FOR":{"tp":0,"fp":0,"fn":0,"tn":0},"PART-OF":{"tp":0,"fp":0,"fn":0,"tn":0}} 
    f1_score_dict = {"COMPARE":{'f1':0,'p':0,'r':0,'accuracy':0},"CONJUNCTION":{'f1':0,'p':0,'r':0,'accuracy':0},"FEATURE-OF":{'f1':0,'p':0,'r':0,'accuracy':0},"USED-FOR":{'f1':0,'p':0,'r':0,'accuracy':0},"HYPONYM-OF":{'f1':0,'p':0,'r':0,'accuracy':0},"EVALUATE-FOR":{'f1':0,'p':0,'r':0,'accuracy':0},"PART-OF":{'f1':0,'p':0,'r':0,'accuracy':0}} 
    # False Positive for "relation"
    fn_pr = {}  # False Negative for "pr"

    # 解析 JSON 数据


    filename = './k'+str(i)+'/os.json'

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
        print(i)
        print(relation)
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
    average_f1_values.append(average_f1)
    logging.info(f'Average f1 :{average_f1}')
    df = pd.DataFrame.from_dict(f1_score_dict, orient='index')

    # Write DataFrame to Excel
    df.to_excel("./result/k"+str(i)+"_evaluation.xlsx", index_label='Field')
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
average_f1_values.append(0.30933)

average_f1_values.append(0.27201)
average_f1_values.append(0.26764)
print(average_f1_values)
N_values = range(1, len(average_f1_values) + 1)
# 绘制折线图
plt.plot(N_values, average_f1_values, marker='o', linestyle='-')

# 设置标题和标签
plt.title('Average F1 Scores Over k-shot demostrations')
plt.xlabel('Number of demostrations')
plt.ylabel('Average F1 Score')

# 显示图例
plt.legend(['Average F1'])

# 显示图形

plt.savefig('./f1-scierc.png')
plt.close()
