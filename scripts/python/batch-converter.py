#!/usr/bin/env python3
"""
Persian Web Font Architecture™ — Batch Font Converter
تبدیل دسته‌ای فونت‌ها با اعمال پاشلاین کامل

Usage:
    python batch-converter.py --input-dir ./fonts/raw/ --output-dir ./fonts/build/ --lang fa
    python batch-converter.py --input font.ttf --output-dir ./optimized/ --preset persian-blog
"""

import sys
import os
import subprocess
import argparse
import glob
from pathlib import Path

def run_analyzer(font_path):
    """Run font-analyzer.py and get JSON output."""
    analyzer = os.path.join(os.path.dirname(__file__), "font-analyzer.py")
    if not os.path.exists(analyzer):
        print("   ⚠️  Analyzer not found, skipping analysis")
        return {}
    
    result = subprocess.run(
        ["python", analyzer, font_path, "--json"],
        capture_output=True, text=True
    )
    try:
        return json.loads(result.stdout)
    except:
        return {}

def run_subsetter(font_path, output_path, lang, preset=None):
    """Run subsetter.py to create subset."""
    subsetter = os.path.join(os.path.dirname(__file__), "subsetter.py")
    if not os.path.exists(subsetter):
        print("   ⚠️  Subsetter not found, skipping subsetting")
        return font_path  # Return original
    
    cmd = ["python", subsetter, font_path, "-o", output_path, "--lang", lang]
    if preset:
        cmd.extend(["--preset", preset])
    
    subprocess.run(cmd, check=True)
    return output_path

def convert_to_woff2(input_path, output_dir):
    """Convert TTF to WOFF2 using system woff2_compress."""
    output_name = Path(input_path).stem + ".woff2"
    output_path = os.path.join(output_dir, output_name)
    
    # Try woff2_compress
    try:
        if sys.platform == "win32":
            # Assume woff2_compress.exe in PATH
            subprocess.run(["woff2_compress", input_path], check=True, capture_output=True)
            # woff2_compress creates file next to input
            generated = input_path.replace(".ttf", ".woff2")
            if os.path.exists(generated):
                os.rename(generated, output_path)
        else:
            subprocess.run(["woff2_compress", input_path], check=True, capture_output=True)
            generated = input_path.replace(".ttf", ".woff2")
            if os.path.exists(generated):
                os.rename(generated, output_path)
    except:
        # Fallback: use Python fonttools
        from fontTools.ttLib import TTFont
        font = TTFont(input_path)
        font.flavor = 'woff2'
        font.save(output_path)
        print("   ℹ️  Used fonttools (woff2_compress not available)")
    
    return output_path

def convert_all(input_dir, output_dir, lang, preset=None):
    """Convert all TTF files in a directory."""
    os.makedirs(output_dir, exist_ok=True)
    
    ttf_files = glob.glob(os.path.join(input_dir, "*.ttf")) + \
                glob.glob(os.path.join(input_dir, "*.otf"))
    
    results = []
    for font_path in sorted(ttf_files):
        name = os.path.basename(font_path)
        print(f"\n   Processing: {name}")
        
        # Step 1: Analyze
        print(f"   ├─ Analyze...")
        analysis = run_analyzer(font_path)
        if analysis:
            print(f"   │  {analysis.get('glyph_count', '?')} glyphs, {analysis.get('size_kb', '?')} KB")
        
        # Step 2: Subset
        subset_path = os.path.join(output_dir, f"{Path(name).stem}-subset.ttf")
        print(f"   ├─ Subsetting ({lang})...")
        subset_path = run_subsetter(font_path, subset_path, lang, preset)
        
        # Step 3: Convert to WOFF2
        print(f"   └─ Converting to WOFF2...")
        woff2_path = convert_to_woff2(subset_path, output_dir)
        
        # Cleanup intermediate subset
        if subset_path != font_path and os.path.exists(subset_path):
            os.remove(subset_path)
        
        woff2_size = os.path.getsize(woff2_path) / 1024
        print(f"      ✅ {Path(woff2_path).name} ({woff2_size:.1f} KB)")
        results.append(woff2_path)
    
    return results

def main():
    parser = argparse.ArgumentParser(description="PWFA Batch Font Converter")
    parser.add_argument("--input-dir", help="Input directory with TTF/OTF files")
    parser.add_argument("--input", help="Single input font file")
    parser.add_argument("-o", "--output-dir", default="./fonts/optimized", help="Output directory")
    parser.add_argument("--lang", default="fa", help="Language for subsetting")
    parser.add_argument("--preset", help="Preset for subsetting")
    
    args = parser.parse_args()
    
    print(f"\n{'='*50}")
    print(f"  Persian Web Font Architecture™ — Batch Converter")
    print(f"{'='*50}")
    
    if args.input:
        # Single file mode
        os.makedirs(args.output_dir, exist_ok=True)
        subset_path = os.path.join(args.output_dir, f"{Path(args.input).stem}-subset.ttf")
        
        print(f"\n   File: {args.input}")
        print(f"   ├─ Subsetting...")
        subset_path = run_subsetter(args.input, subset_path, args.lang, args.preset)
        print(f"   └─ Converting...")
        woff2_path = convert_to_woff2(subset_path, args.output_dir)
        if os.path.exists(subset_path):
            os.remove(subset_path)
        print(f"      ✅ {Path(woff2_path).name}")
        
    elif args.input_dir:
        results = convert_all(args.input_dir, args.output_dir, args.lang, args.preset)
        print(f"\n{'='*50}")
        print(f"  ✅ Converted {len(results)} fonts")
        
    else:
        print("Error: Specify --input or --input-dir")
        sys.exit(1)
    
    print(f"{'='*50}")

if __name__ == "__main__":
    import json
    main()