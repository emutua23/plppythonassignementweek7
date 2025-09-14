"""
Medical Insurance Dataset - Data Analysis Module
===============================================

This module provides comprehensive statistical analysis capabilities for medical insurance data.
Author: Data Analysis System
Date: September  2025
"""

import pandas as pd
import numpy as np
from scipy import stats
import warnings
warnings.filterwarnings('ignore')

class MedicalInsuranceAnalyzer:
    """
    A class to perform comprehensive analysis on medical insurance data.
    """

    def __init__(self, df_clean, df_labeled=None):
        """
        Initialize the analyzer with clean data.

        Parameters:
        df_clean (pd.DataFrame): Cleaned numerical dataset
        df_labeled (pd.DataFrame): Dataset with human-readable labels
        """
        self.df_clean = df_clean
        self.df_labeled = df_labeled if df_labeled is not None else df_clean
        self.analysis_results = {}

    def basic_statistics(self):
        """
        Calculate basic descriptive statistics.

        Returns:
        dict: Basic statistics summary
        """
        print("📊 Calculating basic statistics...")

        desc_stats = self.df_clean.describe()
        additional_stats = {
            'median': self.df_clean.select_dtypes(include=[np.number]).median(),
            'mode': self.df_clean.select_dtypes(include=[np.number]).mode().iloc[0],
            'std_dev': self.df_clean.select_dtypes(include=[np.number]).std(),
            'variance': self.df_clean.select_dtypes(include=[np.number]).var(),
            'skewness': self.df_clean.select_dtypes(include=[np.number]).skew(),
            'kurtosis': self.df_clean.select_dtypes(include=[np.number]).kurtosis()
        }

        self.analysis_results['basic_stats'] = {
            'descriptive': desc_stats,
            'additional': additional_stats
        }

        return self.analysis_results['basic_stats']

    def correlation_analysis(self):
        """
        Perform correlation analysis.

        Returns:
        dict: Correlation results
        """
        print("🔗 Performing correlation analysis...")

        corr_matrix = self.df_clean.corr()

        # Find strongest correlations with charges
        charges_corr = corr_matrix['charges'].drop('charges').abs().sort_values(ascending=False)

        self.analysis_results['correlation'] = {
            'matrix': corr_matrix,
            'charges_correlations': charges_corr,
            'strongest_predictor': charges_corr.index[0],
            'strongest_correlation': charges_corr.iloc[0]
        }

        return self.analysis_results['correlation']

    def group_analysis(self):
        """
        Perform group-based analysis for categorical variables.

        Returns:
        dict: Group analysis results
        """
        print("👥 Performing group analysis...")

        group_results = {}

        if 'smoker_label' in self.df_labeled.columns:
            # Smoker analysis
            smoker_stats = self.df_labeled.groupby('smoker_label')['charges'].agg([
                'count', 'mean', 'median', 'std', 'min', 'max'
            ])
            group_results['smoker'] = smoker_stats

        if 'sex_label' in self.df_labeled.columns:
            # Sex analysis
            sex_stats = self.df_labeled.groupby('sex_label')['charges'].agg([
                'count', 'mean', 'median', 'std', 'min', 'max'
            ])
            group_results['sex'] = sex_stats

        if 'region_label' in self.df_labeled.columns:
            # Region analysis
            region_stats = self.df_labeled.groupby('region_label')['charges'].agg([
                'count', 'mean', 'median', 'std', 'min', 'max'
            ])
            group_results['region'] = region_stats

        # Children analysis
        children_stats = self.df_clean.groupby('children')['charges'].agg([
            'count', 'mean', 'median', 'std', 'min', 'max'
        ])
        group_results['children'] = children_stats

        self.analysis_results['groups'] = group_results
        return group_results

    def statistical_tests(self):
        """
        Perform statistical tests for group differences.

        Returns:
        dict: Statistical test results
        """
        print("🧮 Performing statistical tests...")

        test_results = {}

        # T-test for smoker vs non-smoker charges
        if 'smoker_label' in self.df_labeled.columns:
            smoker_charges = self.df_labeled[self.df_labeled['smoker_label'] == 'yes']['charges']
            nonsmoker_charges = self.df_labeled[self.df_labeled['smoker_label'] == 'no']['charges']

            t_stat, p_value = stats.ttest_ind(smoker_charges, nonsmoker_charges)
            test_results['smoker_ttest'] = {
                't_statistic': t_stat,
                'p_value': p_value,
                'significant': p_value < 0.05
            }

        # T-test for male vs female charges
        if 'sex_label' in self.df_labeled.columns:
            male_charges = self.df_labeled[self.df_labeled['sex_label'] == 'male']['charges']
            female_charges = self.df_labeled[self.df_labeled['sex_label'] == 'female']['charges']

            t_stat, p_value = stats.ttest_ind(male_charges, female_charges)
            test_results['sex_ttest'] = {
                't_statistic': t_stat,
                'p_value': p_value,
                'significant': p_value < 0.05
            }

        # ANOVA for regional differences
        if 'region_label' in self.df_labeled.columns:
            region_groups = [group['charges'].values for name, group in self.df_labeled.groupby('region_label')]
            f_stat, p_value = stats.f_oneway(*region_groups)
            test_results['region_anova'] = {
                'f_statistic': f_stat,
                'p_value': p_value,
                'significant': p_value < 0.05
            }

        self.analysis_results['statistical_tests'] = test_results
        return test_results

    def generate_insights(self):
        """
        Generate key insights from the analysis.

        Returns:
        dict: Key insights and findings
        """
        print("💡 Generating insights...")

        insights = {}

        # Correlation insights
        if 'correlation' in self.analysis_results:
            corr_data = self.analysis_results['correlation']
            insights['correlations'] = {
                'strongest_predictor': corr_data['strongest_predictor'],
                'correlation_value': corr_data['strongest_correlation'],
                'interpretation': self._interpret_correlation(corr_data['strongest_correlation'])
            }

        # Group insights
        if 'groups' in self.analysis_results:
            group_data = self.analysis_results['groups']

            if 'smoker' in group_data:
                smoker_means = group_data['smoker']['mean']
                if len(smoker_means) >= 2:
                    smoker_multiplier = smoker_means.max() / smoker_means.min()
                    insights['smoking_impact'] = {
                        'multiplier': smoker_multiplier,
                        'difference': smoker_means.max() - smoker_means.min(),
                        'high_group': smoker_means.idxmax(),
                        'low_group': smoker_means.idxmin()
                    }

        # Statistical significance insights
        if 'statistical_tests' in self.analysis_results:
            test_data = self.analysis_results['statistical_tests']
            significant_factors = []

            for test_name, results in test_data.items():
                if results['significant']:
                    significant_factors.append(test_name.replace('_ttest', '').replace('_anova', ''))

            insights['significant_factors'] = significant_factors

        self.analysis_results['insights'] = insights
        return insights

    def _interpret_correlation(self, corr_value):
        """
        Interpret correlation strength.

        Parameters:
        corr_value (float): Correlation coefficient

        Returns:
        str: Interpretation of correlation strength
        """
        abs_corr = abs(corr_value)

        if abs_corr >= 0.7:
            return "Strong"
        elif abs_corr >= 0.5:
            return "Moderate"
        elif abs_corr >= 0.3:
            return "Weak"
        else:
            return "Very weak"

    def run_full_analysis(self):
        """
        Run the complete analysis pipeline.

        Returns:
        dict: Complete analysis results
        """
        print("🔄 Running full analysis pipeline...")

        self.basic_statistics()
        self.correlation_analysis()
        self.group_analysis()
        self.statistical_tests()
        self.generate_insights()

        print("✅ Analysis complete!")
        return self.analysis_results

    def export_results(self, output_path='/home/user/output/analysis_results.json'):
        """
        Export analysis results to JSON file.

        Parameters:
        output_path (str): Path to save results
        """
        import json

        # Convert DataFrames to dictionaries for JSON serialization
        exportable_results = {}

        for key, value in self.analysis_results.items():
            if isinstance(value, dict):
                exportable_results[key] = {}
                for sub_key, sub_value in value.items():
                    if isinstance(sub_value, pd.DataFrame):
                        exportable_results[key][sub_key] = sub_value.to_dict()
                    elif isinstance(sub_value, pd.Series):
                        exportable_results[key][sub_key] = sub_value.to_dict()
                    else:
                        exportable_results[key][sub_key] = sub_value
            else:
                exportable_results[key] = value

        with open(output_path, 'w') as f:
            json.dump(exportable_results, f, indent=2, default=str)

        print(f"✅ Results exported to: {output_path}")

# Example usage
if __name__ == "__main__":
    # This would typically be used with data from data_loader.py
    print("This module requires cleaned data from data_loader.py")
    print("Example usage:")
    print("  from data_loader import MedicalInsuranceDataLoader")
    print("  from data_analyzer import MedicalInsuranceAnalyzer")
    print("  ")
    print("  # Load and clean data")
    print("  loader = MedicalInsuranceDataLoader(url='your_url')")
    print("  loader.download_data()")
    print("  loader.load_data()")
    print("  clean_data = loader.clean_data()")
    print("  labeled_data = loader.create_labeled_data()")
    print("  ")
    print("  # Analyze data")
    print("  analyzer = MedicalInsuranceAnalyzer(clean_data, labeled_data)")
    print("  results = analyzer.run_full_analysis()")
    print("  analyzer.export_results()")
