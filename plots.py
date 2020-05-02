import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.dates import DateFormatter
import plotly.graph_objects as go
import os
import plotly.express as px
if not os.path.exists("images"):
    os.mkdir("images")

# loading data-sets
df_confirmed = pd.read_csv("dataset/time_series_covid19_confirmed_global.csv")
df_deaths = pd.read_csv("dataset/time_series_covid19_deaths_global.csv")
df_recovered = pd.read_csv("dataset/time_series_covid19_recovered_global.csv")

to_drop = ["Province/State", "Lat", "Long"]

df_confirmed = df_confirmed.drop(to_drop, axis=1)
df_deaths = df_deaths.drop(to_drop, axis=1)
df_recovered = df_recovered.drop(to_drop, axis=1)

df_confirmed = df_confirmed.groupby(["Country/Region"]).sum().reset_index()
df_deaths = df_deaths.groupby(["Country/Region"]).sum().reset_index()
df_recovered = df_recovered.groupby(["Country/Region"]).sum().reset_index()

# Sort columns based on highest number of cases
last_date = df_confirmed.columns[-1]
# since last day is a rolling sum of dates
df_confirmed_sorted = df_confirmed.sort_values(ascending=False, by=last_date)
df_deaths_sorted = df_deaths.sort_values(ascending=False, by=last_date)
df_recovered_sorted = df_recovered.sort_values(ascending=False, by=last_date)


# selecting 10 countries with highest cases
df_conf_10 = df_confirmed_sorted.head(10)
df_death_10 = df_deaths_sorted.head(10)
df_rec_10 = df_recovered_sorted.head(10)


def plot_top_10(df_type="case"):
    if df_type == "recover":
        df = df_rec_10
    elif df_type == "death":
        df = df_death_10
    else:
        df = df_conf_10

    fig = px.bar(data_frame=df,
           x=last_date,
           y="Country/Region",
           orientation="h")
    fig.show()
    fig.write_image("images/Top_10_"+df_type+".png")


# plot_top_10()
# plot_top_10("death")
# plot_top_10("recover")


def plot_comparison(countries_to_plot=[], df_type="cases"):
    if df_type == "cases":
        df_t = df_confirmed.T
    elif df_type == "death":
        df_t = df_deaths.T
    elif df_type == "recovered":
        df_t = df_recovered.T

    new_header = df_t.iloc[0]
    df_t = df_t[1:]
    df_t.columns = new_header
    df_t = df_t.reset_index()
    df_t.rename(columns={"index": "Date"}, inplace=True)
    df_t['Date'] = pd.to_datetime(df_t["Date"], infer_datetime_format=True)

    fig = go.Figure()
    name = ""
    for country in countries_to_plot:

        fig.add_trace(go.Scatter(
            x=df_t['Date'],
            y=df_t[country],
            name=country,
            connectgaps=True
        ))
        name += country + "_"
    fig.update_layout(xaxis_title="Date",
                      yaxis_title=df_type,
                      yaxis_type="log")
    fig.show()

    fig.write_image("images/comparison_"+name+df_type+".png")


countries = ["Pakistan", "US", "France", "Italy"]
# plot_comparison(countries)

# plot_comparison(countries, "death")


def daily_cases_country(country="Pakistan", dtype="cases"):
    if dtype == "cases":
        df = df_confirmed[df_confirmed["Country/Region"] == country]
    elif dtype == "death":
        df = df_deaths[df_deaths["Country/Region"] == country]
    else:
        df = df_recovered[df_recovered["Country/Region"] == country]
    df_selected = df.T.reset_index()
    new_header = df.iloc[0]
    df_selected = df_selected[1:]
    df.columns = new_header
    df_selected.columns = ["Date", dtype]
    df_selected[dtype] = df_selected[dtype].diff().fillna(0)
    df_selected["Date"] = pd.to_datetime(df_selected["Date"], infer_datetime_format=True)
    fig = px.bar(data_frame=df_selected,
                 x="Date",
                 y=dtype,
                 labels={"Date": "Date",
                         dtype: "No of daily "+dtype},
                 title="Daily "+dtype+" in  "+country)
    fig.show()
    fig.write_image("images/Daily_" + dtype + "_" + country + ".png")


daily_cases_country("Pakistan", "cases")
daily_cases_country("Pakistan", "death")
daily_cases_country("Pakistan", "recovered")
