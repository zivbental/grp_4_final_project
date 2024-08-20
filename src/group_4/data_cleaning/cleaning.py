import pandas as pd
import pathlib as path
from typing import Union

class DataCleaning:
    """ 
    A class to perform various data cleaning operations on a pandas DataFrame.
    This class provides methods to load data from a file, remove rows with NaN values,
    filter rows based on conditions, remove specified columns, and apply all these 
    cleaning steps in a sequence. The class is designed to handle files in both 
    .csv and .xlsx formats.
    
    Attributes:
    ----------
    filename : pathlib.Path or str
        The path to the file that contains the data.
    data : pd.DataFrame
        The DataFrame containing the loaded data.

     Methods:
    --------
    remove_na(self, columns=None) -> 'DataCleaning':
        Removes rows with NaN values in the specified columns. If no columns are specified,
        it removes rows with NaN values across the entire DataFrame.
        
    filter_columns(self, column_name_to_filter: str, threshold: float, condition: str) -> 'DataCleaning':
        Filters the DataFrame rows based on whether the values in a specified column are 
        smaller or larger than a given threshold. The condition can be 'smaller' or 'larger'.
        
    remove_columns(self, column_name_to_remove: str) -> 'DataCleaning':
        Removes the specified column from the DataFrame.
        
    clean_data(self, column_name_to_filter: str, threshold: float, condition: str, column_name_to_remove: str) -> pd.DataFrame:
        Applies all the cleaning methods (removing columns, removing NaN values, filtering 
        based on a threshold) and returns the cleaned DataFrame with a reset index.
    """    
    def __init__(self,filename : Union[path.Path,str]):
        """Check if the filename is path"""
        if isinstance(filename,path.Path):
            self.filename = filename
            """Check if the file name is string"""
        elif isinstance(filename,str):
            self.filename = path.Path(filename)
            """If not raise type error"""
        else:
          raise TypeError('file name must be either a string or a pathlib path')
        
        self.data = self.load_data()    
    
    def load_data(self) -> pd.DataFrame:
         """
         Load data from file to pandas data frame
         This method checks if the file is either xslx or csv file.
         Returns:
        -------
        pd.DataFrame
            The loaded DataFrame.
            
        Raises:
        -------
        ValueError: If the file format is not supported (i.e., not .csv or .xlsx).
        """
         if self.filename.suffix=='.xlsx':
            df = pd.read_excel(self.filename)
         elif self.filename.suffix=='.csv':
            df = pd.read_csv(self.filename)
         else:
            raise ValueError('file format not supported, xlsx or csv only')
         return df
    
    def remove_na(self, columns=None)-> 'DataCleaning':
        """
        Removes NaN value rows from data frame in the columns mentiond
        
        Parameters:
        ----------
        columns : list, optional
            A list of column names to check for NaN values. If None, all columns are checked.

        Returns:
        -------
        self : DataCleaning
            Returns the DataCleaning object with the DataFrame updated to remove rows with NaN values.
        """ 
        if columns is None:
            columns = self.data.columns
        self.data = self.data.dropna(subset = columns)
        return self
       
    def filter_columns(self,column_name_to_filter:str,threshold:float,condition:str)-> 'DataCleaning':
        """
        Filters rows based on provided columns' values smaller / larger than the threshold
        Parameters:
        ----------
        column_name_to_filter : str
            The name of the column to use for filtering.
        threshold : float
            The threshold value to use for filtering.
        condition : str
            A string that determines whether to filter for values 'smaller' or 'larger' than the threshold.
            The string is case-insensitive.

        Returns:
        -------
        self : DataCleaning
            Returns the DataCleaning object with the DataFrame filtered based on the given condition.

        Raises:
        -------
        ValueError: If the column does not exist in the DataFrame.
        ValueError: If the condition is neither 'smaller' nor 'larger'.
        """
        condition = condition.lower()
        """First to check if column name exists"""
        if column_name_to_filter not in self.data.columns:
            raise ValueError('column name provided does not exist')
        """Filter based on condition input"""
        if condition == 'smaller':
         self.data = self.data[self.data[column_name_to_filter] < threshold]
        elif condition == 'larger':
            self.data = self.data[self.data[column_name_to_filter] > threshold]
        else:
            raise ValueError('invalid condition, either larger of smaller')
        return self
    
    def remove_columns(self,column_name_to_remove:str)-> 'DataCleaning':
        """
        Removes columns from dataframe
        Parameters:
        ----------
        column_name_to_remove : str
            The name of the column to be removed.
        Returns:
        -------
        self : DataCleaning
        Raises:
        -------
        ValueError: If the column does not exist in the DataFrame.
        """
        if column_name_to_remove not in self.data.columns:
            raise ValueError('column name provided does not exist')
        else:
            self.data = self.data.drop(columns=column_name_to_remove)
        return self

    def clean_data(self, column_name_to_filter:str, threshold:float,condition:str, column_name_to_remove:str) -> pd.DataFrame:
        """Applies all the cleaning methods to the dataframe:
        1.Remove unwanted columns.
        2.Removes rows with NaN values.
        3.Filters rows according to a columns' values compared to a threshold.
        4.Resets the dataframe index 
       
        Parameters:
        ----------
        column_name_to_filter : str
            The name of the column to use for filtering.
        threshold : float
            The threshold value for filtering.
        condition : str
            A string that determines whether to filter for values 'smaller' or 'larger' than the threshold.
        column_name_to_remove : str
            The name of the column to be removed.

        Returns:
        -------
        pd.DataFrame
            The cleaned DataFrame with the specified column removed, NaN values dropped, filtered by the threshold, and with the index reset.
        """
        self.remove_columns(column_name_to_remove)
        self.remove_na()
        self.filter_columns(column_name_to_filter, threshold,condition)
        self.data = self.data.reset_index(drop=True)
        return self.data
                
