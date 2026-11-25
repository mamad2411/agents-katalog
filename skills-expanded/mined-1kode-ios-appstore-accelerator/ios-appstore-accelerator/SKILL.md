---
name: ios-appstore-accelerator
description: Guide vibe coders through iOS App Store submission. Use when user needs help with App Store submission, privacy policies, app metadata, screenshots, Info.plist validation, Apple guidelines compliance, or pre-submission review. Triggers on phrases like "submit to App Store", "App Store rejection", "privacy policy for iOS", "app metadata", "screenshot requirements", or "Apple review".
---

# iOS App Store Accelerator

Submit iOS apps to the App Store with confidence. This skill transforms App Store submission from a confusing multi-day research project into a streamlined checklist-driven process.

## Quick Start

Run the appropriate command based on your stage:

| Stage | Command | What It Does |
|-------|---------|--------------|
| Planning | `/appstore:checklist` | Generate full compliance checklist |
| Legal | `/appstore:privacy-policy` | Create privacy policy from app analysis |
| Marketing | `/appstore:metadata` | Generate App Store listing content |
| Final | `/appstore:review-prepare` | Pre-flight check before submission |

## Workflow Overview

App Store submission follows this sequence:

1. **Compliance Check** → Identify what's missing
2. **Privacy & Legal** → Generate required policies
3. **Metadata Prep** → Create App Store listing content
4. **Asset Validation** → Verify screenshots, icons, builds
5. **Pre-flight Review** → Final check before submission

## Key Apple Requirements

### Required for ALL Apps

- **Privacy Policy URL**: Public webpage with privacy policy
- **App Icon**: 1024×1024 PNG, no alpha/transparency, no rounded corners
- **Screenshots**: Device-specific dimensions (see references/screenshot-specs.md)
- **Metadata**: Name (30 chars), subtitle (30 chars), description, keywords (100 chars)
- **Support URL**: Public webpage for user support
- **Age Rating**: Questionnaire responses for content rating

### Required Since 2024

- **Privacy Manifest** (`PrivacyInfo.xcprivacy`): Required if app uses certain APIs
- **Privacy Nutrition Labels**: Data collection disclosures in App Store Connect

### Common Rejection Triggers

See `references/common-rejection-reasons.md` for detailed patterns. Top issues:

1. **Crashes/Bugs** (2.1) - App doesn't function as described
2. **Misleading Metadata** (2.3) - Screenshots/description don't match app
3. **Privacy Violations** (5.1.1) - Missing or inadequate privacy handling
4. **Minimum Functionality** (4.2) - App is too simple or web wrapper
5. **Deprecated APIs** (2.5.1) - Using outdated system calls

## Command Reference

### /appstore:checklist

Generate a comprehensive compliance checklist by analyzing the project.

**Output includes:**
- Required assets status (icon, screenshots)
- Info.plist validation
- Privacy manifest requirements
- Metadata completeness
- Common rejection risk factors

### /appstore:privacy-policy

Generate a privacy policy based on app's data practices.

**Process:**
1. Analyze app for data collection (analytics, user accounts, etc.)
2. Identify third-party SDKs and their data practices
3. Generate compliant privacy policy from template
4. Output ready-to-host HTML/Markdown

### /appstore:metadata

Create App Store listing content optimized for discovery.

**Generates:**
- App name options (within 30 char limit)
- Subtitle options (within 30 char limit)
- Full description with feature highlights
- Keyword suggestions (within 100 char limit)
- Screenshot text overlay suggestions

### /appstore:review-prepare

Final pre-submission validation.

**Checks:**
- All required fields populated
- Assets meet specifications
- No obvious rejection triggers
- Test account credentials ready (if needed)
- Review notes prepared for edge cases

## Scripts

| Script | Purpose |
|--------|---------|
| `scripts/privacy_policy_generator.py` | Generate privacy policy from data practices |
| `scripts/screenshot_validator.py` | Validate screenshot dimensions and format |
| `scripts/info_plist_analyzer.py` | Parse and validate Info.plist |
| `scripts/privacy_manifest_checker.py` | Check Privacy Manifest requirements |

## References

| File | Content |
|------|---------|
| `references/apple-guidelines-checklist.md` | Complete submission checklist |
| `references/common-rejection-reasons.md` | Top 10 rejections with fixes |
| `references/privacy-manifest-guide.md` | Privacy Manifest requirements |
| `references/metadata-best-practices.md` | ASO and metadata optimization |

## Assets

| File | Purpose |
|------|---------|
| `assets/privacy-policy-template.md` | Privacy policy template |
| `assets/terms-of-service-template.md` | Terms of service template |

## Tips for Success

1. **Start Early**: Begin checklist review before code is "done"
2. **Test on Device**: Simulator-only testing misses real issues
3. **Use TestFlight**: Beta test with real users before submission
4. **Prepare Review Notes**: Explain non-obvious features to reviewers
5. **Have Test Credentials Ready**: If login required, provide demo account

## When Things Go Wrong

If rejected:
1. Read the rejection reason carefully (Resolution Center)
2. Check `references/common-rejection-reasons.md` for the guideline
3. Fix the specific issue cited
4. Reply in Resolution Center with explanation of fix
5. Resubmit binary

Average review time: 24-48 hours. Expedited review available for critical fixes.
