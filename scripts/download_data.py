"""Download every public dataset used by this project.

No key and no login are needed for any URL below.
Run from the project root: python3 scripts/download_data.py
Every URL is also recorded in data/raw/PROVENANCE.md.
"""
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "data" / "raw"
RAW.mkdir(parents=True, exist_ok=True)

URLS = {
    "GLB.Ts+dSST.csv": "https://raw.githubusercontent.com/jwavalosq/climate_change/main/data/GLB.Ts+dSST.csv",
    "ZonAnn.Ts+dSST.csv": "https://data.giss.nasa.gov/gistemp/tabledata_v4/ZonAnn.Ts+dSST.csv",
    "co2_mm_mlo.txt": "https://gml.noaa.gov/webdata/ccgg/trends/co2/co2_mm_mlo.txt",
    "co2_annmean_mlo.txt": "https://gml.noaa.gov/webdata/ccgg/trends/co2/co2_annmean_mlo.txt",
    "events-US.csv": "https://www.ncei.noaa.gov/access/billions/events-US.csv",
    "time-series-US.csv": "https://www.ncei.noaa.gov/access/billions/time-series-US.csv",
}

for filename, url in URLS.items():
    target = RAW / filename
    print(f"Downloading {url} -> {target}")
    urllib.request.urlretrieve(url, target)
    print(f"  saved {target.stat().st_size} bytes")

print("Done. Check data/raw/PROVENANCE.md for source details.")
