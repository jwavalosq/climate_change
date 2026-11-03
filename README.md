# Climate in Charts: Warming Trends and Extreme Events

A beginner friendly story, told with real public data. No background in climate science is needed. Every hard word is explained before it is used, and every number names its source.

## The story in one paragraph

The Earth, on average, is warmer now than it was in the 1880s. That is not a guess from one hot year. It shows up in decade averages, in every season, and most strongly in the far north. Carbon dioxide measured at Mauna Loa in Hawaii rose at the same time, from 315.98 parts per million in 1959 to 427.35 parts per million in 2025. In the United States, the number of weather and climate disasters costing at least 1 billion dollars rose from 33 in the 1980s to 131 in the 2010s, with 115 more in just 2020 to 2024. This project shows those three threads side by side, and it is careful about what each thread can and cannot prove.

## Start here, zero to hero

1. **Notebook 1, global temperature by decade.** Learn what an anomaly is, then see decade averages climb.
2. **Notebook 2, CO2 and temperature together.** Learn what ppm means, then see the two series rise together, with a correlation of 0.964 for 1959 to 2023. Correlation means they moved together. It does not, alone, prove a sole cause.
3. **Notebook 3, extreme events.** Learn what a billion-dollar disaster is, then see counts and costs by year, decade, and type.
4. **Notebook 4, regional patterns.** See that the northern hemisphere warmed more than the southern hemisphere, and the far north warmed about 3.1 times as much as the globe.
5. **Notebook 5, two original checks.** A warming pace check, and a cost versus frequency check. The second check is the surprise: total disaster cost rose mainly because there were more events, not because the average event kept getting costlier.
6. **Notebook 6, what the data shows and does not show.** An audit of every headline number, plus the limits, in plain words.

## Key verified findings

All numbers below were computed from the files in data/processed. Full workings are in the notebooks.

- Global decade averages, NASA GISTEMP repo file, baseline 1951 to 1980: 1880s, minus 0.209 degrees Celsius. 1980s, plus 0.247 degrees. 2010s, plus 0.806 degrees. 2020 to 2023 only, plus 0.980 degrees.
- Warmest single year in the repo file: 2023, plus 1.17 degrees.
- Warming pace, linear trend: 0.079 degrees per decade since 1880, 0.195 per decade since 1980, 0.235 per decade since 2000.
- CO2, NOAA Mauna Loa annual mean: 315.98 ppm in 1959, 421.08 ppm in 2023, 427.35 ppm in 2025. That is a rise of 111.37 ppm from 1959 to 2025.
- Correlation, annual CO2 versus annual temperature anomaly, 1959 to 2023: 0.964. Strong and positive. Stated as correlation, not as proof of sole cause.
- Regional rise, 1880 to 1889 mean compared with 2014 to 2023 mean, NASA zonal file: global, about 1.14 degrees. Northern hemisphere, about 1.51 degrees. Southern hemisphere, about 0.78 degrees. Far north, 64N to 90N, about 3.55 degrees, about 3.1 times the global rise.
- Seasons, same comparison, repo file: winter 1880s mean minus 0.24 degrees, 2014 to 2023 mean plus 0.92 degrees. Summer minus 0.20 degrees, then plus 0.87 degrees. Every season rose.
- Billion-dollar disasters, NOAA NCEI, United States, 1980 to 2024: 403 events, about 2,917.6 billion dollars CPI adjusted, 16,941 deaths listed.
- Disaster counts by decade: 1980s, 33 events. 1990s, 57. 2000s, 67. 2010s, 131. 2020 to 2024, 115.
- Disaster cost by type, total CPI adjusted: tropical cyclones, about 1,543.0 billion dollars from 67 events. Severe storms, about 514.0 billion dollars from 203 events. Drought, about 367.8 billion dollars from 32 events.
- Costliest single event: Hurricane Katrina, 2005, about 201.3 billion dollars CPI adjusted. Deadliest listed: Hurricane Maria, 2017, 2,981 deaths.
- Average cost per event, the original cost versus frequency check: 1980s, 6.66 billion dollars. 1990s, 5.88. 2000s, 9.28. 2010s, 7.59. 2020 to 2024, 6.49. The average bounces, it does not climb steadily, while the count climbs. So the total cost rise is driven mainly by frequency in this dataset.
- Zonal file only, beyond the repo file: global anomaly 1.28 degrees in 2024 and 1.18 degrees in 2025. These are reported separately, because the repo file ends in 2023.

## What this project does not claim

- It does not claim a temperature for any single town or day. These are global and regional averages.
- It does not claim that correlation proves a sole cause. See notebook 2 and notebook 6.
- It does not claim a global disaster trend. The disaster file covers the United States only, counts only events over 1 billion dollars, and ends in 2024.
- It does not fill gaps with guesses. Where a dataset stops, the story stops for that dataset.

## How to run it

Install the libraries, then process the data, then run the notebooks:

```
pip install -r requirements.txt
python3 scripts/download_data.py
python3 scripts/process_data.py
python3 scripts/make_charts.py
python3 scripts/build_notebooks.py
jupyter nbconvert --to notebook --execute --inplace notebooks/*.ipynb
```

Or run everything except notebook execution with:

```
bash scripts/rebuild_all.sh
```

## Files in this project

- notebooks/, 6 notebooks, each starting with a pip install cell, each executed end to end with zero cell errors.
- charts/, 15 charts.
- data/raw/, the downloaded files, plus PROVENANCE.md with every URL.
- data/processed/, tidy CSV tables made by scripts/process_data.py.
- scripts/, download, process, chart, and notebook building scripts, plus rebuild_all.sh.
- docs/, a story site in GitHub Pages style, with chart copies in docs/charts/.
- BUILD_REPORT.md, exactly which files were used, what ran, what failed or was approximated, and what was cut and why.

## Sources

- NASA GISTEMP global and zonal temperature, via the original repo file and the NASA tabledata files. See data/raw/PROVENANCE.md.
- NOAA Global Monitoring Laboratory, Mauna Loa CO2.
- NOAA NCEI, Billion-Dollar Weather and Climate Disasters archive, 1980 to 2024, CPI adjusted.

## Original repo files built on

This is a fresh local build. It builds on, and does not delete or overwrite, these files in github.com/jwavalosq/climate_change: data/GLB.Ts+dSST.csv, code/temperature_index_plot.R, figures/temperature_index_plot.png, and the README stub. The temperature file was refetched from its raw URL for this build. The R script was not rerun, because this build uses Python.

## Licence and reuse note

The source datasets are United States government public data. Cite NASA GISTEMP, NOAA Global Monitoring Laboratory, and NOAA NCEI when you reuse the numbers, and keep the year ranges and units with them.
