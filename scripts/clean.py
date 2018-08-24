import pandas as pd

data_2015 = pd.DataFrame.from_csv("batters2015.csv").reset_index()
data_2016 = pd.DataFrame.from_csv("batters2016.csv").reset_index()
data_2017 =  pd.DataFrame.from_csv("batters2017.csv").reset_index()

names_2015 = set(data_2015['Player'])
names_2016 = set(data_2016['Player'])
names_2017 = set(data_2017['Player'])

common_names = names_2015.intersection(names_2016, names_2017)
selected_2015 = data_2015.loc[data_2015['Player'].isin(common_names)]
selected_2016 = data_2016.loc[data_2016['Player'].isin(common_names)]
selected_2017 = data_2017.loc[data_2017['Player'].isin(common_names)]

data = pd.concat([selected_2015, selected_2016, selected_2017])

data['hr/ab'] = data['HR']/data['AB']
data['so/ab'] = data['SO']/data['AB']
data['obp'] = data['OBP']

data.drop(data.iloc[:, 4:32],  axis = 1, inplace = True)
data.reset_index(drop = True, inplace = True)
data['Player'] = data['Player'].str.replace(', ','-')

data.to_csv("data.csv")