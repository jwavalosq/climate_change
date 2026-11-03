"""Make every chart in charts/ from the processed CSV files.

Run from the project root: python3 scripts/make_charts.py
Style: plain titles, labelled axes, a source line under each chart.
No map is drawn, because no gridded map dataset was used in this build.
"""
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
PROC = ROOT / "data" / "processed"
CH = ROOT / "charts"
CH.mkdir(parents=True, exist_ok=True)

plt.rcParams.update({"figure.dpi": 150, "axes.titlesize": 13, "axes.labelsize": 11,
                     "xtick.labelsize": 9, "ytick.labelsize": 9})

G = pd.read_csv(PROC / "global_annual.csv")
D = pd.read_csv(PROC / "decade_means.csv")
Z = pd.read_csv(PROC / "zonal_annual.csv")
C = pd.read_csv(PROC / "co2_annual.csv")
J = pd.read_csv(PROC / "co2_temp_annual.csv")
EV = pd.read_csv(PROC / "disasters_events.csv")
BY = pd.read_csv(PROC / "disasters_by_year.csv")
BD = pd.read_csv(PROC / "disasters_by_decade.csv")
BT = pd.read_csv(PROC / "disasters_by_decade_type.csv")


def save(fig, name, source):
    fig.text(0.01, 0.01, f"Source: {source}", fontsize=7, color="#555555")
    fig.tight_layout(rect=[0, 0.04, 1, 1])
    fig.savefig(CH / name, bbox_inches="tight")
    plt.close(fig)
    print(f"saved {name}")


SRC_TEMP = "NASA GISTEMP, repo file GLB.Ts+dSST.csv, 1880-2023"
SRC_ZON = "NASA GISTEMP zonal means, 1880-2025"
SRC_CO2 = "NOAA Global Monitoring Laboratory, Mauna Loa"
SRC_DIS = "NOAA NCEI, Billion-Dollar Disasters archive, 1980-2024, CPI adjusted"

# 1. Annual global anomaly
fig, ax = plt.subplots(figsize=(10, 5))
ax.plot(G["year"], G["annual_anomaly_c"], color="#1f77b4", linewidth=1)
ax.axhline(0, color="grey", linewidth=0.8)
ax.set_title("Global temperature anomaly, each year from 1880 to 2023")
ax.set_xlabel("Year")
ax.set_ylabel("Anomaly in degrees Celsius, versus 1951-1980")
save(fig, "01_global_annual_anomaly.png", SRC_TEMP)

# 2. Decade means
fig, ax = plt.subplots(figsize=(10, 5))
ax.bar(D["decade"], D["mean_anomaly_c"], color="#2ca02c")
ax.axhline(0, color="grey", linewidth=0.8)
ax.set_title("Average temperature anomaly by decade")
ax.set_xlabel("Decade (2020s covers 2020-2023 only)")
ax.set_ylabel("Mean anomaly in degrees Celsius")
plt.setp(ax.get_xticklabels(), rotation=30, ha="right")
save(fig, "02_decade_means.png", SRC_TEMP)

# 3. Decade change, the warming pace metric
d2 = D.dropna(subset=["change_from_previous_decade_c"])
fig, ax = plt.subplots(figsize=(10, 5))
ax.bar(d2["decade"], d2["change_from_previous_decade_c"], color="#d62728")
ax.axhline(0, color="grey", linewidth=0.8)
ax.set_title("How much the decade average moved, compared with the decade before")
ax.set_xlabel("Decade")
ax.set_ylabel("Change in degrees Celsius")
plt.setp(ax.get_xticklabels(), rotation=30, ha="right")
save(fig, "03_decade_change_pace.png", SRC_TEMP)

# 4. Rolling 10 year mean
g = G.copy()
g["rolling_10yr"] = g["annual_anomaly_c"].rolling(10).mean()
fig, ax = plt.subplots(figsize=(10, 5))
ax.plot(g["year"], g["annual_anomaly_c"], color="#bbbbbb", linewidth=0.8, label="Single year")
ax.plot(g["year"], g["rolling_10yr"], color="#1f77b4", linewidth=2, label="10 year rolling mean")
ax.axhline(0, color="grey", linewidth=0.8)
ax.legend()
ax.set_title("Single years jump around. The 10 year mean shows the trend.")
ax.set_xlabel("Year")
ax.set_ylabel("Anomaly in degrees Celsius")
save(fig, "04_rolling_10yr_mean.png", SRC_TEMP)

# 5. CO2 annual
fig, ax = plt.subplots(figsize=(10, 5))
ax.plot(C["year"], C["mean_ppm"], color="#9467bd", linewidth=2)
ax.set_title("Carbon dioxide at Mauna Loa, annual mean, 1959 to 2025")
ax.set_xlabel("Year")
ax.set_ylabel("Parts per million (ppm)")
save(fig, "05_co2_annual.png", SRC_CO2)

# 6. CO2 and temperature, two lines on separate scales
fig, ax1 = plt.subplots(figsize=(10, 5))
ax1.plot(J["year"], J["mean_ppm"], color="#9467bd", linewidth=2, label="CO2 (ppm)")
ax1.set_xlabel("Year")
ax1.set_ylabel("CO2 in ppm", color="#9467bd")
ax2 = ax1.twinx()
ax2.plot(J["year"], J["annual_anomaly_c"], color="#d62728", linewidth=1.5, label="Temperature anomaly")
ax2.set_ylabel("Temperature anomaly in degrees Celsius", color="#d62728")
ax1.set_title("CO2 and global temperature rose together, 1959 to 2023")
save(fig, "06_co2_and_temperature_dual.png", f"{SRC_CO2}; {SRC_TEMP}")

# 7. Scatter, CO2 versus temperature
fig, ax = plt.subplots(figsize=(8, 6))
ax.scatter(J["mean_ppm"], J["annual_anomaly_c"], s=20, color="#1f77b4")
ax.set_title("Each dot is one year: higher CO2, higher temperature anomaly")
ax.set_xlabel("CO2 in ppm, Mauna Loa annual mean")
ax.set_ylabel("Temperature anomaly in degrees Celsius")
save(fig, "07_co2_vs_temperature_scatter.png", f"{SRC_CO2}; {SRC_TEMP}")

# 8. Disaster count by year
fig, ax = plt.subplots(figsize=(10, 5))
ax.bar(BY["year"], BY["event_count"], color="#ff7f0e")
ax.set_title("Billion-dollar disasters in the United States, count by year, 1980 to 2024")
ax.set_xlabel("Year")
ax.set_ylabel("Number of events")
save(fig, "08_disasters_count_by_year.png", SRC_DIS)

# 9. Disaster cost by decade
fig, ax = plt.subplots(figsize=(10, 5))
ax.bar(BD["decade"], BD["total_cost_cpi_billion_usd"], color="#d62728")
ax.set_title("Total CPI adjusted cost of billion-dollar disasters, by decade")
ax.set_xlabel("Decade (2020s covers 2020-2024 only)")
ax.set_ylabel("Billion US dollars, CPI adjusted")
plt.setp(ax.get_xticklabels(), rotation=20, ha="right")
save(fig, "09_disasters_cost_by_decade.png", SRC_DIS)

# 10. Disaster count by type
by_type = EV.groupby("disaster_type").size().sort_values(ascending=False)
fig, ax = plt.subplots(figsize=(10, 5))
ax.bar(by_type.index, by_type.values, color="#2ca02c")
ax.set_title("Billion-dollar disasters by type, 1980 to 2024: count")
ax.set_xlabel("Disaster type")
ax.set_ylabel("Number of events")
plt.setp(ax.get_xticklabels(), rotation=20, ha="right")
save(fig, "10_disasters_by_type_count.png", SRC_DIS)

# 11. Disaster cost by type
by_cost = EV.groupby("disaster_type")["cost_cpi_adjusted_billion_usd"].sum().sort_values(ascending=False)
fig, ax = plt.subplots(figsize=(10, 5))
ax.bar(by_cost.index, by_cost.values, color="#9467bd")
ax.set_title("Billion-dollar disasters by type, 1980 to 2024: total cost")
ax.set_xlabel("Disaster type")
ax.set_ylabel("Billion US dollars, CPI adjusted")
plt.setp(ax.get_xticklabels(), rotation=20, ha="right")
save(fig, "11_disasters_by_type_cost.png", SRC_DIS)

# 12. Cost per event by decade, the original cost versus frequency check
fig, ax = plt.subplots(figsize=(10, 5))
ax.bar(BD["decade"], BD["mean_cost_per_event_billion_usd"], color="#17becf")
ax.set_title("Average cost per billion-dollar event, by decade")
ax.set_xlabel("Decade (2020s covers 2020-2024 only)")
ax.set_ylabel("Billion US dollars per event, CPI adjusted")
plt.setp(ax.get_xticklabels(), rotation=20, ha="right")
save(fig, "12_cost_per_event_by_decade.png", SRC_DIS)

# 13. Hemispheres
z23 = Z[Z["year"] <= 2023]
fig, ax = plt.subplots(figsize=(10, 5))
ax.plot(z23["year"], z23["northern_hemisphere_c"], label="Northern hemisphere", color="#d62728")
ax.plot(z23["year"], z23["southern_hemisphere_c"], label="Southern hemisphere", color="#1f77b4")
ax.plot(z23["year"], z23["global_c"], label="Global", color="black", linewidth=1)
ax.axhline(0, color="grey", linewidth=0.8)
ax.legend()
ax.set_title("Northern hemisphere warmed more than southern hemisphere, 1880 to 2023")
ax.set_xlabel("Year")
ax.set_ylabel("Anomaly in degrees Celsius")
save(fig, "13_hemisphere_comparison.png", SRC_ZON)

# 14. Arctic versus global
fig, ax = plt.subplots(figsize=(10, 5))
ax.plot(z23["year"], z23["arctic_64_to_90_c"], label="64N to 90N (far north)", color="#d62728")
ax.plot(z23["year"], z23["global_c"], label="Global", color="black", linewidth=1)
ax.axhline(0, color="grey", linewidth=0.8)
ax.legend()
ax.set_title("The far north warmed much faster than the globe as a whole")
ax.set_xlabel("Year")
ax.set_ylabel("Anomaly in degrees Celsius")
save(fig, "14_arctic_vs_global.png", SRC_ZON)

# 15. Seasonal means, recent versus early
early = G[G["year"].between(1880, 1889)][["winter_djf_c", "spring_mam_c", "summer_jja_c", "autumn_son_c"]].mean()
recent = G[G["year"].between(2014, 2023)][["winter_djf_c", "spring_mam_c", "summer_jja_c", "autumn_son_c"]].mean()
labels = ["Winter (DJF)", "Spring (MAM)", "Summer (JJA)", "Autumn (SON)"]
fig, ax = plt.subplots(figsize=(10, 5))
x = range(len(labels))
ax.bar([i - 0.2 for i in x], early.values, width=0.4, label="1880-1889 mean", color="#bbbbbb")
ax.bar([i + 0.2 for i in x], recent.values, width=0.4, label="2014-2023 mean", color="#d62728")
ax.axhline(0, color="grey", linewidth=0.8)
ax.set_xticks(list(x))
ax.set_xticklabels(labels)
ax.legend()
ax.set_title("Every season is warmer in 2014-2023 than in 1880-1889")
ax.set_ylabel("Anomaly in degrees Celsius")
save(fig, "15_seasonal_comparison.png", SRC_TEMP)

print("All charts done.")
