import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# Load dataset
data = pd.read_excel("/Users/gurdeeprathi/Downloads/Project_Dataset.xlsx")

# All crime columns (skip S.No, State, District)
crime_cols = [c for c in data.columns if c not in ['S. No', 'State', 'District']]
#Objective 1: Year-wise Trend of Total Crimes

# Add up each crime column across all rows
crime_totals = data[crime_cols].sum().sort_values(ascending=False)
top10 = crime_totals.head(10)
top10.index = [i.strip() for i in top10.index]  # clean spaces

plt.figure(figsize=(12, 7))
colors = sns.color_palette('magma', 10)
bars = plt.barh(top10.index[::-1], top10.values[::-1], color=colors[::-1])

# Add value labels on each bar
for bar, val in zip(bars, top10.values[::-1]):
    plt.text(bar.get_width() + 200, bar.get_y() + bar.get_height()/2,
             f'{int(val):,}', va='center', fontsize=9)

plt.title('Top 10 Most Prevalent Crimes Against Women', fontsize=14, fontweight='bold')
plt.xlabel('Total Reported Cases')
plt.ylabel('Crime Category')
plt.tight_layout()
plt.show()



#Objective 2 — Which States Have the Most Crimes?
# Group by state and sum all crimes
state_crimes = data.groupby('State')[crime_cols].sum()
state_crimes['Total'] = state_crimes.sum(axis=1)
top10_states = state_crimes['Total'].sort_values(ascending=False).head(10)

fig, axes = plt.subplots(1, 2, figsize=(16, 7))
fig.suptitle('State-wise Crime Distribution', fontsize=14, fontweight='bold')

# Left: Bar chart
sns.barplot(x=top10_states.values,
hue=top10_states.index,
y=top10_states.index,
palette='Reds_r',
ax=axes[0])
axes[0].set_title('Top 10 States by Total Crimes')
axes[0].set_xlabel('Total Cases')
axes[0].set_ylabel('State')

# Right: Pie chart
axes[1].pie(top10_states.values, labels=top10_states.index,
            autopct='%1.1f%%', startangle=140, explode=[0.05]*10,
            wedgeprops={'edgecolor': 'white'},
            colors=sns.color_palette('Spectral', 10))
axes[1].set_title('Share of Top 10 States')

plt.tight_layout()
plt.show()



#Objective 3 — Women (18+) vs Girls (under 18)
# Define age-specific columns
adult_cols = ['Rape of Women (above 18)', 'Attempt to rape Women (above 18)',
              'Assault on Women (18 Yrs. And above)', 'insult to modesty Women (18 Yrs. And above)']
minor_cols = ['Rape of Women (Below 18)', 'Attempt to rape Girls (Below 18)',
              'Assualt on Girls (Below 18 yrs)', 'Child Rape']
labels = ['Rape', 'Attempt to Rape', 'Assault', 'Other']

adult_vals = [data[c].sum() for c in adult_cols]
minor_vals  = [data[c].sum() for c in minor_cols]

fig, axes = plt.subplots(1, 2, figsize=(16, 7))
fig.suptitle('Women (18+) vs Girls (Under 18) — Crime Comparison', fontsize=13, fontweight='bold')

# Left: Grouped bar
x = np.arange(4)
axes[0].bar(x - 0.175, adult_vals, 0.35, label='Women (18+)', color='#E07B7B', edgecolor='white')
axes[0].bar(x + 0.175, minor_vals, 0.35, label='Girls (<18)',  color='#7BAEE0', edgecolor='white')
axes[0].set_xticks(x)
axes[0].set_xticklabels(labels, fontsize=9)
axes[0].set_ylabel('Total Cases')
axes[0].set_title('Crime Breakdown by Age Group')
axes[0].legend()

# Right: Donut chart
total_adult = sum(adult_vals)
total_minor = sum(minor_vals)
axes[1].pie([total_adult, total_minor],
            labels=[f'Women (18+)\n{total_adult:,}', f'Girls (<18)\n{total_minor:,}'],
            colors=['#E07B7B', '#7BAEE0'], autopct='%1.1f%%',
            wedgeprops={'width': 0.5, 'edgecolor': 'white'})
axes[1].set_title('Overall Share: Women vs Girls')

plt.tight_layout()
plt.show()





#Objective 4 — Crime Type Breakdown in Top 5 States (Stacked Bar)
# Pick 6 major crime categories to compare across top states
selected_crimes = ['Dowry Deaths', 'Cruelty by Inlaws',
                   'Kidnapping & Abduction of Women',
                   'Rape ', 'Cyber Crimes',
                   'Protection of Women from Domestic Violence Act']
nice_labels = ['Dowry Deaths', 'Cruelty by Inlaws',
               'Kidnapping', 'Rape', 'Cyber Crimes', 'Domestic Violence']

# Find top 5 states by total crimes
state_crimes = data.groupby('State')[crime_cols].sum()
state_crimes['Total'] = state_crimes.sum(axis=1)
top5 = state_crimes['Total'].sort_values(ascending=False).head(5).index.tolist()

# Build plot data
plot_df = state_crimes.loc[top5, selected_crimes].copy()
plot_df.columns = nice_labels

plot_df.plot(kind='bar', stacked=True, colormap='tab10',
             figsize=(12, 7), edgecolor='white')
plt.title('Objective 5: What Types of Crimes Happen Most in Top 5 States?',
          fontsize=14, fontweight='bold')
plt.xlabel('State')
plt.ylabel('Total Cases')
plt.xticks(rotation=20, ha='right')
plt.legend(title='Crime Type', bbox_to_anchor=(1.01, 1), loc='upper left')
plt.tight_layout()
plt.show()





#Objective 6 — Cyber Crimes vs Traditional Crimes by State
# Define crime groups
traditional = ['Rape ', 'Dowry Deaths', 'Cruelty by Inlaws',
               'Kidnapping & Abduction of Women', 'Acid Attack']
cyber       = ['Cyber Crimes', 'Publishing or Transmitting of Sexually Explicit Material',
               'Other Women Centric Cyber Crimes']

# Total per state
state_group = data.groupby('State')
trad_total  = state_group[traditional].sum().sum(axis=1)
cyber_total = state_group[cyber].sum().sum(axis=1)

# Build comparison dataframe
compare_df = pd.DataFrame({'Traditional Crimes': trad_total, 'Cyber Crimes': cyber_total})
top10 = compare_df.sort_values('Traditional Crimes', ascending=False).head(10)

fig, axes = plt.subplots(1, 2, figsize=(16, 7))
fig.suptitle('Objective 6: Cyber Crimes vs Traditional Crimes by State',
             fontsize=14, fontweight='bold')

# Left: Grouped bar
top10.plot(kind='bar', ax=axes[0], color=['#FF6B6B', '#4ECDC4'], edgecolor='white')
axes[0].set_title('Top 10 States: Cyber vs Traditional')
axes[0].set_xlabel('State')
axes[0].set_ylabel('Total Cases')
axes[0].set_xticklabels(top10.index, rotation=30, ha='right')
axes[0].legend(title='Crime Type')

# Right: Scatter — does high traditional = high cyber?
axes[1].scatter(trad_total, cyber_total, color='steelblue', alpha=0.7, s=60)
for state in trad_total.nlargest(5).index:
    axes[1].annotate(state, (trad_total[state], cyber_total[state]),
                     fontsize=7, xytext=(5, 3), textcoords='offset points')
axes[1].set_title('Are States with More Traditional Crimes\nAlso High in Cyber Crimes?')
axes[1].set_xlabel('Traditional Crime Total')
axes[1].set_ylabel('Cyber Crime Total')

plt.tight_layout()
plt.show()
