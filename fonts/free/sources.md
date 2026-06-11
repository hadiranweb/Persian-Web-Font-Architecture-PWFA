# 📦 منابع فونت‌های آزاد فارسی (Free/Libre Fonts)

> کلیه فونت‌های زیر دارای لایسنس آزاد (SIL OFL / GPL / CC) هستند.  
> می‌توانید آزادانه در پروژه‌های تجاری و غیرتجاری استفاده کنید.

---

## ✅ فونت‌های پیشنهادی برای وب

### ۱. Vazirmatn ⭐ — بهترین برای متن بلند
| مورد | توضیح |
|---|---|
| **وب‌سایت** | [github.com/rastikerdar/vazirmatn](https://github.com/rastikerdar/vazirmatn) |
| **لایسنس** | SIL Open Font License 1.1 |
| **وزن‌ها** | Thin تا Black (۹ وزن) |
| **ویژگی** | عالی برای بدنه، نسخه Vazirmatn FD با اعداد فارسی |
| **حجم بهینه** | ~۱۸KB برای WOFF2 Subset |

### ۲. Vazir Code — مخصوص کد و ترمینال
| مورد | توضیح |
|---|---|
| **وب‌سایت** | [github.com/rastikerdar/vazir-code-font](https://github.com/rastikerdar/vazir-code-font) |
| **لایسنس** | SIL OFL |
| **ویژگی** | فونت Monospace فارسی |

### ۳. Samim
| مورد | توضیح |
|---|---|
| **وب‌سایت** | [github.com/rastikerdar/samim-font](https://github.com/rastikerdar/samim-font) |
| **لایسنس** | SIL OFL |
| **وزن‌ها** | ۳ وزن |

### ۴. Shabnam
| مورد | توضیح |
|---|---|
| **وب‌سایت** | [github.com/rastikerdar/shabnam-font](https://github.com/rastikerdar/shabnam-font) |
| **لایسنس** | SIL OFL |
| **وزن‌ها** | ۶ وزن |

### ۵. Parastoo
| مورد | توضیح |
|---|---|
| **وب‌سایت** | [github.com/rastikerdar/parastoo-font](https://github.com/rastikerdar/parastoo-font) |
| **لایسنس** | SIL OFL |
| **ویژگی** | طراحی لطیف و نرم |

### ۶. Tanha
| مورد | توضیح |
|---|---|
| **وب‌سایت** | [github.com/rastikerdar/tanha-font](https://github.com/rastikerdar/tanha-font) |
| **لایسنس** | SIL OFL |

---

## 🌍 فونت‌های بین‌المللی با پشتیبانی فارسی

### Noto Naskh Arabic (Google)
| مورد | توضیح |
|---|---|
| **وب‌سایت** | [fonts.google.com/noto](https://fonts.google.com/noto) |
| **لایسنس** | SIL OFL |
| **ویژگی** | فونت استاندارد گوگل برای عربی/فارسی |

### Noto Nastaliq Urdu
| مورد | توضیح |
|---|---|
| **وب‌سایت** | [fonts.google.com/noto](https://fonts.google.com/noto) |
| **لایسنس** | SIL OFL |
| **ویژگی** | نستعلیق استاندارد متن‌باز |

---

## ⚠️ فونت‌های تجاری (نیازمند مجوز)

| فونت | منبع |
|---|---|
| **IRANSans** | رایگان برای وب — fontiran.com |
| **IRANyekan** | رایگان برای وب — fontiran.com |
| **B Zar** | IranFont / تایپ فا |
| **B Titr** | IranFont / تایپ فا |
| **IranNastaliq** | رایگان — ایران فونت |

> برای فونت‌های تجاری، فایل اصلی را از صاحب مجوز تهیه کنید و خودتان subset/convert کنید.

---

## 🔧 نحوه استفاده از این فونت‌ها

```bash
# ۱. دانلود از GitHub
git clone https://github.com/rastikerdar/vazirmatn.git

# ۲. زیرمجموعه‌سازی برای فارسی
python scripts/python/subsetter.py vazirmatn/Vazirmatn-Regular.ttf --lang fa -o vazirmatn-fa.ttf

# ۳. تبدیل به WOFF2
bash scripts/bash/convert-to-woff2.sh vazirmatn-fa.ttf -o ./build/

# ۴. استفاده در CSS
@font-face {
    font-family: 'Vazirmatn';
    src: url('./build/vazirmatn-fa.woff2') format('woff2');
    font-display: swap;
}
```