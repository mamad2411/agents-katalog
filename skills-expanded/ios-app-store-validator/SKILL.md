# iOS App Store Validator

Use this skill when preparing an iOS app for App Store submission. This validates against Apple's App Store Review Guidelines to catch rejection-worthy issues early.

## When to Use

- Before submitting to App Store Connect
- When preparing for TestFlight external testing
- After significant app updates
- When adding new permissions or entitlements
- When concerned about potential rejection

## How to Apply

Read the full agent prompt from `agents/app-store-validator/app-store-validator.md` in the ios-developer-agents repository.

Follow the validation process:

1. **Fetch Current Guidelines** - Get latest from developer.apple.com
2. **Technical Configuration Scan**
   - Info.plist validation (usage descriptions, capabilities)
   - Privacy Manifest (PrivacyInfo.xcprivacy)
   - Entitlements check
   - Code-level issues (private APIs, deprecated frameworks)
3. **Metadata Validation** - App name, description, screenshots, age rating
4. **Privacy & Legal Compliance** - Privacy policy, terms, GDPR/CCPA
5. **In-App Purchase Validation** - If applicable

## Output Format

Provide structured findings with:
- Submission Readiness status (READY / BLOCKED / NEEDS REVIEW)
- Blockers (will cause rejection)
- Warnings (may cause rejection)
- Metadata review table
- Technical configuration table
- Pre-submission checklist
