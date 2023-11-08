# Databasics-Vectorized Operations

A brief exploration of vectorized and non-vectorized implementations of database operations. We will time our operations and replicate the same operations using different methods to see how processing speed improves.

## Our goals in this project are:

1. Establish a synthetic database
2. Perform some basic operations using a non-vectorized solution
3. Explore other methods and iteratively improve processing time while measuring results

As always, lets install our packages.

    import pandas as pd
    import numpy as np
    import time
    import random as rand

### Establish a Synthetic Database

Now we create a synthetic database to perform our basic operations. Three columns with integer and string data should do fine. We use 50000 to highlight differences in processing time.

    column = rand.choices(['Dropout' if i == 13 or i ==21 else i for i in range(0,100)],k=50000)
    othercolumn = rand.choices([i for i in range(20,80)], k=50000)
    colors = rand.choices(['Red', 'Blue', 'Green', 'Yellow', 'Violet'], k=50000)
    df_og = pd.Dataframe({'column':column, 'othercolumn':othercolumn, 'color':colors})
