version: 1

rules:
  - id: dependency-insight
    name: DependencyInsight
    description: |
      Scans dependencies for high/critical vulnerabilities with "npm audit".
      Blocks commits when such vulnerabilities are detected.
    trigger: onFileChange(package.json|package-lock.json)|weekly
    run: node scripts/dependencyInsight.js
    success_message: "✅ No critical vulnerabilities detected."
    failure_message: "❌ Vulnerabilities found – address them before committing."
 