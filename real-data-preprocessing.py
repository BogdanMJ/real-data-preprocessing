import pandas
import numpy

data = pandas.read_csv('EURUSD_H4.csv')
df = pandas.DataFrame(data)
data_2500 = df.head(2500) # Wyciągnięcie pierwszsych 2500 elementów

del data_2500["SMA14IND"] # usunięcie całej kolumny
del data_2500["SMA50IND"] # usunięcie całej kolumny

pusteCLOSE = data_2500['Close'].isna().sum() #Zliczanie elementów pustych w kolumnie CLOSE

data_2500['Close'] = data_2500['Close'].interpolate() # uzupełnienie pustych danych o srednią z 2 sąsiednich
data_2500['SMA14'] = data_2500['SMA14'].interpolate() # uzupełnienie pustych danych o srednią z 2 sąsiednich
data_2500['SMA50'] = data_2500['SMA50'].interpolate() # uzupełnienie pustych danych o srednią z 2 sąsiednich

data_2500['Bulls'] = data_2500['Bulls'].fillna(0) # Uzupełnia wartoci puste liczbą 0
data_2500['CCI'] = data_2500['CCI'].fillna(0) # Uzupełnia wartoci puste liczbą 0
data_2500['DM'] = data_2500['DM'].fillna(0) # Uzupełnia wartoci puste liczbą 0
data_2500['OSMA'] = data_2500['OSMA'].fillna(0) # Uzupełnia wartoci puste liczbą 0
data_2500['RSI'] = data_2500['RSI'].fillna(0) # Uzupełnia wartoci puste liczbą 0
data_2500['Stoch'] = data_2500['Stoch'].fillna(0) # Uzupełnia wartoci puste liczbą 0

kor1 = data_2500['Close'].corr(data_2500['SMA14']) # korelacja między kolumnami
kor2 = data_2500['Close'].corr(data_2500['SMA50'])
większa_korelacja = max(kor1, kor2)

# usunięcie kolumny o większej korelacji
if kor1 < kor2:
    del data_2500["SMA50"]
if kor1 > kor2:
    del data_2500["SMA14"]


#Wyciąganie wartoci ujemnych z CCI
ujemne_CCI = []
for el in data_2500['CCI']:
    if el < 0 :
        ujemne_CCI.append(el)
print(f"Iloć ujemnych atrybutów dla CCI wynosi: {len(ujemne_CCI)}") 

#Podanie min i max dla pozostałych atrybutów -> ??

min_Close = data_2500['Close'].min()
max_Close = data_2500['Close'].max()

min_SMA50 = data_2500['SMA50'].min()
max_SMA50 = data_2500['SMA50'].max()

min_Bulls = data_2500['Bulls'].min()
max_Bulls = data_2500['Bulls'].max()

#Normalizacja danych dla kolumn Close i SMA50
atrybuty = ['Close','SMA50']
for atrybut in atrybuty:
    max = data_2500[atrybut].max()
    min = data_2500[atrybut].min()
    data_2500[atrybut] = (data_2500[atrybut] - min) / (max - min)

"""
seria = pandas.cut(pandas.Series(numpy.array(data_2500['Bulls'])),2,labels=['Lower','Upper'])
data_2500['Bulls'].hist()
"""

data_2500['Bulls'].hist() # histogram przed dyskretyzacją

# histogram po dyskretyzacji
etykiety = ['Up','Down']
seria = pandas.Series(numpy.array(data_2500['Bulls']))
wynik = pandas.cut(seria,2,labels = etykiety)  
wynik.hist()


data_2500['Close'].hist() # histogram przed dyskretyzacją

# histogram po dyskretyzacji
etykietyClose = ['0,0 - 0,25','0,26 - 0,5','0,51 - 0,75','0,76 - 1,0']
seriaClose = pandas.Series(numpy.array(data_2500['Close']))
wynikClose = pandas.cut(seriaClose,4,labels = etykietyClose)
wynikClose.hist()

#Rysowanie wykresu kołowego
data_2500['Decision'].value_counts().plot.pie()

#rysowanie wykresu liniowego 

data_2500['Close'].plot()


print(f"Puste z kolumy Close: {pusteCLOSE}")
print(f"Większa Korelacja dla: {większa_korelacja}")
print(data_2500)
