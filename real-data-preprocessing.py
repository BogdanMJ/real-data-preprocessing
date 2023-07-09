import pandas
import numpy

data = pandas.read_csv('EURUSD_H4.csv')
df = pandas.DataFrame(data)
data_2500 = df.head(2500) # Extraction of the first 2500 items

del data_2500["SMA14IND"] # remove the entire column
del data_2500["SMA50IND"] # remove the entire column

emptyCLOSE = data_2500['Close'].isna().sum() # Counting empty elements in the CLOSE column

data_2500['Close'] = data_2500['Close'].interpolate() # filling empty data with an average of 2 neighboring ones
data_2500['SMA14'] = data_2500['SMA14'].interpolate() # filling empty data with an average of 2 neighboring ones
data_2500['SMA50'] = data_2500['SMA50'].interpolate() # filling empty data with an average of 2 neighboring ones

data_2500['Bulls'] = data_2500['Bulls'].fillna(0) # Filling blank values with 0
data_2500['CCI'] = data_2500['CCI'].fillna(0) # Filling blank values with 0
data_2500['DM'] = data_2500['DM'].fillna(0) # Filling blank values with 0
data_2500['OSMA'] = data_2500['OSMA'].fillna(0) # Filling blank values with 0
data_2500['RSI'] = data_2500['RSI'].fillna(0) # Filling blank values with 0
data_2500['Stoch'] = data_2500['Stoch'].fillna(0)# Filling blank values with 0

kor1 = data_2500['Close'].corr(data_2500['SMA14']) # correlation between columns
kor2 = data_2500['Close'].corr(data_2500['SMA50']) # correlation between columns
greater_correlation = max(kor1, kor2)

# delete column with higher correlation
if kor1 < kor2:
    del data_2500["SMA50"]
if kor1 > kor2:
    del data_2500["SMA14"]


#Extracting negative values from CCI
negative_CCI = []
for el in data_2500['CCI']:
    if el < 0 :
        negative_CCI.append(el)
print(f"The number of negative attributes for CCI is: {len(negative_CCI)}") 

# Specifying min and max for other attributes

min_Close = data_2500['Close'].min()
max_Close = data_2500['Close'].max()

min_SMA50 = data_2500['SMA50'].min()
max_SMA50 = data_2500['SMA50'].max()

min_Bulls = data_2500['Bulls'].min()
max_Bulls = data_2500['Bulls'].max()

#Data normalization for Close and SMA50 columns
attributes = ['Close','SMA50']
for attribute in attributes:
    max = data_2500[attribute].max()
    min = data_2500[attribute].min()
    data_2500[attribute] = (data_2500[attribute] - min) / (max - min)

"""
seria = pandas.cut(pandas.Series(numpy.array(data_2500['Bulls'])),2,labels=['Lower','Upper'])
data_2500['Bulls'].hist()
"""

data_2500['Bulls'].hist() # histogram before discretization

# histogram after discretization
labels = ['Up','Down']
series = pandas.Series(numpy.array(data_2500['Bulls']))
result = pandas.cut(series,2,labels = labels)  
result.hist()


data_2500['Close'].hist() # histogram before discretization

# histogram after discretization
labelsClose = ['0,0 - 0,25','0,26 - 0,5','0,51 - 0,75','0,76 - 1,0']
seriesClose = pandas.Series(numpy.array(data_2500['Close']))
resultClose = pandas.cut(seriesClose,4,labels = labelsClose)
resultClose.hist()

# Drawing a pie chart
data_2500['Decision'].value_counts().plot.pie()

# Drawing a line graph

data_2500['Close'].plot()


print(f"Empty from the Close column: {emptyCLOSE}")
print(f"Greater Correlation for: {greater_correlation}")
print(data_2500)
