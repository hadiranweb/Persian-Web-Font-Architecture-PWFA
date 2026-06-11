# راهنمای پیاده‌سازی فونت‌های اداری در CSS

> حل مشکلات نمایش و بهینه‌سازی @font-face برای فونت‌های فارسی

---

## ۱. مشکل اصلی: چرا فونت فارسی در وب درست نمایش داده نمی‌شود؟

### مشکلات رایج:

| مشکل | علت | راه‌حل |
|---|---|---|
| **فاصله‌های نامنظم** | نبود hinting مناسب در فونت TTF | استفاده از WOFF2 + font-smooth |
| **اعداد فارسی به لاتین تبدیل می‌شوند** | نبود unicode-range | تنظیم محدوده فارسی برای numbers |
| **تغییر سایز فونت در مرورگرهای مختلف** | نبود font-size-adjust | تنظیم fallback با aspect-ratio مشابه |
| **FOUT شدید** | font-display پیش‌فرض (block) | font-display: swap |
| **لود کند** | حجم بالای فایل | زیرمجموعه‌سازی + WOFF2 |

---

## ۲. قالب کامل @font-face برای فونت اداری

```css
/* ☑️ قالب پیشنهادی برای B Zar */
@font-face {
    font-family: 'B Zar';
    src: url('fonts/b-zar.woff2') format('woff2'),
         url('fonts/b-zar.woff') format('woff');
    font-weight: normal;
    font-style: normal;
    font-display: swap;
    unicode-range: U+0600-06FF, U+FB50-FDFF, U+FE70-FEFF, U+0020-007E;
    size-adjust: 95%;  /* تنظیم اندازه نسبی با fallback */
}

/* ☑️ قالب پیشنهادی برای B Titr */
@font-face {
    font-family: 'B Titr';
    src: url('fonts/b-titr.woff2') format('woff2');
    font-weight: bold;
    font-display: swap;
    unicode-range: U+0600-06FF, U+FB50-FDFF, U+FE70-FEFF, U+0020-007E;
}

/* ☑️ قالب پیشنهادی برای B Mitra */
@font-face {
    font-family: 'B Mitra';
    src: url('fonts/b-mitra.woff2') format('woff2');
    font-weight: normal;
    font-display: swap;
}
```

---

## ۳. بهترین Fallback Stack برای فارسی

```css
/* --- متن بلند (body, article) --- */
body {
    font-family: 'B Zar', 'Vazirmatn', 'IRANSans', Tahoma, sans-serif;
    /* 
       B Zar: بهترین برای متن بلند اداری
       Vazirmatn: جایگزین متن‌باز عالی
       IRANSans: جایگزین ایرانی متداول
       Tahoma: fallback پنجره‌ای استاندارد
       sans-serif: نهایی
    */
}

/* --- عنوان (h1, h2, h3) --- */
h1 {
    font-family: 'B Titr', 'B Zar', 'Vazirmatn', Tahoma, sans-serif;
    /* B Titr برای عنوان مناسب‌تر است */
}

/* --- کد و اعداد --- */
code, pre {
    font-family: 'B Mitra', 'Vazirmatn FD', 'Courier New', monospace;
    /* 'Vazirmatn FD' شامل اعداد فارسی است */
}
```

---

## ۴. تنظیمات پیشرفته

### ۴.۱. اصلاح نمایش در مرورگر
```css
body {
    -webkit-font-smoothing: antialiased;  /* بهتر برای macOS */
    -moz-osx-font-smoothing: grayscale;   /* بهتر برای Firefox macOS */
    text-rendering: optimizeLegibility;   /* برای نمایش زیباتر */
    font-feature-settings: "kern" 1;      /* کرنینگ بهتر */
}
```

### ۴.۲. تنظیم اعداد فارسی
```css
/* اگر فونت شما اعداد فارسی را در unicode-range متفاوتی دارد: */
@font-face {
    font-family: 'MyFont';
    src: url('myfont.woff2') format('woff2');
    unicode-range: U+06F0-06F9; /* فقط اعداد فارسی ۰-۹ */
}

/* برای اعمال اعداد فارسی در المان‌های خاص: */
.persian-numbers {
    font-variant-numeric: traditional-nums;  /* اعداد قدیمی/سنتی */
    -moz-font-feature-settings: "anum";
    -webkit-font-feature-settings: "anum";
    font-feature-settings: "anum";
}
```

---

## ۵. چک‌لیست نهایی پیاده‌سازی

- [ ] فونت‌ها به WOFF2 تبدیل شده‌اند
- [ ] @font-face شامل `font-display: swap` است
- [ ] `unicode-range` تنظیم شده (برای جلوگیری از لود اضافی)
- [ ] fallback stack کامل تعریف شده
- [ ] `preload` در HTML اضافه شده
- [ ] تست در Chrome, Firefox, Safari
- [ ] بررسی Lighthouse برای فونت‌ها
- [ ] اعداد فارسی در جای درست نمایش داده می‌شوند