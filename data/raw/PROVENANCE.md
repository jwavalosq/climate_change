# Data provenance

Every file in data/raw, where it came from, and what it covers. No key or login was used for any download. All downloads were made on November 2 to 3, 2026, local time in New York, and the files in this folder are the snapshot used for every number in this project.

## Files from the original repo

Original repo: github.com/jwavalosq/climate_change

Existing files in that repo, preserved in the source repo and not deleted or overwritten by this local build:

- data/GLB.Ts+dSST.csv, NASA GISTEMP global temperature, the file this project builds on.
- code/temperature_index_plot.R, the original R plot script.
- figures/temperature_index_plot.png, the original R plot output.
- README stub.

This local build fetched the first file again from its raw URL, so the numbers can be checked without touching the source repo. The R script was not rerun, because this build uses Python. Its output is superseded by the new charts, but the original files remain untouched in the source repo.

## 1. Global temperature, repo file

- File: GLB.Ts+dSST.csv
- URL: https://raw.githubusercontent.com/jwavalosq/climate_change/main/data/GLB.Ts+dSST.csv
- Source: NASA Goddard Institute for Space Studies, GISTEMP, land ocean global means.
- Coverage: 1880 to 2023, monthly and annual values. The J-D column is the January to December annual mean anomaly.
- Baseline: 1951 to 1980. An anomaly is the difference from that baseline average, in degrees Celsius.
- Note: values marked *** in the raw file mean missing. The cleaning script turns them into empty values.

## 2. Zonal temperature means

- File: ZonAnn.Ts+dSST.csv
- URL: https://data.giss.nasa.gov/gistemp/tabledata_v4/ZonAnn.Ts+dSST.csv
- Source: NASA GISTEMP, zonal annual means, same baseline as above.
- Coverage: 1880 to 2025 in the downloaded file.
- Use in this project: hemispheres and latitude bands. For comparisons with the repo global file, years to 2023 are used. The 2024 global value is 1.28 degrees and the 2025 global value is 1.18 degrees, reported separately and never mixed into a repo file decade mean.

## 3. Carbon dioxide, monthly means

- File: co2_mm_mlo.txt
- URL: https://gml.noaa.gov/webdata/ccgg/trends/co2/co2_mm_mlo.txt
- Source: NOAA Global Monitoring Laboratory, Mauna Loa, Hawaii.
- Coverage: monthly from 1958 to September 2026 in the downloaded file. The project uses annual means for the main analysis, and the monthly file is kept for reference.

## 4. Carbon dioxide, annual means

- File: co2_annmean_mlo.txt
- URL: https://gml.noaa.gov/webdata/ccgg/trends/co2/co2_annmean_mlo.txt
- Source: NOAA Global Monitoring Laboratory, Mauna Loa.
- Coverage: annual means, 1959 to 2025 in the downloaded file. The 1959 value is 315.98 ppm. The 2025 value is 427.35 ppm.
- Unit: ppm means parts per million.

## 5. Billion-dollar disasters, event level

- File: events-US.csv
- URL: https://www.ncei.noaa.gov/access/billions/events-US.csv
- Source: NOAA National Centers for Environmental Information (NCEI), Billion-Dollar Weather and Climate Disasters, United States.
- Coverage: 1980 to 2024, 403 events.
- Costs: the file states costs in millions of dollars. The CPI adjusted column is used for totals in this project, and the processed file adds a billions column. CPI means Consumer Price Index, the inflation adjustment.
- Status note, important: NOAA stopped updating this product in 2025. The 1980 to 2024 archive remains the source used here. Climate Central now continues a similar list, but its post 2024 events are not included, so the years stay comparable. Do not extend the series with a different source without labelling the break.

## 6. Billion-dollar disasters, time series

- File: time-series-US.csv
- URL: https://www.ncei.noaa.gov/access/billions/time-series-US.csv
- Source: NOAA NCEI, same product as file 5.
- Coverage: one row per year, 1980 to 2024, with counts and costs by disaster type.
- Note: this file states costs in billions of dollars, unlike the events file, which states millions. The cleaning script does not mix the two units. The time series file was downloaded for cross checking, and the event file is the primary source for the totals in this project, because it lets the project count and sum events directly.

## Attribution rule used throughout

Official figures are labelled with their agency: NASA for temperature, NOAA for CO2 and disasters. Independent figures are not used for headline numbers in this project. Where a figure is disputed between sources, for example insurer cost estimates versus NOAA cost estimates, this project uses NOAA and labels it as NOAA, so a reader can compare with the other source.

## How to refresh

Run: python3 scripts/download_data.py

Then run: python3 scripts/process_data.py

A refresh will change the numbers if the sources update. Re-run the notebooks after any refresh, and update BUILD_REPORT.md with the new coverage dates.
