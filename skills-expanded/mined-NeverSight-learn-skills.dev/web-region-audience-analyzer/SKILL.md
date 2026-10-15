---
name: web-region-audience-analyzer
description: Use when you need to determine the geographic region, target audience, or primary language of a website, and get cross-border localization optimization recommendations. Useful for market research, localization audits, hreflang checks, or understanding a site's demographic focus. Targets multilingual cross-border websites (e.g., Shopify global stores, SaaS multi-language sites), NOT domestic single-language sites.
---

# Web Region & Audience Analyzer

## Overview

This skill analyzes web pages to infer their geographic region, primary language, and target audience. It fuses multiple data sources—IP geolocation, HTML metadata, content signals (currencies, phone numbers), and language detection—to provide a confidence-scored assessment.

**NEW**: After analysis, it generates **cross-border localization optimization recommendations** with a letter grade (A–F), identifying issues in hreflang configuration, locale declarations, signal consistency, market adaptation, and more—with concrete code examples for each fix.

## Workflow

1. **Run Analysis**: Execute the provided Python script on a target URL.
2. **Interpret Results**: Review the JSON output for `primaryRegion`, `likelyAudience`, and `confidence` scores.
3. **Review Optimization**: Check the `optimization` section for the grade, score, and actionable recommendations.
4. **Verify Evidence**: Check the `evidence` section to see which signals (IP, HTML, Content) contributed to the conclusion.

## Usage

### Setup (Optional but Recommended)

For best results, install the optional dependencies:

```bash
pip install langdetect beautifulsoup4
```

### Basic Analysis (Recommended)

Run the analyzer with default settings (includes IP geolocation, language detection, and optimization recommendations):

```bash
python3 scripts/analyze_webpage.py https://example.com
```

### Advanced Options

**With NLP Cloud (Higher Accuracy Language Detection):**
If you have an NLP Cloud token, use it for better language detection:
```bash
python3 scripts/analyze_webpage.py https://example.com --nlpcloud-token YOUR_TOKEN
```

**Disable IP Geolocation:**
If you only want to analyze on-page content signals:
```bash
python3 scripts/analyze_webpage.py https://example.com --no-ip-geo
```

**Disable Optimization Recommendations:**
If you only need the region/audience analysis without recommendations:
```bash
python3 scripts/analyze_webpage.py https://example.com --no-recommendations
```

**Save Output to File:**
```bash
python3 scripts/analyze_webpage.py https://example.com --output result.json
```

**Export Markdown Report (Saved to Downloads by Default):**
```bash
python3 scripts/analyze_webpage.py https://example.com --format markdown
```

**Export Markdown Report to a Custom Path:**
```bash
python3 scripts/analyze_webpage.py https://example.com --format markdown --output report.md
```

**Specify Target Audience for Persona Analysis:**
```bash
python3 scripts/analyze_webpage.py https://example.com \
  --target-audience "North America women 25-35 fashion shoppers"
```

## Interpreting Results

The script outputs a JSON object. Key fields to look for:

### Region & Audience

- **`result.primaryRegion`**: ISO 3166-1 alpha-2 country code (e.g., "US", "CN", "DE").
- **`result.likelyAudience`**: Human-readable description of the target demographic.
- **`result.regionConfidence`**: 0.0 to 1.0 score.
  - `> 0.8`: High confidence (multiple signals agree).
  - `0.5 - 0.8`: Moderate confidence (some signals agree, others missing).
  - `< 0.5`: Low confidence (conflicting or missing signals).

### Optimization Recommendations (Cross-Border Focus)

- **`optimization.summary.grade`**: Overall grade A–F (A = excellent, F = major issues).
- **`optimization.summary.score`**: Numeric score 0–100.
- **`optimization.summary.critical`**: Count of critical issues (must fix).
- **`optimization.summary.warnings`**: Count of warnings (should fix).
- **`optimization.summary.info`**: Count of informational suggestions (nice to have).
- **`optimization.recommendations[]`**: List of issues, each with:
  - `severity`: "critical" / "warning" / "info"
  - `category`: Issue category (hreflang, locale-declaration, locale-consistency, tld-content-mismatch, hosting-alignment, charset, market-adaptation, market-coverage)
  - `issue`: What's wrong
  - `recommendation`: What to do
  - `codeExample`: HTML/code snippet showing the fix (when applicable)

### Recommendation Categories

| Category | What it checks |
|----------|---------------|
| `hreflang` | Missing hreflang tags, missing x-default, missing self-referencing tags |
| `locale-declaration` | Missing `<html lang>`, `og:locale`, `content-language` |
| `locale-consistency` | Conflicts between declared language signals |
| `tld-content-mismatch` | ccTLD region vs actual content language mismatch |
| `hosting-alignment` | Server location vs target audience, CDN detection |
| `charset` | Missing or non-UTF-8 charset for multilingual content |
| `market-adaptation` | Local currency display, regional social media presence, **local payment methods** |
| `market-coverage` | Major language markets not covered by hreflang |
| `cultural-adaptation` | **Spelling (US vs UK)**, **Measurement Units (Metric vs Imperial)** |
| `ux-mobile` | **Viewport meta tag** configuration |
| `ux-forms` | **Input types** (email, tel) for mobile keyboards |
| `accessibility` | **Image alt text** presence |

### Evidence Sources

- **`evidence.ipGeolocation`**: Physical location of the server (hosting). *Note: CDNs may mask the true origin.*
- **`evidence.htmlSignals`**: Explicit declarations in code (`<html lang>`, `og:locale`, TLD).
- **`evidence.contentSignals`**: Cultural markers in text (currencies, phone formats, social media links).
- **`evidence.languageDetection`**: Statistical analysis of the visible text.

## Troubleshooting

- **"Language detection failed"**: Ensure `langdetect` is installed (`pip install langdetect`) or use `--nlpcloud-token`.
- **"IP Geolocation failed"**: Check network connectivity. The free API has a rate limit of 45 req/min.
- **Low Confidence**: The site might be global/generic (e.g., `.com` domain, English text, US hosting) without specific regional markers.
- **Grade "D" or "F"**: The site has significant cross-border localization gaps. Focus on fixing critical issues first (hreflang, lang attribute).

## References

- **[API Reference](references/api-reference.md)**: Details on IP-API and NLP Cloud integration.
- **[Signal Patterns](references/signal-patterns.md)**: Regex patterns and mappings used for manual verification.
