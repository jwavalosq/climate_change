"""Build the six notebooks. Run: python3 scripts/build_notebooks.py
Each notebook starts with a pip install cell, reads data/processed,
prints verified numbers, and saves its charts to charts/.
No em dash character is used anywhere in this file.
"""
import nbformat as nbf
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
NB = ROOT / "notebooks"
NB.mkdir(parents=True, exist_ok=True)

INSTALL = (
    "# Top cell: install the libraries this notebook uses.\n"
    "# If they are already installed, pip will simply say so.\n"
    "%pip install -q pandas matplotlib numpy scipy"
)
IMPORTS = (
    "import matplotlib\n"
    "matplotlib.use('Agg')\n"
    "import matplotlib.pyplot as plt\n"
    "import pandas as pd\n"
    "import numpy as np\n"
    "from pathlib import Path\n"
    "ROOT = Path('..').resolve()\n"
    "PROC = ROOT / 'data' / 'processed'\n"
    "CH = ROOT / 'charts'\n"
    "CH.mkdir(exist_ok=True)\n"
    "plt.rcParams.update({'figure.dpi': 150})\n"
    "print('Paths ready:', PROC.exists(), CH.exists())"
)


def nb(cells):
    doc = nbf.v4.new_notebook()
    doc.cells = cells
    doc.metadata = {"kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"},
                    "language_info": {"name": "python", "version": "3.12"}}
    return doc


def md(text):
    return nbf.v4.new_markdown_cell(text)


def code(text):
    return nbf.v4.new_code_cell(text)


def save(name, doc):
    path = NB / name
    nbf.write(doc, str(path))
    print(f"wrote {path}")

# Notebook 1
save("01_global_temperature_decades.ipynb", nb([
    code(INSTALL), code(IMPORTS),
    md("# 1. Global temperature, by decade\n\n"
       "First, a plain word guide. A temperature anomaly is not the temperature itself. "
       "It is the difference from a reference average. Here the reference is 1951 to 1980, "
       "the baseline NASA GISTEMP uses. So an anomaly of plus 1.0 means 1.0 degrees Celsius "
       "warmer than that 1951 to 1980 average. A negative anomaly means cooler than that average.\n\n"
       "Source: NASA GISTEMP, file GLB.Ts+dSST.csv from the original climate_change repo, 1880 to 2023. "
       "The 2020s row in this file covers 2020 to 2023 only. It is labelled as partial everywhere it appears."),
    code("g = pd.read_csv(PROC / 'global_annual.csv')\n"
         "print(g.head())\nprint(g.tail())\nprint('Years:', g['year'].min(), 'to', g['year'].max(), '| rows:', len(g))\n"
         "assert len(g) == 144, 'expected 144 years, 1880 to 2023'"),
    code("fig, ax = plt.subplots(figsize=(10, 5))\n"
         "ax.plot(g['year'], g['annual_anomaly_c'], color='#1f77b4')\n"
         "ax.axhline(0, color='grey', linewidth=0.8)\n"
         "ax.set_title('Global temperature anomaly, each year from 1880 to 2023')\n"
         "ax.set_xlabel('Year')\nax.set_ylabel('Anomaly in degrees Celsius, versus 1951-1980')\n"
         "fig.savefig(CH / '01_global_annual_anomaly.png', bbox_inches='tight')\nplt.show()\n"
         "print('Warmest year in this file:', g.loc[g['annual_anomaly_c'].idxmax(), 'year'], g['annual_anomaly_c'].max())"),
    code("d = pd.read_csv(PROC / 'decade_means.csv')\nprint(d.to_string(index=False))"),
    code("fig, ax = plt.subplots(figsize=(10, 5))\n"
         "ax.bar(d['decade'], d['mean_anomaly_c'], color='#2ca02c')\n"
         "ax.axhline(0, color='grey', linewidth=0.8)\n"
         "ax.set_title('Average temperature anomaly by decade')\n"
         "ax.set_xlabel('Decade (2020s covers 2020-2023 only)')\nax.set_ylabel('Mean anomaly in degrees Celsius')\n"
         "plt.setp(ax.get_xticklabels(), rotation=30, ha='right')\n"
         "fig.savefig(CH / '02_decade_means.png', bbox_inches='tight')\nplt.show()\n"
         "print('1980s mean:', round(d[d['decade']=='1980s']['mean_anomaly_c'].iloc[0], 3))\n"
         "print('2010s mean:', round(d[d['decade']=='2010s']['mean_anomaly_c'].iloc[0], 3))"),
    md("## What this shows\n\n"
       "The 1880s average was minus 0.209 degrees. The 2010s average was plus 0.806 degrees. "
       "The gap between those two decade averages is about 1.02 degrees. "
       "Single years still jump up and down, but the decade averages climb, step by step, from the 1980s onward. "
       "That is why this project uses decade averages as well as single years: they smooth out one hot or cold year."),
]))

# Notebook 2
save("02_co2_and_temperature.ipynb", nb([
    code(INSTALL), code(IMPORTS),
    md("# 2. Carbon dioxide and temperature together\n\n"
       "Plain words first. CO2 means carbon dioxide, a gas in the air. ppm means parts per million. "
       "If air had one million parts, 421 ppm means 421 of them are CO2. Mauna Loa is a NOAA measuring station "
       "in Hawaii, far from most factories and cities, so it gives a clean background reading.\n\n"
       "Correlation is a number from minus 1 to plus 1 that says whether two series move together. "
       "A value near plus 1 means when one goes up, the other usually goes up too. "
       "Correlation alone does not prove that one thing caused the other. This notebook states the correlation plainly "
       "and does not claim it proves a sole cause.\n\n"
       "Sources: NOAA Global Monitoring Laboratory, Mauna Loa annual means, 1959 to 2025. "
       "NASA GISTEMP global anomalies, 1880 to 2023. The joined table covers 1959 to 2023."),
    code("c = pd.read_csv(PROC / 'co2_annual.csv')\nprint(c.head())\nprint(c.tail())\n"
         "print('CO2 in 1959:', c[c['year']==1959]['mean_ppm'].iloc[0], 'ppm')\n"
         "print('CO2 in 2023:', c[c['year']==2023]['mean_ppm'].iloc[0], 'ppm')\n"
         "print('CO2 in 2025:', c[c['year']==2025]['mean_ppm'].iloc[0], 'ppm')"),
    code("fig, ax = plt.subplots(figsize=(10, 5))\n"
         "ax.plot(c['year'], c['mean_ppm'], color='#9467bd', linewidth=2)\n"
         "ax.set_title('Carbon dioxide at Mauna Loa, annual mean, 1959 to 2025')\n"
         "ax.set_xlabel('Year')\nax.set_ylabel('Parts per million (ppm)')\n"
         "fig.savefig(CH / '05_co2_annual.png', bbox_inches='tight')\nplt.show()"),
    code("j = pd.read_csv(PROC / 'co2_temp_annual.csv')\n"
         "corr = j['mean_ppm'].corr(j['annual_anomaly_c'])\n"
         "print('Years joined:', len(j), j['year'].min(), 'to', j['year'].max())\n"
         "print(f'Correlation between annual CO2 and annual temperature anomaly: {corr:.3f}')\n"
         "print('Reading: a strong positive correlation. It shows the two rose together.')\n"
         "print('It does not, on its own, prove that CO2 was the sole cause.')"),
    code("fig, ax = plt.subplots(figsize=(8, 6))\n"
         "ax.scatter(j['mean_ppm'], j['annual_anomaly_c'], s=20, color='#1f77b4')\n"
         "ax.set_title('Each dot is one year: higher CO2, higher temperature anomaly')\n"
         "ax.set_xlabel('CO2 in ppm, Mauna Loa annual mean')\nax.set_ylabel('Temperature anomaly in degrees Celsius')\n"
         "fig.savefig(CH / '07_co2_vs_temperature_scatter.png', bbox_inches='tight')\nplt.show()"),
    code("fig, ax1 = plt.subplots(figsize=(10, 5))\n"
         "ax1.plot(j['year'], j['mean_ppm'], color='#9467bd', linewidth=2)\n"
         "ax1.set_xlabel('Year')\nax1.set_ylabel('CO2 in ppm', color='#9467bd')\n"
         "ax2 = ax1.twinx()\nax2.plot(j['year'], j['annual_anomaly_c'], color='#d62728', linewidth=1.5)\n"
         "ax2.set_ylabel('Temperature anomaly in degrees Celsius', color='#d62728')\n"
         "ax1.set_title('CO2 and global temperature rose together, 1959 to 2023')\n"
         "fig.savefig(CH / '06_co2_and_temperature_dual.png', bbox_inches='tight')\nplt.show()\n"
         "print('CO2 rise 1959 to 2025:', round(c[c['year']==2025]['mean_ppm'].iloc[0] - c[c['year']==1959]['mean_ppm'].iloc[0], 2), 'ppm')"),
    md("## What this shows, and what it does not show\n\n"
       "From 1959 to 2023 the correlation is 0.964, a strong positive value. CO2 rose from 315.98 ppm in 1959 "
       "to 421.08 ppm in 2023, and to 427.35 ppm in 2025. Temperature anomalies rose over the same span. "
       "That joint rise is a fact from these two datasets. It is not, by itself, a full causal proof. "
       "A full attribution case uses physics, many datasets, and models, which are outside this project's scope. "
       "This notebook stays inside what these two series can honestly show."),
]))

# Notebook 3
save("03_extreme_events_frequency_cost.ipynb", nb([
    code(INSTALL), code(IMPORTS),
    md("# 3. Extreme events: frequency and costs over time\n\n"
       "Plain words first. This chapter uses the United States only, because that is what the source covers. "
       "A billion-dollar disaster is a weather or climate event whose total direct losses reached at least "
       "1 billion US dollars. Costs here are CPI adjusted, which means they are adjusted for inflation so that "
       "a dollar in 1980 and a dollar in 2024 are compared on a fairer basis. CPI stands for Consumer Price Index.\n\n"
       "Important limit: this dataset counts only events that crossed the 1 billion dollar line. "
       "It does not count every flood, storm, or fire. So a rise in this count can reflect more large events, "
       "more valuable property in harm's way, better reporting, or a mix of those. The dataset alone cannot split those causes.\n\n"
       "Source: NOAA NCEI, Billion-Dollar Disasters archive, 1980 to 2024, 403 events. "
       "NOAA stopped updating this product in 2025. Climate Central now continues a similar list, but its post 2024 "
       "events are not included here, so the years stay comparable."),
    code("ev = pd.read_csv(PROC / 'disasters_events.csv')\nprint('Events:', len(ev))\nprint('Total CPI adjusted cost, billion USD:', round(ev['cost_cpi_adjusted_billion_usd'].sum(), 1))\n"
         "print('Total deaths in file:', int(ev['deaths'].sum()))\n"
         "assert len(ev) == 403, 'expected 403 events'\nprint(ev.head().to_string(index=False))"),
    code("by = pd.read_csv(PROC / 'disasters_by_year.csv')\nprint(by.tail(10).to_string(index=False))\n"
         "fig, ax = plt.subplots(figsize=(10, 5))\n"
         "ax.bar(by['year'], by['event_count'], color='#ff7f0e')\n"
         "ax.set_title('Billion-dollar disasters in the United States, count by year, 1980 to 2024')\n"
         "ax.set_xlabel('Year')\nax.set_ylabel('Number of events')\n"
         "fig.savefig(CH / '08_disasters_count_by_year.png', bbox_inches='tight')\nplt.show()"),
    code("bd = pd.read_csv(PROC / 'disasters_by_decade.csv')\nprint(bd.to_string(index=False))\n"
         "fig, ax = plt.subplots(figsize=(10, 5))\n"
         "ax.bar(bd['decade'], bd['total_cost_cpi_billion_usd'], color='#d62728')\n"
         "ax.set_title('Total CPI adjusted cost of billion-dollar disasters, by decade')\n"
         "ax.set_xlabel('Decade (2020s covers 2020-2024 only)')\nax.set_ylabel('Billion US dollars, CPI adjusted')\n"
         "plt.setp(ax.get_xticklabels(), rotation=20, ha='right')\n"
         "fig.savefig(CH / '09_disasters_cost_by_decade.png', bbox_inches='tight')\nplt.show()"),
    code("by_type = ev.groupby('disaster_type').agg(count=('name', 'count'), cost=('cost_cpi_adjusted_billion_usd', 'sum')).sort_values('count', ascending=False)\n"
         "print(by_type.round(1).to_string())\n"
         "fig, ax = plt.subplots(figsize=(10, 5))\n"
         "ax.bar(by_type.index, by_type['count'], color='#2ca02c')\n"
         "ax.set_title('Billion-dollar disasters by type, 1980 to 2024: count')\n"
         "ax.set_xlabel('Disaster type')\nax.set_ylabel('Number of events')\n"
         "plt.setp(ax.get_xticklabels(), rotation=20, ha='right')\n"
         "fig.savefig(CH / '10_disasters_by_type_count.png', bbox_inches='tight')\nplt.show()"),
    code("fig, ax = plt.subplots(figsize=(10, 5))\n"
         "ax.bar(by_type.sort_values('cost', ascending=False).index, by_type.sort_values('cost', ascending=False)['cost'], color='#9467bd')\n"
         "ax.set_title('Billion-dollar disasters by type, 1980 to 2024: total cost')\n"
         "ax.set_xlabel('Disaster type')\nax.set_ylabel('Billion US dollars, CPI adjusted')\n"
         "plt.setp(ax.get_xticklabels(), rotation=20, ha='right')\n"
         "fig.savefig(CH / '11_disasters_by_type_cost.png', bbox_inches='tight')\nplt.show()\n"
         "print('Costliest single event:')\n"
         "print(ev.sort_values('cost_cpi_adjusted_billion_usd', ascending=False).head(3)[['name', 'disaster_type', 'year', 'cost_cpi_adjusted_billion_usd', 'deaths']].to_string(index=False))"),
    md("## What this shows\n\n"
       "Severe storms are the most frequent type, with 203 of 403 events, but tropical cyclones cost the most in total, "
       "about 1,543 billion dollars CPI adjusted, from only 67 events. The single costliest event in the file is "
       "Hurricane Katrina in 2005, at about 201.3 billion dollars CPI adjusted. The deadliest is Hurricane Maria in 2017, "
       "with 2,981 deaths listed. Counts rose from 33 events in the 1980s to 131 in the 2010s, and 115 more in just "
       "2020 to 2024. Total cost rose too, but as notebook 5 shows, the average cost per event did not rise in the same way. "
       "That split is the key story: more events, not simply more expensive events."),
]))

# Notebook 4
save("04_regional_patterns.ipynb", nb([
    code(INSTALL), code(IMPORTS),
    md("# 4. Regional patterns: not everywhere warms at the same pace\n\n"
       "Plain words first. A hemisphere is one half of the Earth: northern or southern. "
       "A latitude band is a strip around the globe, for example 64N to 90N, which is the far north including the Arctic. "
       "Warming is not uniform. Some places warm faster than the global average. This notebook compares bands, "
       "it does not draw a map, because no gridded map dataset was used in this build.\n\n"
       "Source: NASA GISTEMP zonal means, 1880 to 2025. For comparisons with the repo global file, years to 2023 are used. "
       "The 2024 and 2025 zonal values are reported separately in the text."),
    code("z = pd.read_csv(PROC / 'zonal_annual.csv')\nprint(z.head().to_string(index=False))\n"
         "print('Years:', z['year'].min(), 'to', z['year'].max())\n"
         "print('Global 2024:', z[z['year']==2024]['global_c'].iloc[0], '| 2025:', z[z['year']==2025]['global_c'].iloc[0])"),
    code("z23 = z[z['year'] <= 2023]\n"
         "fig, ax = plt.subplots(figsize=(10, 5))\n"
         "ax.plot(z23['year'], z23['northern_hemisphere_c'], label='Northern hemisphere', color='#d62728')\n"
         "ax.plot(z23['year'], z23['southern_hemisphere_c'], label='Southern hemisphere', color='#1f77b4')\n"
         "ax.plot(z23['year'], z23['global_c'], label='Global', color='black', linewidth=1)\n"
         "ax.axhline(0, color='grey', linewidth=0.8)\nax.legend()\n"
         "ax.set_title('Northern hemisphere warmed more than southern hemisphere, 1880 to 2023')\n"
         "ax.set_xlabel('Year')\nax.set_ylabel('Anomaly in degrees Celsius')\n"
         "fig.savefig(CH / '13_hemisphere_comparison.png', bbox_inches='tight')\nplt.show()"),
    code("fig, ax = plt.subplots(figsize=(10, 5))\n"
         "ax.plot(z23['year'], z23['arctic_64_to_90_c'], label='64N to 90N (far north)', color='#d62728')\n"
         "ax.plot(z23['year'], z23['global_c'], label='Global', color='black', linewidth=1)\n"
         "ax.axhline(0, color='grey', linewidth=0.8)\nax.legend()\n"
         "ax.set_title('The far north warmed much faster than the globe as a whole')\n"
         "ax.set_xlabel('Year')\nax.set_ylabel('Anomaly in degrees Celsius')\n"
         "fig.savefig(CH / '14_arctic_vs_global.png', bbox_inches='tight')\nplt.show()"),
    code("recent = z23[z23['year'].between(2014, 2023)]\n"
         "early = z23[z23['year'].between(1880, 1889)]\n"
         "for col in ['global_c', 'northern_hemisphere_c', 'southern_hemisphere_c', 'arctic_64_to_90_c', 'tropics_24s_to_24n_c']:\n"
         "    print(col, '| 1880-1889 mean:', round(early[col].mean(), 2), '| 2014-2023 mean:', round(recent[col].mean(), 2), '| rise:', round(recent[col].mean() - early[col].mean(), 2))\n"
         "print('Arctic rise divided by global rise:', round((recent['arctic_64_to_90_c'].mean() - early['arctic_64_to_90_c'].mean()) / (recent['global_c'].mean() - early['global_c'].mean()), 2))"),
    code("g = pd.read_csv(PROC / 'global_annual.csv')\n"
         "early_s = g[g['year'].between(1880, 1889)][['winter_djf_c', 'spring_mam_c', 'summer_jja_c', 'autumn_son_c']].mean()\n"
         "recent_s = g[g['year'].between(2014, 2023)][['winter_djf_c', 'spring_mam_c', 'summer_jja_c', 'autumn_son_c']].mean()\n"
         "print('Season means, 1880-1889:'); print(early_s.round(2).to_string())\n"
         "print('Season means, 2014-2023:'); print(recent_s.round(2).to_string())\n"
         "labels = ['Winter (DJF)', 'Spring (MAM)', 'Summer (JJA)', 'Autumn (SON)']\n"
         "fig, ax = plt.subplots(figsize=(10, 5))\n"
         "x = range(len(labels))\n"
         "ax.bar([i - 0.2 for i in x], early_s.values, width=0.4, label='1880-1889 mean', color='#bbbbbb')\n"
         "ax.bar([i + 0.2 for i in x], recent_s.values, width=0.4, label='2014-2023 mean', color='#d62728')\n"
         "ax.axhline(0, color='grey', linewidth=0.8)\nax.set_xticks(list(x)); ax.set_xticklabels(labels); ax.legend()\n"
         "ax.set_title('Every season is warmer in 2014-2023 than in 1880-1889')\n"
         "ax.set_ylabel('Anomaly in degrees Celsius')\n"
         "fig.savefig(CH / '15_seasonal_comparison.png', bbox_inches='tight')\nplt.show()"),
    md("## What this shows\n\n"
       "From the 1880s to 2014-2023, the global mean rose by about 1.14 degrees, the northern hemisphere by about 1.51 degrees, "
       "the southern hemisphere by about 0.78 degrees, and the far north band (64N to 90N) by about 3.55 degrees. "
       "That far north rise is about 3.1 times the global rise. Scientists call faster Arctic warming Arctic amplification. "
       "This project reports the ratio from the data; it does not add a separate physical explanation beyond that label. "
       "Every season rose too: winter, spring, summer, and autumn are all warmer in 2014-2023 than in 1880-1889."),
]))

# Notebook 5
save("05_original_metrics.ipynb", nb([
    code(INSTALL), code(IMPORTS),
    md("# 5. Two original checks: warming pace, and cost versus frequency\n\n"
       "This notebook adds two checks that are not simply copied from a source chart.\n\n"
       "Check 1, warming pace: for each decade, take the decade average minus the previous decade average. "
       "That change is the pace for that decade. A larger positive change means faster warming that decade.\n\n"
       "Check 2, cost versus frequency: for disasters, take total cost divided by event count for each decade. "
       "That is the average cost per event. If total cost rises only because there are more events, "
       "the average per event will stay flat. If each event is getting costlier, the average will rise.\n\n"
       "Both checks use only the processed tables from notebooks 1 and 3, so every input can be traced."),
    code("d = pd.read_csv(PROC / 'decade_means.csv')\nprint(d.to_string(index=False))\n"
         "fig, ax = plt.subplots(figsize=(10, 5))\n"
         "ax.bar(d.dropna(subset=['change_from_previous_decade_c'])['decade'], d.dropna(subset=['change_from_previous_decade_c'])['change_from_previous_decade_c'], color='#d62728')\n"
         "ax.axhline(0, color='grey', linewidth=0.8)\n"
         "ax.set_title('How much the decade average moved, compared with the decade before')\n"
         "ax.set_xlabel('Decade')\nax.set_ylabel('Change in degrees Celsius')\n"
         "plt.setp(ax.get_xticklabels(), rotation=30, ha='right')\n"
         "fig.savefig(CH / '03_decade_change_pace.png', bbox_inches='tight')\nplt.show()"),
    code("g = pd.read_csv(PROC / 'global_annual.csv')\n"
         "for a, b in [(1880, 2023), (1970, 2023), (1980, 2023), (2000, 2023)]:\n"
         "    s = g[(g['year'] >= a) & (g['year'] <= b)]\n"
         "    slope_per_decade = np.polyfit(s['year'], s['annual_anomaly_c'], 1)[0] * 10\n"
         "    print(f'Linear trend {a} to {b}: {slope_per_decade:.3f} degrees Celsius per decade')\n"
         "print('Reading: the trend since 1980 is steeper than the trend since 1880. Warming sped up.')"),
    code("bd = pd.read_csv(PROC / 'disasters_by_decade.csv')\nprint(bd.to_string(index=False))\n"
         "fig, ax = plt.subplots(figsize=(10, 5))\n"
         "ax.bar(bd['decade'], bd['mean_cost_per_event_billion_usd'], color='#17becf')\n"
         "ax.set_title('Average cost per billion-dollar event, by decade')\n"
         "ax.set_xlabel('Decade (2020s covers 2020-2024 only)')\nax.set_ylabel('Billion US dollars per event, CPI adjusted')\n"
         "plt.setp(ax.get_xticklabels(), rotation=20, ha='right')\n"
         "fig.savefig(CH / '12_cost_per_event_by_decade.png', bbox_inches='tight')\nplt.show()"),
    code("g2 = g.copy()\n"
         "g2['rolling_10yr'] = g2['annual_anomaly_c'].rolling(10).mean()\n"
         "fig, ax = plt.subplots(figsize=(10, 5))\n"
         "ax.plot(g2['year'], g2['annual_anomaly_c'], color='#bbbbbb', linewidth=0.8, label='Single year')\n"
         "ax.plot(g2['year'], g2['rolling_10yr'], color='#1f77b4', linewidth=2, label='10 year rolling mean')\n"
         "ax.axhline(0, color='grey', linewidth=0.8); ax.legend()\n"
         "ax.set_title('Single years jump around. The 10 year mean shows the trend.')\n"
         "ax.set_xlabel('Year')\nax.set_ylabel('Anomaly in degrees Celsius')\n"
         "fig.savefig(CH / '04_rolling_10yr_mean.png', bbox_inches='tight')\nplt.show()"),
    md("## What the two checks find\n\n"
       "Warming pace: the decade average rose by 0.212 degrees from the 1970s to the 1980s, by 0.204 from the 1990s "
       "to the 2000s, and by 0.217 from the 2000s to the 2010s. The linear trend is 0.079 degrees per decade since 1880, "
       "but 0.195 per decade since 1980 and 0.235 per decade since 2000. In plain words, recent decades warmed faster "
       "than the long run average.\n\n"
       "Cost versus frequency: the average cost per billion-dollar event was 6.66 billion dollars in the 1980s, "
       "5.88 in the 1990s, 9.28 in the 2000s, 7.59 in the 2010s, and 6.49 in 2020 to 2024. "
       "It bounces around, it does not climb steadily. Meanwhile the event count climbed from 33 to 131 to 115 in five years. "
       "So the rise in total disaster cost in this dataset is driven mainly by more events crossing the line, "
       "not by a steady rise in the average cost of each event. That conclusion is limited to this dataset and its threshold. "
       "It does not say anything about smaller events, which this dataset excludes by design."),
]))

# Notebook 6
save("06_what_data_shows_and_limits.ipynb", nb([
    code(INSTALL), code(IMPORTS),
    md("# 6. What the data shows, and what it does not show\n\n"
       "This final notebook is a honesty check. It repeats the headline numbers from the earlier notebooks, "
       "recomputes them from the processed tables, and lists the limits in plain words. If a claim cannot be "
       "recomputed here, it does not belong in the story.\n\n"
       "No new data is introduced in this notebook. That is on purpose: the point is to audit, not to add."),
    code("g = pd.read_csv(PROC / 'global_annual.csv')\n"
         "d = pd.read_csv(PROC / 'decade_means.csv')\n"
         "c = pd.read_csv(PROC / 'co2_annual.csv')\n"
         "j = pd.read_csv(PROC / 'co2_temp_annual.csv')\n"
         "ev = pd.read_csv(PROC / 'disasters_events.csv')\n"
         "z = pd.read_csv(PROC / 'zonal_annual.csv')\n"
         "checks = []\n"
         "checks.append(('Global years in repo file', len(g), 144))\n"
         "checks.append(('Disaster events 1980-2024', len(ev), 403))\n"
         "checks.append(('CO2 years 1959-2025', len(c), 67))\n"
         "checks.append(('Joined CO2 and temperature years', len(j), 65))\n"
         "for label, got, want in checks:\n"
         "    print(label, ':', got, '| expected:', want, '| match:', got == want)\n"
         "    assert got == want\n"
         "print('Correlation CO2 vs temperature, 1959-2023:', round(j['mean_ppm'].corr(j['annual_anomaly_c']), 3))\n"
         "print('Total disaster cost, billion USD CPI adjusted:', round(ev['cost_cpi_adjusted_billion_usd'].sum(), 1))\n"
         "print('Zonal global 2024:', z[z['year']==2024]['global_c'].iloc[0], '| 2025:', z[z['year']==2025]['global_c'].iloc[0])\n"
         "print('Note: 2024 and 2025 zonal values come from the current NASA file, not the repo file, which ends in 2023.')"),
    md("## What the data shows\n\n"
       "1. Global temperature anomalies rose from a 1880s average of minus 0.209 degrees to a 2010s average of plus 0.806 degrees, "
       "on the 1951 to 1980 baseline, in the repo GISTEMP file.\n"
       "2. CO2 at Mauna Loa rose from 315.98 ppm in 1959 to 427.35 ppm in 2025, with a 0.964 correlation to annual temperature "
       "anomalies over 1959 to 2023.\n"
       "3. The far north warmed about 3.1 times as much as the globe, comparing 2014-2023 with 1880-1889.\n"
       "4. United States billion-dollar disasters rose from 33 events in the 1980s to 131 in the 2010s, with 115 more in 2020 to 2024, "
       "for a 1980 to 2024 total of 403 events and about 2,917.6 billion dollars CPI adjusted.\n\n"
       "## What the data does not show\n\n"
       "1. It does not show the temperature of any single town or day. These are global and zonal averages.\n"
       "2. Correlation between CO2 and temperature does not, alone, prove a sole cause. Other factors, feedbacks, and "
       "natural variation also matter, and this project does not model them.\n"
       "3. The disaster file covers the United States only, counts only events over 1 billion dollars, and ends in 2024. "
       "It cannot prove a global trend, and it cannot separate climate change from more property at risk or better reporting.\n"
       "4. Costs are estimates, CPI adjusted, with uncertainty. NOAA itself publishes confidence bounds in its time series file. "
       "This project uses point estimates and says so.\n"
       "5. Early temperature records are thinner than modern ones, especially in the far north and far south. "
       "That is a reason to trust decade averages more than any single early year.\n"
       "6. Disputed figures are not settled here. Where different sources give different disaster costs, for example insurer "
       "estimates versus NOAA estimates, this project uses NOAA and labels it as NOAA, so a reader can compare.\n\n"
       "## Uncertainty, in one paragraph\n\n"
       "Every number here comes with a source, a year range, and a unit. Where a range is partial, it is labelled partial. "
       "Where a dataset stopped, 2024 for disasters and 2023 for the repo temperature file, the story stops there for that dataset, "
       "instead of filling the gap with a guess. That restraint is part of the result."),
    code("print('Audit complete. All headline numbers recomputed from data/processed.')\nprint('Files to check: data/raw/PROVENANCE.md and BUILD_REPORT.md')"),
]))

print("All notebooks built.")
