"""
Medical Insurance Dataset - Data Visualization Module
===================================================

This module provides comprehensive visualization capabilities for medical insurance data analysis.
Author: Data Analysis System
Date: September 2025
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import warnings
warnings.filterwarnings('ignore')

class MedicalInsuranceVisualizer:
    """
    A class to create comprehensive visualizations for medical insurance data.
    """

    def __init__(self, df_clean, df_labeled=None):
        """
        Initialize the visualizer with clean data.

        Parameters:
        df_clean (pd.DataFrame): Cleaned numerical dataset
        df_labeled (pd.DataFrame): Dataset with human-readable labels
        """
        self.df_clean = df_clean
        self.df_labeled = df_labeled if df_labeled is not None else df_clean

        # Set up plotting style
        plt.style.use('default')
        sns.set_palette("husl")
        plt.rcParams['figure.figsize'] = (12, 8)
        plt.rcParams['font.size'] = 10

    def create_line_chart(self, x_col='age', y_col='charges', save_path=None):
        """
        Create a line chart showing trend over a continuous variable.

        Parameters:
        x_col (str): Column for x-axis
        y_col (str): Column for y-axis
        save_path (str): Path to save the plot

        Returns:
        matplotlib.figure.Figure: The created figure
        """
        print(f"📈 Creating line chart: {y_col} vs {x_col}")

        # Group by x_col and calculate mean y_col
        grouped_data = self.df_clean.groupby(x_col)[y_col].mean().reset_index()

        fig, ax = plt.subplots(figsize=(12, 6))
        ax.plot(grouped_data[x_col], grouped_data[y_col], marker='o', linewidth=2, markersize=4)

        # Add trend line
        z = np.polyfit(grouped_data[x_col], grouped_data[y_col], 1)
        p = np.poly1d(z)
        ax.plot(grouped_data[x_col], p(grouped_data[x_col]), "--", alpha=0.7, color='red',
                label=f'Trend Line (slope: ${z[0]:.0f} per unit)')

        ax.set_title(f'{y_col.title()} Trend by {x_col.title()}', fontsize=16, fontweight='bold')
        ax.set_xlabel(f'{x_col.title()}', fontsize=12)
        ax.set_ylabel(f'{y_col.title()} ($)', fontsize=12)
        ax.grid(True, alpha=0.3)
        ax.legend()

        # Format y-axis for currency
        ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'${x:,.0f}'))

        plt.tight_layout()

        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            print(f"✅ Line chart saved to: {save_path}")

        return fig

    def create_bar_chart(self, x_col='region_label', y_col='charges', save_path=None):
        """
        Create a bar chart for categorical comparisons.

        Parameters:
        x_col (str): Categorical column for x-axis
        y_col (str): Numerical column for y-axis
        save_path (str): Path to save the plot

        Returns:
        matplotlib.figure.Figure: The created figure
        """
        print(f"📊 Creating bar chart: {y_col} by {x_col}")

        # Calculate averages by category
        if x_col in self.df_labeled.columns:
            grouped_data = self.df_labeled.groupby(x_col)[y_col].mean().sort_values(ascending=False)
        else:
            grouped_data = self.df_clean.groupby(x_col)[y_col].mean().sort_values(ascending=False)

        fig, ax = plt.subplots(figsize=(10, 6))
        colors = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4', '#F7DC6F'][:len(grouped_data)]
        bars = ax.bar(grouped_data.index, grouped_data.values, color=colors, alpha=0.8)

        # Add value labels on bars
        for bar in bars:
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height + height*0.01,
                   f'${height:,.0f}', ha='center', va='bottom', fontweight='bold')

        ax.set_title(f'Average {y_col.title()} by {x_col.replace("_label", "").title()}', 
                    fontsize=16, fontweight='bold')
        ax.set_xlabel(f'{x_col.replace("_label", "").title()}', fontsize=12)
        ax.set_ylabel(f'Average {y_col.title()} ($)', fontsize=12)
        ax.tick_params(axis='x', rotation=45)
        ax.grid(True, alpha=0.3, axis='y')

        # Format y-axis for currency
        ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'${x:,.0f}'))

        plt.tight_layout()

        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            print(f"✅ Bar chart saved to: {save_path}")

        return fig

    def create_histogram(self, col='bmi', bins=30, save_path=None):
        """
        Create a histogram for distribution analysis.

        Parameters:
        col (str): Column to plot
        bins (int): Number of bins
        save_path (str): Path to save the plot

        Returns:
        matplotlib.figure.Figure: The created figure
        """
        print(f"📊 Creating histogram: {col} distribution")

        fig, ax = plt.subplots(figsize=(10, 6))

        n, bins_used, patches = ax.hist(self.df_clean[col], bins=bins, alpha=0.7, 
                                       color='skyblue', edgecolor='black', linewidth=0.5)

        # Add statistics lines
        mean_val = self.df_clean[col].mean()
        median_val = self.df_clean[col].median()

        ax.axvline(mean_val, color='red', linestyle='--', linewidth=2, 
                  label=f'Mean: {mean_val:.2f}')
        ax.axvline(median_val, color='orange', linestyle='--', linewidth=2, 
                  label=f'Median: {median_val:.2f}')

        ax.set_title(f'Distribution of {col.upper()}', fontsize=16, fontweight='bold')
        ax.set_xlabel(f'{col.upper()}', fontsize=12)
        ax.set_ylabel('Frequency', fontsize=12)
        ax.legend()
        ax.grid(True, alpha=0.3, axis='y')

        # Add statistics text box
        stats_text = f'Total: {len(self.df_clean):,}\nStd Dev: {self.df_clean[col].std():.2f}\nMin: {self.df_clean[col].min():.2f}\nMax: {self.df_clean[col].max():.2f}'
        ax.text(0.75, 0.95, stats_text, transform=ax.transAxes,
               bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.8),
               verticalalignment='top', fontsize=10)

        plt.tight_layout()

        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            print(f"✅ Histogram saved to: {save_path}")

        return fig

    def create_scatter_plot(self, x_col='bmi', y_col='charges', hue_col='smoker_label', save_path=None):
        """
        Create a scatter plot for relationship analysis.

        Parameters:
        x_col (str): Column for x-axis
        y_col (str): Column for y-axis
        hue_col (str): Column for color coding
        save_path (str): Path to save the plot

        Returns:
        matplotlib.figure.Figure: The created figure
        """
        print(f"📊 Creating scatter plot: {x_col} vs {y_col}")

        fig, ax = plt.subplots(figsize=(12, 8))

        # Plot points with color coding
        if hue_col and hue_col in self.df_labeled.columns:
            unique_categories = self.df_labeled[hue_col].unique()
            colors = ['blue', 'red', 'green', 'orange']

            for i, category in enumerate(unique_categories):
                subset = self.df_labeled[self.df_labeled[hue_col] == category]
                ax.scatter(subset[x_col], subset[y_col], 
                         alpha=0.6, s=30, c=colors[i % len(colors)], 
                         label=f'{category} (n={len(subset)})')
        else:
            ax.scatter(self.df_clean[x_col], self.df_clean[y_col], 
                      alpha=0.6, s=30, c='blue')

        # Add trend line
        z = np.polyfit(self.df_clean[x_col], self.df_clean[y_col], 1)
        p = np.poly1d(z)
        x_range = np.linspace(self.df_clean[x_col].min(), self.df_clean[x_col].max(), 100)
        ax.plot(x_range, p(x_range), "--", alpha=0.8, color='green',
               label=f'Trend (r={self.df_clean[x_col].corr(self.df_clean[y_col]):.3f})')

        ax.set_title(f'{x_col.upper()} vs {y_col.title()}', fontsize=16, fontweight='bold')
        ax.set_xlabel(f'{x_col.upper()}', fontsize=12)
        ax.set_ylabel(f'{y_col.title()} ($)', fontsize=12)
        ax.legend()
        ax.grid(True, alpha=0.3)

        # Format y-axis for currency if it's charges
        if 'charge' in y_col.lower():
            ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'${x:,.0f}'))

        # Add correlation text
        corr_coef = self.df_clean[x_col].corr(self.df_clean[y_col])
        ax.text(0.05, 0.95, f'Correlation: {corr_coef:.3f}', 
               transform=ax.transAxes,
               bbox=dict(boxstyle='round', facecolor='lightgray', alpha=0.8),
               fontsize=12, fontweight='bold')

        plt.tight_layout()

        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            print(f"✅ Scatter plot saved to: {save_path}")

        return fig

    def create_correlation_heatmap(self, save_path=None):
        """
        Create a correlation matrix heatmap.

        Parameters:
        save_path (str): Path to save the plot

        Returns:
        matplotlib.figure.Figure: The created figure
        """
        print("🔥 Creating correlation heatmap")

        fig, ax = plt.subplots(figsize=(10, 8))

        corr_matrix = self.df_clean.corr()
        mask = np.triu(np.ones_like(corr_matrix, dtype=bool))

        sns.heatmap(corr_matrix, annot=True, cmap='RdYlBu_r', center=0,
                   mask=mask, square=True, fmt='.3f',
                   cbar_kws={"shrink": .8}, ax=ax)

        ax.set_title('Correlation Matrix Heatmap\n(Medical Insurance Dataset)', 
                    fontsize=16, fontweight='bold')

        plt.tight_layout()

        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            print(f"✅ Correlation heatmap saved to: {save_path}")

        return fig

    def create_box_plots(self, save_path=None):
        """
        Create box plots for categorical comparisons.

        Parameters:
        save_path (str): Path to save the plot

        Returns:
        matplotlib.figure.Figure: The created figure
        """
        print("📦 Creating box plots")

        fig, axes = plt.subplots(2, 2, figsize=(15, 10))

        # Box plot 1: Charges by Smoker
        if 'smoker_label' in self.df_labeled.columns:
            sns.boxplot(data=self.df_labeled, x='smoker_label', y='charges', ax=axes[0,0])
            axes[0,0].set_title('Charges by Smoking Status', fontweight='bold')
            axes[0,0].yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'${x:,.0f}'))

        # Box plot 2: Charges by Sex
        if 'sex_label' in self.df_labeled.columns:
            sns.boxplot(data=self.df_labeled, x='sex_label', y='charges', ax=axes[0,1])
            axes[0,1].set_title('Charges by Sex', fontweight='bold')
            axes[0,1].yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'${x:,.0f}'))

        # Box plot 3: Charges by Region
        if 'region_label' in self.df_labeled.columns:
            sns.boxplot(data=self.df_labeled, x='region_label', y='charges', ax=axes[1,0])
            axes[1,0].set_title('Charges by Region', fontweight='bold')
            axes[1,0].tick_params(axis='x', rotation=45)
            axes[1,0].yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'${x:,.0f}'))

        # Box plot 4: Charges by Children
        sns.boxplot(data=self.df_clean, x='children', y='charges', ax=axes[1,1])
        axes[1,1].set_title('Charges by Number of Children', fontweight='bold')
        axes[1,1].yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'${x:,.0f}'))

        plt.tight_layout()

        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            print(f"✅ Box plots saved to: {save_path}")

        return fig

    def create_all_required_plots(self, output_dir='/home/user/output/'):
        """
        Create all required plots and save them.

        Parameters:
        output_dir (str): Directory to save all plots

        Returns:
        dict: Dictionary of created figures
        """
        print("🎨 Creating all required visualizations...")

        figures = {}

        # 1. Line chart
        figures['line_chart'] = self.create_line_chart(
            save_path=f'{output_dir}line_chart_age_vs_charges.png'
        )
        plt.close()

        # 2. Bar chart
        figures['bar_chart'] = self.create_bar_chart(
            save_path=f'{output_dir}bar_chart_region_charges.png'
        )
        plt.close()

        # 3. Histogram
        figures['histogram'] = self.create_histogram(
            save_path=f'{output_dir}histogram_bmi_distribution.png'
        )
        plt.close()

        # 4. Scatter plot
        figures['scatter_plot'] = self.create_scatter_plot(
            save_path=f'{output_dir}scatter_plot_bmi_vs_charges.png'
        )
        plt.close()

        # 5. Correlation heatmap
        figures['correlation_heatmap'] = self.create_correlation_heatmap(
            save_path=f'{output_dir}correlation_heatmap.png'
        )
        plt.close()

        # 6. Box plots
        figures['box_plots'] = self.create_box_plots(
            save_path=f'{output_dir}box_plots_categorical.png'
        )
        plt.close()

        print("✅ All visualizations created and saved!")
        return figures

# Example usage
if __name__ == "__main__":
    print("This module requires cleaned data from data_loader.py")
    print("Example usage:")
    print("  from data_loader import MedicalInsuranceDataLoader")
    print("  from data_visualizer import MedicalInsuranceVisualizer")
    print("  ")
    print("  # Load and clean data")
    print("  loader = MedicalInsuranceDataLoader(url='your_url')")
    print("  clean_data = loader.clean_data()")
    print("  labeled_data = loader.create_labeled_data()")
    print("  ")
    print("  # Create visualizations")
    print("  visualizer = MedicalInsuranceVisualizer(clean_data, labeled_data)")
    print("  figures = visualizer.create_all_required_plots()")
