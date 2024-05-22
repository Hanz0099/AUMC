def format_retrieved_documents(documents):
    for index, doc in enumerate(documents):
        try:
            print(f"Document {index + 1} Type: {type(doc)}")
            print(doc)  # 这将打印文档的整个字典，用于调试
            lines = doc['page_content'].split('\n')
            for line in lines:
                if line.strip() == '':  # 跳过空行
                    continue
                parts = line.split('\t')
                parts = [part.strip() for part in parts if part.strip() != '']
                if len(parts) > 1:  # 避免打印空行或没有分隔符的行
                    print(f"{parts[0]:30}: {' '.join(parts[1:])}")
            print("\n" + "="*50 + "\n")
        except Exception as e:
            print(f"Error processing document {index + 1}: {e}")

# 示例用法，确保数据结构正确
documents = [
    {
        "page_content": (
            "Study Author List\tCabirol A, Haase A\t\t\t\n"
            "Study PMC ID\tPMC6920473\t\t\t\t\n"
            # 省略了其他部分以保持简洁
            "Experiment Imaging Method\ttwo-photon laser scanning microscopy"
        ),
        "metadata": {'source': '/Users/hnfd/Desktop/zhanghan/UvA/Thesis/AUMC/All-txt/idr0075-study.txt'}
    },
    # 添加更多文档
]

# 直接调用函数，不需要打印返回值，因为函数没有返回值，它直接输出结果
format_retrieved_documents(documents)