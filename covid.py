# mypy: ignore-errors
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import pandas as pd

url = "https://raw.githubusercontent.com/datasets/covid-19/main/data/countries-aggregated.csv"

print("Loading dataset...")
df = pd.read_csv(url)

print("\nFirst rows:")
print(df.head())

print("\nChecking missing values:")
print(df.isnull().sum())

df = df.dropna()

country = "Germany"
df_country = df[df["Country"] == country].reset_index(drop=True)

print(f"\nData for {country}:")
print(df_country.head())

df_country["Active"] = (
    df_country["Confirmed"] - df_country["Recovered"] - df_country["Deaths"]
)

df_country["DailyConfirmed"] = df_country["Confirmed"].diff().fillna(0)
df_country["DailyDeaths"] = df_country["Deaths"].diff().fillna(0)

print("\nSummary statistics:")
print(df_country.describe())

df_country.to_csv("covid_cleaned.csv", index=False)
print("\nSaved cleaned dataset to covid_cleaned.csv")

df = pd.read_csv("covid_cleaned.csv")

df["Date"] = pd.to_datetime(df["Date"], format="%Y-%m-%d")

df["MA7_Cases"] = df["DailyConfirmed"].rolling(window=7).mean()
df["MA7_Deaths"] = df["DailyDeaths"].rolling(window=7).mean()

plt.figure(figsize=(10, 5))
plt.plot(df["Date"], df["DailyConfirmed"], label="Daily Cases", alpha=0.4)
plt.plot(df["Date"], df["MA7_Cases"], label="7-Day MA", linewidth=2)

plt.title("Daily New COVID-19 in Germany")
plt.xlabel("Date")
plt.ylabel("Cases")
plt.xticks(rotation=45)

plt.gca().xaxis.set_major_locator(mdates.AutoDateLocator(minticks=5, maxticks=10))
plt.gca().xaxis.set_major_formatter(mdates.DateFormatter("%Y-%m"))

plt.legend()
plt.tight_layout()
plt.savefig("daily_cases.png", dpi=150)
plt.show()

plt.figure(figsize=(10, 5))
plt.plot(df["Date"], df["Active"], label="Active Cases", linewidth=2)
plt.plot(df["Date"], df["Recovered"], label="Recovered", linewidth=2)

plt.title("Active vs Recovered Cases")
plt.xlabel("Date")
plt.ylabel("People")
plt.xticks(rotation=45)

plt.gca().xaxis.set_major_locator(mdates.AutoDateLocator(minticks=5, maxticks=10))
plt.gca().xaxis.set_major_formatter(mdates.DateFormatter("%Y-%m"))

plt.legend()
plt.tight_layout()
plt.savefig("active_vs_recovered.png", dpi=150)
plt.show()

summary = {
    "Max Daily Cases": df["DailyConfirmed"].max(),
    "Max Daily Deaths": df["DailyDeaths"].max(),
    "Total Confirmed": df["Confirmed"].iloc[-1],
    "Total Deaths": df["Deaths"].iloc[-1],
    "Total Recovered": df["Recovered"].iloc[-1],
}

print("\n=== COVID-19 Summary Report ===")
for k, v in summary.items():
    print(f"{k}: {v}")

pd.DataFrame([summary]).to_csv("summary_report.csv", index=False)
print("\nSaved 'summary_report.csv'")
