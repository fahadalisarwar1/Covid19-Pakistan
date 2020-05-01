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
col_confirmed = ["Date", "Cases"]
df_pak_confirmed.columns = col_confirmed

df_pak_deaths = df_pak_deaths.T.reset_index()
col_deaths = ["Date", "Deaths"]
df_pak_deaths.columns = col_deaths

df_pak_recovered = df_pak_recovered.T.reset_index()
col_recovered = ["Date", "Recovered"]
df_pak_recovered.columns = col_recovered


print(df_pak_confirmed.shape)
print(df_pak_deaths.shape)
print(df_pak_recovered.shape)

# merging into a single data frame
df_pakistan = df_pak_confirmed
df_pakistan["Deaths"] = df_pak_deaths['Deaths']
df_pakistan["Recovered"] = df_pak_recovered['Recovered']
df_pakistan['ActiveCases'] = df_pakistan['Cases'] - (df_pakistan['Deaths']+df_pakistan['Recovered'])

df_pakistan['Date'] = pd.to_datetime(df_pakistan["Date"], infer_datetime_format=True)

df_world = df_confirmed[df_confirmed['Country/Region'] != "Pakistan"]


































































