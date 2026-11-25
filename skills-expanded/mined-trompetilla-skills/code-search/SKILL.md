# Code Search Skill

Smart, context-aware repository search tool. Use this instead of complex `grep` or `find` commands.

## Why use this?
- **Smarter than grep**: Ignores `node_modules`, `.git`, lockfiles automatically.
- **Context-aware**: Shows lines before/after matches (`--context 2`).
- **Structured**: Can output JSON for machine parsing.
- **Safe**: Limits output size to prevent token overflow.

## Usage

### CLI
```bash
# Basic search
node skills/code-search/index.js --query "function main"

# Search specific file types (glob pattern support is basic: *.js, *.ts)
node skills/code-search/index.js --query "TODO" --include "*.js"

# Search with context (2 lines around match)
node skills/code-search/index.js --query "error" --context 2

# Output JSON
node skills/code-search/index.js --query "export default" --json
```

### From other skills (Node.js)
```javascript
const { execSync } = require('child_process');
const output = execSync('node skills/code-search/index.js --query "myFunction" --json').toString();
const results = JSON.parse(output);
```

## Configuration
- Default max matches: 50 (prevents spamming output)
- Default ignore list: `.git`, `node_modules`, `dist`, `build`, `coverage`, `.npm-global`

## Troubleshooting
- If no results found, try broadening search term.
- If too many results, use `--include` to filter file types.
