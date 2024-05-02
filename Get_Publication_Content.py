import requests
import xml.etree.ElementTree as ET
import json

def search_uid(title):
    base_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"
    params = {
        "db": "pubmed",  # choose pubmed database
        "term": title,
        "retmode": "json"
    }
    response = requests.get(base_url, params=params)
    data = response.json()
    uids = data['esearchresult']['idlist']
    return uids

def fetch_methods(uid):
    base_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi"
    params = {
        "db": "pubmed",
        "id": uid,
        "retmode": "xml",  # xml may contain richer
        "rettype": "methods"
    }
    response = requests.get(base_url, params=params)
    if response.status_code == 200:
        # 解析 XML 数据
        root = ET.fromstring(response.text)
        
        # 寻找 <AbstractText> 标签，假设我们关心的是所有摘要文本
        abstract_texts = root.findall('.//AbstractText')
        
        # 将所有摘要文本拼接成一个字符串
        abstract = " ".join([text.text for text in abstract_texts if text.text is not None])
        
        return abstract
    else:
        return "Failed to fetch data"  # 返回错误信息
    

def process_titles_and_fetch_abstracts(titles):
    results = {}
    for title in titles:
        uids = search_uid(title)
        if uids:
            abstract = fetch_methods(uids[0])  # assuming we take the first UID found
            results[title] = abstract
        else:
            results[title] = "No UID found or failed to fetch abstract"
    
    # 存储结果到 JSON 文件
    with open('results.json', 'w') as f:
        json.dump(results, f, indent=4)

    return results
