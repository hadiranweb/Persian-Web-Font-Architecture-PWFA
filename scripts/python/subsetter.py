#!/usr/bin/env python3
"""
Persian Web Font Architecture™ — Font Subsetter
زیرمجموعه‌سازی هوشمند فونت بر اساس پروفایل زبان

Usage:
    python subsetter.py input.ttf --lang fa -o output.ttf
    python subsetter.py input.ttf --unicodes "U+0600-06FF" -o output.ttf
    python subsetter.py input.ttf --preset persian-blog -o output.ttf
"""

import sys
import json
import os
import argparse
from fontTools.ttLib import TTFont
from fontTools.subset import Subsetter, Options

# Language profiles
LANGUAGE_PROFILES = {
    "fa": {  # Persian
        "name": "Persian",
        "unicodes": "U+0020-007E,U+00A0-00FF,U+0600-06FF,U+0750-077F,U+08A0-08FF,U+2000-206F,U+FB50-FDFF,U+FE70-FEFF",
        "description": "Persian + Basic Latin + Punctuation"
    },
    "ar": {  # Arabic
        "name": "Arabic",
        "unicodes": "U+0020-007E,U+0600-06FF,U+0750-077F,U+08A0-08FF,U+2000-206F,U+FB50-FDFF,U+FE70-FEFF",
        "description": "Arabic + Basic Latin + Punctuation"
    },
    "ur": {  # Urdu
        "name": "Urdu",
        "unicodes": "U+0020-007E,U+0600-06FF,U+0750-077F,U+08A0-08FF,U+2000-206F,U+FB50-FDFF,U+FE70-FEFF",
        "description": "Urdu + Basic Latin + Punctuation"
    },
    "en": {  # English only
        "name": "English (Latin)",
        "unicodes": "U+0020-007E,U+00A0-00FF,U+2000-206F",
        "description": "Basic Latin + Extended Latin + Punctuation"
    }
}

# Presets (combinations for real use cases)
PRESETS = {
    "persian-blog": {
        "name": "Persian Blog",
        "lang": "fa",
        "description": "بهینه شده برای وبلاگ فارسی (متن بلند)"
    },
    "persian-news": {
        "name": "Persian News",
        "lang": "fa",
        "description": "بهینه شده برای سایت خبری فارسی"
    },
    "arabic-portal": {
        "name": "Arabic Portal",
        "lang": "ar",
        "description": "Optimized for Arabic news portal"
    },
    "bilingual-fa-en": {
        "name": "Bilingual Persian-English",
        "unicodes": "U+0020-007E,U+00A0-00FF,U+0600-06FF,U+0750-077F,U+08A0-08FF,U+2000-206F,U+FB50-FDFF,U+FE70-FEFF",
        "description": "فارسی + انگلیسی کامل"
    }
}

def subset_font(input_path, output_path, unicodes, keep_layout_tables=True):
    """Subset a font to keep only specified Unicode ranges."""
    font = TTFont(input_path)
    
    options = Options()
    options.layout_features = ['*'] if keep_layout_tables else []
    options.name_IDs = ['*']
    options.notdef_outline = True
    options.recalc_bounds = True
    options.canonical_order = True
    
    subsetter = Subsetter(options=options)
    subsetter.populate(unicodes=unicodes)
    subsetter.subset(font)
    
    font.save(output_path)
    
    # Stats
    original_size = os.path.getsize(input_path)
    new_size = os.path.getsize(output_path)
    
    return {
        "input": os.path.basename(input_path),
        "output": os.path.basename(output_path),
        "original_kb": round(original_size / 1024, 1),
        "new_kb": round(new_size / 1024, 1),
        "saved_kb": round((original_size - new_size) / 1024, 1),
        "saved_percent": round((1 - new_size / original_size) * 100, 1)
    }

def main():
    parser = argparse.ArgumentParser(description="PWFA Font Subsetter")
    parser.add_argument("input", help="Input font file (.ttf)")
    parser.add_argument("-o", "--output", default="subset.ttf", help="Output font file")
    parser.add_argument("--lang", help="Language profile (fa, ar, ur, en)")
    parser.add_argument("--unicodes", help="Custom Unicode ranges")
    parser.add_argument("--preset", help="Use a preset configuration")
    parser.add_argument("--no-layout", action="store_true", help="Remove OpenType layout tables (not recommended for Persian/Arabic)")
    
    args = parser.parse_args()
    
    if not os.path.exists(args.input):
        print(f"Error: File not found: {args.input}")
        sys.exit(1)
    
    # Determine Unicode ranges
    unicodes = None
    preset_name = "custom"
    
    if args.preset:
        if args.preset in PRESETS:
            preset = PRESETS[args.preset]
            if "unicodes" in preset:
                unicodes = preset["unicodes"]
            elif "lang" in preset:
                unicodes = LANGUAGE_PROFILES[preset["lang"]]["unicodes"]
            preset_name = preset["name"]
            print(f"   Preset: {preset['name']} — {preset['description']}")
        else:
            print(f"Error: Unknown preset '{args.preset}'")
            print(f"Available: {', '.join(PRESETS.keys())}")
            sys.exit(1)
    elif args.lang:
        if args.lang in LANGUAGE_PROFILES:
            unicodes = LANGUAGE_PROFILES[args.lang]["unicodes"]
            preset_name = LANGUAGE_PROFILES[args.lang]["name"]
            print(f"   Language: {LANGUAGE_PROFILES[args.lang]['name']}")
        else:
            print(f"Error: Unknown language '{args.lang}'")
            sys.exit(1)
    elif args.unicodes:
        unicodes = args.unicodes
    else:
        print("Error: Specify --lang, --preset, or --unicodes")
        sys.exit(1)
    
    print(f"\n{'='*50}")
    print(f"  Persian Web Font Architecture™ — Font Subsetter")
    print(f"{'='*50}")
    
    result = subset_font(args.input, args.output, unicodes, not args.no_layout)
    
    print(f"   Input:     {result['input']} ({result['original_kb']} KB)")
    print(f"   Output:    {result['output']} ({result['new_kb']} KB)")
    print(f"   Saved:     {result['saved_kb']} KB ({result['saved_percent']}%)")
    print(f"{'='*50}")
    print(f"   ✅ Done! File saved to: {args.output}")

if __name__ == "__main__":
    main()