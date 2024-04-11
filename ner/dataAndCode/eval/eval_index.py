import copy
import csv
import time
import numpy as np
import pandas as pd
import logging
now_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())

logging.basicConfig(
    level=logging.INFO,
     format='%(asctime)s %(levelname)-8s %(module)s[line:%(lineno)d]: >> %(message)s',
     datefmt='%Y-%m-%d %H:%M:%S'
     )


# csv_path = './data/compare.csv'
# out = open(csv_path,'a+',encoding="utf-8")
# csv_writer = csv.writer(out)

# raw_data_path = './data/full_data.json'
# raw_data_list = []
# with open(raw_data_path, 'r',encoding='utf-8') as f_raw:
#     for line in f_raw.readlines():
#         raw_data_list.append(eval(line))


# data_path = '/data/xf2022/projects/ChatGLM2-6B/ptuning/output/inference/adgen-chatglm2-6b-32k-pt-128-2e-220230815_2039/generated_predictions.txt'
# data_path = "/data/xf2022/projects/ChatGLM2-6B/ptuning/output/gov1000_2_rawData20230813_1731/result/result.txt"
# data_path = './data/result_500.txt'
data_path='../result/result_index.txt'
# data_path ='./data/res1.txt'
logging.info(f'data_path:{data_path}')

data = []
labels = []
predicts = []


data = []
labels = []
predicts = []
def deep_copy(predict_dict,predict,type_li):
    predict_copy_dbz=[]
    for p in predict:
        p_copy={}
        p_copy['中标金额']=p['中标金额']
        p_copy['中标单位']=p['中标单位']
        predict_copy_dbz.append(p_copy)
    for type in type_li:
        predict_dict[type]=predict_copy_dbz
    
with open(data_path, 'r', encoding='utf-8') as f:
    for line in f.readlines():
        try:
            data.append(eval(line))
        except:
            print(line)
i=0
for item in data:
    try:
        i=i+1
        labels.append(eval(item['labels']))
        predicts.append(eval(item['predict']))
    except:
        print(i)
        if len(labels)>len(predicts):
            labels.remove(eval(item['labels']))
        pass

logging.info(f'样本数量:{len(data)}')

def get_dictionary(items):
    dictionary = {}
    for item in items:
        try:
            key, value = item.split('：', 1)
            dictionary[key] = value
        except:
            logging.info(f'异常数据:{items}')    

    return dictionary

# for ss in data:
#     # label_items = ss["labels"].split('；')[:-1]
#     # predict_items = ss["predict"].split('；')[:-1]
#     # labels.append(get_dictionary(label_items))
#     # predicts.append(get_dictionary(predict_items))
#     labels.append(ss["labels"])
#     predicts.append(ss["predict"])
    

logging.info(f'原样本数量:{len(labels)}')
logging.info(f'预测样本数量:{len(predicts)}')

scores = []
scores_dict = {}
error_list = []
error_dict={}
assert len(labels) == len(predicts)
len_cgxx=0
c_zbdw = 0
c_zbjine=0
c=0
n = 0
f1_calculate_dict={'中标单位':{'tp':0,'tn':0,'fp':0,'fn':0}, '中标金额': {'tp':0,'tn':0,'fp':0,'fn':0}}
f1_score_dict={ '中标单位':{'f1':0,'p':0,'r':0,'accuracy':0}, '中标金额':{'f1':0,'p':0,'r':0,'accuracy':0}}
for i in range(0,len(labels)):
    label=labels[i]
    preict = predicts[i]
    dict_zbxx={}
    for item_label in label:
        dict_zbxx[item_label['中标单位']]=item_label['中标金额']
    #logging.info(f'Label中标信息:{dict_zbxx}')
    copied_keys = copy.deepcopy(list(dict_zbxx.keys()))
    len_cgxx=len_cgxx+len(dict_zbxx)
    for item in preict:
        if item['中标单位'] in dict_zbxx.keys():
            f1_calculate_dict['中标单位']['tp']+=1
            if item['中标单位'] in copied_keys:
                copied_keys.remove(item['中标单位'])
            if '中标单位' not in scores_dict:
                scores_dict['中标单位'] = 1
            else:
                scores_dict['中标单位'] += 1
            if item['中标金额']==dict_zbxx[item['中标单位']]:
                if item['中标金额']=='null':
                    f1_calculate_dict['中标金额']['tn']+=1
                else:
                    f1_calculate_dict['中标金额']['tp']+=1
                if '中标金额' not in scores_dict:
                    scores_dict['中标金额'] = 1
                else:
                    scores_dict['中标金额'] += 1
            else:
                if dict_zbxx[item['中标单位']]=="null":
                    f1_calculate_dict['中标金额']['fn']+=1
                else:
                    f1_calculate_dict['中标金额']['fp']+=1  
                # if '中标金额' not in error_dict:
                #     error_dict['中标金额']=[]
                #     error_dict['中标金额'].append([ {"label":str(label)}, {"predict":str(predict)}, {str(dict_zbxx[item['中标单位']]):str(item['中标金额'])}])
                # else:
                #     error_dict['中标金额'].append([ {"label":str(label)}, {"predict":str(predict)}, {str(dict_zbxx[item['中标单位']]):str(item['中标金额'])}])
                # error_list[index].append([label, predict, {label_key:predict[label_key]}])
        else:
            f1_calculate_dict['中标单位']['fp']+=1
            # if '中标单位' not in error_dict:
            #     error_dict['中标单位']=[]
            #     error_dict['中标单位'].append([ {"label":str(label)}, {"predict":str(predict)}, {str(label[label_key]):str(item['中标单位'])}])
            # else:
            #     error_dict['中标单位'].append([ {"label":str(label)}, {"predict":str(predict)}, {str(label[label_key]):str(item['中标单位'])}])
            #     error_list[index].append([ label, predict, {label_key:predict[label_key]}])
    for key in copied_keys:
        f1_calculate_dict['中标单位']['fn']+=1
        f1_calculate_dict['中标金额']['fn']+=1
        # logging.info(f'key:{copied_keys}')
        # if '中标单位' not in error_dict:
        #     error_dict['中标单位']=[]
        #     error_dict['中标单位'].append([ {"label":str(label)}, {"predict":str(predict)}, {str(key):""}])
        # else:
        #     error_dict['中标单位'].append([ {"label":str(label)}, {"predict":str(predict)}, {str(key):""}])
        #     error_list[index].append([ label, predict, {label_key:predict[label_key]}])


for field, counts in f1_calculate_dict.items():
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
    print(field)
    accuracy = (tp + tn) / (tp + tn + fp + fn)

    # Write to f1_score_dict
    f1_score_dict[field]['f1'] = f1
    f1_score_dict[field]['p'] = precision
    f1_score_dict[field]['r'] = recall
    f1_score_dict[field]['accuracy'] = accuracy
    
    
    # for index, (label_key, label_value) in enumerate(label.items()):     
    #     try:
    #         if label_key == '所属地区':
    #             if predict[label_key] in label_value or label_value in predict[label_key]:
    #             # if predict[label_key] == label_value:
    #                 c += 1
    #                 if label_key not in scores_dict:
    #                     scores_dict[label_key] = 1
    #                 else:
    #                     scores_dict[label_key] += 1
    #             else:
    #                 error_list[index].append([ label, predict, {label_key:predict[label_key]}])
    #                 if label_key not in error_dict:
    #                     error_dict[label_key]=[]
    #                     error_dict[label_key].append([ {"label":label}, {"predict":predict}, {label[label_key]:predict[label_key]}])
    #                 else:
    #                     error_dict[label_key].append([ {"label":label}, {"predict":predict}, {label[label_key]:predict[label_key]}])
    #                 print({label_key:predict[label_key]})
    #         # if predict[label_key] in label_value or label_value in predict[label_key]:
    #         elif label_key == '评委名单':
    #             set_predict=set(predict[label_key])
    #             set_label=set(label_value)
    #             if set_label==set_predict:
    #                 c += 1
    #                 if label_key not in scores_dict:
    #                     scores_dict[label_key] = 1
    #                 else:
    #                     scores_dict[label_key] += 1
    #             else:
    #                 error_list[index].append([ label, predict, {label_key:predict[label_key]}])
    #                 if label_key not in error_dict:
    #                     error_dict[label_key]=[]
    #                     error_dict[label_key].append([ {"label":str(label)}, {"predict":str(predict)}, {str(label[label_key]):str(predict[label_key])}])
    #                     print(error_dict[label_key])
    #                 else:
    #                     error_dict[label_key].append([ {"label":str(label)}, {"predict":str(predict)}, {str(label[label_key]):str(predict[label_key])}])
    #                     print({label_key:predict[label_key]})
    #         elif label_key == '中标信息':
    #             dict_zbxx={}
    #             for item_label in label_value:
    #                 dict_zbxx[item_label['中标单位']]=item_label['中标金额']
    #             #logging.info(f'Label中标信息:{dict_zbxx}')
    #             copied_keys = copy.deepcopy(list(dict_zbxx.keys()))
    #             len_cgxx=len_cgxx+len(dict_zbxx)
    #             for item in predict[label_key]:
    #                 if item['中标单位'] in dict_zbxx.keys():
    #                     copied_keys.remove(item['中标单位'])
    #                     if '中标单位' not in scores_dict:
    #                         scores_dict['中标单位'] = 1
    #                     else:
    #                         scores_dict['中标单位'] += 1
    #                     if item['中标金额']==dict_zbxx[item['中标单位']]:
    #                         if '中标金额' not in scores_dict:
    #                             scores_dict['中标金额'] = 1
    #                         else:
    #                             scores_dict['中标金额'] += 1
    #                     else:
    #                         if '中标金额' not in error_dict:
    #                             error_dict['中标金额']=[]
    #                             error_dict['中标金额'].append([ {"label":str(label)}, {"predict":str(predict)}, {str(dict_zbxx[item['中标单位']]):str(item['中标金额'])}])
    #                         else:
    #                             error_dict['中标金额'].append([ {"label":str(label)}, {"predict":str(predict)}, {str(dict_zbxx[item['中标单位']]):str(item['中标金额'])}])
    #                         error_list[index].append([label, predict, {label_key:predict[label_key]}])
    #                 else:
    #                     if '中标单位' not in error_dict:
    #                         error_dict['中标单位']=[]
    #                         error_dict['中标单位'].append([ {"label":str(label)}, {"predict":str(predict)}, {str(label[label_key]):str(item['中标单位'])}])
    #                     else:
    #                         error_dict['中标单位'].append([ {"label":str(label)}, {"predict":str(predict)}, {str(label[label_key]):str(item['中标单位'])}])
    #                         error_list[index].append([ label, predict, {label_key:predict[label_key]}])
    #             for key in copied_keys:
    #                 logging.info(f'key:{copied_keys}')
    #                 if '中标单位' not in error_dict:
    #                     error_dict['中标单位']=[]
    #                     error_dict['中标单位'].append([ {"label":str(label)}, {"predict":str(predict)}, {str(key):""}])
    #                 else:
    #                     error_dict['中标单位'].append([ {"label":str(label)}, {"predict":str(predict)}, {str(key):""}])
    #                     error_list[index].append([ label, predict, {label_key:predict[label_key]}])
    #         else:    
    #             if predict[label_key] == label_value:
    #                 c += 1
    #                 if label_key not in scores_dict:
    #                     scores_dict[label_key] = 1
    #                 else:
    #                     scores_dict[label_key] += 1
    #             else:
    #                 if label_key not in error_dict:
    #                     error_dict[label_key]=[]
    #                     error_dict[label_key].append([ {"label":label}, {"predict":predict}, {label[label_key]:predict[label_key]}])
    #                 else:
    #                     error_dict[label_key].append([ {"label":label}, {"predict":predict}, {label[label_key]:predict[label_key]}])
    #                 error_list[index].append([ label, predict, {label_key:predict[label_key]}])
    #                 # print({label_key:predict[label_key]})
    #     except Exception as e:
    # # 捕获其他异常，并打印异常信息
    #         import traceback
    #         traceback.print_exc()
    #         #print(f"Caught an exception: {e}")
    #         pass


# acc = c / n
# scores.append({"完全匹配":acc})
# acc_jine = c_zbjine / n
# scores.append({"中标金额匹配":acc_jine})
# acc_zbdw = c_zbdw / n
# scores.append({"中标单位匹配":acc_zbdw})
# for key in scores_dict:
#     if key=='中标单位' or key=='中标金额':
#         scores_dict[key]/=len_cgxx
#     else:   
#         scores_dict[key] /= len(labels)


error_file_path = "../error/error_index/"
with open(error_file_path+"error.txt", 'w', encoding='utf-8') as f_error:
    for errors in error_list:
        f_error.write(str(errors) + '\n')

# for key in error_dict.keys():
#     with open(error_file_path+"error_"+str(key)+'.txt', 'w', encoding='utf-8') as f_error:
#         for error in error_dict[key]:
#             f_error.write(str(error) + '\n')  
logging.info(f'data_path:{data_path}')
# logging.info(f'error_data_path:{error_file_path}')
logging.info(f'match way:完全匹配')
logging.info(f'scores:{f1_score_dict}')
df = pd.DataFrame.from_dict(f1_score_dict, orient='index')

# Write DataFrame to Excel
df.to_excel("../result/index_evaluation1.xlsx", index_label='Field')
# csv_writer.writerow([now_time])
# csv_writer.writerow([data_path])
# csv_writer.writerow([error_file_path])
# csv_writer.writerow(['match way:完全匹配'])
# csv_writer.writerow([scores_dict])
# csv_writer.writerow([np.mean(scores)])



# nohup python eval_gov.py >> ./log/eval_chatglm_6b_32k_gov_2.log &