# 🔄 Pipeline — پاشلاین بهینه‌سازی فونت

> راهنمای گام‌به‌گام برای بهینه‌سازی یک فونت وب از صفر تا صد

---

## 🚀 مسیر سریع (Express Path)

```bash
# ۱. تحلیل فونت
python scripts/python/font-analyzer.py fonts/input/myfont.ttf

# ۲. زیرمجموعه‌سازی برای فارسی
python scripts/python/subsetter.py fonts/input/myfont.ttf --lang fa -o fonts/subset/

# ۳. تبدیل به WOFF2
bash scripts/bash/convert-to-woff2.sh fonts/subset/myfont-subset.ttf -o fonts/optimized/

# ۴. تولید CSS
# از قالب css/templates/font-face-base.css استفاده کنید

# ۵. تست
open examples/persian-text.html
```

---

## 📋 گام ۱: تحلیل فونت (Analysis)

### دستور
```bash
python scripts/python/font-analyzer.py path/to/font.ttf
```

### خروجی
```json
{
  "file": "font.ttf",
  "size_kb": 245,
  "glyph_count": 1250,
  "tables": ["cmap", "head", "hhea", "hmtx", "name", "OS/2", "post", "GSUB", "GPOS", "glyf", "loca"],
  "unicode_ranges": ["Basic Latin", "Arabic", "Latin-1 Supplement", "Arabic Presentation Forms"],
  "language_coverage": {
    "Persian": 0.95,
    "Arabic": 0.90,
    "English": 0.85
  },
  "license": "SIL Open Font License 1.1",
  "is_subsettable": true,
  "estimated_subset_size_kb": 35
}
```

---

## 📋 گام ۲: زیرمجموعه‌سازی (Subsetting)

### اصول
- برای فونت فارسی: ~۲۰۰ گلیف کافی است (به جای ۱۰۰۰+)
- فقط گلیف‌های مربوط به Unicode Range زبان هدف نگه داشته شود
- ویژگی‌های OpenType (GSUB, GPOS) حتماً حفظ شوند

### دستور
```bash
# زیرمجموعه‌سازی ساده
python scripts/python/subsetter.py font.ttf --lang fa -o subset.ttf

# با تعریف دستی Unicode Range
python scripts/python/subsetter.py font.ttf \
  --unicodes "U+0020-007E,U+0600-06FF,U+FB50-FDFF,U+FE70-FEFF" \
  --output-layout-tables \
  -o subset.ttf

# با پریست کامل
python scripts/python/subsetter.py font.ttf --preset persian-blog -o subset.ttf
```

### نتیجه
```
قبل: 245 KB (1250 گلیف)
بعد:  28 KB ( 210 گلیف)
──────────────────────
صرفه‌جویی: ~88٪ حجم
```

---

## 📋 گام ۳: تبدیل به WOFF2 (Conversion)

### دستور
```bash
# تک فایل
bash scripts/bash/convert-to-woff2.sh subset.ttf -o optimized/

# دسته‌ای
bash scripts/bash/convert-to-woff2.sh --input-dir ./subset/ --output-dir ./optimized/

# با بالاترین فشرده‌سازی
woff2_compress subset.ttf  # خروجی: subset.woff2
```

### مقایسه حجم
```
TTF  → WOFF2  = 245 KB →  18 KB  (۹۳٪ کاهش!)
TTF  → WOFF   = 245 KB →  32 KB  (۸۷٪ کاهش)
TTF  → Zopfli = 245 KB →  15 KB  (۹۴٪ کاهش)
```

---

## 📋 گام ۴: تولید CSS (CSS Generation)

### قالب پایه
```css
/* از css/templates/font-face-base.css استفاده کنید */

@font-face {
    font-family: 'FontName';
    src: url('../fonts/optimized/font.woff2') format('woff2'),
         url('../fonts/optimized/font.woff') format('woff');
    font-weight: normal;
    font-style: normal;
    font-display: swap;
    unicode-range: U+0600-06FF, U+FB50-FDFF, U+FE70-FEFF, U+0020-007E;
}
```

---

## 📋 گام ۵: تحویل و بهینه‌سازی نهایی (Delivery)

### Self-Hosted
```html
<link rel="preload" as="font" href="font.woff2" crossorigin>
<link rel="stylesheet" href="css/fonts.css">
```

### CDN
```nginx
# nginx.conf
location /fonts/ {
    add_header Cache-Control "public, max-age=31536000, immutable";
    add_header Access-Control-Allow-Origin "*";
}
```

---

## 📊 چک‌لیست نهایی

- [ ] حجم WOFF2 نهایی < ۲۰KB
- [ ] font-display: swap تنظیم شده
- [ ] preload در HTML اضافه شده
- [ ] unicode-range محدود شده
- [ ] CORS headers برای CDN تنظیم شده
- [ ] Fallback font stack تعریف شده
- [ ] تست در Chrome, Firefox, Safari انجام شده
- [ ] تست Lighthouse با Font Display audit پاس شده

---

*Persian Web Font Architecture™ — Pipeline Document v1.0*