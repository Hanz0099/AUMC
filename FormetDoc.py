def format_retrieved_documents(documents):
    result = "Starting document formatting...\n"
    for index, doc in enumerate(documents):
        try:
            result += f"Document {index + 1} Type: {type(doc)}\n"
            lines = doc.page_content.split('\n')
            
            for line in lines:
                if line.strip() == '':
                    continue
                parts = line.split('\t')
                parts = [part.strip() for part in parts if part.strip() != '']
                if len(parts) > 1:
                    result += f"{parts[0]:30}: {' '.join(parts[1:])}\n"
            result += "\n" + "="*50 + "\n"
        except AttributeError as e:
            result += f"Error in Document {index + 1}: Document object may not have 'page_content' attribute\n"
        except Exception as e:
            result += f"Error processing Document {index + 1}: {str(e)}\n"
    result += "Finished document formatting.\n"
    return result

""" # 示例用法
documents = [
    {
        "page_content": (
            "Study Author List\tCabirol A, Haase A\t\t\t\n"
            "Study PMC ID\tPMC6920473\t\t\t\t\n"
            "Study DOI\thttps://doi.org/10.1038/s41598-019-55974-2\t\t\t\n"
            "\t\t\t\t\n"
            "# Study Contacts\t\t\t\t\n"
            "Study Person Last Name\tHaase\t\t\t\n"
            "Study Person First Name\tAlbrecht\t\t\t\n"
            "Study Person Email\talbrecht.haase@unitn.it\t\t\t\n"
            "Study Person Address\tUniversity of Trento, piazza Manifattura 1, 38068 Rovereto, Italy\t\t"
            "Study Person ORCID\t0000-0002-8324-0047\t\t\t\n"
            "Study Person Roles\tsubmitter\t\t\t\n"
            "\t\t\t\t\n"
            "# Study License and Data DOI\t\t\t\t\n"
            "Study License\tCC BY 4.0\t\t\t\n"
            "Study License URL\thttps://creativecommons.org/licenses/by/4.0/\t\t\t\n"
            "Study Copyright\tAmelie Cabirol, Albrecht Haase\t\t\n"
            "Study Data Publisher\tUniversity of Dundee\t\t\t\n"
            "Study Data DOI\thttps://doi.org/10.17867/10000132\t\t\t\t\n"
            "\t\t\t\t\n"
            "Term Source Name\tNCBITaxon\tEFO\tCMPO\tFBbi\n"
            "Term Source URI\thttp://purl.obolibrary.org/obo/\thttp://www.ebi.ac.uk/efo/\thttp://www.ebi.ac.uk/cmpo/\thttp://purl.obolibrary.org/obo/\n"
            "\t\t\t\t\n"
            "# EXPERIMENT SECTION\t\t\t\t\n"
            "# Experiment Section containing all information relative to each experiment in the study including materials used, protocols names and description, phenotype names and description. For multiple experiments this section should be repeated.  Copy and paste the whole section below and fill out for the next experiment.\t\t\t\t\n"
            "\t\t\t\t\n"
            "Experiment Number\t1\t\t\t\n"
            "Comment[IDR Experiment Name]\tidr0075-cabirol-honeybee/experimentA\t\n"
            "Experiment Sample Type\ttissue\t\t\n"
            "Experiment Description\tTo study the spatial distribution of synaptic complexes called microglomeruli in the mushroom body neuropils of the honeybee brain, those structures where imaged by two-photon microscopy. A data analysis method was developed to automatically obtain the loci of those structures from large volume samples allowing to analyse their 3D density distribution.\t\t\n"
            "Experiment Size\t5D Images: 20\tAverage Image Dimension (XYZCT): 512 x 512 x 100 x 1 Total Tb: 0.001\t# fill in any values you know\t\n"
            "Experiment Example Images\t\t\t\t\n"
            "Experiment Imaging Method\ttwo-photon laser scanning microscopy"
        ),
        "metadata": {'source': '/Users/hnfd/Desktop/zhanghan/UvA/Thesis/AUMC/All-txt/idr0075-study.txt'}
    },
    {
        "page_content": (
            "Experiment Imaging Method Term Source REF\tFbbi\t\t\t\n"
            "Experiment Imaging Method Term Accession\tFBbi_00000254\t\t\t\n"
            "Experiment Comments\t\t\t\t\n"
            "\t\t\t\t\n"
            "# assay files\t\t\t\t\n"
            "Experiment Assay File\tidr0075-experimentB-assays\t\t\t\n"
            "Experiment Assay File Format\ttab-delimited text\t\t\t\n"
            "Assay Experimental Conditions\t\t\t\n"
            "Assay Experimental Conditions Term Source REF\t\t\t\n"
            "Assay Experimental Conditions Term Accession\t\t\t\t\n"
            "Quality Control Description\t\t\n"
            "\t\t\t\t\n"
            "# Protocols\t\t\t\t\n"
            "Protocol Name\tgrowth protocol\ttreatment protocol\timage acquisition and feature extraction protocol\tdata analysis protocol\n"
            "Protocol Type\tgrowth protocol\ttreatment protocol\timage acquisition and feature extraction protocol\tdata analysis protocol\n"
            "Protocol Type Term Source REF\tEFO\tEFO\t\t\n"
            "Protocol Type Term Accession\tEFO_0003789\tEFO_0003969\t\t\n"
            "Protocol Description\tHoneybees where reared to the age of 7 days in complete darkness, then sacrificed. Details in http://dx.doi.org/10.1101/589770 Materials and methods: Animals. Brains were extracted and immunostained with Alexa-488 using SYNORF1 antibodies and cleared methyl salicylate. Details in http://dx.doi.org/10.1101/589770 Materials and methods: Immunostaining of synapsin in whole-mount brains. Brains where imaged with a two-photon microscope (Bruker Ultima IV), voxel size MB calyx overview: (1.031x1.031x5)micron,  voxel size MB calyx overview: (0.3438x0.3438x0.5) micron, Details in http://dx.doi.org/10.1101/589770 Materials and methods: Image acquisition. 3D Loci of the synaptic complexes called microglomeruli were obtained by a multi-threshold segmentation protocol developed for this purpose. Details in http://dx.doi.org/10.1101/589770 Materials and methods: Volume reconstruction of the MB lip, Image processing for the quantification of microglomeruli, Quantification of microglomeruli in ROIs, Correction for the elliptic image of the microglomeruli."
        ),
        "metadata": {'source': '/Users/hnfd/Desktop/zhanghan/UvA/Thesis/AUMC/All-txt/idr0075-study.txt'}
    },
    # ... Add other documents here following the same pattern ...
]


new = format_retrieved_documents(documents)
print(new)    """