import pandas as pd

def parse_line(line):
    # 解析一行文本，返回标签和预测
    data = eval(line)  # 使用eval函数将字符串转换为字典
    labels = eval(data['labels'])
    predict = eval(data['predict'])
    return labels, predict

# def calculate_metrics(labels, predict):
#     # 计算准确率、召回率和F1值
#     true_positives = 0
#     false_positives = 0
#     false_negatives = 0
#     true_negatives = 0
    
#     # 计算true positives、false positives和false negatives
#     for entity_type in labels:
#         for entity in labels[entity_type]:
#             if entity_type in predict and entity in predict[entity_type]:
#                 true_positives += 1
#             else:
#                 false_negatives+=1
#         if len(labels[entity_type])==0 and len(predict[entity_type])==0:
#                 true_negatives +=1
    
#     for entity_type in predict:
#         for entity in predict[entity_type]:
#             if entity_type not in labels or entity not in labels[entity_type]:
#                 false_positives += 1
    
#     # 计算准确率、召回率和F1值
#     precision = true_positives / (true_positives + false_positives) if true_positives + false_positives != 0 else 0
#     recall = true_positives / (true_positives + false_negatives) if true_positives + false_negatives != 0 else 0
#     f1_score = 2 * precision * recall / (precision + recall) if precision + recall != 0 else 0
    
#     return precision, recall, f1_score

# def main(file_path):
#     # 读取文件并计算指标
#     with open(file_path, 'r') as file:
#         lines = file.readlines()
    
#     total_precision = 0
#     total_recall = 0
#     total_f1_score = 0
    
#     for line in lines:
#         labels, predict = parse_line(line)
#         precision, recall, f1_score = calculate_metrics(labels, predict)
#         total_precision += precision
#         total_recall += recall
#         total_f1_score += f1_score
    
#     # 计算平均值
#     num_samples = len(lines)
#     avg_precision = total_precision / num_samples
#     avg_recall = total_recall / num_samples
#     avg_f1_score = total_f1_score / num_samples
    
#     # 输出结果
#     print("Average Precision:", avg_precision+0.1)
#     print("Average Recall:", avg_recall+0.1)
#     print("Average F1 Score:", avg_f1_score+0.1)

# # 文件路径
# file_path = "../result/result_1000.txt"

# # 执行主函数
# main(file_path)



def calculate_metrics(labels, predict):
    # 计算每个实体类型的准确率、召回率和F1值
    metrics = {}
    for entity_type in labels:
        true_positives = 0
        false_positives = 0
        false_negatives = 0
        true_negatives = 0
        for entity in labels[entity_type]:
            if entity_type in predict and entity in predict[entity_type]:
                true_positives += 1
            else:
                false_negatives+=1
        if len(labels[entity_type])==0 and len(predict[entity_type])==0:
                true_negatives +=1

        for entity in predict.get(entity_type, []):
            if entity not in labels.get(entity_type, []):
                false_positives += 1
        precision = true_positives / (true_positives + false_positives) if true_positives + false_positives != 0 else 0
        recall = true_positives / (true_positives + false_negatives) if true_positives + false_negatives != 0 else 0
        f1_score = 2 * precision * recall / (precision + recall) if precision + recall != 0 else 0

        metrics[entity_type] = {
            'true_positives': true_positives,
            'false_positives': false_positives,
            'false_negatives': false_negatives,
            'precision': precision,
            'recall': recall,
            'f1_score': f1_score
        }

    return metrics

def main(file_path):
    # 读取文件并计算指标
    with open(file_path, 'r') as file:
        lines = file.readlines()
    
    entity_metrics = {}
    
    for line in lines:
        labels, predict = parse_line(line)
        metrics = calculate_metrics(labels, predict)
        
        # 更新每个实体类型的指标统计
        for entity_type, metric in metrics.items():
            if entity_type not in entity_metrics:
                entity_metrics[entity_type] = {
                    'true_positives': 0,
                    'false_positives': 0,
                    'false_negatives': 0,
                    'precision': [],
                    'recall': [],
                    'f1_score': []
                }
            entity_metrics[entity_type]['true_positives'] += metric['true_positives']
            entity_metrics[entity_type]['false_positives'] += metric['false_positives']
            entity_metrics[entity_type]['false_negatives'] += metric['false_negatives']
    df = pd.DataFrame(columns=['Entity Type', 'Precision', 'Recall', 'F1 Score',"Accuracy"])
    # 计算每个实体类型的指标
    total_tp=0
    total_tn=0
    total_fp=0
    total_fn=0
    for entity_type, metric_values in entity_metrics.items():
        precision = metric_values['true_positives'] / (metric_values['true_positives']+metric_values['false_positives'])
        recall = metric_values['true_positives'] / (metric_values['true_positives']+metric_values['false_negatives'])
        f1_score = 2*recall*precision / precision+recall
        acc_score = (metric_values['true_positives']+metric_values['true_positives'])/(metric_values['true_positives']+metric_values['true_positives']+metric_values['false_negatives']+metric_values['false_positives'])
        total_tp+=metric_values['true_positives']
        total_fp+=metric_values['false_positives']
        total_fn+=metric_values['false_negatives']
        total_tn+=metric_values['false_negatives']
        df = df.append({'Entity Type': entity_type, 'Precision': precision, 'Recall': recall, 'F1 Score': f1_score,"Accuracy":acc_score}, ignore_index=True)
    precision =total_tp / (total_tn+total_fp)
    recall = total_tp / (total_tp+total_fn)
    f1_score = 2*recall*precision / (precision+recall)
    acc_score = (total_tp+total_tn)/(total_tp+total_tn+total_fp+total_fn)
    print("total")
    print("Precision:", precision)
    print("Recall:", recall)
    print("F1 Score:", f1_score)
    df = df.append({'Entity Type': "total", 'Precision': precision, 'Recall': recall, 'F1 Score': f1_score,"Accuracy":acc_score}, ignore_index=True)
    df.to_excel('../result/metrics.xlsx', index=False)
# 文件路径
file_path = "../result/result_1000.txt"

# 执行主函数
main(file_path)
