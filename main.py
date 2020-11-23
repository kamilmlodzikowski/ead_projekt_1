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
# print(df)

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
# print("\nZADANIE 4")
df.loc[df['gender'] == 'M', 'male_frequency'] = df.loc[df['gender'] == 'M', 'number'] / df.loc[df['gender'] == 'M', 'total_births_male']
df.loc[df['gender'] == 'F', 'female_frequency'] = df.loc[df['gender'] == 'F', 'number'] / df.loc[df['gender'] == 'F', 'total_births_female']
# print(df[['male_frequency', 'female_frequency']])

#  ZADANIE 5
print("\nZADANIE 5")
births_per_year = df[['year', 'total_births', 'total_births_male', 'total_births_female']].groupby(['year'], as_index=False).mean()
births_per_year['f_m_ratio'] = births_per_year.loc[:, 'total_births_female']/births_per_year.loc[:, 'total_births_male']

fig, axes = plt.subplots(nrows=2, ncols=1)
births_per_year.plot(ax=axes[0],x='year', y='total_births'); axes[0].set_title('Liczba narodzin w danym roku - zad 1')
births_per_year.plot(ax=axes[1],x='year', y=['f_m_ratio']); axes[1].set_title('Stosunek liczby narodzin dziewczynek do liczby narodzin chłopców - zad 1')


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
    return popular_df2


popular_by_year_male = top1000(popular_male['number'])
popular_by_year_female = top1000(popular_female['number'])
male_top_1000: pd.DataFrame = popular_by_year_male.sum(axis=0).sort_values(ascending=False)[:1000]
female_top_1000 = popular_by_year_female.sum(axis=0).sort_values(ascending=False)[:1000]
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
    name_data.plot(ax=axes[it_ax], label='Liczba').set_title(it_name+" - zad 7")
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


#  ZADANIE 8
print("\nZADANIE 8")
births_per_year.set_index('year', inplace=True)
procent_df = pd.DataFrame(index=births_per_year.index)

procent_df.loc[:,'male'] = popular_by_year_male.sum(axis=1)/births_per_year.loc[:,'total_births_male']
procent_df.loc[:,'female'] = popular_by_year_female.sum(axis=1)/births_per_year.loc[:,'total_births_female']
procent_df.rename_axis('year', inplace=True)
procent_df.plot(use_index=True, y=['male', 'female']).set_title('Różnorodność imion - zad 8')

roznica_df = procent_df.iloc[(procent_df['male']-procent_df['female']).abs().argsort()]
print('Największą różnicę w różnorodności między imionami męskimi a żeńskimi zaobserwowano w '+str(roznica_df.iloc[-1].name+' roku.'))

#  ZADANIE 9
print("\nZADANIE 9")
df.loc[:, 'last_letter'] = pd.Series([i[-1] for i in df.loc[:, 'name'].values])
letter_df: pd.DataFrame = df[['year', 'gender', 'last_letter', 'number']].groupby(['year', 'gender', 'last_letter']).sum()
years = ['1910', '1960', '2015']
genders = ['M', 'F']
letter_df = letter_df.loc[years]
for year in years:
    letter_df.loc[year, 'total'] = letter_df.loc[year, 'number'].sum()
letter_df['norm'] = letter_df['number']/letter_df['total']
tmp_letter_df = pd.DataFrame()
for year in years:
    # for gender in genders:
    tmp_letter_df.loc[:, year] = letter_df.loc[year, 'norm']
fig, axes = plt.subplots(nrows=2, ncols=1)
tmp_letter_df.loc['F',:].plot.bar(ax=axes[0],use_index=True, y=years).set_title("Popularności litery u kobiet - zad 9")
tmp_letter_df.loc['M',:].plot.bar(ax=axes[1],use_index=True, y=years).set_title("Popularności litery u mężczyzn - zad 9")


roznica_df_male = tmp_letter_df.loc['M',:].iloc[(tmp_letter_df.loc['M','2015']-tmp_letter_df.loc['M','1910']).argsort()]
roznica_df_male['roznica'] = roznica_df_male['2015']-roznica_df_male['1910']
# print(roznica_df_male)
print("U mężczyzn największy spadek ma litera '" + str(roznica_df_male.iloc[0].name) + "', a wzrost litera '"
      + str(roznica_df_male.iloc[-1].name)+ "'.")
roznica_df_male = tmp_letter_df.loc['M',:].iloc[(tmp_letter_df.loc['M','2015']-tmp_letter_df.loc['M','1910']).abs().argsort()]
roznica_df_male['roznica'] = (roznica_df_male['2015']-roznica_df_male['1910']).abs()

roznica_df_female = tmp_letter_df.loc['F',:].iloc[(tmp_letter_df.loc['F','2015']-tmp_letter_df.loc['F','1910']).argsort()]
roznica_df_female['roznica'] = roznica_df_female['2015']-roznica_df_female['1910']
# print(roznica_df_female)
print("U kobiet największy spadek ma litera '" + str(roznica_df_female.iloc[0].name) + "', a wzrost litera '"
      + str(roznica_df_female.iloc[-1].name)+ "'.")
roznica_df_female = tmp_letter_df.loc['F',:].iloc[(tmp_letter_df.loc['F','2015']-tmp_letter_df.loc['F','1910']).abs().argsort()]
roznica_df_female['roznica'] = (roznica_df_female['2015']-roznica_df_female['1910']).abs()

letter_df2: pd.DataFrame = df[['year', 'gender', 'last_letter', 'number']].groupby(['year', 'gender', 'last_letter']).sum()
# print(letter_df2)
diff = [list(roznica_df_male.iloc[-3:].index), list(roznica_df_female.iloc[-3:].index)]

for year in births_per_year.index:
    letter_df2.loc[year, 'total'] = letter_df2.loc[year, 'number'].sum()
letter_df2['norm'] = letter_df2['number'] / letter_df2['total']

letter_df2 = letter_df2.groupby(['gender','last_letter', 'year']).sum()
fig, axes = plt.subplots(nrows=2, ncols=1)
titles = ['Przebieg trendu popularności najbardziej zmiennych liter u mężczyzn',
          'Przebieg trendu popularności najbardziej zmiennych liter u kobiet']
for gender, let_list , i,title in zip(genders,diff,[0,1],titles):
    for letter in let_list:
        letter_df2.loc[gender, :].loc[letter, :].plot(ax=axes[i], use_index=True, y='norm', label=letter).set_title(title+" - zad 9")
axes[0].set_ylabel('Popularność litery')
axes[1].set_ylabel('Popularność litery')

#  ZADANIE 10
print("\nZADANIE 10")
names = df[['name', 'gender', 'number']].groupby(['gender', 'name']).sum()
F_names = names.loc['F', :]
M_names = names.loc['M', :]
common_names = F_names.index.intersection(M_names.index)
F_names = F_names.loc[common_names, :].sort_values('number', ascending=False)
M_names = M_names.loc[common_names, :].sort_values('number', ascending=False)
print('Najpopularniejsze imię męskie: ', M_names.index[0])
print('Najpopularniejsze imię żeńskie: ', F_names.index[0])

#  ZADANIE 11
print("\nZADANIE 11")
ratio = df[['name', 'gender', 'year', 'number']].fillna(0).groupby(['gender', 'name', 'year']).sum()
ratio2 = pd.concat([pd.DataFrame(ratio.loc['M', :].rename(columns={"number": "male"})),
                    pd.DataFrame(ratio.loc['F', :].rename(columns={"number": "female"}))],
                   axis=1)

ratio2['ratio_M'] = (ratio2['male']/ratio2['male'].sum()).fillna(0)
ratio2['ratio_F'] = (ratio2['female']/ratio2['female'].sum()).fillna(0)
# print(ratio2)

ratio1880_1920 = ratio2.groupby(['year', 'name']).sum().loc['1880':'1920', :].groupby(['name']).sum()
ratio1880_1920['ratio_M'] = (ratio1880_1920['male']/(ratio1880_1920['male'].sum()+ratio1880_1920['female'].sum())).fillna(0).replace([np.inf, -np.inf], 0)
ratio1880_1920['ratio_F'] = (ratio1880_1920['female']/(ratio1880_1920['male'].sum()+ratio1880_1920['female'].sum())).fillna(0).replace([np.inf, -np.inf], 0)
ratio1880_1920['diff1'] = ratio1880_1920['ratio_M'] - ratio1880_1920['ratio_F']
# print(ratio1880_1920)

ratio2000_2020 = ratio2.groupby(['year', 'name']).sum().loc['2000':'2020', :].groupby(['name']).sum()
ratio2000_2020['ratio_M'] = (ratio2000_2020['male']/(ratio2000_2020['male'].sum()+ratio2000_2020['female'].sum())).fillna(0).replace([np.inf, -np.inf], 0)
ratio2000_2020['ratio_F'] = (ratio2000_2020['female']/(ratio2000_2020['male'].sum()+ratio2000_2020['female'].sum())).fillna(0).replace([np.inf, -np.inf], 0)
ratio2000_2020['diff2'] = ratio2000_2020['ratio_M'] - ratio2000_2020['ratio_F']
# print(ratio2000_2020)

diff = pd.concat([ratio1880_1920['diff1'], ratio2000_2020['diff2']], axis=1).dropna()
diff['diff'] = (diff['diff1'] - diff['diff2'])
diff.sort_values('diff', inplace=True)
print("Imiona, które były początkowo żeńskie: " + str(diff.index[0]) +' i ' + str(diff.index[1]))
print("Imiona, które były początkowo męskie: " + str(diff.index[-1]) +' i ' + str(diff.index[-2]))

fig, axes = plt.subplots(nrows=2, ncols=2)
ratio2.loc[str(diff.index[0]),:].plot(ax=axes[0,0], y=['ratio_M', 'ratio_F']).set_title(str(diff.index[0]))
ratio2.loc[str(diff.index[1]),:].plot(ax=axes[0,1], y=['ratio_M', 'ratio_F']).set_title(str(diff.index[1]))
ratio2.loc[str(diff.index[-1]),:].plot(ax=axes[1,0], y=['ratio_M', 'ratio_F']).set_title(str(diff.index[-1]))
ratio2.loc[str(diff.index[-2]),:].plot(ax=axes[1,1], y=['ratio_M', 'ratio_F']).set_title(str(diff.index[-2]))


plt.show()
