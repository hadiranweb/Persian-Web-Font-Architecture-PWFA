# راهنمای زیرمجموعه‌سازی (Subsetting) فونت فارسی

> کاهش ۹۰٪ حجم فونت با نگه‌داشتن فقط حروف ضروری

---

## ۱. اصل ماجرا: چرا Subsetting انقدر مؤثر است؟

یک فونت فارسی کامل معمولاً شامل **۱۰۰۰ تا ۳۰۰۰ گلیف** است:

```
┌─────────────────────────────────────────┐
│             ۳۰۰۰ گلیف                   │
├─────────────────────────────────────────┤
│  ████████  لاتین (Basic + Extended)     │ ~۴۰۰ گلیف
│  ████████  فارسی/عربی                   │ ~۲۰۰ گلیف
│  ████████  عربی گسترده (تفسیری)         │ ~۳۰۰ گلیف
│  ████████  علائم و نشانه‌ها              │ ~۲۰۰ گلیف
│  ████████  گلیف‌های تکراری/قدیمی         │ ~۵۰۰ گلیف
│  ████████  گلیف‌های زبان‌های دیگر        │ ~۱۰۰۰ گلیف
│  ████████  گلیف‌های CJK/غیره             │ ~۴۰۰ گلیف
└─────────────────────────────────────────┘

✅ بعد از Subsetting برای فارسی:
┌──────────────────┐
│   ~۲۰۰ گلیف      │ ← فقط حروف واقعی مورد نیاز
└──────────────────┘
```

---

## ۲. Unicode Range فارسی

حروف فارسی در این محدوده‌ها قرار دارند:

| محدوده | نام | توضیح |
|---|---|---|
| `U+0020-007E` | Basic Latin | فاصله، اعداد انگلیسی، نقطه‌گذاری |
| `U+00A0-00FF` | Latin-1 Supplement | علائم اضافه |
| `U+0600-06FF` | Arabic | **هسته اصلی فارسی و عربی** |
| `U+FB50-FDFF` | Arabic PF-A | اشکال مختلف حروف عربی |
| `U+FE70-FEFF` | Arabic PF-B | اشکال منفصل حروف |
| `U+2000-206F` | General Punctuation | خط تیره، گیومه، نیم‌فاصله |

### حروف ضروری فارسی (حدود ۲۰۰ گلیف)

```
آ ا ب پ ت ث ج چ ح خ د ذ ر ز ژ س ش ص ض ط ظ ع غ ف ق ک گ ل م ن و ه ی
٠ ١ ٢ ٣ ٤ ٥ ٦ ٧ ٨ ٩
، ! ؟ . « » ( ) [ ] - ً ٌ ٍ َ ُ ِ ّ ْ
ء أ إ ؤ ئ ء
۰ ۱ ۲ ۳ ۴ ۵ ۶ ۷ ۸ ۹
```

---

## ۳. دستورات عملی Subsetting

### با fonttools (پیشنهادی)
```bash
# نصب
pip install fonttools brotli

# زیرمجموعه‌سازی برای فارسی
pyftsubset font.ttf \
  --unicodes="U+0020-007E,U+0600-06FF,U+FB50-FDFF,U+FE70-FEFF,U+2000-206F" \
  --layout-features='*' \
  --glyph-names \
  --symbol-cmap \
  --legacy-cmap \
  --notdef-outline \
  --recommended-glyphs \
  --output-file=font-fa.ttf
```

### با اسکریپت PWFA
```bash
python scripts/python/subsetter.py font.ttf --lang fa -o font-fa.ttf

# با پریست وبلاگ فارسی
python scripts/python/subsetter.py font.ttf --preset persian-blog -o font-fa.ttf
```

---

## ۴. Subsetting با Glyphhanger (Node.js)

```bash
# نصب
npm install -g glyphhanger

# استفاده (بر اساس محتوای HTML واقعی)
glyphhanger http://example.com --subset=*.ttf --formats=woff2,woff

# یا بر اساس فایل متنی
glyphhanger --string="متن فارسی نمونه" --subset=font.ttf --formats=woff2
```

---

## ۵. چک‌لیست

- [ ] فقط حروف فارسی + اعداد نگه داشته شود
- [ ] ویژگی‌های OpenType (GSUB, GPOS) حفظ شود
- [ ] حتماً گلیف notdef (□) نگه داشته شود
- [ ] خروجی WOFF2 شود
- [ ] نتیجه نهایی < ۲۰KB

---

> 💡 **نکته:** اگر فونت فارسی شما پس از subsetting اعراب (حرکات) را درست نمایش نمی‌دهد، حتماً `--layout-features='*'` را اضافه کنید تا GSUB/GPOS Tables حفظ شوند.