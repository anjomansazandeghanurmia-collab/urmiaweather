# هواشناسی انجمن سازندگان ذی‌صلاح ساختمان شهرستان ارومیه

## فایل‌ها (همه را در ریشه‌ی مخزن بگذار)
index.html                      خود سایت
manifest.json, sw.js            نصب به‌صورت برنامه‌ی گوشی (PWA)
icon-192.png, icon-512.png      آیکن برنامه
alerts.json                     اطلاعیه‌های رسمی (خودکار)
obs.json                        دمای واقعی ایستگاه فرودگاه ارومیه (خودکار)
scripts/fetch_alerts.py         خواندن هشدارها از اخبار
scripts/fetch_obs.py            خواندن METAR فرودگاه ارومیه
.github/workflows/alerts.yml    اجرای خودکار هر ۳ ساعت
.github/workflows/obs.yml       اجرای خودکار هر نیم‌ساعت

## راه‌اندازی
1. همه‌ی فایل‌ها و پوشه‌ها را در مخزن GitHub بگذار (پوشه‌ی .github را هم).
2. Settings > Pages > Deploy from a branch > main و پوشه‌ی root.
3. Settings > Actions > General > Workflow permissions > Read and write permissions.
4. تب Actions: هر دو گردش‌کار update-obs و update-alerts را یک بار Run workflow کن.

## اگر بالای سایت نوشته «دمای فعلی: مدل»
- obs.json را در مخزن باز کن. اگر فقط {} است، گردش‌کار update-obs را اجرا کن.
- اگر اجرا قرمز شد، روی آن کلیک کن و متن خطا را بخوان (به‌خصوص خط source).
- اسکریپت سه منبع را به‌ترتیب امتحان می‌کند (aviationweather.gov، فایل METAR سازمان NOAA، و آخرین راه allmetsat.com).
- بعد از پر شدن obs.json، صفحه را با Ctrl+F5 تازه کن.
- داخل پرانتز، دلیل دقیق نوشته می‌شود: «گزارش ایستگاه دریافت نشد» یا «آخرین گزارش ایستگاه N ساعت پیش است».

## نصب روی گوشی
اندروید: Chrome > ⋮ > Install app. آیفون: Safari > Share > Add to Home Screen.
از داخل تلگرام/اینستاگرام نصب ممکن نیست؛ اول «Open in browser» را بزن.
