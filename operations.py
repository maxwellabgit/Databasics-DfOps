import pandas as pd
import numpy as np
import time
import random as rand


#Database setup
column = rand.choices(['Dropout' if i == 13 or i ==21 else i for i in range(0,100)],k=50000)
othercolumn = rand.choices([i for i in range(20,80)], k=50000)
colors = rand.choices(['Red', 'Blue', 'Green', 'Yellow', 'Violet'], k=50000)
df_og = pd.Dataframe({'column':column, 'othercolumn':othercolumn, 'color':colors})

#non-vectorized implementation:
df = df_og
start = time.time()
newcolumn = []
i = 0
while i < len(df):
  if df['column'][i] != 'Dropout' and df['othercolumn'][i] >= 50:
    newcolumn.append(100)
  elif df['column'][i] != 'Dropout' and df['othercolumn'][i] < 50:
    newcolumn.append(0)
  else:
    newcolumn.append(df['othercolumn'][i])
  i += 1
df = pd.DataFrame({'column':column, 'othercolumn':othercolumn, 'color':colors, 'newcolumn':newcolumn})

t = time.time() - start
print('while loop solution run time: ' + str(t))


#define the above code as a function and apply lambda, the good old
df = df_og
start = time.time()
def newcolumn(col1, col2):
  if col1 != 'Dropout' and col2 >= 50:
    return 100
  elif col1 != 'Dropout' and col2 < 50:
    return 0
  else:
    return col2
df['newcolumn'] = df.apply(lambda x: newcolumn(x['column'], x['othercolumn']), axis=1)

t2 = time.time() - start
print('apply lambda solution run time: ' + str(t2))
print('increase in speed from while loops: ' + str(int((t1 - t2)/t*100)) + '%')


#np.where, the lightning fast numpy version of apply. It only works with one logic statement though :(
df = df_og
start = time.time()
df['newcolumn'] = np.where((df['column']!='Dropout') & (df['othercolumn']>50), 100, df['othercolumn'])
df['newcolumn'] = np.where((df['column']!='Dropout') & (df['othercolumn']<=50), 0, df['newcolumn'])

t3 = time.time() - start
print('numpy where solution run time: ' + str(t3))
print('increase in speed from apply lambda: ' + str(int((t2 - t3)/t*100)) + '%')


#np.select, vectorized and works with multiple logic statements (one giant if, elif, else)
df = df_og
start = time.time()
conditions = [
  (df['column'] != 'Dropout') & (df['othercolumn'] > 50),
  (df['column'] != 'Dropout') & (df['othercolumn'] <= 50)
]
options = [
  100,
  0
]
df['newcolumn'] = np.select(conditions, options, df['othercolumn'])

t4 = time.time() - start
print('numpy select run time: ' + str(t4))



