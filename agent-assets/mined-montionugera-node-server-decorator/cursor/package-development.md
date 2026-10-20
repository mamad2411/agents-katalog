---
description: NPM package development and publishing standards
globs: ["package.json", "tsconfig.json", "*.md"]
alwaysApply: false
---

# 📦 Package Development Standards

## Version Control & Commits
- Keep commit messages short, avoid newlines or special characters
- Use conventional commits: `feat:`, `fix:`, `docs:`, `test:`
- Commit changes frequently for version control
- Use trunk-based development with feature branches

## TypeScript Configuration
- Compile output to `dist/` directory
- Include type declarations (`.d.ts` files)
- Set main entry point to `dist/index.js`
- Set types entry point to `dist/index.d.ts`

## Package.json Requirements
- Include proper `main` and `types` fields
- Use semantic versioning (major.minor.patch)
- Include relevant keywords for discoverability
- Add proper build and test scripts

## Export Strategy
- Export all public APIs from `src/index.ts`
- Use named exports for better tree-shaking
- Keep internal utilities private (don't export)
- Follow consistent naming conventions

## Documentation
- Update README.md with usage examples
- Include installation instructions
- Document all exported decorators
- Show TypeScript usage examples

## Publishing Checklist
- Run tests before publishing: `npm test`
- Build package: `npm run build`
- Verify dist files exist
- Update version number
- Use `npm publish` for releases
