import pandas as pd
import gseapy as gp
import os
from concurrent.futures import ThreadPoolExecutor 
from requests.exceptions import RequestException 
from json import JSONDecodeError 


def get_mouse_gene_sets() -> list:
    '''
    Retrieve all gene sets related to mice from the available gene sets in GSEApy.

    output: 
        list of gene sets related to mice
    '''
    available_gene_sets = gp.get_library_name()  # Checking for all the available databases
    mouse_gene_sets = [gene_set for gene_set in available_gene_sets if 'Mouse' in gene_set]  # Include only databases for mice
    return mouse_gene_sets

def enrich_gene(gene) -> list:
    '''

    Find the pathway of the gene is part of using GSEApy library

    input: 

        gene_name (string)

    output: list of pathways

    '''
    try:
        mouse_gene_sets = get_mouse_gene_sets()
        enr = gp.enrichr(gene_list=[gene], gene_sets=mouse_gene_sets, organism='Mouse', outdir=None) #using GSEApy to find all the enrichment for given gene name in all the databases related to mice
        
        if not enr.results.empty: #if there is pathway/s for the gene, make it a list
            pathways = enr.results['Term'].tolist()
            return pathways
        else:
            return 'No related pathways found' #dealing no results
    #dealing with API and JSOND errors 
    except (RequestException, JSONDecodeError) as e:
        return f"Error processing gene {gene}: {e}"
           





