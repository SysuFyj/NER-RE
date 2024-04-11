import json
import pandas as pd

# 读取包含 JSON 的文件，并按行读取
with open("../data/rl_data/generated.json", "r", encoding='utf-8') as file:
    json_lines = file.readlines()

# 初始化一个空的列表来存储所有 JSON 对象的字典
json_data = []

# 遍历每行 JSON 数据并解析
for line in json_lines:
    print(line)
    json_obj = json.loads(line)
    json_data.append(json_obj)

# 将 JSON 数据转换为 DataFrame
df = pd.DataFrame(json_data)

# 将 DataFrame 写入 Excel 文件
df.to_excel("../data/rl_data/generated.xlsx", encoding='utf-8', index=False)
