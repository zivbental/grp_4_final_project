"""Main module."""
from group_4.data_cleaning import DataCleaning, create_test_df, filter_protein_coding_genes
from group_4.data_processing import enrich_gene, scrape_for_pathway, process_data_for_volcanoplot
from group_4.visualizations import RNABarPlotter, ScatterPlotToolkit

import pathlib as path
import pytest

#test for file validity - that it can accept the file
# check that it removes the nan completly
#check that it removes the column completly
# check that it leaves only values smaller than threshold
# check that it does it combined

def test_valid_input():
    """check if the path input is valid"""
    fname = path.Path('original_test_data.xlsx')
    q = DataCleaning(fname)
    assert fname == q.filename

def test_str_input():
    q = DataCleaning('results_deseq2.xlsx')
    assert path.Path('results_deseq2.xlsx') == q.filename
def test_srt_input():
    """check if the string input is valid"""
    q = DataCleaning('original_test_data.xlsx')
    assert path.Path('original_test_data.xlsx') == q.filename

def test_missing_file():
    """check of file input exists"""
    fname = path.Path('teststs.fdfd')
    with pytest.raises(ValueError):
        DataCleaning(fname)

def test_wrong_input_type():
    """check for invalid file input"""
    fname = 2
    with pytest.raises(TypeError):
        q = DataCleaning(path.Path(fname))

def test_data_attr_exists():
    """check if the data attribute exists in the class"""
    fname = 'original_test_data.xlsx'
    q = DataCleaning(fname)
    q.load_data()
    assert hasattr(q, 'data')

def test_data_attr_is_df():
    """check if the output is a dataframe"""
    fname = 'original_test_data.xlsx'
    q = DataCleaning(fname)
    q.load_data()
    assert isinstance(q.data, pd.DataFrame)

def test_for_na_values():
    """check all nan values were removed"""
    q = DataCleaning('original_test_data.xlsx')
    q.remove_na()
    assert not q.data.isnull().any().any()

def test_column_in_dataframe(column_name_to_remove = 'Unnamed: 0'):
    """check if unwanted column is in dataframe"""
    q = DataCleaning('original_test_data.xlsx')
    assert column_name_to_remove in q.data.columns 

def test_for_unwanted_column(column_name_to_remove = 'Unnamed: 0'):
    """check unwated column was removed"""
    q = DataCleaning('original_test_data.xlsx')
    q.remove_columns(column_name_to_remove)
    assert column_name_to_remove not in q.data.columns

def test_for_filterd_values(column_name_to_filter = 'padj',threshold = 0.1):
    """check for proper filtering"""
    q = DataCleaning('original_test_data.xlsx')
    q.filter_columns(column_name_to_filter,threshold)
    assert (q.data[column_name_to_filter]<threshold).all()

def test_for_cleaned_data(column_name_to_filter = 'padj',threshold = 0.1,column_name_to_remove =  'Unnamed: 0'):
    """check clean data gives right output"""
    q = DataCleaning('original_test_data.xlsx')
    q.clean_data(column_name_to_filter,threshold,column_name_to_remove)
    assert (q.data[column_name_to_filter]<threshold).all()
    assert column_name_to_remove not in q.data.columns
    assert not q.data.isnull().any().any()

################ test for data scraping ################

def test_scrape_for_pathway():
    expected_result = [
        'Signal Transduction (Homo sapiens)',
        'Metabolism (Homo sapiens)',
        'Gene expression (Transcription) (Homo sapiens)',
        'Disease (Homo sapiens)',
        'Developmental Biology (Homo sapiens)'
    ]
    
    result = scrape_for_pathway('Cdk8')
    
    assert result == expected_result


################ test for data processing ################

# create data for data processing
data = DataCleaning('results_deseq2.xlsx')
results = data.clean_data(column_name_to_filter='padj', 
    threshold=0.1, 
    condition='smaller',
    column_name_to_remove='Unnamed: 0')
test_data = DataCleaning('results_deseq2.xlsx')
result = test_data.clean_data(column_name_to_filter='padj',threshold=0.1, condition = 'smaller', column_name_to_remove='Unnamed: 0')

def test_validate_p_vals():
    # Test with non-float column (str_column)
    with pytest.raises(ValueError, match="The p-values column must contain float values."):
        validate_p_vals(result['row'])

    # Test with fold_change column that contains values outside the [0, 1] range
    with pytest.raises(ValueError, match=re.escape("The p-values column contains values outside the range [0, 1].")):
        validate_p_vals(result['log2FoldChange'])

    # Test with a valid p-value column
    assert validate_p_vals(result['padj']) == True

def test_minus_log10_col_valid():
    # Test with a valid p-value column
    result_df = minus_log10_col(result, 'padj')
    expected_df = result.copy()
    expected_df['-log10(p-value)'] = -np.log10(result['padj'])
    pd.testing.assert_frame_equal(result_df, expected_df)

def test_minus_log10_col_invalid_column():
    # Test with a non-existent p-value column
    with pytest.raises(KeyError, match="The column 'p_value' does not exist in the DataFrame."):
        minus_log10_col(result, 'p_value')

def test_minus_log10_col_invalid_pvals():
    # Test with invalid p-values (non-float values)
    with pytest.raises(ValueError, match="The p-values column must contain float values."):
        minus_log10_col(result, 'row')

df_to_label = pd.DataFrame({
    'value': [0.5, 1.5, 2.5, 3.5]  # Example data
})

def test_label_by_order_valid():
    # Test with valid thresholds and labels
    thresholds = [1, 2]
    labels = ['Low', 'Medium', 'High']
    result_df = label_by_order(df_to_label, 'value', 'label', thresholds, labels)
    
    # Define expected output DataFrame with categorical dtype
    expected_df = df_to_label.copy()
    expected_df['label'] = pd.Categorical(['Low', 'Medium', 'High', 'High'], categories=labels, ordered=True)
    pd.testing.assert_frame_equal(result_df, expected_df)


def test_label_by_order_invalid_thresholds_non_numeric():
    # Test with non-numeric thresholds
    thresholds = ['a', 'b']
    labels = ['Low', 'High', 'Very High']
    with pytest.raises(ValueError, match="All thresholds must be numeric values."):
        label_by_order(df_to_label, 'value', 'label', thresholds, labels)

def test_label_by_order_invalid_labels_count():
    # Test with incorrect number of labels
    thresholds = [1, 2, 3]
    labels = ['Low', 'High']  # Only 3 labels, but 4 are needed
    with pytest.raises(ValueError, match="The number of labels must be exactly one more than the number of thresholds."):
        label_by_order(df_to_label, 'value', 'label', thresholds, labels)

def test_label_by_order_invalid_thresholds_order():
    # Test with unsorted thresholds
    thresholds = [2, 1]  # Unsorted
    labels = ['Low', 'High', 'Very High']
    with pytest.raises(ValueError, match="Thresholds must be sorted in ascending order."):
        label_by_order(df_to_label, 'value', 'label', thresholds, labels)

# set of tests for the function identify_top_n_values #
def test_invalid_n_top():
    """Test that the function raises a ValueError for invalid n_top."""
  
    with pytest.raises(ValueError, match="n_top must be a positive integer"):
        identify_top_n_values(data, 'padj', -3) 

def test_non_numeric_reference_column():
    """Test that the function raises a ValueError for a non-numeric reference column."""
    with pytest.raises(ValueError, match="The reference column must contain numeric data"):
        identify_top_n_values(results, 'row', 3)

def test_n_values_greater_than_rows():
    """Test that the function raises ValuEerror for n_top greater than amount of rows in the dataframe """
    with pytest.raises(ValueError, match="n_top cannot be greater than the number of rows in the DataFrame"):
        identify_top_n_values(results, 'padj', results.shape[0]+1)

def test_identify_top_n_values_top():
    """Test that the function correctly identifies the top N values."""
    top_values_df, top_n_threshold = identify_top_n_values(results, 'padj', 3)
    df  = results.sort_values('padj', ascending=False).reset_index(drop=True)
    expected_df = df.iloc[:4]
    expected_threshold = 0.044372552904792
    pd.testing.assert_frame_equal(top_values_df.reset_index(drop=True), expected_df)
    assert top_n_threshold == expected_threshold, "The threshold for top N values is incorrect."

def test_identify_bottom_n_values_top():
    """Test that the function correctly identifies the top N values."""
    top_values_df, top_n_threshold = identify_top_n_values(results, 'padj', 3,False)
    df  = results.sort_values('padj', ascending=True).reset_index(drop=True)
    expected_df = df.iloc[:3]
    expected_threshold = 1.32085855677125e-51
    pd.testing.assert_frame_equal(top_values_df.reset_index(drop=True), expected_df)
    assert top_n_threshold == expected_threshold, "The threshold for top N values is incorrect."

    
def test_get_mouse_gene_sets():
    mouse_gene_sets = get_mouse_gene_sets()

    # Check if the function returns a non-empty list
    if isinstance(mouse_gene_sets, list) and len(mouse_gene_sets) > 0:
        print(f"Test passed: {len(mouse_gene_sets)} mouse-related gene sets found.")
    else:
        print("Test failed: No mouse-related gene sets found.")

test_get_mouse_gene_sets()







