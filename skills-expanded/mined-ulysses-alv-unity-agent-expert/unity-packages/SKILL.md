---
name: unity-packages
description: >
  Unity 6000.3 LTS package management patterns. Covers Package Manager,
  custom packages, scoped registries, and package development.
  Trigger: When working with Unity packages, creating custom packages,
  or managing dependencies in Unity 6000.
license: Apache-2.0
metadata:
  author: gentleman-programming
  version: "1.0"
---

## When to Use

- Creating custom Unity packages
- Configuring scoped registries
- Managing package dependencies
- Publishing packages to registries
- Resolving package conflicts

## Critical Rules

### Package Structure
```
com.mycompany.mypackage/
├── package.json          # Package manifest
├── Runtime/              # Runtime code
├── Editor/               # Editor-only code
├── Tests/                # Test code
└── Documentation~/       # Documentation (not included in package)
```

### package.json
```json
{
  "name": "com.mycompany.mypackage",
  "version": "1.0.0",
  "displayName": "My Package",
  "description": "Package description",
  "unity": "6000.3",
  "dependencies": {
    "com.unity.modules.unitywebrequest": "1.0.0"
  }
}
```

## Scoped Registries

### scopedRegistries in manifest.json
```json
{
  "scopedRegistries": [
    {
      "name": "My Registry",
      "url": "https://my-registry.com",
      "scopes": ["com.mycompany"]
    }
  ]
}
```

## Common Mistakes

| Mistake | Correct |
|---------|---------|
| Missing package.json | Required for every package |
| Wrong Unity version | Set "unity": "6000.3" |
| Not using assembly definitions | Use .asmdef for proper compilation |

## Response Format

1. Identify package problem
2. Provide Unity 6000 patterns
3. Include package.json examples
