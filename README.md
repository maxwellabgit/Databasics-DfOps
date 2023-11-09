# Databasics-Vectorized Operations

A brief exploration of vectorized and non-vectorized implementations of database operations. We will time the same operation using different methods to see how processing speed improves. Our goal is to add a new column to the dataframe using the most efficient method.

## Our goals in this project are:

1. Establish an example database
2. Perform some basic operations using a non-vectorized solution
3. Explore other methods and iteratively improve processing time while measuring results

As always, lets install our packages.

    import pandas as pd
    import numpy as np
    import time
    import random as rand

### Establish an Example Database

Now we create an example database to perform our basic operations. Three columns with integer and string data should do fine. We use 50000 rows to highlight differences in processing time.

    column = rand.choices(['Dropout' if i == 13 or i ==21 else i for i in range(0,100)],k=50000)
    othercolumn = rand.choices([i for i in range(20,80)], k=50000)
    colors = rand.choices(['Red', 'Blue', 'Green', 'Yellow', 'Violet'], k=50000)
    df_og = pd.Dataframe({'column':column, 'othercolumn':othercolumn, 'color':colors})

![an image of the databse, gets the mind going](https://github.com/maxwellabgit/Databasics-VectorizedOps/blob/main/githubprofilebuildlast.png)

### Perform Some Basic Operations

Our next objective is to add a new column with some basic calculations. Let's choose three conditions: 
- The first column's value is not equal to 'Dropout' AND the second column's value is greater than or equal to 50, then the corresponding value is 100
- The first column's value is not equal to 'Dropout' AND the second column's value is less than 50, then the corresponding value is 0
- In any other case, the corresponding value is equal to the second column's

Ensure our dataframe is the same as the original for quality purposes, and start a timer.

    df = df_og
    start = time.time()

Apply our three conditions using a while loop to create a new column.

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

End the timer and print the result.

    t = time.time() - start
    print('while loop solution run time: ' + str(t))

While loop run time is .677 seconds with 50000 rows. Scaling is not an option.

![while loop run time...](https://github.com/maxwellabgit/Databasics-VectorizedOps/blob/main/github112.png)

A while loop iteratively applies the inner operations one item at a time, meaning as the database size increases the processing time will increase linearly O(N). If we need to increase the complexity of our operations this method will fail quickly.

### Explore Other Methods and Iteratively Improve

Our processing speed would increase greatly if we could run the application of these three conditions on each row __in parallel__. Let's take the logic from our while loop and define a new function called makenewcol(col1, col2).

    def makenewcol(col1, col2):
      if col1 != 'Dropout' and col2 >= 50:
        return 100
      elif col1 != 'Dropout' and col2 < 50:
        return 0
      else:
        return col2

Now, we can apply our new function to each row at once using *__.apply lambda__*. 

    df['newcolumn'] = df.apply(lambda x: makenewcol(x['column'], x['othercolumn']), axis=1)

We ensure we are starting with the same dataframe and we use the time module to measure processing time.

    df = df_og
    start = time.time()
    [...]
    t2 = time.time() - start
    print('apply lambda solution run time: ' + str(t2))
    print('increase in speed from while loops: ' + str(int((t1 - t2)/t*100)) + '%')

The same logic defined within a function and applied with *__.apply__* improves processing time by 48%.

![.apply(lambda x: ) runtime...](https://github.com/maxwellabgit/Databasics-VectorizedOps/blob/main/github111.png)

### __We can stil do better!__

A lot of people stop at apply lambda after the first iteration of performance improvement. In reality, there is another faster tool we can use called *__numpy where__*. *__.apply__* is a pandas function writted in Python, but *__numpy where__* is written in C and can perform vectorized operations faster than Python. This operation requires two function calls because *__numpy where__* only takes a single logical statement.

    df['newcolumn'] = np.where((df['column']!='Dropout') & (df['othercolumn']>50), 100, df['othercolumn'])
    df['newcolumn'] = np.where((df['column']!='Dropout') & (df['othercolumn']<=50), 0, df['othercolumn'])

Again, we ensure we are starting with the same dataframe and we use the time module to measure processing time.

    df = df_og
    start = time.time()
    [...]
    t3 = time.time() - start
    print('numpy where solution run time: ' + str(t3))
    print('increase in speed from apply lambda: ' + str(int((t2 - t3)/t*100)) + '%')

After an increase in performance by about 50%, *__numpy where__* beats *__.apply__* by another 40% using the same logic and data.

![*__np.where__* run time](https://github.com/maxwellabgit/Databasics-VectorizedOps/blob/main/Screenshot%202023-11-08%20195301.png)

A cleaner approach that I much prefer is to use a module called *__numpy select__*. This allows us to run many conditions in the same way as an 'if', 'elif', 'else' block, so we aren't calling the same function twice.

    conditions = [
      (df['column'] != 'Dropout') & (df['othercolumn'] > 50),
      (df['column'] != 'Dropout') & (df['othercolumn'] <= 50)
    ]
    options = [
      100,
      0
    ]
    df['newcolumn'] = np.select(conditions, options, df['othercolumn'])

> [!NOTE]
> the order of the statements in the 'conditions' and 'options' lists matters just like a normal 'if', 'elif', 'else' block.

Again, we ensure we are starting with the same dataframe and we use the time module to measure processing time.

    df = df_og
    start = time.time()
    [...]
    t4 = time.time() - start
    print('numpy select run time: ' + str(t4))

###In most cases, *__numpy select__* and *__numpy where__* have comparable runtimes, but numpy select is at least more readable than a dozen numpy where statements.

![*__np.select__* run time](https://github.com/maxwellabgit/Databasics-VectorizedOps/blob/main/Screenshot%202023-11-08%20195345.png)

### Summary

While loops should be avoided at all costs unless other solutions do not exist. A common alternative, *__.apply lambda__*, is a fantastic tool that dramatically increases processing speed. However, many programmers stop here when they could instead use *__numpy where__* or *__numpy select__* which are much more efficient and just as intuitive to use.

