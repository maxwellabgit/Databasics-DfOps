import pandas as pd
import numpy as np
import re
import time

#non-vectorized implementation:
newcolumn = []
i = 0
while i < len(df):
  if df['column'][i] != None & df['column'][i] > 50:
    y = 100
  else:
    y = df['othercolumn'][i]
  newcolumn.append(y)
  i += 1

#apply lambda, the good old 
df['newcolumn'] = df.apply(lambda x: 100 if x['column'] not None and x['column'] > 50 else x['othercolumn'])

#np.where, the lightning fast bretheren of apply that vectorizes an operation on a column but only works with one logic statement

df['newcolumn'] = np.where((df['column'] != None) & (df['column'] > 50), 100, df['othercolumn'])

#np.select, vectorized and works with multiple logic statements (one giant if, elif, else)

conditions = [
  (df['column'] != None) & (df['column'] > 50),
  (df['column'] != None) & (df['column'] == 50),
  (df['column'] != None) & (df['column'] < 50)
]
options = [
  100,
  50,
  0
]
df['newcolumn'] = np.select(conditions, options, df['othercolumn'])

#quick way to filter certain columns or the entire database

df['column'] = df[df['column'].str.contains("|".join(wordstokeep))]
df = df[df['othercolumn'] != df['newcolumn']]

