#Libraries used
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
#code

# Reading DataSet
data = pd.read_excel("/Users/gurdeeprathi/Downloads/Project_Dataset.xlsx")
print("Data imported succesfully")

print(data.head())


data.info()


print(data.describe())

print("\nMissing Values:\n", data.isnull().sum())


print("\nDuplicate Rows:", data.duplicated().sum())








#objective N
crime_data = data.iloc[:, 3:]

crime_totals = crime_data.sum().sort_values(ascending=False)
top_10_crimes = crime_totals.head(10)
print("Top 10 Most Prevalent Crimes Against Women:\n")
print(top_10_crimes)
plt.figure(figsize=(10, 6))
sns.barplot(x=top_10_crimes.values,
hue=top_10_crimes.index,
y=top_10_crimes.index,
palette='magma',
legend=False
)
plt.title('Top 10 Most Prevalent Crimes Against Women')
plt.xlabel('Total Cases')
plt.ylabel('Crime Category')
plt.show()




#objective 3: 1.To compare the frequency of crimes committed against women above 18 and girls below 18 using age-segmented data columns such as rape, attempt to rape, and assault
adult_crimes = ['Rape ', 'Rape of Women (above 18)', 'Sexual Harassment']
minor_crimes = ['Child Rape', 'Sexual Assault of Children', 'Use of Child for Pornography']

adult_total = data[adult_crimes].sum().sum()
minor_total = data[minor_crimes].sum().sum()

crime_comparison = pd.Series({'Women (18+)': adult_total, 'Girls (<18)': minor_total})

# Plotting
plt.figure(figsize=(6, 5))
sns.barplot(x=crime_comparison.index, y=crime_comparison.values)
plt.title('Comparison of Crimes Against Women vs Girls')
plt.ylabel('Total Cases')
plt.xlabel('Age Group')

plt.show()

crime_data = data.iloc[:, 3:]

# Get top 15 crimes based on total counts
top_15_crimes = crime_data.sum().sort_values(ascending=False).head(10).index.tolist()


# Calculate total crimes per state
state_crimes = data.groupby('State').sum(numeric_only=True)
state_crimes['Total Crimes'] = state_crimes.sum(axis=1)

# Sort and get top 10 states
top10_states_line = state_crimes['Total Crimes'].sort_values(ascending=False).head(10)

# Plotting the Line Chart
plt.figure(figsize=(12, 6))
plt.plot(top10_states_line.index, top10_states_line.values, marker='o', linestyle='-', color='b', linewidth=2)

plt.title('Trend of Total Crimes Against Women in Top 10 States', fontsize=14)
plt.xlabel('State', fontsize=12)
plt.ylabel('Total Cases', fontsize=12)
plt.xticks(rotation=45)
plt.grid(True, linestyle='--', alpha=0.7)
plt.tight_layout()

plt.show()


# Reading DataSet
data=pd.read_excel("/Users/gurdeeprathi/Downloads/Project_Dataset.xlsx")
print("Data imported succesfully")
exclude_cols = ['SNo', 'Year', 'State/UT', 'District']
crime_cols = [col for col in data.columns if col not in exclude_cols and data[col].dtype in ['int64', 'float64']]

# Group by State/UT and calculate total crimes
state_crimes = data.groupby('State')[crime_cols].sum()
state_crimes['Total Crimes'] = state_crimes.sum(axis=1)

# Sort and get top 10 states
top10_states = state_crimes['Total Crimes'].sort_values(ascending=False).head(10)

# Plot pie chart
plt.figure(figsize=(10, 8))
plt.pie(top10_states, labels=top10_states.index, autopct='%1.1f%%', startangle=140, textprops={'fontsize': 9})
plt.title('Top 10 States Contributing to National Crimes Against Women', fontsize=14)
plt.tight_layout()
plt.show()
