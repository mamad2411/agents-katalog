---
name: bill-96-compliance-matrix
description: Comprehensive Bill 96 compliance audit matrix for Quebec businesses. This skill should be used when performing forensic audits, generating compliance reports, or advising on French language requirements in Quebec.
license: CC-BY-NC-SA-4.0
---

# Bill 96 Compliance Matrix (Le Registre Loi 96 Edition)

This skill provides the official internal compliance matrix for auditing Quebec businesses against the Charter of the French Language (Bill 96).

## Compliance Domains

### 1. Linguistic Presence (Web & Digital)
- **Primary Domain**: Does the primary domain or landing page prioritize French (`fr-CA` or `fr-QC`)?
- **Navigation**: Is the menu/navigation first presented in French?
- **Product Descriptions**: Are all product/service descriptions available in French with equivalent quality to English?
- **Checkout/Cart**: Is the entire purchase flow available in French?

### 2. Legal & Documentation
- **Terms of Service**: Are the TOS available in French? (Mandatory since June 2023)
- **Privacy Policy**: Is the privacy policy available in French?
- **Contracts**: Are employment and consumer contracts available in French before any other language?

### 3. Visual & Aesthetic (Vision Audit)
- **Banners & Hero Images**: Do visual assets containing text have a French version or predominant French text?
- **Alt Text**: Is accessibility metadata provided in French?
- **Logos**: Are descriptive marks or taglines translated or accompanied by a French equivalent?

## Risk Scoring Model

| Severity | Criteria | Impact |
| :--- | :--- | :--- |
| **CRITICAL** (80-100) | No French version, hidden French toggle, English-only legal. | Immediate OQLF reporting potential. |
| **HIGH** (60-79) | Mixed content, English-first navigation, missing French TOS. | High risk of formal notice. |
| **MODERATE** (30-59) | French present but incomplete or lower quality than English. | Compliance gap identified. |
| **LOW** (0-29) | Full French parity, localized SEO, bilingual gateway. | Compliant (Le Registre Loi 96 Shield). |

## Forensic Audit Workflow

1. **Scout**: Extract business metadata (NEQ, Name, Sector).
2. **Scan**: Perform text-based analysis of the domain.
3. **Vision**: Use Antigravity Vision tools to analyze visual compliance.
4. **Score**: Apply the matrix to generate the `riskScore`.
5. **Report**: Generate the `remediationPackage` in French.

## Remédiation Tiers (French First)

- **BOUCLIER (SHIELD)**: Minor fixes, localization of tags. (49$)
- **SENTINELLE (SENTINEL)**: Full legal translation + SEO. (299$)
- **FORTERESSE (FORTRESS)**: Complete infrastructure overhaul, 24/7 compliance monitoring. (599$)
