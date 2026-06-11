# 🏛️ Persian Web Font Architecture™ — معماری کامل

> **هدف:** ایجاد یک استاندارد معماری برای بهینه‌سازی فونت وب در زبان‌های غیرلاتین  
> *Creating an architectural standard for non-Latin web font optimization*

---

## ۱. فلسفه معماری (Architecture Philosophy)

این پروژه بر سه اصل استوار است:

### ۱.۱. معماری محور (Architecture-First)
نه یک ابزار، بلکه **یک شبکه معماری** که ابزارها در آن زندگی می‌کنند.  
**مهم نیست از چه زبانی استفاده می‌شود، مهم این است که فرایندها استاندارد باشند.**

### ۱.۲. چندزبانگی ابزاری (Language-Agnostic)
اسکریپت‌ها می‌توانند Python, Node.js, Bash یا هر زبان دیگری باشند.  
معماری باید آنقدر شفاف باشد که هر توسعه‌دهنده‌ای بتواند قطعۀ گمشده را به زبان خودش بنویسد.

### ۱.۳. مقیاس‌پذیری زبانی (Language-Scalable)
طراحی شده برای گسترش به همه زبان‌های غیرلاتین. افزودن یک زبان جدید = افزودن یک پریست، نه بازنویسی معماری.

---

## ۲. لایه‌های معماری (Architecture Layers)

```
LAYER 0: Font Source (ورودی)
│
├── TTF / OTF Raw Files
├── Metadata: نام، وزن، استایل، مجوز
└── زبان / Unicode Range
│
▼
LAYER 1: Analysis (تحلیل)
│
├── حجم فایل (KB/MB)
├── تعداد گلیف‌ها
├── Unicode Range Coverage
├── جدول‌های OpenType موجود
└── گزارش مجوز (License Check)
│
▼
LAYER 2: Subsetting (زیرمجموعه‌سازی)
│
├── نگاشت زبان → Unicode Range
├── حذف گلیف‌های غیرضروری
│   ├── Latin extras (برای فونت فارسی)
│   ├── Arabic extras (برای فونت لاتین)
│   └── Ideograms (برای CJK)
└── حفظ ویژگی‌های OpenType ضروری
│
▼
LAYER 3: Conversion (تبدیل)
│
├── TTF → WOFF2
├── TTF → Zopfli WOFF
├── TTF → EOT (IE Legacy)
└── TTF → SVG Font (Legacy)
│
▼
LAYER 4: CSS Generation (تولید CSS)
│
├── @font-face با format های مختلف
├── font-display: swap / optional
├── unicode-range برای زبان خاص
├── preload hints
└── fallback stack
│
▼
LAYER 5: Delivery (تحویل)
│
├── self-hosted
│   ├── CDN-ready
│   └── Cache stratégie
├── Google Fonts-like API (اختیاری)
└── Service Worker Cache
```

---

## ۳. پروفایل زبان (Language Profile)

هر زبان یک **پروفایل** دارد که تعیین می‌کند Subsetting چگونه انجام شود:

```json
{
  "language": "Persian",
  "code": "fa",
  "script": "Arabic",
  "unicode_ranges": [
    {"name": "Arabic", "range": "U+0600–U+06FF"},
    {"name": "Arabic Supplement", "range": "U+0750–U+077F"},
    {"name": "Arabic Extended-A", "range": "U+08A0–U+08FF"},
    {"name": "Basic Latin", "range": "U+0020–U+007E"},
    {"name": "Latin-1 Supplement", "range": "U+00A0–U+00FF"},
    {"name": "General Punctuation", "range": "U+2000–U+206F"},
    {"name": "Arabic Presentation Forms", "range": "U+FB50–U+FDFF"},
    {"name": "Arabic PF-A", "range": "U+FE70–U+FEFF"}
  ],
  "glyph_count_estimate": 200,
  "priority_glyphs": ["آ", "ا", "ب", "پ", "ت", "ث", "ج", "چ", "ح", "خ", "د", "ذ", "ر", "ز", "ژ", "س", "ش", "ص", "ض", "ط", "ظ", "ع", "غ", "ف", "ق", "ک", "گ", "ل", "م", "ن", "و", "ه", "ی"],
  "special_features": ["init", "medi", "fina", "isol", "rlig", "calt"]
}
```

### زبان‌های پشتیبانی‌شده

| زبان | کد | اسکریپت | Unicode Range اصلی | وضعیت |
|---|---|---|---|---|
| فارسی | fa | Arabic | U+0600–06FF, U+FB50–FDFF | ✅ |
| عربی | ar | Arabic | U+0600–06FF, U+0750–077F | 🔄 |
| اردو | ur | Arabic (Nastaliq) | U+0600–06FF, U+FB50–FDFF | 🔄 |
| کردی | ku | Arabic | U+0600–06FF | 🔄 |
| پشتو | ps | Arabic | U+0600–06FF | 🔄 |

---

## ۴. پاشلاین کامل (Full Pipeline)

### ۴.۱. حالت دستی (Manual)
```
Input TTF
  → 1. font-analyzer.py (تحلیل)
  → 2. subsetter.py (زیرمجموعه‌سازی با پروفایل زبان)
  → 3. convert-to-woff2.sh (تبدیل)
  → 4. قالب CSS (تولید @font-face)
  → 5. تست در مرورگر
```

### ۴.۲. حالت خودکار (Automated)
```bash
# یک دستور برای همه چیز
bash optimize-all.sh font.ttf --lang fa --output ./build/
```

### ۴.۳. حالت CI/CD
```yaml
# GitHub Actions / GitLab CI
jobs:
  font-optimize:
    steps:
      - run: pip install fonttools brotli
      - run: python scripts/python/subsetter.py --lang fa
      - run: bash scripts/bash/convert-to-woff2.sh
      - run: npm run test-font-metrics
```

---

## ۵. تصمیمات معماری (Architecture Decision Log)

| ADL | تصمیم | دلیل |
|---|---|---|
| ADL-001 | WOFF2 فرمت اصلی باشد | بهترین فشرده‌سازی، پشتیبانی ۹۶٪ مرورگرها |
| ADL-002 | Subsetting اجباری باشد | کاهش ۶۰-۸۰٪ حجم برای فونت فارسی |
| ADL-003 | font-display: swap | جلوگیری از FOIT و بهبود LCP |
| ADL-004 | Python زبان اصلی اتوماسیون | fonttools بالغ‌ترین کتابخانه |
| ADL-005 | Bash برای کمندهای ساده | بدون وابستگی، همه‌جا موجود |
| ADL-006 | پروفایل زبان در JSON | قابل گسترش بدون تغییر کد |
| ADL-007 | CI/CD اجباری | تضمین کیفیر خروجی |

---

## ۶. مقایسه ابزارها (Tool Comparison)

| ابزار | کاربرد | مزایا | معایب |
|---|---|---|---|
| **fonttools** | Subsetting, Analysis | کامل‌ترین، Python | نیاز به یادگیری CLI |
| **woff2** | تبدیل فرمت | سریع، استاندارد | فقط تبدیل |
| **brotli** | فشرده‌سازی بخش WOFF2 | فشرده‌سازی بالا | Embedded در woff2 |
| **glyphhanger** | Subsetting هوشمند | خودکار، عالی | وابستگی به Node |
| **fontforge** | ویرایش دستی | قدرتمند | GUI/Scripting |

---

## ۷. شاخص‌های کلیدی عملکرد (KPIs)

| متریک | هدف | ابزار اندازه‌گیری |
|---|---|---|
| حجم فونت WOFF2 | < ۲۰KB برای فارسی | ls -lh / woff2 info |
| زمان لود | < ۱۰۰ms | Lighthouse / WebPageTest |
| FOUT时长 | < ۲۰۰ms | font-display: swap |
| CLS | < 0.1 | Lighthouse |
| پشتیبانی مرورگر | > ۹۵٪ | caniuse.com |

---

## ۸. دیاگرام جریان داده (Data Flow)

```
[TFF Raw] ──→ [Analyzer] ──→ [Profile Matcher] ──→ [Subsetter] ──→ [Converter] ──→ [CSS Gen] ──→ [CDN]
   ↑              ↑                  ↑                   ↑               ↑               ↑
   │              │                  │                   │               │               │
   ├─ font.ttf    ├─ report.json     ├─ lang-profile     ├─ subset.ttf   ├─ font.woff2   ├─ style.css
   └─ font.otf    └─ metrics.json    └─ unicode-range    └─ subset.ufo   └─ font.woff    └─ preload.html
```

---

*Persian Web Font Architecture™ — Architecture Document v1.0*