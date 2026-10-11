# هواشناسی انجمن سازندگان ذی‌صلاح ساختمان شهرستان ارومیه

## ساختار فایل‌ها
index.html                      صفحه‌ی سایت
alerts.json                     اطلاعیه‌های رسمی (خودکار به‌روز می‌شود)
scripts/fetch_alerts.py         خواندن هشدارها از اخبار
.github/workflows/alerts.yml    اجرای خودکار هر ۳ ساعت

## راه‌اندازی
1. یک مخزن (Repository) جدید در GitHub بساز و همه‌ی فایل‌ها را با همین ساختار آپلود کن.
2. Settings > Pages > Source: Deploy from a branch > شاخه‌ی main و پوشه‌ی / (root) را انتخاب کن.
3. Settings > Actions > General > Workflow permissions: گزینه‌ی Read and write permissions را فعال کن.
4. تب Actions > update-alerts > Run workflow را یک بار بزن.

## نصب به‌صورت برنامه‌ی گوشی (PWA)
- اندروید (Chrome): دکمه‌ی «📲 نصب روی گوشی» بالای سایت یا منوی ⋮ > Install app
- آیفون (Safari): دکمه‌ی Share > Add to Home Screen
- فایل‌های manifest.json، sw.js و icon-192/512.png را کنار index.html نگه دار.
- برای فایل APK یا انتشار در مایکت: آدرس سایت را در pwabuilder.com بده و Android را بگیر.

## دمای دقیق فعلی (METAR فرودگاه ارومیه)
گردش‌کار obs.yml هر نیم‌ساعت آخرین گزارش مشاهده‌ای ایستگاه OITR را در obs.json ذخیره می‌کند.
سایت اگر این فایل کمتر از ۳ ساعت قدمت داشته باشد، دما، رطوبت، باد و فشار فعلی را از آن می‌خواند؛ وگرنه از مدل.
برای اولین بار از تب Actions گزینه‌ی update-obs را Run workflow کن.
