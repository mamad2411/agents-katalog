---
description: Run Supply Chain Security and Dependency Management Check
globs:
  [
    'package.json',
    'package-lock.json',
    'yarn.lock',
    'pnpm-lock.yaml',
    '**/sbom.json',
    '.github/workflows/*.yml',
  ]
---

# Security: Supply Chain Security & Dependency Management

<audit_rules>

- You MUST implement Software Bill of Materials (SBOM) generation for all builds and deployments.
- You MUST configure automated vulnerability scanning for all dependencies using tools like Snyk or GitHub Dependabot.
- You MUST implement dependency pinning with exact versions in lock files to prevent supply chain attacks.
- You MUST configure signed commits and require signature verification for critical repositories.
- You MUST implement proper dependency allowlists and block suspicious or unmaintained packages.
- You MUST ensure all third-party packages are vetted for security and maintenance before inclusion.
- You MUST configure automated dependency updates with security patch prioritization.
- You MUST implement proper container image scanning for vulnerabilities in production deployments.
- You MUST ensure all build tools and CI/CD pipelines are secured and monitored for unauthorized changes.
- You MUST configure proper artifact provenance tracking and verification for all deployed packages.
  </audit_rules>

<example_good>

```json
// package.json with security configurations
{
  "name": "secure-app",
  "version": "1.0.0",
  "dependencies": {
    "express": "^4.18.2",
    "lodash": "4.17.21" // Pinned version, not caret
  },
  "devDependencies": {
    "@snyk/cli": "^1.1200.0",
    "audit-ci": "^6.6.0"
  },
  "scripts": {
    "audit": "audit-ci --moderate",
    "sbom": "cyclonedx-bom --output-format json --output-file sbom.json",
    "preinstall": "npx allowlist-check",
    "test": "npm run audit && npm run test:unit"
  },
  "engines": {
    "node": ">=18.17.0",
    "npm": ">=9.0.0"
  }
}
```

```yaml
# .github/workflows/security.yml
name: Security Pipeline

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  security-scan:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0

      - name: Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: '18'
          cache: 'npm'

      - name: Install dependencies
        run: npm ci --ignore-scripts

      - name: Run security audit
        run: npm audit --audit-level moderate

      - name: Generate SBOM
        run: npm run sbom

      - name: Scan container image
        uses: aquasecurity/trivy-action@master
        with:
          image-ref: 'myapp:${{ github.sha }}'
          format: 'sarif'
          output: 'trivy-results.sarif'

      - name: Upload SBOM
        uses: actions/upload-artifact@v3
        with:
          name: sbom
          path: sbom.json
```

</example_good>

<example_bad>

```json
// BAD: Unpinned dependencies, no security configurations
{
  "name": "insecure-app",
  "version": "1.0.0",
  "dependencies": {
    "express": "*", // BAD: Wildcard version
    "lodash": "^4.17.0", // BAD: Caret allows vulnerable updates
    "suspicious-package": "1.0.0" // BAD: Unvetted dependency
  },
  "scripts": {
    "install": "npm install" // BAD: No security checks
  }
}

// BAD: No lock file committed, allowing supply chain attacks
// No SBOM generation
// No vulnerability scanning
// No dependency allowlist
```

</example_bad>
