import pandas as pd
import os
import matplotlib.pyplot as plt
import numpy as np

#  ZADANIE 1
files = [f for f in os.listdir('.') if f.endswith('.txt')]
df_list = []
for file in files:
    tmp_df = pd.read_csv(file, index_col=None, header=None)
    year = file[3:-4]
    tmp_df.loc[:, 'year'] = year
    tmp_df.rename(columns={0: 'name', 1: 'gender', 2: 'number'}, inplace=True)
    tmp_df.loc[:, 'total_births'] = tmp_df.loc[:, 'number'].sum()
    tmp_df.loc[:, 'total_births_male'] = tmp_df.loc[tmp_df['gender']=='M', 'number'].sum()
    tmp_df.loc[:, 'total_births_female'] = tmp_df.loc[tmp_df['gender'] == 'F', 'number'].sum()
    df_list.append(tmp_df)
    # print(tmp_df)
df = pd.concat(df_list, axis=0, ignore_index=True)
print(df)

#  ZADANIE 2
print("\nZADANIE 2")
names = df.loc[:, 'name'].unique()
print("Unikalnych imion: " + str(len(names)))

#  ZADANIE 3
print("\nZADANIE 3")
names_m = df.loc[df['gender'] == 'M', 'name'].unique()
names_f = df.loc[df['gender'] == 'F', 'name'].unique()
print("Unikalnych imion męskich: " + str(len(names_m)))
print("Unikalnych imion żeńskich: " + str(len(names_f)))

#  ZADANIE 4
print("\nZADANIE 4")
df.loc[df['gender'] == 'M', 'male_frequency'] = df.loc[df['gender'] == 'M', 'number'] / df.loc[df['gender'] == 'M', 'total_births_male']
df.loc[df['gender'] == 'F', 'female_frequency'] = df.loc[df['gender'] == 'F', 'number'] / df.loc[df['gender'] == 'F', 'total_births_female']
print(df[['male_frequency', 'female_frequency']])

#  ZADANIE 5
print("\nZADANIE 5")
births_per_year = df[['year', 'total_births', 'total_births_male', 'total_births_female']].groupby(['year'], as_index=False).mean()
births_per_year['f_m_ratio'] = births_per_year.loc[:, 'total_births_female']/births_per_year.loc[:, 'total_births_male']

fig, axes = plt.subplots(nrows=2, ncols=1)
births_per_year.plot(ax=axes[0],x='year', y='total_births'); axes[0].set_title('Liczba narodzin w danym roku')
births_per_year.plot(ax=axes[1],x='year', y=['f_m_ratio']); axes[1].set_title('Stosunek liczby narodzin dziewczynek do liczby narodzin chłopców')
plt.show()

roznica_df = births_per_year.iloc[(births_per_year['f_m_ratio']-1).abs().argsort()]
print('Najmniejszą różnicę w liczbie urodzeń między chłopcami a dziewczynkami zanotowano w roku ' + str(roznica_df['year'].iloc[0])
      +', a największą w roku ' + str(roznica_df['year'].iloc[-1]))

#  ZADANIE 6
print("\nZADANIE 6")
popular_male: pd.DataFrame = df.loc[df['gender'] == 'M', :].pivot(index='year', columns='name', values=['number', 'total_births_male'])
popular_female: pd.DataFrame = df.loc[df['gender'] == 'F', :].pivot(index='year', columns='name', values=['number','total_births_female'])
popular_female.rename(columns={'total_births_female': 'total_births'}, inplace=True)
popular_male.rename(columns={'total_births_male': 'total_births'}, inplace=True)
popular = popular_male.add(popular_female, fill_value=0)
popular = pd.DataFrame(popular)
# print(popular)

# print(popular['number'])

def top1000(popular_df):
    popular_df = popular_df.fillna(0)
    popular_df2 = pd.DataFrame()
    for index, row in popular_df.iterrows():
        popular_df2 = popular_df2.append(row.sort_values(ascending=False)[:1000])
    return popular_df2.sum(axis=0).sort_values(ascending=False)[:1000]


male_top_1000: pd.DataFrame = top1000(popular_male['number'])
female_top_1000 = top1000(popular_female['number'])
print('\nNajpopularniejsze imiona męskie: ')
print(male_top_1000)
print('\nNajpopularniejsze imiona żeńskie: ')
print(female_top_1000)

#  ZADANIE 7
print("\nZADANIE 7")
fig, axes = plt.subplots(nrows=2, ncols=2, figsize=(15, 8))
names_list = ['Harry', 'Marilin', male_top_1000.index[0], female_top_1000.index[0]]
axs = [(0,0), (0,1), (1,0), (1,1)]
lata = ['1940', '1980', '2019']
for it_name, it_ax in zip(names_list, axs):
    name_data = popular['number'].loc[:,it_name]
    name_data.plot(ax=axes[it_ax], label='Liczba').set_title(it_name)
    for rok in lata:
        liczba = str(popular['number'].fillna(0).loc[rok, it_name])
        print("Liczba " + it_name + " w roku " + rok + ": " + liczba)
    lines, labels = axes[it_ax].get_legend_handles_labels()
    ax2 = axes[it_ax].twinx()
    ax2.spines['right'].set_position(('axes', 1.0))
    name_data = popular['number'].loc[:, it_name]/popular['total_births'].loc[:, it_name]
    name_data.plot(ax=ax2, label='Popularność', color='red')
    line, label = ax2.get_legend_handles_labels()
    lines += line
    labels += label
    plt.legend(lines, labels, loc='upper right')
    print("-----")
plt.show()