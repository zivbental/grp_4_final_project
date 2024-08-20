"""Main module."""
from data_cleaning import DataCleaning, create_test_df
from data_processing import enrich_gene, scrape_for_pathway, process_data_for_volcanoplot
#from data_cleaning.try_vis import process_data_for_volcanoplot
from visualizations import RNABarPlotter, ScatterPlotToolkit

from concurrent.futures import ThreadPoolExecutor 
import matplotlib.pyplot as plt

import os



def main():
    create_test_df()
    base_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(base_dir, 'results_deseq2.xlsx')

    cleaner = DataCleaning(file_path)
    cleaned_data = cleaner.clean_data(column_name_to_filter='padj',threshold=0.1,condition = 'smaller', column_name_to_remove='Unnamed: 0')
    b_plot = RNABarPlotter(cleaned_data)
    b_plot.plot(0.05)

    '''complex_related_pathway = []
    with ThreadPoolExecutor(max_workers=8) as executor:  #up to 8 threads will run concurrently
        complex_related_pathway = list(executor.map(enrich_gene, cleaned_data['row'])) 
    cleaned_data['complex related pathway'] = complex_related_pathway
    simple_related_pathway = []
    for gene_name in cleaned_data['row']:
      pathway_name = scrape_for_pathway(gene_name)
      simple_related_pathway.append(pathway_name)
    cleaned_data['related pathway'] = simple_related_pathway'''
    processed_data_for_plotting = cleaner.remove_na().data
    final_processed_df, top_genes = process_data_for_volcanoplot(processed_data_for_plotting,'padj','-log10(p-value)','padj','significance',[0.01, 0.05, 0.1],['very significant', 'significant','trend','non-sognificant'],10,False)
    cleaned_data.to_csv('output_data.csv')
    q = ScatterPlotToolkit()
    q.plot(final_processed_df,'log2FoldChange','-log10(p-value)')
    q.set_significance_lines(threshold_p=0.05,threshold_FC=(-2,2))
    q.color_by(final_processed_df,'log2FoldChange','-log10(p-value)',color_by='significance')
    q.label_genes(top_genes,'log2FoldChange','-log10(p-value)','row')
    plt.savefig("volcano_plot.png", format='png', dpi=300)
    plt.show()
    



if __name__ == "__main__":
    main()
