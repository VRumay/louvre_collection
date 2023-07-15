import pandas as pd
import numpy as np 

df = pd.read_excel(r"C:\Users\lafon\OneDrive\Documents\Python lessons\Louvre\catalogue.xlsx")

arrays = np.array_split(df, 100)
counter = 0
for array in arrays:
    counter += 1
    dftemp = pd.DataFrame(array)
    dftemp.to_excel(fr"C:\Users\lafon\OneDrive\Documents\Python lessons\Louvre\catalogues\catalogue-{counter}.xlsx", index=False)

# Hello

