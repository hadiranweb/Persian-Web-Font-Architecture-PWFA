#!/bin/bash
# ================================================================
# Persian Web Font Architecture™ — Convert to WOFF2
# تبدیل فونت TTF/OTF به WOFF2 با فشرده‌سازی بهینه
# ================================================================
# Usage:
#   ./convert-to-woff2.sh font.ttf
#   ./convert-to-woff2.sh font.ttf -o ./optimized/
#   ./convert-to-woff2.sh --input-dir ./fonts/ --output-dir ./woff2/
# ================================================================

set -e

SCRIPT_NAME="PWFA Converter"
VERSION="1.0.0"

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

print_usage() {
    echo "Usage:"
    echo "  $0 <font.ttf>                   Convert single font"
    echo "  $0 <font.ttf> -o <output_dir>   Convert to specific directory"
    echo "  $0 --input-dir <dir> --output-dir <dir>   Batch convert"
    echo "  $0 --help                       Show this help"
}

# Check dependencies
check_deps() {
    if ! command -v woff2_compress &> /dev/null; then
        echo -e "${YELLOW}⚠️  woff2_compress not found.${NC}"
        echo "   Install: sudo apt-get install woff2"
        echo "   Or: brew install woff2"
        echo "   Falling back to fonttools (Python)..."
        
        if ! python3 -c "from fontTools.ttLib import TTFont" 2>/dev/null; then
            echo -e "${RED}❌ fonttools not available either.${NC}"
            echo "   Install: pip install fonttools"
            exit 1
        fi
        return 1
    fi
    return 0
}

# Convert using woff2_compress
convert_with_woff2() {
    local input="$1"
    local output="$2"
    
    local tmp_dir=$(mktemp -d)
    local tmp_woff2="$tmp_dir/$(basename "$input" | sed 's/\.ttf$//;s/\.otf$//').woff2"
    
    # woff2_compress outputs next to the input file
    cp "$input" "$tmp_dir/"
    local tmp_input="$tmp_dir/$(basename "$input")"
    
    woff2_compress "$tmp_input" > /dev/null 2>&1
    
    # Find generated woff2
    local generated=$(find "$tmp_dir" -name "*.woff2" 2>/dev/null | head -1)
    if [ -n "$generated" ]; then
        mv "$generated" "$output"
        rm -rf "$tmp_dir"
        return 0
    fi
    
    rm -rf "$tmp_dir"
    return 1
}

# Convert using Python fonttools fallback
convert_with_fonttools() {
    local input="$1"
    local output="$2"
    
    python3 -c "
from fontTools.ttLib import TTFont
font = TTFont('$input')
font.flavor = 'woff2'
font.save('$output')
"
}

# Main conversion
convert_font() {
    local input="$1"
    local output_dir="$2"
    
    local filename=$(basename "$input")
    local basename="${filename%.*}"
    local output="$output_dir/$basename.woff2"
    
    echo -e "${BLUE}   Converting:${NC} $filename"
    
    local original_size=$(stat -f%z "$input" 2>/dev/null || stat --format=%s "$input" 2>/dev/null)
    
    # Try woff2_compress first, fallback to fonttools
    if command -v woff2_compress &> /dev/null; then
        convert_with_woff2 "$input" "$output"
    else
        convert_with_fonttools "$input" "$output"
    fi
    
    if [ -f "$output" ]; then
        local new_size=$(stat -f%z "$output" 2>/dev/null || stat --format=%s "$output" 2>/dev/null)
        local saved=$(( (original_size - new_size) * 100 / original_size ))
        local original_kb=$(( original_size / 1024 ))
        local new_kb=$(( new_size / 1024 ))
        
        echo -e "   ${GREEN}✅${NC} $basename.woff2"
        echo -e "      ${original_kb}KB → ${new_kb}KB (${saved}% saved)"
    else
        echo -e "   ${RED}❌ Failed to convert: $filename${NC}"
        return 1
    fi
}

# --- Main ---

# Parse arguments
INPUT=""
OUTPUT_DIR="./fonts/optimized"
INPUT_DIR=""
BATCH=false

while [[ $# -gt 0 ]]; do
    case "$1" in
        --input-dir)
            INPUT_DIR="$2"
            BATCH=true
            shift 2
            ;;
        --output-dir|-o)
            OUTPUT_DIR="$2"
            shift 2
            ;;
        --help|-h)
            print_usage
            exit 0
            ;;
        --version|-v)
            echo "$SCRIPT_NAME v$VERSION"
            exit 0
            ;;
        *)
            if [ -z "$INPUT" ]; then
                INPUT="$1"
            fi
            shift
            ;;
    esac
done

echo ""
echo -e "${BLUE}==================================================${NC}"
echo -e "${BLUE}  $SCRIPT_NAME${NC}"
echo -e "${BLUE}==================================================${NC}"

check_deps
mkdir -p "$OUTPUT_DIR"

if [ "$BATCH" = true ] && [ -n "$INPUT_DIR" ]; then
    echo -e "\n${YELLOW}   Batch converting: $INPUT_DIR → $OUTPUT_DIR${NC}"
    count=0
    for font in "$INPUT_DIR"/*.ttf "$INPUT_DIR"/*.otf; do
        if [ -f "$font" ]; then
            convert_font "$font" "$OUTPUT_DIR"
            count=$((count + 1))
        fi
    done
    echo -e "\n${GREEN}   ✅ Converted $count fonts${NC}"
    
elif [ -n "$INPUT" ]; then
    convert_font "$INPUT" "$OUTPUT_DIR"
else
    echo -e "${RED}❌ No input file specified${NC}"
    print_usage
    exit 1
fi

echo -e "${BLUE}==================================================${NC}"
echo ""