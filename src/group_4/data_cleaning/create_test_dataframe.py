import pandas as pd
import numpy as np
import pathlib as path

def create_test_df():
    # Specify file paths for saving the data
    original_file_path = path.Path('original_test_data.xlsx')

    # Create a larger test DataFrame with NaN values and padj values
    test_data = pd.DataFrame({
        'Unnamed: 0': range(100),
        'row': [f'Gene{i}' for i in range(100)],
        'log2FoldChange': np.random.randn(100),
        'padj': np.random.rand(100),  # Random values between 0 and 1
        
    })

    # Introduce some NaN values in 'log2FoldChange' and 'padj'
    nan_indices = np.random.choice(test_data.index, size=10, replace=False)
    test_data.loc[nan_indices, 'log2FoldChange'] = np.nan
    test_data.loc[nan_indices, 'padj'] = np.nan

    # Save the original test DataFrame to the specified CSV file
    test_data.to_excel(original_file_path, index=False)
