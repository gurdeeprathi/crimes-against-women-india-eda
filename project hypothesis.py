import pandas as pd
from scipy import stats

# Reading DataSet
data = pd.read_excel("/Users/gurdeeprathi/Downloads/Project_Dataset.xlsx")

# Defining columns based on previous context
adult_crimes = ['Rape ', 'Rape of Women (above 18)', 'Sexual Harassment']
minor_crimes = ['Child Rape', 'Sexual Assault of Children', 'Use of Child for Pornography']

# Calculating totals per district/row
adult_totals = data[adult_crimes].sum(axis=1)
minor_totals = data[minor_crimes].sum(axis=1)

# Performing a paired t-test
t_stat, p_value = stats.ttest_rel(adult_totals, minor_totals)

print(f"T-statistic: {t_stat:.4f}")
print(f"P-value: {p_value:.4e}")

if p_value < 0.05:
    print("Reject Null Hypothesis: Significant difference in mean crimes against adult women vs minor girls.")
else:
    print("Fail to Reject Null Hypothesis: No significant difference.")
