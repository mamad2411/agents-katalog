# 🎨 Unified Code Formatting & Quality Standards

## 📋 Overview

This rule consolidates all code formatting, linting, and quality standards across your development stack. It provides universal guidelines for maintaining consistent, clean, and professional code across all projects.

## 🛠️ Universal Formatting Tools

### **Prettier - Universal Code Formatter**
```json
// .prettierrc
{
  "semi": true,
  "trailingComma": "es5",
  "singleQuote": true,
  "printWidth": 80,
  "tabWidth": 2,
  "useTabs": false
}
```

### **ESLint - JavaScript/TypeScript Linting**
```json
// .eslintrc.json
{
  "extends": [
    "eslint:recommended",
    "@typescript-eslint/recommended",
    "prettier"
  ],
  "plugins": ["@typescript-eslint"],
  "rules": {
    "no-console": "warn",
    "prefer-const": "error",
    "no-unused-vars": "error"
  }
}
```

### **EditorConfig - Editor Consistency**
```ini
# .editorconfig
root = true

[*]
charset = utf-8
end_of_line = lf
insert_final_newline = true
trim_trailing_whitespace = true

[*.{js,jsx,ts,tsx,json,css,scss,html,md}]
indent_style = space
indent_size = 2

[*.{py,rst}]
indent_style = space
indent_size = 4

[*.{go,rs,cpp,c,h}]
indent_style = tab
indent_size = 4
```

## 🐍 Python Formatting Standards

### **Black - Code Formatter**
```bash
# Install Black
pip install black

# Format all Python files
black .

# Format specific file
black src/main.py
```

### **Ruff - Fast Python Linter**
```bash
# Install Ruff
pip install ruff

# Lint all files
ruff check .

# Auto-fix issues
ruff check --fix .
```

### **PEP 8 Compliance**
- **Line Length**: Maximum 79 characters
- **Indentation**: 4 spaces (no tabs)
- **Naming**: snake_case for variables/functions, PascalCase for classes
- **Imports**: Group imports (standard library, third-party, local)

```python
# ✅ Good Python formatting
import os
import sys
from typing import List, Optional

import requests
import pandas as pd

from .models import User
from .utils import format_name


class UserManager:
    def __init__(self, users: List[User]):
        self.users = users
    
    def get_user_by_id(self, user_id: int) -> Optional[User]:
        return next((user for user in self.users if user.id == user_id), None)
```

## 🦀 Rust Formatting Standards

### **cargo fmt - Rust Formatter**
```bash
# Format all Rust code
cargo fmt

# Check formatting without changes
cargo fmt --check
```

### **cargo clippy - Rust Linter**
```bash
# Run clippy checks
cargo clippy

# Run with warnings as errors
cargo clippy -- -D warnings
```

### **Rust Style Guidelines**
- **Indentation**: 4 spaces
- **Line Length**: 100 characters maximum
- **Naming**: snake_case for variables/functions, PascalCase for types
- **Documentation**: Use `///` for public items

```rust
// ✅ Good Rust formatting
use std::collections::HashMap;
use serde::{Deserialize, Serialize};

/// Represents a user in the system
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct User {
    pub id: u32,
    pub name: String,
    pub email: String,
}

impl User {
    /// Creates a new user with the given parameters
    pub fn new(id: u32, name: String, email: String) -> Self {
        Self { id, name, email }
    }
    
    /// Returns the user's display name
    pub fn display_name(&self) -> &str {
        &self.name
    }
}
```

## ⚡ TypeScript/JavaScript Formatting

### **TypeScript ESLint Configuration**
```json
// .eslintrc.json for TypeScript
{
  "extends": [
    "@typescript-eslint/recommended",
    "@typescript-eslint/recommended-requiring-type-checking",
    "prettier"
  ],
  "parser": "@typescript-eslint/parser",
  "plugins": ["@typescript-eslint"],
  "rules": {
    "@typescript-eslint/no-unused-vars": "error",
    "@typescript-eslint/explicit-function-return-type": "warn",
    "@typescript-eslint/no-explicit-any": "warn",
    "prefer-const": "error",
    "no-var": "error"
  }
}
```

### **TypeScript Style Guidelines**
- **Indentation**: 2 spaces
- **Line Length**: 80-100 characters
- **Naming**: camelCase for variables/functions, PascalCase for types/interfaces
- **Types**: Prefer interfaces over types for objects

```typescript
// ✅ Good TypeScript formatting
interface User {
  id: number;
  name: string;
  email: string;
  isActive: boolean;
}

interface UserService {
  getUserById(id: number): Promise<User | null>;
  createUser(userData: Omit<User, 'id'>): Promise<User>;
}

class UserManager implements UserService {
  private users: User[] = [];

  async getUserById(id: number): Promise<User | null> {
    return this.users.find(user => user.id === id) || null;
  }

  async createUser(userData: Omit<User, 'id'>): Promise<User> {
    const newUser: User = {
      id: Date.now(),
      ...userData,
    };
    
    this.users.push(newUser);
    return newUser;
  }
}
```

## 🎨 Frontend Framework Standards

### **React/Next.js Formatting**
```json
// .eslintrc.json for React
{
  "extends": [
    "next/core-web-vitals",
    "@typescript-eslint/recommended",
    "prettier"
  ],
  "rules": {
    "react-hooks/rules-of-hooks": "error",
    "react-hooks/exhaustive-deps": "warn",
    "react/prop-types": "off"
  }
}
```

### **Vue.js Style Guide**
```json
// .eslintrc.js for Vue
module.exports = {
  extends: [
    'plugin:vue/vue3-recommended',
    '@typescript-eslint/recommended',
    'prettier'
  ],
  rules: {
    'vue/multi-word-component-names': 'off',
    'vue/no-unused-vars': 'error'
  }
}
```

### **Svelte Formatting**
```json
// .eslintrc.js for Svelte
module.exports = {
  extends: [
    'plugin:svelte/recommended',
    '@typescript-eslint/recommended',
    'prettier'
  ],
  parser: 'svelte-eslint-parser',
  rules: {
    'svelte/valid-compile': 'error'
  }
}
```

## 📱 Mobile Development Standards

### **React Native Formatting**
```json
// .eslintrc.js for React Native
module.exports = {
  extends: [
    '@react-native-community',
    '@typescript-eslint/recommended',
    'prettier'
  ],
  rules: {
    'react-native/no-inline-styles': 'warn',
    'react-native/no-unused-styles': 'error'
  }
}
```

### **Flutter/Dart Formatting**
```bash
# Format Dart code
dart format .

# Analyze Dart code
dart analyze .
```

```yaml
# analysis_options.yaml
include: package:flutter_lints/flutter.yaml

linter:
  rules:
    - always_declare_return_types
    - avoid_print
    - prefer_const_constructors
    - prefer_final_fields
```

## 🧪 Testing Framework Standards

### **Jest Configuration**
```json
// jest.config.js
module.exports = {
  preset: 'ts-jest',
  testEnvironment: 'node',
  collectCoverageFrom: [
    'src/**/*.{ts,tsx}',
    '!src/**/*.d.ts',
    '!src/**/*.test.{ts,tsx}'
  ],
  coverageThreshold: {
    global: {
      branches: 80,
      functions: 80,
      lines: 80,
      statements: 80
    }
  }
};
```

### **Playwright Configuration**
```typescript
// playwright.config.ts
import { defineConfig, devices } from '@playwright/test';

export default defineConfig({
  testDir: './tests',
  fullyParallel: true,
  forbidOnly: !!process.env.CI,
  retries: process.env.CI ? 2 : 0,
  workers: process.env.CI ? 1 : undefined,
  reporter: 'html',
  use: {
    baseURL: 'http://localhost:3000',
    trace: 'on-first-retry',
  },
  projects: [
    {
      name: 'chromium',
      use: { ...devices['Desktop Chrome'] },
    },
  ],
});
```

## 🔧 Build Tool Standards

### **Vite Configuration**
```typescript
// vite.config.ts
import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';
import path from 'path';

export default defineConfig({
  plugins: [react()],
  resolve: {
    alias: {
      '@': path.resolve(__dirname, './src'),
    },
  },
  build: {
    outDir: 'dist',
    sourcemap: true,
    rollupOptions: {
      output: {
        manualChunks: {
          vendor: ['react', 'react-dom'],
        },
      },
    },
  },
});
```

### **Webpack Configuration**
```javascript
// webpack.config.js
const path = require('path');

module.exports = {
  entry: './src/index.js',
  output: {
    path: path.resolve(__dirname, 'dist'),
    filename: 'bundle.js',
    clean: true,
  },
  module: {
    rules: [
      {
        test: /\.tsx?$/,
        use: 'ts-loader',
        exclude: /node_modules/,
      },
    ],
  },
  resolve: {
    extensions: ['.tsx', '.ts', '.js'],
    alias: {
      '@': path.resolve(__dirname, 'src'),
    },
  },
};
```

## 📊 Code Quality Metrics

### **Coverage Thresholds**
- **Unit Tests**: Minimum 80% coverage
- **Integration Tests**: Minimum 70% coverage
- **E2E Tests**: Critical user flows covered
- **Type Coverage**: 100% for TypeScript projects

### **Performance Standards**
- **Bundle Size**: < 250KB for main bundle
- **Lighthouse Score**: > 90 for all metrics
- **First Contentful Paint**: < 1.5 seconds
- **Largest Contentful Paint**: < 2.5 seconds

### **Security Standards**
- **Dependency Vulnerabilities**: 0 critical/high
- **Code Scanning**: Automated security checks
- **Secret Detection**: No hardcoded secrets
- **Input Validation**: All user inputs validated

## 🚀 Automation & CI/CD

### **Pre-commit Hooks**
```json
// .husky/pre-commit
#!/bin/sh
. "$(dirname "$0")/_/husky.sh"

npm run lint
npm run format:check
npm run test
npm run build
```

### **GitHub Actions Workflow**
```yaml
# .github/workflows/code-quality.yml
name: Code Quality

on: [push, pull_request]

jobs:
  quality:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-node@v3
        with:
          node-version: '18'
      
      - run: npm ci
      - run: npm run lint
      - run: npm run format:check
      - run: npm run test
      - run: npm run build
      
      - name: Upload coverage
        uses: codecov/codecov-action@v3
```

## 📝 Documentation Standards

### **Code Comments**
- **Function Documentation**: JSDoc for JavaScript/TypeScript
- **API Documentation**: OpenAPI/Swagger for APIs
- **Inline Comments**: Explain complex logic, not obvious code
- **README Files**: Project setup, usage, and contribution guidelines

### **Commit Message Format**
```bash
# Conventional Commits
feat: add user authentication system
fix: resolve login validation issue
docs: update API documentation
style: format code according to style guide
refactor: simplify user service logic
test: add unit tests for user validation
chore: update dependencies
```

## 🎯 Best Practices Summary

### **Do's ✅**
- Use automated formatting tools (Prettier, Black, cargo fmt)
- Configure ESLint with strict rules
- Maintain consistent naming conventions
- Write comprehensive tests
- Document complex logic
- Use TypeScript for type safety
- Follow framework-specific style guides

### **Don'ts ❌**
- Mix tabs and spaces
- Ignore linting warnings
- Skip code reviews
- Hardcode configuration values
- Use `any` type in TypeScript
- Commit unformatted code
- Skip automated testing

## 🔄 Maintenance & Updates

### **Regular Tasks**
- **Weekly**: Update dependencies and security patches
- **Monthly**: Review and update formatting rules
- **Quarterly**: Audit code quality metrics
- **Annually**: Evaluate new tools and standards

### **Tool Updates**
```bash
# Update Prettier
npm update prettier

# Update ESLint
npm update eslint @typescript-eslint/eslint-plugin

# Update Python tools
pip install --upgrade black ruff

# Update Rust tools
rustup update
```

---

**Rule Created**: $(date)  
**Coverage**: All major languages and frameworks  
**Tools**: Prettier, ESLint, Black, Ruff, cargo fmt  
**Status**: ✅ Comprehensive and Ready to Use
description:
globs:
alwaysApply: true
---
