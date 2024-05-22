import os
import re

def extract_content_from_txt(folder_path):
    # 初始化一个空字典来存储结果
    extracted_content = {}

    # 遍历指定文件夹中的所有txt文件
    for file_name in os.listdir(folder_path):
        if file_name.endswith('.txt'):
            file_path = os.path.join(folder_path, file_name)
            
            # 读取txt文件内容
            with open(file_path, 'r', encoding='utf-8') as file:
                content = file.read()
                
                # 使用正则表达式提取Study Description之后到Study Organism之前的内容
                match = re.search(r'Study Description(.*?)Study Organism', content, re.DOTALL)
                if match:
                    extracted_text = match.group(1).strip()
                    extracted_content[file_name] = extracted_text

    return extracted_content

# 使用示例
folder_path = '/Users/hnfd/Desktop/zhanghan/UvA/Thesis/AUMC/All-txt'
result = extract_content_from_txt(folder_path)
print(result)