# عیب‌یابی مشکلات رایج فونت فارسی در وب

---

## ❌ مشکل ۱: فونت لود نمی‌شود (404)

**علت:** مسیر فایل اشتباه است

```css
/* ❌ اشتباه */
src: url('fonts/font.woff2');

/* ✅ درست (مسیر نسبی به CSS) */
src: url('../fonts/font.woff2');

/* ✅ یا مسیر absolute */
src: url('/assets/fonts/font.woff2');
```

---

## ❌ مشکل ۲: متن نامرئی می‌ماند (FOIT)

**علت:** font-display پیش‌فرض = block (متن تا ۳ ثانیه نامرئی)

```css
/* ❌ پیش‌فرض (بد) */
@font-face {
    src: url('font.woff2');
    /* font-display: block است */
}

/* ✅ درست */
@font-face {
    src: url('font.woff2');
    font-display: swap;  /* متن بلافاصله با fallback نمایش داده شود */
}
```

---

## ❌ مشکل ۳: اعداد فارسی به لاتین نمایش داده می‌شوند

**علت:** فونت فعلی گلیف عدد فارسی ندارد

```css
/* ✅ راه‌حل: استفاده از فونت مجزا برای اعداد */
@font-face {
    font-family: 'PersianNumbers';
    src: url('font-numbers.woff2') format('woff2');
    unicode-range: U+06F0-06F9;  /* فقط اعداد فارسی */
}

.persian-number {
    font-family: 'PersianNumbers', inherit;
}

/* ✅ یا استفاده از font-variant-numeric */
.persian-numbers {
    font-variant-numeric: traditional-nums;
}
```

---

## ❌ مشکل ۴: فاصله خطوط نامنظم است

**علت:** نبود hinting در فونت + عدم تطابق size-adjust

```css
/* ✅ راه‌حل: تنظیم size-adjust */
@font-face {
    font-family: 'MyFont';
    src: url('font.woff2') format('woff2');
    size-adjust: 95%;  /* تنظیم نسبت اندازه با fallback */
}
```

---

## ❌ مشکل ۵: فونت در مرورگر سافاری کار نمی‌کند

**علت:** Safari نیاز به فرمت‌های بیشتر دارد

```css
/* ✅ راه‌حل: ارائه چند فرمت */
@font-face {
    font-family: 'MyFont';
    src: url('font.woff2') format('woff2'),
         url('font.woff') format('woff');  /* Safari fallback */
    font-display: swap;
}
```

---

## ❌ مشکل ۶: حجم فونت بالا و لود کند

**علت:** عدم زیرمجموعه‌سازی

```bash
# ✅ راه‌حل: Subsetting
python scripts/python/subsetter.py font.ttf --lang fa -o font-fa.ttf
# حجم از ۴۸۰KB → ۲۸KB

# سپس تبدیل به WOFF2
woff2_compress font-fa.ttf
# حجم نهایی: ~۱۸KB
```

---

## ❌ مشکل ۷: تغییر ظاهر فونت بعد از لود (Layout Shift)

**علت:** تفاوت اندازه فونت اصلی و fallback

```css
/* ✅ راه‌حل: size-adjust */
@font-face {
    font-family: 'MyFont';
    src: url('font.woff2');
    size-adjust: 90%;
}

/* ✅ تنظیم fallback با ارتفاع یکسان */
body {
    font-family: 'MyFont', Tahoma, sans-serif;
    /* از Tahoma استفاده کنید که به فونت فارسی نزدیک‌تر است */
}
```

---

## ❌ مشکل ۸: اعراب (حرکات) درست نمایش داده نمی‌شوند

**علت:** از بین رفتن GSUB Table در Subsetting

```bash
# ❌ اشتباه: حذف layout-features
pyftsubset font.ttf --unicodes="..." -o bad.ttf

# ✅ درست: نگه‌داشتن layout-features
pyftsubset font.ttf \
  --unicodes="..." \
  --layout-features='*' \
  -o good.ttf
```

---

## 🔧 ابزارهای تشخیص سریع

| ابزار | کاربرد |
|---|---|
| Chrome DevTools → Network | بررسی لود فونت (status, size, timing) |
| Chrome DevTools → Coverage | مشاهده گلیف‌های استفاده‌شده |
| Lighthouse → Font Display | بررسی font-display تنظیمات |
| pwfa font-analyzer.py | تحلیل ساختار فونت |
| pwfa optimize-all.sh | پاشلاین کامل عیب‌زدایی |