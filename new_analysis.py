import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.dates import DateFormatter
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


def plot_top_10_cases():
    fig, ax = plt.subplots(figsize=(19.20, 10.80))
    ax.barh(
            df_conf_10["Country/Region"].values,
            df_conf_10[last_date].values,
            align="center")
    for index, value in enumerate(df_conf_10[last_date].values):
        plt.text(value, index, str(value))
    ax.set(
        xlabel="Cases",
        ylabel="Countries",
        title="Covid-19 cases top 10 countries"
    )

    plt.savefig("images/1_Covid-19_top_10_countries.png", dpi=200)
    plt.show()


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
    fig, ax = plt.subplots(figsize=(19.20, 10.80))
    ax.set_yscale('log')

    for country in countries_to_plot:
        ax.plot(df_t['Date'], df_t[country], label=country)
        ax.set(xlabel="Date",
               ylabel=df_type,
               title="Covid-19 data "+ df_type)
        ax.legend()
        date_form = DateFormatter("%d-%m")
        ax.xaxis.set_major_formatter(date_form)

        plt.show()
        plt.savefig("images/country_comparison_"+df_type+".png")


do_plot = False
list_countries = ["Pakistan", "China", "US", "France", "United Kingdom"]
if do_plot:
    plot_comparison(list_countries, "death")


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
                         dtype: "No of daily cases"},
                 title="Daily "+dtype+" in  "+country)
    fig.show()
    fig.write_image("images/Daily_" + dtype + "_" + country + ".png")


daily_cases_country("US", "death")
daily_cases_country("Pakistan", "death")
