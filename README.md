# 🏛️ Persian Web Font Architecture™ (PWFA)

> **چارچوب معماری بهینه‌سازی فونت وب برای زبان‌های غیرلاتین**  
> *An architectural framework for non-Latin web font optimization*

---

## 🧭 معرفی (Introduction)

**Persian Web Font Architecture™** یک چارچوب معماری (Architecture Framework) است برای **بهینه‌سازی، بسته‌بندی و سرویس‌دهی فونت‌های وب** در زبان‌های غیرلاتین، با تمرکز اولیه بر **فارسی** و قابلیت گسترش به **عربی، اردو، کردی، پشتو و سایر زبان‌ها**.

این پروژه **نرم‌افزار سنگین نیست**، بلکه یک **شبکه معماری (Architecture Network)** است شامل:
- ✅ فرایندها و پاشلاین‌های استاندارد
- ✅ اسکریپت‌های سبک و چندزبانگی (Python, Node, Bash)
- ✅ قالب‌های CSS بهینه
- ✅ مستندات آموزشی و عیب‌یابی
- ✅ فونت‌های آزاد (Free/Libre) + راهنمای فونت‌های تجاری

---

## 📐 معماری کلان (High-Level Architecture)

```
                      ┌─────────────────────────┐
                      │    Source Fonts Layer    │
                      │  (TTF/OTF - ورودی)      │
                      └────────────┬────────────┘
                                   ↓
                      ┌─────────────────────────┐
                      │   Analysis & Profiling   │
                      │  (حجم، گلیف‌ها، مجوز)   │
                      └────────────┬────────────┘
                                   ↓
                      ┌─────────────────────────┐
                      │    Subsetting Layer      │
                      │  (زیرمجموعه‌سازی گلیف)   │
                      └────────────┬────────────┘
                                   ↓
                      ┌─────────────────────────┐
                      │    Conversion Layer      │
                      │  (TTF → WOFF2, Zopfli)  │
                      └────────────┬────────────┘
                                   ↓
                      ┌─────────────────────────┐
                      │   CSS Generation Layer   │
                      │  (font-face @font-face)  │
                      └────────────┬────────────┘
                                   ↓
                      ┌─────────────────────────┐
                      │  Delivery & Cache Layer  │
                      │  (CDN, preload, swap)    │
                      └─────────────────────────┘
```

---

## 📁 ساختار ریپازیتوری (Repository Structure)

```
persian-web-font-architecture/
│
├── README.md                   ← همین فایل
├── LICENSE.md                  ← Fanous Community License
├── ARCHITECTURE.md             ← معماری کامل و تصمیمات فنی
├── PIPELINE.md                 ← پاشلاین گام‌به‌گام
│
├── architecture/               ← دیاگرام‌ها و مدل‌های معماری
│   ├── layers.md
│   ├── decision-log.md
│   └── comparison-matrix.md
│
├── fonts/
│   ├── free/                   ← فونت‌های آزاد (لیسانس آزاد)
│   │   ├── sources.md          ← لیست منابع دانلود
│   │   └── optimized/          ← نسخه‌های بهینه‌شده
│   └── commercial/             ← راهنمای فونت‌های تجاری
│       └── guide.md
│
├── css/
│   ├── templates/              ← قالب‌های آماده @font-face
│   │   ├── font-face-base.css
│   │   ├── font-face-persian.css
│   │   ├── font-face-arabic.css
│   │   └── font-display.css
│   └── examples/               ← نمونه‌های پیاده‌سازی
│       └── persian-text.html
│
├── scripts/
│   ├── python/                 ← اسکریپت‌های Python
│   │   ├── font-analyzer.py
│   │   ├── subsetter.py
│   │   └── batch-converter.py
│   ├── node/                   ← اسکریپت‌های Node.js
│   │   └── font-metrics.js
│   └── bash/                   ← اسکریپت‌های Bash
│       ├── convert-to-woff2.sh
│       └── optimize-all.sh
│
├── templates/
│   ├── .fontconfig             ← قالب تنظیمات
│   └── ci-cd.yml               ← قالب پایپلاین CI/CD
│
├── config/
│   ├── default.toml            ← تنظیمات پیش‌فرض
│   └── presets/                ← پریست‌های آماده
│       ├── persian-blog.toml
│       └── arabic-news.toml
│
├── docs/
│   ├── fa/                     ← مستندات فارسی
│   │   ├── 01-introduction.md
│   │   ├── 02-installation.md
│   │   ├── 03-subsetting.md
│   │   ├── 04-woff2-vs-ttf.md
│   │   ├── 05-best-fonts.md
│   │   ├── 06-troubleshooting.md
│   │   └── 07-advanced.md
│   └── en/                     ← English docs
│       └── (same structure)
│
├── test/
│   ├── fixtures/               ← فونت‌های تست
│   └── expected/               ← خروجی‌های مورد انتظار
│
└── examples/
    ├── persian-blog/           ← نمونه وبلاگ فارسی
    ├── arabic-news/            ← نمونه سایت خبری عربی
    └── multi-language/         ← نمونه چندزبانه
```

---

## 🚀 گام‌های سریع (Quick Start)

### ۱. نصب وابستگی‌ها
```bash
# نصب WOFF2 converter
sudo apt-get install woff2

# نصب fonttools برای subsetting
pip install fonttools brotli zopfli

# یا استفاده از Docker
docker pull pwfa/font-optimizer
```

### ۲. بهینه‌سازی یک فونت
```bash
# با یک دستور
bash scripts/bash/optimize-all.sh input-font.ttf -o output/
```

### ۳. استفاده در CSS
```css
@import url('css/templates/font-face-base.css');

@font-face {
    font-family: 'My Persian Font';
    src: url('fonts/optimized/my-font.woff2') format('woff2');
    font-display: swap;
}
```

---

## 📜 لایسنس

این پروژه تحت **Fanous Community License** منتشر می‌شود.  
مشاهده فایل [LICENSE.md](LICENSE.md) برای جزئیات.

```
Financial Compass 8D™ — Architecture Branch
Crafted by @hadiranweb & Fanous Web 3
```

---

## 🧰 وابستگی‌های فنی (Tech Stack)

| ابزار | کاربرد |
|---|---|
| **Woff2** | تبدیل TTF → WOFF2 |
| **fonttools** | زیرمجموعه‌سازی، تحلیل، تبدیل |
| **Brotli / Zopfli** | فشرده‌سازی بهتر |
| **Python 3+** | اسکریپت‌های اصلی |
| **Bash** | اتوماسیون خط فرمان |
| **Node.js** | ابزارهای جانبی (اختیاری) |
| **Docker** | کانتینریسازی (اختیاری) |

---

## 🌐 زبان‌های پشتیبانی‌شده (Current & Planned)

| وضعیت | زبان | اسکریپت |
|---|---|---|
| ✅ | فارسی (Farsi/Persian) | Arabic-based |
| 🔄 | عربی (Arabic) | Arabic-based |
| 🔄 | اردو (Urdu) | Arabic-based (Nastaliq) |
| 🔄 | کردی (Kurdish) | Arabic-based |
| 🔄 | پشتو (Pashto) | Arabic-based |
| 📋 | روسی (Cyrillic) | Cyrillic |
| 📋 | چینی (Han) | CJK |

> ✅ = کامل | 🔄 = در حال توسعه | 📋 = برنامه آینده

---

## 🤝 مشارکت (Contributing)

این پروژه یک **معماری باز** است. مشارکت به شکل‌های زیر ممکن است:
- افزودن پریست زبان جدید
- بهبود اسکریپت‌ها
- تکمیل مستندات
- گزارش باگ و پیشنهاد

---

*Persian Web Font Architecture™ (PWFA) — © 2026 Hadi Jafari (Fanous Web 3)*