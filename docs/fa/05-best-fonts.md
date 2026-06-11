# بهترین فونت‌های فارسی استاندارد برای متون بلند وب‌سایت

---

## 🏆 رتبه‌بندی بر اساس کاربرد

### ۱. برای متن بدنه (Body Text) — خوانایی حرف اول

| رتبه | فونت | لایسنس | وزن مناسب | دلیل |
|---|---|---|---|---|
| 🥇 | **Vazirmatn** | SIL OFL (آزاد) | 400 | بهترین خوانایی در سایز کوچک، متن‌باز |
| 🥇 | **IRANSans** | رایگان برای وب | 400 | استاندارد ملی، پشتیبانی گسترده |
| 🥈 | **B Zar** | تجاری | Normal | کلاسیک اداری |
| 🥈 | **IRANyekan** | رایگان | 400 | مدرن و خوشخوان |
| 🥉 | **Shabnam** | SIL OFL (آزاد) | 400 | خوانا، شبیه ایرانسنس |

### ۲. برای عنوان (Heading) — تأثیر بصری

| رتبه | فونت | لایسنس | وزن مناسب |
|---|---|---|---|
| 🥇 | **B Titr** | تجاری | Bold |
| 🥇 | **Vazirmatn Bold** | SIL OFL | 700 |
| 🥈 | **IRANSans Bold** | رایگان | 700 |
| 🥉 | **Samim Bold** | SIL OFL | 700 |

### ۳. برای نستعلیق (تزئینی)

| فونت | لایسنس | کاربرد |
|---|---|---|
| **IranNastaliq** | رایگان | عنوان‌های هنری |
| **Noto Nastaliq Urdu** | SIL OFL (آزاد) | متن بلند نستعلیق |

---

## 📊 مقایسه حجم بهینه‌شده (Subset + WOFF2)

| فونت | حجم کامل | حجم بهینه | کاهش |
|---|---|---|---|
| Vazirmatn | ۴۵۰ KB | ۱۸ KB | ۹۶٪ |
| IRANSans | ۵۲۰ KB | ۲۲ KB | ۹۶٪ |
| Shabnam | ۳۸۰ KB | ۱۶ KB | ۹۶٪ |
| Samim | ۳۵۰ KB | ۱۵ KB | ۹۶٪ |

---

## 🎯 توصیه نهایی

### برای وب‌سایت حرفه‌ای فارسی (پیشنهاد برتر):

```css
/* ✅ ترکیب طلایی: */
body {
    font-family: 'Vazirmatn', 'IRANSans', Tahoma, sans-serif;
    /* Vazirmatn = متن‌باز، خوانا، بهینه */
}

h1, h2, h3 {
    font-family: 'Vazirmatn', 'B Titr', Tahoma, sans-serif;
}

/* اگر مجوز B Zar را دارید: */
body {
    font-family: 'B Zar', 'Vazirmatn', Tahoma, sans-serif;
}
```

### برای حداکثر سرعت:

```bash
# 1. دانلود Vazirmatn از GitHub
# 2. زیرمجموعه‌سازی برای فارسی
python subsetter.py Vazirmatn-Regular.ttf --lang fa -o vazirmatn-fa.ttf

# 3. تبدیل به WOFF2
woff2_compress vazirmatn-fa.ttf

# 4. نتیجه: ~18KB فونت فوق‌العاده خوانا!
```