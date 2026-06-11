#!/bin/bash
# ================================================================
# Persian Web Font Architecture™ — Full Optimization Pipeline
# پاشلاین کامل بهینه‌سازی: Analysis → Subset → Convert → Report
# ================================================================
# Usage:
#   ./optimize-all.sh input.ttf --lang fa
#   ./optimize-all.sh input.ttf --preset persian-blog
#   ./optimize-all.sh --input-dir ./raw/ --output-dir ./build/ --lang fa
# ================================================================

set -e

SCRIPT_NAME="PWFA Optimization Pipeline"
VERSION="1.0.0"

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m'

print_banner() {
    echo ""
    echo -e "${BLUE}┌──────────────────────────────────────────────────┐${NC}"
    echo -e "${BLUE}│  ${CYAN}Persian Web Font Architecture™${NC}                ${BLUE}│${NC}"
    echo -e "${BLUE}│  ${YELLOW}Full Optimization Pipeline v${VERSION}${NC}                ${BLUE}│${NC}"
    echo -e "${BLUE}└──────────────────────────────────────────────────┘${NC}"
    echo ""
}

# Find script directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(cd "$SCRIPT_DIR/../.." && pwd)"

run_step() {
    local step_name="$1"
    local cmd="$2"
    
    echo -e "${YELLOW}   ⚙️  $step_name...${NC}"
    
    if eval "$cmd" > /dev/null 2>&1; then
        echo -e "   ${GREEN}   ✅ $step_name completed${NC}"
        return 0
    else
        echo -e "   ${RED}   ❌ $step_name failed${NC}"
        return 1
    fi
}

optimize_font() {
    local input="$1"
    local lang="$2"
    local preset="$3"
    local output_dir="$4"
    
    local filename=$(basename "$input")
    local basename="${filename%.*}"
    
    mkdir -p "$output_dir"
    
    local subset_output="$output_dir/$basename-subset.ttf"
    local woff2_output="$output_dir/$basename.woff2"
    local report_output="$output_dir/$basename-report.json"
    
    # Input size
    local input_size=$(stat -f%z "$input" 2>/dev/null || stat --format=%s "$input" 2>/dev/null)
    local input_kb=$((input_size / 1024))
    
    echo -e "\n${CYAN}   📄 File: $filename (${input_kb}KB)${NC}"
    
    # Step 1: Analyze
    local analyzer="$PROJECT_DIR/scripts/python/font-analyzer.py"
    if [ -f "$analyzer" ]; then
        run_step "Analysis" "python3 '$analyzer' '$input' --json > '$report_output'"
    fi
    
    # Step 2: Subset
    local subsetter="$PROJECT_DIR/scripts/python/subsetter.py"
    if [ -f "$subsetter" ]; then
        local subset_args="--lang $lang"
        [ -n "$preset" ] && subset_args="--preset $preset"
        
        run_step "Subsetting ($lang)" "python3 '$subsetter' '$input' -o '$subset_output' $subset_args"
    else
        subset_output="$input"
    fi
    
    # Step 3: Convert to WOFF2
    local converter="$SCRIPT_DIR/convert-to-woff2.sh"
    if [ -f "$converter" ]; then
        run_step "WOFF2 Conversion" "bash '$converter' '$subset_output' -o '$output_dir'"
    fi
    
    # Final report
    if [ -f "$woff2_output" ]; then
        local final_size=$(stat -f%z "$woff2_output" 2>/dev/null || stat --format=%s "$woff2_output" 2>/dev/null)
        local final_kb=$((final_size / 1024))
        local saved=$(( (input_size - final_size) * 100 / input_size ))
        
        echo -e "\n${GREEN}   📊 Optimization Report:${NC}"
        echo -e "      ${BLUE}Before:${NC} ${input_kb}KB"
        echo -e "      ${BLUE}After:${NC}  ${final_kb}KB"
        echo -e "      ${BLUE}Saved:${NC}  ${saved}%"
        
        # Cleanup subset file
        [ -f "$subset_output" ] && rm "$subset_output"
        
        return 0
    else
        echo -e "   ${RED}❌ Final WOFF2 not found${NC}"
        return 1
    fi
}

# --- Parse arguments ---
INPUT=""
INPUT_DIR=""
OUTPUT_DIR="./fonts/build"
LANG="fa"
PRESET=""
BATCH=false

while [[ $# -gt 0 ]]; do
    case "$1" in
        --input-dir) INPUT_DIR="$2"; BATCH=true; shift 2 ;;
        --output-dir|-o) OUTPUT_DIR="$2"; shift 2 ;;
        --lang|-l) LANG="$2"; shift 2 ;;
        --preset|-p) PRESET="$2"; shift 2 ;;
        --help|-h) echo "Usage: $0 <font.ttf> [--lang fa] [--preset persian-blog] [-o ./build/]"; exit 0 ;;
        *) [ -z "$INPUT" ] && INPUT="$1"; shift ;;
    esac
done

# --- Execute ---
print_banner

echo -e "${BLUE}   Language:${NC} $LANG"
echo -e "${BLUE}   Output:${NC}   $OUTPUT_DIR"
[ -n "$PRESET" ] && echo -e "${BLUE}   Preset:${NC}   $PRESET"

if [ "$BATCH" = true ] && [ -n "$INPUT_DIR" ]; then
    count=0
    for font in "$INPUT_DIR"/*.ttf "$INPUT_DIR"/*.otf; do
        [ -f "$font" ] || continue
        optimize_font "$font" "$LANG" "$PRESET" "$OUTPUT_DIR"
        count=$((count + 1))
    done
    echo -e "\n${GREEN}   ✅ Optimized $count fonts → $OUTPUT_DIR${NC}"
    
elif [ -n "$INPUT" ]; then
    optimize_font "$INPUT" "$LANG" "$PRESET" "$OUTPUT_DIR"
else
    echo -e "${RED}❌ Specify input file or --input-dir${NC}"
    echo "Usage: $0 <font.ttf> [--lang fa] [--preset persian-blog]"
    exit 1
fi

echo ""
echo -e "${GREEN}   🎯 Done!${NC}"
echo ""