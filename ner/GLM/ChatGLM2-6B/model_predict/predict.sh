export CUDA_VISIBLE_DEVICES=0,1,2,3,4
#python sci_er_predict.py
nohup python dbz_index.py  >> ./nohup.txt
# 下面给出的文本是政府采购招标项的公告内容，请从中提取出特定字段，并以json的格式返回，具体的格式如：{项目编号:__, 代理机构:__, 采购方式:__, 采购单位:__, 采购单位联系地址:__, 采购单位联系电话:__, 采购单位联系人姓名:__, 所属地区:__, 总预算:__, 报名开始日期:__, 报名结束日期:__}。请按照以下要求提取字段： 1、只能从原文中提取字段值，没找到的为null； 2、所属地区为项目的地区或采购单位所在地区； 3、报名结束时间是获取采购文件截止时间；
