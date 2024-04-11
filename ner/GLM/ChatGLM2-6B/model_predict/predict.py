import os
import json
import docx
import torch
import logging
import datetime
from torch.nn import Module
from typing import Dict, Tuple, Union, Optional
from transformers import AutoConfig, AutoModel, AutoTokenizer


logging.basicConfig(
    level=logging.INFO,
     format='%(asctime)s %(levelname)-8s %(module)s[line:%(lineno)d]: >> %(message)s',
     datefmt='%Y-%m-%d %H:%M:%S'
     )

os.environ["CUDA_VISIBLE_DEVICES"] = "0"

model_path = "/data/xf2022/pretrained_model/chatglm2-6b-32k"
checkpoint_path = "/data2/fyj2023/project/ChatGLM2-6B/ptuning/output/gov1000_dbz_rawData20240306_1638/adgen-chatglm2-6b-32k-pt-128-2e-2/checkpoint-500"
# checkpoint_path = "/data/xf2022/projects/ChatGLM2-6B/ptuning/output/network_center20230914_2252/adgen-chatglm2-6b-32k-pt-128-1e-2/checkpoint-1350"
# 载入Tokenizer
tokenizer = AutoTokenizer.from_pretrained(model_path, trust_remote_code=True)

# 加载ptuning模型
config = AutoConfig.from_pretrained(model_path, trust_remote_code=True, pre_seq_len=128)
model = AutoModel.from_pretrained(model_path, config=config, trust_remote_code=True)
prefix_state_dict = torch.load(os.path.join(checkpoint_path, "pytorch_model.bin"))
new_prefix_state_dict = {}
for k, v in prefix_state_dict.items():
    if k.startswith("transformer.prefix_encoder."):
        new_prefix_state_dict[k[len("transformer.prefix_encoder."):]] = v
model.transformer.prefix_encoder.load_state_dict(new_prefix_state_dict)


# Comment out the following line if you don't use quantization
model = model.quantize(4)
model = model.cuda()
model = model.eval()


data_list = []
data_path = '/data2/fyj2023/project/ChatGLM2-6B/ptuning/data/government_procurement/dbz_data/test2.json'
with open(data_path, 'r') as fr:
    for line in fr.readlines():
        data = eval(line)
        data_list.append(data)

result_path = '/data2/fyj2023/project/ChatGLM2-6B/ptuning/output/gov1000_dbz_rawData20240306_1638/result/result_500.txt'
with open(result_path, 'w', encoding='utf-8') as fw:
    for i, data in enumerate(data_list):
        #if i % 10 == 0:
        logging.info(i)
       # response, history = model.chat(tokenizer, data['input'], history=[], temperature=0.05)
        response, history = model.chat(tokenizer,
                                    prompt,
                                    history=history,
                                    max_length=2048,
                                    top_p= 0.7,
                                    temperature= 0.95)
        result_dir= {}
        print(response)
        result_dir["labels"] = data['output']
        result_dir["predict"] = str(response)


logging.info(f"model path:{model_path}")
logging.info(f"checkpoint path:{checkpoint_path}")
logging.info(f"data path:{data_path}")
logging.info(f"result path:{result_path}")

# test_data = "从下文中提取字段，并在返回的content中以标准JSON格式返回。请按照以下要求提取字段： 1、返回的结果中，JSON字段名必须为：项目名称、项目编号、代理机构、采购方式、采购单位、采购单位联系地址、采购单位联系人姓名、采购单位联系电话、总预算、公告时间、所属地区、报名开始日期、报名结束日期、采购内容； 2、键为字段名，值为找到的文本，没找到的为null； 3、所属地区为项目的地区或采购单位所在地区； 4、金额不要换算，保留原格式和单位； 5、报名开始日期仅保留年月日； 6、不要额外增加文本中没有的内容； 7、不要对我的消息进行总结、复述、过度解释，不要反复多次的回复意思相近的话语； 8、只能从提供的文本中提取； 下面是需要提取的原文：（训练处）髋关节测试系统等专项设备采购竞争性磋商公告2023年07月04日 12:08 来源： 【打印】公告概要：公告信息：采购项目名称（训练处）髋关节测试系统等专项设备采购品目货物/专用设备/体育设备/其他体育设备采购单位上海市体育训练基地管理中心行政区域上海市公告时间2023年07月04日 12:08获取采购文件时间2023年07月04日至2023年07月11日每日上午:9:30 至 11:00 下午:13:30 至 17:00（北京时间，法定节假日除外）响应文件递交地点上海市中山南一路210号北大楼2楼203室（申朋招标）响应文件开启时间2023年07月14日 13:00响应文件开启地点上海市中山南一路210号北大楼2楼203室（申朋招标）预算金额￥73.080000万元（人民币）联系人及联系方式：项目联系人王燕项目联系电话021-63086383-8009采购单位上海市体育训练基地管理中心采购单位地址上海市崇明区陈家镇北沿公路300号采购单位联系方式资产部021-60199958代理机构名称上海申朋招标服务有限公司代理机构地址上海市中山南一路210号北大楼2楼203室（申朋招标）代理机构联系方式王燕021-63086383-8009项目概况（训练处）髋关节测试系统等专项设备采购 采购项目的潜在供应商应在上海市中山南一路210号北大楼2楼203室（申朋招标）获取采购文件，并于2023年07月14日 13点00分（北京时间）前提交响应文件。一、项目基本情况项目编号：SH-SP2023-236项目名称：（训练处）髋关节测试系统等专项设备采购采购方式：竞争性磋商预算金额：73.0800000 万元（人民币）采购需求：项目名称：（训练处）髋关节测试系统等专项设备采购项目编号： SH-SP2023-236项目主要要求：项目名称：（训练处）髋关节测试系统等专项设备采购；项目类型：货物类预算金额：73.08万元（超过预算及各分项最高限价的投标按无效投标处理）数量：1批（详见货物清单）交货期：合同签订后3个月；质保期： 2年；（具体技术要求详见磋商文件。）合同履行期限：交货期：合同签订后3个月本项目( 不接受 )联合体投标。二、申请人的资格要求：1.满足《中华人民共和国政府采购法》第二十二条规定；2.落实政府采购政策需满足的资格要求：本项目执行政府采购有关支持节能产品、环境认证产品以及支持中小企业、福利企业、监狱企业等的政策规定。3.本项目的特定资格要求：(1) 符合《中华人民共和国政府采购法》第二十二条规定条件，未被列入&ldquo;信用中国&rdquo;网站(www.creditchina.gov.cn)失信被执行人名单、重大税收违法案件当事人名单和中国政府采购网(www.ccgp.gov.cn)政府采购严重违法失信行为记录名单的供应商；(2) 单位负责人为同一人或者存在直接控股、管理关系的不同供应商，不得参加同一合同项下的政府采购活动；为本项目提供整体设计、规范编制或者项目管理、监理、检测等服务的供应商，不得参加本项目的采购活动；(3) 法人依法设立的分支机构以自己的名义参与投标时，应提供依法登记的相关证明材料和由法人出具的授权其分支机构在其经营范围内参加政府采购活动并承担全部民事责任的书面声明。法人与其分支机构不得同时参与同一项目的采购活动；(4) 供应商须具有独立法人资格；(5) 本项目面向大、中、小、微型等各类供应商采购；(6) 本项目不接受联合体投标；(7) 本项目不得分包及转包。(8) 本项目部分产品可接受进口产品（详见货物清单）。三、获取采购文件时间：2023年07月04日 至 2023年07月11日，每天上午9:30至11:00，下午13:30至17:00。（北京时间，法定节假日除外）地点：上海市中山南一路210号北大楼2楼203室（申朋招标）方式：根据公告要求售价：￥700.0 元（人民币）四、响应文件提交截止时间：2023年07月14日 13点00分（北京时间）地点：上海市中山南一路210号北大楼2楼203室（申朋招标）五、开启时间：2023年07月14日 13点00分（北京时间）地点：上海市中山南一路210号北大楼2楼203室（申朋招标）六、公告期限自本公告发布之日起3个工作日。七、其他补充事宜磋商文件的获取：报名资料如下：营业执照（三证或五证合一）（需提供清晰扫描件加盖公章）；法定代表人证明或者法定代表人授权委托书（格式要求：法定代表人签字或盖章、被授权人签字、加盖企业公章）（需提供清晰扫描件）；法定代表人及被授权人身份证（需提供清晰扫描件）。报名要求如下（以上包件均适用）：合格的供应商可于2023-07-04 17:00:00本公告发布之日起至2023-07-11 17:00:00截止，（上午9：00-11：00、下午13：30-17：00，双休日、节假日除外）将上述材料扫描件发送至1536718445@qq.com进行初审（邮件中请写明公司全称、项目负责人姓名、手机号码，以便代理机构项目负责人联系），代理机构将邮件回复通知初审结果，通过初审的供应商在上述规定的时间支付报名费后可获取磋商文件。供应商必须携带上述证照原件及盖章复印件一套到招标代理机构进行现场复核。现场复核地点：上海市中山南一路210号北大楼2楼203室（上海申朋招标服务有限公司）报名及磋商文件费用为： 700元、售后概不退还。账户名称：上海申朋招标服务有限公司开户银行：招商银行股份有限公司上海中山支行账号：121931352110401供应商应在电汇汇款附言中注明：项目编号、投标公司名称。未在规定时间按以上流程报名和购买竞争性磋商文件的供应商，其报名将被拒绝。磋商响应截止及磋商时间：磋商响应截止时间: 2023-07-14 13:00（北京时间），迟到或不符合规定的响应文件恕不接受。磋商谈判时间：2023-07-14 14:00。磋商响应文件递交地点和磋商地点：地点为: 上海市中山南一路210号北大楼2楼203室（申朋招标）八、凡对本次采购提出询问，请按以下方式联系。1.采购人信息名 称：上海市体育训练基地管理中心地址：上海市崇明区陈家镇北沿公路300号联系方式：资产部021-601999582.采购代理机构信息名 称：上海申朋招标服务有限公司地 址：上海市中山南一路210号北大楼2楼203室（申朋招标）联系方式：王燕021-63086383-80093.项目联系方式项目联系人：王燕电 话： 021-63086383-8009"
# start_time = datetime.datetime.now()

# 打开 Word 文档
# doc = docx.Document('/data/xf2022/projects/ChatGLM2-6B/ptuning/data/government_procurement/招标文件/CLF0123GZ03ZC27/CLF0123GZ03ZC27-招标文件.docx')  # 替换为你的 Word 文档路径
# 读取文档中的文本内容
# text = []
# for paragraph in doc.paragraphs:
#     text.append(paragraph.text)
# 输出文本内容
# for line in text:
#     print(line)
# test_data = "\n".join(text)
# test_data = test_data[:20000]

# prefix = "下面是一份招标文件全文，请帮我抽取出其中采购需求的部分，输出该部分的字符串位置即可。以下是招标文件全文："

# response, history = model.chat(tokenizer, prefix+test_data, history=[])
# end_time = datetime.datetime.now()
# logging.info(response)
# logging.info('spend time:', str(end_time - start_time))


# nohup python predict.py>>./log/gov_test_result.log &
