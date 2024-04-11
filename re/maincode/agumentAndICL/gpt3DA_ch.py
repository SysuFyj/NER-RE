import json
import random
from tqdm import tqdm
import argparse
import os
import requests
import traceback


entity_types = {
    "tacrev": ['URL', 'LOCATION', 'IDEOLOGY', 'CRIMINAL CHARGE', 'TITLE', 'STATE OR PROVINCE', 'DATE', 'PERSON', 'NUMBER', 'CITY', 'DURATION', 'CAUSE OF DEATH', 'COUNTRY', 'NATIONALITY', 'RELIGION', 'ORGANIZATION', 'MISCELLANEOUS'],
    "SciERC": ['Generic', 'Material', 'Method', 'Metric', 'OtherScientificTerm', 'Task'],
    "retacred": ['IDEOLOGY', 'ORGANIZATION', 'URL', 'PERSON', 'DURATION', 'COUNTRY', 'LOCATION', 'NATIONALITY', 'TITLE', 'RELIGION', 'NUMBER', 'CITY', 'CAUSE OF DEATH', 'DATE', 'STATE OR PROVINCE', 'CRIMINAL CHARGE'],
    "tacred": ['COUNTRY', 'IDEOLOGY', 'LOCATION', 'DATE', 'PERSON', 'NATIONALITY', 'RELIGION', 'CITY', 'MISCELLANEOUS', 'CAUSE OF DEATH', 'TITLE', 'URL', 'NUMBER', 'ORGANIZATION', 'STATE OR PROVINCE', 'DURATION', 'CRIMINAL CHARGE'],
    'cailian':['服务','属性','职责','方法','标准']
}
relation_dict={
    '服务':'强调[subject]产品目前能提供[object]服务。',
'职责':'强调[subject]人员或岗位需要承担的职责与工作任务[object]。',
'属性':'强调[subject]产品或人具有的特征或性质[object]',
'方法':'为达到目的[subject]所采用的方法[object]。',
'标准':'某种行为[subject]需要遵循的具体标准或某个依据[object]。'
}
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


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--demo_path', '-dp', type=str, required=True, help="The directory of demonstration data.")
    parser.add_argument('--output_dir', type=str, required=True, help="The output directory of generated data.")
    parser.add_argument('--dataset', type=str, required=True, choices=["tacred", "tacrev", "retacred","cailian"])
    parser.add_argument('--k', type=int, default=3, help="k-shot demonstrations")
    parser.add_argument('--num', type=int, default=3, help="generated number")
    args = parser.parse_args()
    
    input_file = args.demo_path
    datasetname = args.dataset
    output_file = os.path.join(args.output_dir, "generated.json")
    data = []
    label_list = {}
    with open(input_file,'r', encoding='utf-8') as f:
        data = json.load(f)
    random.shuffle(data)
    for line in data:
        rel = line['relation']
        if rel not in label_list:
            label_list[rel] = [line]
        else:
            label_list[rel].append(line)


    '''
 系抽取数据集中的样本包含一种关系(relation)、一个上下文(Context)，以及上下文中的一对头实体(subject)和尾实体(object)。头实体和尾实体之间存在着特定的关联，二者必须直接从原文中提取，下文 中是关系抽取数据集中的样例. 这些样例围绕关系 '方法', 关系k的含义为'为达到目的[subject]所采用的方法[object]。':
Relation: 方法. Context: 可通过监控面板控制通风柜调节窗的升降及停止。 Head Entity: 通风柜调节窗的升降及停止. Tail Entity: 监控面板控制. .
Relation: 方法. Context: 乙方要在每次餐后进行桌面、地面及所有设备的清洁消毒工作，保持餐厅整洁。 Head Entity: 保持餐厅整洁. Tail Entity: 清洁消毒工作. .
Relation: 方法. Context: 梯度PCR仪支持通过图文显示模式实时显示运行状态。 Head Entity: 实时显示运行状态. Tail Entity: 图文显示模式. .
按照案例的格式为我生成4组更多围绕关系 '方法'的案例.
    '''

    with open(output_file,'a') as f:
        for k,v in tqdm(label_list.items()):
            prompt = "假设你是一个数据生成专家，关系抽取数据集中的样本包含一种关系(relation)、一个上下文(Context)，以及上下文中的一对Head Entity和Tail Entity。Head Entity和Tail Entity之间存在着特定的relation，二者必须直接从原文中提取，如果必要的话，Head Entity和Tail Entity可以包括动词部分" + \
             "', 关系'" + k + "'的含义为'"+relation_dict[k] +\
            ". 下面的样例围绕关系 '" + k +"'展开:\n"
            for i in range(args.k):
                sample = "Relation: " + k + ". Context: " + v[i]['Context'] + ' ' + "Head Entity: " + v[i]['subject'] + '. ' + "Tail Entity: " + v[i]['object'] +".\n"
                prompt = prompt + sample
            prompt = prompt + "按照上述格式生成"+str(args.num)+"组更多围绕关系 '" + k + "'的数据，注意Context部分的句法最好不要和原案例相同"
            data = {
          "model": "gpt-3.5-turbo-instruct",
          "temperature": 0.6,
          "text": prompt,
          "max_tokens": 3000
                }
            url = 'http://gpt.choicelink.cn:999/completion'
            headers = {'Content-Type': 'application/json'}
            response = requests.post(url, headers=headers, data=json.dumps(data)).json()
            res = response['choices'][0]['text'].split('\n')
            for line in res:
                if len(line) == 0:
                    continue
                try:
                    DAdata = {}
                    data1 = line.split('Relation:')[-1].strip()
                    onepoint = data1.index('.')
                    relation = data1[:onepoint]
                    if relation == k:
                        relation = k
                    else:
                        continue
                    # text
                    data2 = data1.split('Context:')[-1].strip()
                    data2lower = data2.lower()
                    if "head entity:" in data2lower:
                        textend = data2lower.index('head entity:')
                        text = data2[:textend].strip()
                        data3 = data2[textend+len('head entity:'):].strip()
                    else:
                        continue
                    DAdata['Context'] = text
                    headpoint=data3.index('.')
                    truehead=data3[:headpoint]
                    data4=data3.split('Tail Entity:')[-1].strip()
                    tailpoint=data4.index('.')
                    truetail=data4[:tailpoint]
                    DAdata['subject'] = truehead
                    DAdata['object'] = truetail
                    DAdata['relation'] = k
                    f.writelines(json.dumps(DAdata, ensure_ascii=False))
                    f.write('\n')
                except Exception as e:
                    continue
                    
