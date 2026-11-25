---
name: release
description: Cut a release. Bumps the version, updates CHANGELOG.md, and opens a release PR.
disable-model-invocation: true
---
1. Run the full test suite.
2. Bump the version in package.json.
3. Move the Unreleased section of CHANGELOG.md under the new version.
4. Open a pull request titled "Release vX.Y.Z".
