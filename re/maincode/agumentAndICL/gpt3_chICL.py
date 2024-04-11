import json
import random
import time
import requests
from tqdm import tqdm
from collections import Counter
import argparse
import numpy as np
import copy
import os




def convert_token(token):
    """ Convert PTB tokens to normal tokens """
    if (token.lower() == '-lrb-'):
        return '('
    elif (token.lower() == '-rrb-'):
        return ')'
    elif (token.lower() == '-lsb-'):
        return '['
    elif (token.lower() == '-rsb-'):
        return ']'
    elif (token.lower() == '-lcb-'):
        return '{'
    elif (token.lower() == '-rcb-'):
        return '}'
    return token


def f1_score(true, pred_result, rel2id):
    correct = 0
    total = len(true)
    correct_positive = 0
    pred_positive = 0
    gold_positive = 0
    neg = -1
    for name in ['NA', 'na', 'no_relation', 'Other', 'Others', 'false', 'unanswerable']:
        if name in rel2id:
            neg = rel2id[name]
            break
    for i in range(total):
        golden = true[i]
        if golden == pred_result[i]:
            correct += 1
            if golden != neg:
                correct_positive += 1
        if golden != neg:
            gold_positive +=1
        if pred_result[i] != neg:
            pred_positive += 1
    acc = float(correct) / float(total)
    try:
        micro_p = float(correct_positive) / float(pred_positive)
    except:
        micro_p = 0
    try:
        micro_r = float(correct_positive) / float(gold_positive)
    except:
        micro_r = 0
    try:
        micro_f1 = 2 * micro_p * micro_r / (micro_p + micro_r)
    except:
        micro_f1 = 0
    result = {'acc': acc, 'micro_p': micro_p, 'micro_r': micro_r, 'micro_f1': micro_f1}
    return result


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--train_path', '-tp', type=str, required=True, help="The path of training / demonstration data.")
    parser.add_argument('--test_path', '-ttp', type=str, required=True, help="The path of test data.")
    parser.add_argument('--generate_path', '-gp', type=str, required=True, help="The path of generate data.")
    parser.add_argument('--output_success', '-os', type=str, required=True, help="The output directory of successful ICL samples.")
    parser.add_argument('--output_nores', '-on', type=str, required=True, help="The output directory of failed ICL samples.")
    parser.add_argument('--prompt', type=str, required=True, choices=["text", "text_schema", "instruct", "instruct_schema"])
    parser.add_argument('--k', type=int, default=1, help="k-shot demonstrations")
    parser.add_argument('--k_ge', type=int, default=0, help="k-shot generated demonstrations")
    args = parser.parse_args()
    
    # Train / Demostration Set
    with open(args.train_path,'r') as f:
        train = json.load(f)
    label_list = {}
    for line in train:
        rel = line['relation']
        if rel not in label_list:
            label_list[rel] = [line]
        else:
            label_list[rel].append(line)
    ge_train=[]
    with open(args.generate_path,'r') as f:
        ge_train = json.load(f)
    generated_list = {}
    for line in ge_train:
        rel = line['relation']
        if rel not in generated_list:
            generated_list[rel] = [line]
        else:
            generated_list[rel].append(line)

    # Relations
    rels = list(label_list.keys())
    rel2id = {}
    for i, rel in enumerate(rels):
        rel2id[rel] = i

    # Label words
    rel2labelword = {}
    for rel in rels:
        rel2labelword[rel] = rel.lower().replace("_"," ").replace("-", " ").replace("per", "person").replace("org", "organization").replace("stateor", "state or ")
    labelword2rel = {}
    for k,v in rel2labelword.items():
        labelword2rel[v] = k

    # Test Set
    with open(args.test_path,'r') as f:
        test = json.load(f)

    res = []
    true = []
    nores = []
    success = []
    with open(os.path.join(args.output_success, "os.json"),"w") as f:
        for input in tqdm(test):
            random.shuffle(rels)
            try:
                if "text" in args.prompt:
                    prompt = "以下是候选关系列表 " + ', '.join(labelword2rel.keys()) + ".\n"
                else:
                    prompt = "假设你是一个关系抽取的专家，给定一个上下文Context，其中包含一对头实体(object)和尾实体(subject)，从候选关系中确定头实体和尾实体之间的关系，候选关系列表如下: " + \
                     ', '.join(labelword2rel.keys()) + ".\n"
                for rel in rels:
                    random.shuffle(label_list[rel])
                    kshot = label_list[rel][:args.k]
                    for data in kshot:
                        head = data['subject']
                       # headtype = data['subj_type'].lower().replace('_',' ')
                     #   if headtype == "misc":
                       #     headtype = "miscellaneous"
                        tail = data['object']
                     #   tailtype = data['obj_type'].lower().replace('_',' ')
                      #  if tailtype == "misc":
                     #       tailtype = "miscellaneous"
                        sentence = data['Context']
                        relation = rel2labelword[data['relation']]
                        if "schema" in args.prompt:
                          #  prompt += "Context: " + sentence + " The relation between " + headtype + " '" + head + "' and " + tailtype + " '" + tail + "' in the context is " + relation + ".\n"
                            prompt += "Context: " + sentence + " The relation between "

                        else:
                            prompt += "Context: " + sentence + " The relation between '" + head + "' and '" + tail + "' in the context is " + relation + ".\n"
                for rel in rels:
                    random.shuffle(generated_list[rel])
                    kshot = generated_list[rel][:args.k_ge]
                    for data in kshot:
                        head = data['subject']
                       # headtype = data['subj_type'].lower().replace('_',' ')
                     #   if headtype == "misc":
                       #     headtype = "miscellaneous"
                        tail = data['object']
                     #   tailtype = data['obj_type'].lower().replace('_',' ')
                      #  if tailtype == "misc":
                     #       tailtype = "miscellaneous"
                        sentence = data['Context']
                        relation = rel
                        if "schema" in args.prompt:
                          #  prompt += "Context: " + sentence + " The relation between " + headtype + " '" + head + "' and " + tailtype + " '" + tail + "' in the context is " + relation + ".\n"
                            prompt += "Context: " + sentence + " The relation between "

                        else:
                            prompt += "Context: " + sentence + " The relation between '" + head + "' and '" + tail + "' in the context is " + relation + ".\n"
                testhead = input['subject']
             #   testheadtype = input['subj_type'].lower().replace('_',' ')
            #    if testheadtype == "misc":
            #        testheadtype = "miscellaneous"
                testtail = input['object']
              #  testtailtype = input['obj_type'].lower().replace('_',' ')
              #  if testtailtype == "misc":
             #       testtailtype = "miscellaneous"
                testsen = input['Context']
                if "schema" in args.prompt:
                    prompt += "Context: " + testsen + " The relation between "
                else:
                    prompt += "Context: " + testsen + " The relation between '" + testhead + "' and '" + testtail + "' in the context is "
                    # prompt += " The relation between '" + testhead + "' and '" + testtail + "' in the context '" + testsen + "' is "
                # print(prompt)
                url = 'http://gpt.choicelink.cn:999/completion'
                headers = {'Content-Type': 'application/json'}
                data = {
      "model": "gpt-3.5-turbo-instruct",
      "temperature": 0.6,
      "text": prompt,
      "max_tokens": 5
                }
              #  print(json.dumps(data))
                response = requests.post(url, headers=headers, data=json.dumps(data))
                retry =0
                while retry <10:
                  if response.status_code == 200:
                    response=response.json()
                    break
                  else:
                    time.sleep(10)
                    response = requests.post(url, headers=headers, data=json.dumps(data))
                    retry=retry+1
                    print("retrying\n")
                    print("data for retry:"+prompt+"\n")
                    print("response:"+response+"\n")
                resrel = response['choices'][0]['text'].strip().split('.')[0].lower()
                if resrel in labelword2rel:
                    truerel = rel2id[input['relation']]
                    predictrel = rel2id[labelword2rel[resrel]]
                    true.append(truerel)
                    res.append(predictrel)
                    input['pr'] = labelword2rel[resrel]
                    success.append(input)
                    f.writelines(json.dumps(input))
                    f.write('\n')
                elif ("city" in resrel) and (resrel.replace("city", "cities") in labelword2rel):
                    truerel = rel2id[input['relation']]
                    predictrel = rel2id[labelword2rel[resrel.replace("city", "cities")]]
                    true.append(truerel)
                    res.append(predictrel)
                    input['pr'] = labelword2rel[resrel.replace("city", "cities")]
                    success.append(input)
                    f.writelines(json.dumps(input))
                    f.write('\n')
                elif ("country" in resrel) and (resrel.replace("country", "countries") in labelword2rel):
                    truerel = rel2id[input['relation']]
                    predictrel = rel2id[labelword2rel[resrel.replace("country", "countries")]]
                    true.append(truerel)
                    res.append(predictrel)
                    input['pr'] = labelword2rel[resrel.replace("country", "countries")]
                    success.append(input)
                    f.writelines(json.dumps(input))
                    f.write('\n')
                elif ("province" in resrel) and (resrel.replace("province", "provinces") in labelword2rel):
                    truerel = rel2id[input['relation']]
                    predictrel = rel2id[labelword2rel[resrel.replace("province", "provinces")]]
                    true.append(truerel)
                    res.append(predictrel)
                    input['pr'] = labelword2rel[resrel.replace("province", "provinces")]
                    success.append(input)
                    f.writelines(json.dumps(input))
                    f.write('\n')
                else:
                    input['pr'] = resrel
                    nores.append(input)
                time.sleep(1)
          #  except ProtocolError as pe:
          #    print(str(pe))
          #    print("Encountered ProtocolError. Retrying after 10 seconds.")
         #    time.sleep(10)  # Sleep for 10 seconds
              #nores.append(input)
            except Exception as e:
                print(str(e))
                if e._message == 'You exceeded your current quota, please check your plan and billing details.':
                    break
                nores.append(input)
                time.sleep(30)
    print(f1_score(true, res, rel2id))
    if len(nores)!=0:
        json.dump(nores, open(os.path.join(args.output_nores, "no.json"),'w'))
    

