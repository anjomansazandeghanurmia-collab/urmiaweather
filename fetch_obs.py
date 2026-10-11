#!/usr/bin/env python3
"""آخرین گزارش مشاهده‌ای (METAR) فرودگاه ارومیه (OITR) را می‌خواند و obs.json می‌سازد."""
import re, json, math, os, urllib.request
from datetime import datetime, timezone, timedelta

URLS = [
    "https://aviationweather.gov/api/data/metar?ids=OITR&format=raw&hours=3",
    "https://tgftp.nws.noaa.gov/data/observations/metar/stations/OITR.TXT",
    "https://en.allmetsat.com/metar-taf/georgia-armenia-azerbaijan.php?icao=OITR",  # آخرین راه
]
OUT = "obs.json"

def num(s):
    return -int(s[1:]) if s.startswith("M") else int(s)

def rh(t, td):
    f = lambda x: math.exp(17.625 * x / (243.04 + x))
    return round(min(100.0, 100 * f(td) / f(t)))

def parse(line):
    m = re.search(r"\b(\d{2})(\d{2})(\d{2})Z\b", line)
    tt = re.search(r"\b(M?\d{2})/(M?\d{2})\b", line)
    if not (m and tt):
        return None
    d, h, mi = map(int, m.groups())
    now = datetime.now(timezone.utc)
    y, mo = now.year, now.month
    try:
        t = datetime(y, mo, d, h, mi, tzinfo=timezone.utc)
        if t > now + timedelta(hours=2):
            mo, y = (12, y - 1) if mo == 1 else (mo - 1, y)
            t = datetime(y, mo, d, h, mi, tzinfo=timezone.utc)
    except ValueError:
        return None
    temp, dew = num(tt.group(1)), num(tt.group(2))
    w = re.search(r"\b(\d{3}|VRB)(\d{2,3})(?:G(\d{2,3}))?KT\b", line)
    q = re.search(r"\bQ(\d{4})\b", line)
    return {"station": "OITR", "time_utc": t.isoformat(), "temp": temp, "dew": dew, "rh": rh(temp, dew),
            "wind_kmh": round(int(w.group(2)) * 1.852) if w else None,
            "gust_kmh": round(int(w.group(3)) * 1.852) if w and w.group(3) else None,
            "qnh": int(q.group(1)) if q else None, "raw": line.strip()}

def fetch_lines():
    for url in URLS:
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (UrmiaWeatherBot)"})
            text = urllib.request.urlopen(req, timeout=30).read().decode("utf-8", "ignore")
            lines = [l.strip() for l in re.findall(r"OITR \d{6}Z[^\n\r<]*", text)]
            print("source", url, "->", len(lines), "lines")
            if lines:
                return lines
        except Exception as e:
            print("source failed", url, e)
    return []

def main():
    obs = next((o for o in (parse(l) for l in fetch_lines()) if o), None)
    if not obs:
        raise SystemExit("no METAR could be read from any source")
    old = json.load(open(OUT, encoding="utf-8")) if os.path.exists(OUT) else {}
    if old.get("time_utc") != obs["time_utc"]:
        json.dump(obs, open(OUT, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
        print("updated", obs["time_utc"], obs["temp"])
    else:
        print("no change")

if __name__ == "__main__":
    main()
