#!/usr/bin/env python3
"""اطلاعیه‌های رسمی هواشناسی آذربایجان غربی را از اخبار مهر می‌خواند و alerts.json می‌سازد."""
import re, json, html, os, sys, urllib.request
from datetime import datetime, timezone

BASE = "https://www.mehrnews.com"
TAG = BASE + "/tag/%D8%A7%D8%AF%D8%A7%D8%B1%D9%87+%DA%A9%D9%84+%D9%87%D9%88%D8%A7%D8%B4%D9%86%D8%A7%D8%B3%DB%8C+%D8%A2%D8%B0%D8%B1%D8%A8%D8%A7%DB%8C%D8%AC%D8%A7%D9%86+%D8%BA%D8%B1%D8%A8%DB%8C"
OUT = "alerts.json"
MAX_AGE_H = 60  # هشدارهای قدیمی‌تر از این نمایش داده نمی‌شوند

def get(url):
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (UrmiaWeatherBot)"})
    return urllib.request.urlopen(req, timeout=30).read().decode("utf-8", "ignore")

def clean(t):
    return re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", " ", t))).strip()

ICONS = [("سیل|آبگرفتگی|مسیل", "🌊"), ("برف|کولاک", "❄️"), ("رعد|تگرگ", "⛈️"),
         ("باد|تندباد", "💨"), ("گرد و خاک|گردوخاک", "🌫️"), ("سرما|یخبندان", "🥶"), ("باران|رگبار|بارش", "🌧️")]

def parse(path):
    page = get(BASE + path)
    m = re.search(r'article:published_time"\s+content="([^"]+)"', page) or re.search(r'"datePublished"\s*:\s*"([^"]+)"', page)
    if not m:
        return None
    pub = datetime.fromisoformat(m.group(1).replace("Z", "+00:00"))
    if pub.tzinfo is None:
        pub = pub.replace(tzinfo=timezone.utc)
    age = (datetime.now(timezone.utc) - pub).total_seconds() / 3600
    if age > MAX_AGE_H:
        return None
    title = clean((re.search(r"<h1[^>]*>(.*?)</h1>", page, re.S) or re.search(r"<title>(.*?)</title>", page, re.S)).group(1))
    desc = re.search(r'property="og:description"\s+content="([^"]+)"', page)
    body = clean(" ".join(re.findall(r"<p[^>]*>(.*?)</p>", page, re.S)))[:900]
    text = html.unescape(desc.group(1)) if desc else body
    blob = title + " " + body
    if "آذربایجان غربی" not in blob and "ارومیه" not in blob:
        return None
    level = 3 if "قرمز" in title else 2 if "نارنجی" in title else 1 if "زرد" in title else 0
    if not level:
        return None
    icon = next((i for k, i in ICONS if re.search(k, blob)), "⚠️")
    local = pub.astimezone().strftime("%Y-%m-%d %H:%M")
    return {"level": level, "icon": icon, "title": title, "time": "زمان انتشار: " + local,
            "text": text[:320], "source": "خبرگزاری مهر", "link": BASE + path}

def main():
    listing = get(TAG)
    seen, items = set(), []
    for path, label in re.findall(r'href="(/news/\d+/[^"]*)"[^>]*>(.*?)</a>', listing, re.S):
        if path in seen or "هشدار" not in clean(label):
            continue
        seen.add(path)
        if len(seen) > 10:
            break
        try:
            a = parse(path)
            if a:
                items.append(a)
        except Exception as e:
            print("skip", path, e, file=sys.stderr)
    items.sort(key=lambda a: -a["level"])
    old = json.load(open(OUT, encoding="utf-8")) if os.path.exists(OUT) else {}
    if old.get("alerts") != items:
        json.dump({"updated": datetime.now(timezone.utc).isoformat(), "alerts": items},
                  open(OUT, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
        print("updated:", len(items), "alerts")
    else:
        print("no change")

if __name__ == "__main__":
    main()
