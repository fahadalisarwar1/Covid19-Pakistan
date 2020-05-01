import pandas as pd
import matplotlib.pyplot as plt

# loading data-sets
df_confirmed = pd.read_csv("dataset/time_series_covid19_confirmed_global.csv")
df_deaths = pd.read_csv("dataset/time_series_covid19_deaths_global.csv")
df_recovered = pd.read_csv("dataset/time_series_covid19_recovered_global.csv")


# Data exploration
df_confirmed.head()
df_deaths.head()
df_recovered.head()

print(df_confirmed.shape)
print(df_deaths.shape)
print(df_recovered.shape)


# I'm mostly interested in Pakistan's  data so I'll focus on that.
df_pak_confirmed = df_confirmed[df_confirmed["Country/Region"] == "Pakistan"]
df_pak_deaths = df_deaths[df_deaths["Country/Region"] == "Pakistan"]
df_pak_recovered = df_recovered[df_recovered["Country/Region"] == "Pakistan"]


# Let's drop Latitude, Longitude and State as they don't provide any useful information
df_pak_confirmed = df_pak_confirmed.drop(['Country/Region','Province/State', 'Lat', "Long"], axis=1)
df_pak_deaths = df_pak_deaths.drop(['Country/Region', 'Province/State', 'Lat', "Long"], axis=1)
df_pak_recovered = df_pak_recovered.drop(['Country/Region', 'Province/State', 'Lat', "Long"], axis=1)


# Transpose for better visualization
df_pak_confirmed = df_pak_confirmed.T.reset_index()
df_pak_confirmed = df_pak_confirmed.rename(columns={"index": "Date", 177: "Cases"})





