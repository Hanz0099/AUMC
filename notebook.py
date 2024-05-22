template = (
        "Please provide the answer to the question." 
        "After answering, identify the document where the answer is located" 
        "and provide the 'Study Description' and 'Experiment Description' from that document. "
        "Additionally, please provide the 'Experiment Description' from three other related documents."
    )

    prompt = """ The following are users with an AI assistant. 
    AI assistant will provide the answer to the question.
    and identify the document where the answer is located
    and provide the 'Study Description' and 'Experiment Description' from that document. 
    Additionally, please provide the 'Experiment Description' from three other related documents.
    Here are some examples:

    user: what's the study type of "Automated quantification of synaptic boutons reveals their 3D distribution in the honey bee mushroom body"
    AI: 
    The study type of "Automated quantification of synaptic boutons reveals their 3D distribution in the honey bee mushroom body" is an imaging method study.

    You can find more information in idr-0075. The experiment is about: Experiment Description	To study the spatial distribution of synaptic complexes called microglomeruli in the mushroom body neuropils of the honeybee brain, those structures where imaged by two-photon microscopy. A data analysis method was developed to automatically obtain the loci of those structures from large volume samples allowing to analyse their 3D density distribution.
    And the related study is "Automated quantification of synaptic boutons reveals their 3D distribution in the honey bee mushroom body", it is about: Synaptic boutons are highly plastic structures undergoing experience-dependent changes in their number, volume, and shape. Their plasticity has been intensively studied in the insect mushroom bodies by manually counting the number of boutons in small regions of interest and extrapolating this number to the volume of the mushroom body neuropil. Here we extend this analysis to the synaptic bouton distribution within a larger subregion of the mushroom body olfactory neuropil of honey bees (Apis mellifera). This required the development of an automated method combining two-photon imaging with advanced image post-processing and multiple threshold segmentation. The method was first validated in subregions of the mushroom body olfactory and visual neuropils. Further analyses in the olfactory neuropil suggested that previous studies overestimated the number of synaptic boutons. As a reason for that, we identified boundaries effects in the small volume samples. The application of the automated analysis to larger volumes of the mushroom body olfactory neuropil revealed a corrected average density of synaptic boutons and, for the first time, their 3D spatial distribution. This distribution exhibited a considerable heterogeneity. This additional information on the synaptic bouton distribution provides the basis for future studies on brain development, symmetry, and plasticity.
    ”“”

    prompt = PromptTemplate.from_template(template)



    """ def format_context(document):
    # 假设document是一个对象，有page_content和metadata属性
    content = document.page_content  # 获取页面内容
    source = document.metadata.get('source', '未知来源')  # 获取元数据中的来源信息
    
    # 清理和格式化内容
    lines = content.split('\n')
    clean_lines = [line.strip() for line in lines if line.strip() != '']
    formatted_content = '\n'.join(clean_lines[:10])  # 仅展示前10行内容
    
    return f"Source: {source}\nAbstract:\n{formatted_content}" """