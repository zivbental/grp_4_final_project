import pandas as pd
import pathlib
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.cm as cm


class RNABarPlotter:

    """
    A class to generate bar plots for RNA expression data from a DESeq2 analysis.
    This class takes a pandas DataFrame containing RNA expression data, extracts relevant 
    information (RNA names and log2 fold change), and generates a horizontal bar plot to 
    visualize the changes in RNA expression levels.

    Attributes:
    ----------
    df : pd.DataFrame
        The DataFrame containing RNA expression data.
    Methods:
    -------
        get_data(self) -> Tuple[pd.Series, pd.Series]:
        Extracts RNA names and log2 fold change values from the DataFrame.
        generate_bar_plot(self, RNA_names: pd.Series, expression_changes: pd.Series):
        Creates a horizontal bar plot to visualize RNA expression changes.
    """      
    
    def __init__(self, df):
        """Initialize the RNAExpressionPlotter with the path to the data file.
        
        Args:
            A pd.DataFrame, containing RNA deseq2 data
        """
        self.df = df
        
    def get_data(self) -> pd.Series:
        """Extracts RNA names and log2 Fold Change from the DataFrame.

        Returns:
            Tuple[pd.Series, pd.Series]: RNA sequences and log2 Fold Change in expression
        """
        data = self.df
        # Choose RNA names and expression changes
        RNA_names = data['row']
        expression_changes = data['log2FoldChange']

        return RNA_names, expression_changes


    def generate_bar_plot(self, RNA_names, expression_changes):
        """Creates a horizontal bar plot for changes in expression levels.

        Args:
            RNA_names (pd.Series): RNA sequences names
            expression_changes (pd.Series): log2 Fold Change in expression
        """
        # Color map
        cmap = plt.colormaps['RdYlBu']

        # Color bar limits
        norm = plt.Normalize(pd.Series(expression_changes).min(), pd.Series(expression_changes).max())

        # Create a horizontal bar plot with a color scale
        plt.figure(figsize=(12, 10))
        bars = plt.barh(RNA_names, expression_changes, color=cmap(norm(expression_changes)))

        # Add a color bar to show the scale
        sm = cm.ScalarMappable(cmap=cmap, norm=norm)
        sm.set_array([])

        # Positioning the color bar next to the plot
        cbar = plt.colorbar(sm, ax=plt.gca(), orientation='vertical')
        cbar.set_label('log2 Fold Change')

        # Add a vertical line at x=0 for reference
        plt.axvline(0, color='black', linewidth=1)

        # Adding labels and title
        plt.xlabel('Expression Change')
        plt.ylabel('RNA sequence')
        plt.yticks(fontsize=8)
        plt.title('log2 Fold Change - RNAs Expression')
        plt.grid()
        plt.savefig('barplot.png')

    def plot(self, padj_value):
        """Main method to load data, clean it, and plot it.

        Args:
            padj_value: Adjusted p-value threshold of RNAs to plot
        """
        RNA_names, expression_changes = self.get_data()
        self.generate_bar_plot(RNA_names, expression_changes)
