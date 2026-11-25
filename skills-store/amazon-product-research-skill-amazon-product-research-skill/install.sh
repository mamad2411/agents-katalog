#!/usr/bin/env bash
set -euo pipefail

SKILL_NAME="amazon-product-research-skill"
SKILL_DIR="$(cd "$(dirname "$0")" && pwd)"

# Platform detection
detect_platform() {
    case "${1:-auto}" in
        claude|claude-code)  echo "$HOME/.claude/skills" ;;
        copilot|github)      echo ".github/skills" ;;
        cursor)              echo ".cursor/rules" ;;
        windsurf)            echo ".windsurf/skills" ;;
        cline)               echo ".clinerules" ;;
        codex)               echo ".codex/skills" ;;
        gemini)              echo ".gemini/skills" ;;
        auto)
            # Auto-detect based on environment
            if command -v claude >/dev/null 2>&1; then
                echo "$HOME/.claude/skills"
            elif [ -d ".github" ]; then
                echo ".github/skills"
            elif [ -d ".cursor" ]; then
                echo ".cursor/rules"
            elif [ -d ".windsurf" ]; then
                echo ".windsurf/skills"
            elif [ -f ".clinerules" ]; then
                echo ".clinerules"
            elif [ -d ".codex" ]; then
                echo ".codex/skills"
            elif [ -d ".gemini" ]; then
                echo ".gemini/skills"
            else
                echo "$HOME/.claude/skills"  # default
            fi
            ;;
        *)
            echo "Unknown platform: $1" >&2
            echo "Supported: claude, copilot, cursor, windsurf, cline, codex, gemini" >&2
            exit 1
            ;;
    esac
}

PLATFORM="${1:-auto}"
TARGET_BASE=$(detect_platform "$PLATFORM")
TARGET_DIR="$TARGET_BASE/$SKILL_NAME"

echo "Installing $SKILL_NAME..."
echo "Platform: $PLATFORM"
echo "Target: $TARGET_DIR"

# Create target directory
mkdir -p "$TARGET_DIR"

# Copy all files
cp -r "$SKILL_DIR"/* "$TARGET_DIR/" 2>/dev/null || true

# Copy hidden files
cp -r "$SKILL_DIR"/.[!.]* "$TARGET_DIR/" 2>/dev/null || true

# Make scripts executable
chmod +x "$TARGET_DIR/scripts/"*.py 2>/dev/null || true
chmod +x "$TARGET_DIR/install.sh" 2>/dev/null || true

echo ""
echo "✓ Installed successfully to $TARGET_DIR"
echo ""
echo "Next steps:"
echo "1. Set your Apify API token:"
echo "   export APIFY_API_TOKEN='your_token_here'"
echo ""
echo "2. (Optional) Set OpenAI API key for AI analysis:"
echo "   export OPENAI_API_KEY='your_key_here'"
echo ""
echo "3. Run your first analysis:"
echo "   /amazon-product-research Analyze https://www.amazon.com/Best-Sellers-Electronics/zgbs/electronics"
echo ""
echo "Get your Apify token at: https://console.apify.com/account/integrations"
echo "Get your OpenAI key at: https://platform.openai.com/api-keys"
