import pandas as pd
import requests
import os


def download_protein_coding_genes(output_file='protein_coding_genes.tsv'):
    '''
    Downloads a list of protein-coding genes from Ensembl BioMart.
    
    input:
        output_file (str): The file path to save the downloaded gene list.
    
    output :
        protein_coding_genes (set): A set of protein-coding gene names.
    '''

    mart_url = "http://www.ensembl.org/biomart/martservice?query="
    query = f"""<?xml version="1.0" encoding="UTF-8"?>
    <!DOCTYPE Query>
    <Query virtualSchemaName="default" formatter="TSV" header="0" uniqueRows="1" count="" datasetConfigVersion="0.6">
        <Dataset name="mmusculus_gene_ensembl" interface="default">
            <Filter name="biotype" value="protein_coding"/>
            <Attribute name="external_gene_name"/>
        </Dataset>
    </Query>"""

    response = requests.get(mart_url + query)
    if response.status_code == 200:
        with open(output_file, 'w') as f:
            f.write(response.text)
        protein_coding_genes_df = pd.read_csv(output_file, sep='\t', header=None)
        protein_coding_genes = set(protein_coding_genes_df.iloc[:, 0].tolist())
        return protein_coding_genes
    else:
        response.raise_for_status()

def filter_protein_coding_genes(df, protein_coding_genes):
    '''
    Filter the DataFrame to include only genes that are known to translate into proteins.
    
    input:
        df (DataFrame): The input DataFrame containing genes.
        protein_coding_genes (set): A set of protein-coding gene names.
    
    output:
        df_cleaned (DataFrame): Filtered DataFrame containing only protein-coding genes.
    '''
    # Filter DataFrame to include only genes found in the protein-coding gene set
    df_cleaned = df[df['row'].isin(protein_coding_genes)]    
    
    return df_cleaned

