"""Clean the raw downloads into tidy processed CSV files.

Run from the project root: python3 scripts/process_data.py
Inputs: data/raw/
Outputs: data/processed/

Notes on cleaning, in plain words:
- GISTEMP uses *** for a missing value. Those cells become empty.
- The repo global file ends in 2023. The NASA zonal file runs to 2025.
  For decade tables that mix the two, only years present in both are used,
  and later zonal years are shown separately, never silently merged.
- Disaster costs in events-US.csv are in millions of dollars, CPI adjusted.
  The processed files add a billions column so the units are clear.
- Disaster years come from the Begin Date, first four digits.
"""
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "data" / "raw"
OUT = ROOT / "data" / "processed"
OUT.mkdir(parents=True, exist_ok=True)

# 1. Global temperature, repo file, 1880 to 2023
glob = pd.read_csv(RAW / "GLB.Ts+dSST.csv", skiprows=1)
glob["J-D"] = pd.to_numeric(glob["J-D"], errors="coerce")
for col in ["DJF", "MAM", "JJA", "SON"]:
    glob[col] = pd.to_numeric(glob[col], errors="coerce")
global_annual = glob[["Year", "J-D", "DJF", "MAM", "JJA", "SON"]].copy()
global_annual.columns = ["year", "annual_anomaly_c", "winter_djf_c", "spring_mam_c", "summer_jja_c", "autumn_son_c"]
global_annual = global_annual.dropna(subset=["annual_anomaly_c"])
global_annual.to_csv(OUT / "global_annual.csv", index=False)

# Decade means, using complete decades plus a labelled partial 2020s group.
# The 2020s row in this file covers 2020 to 2023 only, and is labelled as such.
g = global_annual.copy()
g["decade_label"] = (g["year"] // 10 * 10).astype(str) + "s"
g.loc[g["year"] >= 2020, "decade_label"] = "2020s (2020-2023 only)"
decade = g.groupby("decade_label", sort=True)["annual_anomaly_c"].agg(["mean", "count"]).reset_index()
decade.columns = ["decade", "mean_anomaly_c", "years_included"]
decade["change_from_previous_decade_c"] = decade["mean_anomaly_c"].diff()
decade.to_csv(OUT / "decade_means.csv", index=False)

# 2. Zonal means, NASA current file, 1880 to 2025
zon = pd.read_csv(RAW / "ZonAnn.Ts+dSST.csv")
zon = zon.rename(columns={"Year": "year", "Glob": "global_c", "NHem": "northern_hemisphere_c",
                          "SHem": "southern_hemisphere_c", "24N-90N": "north_24_to_90_c",
                          "24S-24N": "tropics_24s_to_24n_c", "90S-24S": "south_90_to_24_c",
                          "64N-90N": "arctic_64_to_90_c"})
keep = ["year", "global_c", "northern_hemisphere_c", "southern_hemisphere_c",
        "north_24_to_90_c", "tropics_24s_to_24n_c", "south_90_to_24_c", "arctic_64_to_90_c"]
zon[keep].to_csv(OUT / "zonal_annual.csv", index=False)

# 3. CO2, NOAA Mauna Loa annual means
co2 = pd.read_csv(RAW / "co2_annmean_mlo.txt", comment="#", sep=r"\s+",
                  header=None, names=["year", "mean_ppm", "uncertainty_ppm"])
co2 = co2[co2["year"] >= 1959].copy()
co2.to_csv(OUT / "co2_annual.csv", index=False)

# 4. CO2 joined to temperature, annual, 1959 to 2023 (the overlap)
joined = pd.merge(global_annual[["year", "annual_anomaly_c"]], co2, on="year", how="inner")
joined.to_csv(OUT / "co2_temp_annual.csv", index=False)

# 5. Billion-dollar disasters, event level
ev = pd.read_csv(RAW / "events-US.csv", skiprows=2)
ev["year"] = ev["Begin Date"].astype(str).str[:4].astype(int)
ev["cost_cpi_adjusted_billion_usd"] = ev["CPI-Adjusted Cost"] / 1000.0
ev["cost_unadjusted_billion_usd"] = ev["Unadjusted Cost"] / 1000.0
events = ev[["Name", "Disaster", "Begin Date", "End Date", "year",
             "cost_cpi_adjusted_billion_usd", "cost_unadjusted_billion_usd", "Deaths"]].copy()
events.columns = ["name", "disaster_type", "begin_date", "end_date", "year",
                  "cost_cpi_adjusted_billion_usd", "cost_unadjusted_billion_usd", "deaths"]
events.to_csv(OUT / "disasters_events.csv", index=False)

# By year
by_year = events.groupby("year").agg(
    event_count=("name", "count"),
    total_cost_cpi_billion_usd=("cost_cpi_adjusted_billion_usd", "sum"),
    total_deaths=("deaths", "sum")).reset_index()
by_year["mean_cost_per_event_billion_usd"] = by_year["total_cost_cpi_billion_usd"] / by_year["event_count"]
by_year.to_csv(OUT / "disasters_by_year.csv", index=False)

# By decade and type
events["decade"] = (events["year"] // 10 * 10).astype(str) + "s"
events.loc[events["year"] >= 2020, "decade"] = "2020s (2020-2024)"
by_decade_type = events.groupby(["decade", "disaster_type"]).agg(
    event_count=("name", "count"),
    total_cost_cpi_billion_usd=("cost_cpi_adjusted_billion_usd", "sum"),
    total_deaths=("deaths", "sum")).reset_index()
by_decade_type.to_csv(OUT / "disasters_by_decade_type.csv", index=False)

# By decade, all types (the original cost versus frequency table)
by_decade = events.groupby("decade").agg(
    event_count=("name", "count"),
    total_cost_cpi_billion_usd=("cost_cpi_adjusted_billion_usd", "sum"),
    total_deaths=("deaths", "sum")).reset_index()
by_decade["mean_cost_per_event_billion_usd"] = by_decade["total_cost_cpi_billion_usd"] / by_decade["event_count"]
order = ["1980s", "1990s", "2000s", "2010s", "2020s (2020-2024)"]
by_decade["decade"] = pd.Categorical(by_decade["decade"], categories=order, ordered=True)
by_decade = by_decade.sort_values("decade")
by_decade.to_csv(OUT / "disasters_by_decade.csv", index=False)

print(f"global_annual rows: {len(global_annual)}")
print(f"zonal rows: {len(zon)}")
print(f"co2 rows: {len(co2)}")
print(f"joined rows: {len(joined)}")
print(f"disaster events: {len(events)}")
print("Done.")
