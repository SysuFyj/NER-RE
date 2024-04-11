import json
import re

def extract_info(data):
    result = {}
    output_data=data["output"]
    input_text=data["input"]
    # 转换output为json格式
    output_json = json.loads(output_data)
    
    error_file_path = "../error/error_pre/"  
    
    for item in output_json.get('中标信息', []):
        zbdw = item.get('中标单位', None)
        zbjine = item.get('中标金额', None)
        # 检查中标单位是否在input中完整出现
        if zbdw and zbdw != "null":
            # if (zbdw not in input_text) or re.match(r'^[\u4e00-\u9fa5（）()]+$', zbdw):
            if zbdw not in input_text:
                with open(error_file_path+'中标单位_与原文不一致.txt', 'a', encoding='utf-8') as f:
                    f.write(str(data) + '\n')
            elif not re.match(r'^[\u4e00-\u9fa5（）()《》a-zA-Z]+$', zbdw):
                if "联合体" not in zbdw:
                    with open(error_file_path+'中标单位_格式错误.txt', 'a', encoding='utf-8') as f:
                        f.write(str(data) + '\n')
                
        # 检查中标金额格式
        if zbjine and zbjine != "null":
            if not re.match(r'^\d{1,3}(,\d{3})*(\.\d{2})?$', zbjine):
                with open(error_file_path+'中标金额.txt', 'a', encoding='utf-8') as f:
                    f.write(str(data) + '\n')

        
    
    result['代理机构'] = output_json.get('代理机构', None)
    result['评委名单'] = output_json.get('评委名单', None)
    result['采购单位联系电话'] = output_json.get('采购单位联系电话', None)
    # 检查评委名单是否满足要求
    if result['评委名单']:
        for name in result['评委名单']:
            if not re.match(r'^[\u4e00-\u9fa5]{2,}$', name):
                with open(error_file_path+'评委名单.txt', 'a', encoding='utf-8') as f:
                    f.write(str(data) + '\n')
    else:
        if "评审委员会" in input_text or "磋商小组成员名单" in input_text or "评审专家名单" in input_text or "评审专家（单一来源采购人员）名单" in input_text:
                if "评审专家（单一来源采购人员）名单：\n/" not in input_text:
                    with open(error_file_path+'评委名单_可能未成功识别.txt', 'a', encoding='utf-8') as f:
                        f.write(str(data) + '\n')        
    
    # 检查其他信息是否在input中出现
    for key in ['采购单位联系人姓名', '采购单位联系地址', '采购单位','代理机构']:
        value = output_json.get(key, None)
        if value and value != 'null' and value not in input_text:
            with open(error_file_path+key + '.txt', 'a', encoding='utf-8') as f:
                f.write(str(data) + '\n')
    
    # 检查项目编号格式
    xmbh = output_json.get('项目编号', None)
    if xmbh  and xmbh!="null" and (re.search(r'[：:]|\(|\)', xmbh ) or xmbh not in input_text):
        with open(error_file_path+'项目编号.txt', 'a', encoding='utf-8') as f:
            f.write(str(data)  + '\n')
    
    return "end"
raw_data_path = '../data/data/full_data.json'
raw_data_list = []
with open(raw_data_path, 'r',encoding='utf-8') as f_raw:
    for line in f_raw.readlines():
        raw_data_list.append(eval(line))
# 输入数据
# for data in raw_data_list: 
#     try:
#         result = extract_info(data)
#     except:
#         print(data)
for data in raw_data_list: 
    try:
        result = extract_info(data)
    except:
        print(data)