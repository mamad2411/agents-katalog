---
name: figma-make-extractor
description: Extract source code, design tokens, and assets from Figma Make (.make) files into runnable React applications
triggers:
  - extract code from figma make file
  - decode figma make canvas
  - get source code from make file
  - extract design tokens from figma
  - convert figma make to react app
  - parse figma make binary format
  - extract assets from make file
  - reverse engineer figma make file
---

# Figma Make Extractor

> Skill by [ara.so](https://ara.so) — Design Skills collection.

Extract source code, design tokens, and assets from Figma Make (.make) files. Figma Make is an AI-powered prototyping tool that generates complete React applications. Unlike traditional Figma Design files (.fig), Make files contain React/TypeScript source code, design tokens, assets, and AI chat history - but they're not accessible via the Figma API.

This tool reverse-engineers the .make file format to extract all project contents into a runnable React application.

## Installation

```bash
git clone https://github.com/albertsikkema/figma-make-extractor.git
cd figma-make-extractor/make_extraction
```

No global installation needed - the `run-all.sh` script handles dependency installation automatically.

## Quick Start

```bash
cd make_extraction
./run-all.sh ../YourFile.make
cd output/react_app
npm install --legacy-peer-deps
npm run dev
```

This extracts everything and creates a ready-to-run React app at `output/react_app/`.

## File Structure

A `.make` file is a ZIP archive containing:

```
YourFile.make (ZIP)
├── canvas.fig          # Binary file with source code & design data
├── meta.json           # Project metadata
├── ai_chat.json        # AI conversation history
├── thumbnail.png       # Preview image
├── images/             # Image assets
│   ├── [hash1]
│   └── [hash2]
└── blob_store/         # Additional binary data
```

The `canvas.fig` file uses a custom binary format:
- Header: `fig-makee` magic bytes + padding (12 bytes)
- Chunk 1: Deflate-compressed Kiwi schema (4 bytes size + data)
- Chunk 2: Zstandard-compressed message data (4 bytes size + data)

## Key Scripts

All scripts are in the `make_extraction/` directory:

### Master Script

```bash
# Extract everything and create React app
./run-all.sh <path-to-make-file>

# Clean up all generated files
./cleanup.sh
```

### Individual Scripts

```bash
# 1. Decode canvas.fig binary to JSON
node 01-decode-canvas.js

# 2. Extract source code files
node 02-extract-source-code.js

# 3. Extract design tokens (colors, fonts, CSS vars)
node 03-extract-design-tokens.js

# 4. Create runnable React app
node 04-create-react-app.js
```

## Programmatic Usage

### Decoding canvas.fig

```javascript
const fs = require('fs');
const pako = require('pako');
const { decompress } = require('fzstd');
const kiwi = require('kiwi-schema');

// Read binary file
const buffer = fs.readFileSync('output/extracted/canvas.fig');

// Skip 12-byte header (fig-makee + padding)
let offset = 12;

// Read Chunk 1 (schema) - deflate compressed
const chunk1Size = buffer.readUInt32LE(offset);
offset += 4;
const chunk1Data = buffer.slice(offset, offset + chunk1Size);
offset += chunk1Size;
const schemaBytes = pako.inflate(chunk1Data);

// Read Chunk 2 (data) - zstandard compressed
const chunk2Size = buffer.readUInt32LE(offset);
offset += 4;
const chunk2Data = buffer.slice(offset, offset + chunk2Size);
const messageBytes = decompress(chunk2Data);

// Decode using Kiwi schema
const schema = kiwi.compileSchema(schemaBytes);
const decoded = schema.decodeMessage(messageBytes);

// Handle BigInt in JSON
const json = JSON.stringify(decoded, (key, value) =>
  typeof value === 'bigint' ? value.toString() : value
, 2);

fs.writeFileSync('decoded-message.json', json);
```

### Extracting Source Files

```javascript
const fs = require('fs');

const decoded = JSON.parse(fs.readFileSync('decoded-message.json', 'utf8'));
const outputDir = 'source_files';
fs.mkdirSync(outputDir, { recursive: true });

let fileCount = 0;

function traverse(node) {
  if (!node) return;
  
  // Extract CODE_FILE nodes with source code
  if (node.type === 'CODE_FILE' && node.sourceCode) {
    const fileName = node.name || `file_${fileCount++}`;
    const filePath = `${outputDir}/${fileName}`;
    fs.writeFileSync(filePath, node.sourceCode, 'utf8');
    console.log(`Extracted: ${fileName}`);
  }
  
  // Traverse children
  if (node.children) {
    node.children.forEach(child => traverse(child));
  }
}

traverse(decoded);
```

### Extracting Design Tokens

```javascript
const fs = require('fs');
const path = require('path');

const sourceDir = 'source_files';
const tokens = {
  colors: { hex: new Set(), rgba: new Set(), hsl: new Set() },
  fonts: new Set(),
  cssVariables: new Set()
};

// Regex patterns
const hexPattern = /#[0-9A-Fa-f]{6}(?:[0-9A-Fa-f]{2})?/g;
const rgbaPattern = /rgba?\(\s*\d+\s*,\s*\d+\s*,\s*\d+(?:\s*,\s*[\d.]+)?\s*\)/g;
const hslPattern = /hsla?\(\s*\d+\s*,\s*\d+%\s*,\s*\d+%(?:\s*,\s*[\d.]+)?\s*\)/g;
const fontPattern = /font-family:\s*["']([^"']+)["']/g;
const cssVarPattern = /--[\w-]+/g;

// Scan all source files
fs.readdirSync(sourceDir).forEach(file => {
  const content = fs.readFileSync(path.join(sourceDir, file), 'utf8');
  
  content.match(hexPattern)?.forEach(c => tokens.colors.hex.add(c));
  content.match(rgbaPattern)?.forEach(c => tokens.colors.rgba.add(c));
  content.match(hslPattern)?.forEach(c => tokens.colors.hsl.add(c));
  
  let fontMatch;
  while ((fontMatch = fontPattern.exec(content)) !== null) {
    tokens.fonts.add(fontMatch[1]);
  }
  
  content.match(cssVarPattern)?.forEach(v => tokens.cssVariables.add(v));
});

// Convert Sets to Arrays
const result = {
  colors: {
    hex: Array.from(tokens.colors.hex),
    rgba: Array.from(tokens.colors.rgba),
    hsl: Array.from(tokens.colors.hsl)
  },
  fonts: Array.from(tokens.fonts),
  cssVariables: Array.from(tokens.cssVariables)
};

fs.writeFileSync('design-tokens.json', JSON.stringify(result, null, 2));
```

### Creating React App Structure

```javascript
const fs = require('fs');
const path = require('path');

const sourceDir = 'source_files';
const appDir = 'react_app';
const srcDir = path.join(appDir, 'src');

// Create directory structure
fs.mkdirSync(path.join(srcDir, 'components/ui'), { recursive: true });
fs.mkdirSync(path.join(srcDir, 'hooks'), { recursive: true });
fs.mkdirSync(path.join(srcDir, 'lib'), { recursive: true });
fs.mkdirSync(path.join(srcDir, 'data'), { recursive: true });
fs.mkdirSync(path.join(srcDir, 'styles'), { recursive: true });
fs.mkdirSync(path.join(appDir, 'public'), { recursive: true });

// Organize files by type
fs.readdirSync(sourceDir).forEach(file => {
  let targetDir = srcDir;
  const content = fs.readFileSync(path.join(sourceDir, file), 'utf8');
  
  // Categorize by content patterns
  if (file.startsWith('use-') && file.endsWith('.ts')) {
    targetDir = path.join(srcDir, 'hooks');
  } else if (file === 'utils.ts' || file === 'cn.ts') {
    targetDir = path.join(srcDir, 'lib');
  } else if (content.includes('@radix-ui') || content.includes('shadcn')) {
    targetDir = path.join(srcDir, 'components/ui');
  } else if (file.endsWith('.tsx')) {
    targetDir = path.join(srcDir, 'components');
  } else if (file.endsWith('.css')) {
    targetDir = path.join(srcDir, 'styles');
  }
  
  // Fix import paths
  let fixedContent = content
    .replace(/@radix-ui\/[\w-]+@[\d.]+/g, match => match.split('@')[0] + '@' + match.split('@')[1])
    .replace(/from\s+['"]\.\.\/[\w-]+@[\d.]+\//g, 'from "@/')
    .replace(/from\s+['"]figma:asset:([^'"]+)['"]/g, (match, hash) => {
      return `from "/images/${hash}.png"`;
    });
  
  fs.writeFileSync(path.join(targetDir, file), fixedContent, 'utf8');
});
```

### Creating package.json

```javascript
const packageJson = {
  "name": "figma-make-app",
  "version": "0.1.0",
  "type": "module",
  "scripts": {
    "dev": "vite",
    "build": "tsc && vite build",
    "preview": "vite preview"
  },
  "dependencies": {
    "react": "^18.3.1",
    "react-dom": "^18.3.1",
    "framer-motion": "^11.0.0",
    "lucide-react": "latest"
  },
  "devDependencies": {
    "@types/react": "^18.3.1",
    "@types/react-dom": "^18.3.0",
    "@vitejs/plugin-react": "^4.3.4",
    "typescript": "^5.6.2",
    "vite": "^6.0.1",
    "@tailwindcss/postcss": "^4.0.0"
  }
};

fs.writeFileSync(
  path.join(appDir, 'package.json'),
  JSON.stringify(packageJson, null, 2)
);
```

## Common Patterns

### Verifying .make File Format

```bash
# Check if file is ZIP
xxd -l 4 YourFile.make
# Should show: 504b 0304 (PK..)

# Check canvas.fig header
unzip -q YourFile.make
xxd -l 20 canvas.fig
# Should show: 6669 672d 6d61 6b65 65 (fig-makee)
```

### Converting Colors

```javascript
// RGBA float (0-1) to hex
function rgbaToHex(color) {
  const r = Math.round(color.r * 255);
  const g = Math.round(color.g * 255);
  const b = Math.round(color.b * 255);
  return `#${r.toString(16).padStart(2,'0')}${g.toString(16).padStart(2,'0')}${b.toString(16).padStart(2,'0')}`.toUpperCase();
}

// Example usage
const figmaColor = { r: 0.11764705926179886, g: 0.11764705926179886, b: 0.11764705926179886, a: 1 };
console.log(rgbaToHex(figmaColor)); // #1E1E1E
```

### Handling Image Assets

```javascript
const fs = require('fs');
const path = require('path');

// Copy images from extracted .make to React app public folder
const imagesSourceDir = 'output/extracted/images';
const imagesTargetDir = 'output/react_app/public/images';

fs.mkdirSync(imagesTargetDir, { recursive: true });

fs.readdirSync(imagesSourceDir).forEach(hash => {
  const sourceFile = path.join(imagesSourceDir, hash);
  const targetFile = path.join(imagesTargetDir, `${hash}.png`);
  fs.copyFileSync(sourceFile, targetFile);
});
```

## Output Structure

After running all scripts, the `output/` directory contains:

```
output/
├── extracted/                  # Unzipped .make contents
│   ├── canvas.fig
│   ├── images/
│   ├── meta.json
│   └── ai_chat.json
├── decoded-message.json        # Decoded canvas.fig
├── source_files/               # Raw extracted source files
├── design-tokens.json          # Colors, fonts, CSS vars
└── react_app/                  # Ready-to-run React app
    ├── package.json
    ├── vite.config.ts
    ├── tsconfig.json
    ├── index.html
    ├── public/
    │   └── images/
    └── src/
        ├── main.tsx
        ├── App.tsx
        ├── components/
        │   └── ui/             # shadcn/ui components
        ├── hooks/
        ├── lib/
        ├── data/
        └── styles/
```

## Troubleshooting

### "Invalid stored block lengths" error

The data chunk uses **Zstandard** compression, not zlib/deflate. Install the correct package:

```bash
npm install fzstd
```

### BigInt serialization error

Use a custom JSON replacer to handle BigInt values:

```javascript
JSON.stringify(decoded, (key, value) =>
  typeof value === 'bigint' ? value.toString() : value
, 2);
```

### Empty source code extraction

Verify the node type and property:

```javascript
if (node.type === 'CODE_FILE' && node.sourceCode) {
  // Extract here
}
```

Not all nodes have source code - only `CODE_FILE` nodes with the `sourceCode` property.

### Import path errors in React app

The `04-create-react-app.js` script automatically fixes:
- Version numbers in package names: `@radix-ui/react-dialog@1.1.6` → `@radix-ui/react-dialog`
- Figma asset imports: `figma:asset:hash` → `/images/hash.png`
- Relative paths: `../component` → `@/components/component`

If imports still fail, manually check the generated `vite.config.ts` has the alias:

```typescript
resolve: {
  alias: {
    '@': '/src'
  }
}
```

### npm install fails with peer dependency conflicts

Use the `--legacy-peer-deps` flag:

```bash
npm install --legacy-peer-deps
```

This is common with React 18 and older package versions.

### Tailwind CSS PostCSS error

The generated app uses Tailwind v4 with `@tailwindcss/postcss`. Ensure `postcss.config.js` exists:

```javascript
export default {
  plugins: {
    '@tailwindcss/postcss': {}
  }
};
```

### Animations not working (React StrictMode)

The generated `main.tsx` omits React.StrictMode to avoid timer/animation issues with Framer Motion. If you need StrictMode, wrap the app manually but expect animation glitches.

## Node Types Reference

When traversing the decoded message, you'll encounter these node types:

| Type | Description | Has sourceCode |
|------|-------------|----------------|
| `DOCUMENT` | Root document node | No |
| `CANVAS` | Page/canvas container | No |
| `CODE_LIBRARY` | Code library container | No |
| `CODE_FILE` | Source code file (`.tsx`, `.ts`, `.css`) | **Yes** |
| `CODE_COMPONENT` | Exported React component definition | No |
| `CODE_INSTANCE` | Instance of a component | No |
| `FRAME` | Visual frame (preview) | No |
| `RESPONSIVE_SET` | Responsive breakpoint container | No |

Only extract source code from `CODE_FILE` nodes.

## API Reference

This is a CLI tool, not a library. All functionality is accessed via scripts:

```bash
# Full extraction pipeline
./run-all.sh <path-to-make-file>

# Individual steps (after running run-all.sh or extracting manually)
node 01-decode-canvas.js
node 02-extract-source-code.js
node 03-extract-design-tokens.js
node 04-create-react-app.js

# Cleanup
./cleanup.sh
```

## Environment Variables

No environment variables required. All paths are relative to the script locations.

## License

MIT License - see the repository for full license text.

## Disclaimer

This tool documents a reverse-engineering process for educational purposes. The extracted code remains subject to Figma's terms of service and any applicable licenses. Use responsibly.
