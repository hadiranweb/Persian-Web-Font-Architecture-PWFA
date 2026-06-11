#!/usr/bin/env python3
"""
Persian Web Font Architecture™ — Font Analyzer
تحلیل فونت و استخراج اطلاعات برای بهینه‌سازی

Usage:
    python font-analyzer.py path/to/font.ttf
    python font-analyzer.py path/to/font.ttf --json
"""

import sys
import json
import os
from fontTools.ttLib import TTFont
from fontTools.unicode import Unicode

def analyze_font(font_path):
    """Analyze a font file and return structured information."""
    font = TTFont(font_path)
    
    # Basic info
    name_table = font['name']
    font_name = ""
    for record in name_table.names:
        if record.nameID == 1 and record.platformID == 3:
            font_name = record.toUnicode()
            break
    
    # File size
    file_size = os.path.getsize(font_path)
    
    # Glyph count
    glyph_count = font.getMaxpTable().numGlyphs
    
    # Unicode ranges
    try:
        cmap = font.getBestCmap()
        unicode_ranges = set()
        for code in cmap.keys():
            cat = Unicode[code]
            if cat:
                unicode_ranges.add(cat)
    except:
        unicode_ranges = {"unknown"}
    
    # Tables present
    tables = list(font.keys())
    
    # Language coverage estimation (simplified)
    persian_chars = set(range(0x0600, 0x06FF)) | set(range(0xFB50, 0xFDFF)) | set(range(0xFE70, 0xFEFF))
    latin_chars = set(range(0x0020, 0x007E)) | set(range(0x00A0, 0x00FF))
    
    persian_coverage = sum(1 for c in persian_chars if c in cmap) / len(persian_chars) if persian_chars else 0
    latin_coverage = sum(1 for c in latin_chars if c in cmap) / len(latin_chars) if latin_chars else 0
    
    return {
        "file": os.path.basename(font_path),
        "font_name": font_name,
        "size_bytes": file_size,
        "size_kb": round(file_size / 1024, 1),
        "glyph_count": glyph_count,
        "tables": tables,
        "unicode_ranges": sorted(unicode_ranges),
        "coverage": {
            "persian": round(persian_coverage * 100, 1),
            "latin": round(latin_coverage * 100, 1),
        },
        "estimated_subset_size_kb": round((file_size / 1024) * (200 / glyph_count) if glyph_count > 200 else (file_size / 1024), 1),
        "is_subsettable": glyph_count > 200
    }

def main():
    if len(sys.argv) < 2:
        print("Usage: python font-analyzer.py <font.ttf> [--json]")
        sys.exit(1)
    
    font_path = sys.argv[1]
    use_json = "--json" in sys.argv
    
    if not os.path.exists(font_path):
        print(f"Error: File not found: {font_path}")
        sys.exit(1)
    
    result = analyze_font(font_path)
    
    if use_json:
        print(json.dumps(result, indent=2, ensure_ascii=False))
    else:
        print(f"\n{'='*50}")
        print(f"  Persian Web Font Architecture™ — Font Analyzer")
        print(f"{'='*50}")
        print(f"  Font:          {result['font_name']}")
        print(f"  File:          {result['file']}")
        print(f"  Size:          {result['size_kb']} KB ({result['size_bytes']} bytes)")
        print(f"  Glyphs:        {result['glyph_count']}")
        print(f"  Tables:        {', '.join(result['tables'][:10])}...")
        print(f"  Unicode Ranges:{', '.join(list(result['unicode_ranges'])[:5])}...")
        print(f"  Persian:       {result['coverage']['persian']}%")
        print(f"  Latin:         {result['coverage']['latin']}%")
        print(f"  Est. Subset:   {result['estimated_subset_size_kb']} KB")
        print(f"  Subsettable:   {'✅ Yes' if result['is_subsettable'] else '❌ No (already small)'}")
        print(f"{'='*50}")

if __name__ == "__main__":
    main()