import re

#还有地区和电话

# def torch_gc():
#     if torch.cuda.is_available():
#         with torch.cuda.device(CUDA_DEVICE):
#             torch.cuda.empty_cache()
#             torch.cuda.ipc_collect()
result_path='../result/result_regex.txt'
error_path='../error/regex/err_regex.txt'
def get_dictionary(items):
    dictionary = {}
    for item in items:
        try:
            key, value = item.split('：', 1)
            dictionary[key] = value
        except:
            pass    
    return dictionary
def format_float(num):
    # 将浮点数格式化为保留两位小数
    formatted_num = '{:.2f}'.format(num)
    
    # 将整数部分从小数点开始每三位数字一个逗号
    integer_part, decimal_part = formatted_num.split('.')
    integer_part_with_commas = '{:,}'.format(int(integer_part))
    
    # 拼接整数部分和小数部分
    formatted_num_with_commas = integer_part_with_commas + '.' + decimal_part
    
    return formatted_num_with_commas

def get_name(text):
    pattern = r'采购经办人|采购单位联系方式|采购联系人'
    matches = re.finditer(pattern, text)
    name = 'null'

    for match in matches:
        name = text[match.end()+1:match.end()+7]

        name = re.split('\n| ', name.strip())[0]
        hanzi = r'[\u4e00-\u9fff]+'  # 匹配一个或多个汉字
        name = ''.join(re.findall(hanzi, name))
        if name != None: break
    return name
def get_pN(text):
    pattern = r"采购人信息[^\n]*\n[^\n]*\n[^\n]*\n联系方式：(\d+[ \/\-\d]+)"
    match = re.search(pattern, text)

    if match:
    # 获取匹配结果
        contact_info = match.group(1)
        return contact_info
    else:
        return None
def get_gys(text):
    index = str.find(text,"供应商名称")
    result = text[index + len("供应商名称")]
    if(result!="："):
        pattern = r'供应商名称[^\n]*\n[^\n]*\n[^\n]*\n([^\n]*)\n'
        matches = re.finditer(pattern, text)
        extracted_texts = [match.group(1).strip() for match in matches]
        pattern_jine = re.compile(r'供应商名称[^\n]*\n[^\n]*\n[^\n]*\n[^\n]*\n[^\n]*\n([^\n]*)\n', re.DOTALL)
        matches_jine = pattern_jine.finditer(text)
        extracted_texts_jine = [match.group(1).strip() for match in matches_jine]
        jine=[]
        for line in extracted_texts_jine:
            try:
                line=line.strip()
                i = extract_and_convert_amount(line)
                jine.append(i)
            except:
                jine.append(-1)
        i=0
        res_dict={}
        for gys in extracted_texts:
            if i<len(jine):
                if jine[i]==-1:
                    res_dict[gys]="null"
                res_dict[gys]=format_float(jine[i])
                i+=1
            else:
                res_dict[gys]="null"         
    else:
        pattern1 = re.compile(r'供应商名称：([^\n]*)\n', re.DOTALL)
        matches = pattern1.finditer(text)
        extracted_texts = [match.group(1).strip() for match in matches]
        pattern_jine = re.compile(r'供应商名称：[^\n]*\n[^\n]*\n([^\n]*)\n', re.DOTALL)
        matches_jine = pattern_jine.finditer(text)
        extracted_texts_jine = [match.group(1).strip() for match in matches_jine]
        jine=[]
        for line in extracted_texts_jine:
            try:
                line=line[line.find("：")+ 1:].strip()
                i = extract_and_convert_amount(line)
                jine.append(i)
            except:
                jine.append(-1)
        i=0
        res_dict={}
        for gys in extracted_texts:
            if i<len(jine):
                if jine[i]==-1:
                    res_dict[gys]="null"
                res_dict[gys]=format_float(jine[i])
                i+=1
            else:
                res_dict[gys]="null"
    res_list=[]
    for key, value in res_dict.items():
        dict_zbxx={}
        dict_zbxx["中标单位"]=key
        dict_zbxx["中标金额"]=value
        res_list.append(dict_zbxx)
    return res_list

def extract_and_convert_amount(text):
    # 找到文本中的所有数字
    numbers = [char for char in text if char.isdigit() or char == '.']
    amount_str = ''.join(numbers)
    
    # 判断文本中是否包含"万"，如果包含则乘以10000
    if '万' in text:
        amount = float(amount_str) * 10000
    else:
        amount = float(amount_str)
    return amount     
def replace_name(predict:str,input:str): 
    input = input[262:]
    s2 = "0123456789"
    if predict == "null": # predict 为null
        t = input.find("采购单位联系方式")
        if t != -1 and input[t+13] in s2: # 含有联系方式
            if input[t+9] not in s2: # 含有联系人姓名
                if input[t+11] in s2:
                        predict = input[t+9:t+11]
                else: # 联系人名三个字
                    predict = input[t+9:t+12]
    return predict

def get_projnum(text):
    re_str = r'项目编号'
    matches = re.finditer(re_str, text)
    for match in matches:
        num = text[match.end()+1:match.end()+20]
        ss = re.split('\n| ',num.strip())[0]
        pattern = '[0-9A-Za-z-]'
        num = ''.join(re.findall(pattern, ss))

        return num
    
def get_caigou_way(text):
    # re_str = r'采购方式'
    # matches = re.finditer(re_str, text)
    #单一来源>
    way = '竞争性磋商'
    if '公开招标' in text:
        return "公开招标"
    elif '单一来源' in text:
        return "单一来源"
    elif '竞争性谈判' in text:
        return "竞争性谈判"
    elif '竞争性磋商' in text:
        return "竞争性磋商" 
    else :
        return "其他采购" 
    # for match in matches:
    #     way = text[match.end()+1:match.end()+7]
    #     ss = re.split('\n| ', way.strip())[0]
    #     hanzi = r'[\u4e00-\u9fff]+'  # 匹配一个或多个汉字
    #     way = ''.join(re.findall(hanzi, ss))
        
    #     return way
    
def search_agency(result, text):
    if result == "null":
        pattern = r'代理机构'
        matches = re.finditer(pattern, text)
        right = ""
        for match in matches:
            right_window = text[match.end():match.end()+20]
            segments = re.split('\n|：',right_window)
            for seg in segments:
                if seg.strip().endswith("公司") or seg.strip().endswith("中心") or seg.strip().endswith("院"):
                    return seg
    return result

def get_lxr_name(input:str):
    name = "null"  
    input = input[262:]
    place0 = input.find("采购人信息")
    if place0 != -1:
        ss0 = input[place0:place0+80]
        ss0 = ss0.replace(" ","")
        place1 = ss0.find('联系人')
        if place1 != -1:
            name = ss0[place1:place1+10]
            name = re.split('：|\n|，| ', name)[1]
            hanzi = r'[\u4e00-\u9fff]+'  # 匹配一个或多个汉字
            name = ''.join(re.findall(hanzi, name))
        else:
            place2 = ss0.find('联系方式')
            if place2 != -1:
                name = ss0[place2:place2+10]
                name = re.split('：|\n|，', name)[1]
                hanzi = r'[\u4e00-\u9fff]+'  # 匹配一个或多个汉字
                name = ''.join(re.findall(hanzi, name))
            else:
                place3 = ss0.find('采购经办人')
                if place3 != -1:
                    name = ss0[place3:place3+10]
                    name = re.split('：|\n|，', name)[1]
                    hanzi = r'[\u4e00-\u9fff]+'  # 匹配一个或多个汉字
                    name = ''.join(re.findall(hanzi, name))
        if name=='':name='null'
    return name

def find_jine(input:str):
    t3 = str(input).find("预算金额")
    txt = input[t3:t3+100]
    pattern = r"[\d,]*\.?\d+|\d+"
    match = re.search(pattern, txt)
    if match:
        last_index = match.end()
        num = match.group()
        num = num.replace(",",'')
        num = eval(num)
        if txt[last_index] == "万":
            num = num*10000
        predict = format(num,"0.2f")
        predict=format(predict,",")
    else:
        predict = 'null'

    if predict == "0.00":
        predict = "null"

    return predict


def get_pingwei(input:str):
    t3 = str(input).find("评审专家")
    txt = input[t3:t3+100]
    pattern = re.compile(r'评审专家[^\n]*\n(.*?)\n', re.DOTALL)
    match = pattern.search(input)

    if match:
        extracted_content = match.group(1)
        extracted_list = re.split(r'[ 、]', extracted_content)
        extracted_list = [item for item in extracted_list if item]
        return extracted_list


def get_dizhi(text):
    def get_rightwindows(re_str,text):
        matches = re.finditer(re_str, text)
        match_str = ""
        for match in matches:
            match_str = match_str + "\n" + text[match.end():match.end()+100]
        return match_str.replace(" ","")

    #采购人信息 名称：……\n地址：……\n
    def get_caigourendizhi(text):
        re_str = r'采购人信息|采购人|采购方信息|请按以下方式联系。\n'
        right = get_rightwindows(re_str,text)
        match = re.search(r'地址：',right)
        if match:
            dizhi_str = right[match.end():]
            match = re.search(r'\n',dizhi_str)
            if match:
                dizhi_str = dizhi_str[:match.start()]
                return dizhi_str

    #采购单位地址\n……\n
    def get_danweidizhi(text):
        re_str = r'采购单位地址\n'
        right = get_rightwindows(re_str,text)
        match = re.search(r'\n',right)
        if match:
            dizhi_str = right[:match.start()]
            if len(dizhi_str) <= 1:
                right = right[match.end():]
                match = re.search(r'\n',right)
                if match:
                    dizhi_str = right[:match.start()]
                    return dizhi_str
            else:
                return dizhi_str
    dizhi = get_danweidizhi(text)
    if dizhi is None:
        dizhi = get_caigourendizhi(text)
    if dizhi is None:
        return 'null'
    return dizhi

def get_danwei(input:str):
    danwei = "null"  
    input0 = input[262:]
    pattern = r"采购.信息"
    matches = re.findall(pattern, input0)
    if len(matches) != 0:
        place0 = input0.find(matches[0])
        ss0 = input0[place0+1:place0 + 80].replace(" ", "")
        keywords = ['采购人', '采购单位', '名称']
        danwei = 'null'
        for keyword in keywords:
            place = ss0.find(keyword)
            if place != -1:
                danwei = ss0[place:place + 50]
                list=re.split('：|\n|，| ', danwei)
                for index, element in enumerate(list):
                    if keyword in element:
                        danwei = list[index+1].replace("(", "（").replace(")", "）")
                        break
                break
    else:
        danwei = 'null'
        keywords = ['采购单位', '采购人']
        for keyword in keywords:
            place = input.find(keyword)
            if place != -1:
                ss0 = input[place:place + 50].replace(" ", "")
                danwei = re.split('：|\n|，| ', ss0)[1].replace("(", "（").replace(")", "）").replace(keyword,"")
                danwei = danwei.replace("地址", "")
                break

    return danwei


raw_data_path = '../data/mod/full_data_mod.json'
raw_data_list = []
res_list=[]
with open(raw_data_path, 'r',encoding='utf-8') as f_raw:
    for line in f_raw.readlines():
        raw_data_list.append(eval(line))
# 输入数据
i=0

for data in raw_data_list: 
    try:
        text=data["input"]
        prompt=text[text.find("文本内容如下："):]
    # 获取预测字典
    
        predict_dict = {}
        predict_dict['采购方式'] = get_caigou_way(prompt)
    
        # 总预算
    # predict_dict['总预算'] = find_jine(prompt)

        # 采购单位
        predict_dict['采购单位'] = get_danwei(prompt[262:])
        predict_dict['评委名单'] = get_pingwei(prompt)
        predict_dict['中标信息'] = get_gys(prompt)
        

        # 采购单位联系人姓名
        predict_dict['采购单位联系人姓名'] = get_lxr_name(prompt)

        # 所属地区
        # place_name = predict_dict['所属地区']
        # shi_place = place_name.find('市')
        # if shi_place != -1 :
        # predict_dict['所属地区'] = place_name[:shi_place+1]

        # 采购单位联系电话
        # phone_number = predict_dict['采购单位联系电话']
        # predict_dict['采购单位联系电话'] = phone_number.split(' ')[0]

    #     # 项目编号
        re_num = get_projnum(prompt)
        # length = len(re_num)
        # if len(predict_dict['项目编号'])!= len(re_num) or re_num[:length]!=predict_dict['项目编号'][:length]:
        predict_dict['项目编号'] = re_num 

        # 采购单位联系地址
        predict_dict['采购单位联系地址'] = get_dizhi(prompt)
        predict_dict['采购单位联系电话']=get_pN(prompt)
        # 代理机构
        # if '分公司' in predict_dict['代理机构']:
        predict_dict['代理机构']=search_agency("null",prompt)
        predict_dict['所属地区']="null"
        # ss = predict_dict['代理机构']
        # place = ss.find('有限公司')
        # if place != -1: predict_dict['代理机构'] = ss[:place+4] 

    #     # 报名结束日期
    #     end_date = predict_dict['报名结束日期']
    #     if prompt.find('获取') == -1:
    #         predict_dict['报名结束日期'] = 'null'

        # 重新拼接
        new_response = ''
        res={
    }
        res['labels']=data["output"]
        res['predict']=str(predict_dict)
        i=i+1
        for key, value in predict_dict.items():
            if key!='中标信息' and value==None:
                value="null"
        res_list.append(res)
        if i%50==0:
            print(i)
    except:
        with open(error_path, 'w', encoding='utf-8') as fw:
            fw.write(str(data)+'\n')
        print("出错了"+str(i))
        pass

with open(result_path, 'w', encoding='utf-8') as fw:
    for res in res_list:
        fw.write(str(res)+'\n')
    # except:
    #     print("sb")
    #     pass
# with open(result_path, 'w', encoding='utf-8') as fw:
#     for i, data in enumerate(data_list):
#         if i % 10 == 0:
#             logging.info(i)
#         response, history = model.chat(tokenizer, data['input'], history=[], temperature=0.05)
#         result_dir= {}
#         result_dir["labels"] = data['instruction']
#         result_dir["predict"] = str(response)
#         fw.write(str(result_dir)+'\n')



