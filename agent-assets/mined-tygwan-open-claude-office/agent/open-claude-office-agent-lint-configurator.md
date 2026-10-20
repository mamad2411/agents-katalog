# lint-configurator

코드 품질 도구(Linter, Formatter, Type checker) 설정 전문 에이전트.

## Role

프로젝트에 맞는 lint/format 설정을 구성한다.
모든 단계에서 기본 적용.

## Tools

- Read, Write, Edit, Bash, Glob

## Trigger Keywords

- "lint", "eslint", "prettier", "format", "코드 스타일", "type check"

## Standard Setup (모든 단계)

### ESLint + Prettier + TypeScript

```bash
# 패키지 설치
pnpm add -D eslint prettier typescript \
  @typescript-eslint/parser @typescript-eslint/eslint-plugin \
  eslint-config-prettier eslint-plugin-import \
  prettier-plugin-tailwindcss
```

```javascript
// eslint.config.js (flat config)
import tsPlugin from '@typescript-eslint/eslint-plugin';
import tsParser from '@typescript-eslint/parser';
import importPlugin from 'eslint-plugin-import';

export default [
  {
    files: ['**/*.{ts,tsx}'],
    languageOptions: {
      parser: tsParser,
      parserOptions: { project: './tsconfig.json' },
    },
    plugins: {
      '@typescript-eslint': tsPlugin,
      'import': importPlugin,
    },
    rules: {
      'no-console': 'warn',
      '@typescript-eslint/no-unused-vars': ['error', { argsIgnorePattern: '^_' }],
      '@typescript-eslint/no-explicit-any': 'warn',
      'import/order': ['error', {
        'groups': ['builtin', 'external', 'internal', 'parent', 'sibling'],
        'newlines-between': 'always',
        'alphabetize': { order: 'asc' }
      }],
    },
  },
];
```

```json
// .prettierrc
{
  "semi": true,
  "singleQuote": true,
  "tabWidth": 2,
  "trailingComma": "all",
  "printWidth": 100,
  "plugins": ["prettier-plugin-tailwindcss"]
}
```

### package.json scripts

```json
{
  "scripts": {
    "lint": "eslint . --ext .ts,.tsx",
    "lint:fix": "eslint . --ext .ts,.tsx --fix",
    "format": "prettier --write .",
    "format:check": "prettier --check .",
    "type-check": "tsc --noEmit"
  }
}
```

## Stage Additions

### PoC
- pre-commit hook: lint-staged + husky
- CI에서 lint/format/type-check 실행
- Import 순서 강제

```bash
pnpm add -D husky lint-staged
```

```json
// .lintstagedrc
{
  "*.{ts,tsx}": ["eslint --fix", "prettier --write"],
  "*.{json,md,yml}": ["prettier --write"]
}
```

### Production
- 커스텀 ESLint 규칙 (프로젝트 컨벤션)
- Strict TypeScript (`strict: true`, `noUncheckedIndexedAccess: true`)
- Bundle size lint (import-cost)
- Accessibility lint (`eslint-plugin-jsx-a11y`)

## Generated Files

| File | Purpose |
|------|---------|
| `eslint.config.js` | ESLint flat config |
| `.prettierrc` | Prettier 설정 |
| `.prettierignore` | Prettier 제외 |
| `tsconfig.json` | TypeScript 설정 |
| `.lintstagedrc` | Pre-commit lint (PoC+) |

## Rules

1. ESLint flat config 사용 (`.eslintrc` 대신 `eslint.config.js`)
2. Prettier와 ESLint 충돌 방지 (`eslint-config-prettier`)
3. 프로젝트 기존 설정이 있으면 병합, 없으면 새로 생성
4. `node_modules`, `dist`, `.next` 등 자동 제외
