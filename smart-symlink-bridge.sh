#!/bin/bash
# ============================================================
# SMART SYMLINK BRIDGE — 10K Skills → 21 AI Platforms
# ============================================================
# BUKAN 178K filesystem symlinks (yang bikin device panas).
# Setiap AI platform dapet:
#   1. .skill_index.json (10K skills, keyword searchable, ~212KB)
#   2. lazy-load.sh symlink → catalog (1 symlink, bukan 10K)
#   3. graph-api-bridge.md (instruksi untuk LLM cara akses graph)
#
# Total filesystem entries: 21 platforms × 3 files = 63 entries
# vs old approach: 21 × 8400 = 176,400 symlinks
# Reduction: 99.96%
# ============================================================

CATALOG="$HOME/.agents/skills-catalog"
MASTER_INDEX="$CATALOG/skill_master_index.json"
BRIDGE_SCRIPT="$CATALOG/lazy-load.sh"

# 21 AI Platform dirs
PLATFORMS=(
    ~/.codebuddy ~/.claude ~/.hermes ~/.codex ~/.cline
    ~/.aider ~/.goose ~/.kiro ~/.qwen ~/.gemini
    ~/.orca ~/.continue ~/.copilot ~/.codeium ~/.windsurf
    ~/.dolphin ~/.mistral ~/.openclaude ~/.opencode ~/.devin
    ~/.config/goose
)

echo "=== SMART SYMLINK BRIDGE — Installing to 21 platforms ==="

for platform in "${PLATFORMS[@]}"; do
    skills_dir="$platform/skills"
    mkdir -p "$skills_dir"
    
    # 1. Copy skill index (212KB per platform, total ~4.3MB)
    cp -f "$HOME/.hermes/skills/.skill_index.json" "$skills_dir/.skill_index.json" 2>/dev/null
    
    # 2. Symlink lazy-load.sh (1 symlink, points to catalog)
    ln -sf "$BRIDGE_SCRIPT" "$skills_dir/lazy-load.sh" 2>/dev/null
    
    # 3. Write graph-api-bridge.md (LLM instruction file)
    cat > "$skills_dir/graph-api-bridge.md" << 'BRIDGE_EOF'
# Skill Graph API Bridge

## How to Access 10,000+ Skills

This platform is connected to a skill graph with 10,048 skills.

### Quick Access (via API — zero token cost for discovery):
```bash
# Search skills by keyword
curl -s "http://127.0.0.1:27125/search?q=react"

# Get related skills (graph-based)
curl -s "http://127.0.0.1:27125/related?skill=pdf-generator"

# List all categories (MOCs)
curl -s "http://127.0.0.1:27125/moc"

# Get skills in a category
curl -s "http://127.0.0.1:27125/category?name=AI"

# Load full skill content (gzip decompressed on-the-fly)
curl -s "http://127.0.0.1:27125/load?skill=1000x-token-annihilator"

# Get quality score + usage stats
curl -s "http://127.0.0.1:27125/quality?skill=pdf-generator"

# Get recommended skill combinations
curl -s "http://127.0.0.1:27125/combinations?skill=pdf-generator"

# Get ecosystem stats
curl -s "http://127.0.0.1:27125/stats"
```

### Direct Load (no API needed):
```bash
# Load any skill from gzip catalog
~/.agents/skills-catalog/lazy-load.sh "skill_name"
```

### Rules:
- NEVER readdir() on skills/ — use .skill_index.json instead
- Max 5 skills loaded per task (token budget)
- Load + immediately use + discard (no cache)
- Quality scores guide priority (higher = better)
BRIDGE_EOF
    
    # 4. Thermal protection
    touch "$skills_dir/.metadata_never_index"
    touch "$platform/.metadata_never_index"
    
    echo "  ✓ $(basename $platform): index + loader + bridge + thermal guard"
done

echo ""
echo "=== DONE ==="
echo "Platforms connected: 21"
echo "Skills accessible per platform: 10,048"
echo "Filesystem entries per platform: 4 (index + loader + bridge + guard)"
echo "Total entries: $(( 21 * 4 )) = 84 (vs old 176,400 symlinks)"
echo "Graph API: http://127.0.0.1:27125/health"
