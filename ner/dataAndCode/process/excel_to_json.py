import pandas as pd
import json
import random
def excel_to_json(file_path):
    # 读取 Excel 文件
    df = pd.read_excel(file_path)
    
    # 将 DataFrame 转换为字典列表
    json_list = df.to_dict(orient='records')
    
    return json_list

# Excel 文件路径
excel_file_path = '../data/rl_data/generated.xlsx'

# 调用函数将 Excel 转换为 JSON 列表
json_data = excel_to_json(excel_file_path)

# # 打印 JSON 列表
# print(json_data[0])




# 对 JSON 列表进行 shuffle
random.shuffle(json_data)

# 计算划分的索引位置
split_index = int(len(json_data) * 0.7)

# 将 JSON 列表按照3:7的比例划分
train_data = json_data[:split_index]
test_data = json_data[split_index:]

# 打印划分后的数据
print("训练集：", train_data)
print("测试集：", test_data)

def write_json(json_list, output_file):
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(json_list, f, indent=4, ensure_ascii=False)

# 输出文件路径
output_file_path = '../data/rl_data/RawGenerated.json'
# train_file_path='../data/rl_data/TrainData.json'
# test_file_path='../data/rl_data/TestData.json'
# 调用函数将 JSON 列表写入到 JSON 文件中
write_json(json_data, output_file_path)
# write_json(train_data, train_file_path)
# write_json(test_data, test_file_path)