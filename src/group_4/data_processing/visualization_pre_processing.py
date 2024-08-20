import pandas as pd
import numpy as np
from typing import Union

def validate_p_vals(p_val_col: Union[pd.Series, np.ndarray]) -> bool:
    """Validates that a given column supposedly containing p-values (0 < p-values < 1) 
    actually contains valid p-values.

    Args:
        p_val_col (Union[pd.Series, np.ndarray]): A column or array containing p-values to be validated.

    Raises:
        ValueError: If any value is not a float.
        ValueError: If any value is not between 0 and 1.

    Returns:
        bool: Returns True if the p-values are valid.
    """

    # Validation 1: Check if the given column contains float type (ignoring NA values)
    if not pd.api.types.is_float_dtype(p_val_col.dropna()):
        raise ValueError("The p-values column must contain float values.")

    # Validation 2: Check if the given column contains values between 0 and 1 (ignoring NA values)
    if not p_val_col.between(0.0, 1.0).all():
        raise ValueError("The p-values column contains values outside the range [0, 1].")
    return True

    
def minus_log10_col(df: pd.DataFrame, p_val_col: str,
                    output_col_name :str = '-log10(p-value)') -> pd.DataFrame:
    """Calulates the -log10 col for volcano plot creation

    Args:
        df (pd.DataFrame): df
        p_val_col (str): the column name were the p_values are stored.
    
    Raises: 
        KeyError: there is no p value column in the df
    """
    if p_val_col not in df.columns:
        raise KeyError(f"The column '{p_val_col}' does not exist in the DataFrame.")
    if validate_p_vals(df[p_val_col]):
        df[output_col_name] = -np.log10(df[p_val_col])
        return df
    
def label_by_order(df: pd.DataFrame, ref_col: str, labels_col: str, thresholds: list, 
                   labels: list) -> pd.DataFrame:
    """
    Adds a new column to the DataFrame that labels the samples based on their value 
    in an already existing column. The labels apply in ascending order, so the thresholds
    (and labels) should be sorted accordingly.

    Args:
    - df (pd.DataFrame): DataFrame containing the reference column.
    - ref_col (str): The name of the column containing values to be labeled.
    - labels_col (str): The name of the new label column.
    - thresholds (list): List of thresholds, must be numbers.
    - labels (list): List of labels corresponding to each range between thresholds.

    Returns:
    - DataFrame with an added column of labels.

    Raises:
    - ValueError: If thresholds contain non-numeric values.
    - ValueError: If the number of labels is not one more than the number of thresholds.
    - ValueError: If thresholds are not sorted in ascending order.
    """

    # Validation 1: Check if all thresholds are numeric
    if not all(isinstance(th, (int, float)) for th in thresholds):
        raise ValueError("All thresholds must be numeric values.")

    # Validation 2: Check if the number of labels is one more than the number of thresholds
    if len(labels) != len(thresholds) + 1:
        raise ValueError("The number of labels must be exactly one more than the number of thresholds.")

    # Validation 3: Check if thresholds are sorted in ascending order
    if thresholds != sorted(thresholds):
        raise ValueError("Thresholds must be sorted in ascending order.")

    # Apply labels based on thresholds
    df[labels_col] = pd.cut(df[ref_col], bins=[-float('inf')] + thresholds + [float('inf')],
        labels=labels, right=True)
    df[labels_col] = pd.Categorical(df[labels_col], categories=labels, ordered=True)

    return df

def identify_top_n_values(df: pd.DataFrame, name_of_ref_col: str, n_top: int, 
                          highest: bool = True) -> pd.DataFrame:
    """
    Identifies the top N values (maximum or minimum) in a specific column in a DataFrame.

    Args:
        df (pd.DataFrame): The DataFrame in question.
        name_of_ref_col (str): The reference column title.
        n_top (int): The number of highest or lowest values to identify.
        top (bool): If True, identifies the top N highest values; if False, 
        identifies the top N lowest values.

    Returns:
        top_values_df (pd.DataFrame): A DataFrame containing only the data 
        for the top N values.
        minimal_top_n_value (int, float): The threshold value at the Nth position.
    
    Raises:
        ValueError: If n_top is not a positive integer.
        ValueError: If the reference column does not contain numeric data.
        ValueError: If n_top is greater than the number of available rows.
    """

    # Validation 1: Check if n_top is a positive integer
    if not isinstance(n_top, int) or n_top <= 0:
        raise ValueError("n_top must be a positive integer.")

    # Validation 2: Check if the reference column contains numeric data
    if not pd.api.types.is_numeric_dtype(df[name_of_ref_col]):
        raise ValueError("The reference column must contain numeric data.")

    # Validation 3: Check if n_top is greater than the number of available rows
    if n_top > len(df):
        raise ValueError("n_top cannot be greater than the number of rows in the DataFrame.")

    # Sort the DataFrame based on the reference column
    df = df.sort_values(name_of_ref_col, ascending=not highest).reset_index(drop=True)

    # Identify the Nth threshold value
    top_n_threshold = df.loc[n_top-1, name_of_ref_col]

    # Get the top N values based on the threshold
    if highest:
        top_values_df = df[df[name_of_ref_col] >= top_n_threshold]
    else:
        top_values_df = df[df[name_of_ref_col] <= top_n_threshold]

    return top_values_df, top_n_threshold

def process_data_for_volcanoplot(input_data: pd.DataFrame,p_ref_colname: str,log10colname: str, 
                                 ref_colname: str, label_colname: str, thresholds: list, labels: list, 
                                 n: int, highest: bool):
    """
    Processes data frames in order to visualize it as a volcano plot, a scatter plot of the fold change (FC) of
    gene vs. the -log10 of the p value of the FC. There are three stages of processing:
    1. Calculating a new column for the dataframe with the -log10 of the p-values
    2. Ranking the genes by p value or by FC, so different levels of p value or FC can
    be distinguished in the plot.
    3. Identifying the top genes (top significant or most changed) so they can also be distinguished in the plot.
    To specify whether you want the top highest genes (most changed) or top lowest genes (most significant), specify
    whether higher is true or false (lower).

    Args:
        input_data (pd.DataFrame): data frame of genes, so for each gene there is a FC and p value listed.
        p_ref_colname (str): the column which contains the p_values
        log10colname (str): the new name for the colum that calculates the -log10(p-value)
        ref_colname (str): the colname which the labels will be determined according to it
        label_colname (str): the new name for the label column
        thresholds (list): p-values or FC values which we want to divide the data by, and label accordingly.
        labels (list): the labels that will be given to the ranges of p-values/FC.
        n (int): number of top genes to be isolated
        highest (bool): determine whether we want the highest gene or the lowest gene values.

    Returns:
        processed dataframe with -log10(p-value) column and label column, a dataframe containing only the top genes, and the threshold
        that differentiates between the top selected genes and the rest of the genes.
    """
    with_log_col = minus_log10_col(input_data,p_ref_colname,log10colname)
    processed_df = label_by_order(with_log_col, ref_colname, label_colname, thresholds, labels)
    top_genes, threshold = identify_top_n_values(processed_df,ref_colname,n,highest)
    return processed_df, top_genes

