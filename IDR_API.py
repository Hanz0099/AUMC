import requests
import json

def save_project_data(project_ids):
    MAP_URL = "https://idr.openmicroscopy.org/webclient/api/annotations/?type=map&{type}={project_id}"
    saved_files = []
    
    for project_id in project_ids:
        qs = {'type': 'project', 'project_id': project_id}
        url = MAP_URL.format(**qs)
        response = requests.get(url)
        
        if response.status_code == 200:
            data = response.json()
            filename = f'project_{project_id}.json'
            with open(f'project_{project_id}.json', 'w') as f:
                json.dump(data, f, indent=4)
                saved_files.append(filename)
            print(f'Successfully saved data for project_id {project_id}')
        else:
            print(f"Failed to fetch data for project_id {project_id}")
    return saved_files



def extract_publication_titles_from_file(json_file):
    # 打开 JSON 文件并加载数据
    with open(json_file, 'r', encoding='utf-8') as file:
        json_data = json.load(file)
    
    # 现在 json_data 是一个字典，可以安全地传递给 extract_publication_titles
    return extract_publication_titles(json_data)



def extract_publication_titles(json_data):
    # 创建一个空字典来存储标题和索引
    publication_titles = " "

    # 解析 JSON 数据中的 'annotations' 部分
    annotations = json_data.get('annotations', [])
    
    # 遍历每个注解条目
    for annotation in annotations:
        # 检查每个注解中的 'values' 列表
        values = annotation.get('values', [])
        # 遍历 'values' 列表中的每一项
        for item in values:
            # 检查是否是 'Publication Title'
            if item[0] == "Publication Title" or item[0] == "Study Title":
                # 如果是，则存储标题和索引
                publication_titles = item[1]
                break

    return publication_titles

