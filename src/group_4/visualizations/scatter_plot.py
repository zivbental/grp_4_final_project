import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

class ScatterPlotToolkit:
    """_summary_
    """
    def __init__(self, title='Scatter Plot', xlabel='log2(Fold Change)', ylabel='-log10(p-value)'):
        """_summary_

        Args:
            title (str, optional): _description_. Defaults to 'Volcano Plot'.
            xlabel (str, optional): _description_. Defaults to 'log2(Fold Change)'.
            ylabel (str, optional): _description_. Defaults to '-log10(p-value)'.
        """
        self.fig, self.axs = plt.subplots()  # Create figure and axes
        self.title = title
        self.xlabel = xlabel
        self.ylabel = ylabel
        self.axs.set_title(self.title)
        self.axs.set_xlabel(self.xlabel)
        self.axs.set_ylabel(self.ylabel)
    
    def plot(self, data: pd.DataFrame, x_col, y_col, color: str = 'black'):
        """_summary_

        Args:
            data (pd.DataFrame): _description_
            x_col (_type_): _description_
            y_col (_type_): _description_
            hue (str, optional): _description_. Defaults to None.
            palette (str, optional): _description_. Defaults to 'viridis'.
        """

        sns.scatterplot(data = data, x = x_col, y = y_col, color = color, ax = self.axs)
    def __str__(self):
        """_summary_

        Returns:
            _type_: _description_
        """
        return (f"Scatter plot(title={self.title}, xlabel={self.xlabel}, "
                f"ylabel={self.ylabel})")
    
    def set_significance_lines(self, threshold_p: float = 0.05, threshold_FC: tuple = (-2,2), 
                               Color: str = 'black', Linestyle: str = '--'):
        """_summary_

        Args:
            threshold_p (float, optional): _description_. Defaults to 0.05.
            threshold_FC (tuple, optional): _description_. Defaults to (-2,2).
            Color (str, optional): _description_. Defaults to 'black'.
            Linestyle (str, optional): _description_. Defaults to '--'.
        """
        self.axs.axhline(-np.log10(threshold_p), zorder = 0, color = Color, linestyle = Linestyle)
        self.axs.axvline(threshold_FC[0], zorder = 0, color = 'black', linestyle = "--")
        self.axs.axvline(threshold_FC[1], zorder = 0, color = 'black', linestyle = "--")

    def color_by(self, data: pd.DataFrame, x_col, y_col, color_by: str = 'None'):
        sns.scatterplot(data = data, x = x_col, y = y_col, hue = color_by, ax = self.axs)

    def label_genes(self, genes_df, x_col, y_col, label_col, **kwargs):
        """
        Labels specific genes on the plot.

        Parameters:
        - genes_df: DataFrame containing the gene data with columns for x, y, and labels.
        - x_col: Column name for the x-axis data.
        - y_col: Column name for the y-axis data.
        - label_col: Column name for the gene labels.
        - **kwargs: Additional keyword arguments passed to plt.text.
        """
        for i in range(genes_df.shape[0]):
            self.axs.text(
                genes_df[x_col].iloc[i], 
                genes_df[y_col].iloc[i], 
                genes_df[label_col].iloc[i],
                **kwargs)  # Allows for customization of text appearance, such as fontsize, color, etc.
    
    def set_size(self, figsize: tuple = (10, 6)):
        """
        Sets the size of the plot.

        Args:
            figsize (tuple, optional): The size of the figure (width, height). Defaults to (10, 6).
        """
        self.fig.set_size_inches(figsize)

    def set_axes(self, xlim: tuple = None, ylim: tuple = None):
        """
        Sets the limits for the x and y axes.

        Args:
            xlim (tuple, optional): The limits for the x-axis (min, max). Defaults to None.
            ylim (tuple, optional): The limits for the y-axis (min, max). Defaults to None.
        """
        if xlim:
            self.axs.set_xlim(xlim)
        if ylim:
            self.axs.set_ylim(ylim)
            