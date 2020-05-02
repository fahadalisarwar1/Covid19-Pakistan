import pandas as pd
import matplotlib.pyplot as plt


df_pak = pd.read_csv("dataset/pakistan_ts.csv").drop("Unnamed: 0", axis=1)
plt.plot(df_pak['Pakistan'].values)
plt.show()
