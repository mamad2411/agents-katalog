#!/bin/bash
# ============================================================
# REPO REFERENCE CATALOG — 50+ Premium Code Repos
# ============================================================
# Clone lightweight copies (README + structure only, NO full code)
# to give AI platforms reference for good repo structure.
#
# Each repo becomes:
#   ~/.agents/repo-refs/<repo-name>/
#     README.md (structure summary)
#     TREE.txt (file tree, max depth 3)
#     PATTERNS.md (key patterns extracted)
#
# Total disk: ~5MB (READMEs + trees only, NOT full code)
# ============================================================

REFS_DIR="$HOME/.agents/repo-refs"
mkdir -p "$REFS_DIR"

# 50 premium repos — curated for structure quality
REPOS=(
    # AI/LLM frameworks
    "https://github.com/langchain-ai/langchain|langchain"
    "https://github.com/openai/openai-python|openai-python"
    "https://github.com/anthropics/anthropic-sdk-python|anthropic-sdk"
    "https://github.com/microsoft/autogen|autogen"
    "https://github.com/crewAIInc/crewAI|crewai"
    "https://github.com/run-llama/llama_index|llama-index"
    "https://github.com/hwchase17/langgraph|langgraph"
    "https://github.com/emd-group/foundry|foundry"
    # Web frameworks
    "https://github.com/vercel/next.js|nextjs"
    "https://github.com/facebook/react|react"
    "https://github.com/vuejs/core|vue-core"
    "https://github.com/sveltejs/svelte|svelte"
    "https://github.com/nuxt/nuxt|nuxt"
    "https://github.com/remix-run/remix|remix"
    "https://github.com/astro.build/astro|astro"
    # Backend
    "https://github.com/expressjs/express|express"
    "https://github.com/fastify/fastify|fastify"
    "https://github.com/koajs/koa|koa"
    "https://github.com/nestjs/nest|nestjs"
    "https://github.com/django/django|django"
    "https://github.com/fastapi/fastapi|fastapi"
    "https://github.com/laravel/laravel|laravel"
    "https://github.com/rails/rails|rails"
    "https://github.com/gin-gonic/gin|gin"
    "https://github.com/fiber-go/fiber|fiber-go"
    # DevOps/Infra
    "https://github.com/docker/compose|docker-compose"
    "https://github.com/kubernetes/kubernetes|kubernetes"
    "https://github.com/terraform-linters/tflint|tflint"
    "https://github.com/ansible/ansible|ansible"
    "https://github.com/hashicorp/terraform|terraform"
    "https://github.com/helm/helm|helm"
    # Database
    "https://github.com/redis/redis|redis"
    "https://github.com/postgres/postgres|postgres"
    "https://github.com/mysql/mysql-server|mysql"
    "https://github.com/mongodb/mongo|mongodb"
    "https://github.com/prisma/prisma|prisma"
    "https://github.com/drizzle-team/drizzle-orm|drizzle-orm"
    # Tools/CLI
    "https://github.com/tmux/tmux|tmux"
    "https://github.com/cli/cli|github-cli"
    "https://github.com/junegunn/fzf|fzf"
    "https://github.com/BurntSushi/ripgrep|ripgrep"
    "https://github.com/ogham/exa|exa"
    "https://github.com/sharkdp/bat|bat"
    "https://github.com/starship/starship|starship"
    # Creative/Content
    "https://github.com/slidev/slidev|slidev"
    "https://github.com/marp-team/marp-core|marp"
    "https://github.com/impress/impress.js|impress-js"
    "https://github.com/revealjs/reveal.js|revealjs"
    # Security
    "https://github.com/trufflesecurity/trufflehog|trufflehog"
    "https://github.com/semgrep/semgrep|semgrep"
    "https://github.com/bridgecrewio/checkov|checkov"
    # Monorepo/Build
    "https://github.com/turbo-tools/turbo|turbo"
    "https://github.com/nrwl/nx|nx"
    "https://github.com/lerna/lerna|lerna"
)

echo "=== REPO REFERENCE CATALOG ==="
echo "Cloning README + structure from ${#REPOS[@]} repos..."
echo ""

SUCCESS=0
FAIL=0

for repo_entry in "${REPOS[@]}"; do
    IFS='|' read -r url name <<< "$repo_entry"
    target="$REFS_DIR/$name"
    
    if [ -d "$target" ]; then
        echo "  ~ $name (already exists, skip)"
        continue
    fi
    
    # Shallow clone --depth 1 --filter=blob:none (minimal download)
    git clone --depth 1 --filter=blob:none --sparse "$url" "$target" 2>/dev/null
    
    if [ ! -d "$target" ]; then
        echo "  ✗ $name (clone failed)"
        FAIL=$((FAIL + 1))
        continue
    fi
    
    # Extract README
    cd "$target"
    git sparse-checkout set README.md docs README 2>/dev/null
    
    # Generate TREE.txt (depth 3, max 200 lines)
    find . -maxdepth 3 -not -path './.git/*' | head -200 > TREE.txt 2>/dev/null
    
    # Generate PATTERNS.md
    cat > PATTERNS.md << PATTERNS_EOF
# $name — Key Patterns

## Source: $url
## Cloned: $(date -u +%Y-%m-%dT%H:%M:%SZ)

## Structure Overview
$(head -50 TREE.txt 2>/dev/null | tr '\n' '|' | sed 's/|/\\n/g')

## README Summary
$(head -100 README.md 2>/dev/null || echo "No README found")
PATTERNS_EOF
    
    # Remove .git to save space
    rm -rf .git
    
    # Thermal guard
    touch "$target/.metadata_never_index"
    
    SIZE=$(du -sh "$target" 2>/dev/null | cut -f1)
    echo "  ✓ $name ($SIZE)"
    SUCCESS=$((SUCCESS + 1))
done

echo ""
echo "=== DONE ==="
echo "Repos cloned: $SUCCESS"
echo "Failed: $FAIL"
echo "Location: $REFS_DIR"
TOTAL_SIZE=$(du -sh "$REFS_DIR" 2>/dev/null | cut -f1)
echo "Total size: $TOTAL_SIZE"

# Build master index of repo references
python3 -c "
import os, json
refs_dir = os.path.expanduser('$REFS_DIR')
repos = []
for name in sorted(os.listdir(refs_dir)):
    path = os.path.join(refs_dir, name)
    if not os.path.isdir(path) or name.startswith('.'):
        continue
    tree_file = os.path.join(path, 'TREE.txt')
    tree = ''
    if os.path.exists(tree_file):
        with open(tree_file) as f:
            tree = f.read()[:2000]
    repos.append({'name': name, 'path': path, 'tree_preview': tree[:500]})
index = {'version': '1.0', 'count': len(repos), 'repos': repos}
index_path = os.path.join(refs_dir, 'repo-master-index.json')
with open(index_path, 'w') as f:
    json.dump(index, f, indent=2)
print(f'Master index: {index_path} ({len(repos)} repos)')
" 2>/dev/null
