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
