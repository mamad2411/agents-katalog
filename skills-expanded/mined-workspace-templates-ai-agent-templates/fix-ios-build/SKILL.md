---
name: fix-ios-build
description: Diagnoses an Xcode build or code signing failure from the error output and applies the smallest fix that makes it build.
disable-model-invocation: true
---

Fix the iOS build failure. Scheme or error text: $ARGUMENTS

1. Find the project: `ls *.xcworkspace *.xcodeproj`. Prefer the workspace. List schemes with `xcodebuild -list`.
2. Reproduce: `xcodebuild -scheme <scheme> -destination 'generic/platform=iOS Simulator' build 2>&1 | tail -n 80`. If the user pasted an error, start from it but still reproduce.
3. Find the first "error:" line, not the last. Classify it:
   - Compiler: open the file and fix the code.
   - Dependency: check Package.resolved, Podfile.lock and the minimum deployment target.
   - Signing: compare the bundle id, team and profile with `security find-identity -v -p codesigning` and the target's signing settings.
   - Linker: look for missing frameworks, duplicate symbols, architecture exclusions.
4. Apply the smallest fix and rebuild. Stop after three failed attempts and report what you learned.

Do not delete DerivedData, change the team, or edit certificates or profiles without asking. Report the cause, the change, and the build result.
