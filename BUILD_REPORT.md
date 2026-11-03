# BUILD_REPORT

Project: Climate in Charts: Warming Trends and Extreme Events
Local folder: this folder only. Nothing was published, pushed, posted, or signed into.

## Exactly which files were used

Raw inputs, all in data/raw, all downloaded with no key or login:

- GLB.Ts+dSST.csv, from https://raw.githubusercontent.com/jwavalosq/climate_change/main/data/GLB.Ts+dSST.csv, NASA GISTEMP, 1880 to 2023, 144 annual rows after cleaning.
- ZonAnn.Ts+dSST.csv, from https://data.giss.nasa.gov/gistemp/tabledata_v4/ZonAnn.Ts+dSST.csv, NASA GISTEMP zonal means, 1880 to 2025, 146 rows.
- co2_mm_mlo.txt, from https://gml.noaa.gov/webdata/ccgg/trends/co2/co2_mm_mlo.txt, NOAA Mauna Loa monthly, to September 2026 in the download, kept for reference.
- co2_annmean_mlo.txt, from https://gml.noaa.gov/webdata/ccgg/trends/co2/co2_annmean_mlo.txt, NOAA Mauna Loa annual means, 1959 to 2025, 67 rows.
- events-US.csv, from https://www.ncei.noaa.gov/access/billions/events-US.csv, NOAA NCEI billion-dollar disasters, 1980 to 2024, 403 events.
- time-series-US.csv, from https://www.ncei.noaa.gov/access/billions/time-series-US.csv, NOAA NCEI time series, downloaded for cross checking only. The event file is the primary source for disaster totals, because it allows direct counting and summing.

Original repo files built on, not deleted or overwritten, in github.com/jwavalosq/climate_change:

- data/GLB.Ts+dSST.csv
- code/temperature_index_plot.R
- figures/temperature_index_plot.png
- README stub

The R script was not rerun. This build uses Python, and the new charts supersede the original R plot output in this local folder only. The source repo files were not touched.

Processed outputs, made by scripts/process_data.py, all in data/processed:

- global_annual.csv, 144 rows
- decade_means.csv
- zonal_annual.csv, 146 rows
- co2_annual.csv, 67 rows
- co2_temp_annual.csv, 65 rows, 1959 to 2023 overlap
- disasters_events.csv, 403 rows
- disasters_by_year.csv, 45 rows, 1980 to 2024
- disasters_by_decade.csv
- disasters_by_decade_type.csv

## What ran

In order, from the project root:

1. python3 scripts/download_data.py, saved all six raw files.
2. python3 scripts/process_data.py, made all processed CSV files.
3. python3 scripts/make_charts.py, made 15 charts in charts/.
4. python3 scripts/build_notebooks.py, made 6 notebooks in notebooks/.
5. jupyter nbconvert, executed each notebook in place, one by one, with a 180 second timeout per notebook.
6. Final verification: a script read every notebook JSON file, counted executed code cells, and checked for error outputs. Result: 6 notebooks, 37 code cells in total, zero error outputs.
7. Charts were copied to docs/charts/, and docs/index.html was built to show them.

Notebook counts, code cells executed:

- 01_global_temperature_decades.ipynb, 6 code cells, 0 errors
- 02_co2_and_temperature.ipynb, 7 code cells, 0 errors
- 03_extreme_events_frequency_cost.ipynb, 7 code cells, 0 errors
- 04_regional_patterns.ipynb, 7 code cells, 0 errors
- 05_original_metrics.ipynb, 6 code cells, 0 errors
- 06_what_data_shows_and_limits.ipynb, 4 code cells, 0 errors

Chart count: 15 PNG files in charts/, and the same 15 copied to docs/charts/.

Chart list:

1. 01_global_annual_anomaly.png
2. 02_decade_means.png
3. 03_decade_change_pace.png
4. 04_rolling_10yr_mean.png
5. 05_co2_annual.png
6. 06_co2_and_temperature_dual.png
7. 07_co2_vs_temperature_scatter.png
8. 08_disasters_count_by_year.png
9. 09_disasters_cost_by_decade.png
10. 10_disasters_by_type_count.png
11. 11_disasters_by_type_cost.png
12. 12_cost_per_event_by_decade.png
13. 13_hemisphere_comparison.png
14. 14_arctic_vs_global.png
15. 15_seasonal_comparison.png

## What failed or was approximated

- First notebook execution pass: notebooks 1 to 4 hit a transient IPython and matplotlib backend import error, mentioning backend2gui, while notebooks 5 and 6 succeeded. No notebook content was changed. A second full execution pass succeeded for all six notebooks, and the final verification above shows zero errors. The cause looks like a first run kernel startup race between the system matplotlib and the user installed IPython, not a code error in the notebooks. This is recorded here so a future rerun that hits the same transient error is not mistaken for a data error. Rerun the single notebook if it happens.
- No data values were approximated. Every headline number is computed from the processed tables in the notebooks. Rounding is to two or three decimals in the text, and full values are in the CSV files.
- Disaster costs use NOAA point estimates. NOAA also publishes confidence bounds in its time series file. Those bounds were not charted, and the report says so in notebook 6. Using point estimates only is a simplification, not a correction to the data.
- The 2020s decade rows are partial by design: temperature 2020 to 2023 in the repo file, disasters 2020 to 2024 in the archive. They are labelled partial everywhere, and they are never presented as full decades.
- The zonal file runs to 2025 while the repo global file runs to 2023. The two are not mixed in any decade mean. Zonal 2024 and 2025 values are reported separately.

## What was cut and why

- Maps: cut. No gridded map dataset was used, so no map was drawn. Regional patterns are shown with hemisphere and latitude band lines instead. Drawing a map from band averages would have been fake precision.
- Post 2024 disaster events: cut. NOAA stopped updating the product in 2025, and Climate Central now continues a similar list with a different threshold history. Adding its events would have broken comparability, so the series stops at 2024 and the break is labelled.
- A full causal attribution model: cut. That needs physics, many datasets, and models outside this project. The CO2 chapter therefore states correlation plainly, 0.964 for 1959 to 2023, and does not claim sole cause.
- A global disaster trend: cut. The disaster file covers the United States only. No global disaster claim is made.
- Statistical significance tests: cut. No p values or formal tests are presented, because the project is a descriptive, beginner friendly story, and inventing a test on aggregated series would have added false rigour. Trends are reported as fitted slopes, labelled as such.
- The original R plot: not rerun, for the reason given above. It is not a cut from the source repo, which still holds it.
- Climate Central continuation data, insurer cost estimates, and other independent disaster cost figures: not used for headline numbers. They are mentioned only as a comparison point in notebook 6, so the NOAA attribution stays clean.

## Original metrics added

1. Decade over decade warming pace: each decade mean minus the previous decade mean, plus linear trends per decade for 1880 to 2023, 1970 to 2023, 1980 to 2023, and 2000 to 2023.
2. Disaster cost versus frequency: total CPI adjusted cost divided by event count, by decade, showing that the average per event bounces while the count climbs.

## Things that could not be verified

- Whether the repo global file in the source repo has been updated since the download. The downloaded snapshot ends in 2023. If the source file updates, re-run scripts/download_data.py and update this report.
- Whether Climate Central post 2024 events match NOAA methods closely enough to extend the series. That comparison was not attempted, and no such extension is claimed.
- Insurer versus NOAA cost differences for individual events. Those are noted as a known source of dispute, but no insurer figures were verified or used here.

## Rebuild

```
pip install -r requirements.txt
python3 scripts/download_data.py
python3 scripts/process_data.py
python3 scripts/make_charts.py
python3 scripts/build_notebooks.py
jupyter nbconvert --to notebook --execute --inplace notebooks/*.ipynb
cp charts/*.png docs/charts/
```

Or: bash scripts/rebuild_all.sh, then execute the notebooks and copy the charts as above.
