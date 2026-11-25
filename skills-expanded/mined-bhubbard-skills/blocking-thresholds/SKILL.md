---
name: blocking-thresholds
description: Guides the configuration of click fraud blocking thresholds in ClickCease.
---

# ClickCease Blocking Thresholds Configuration

This skill explains how to configure blocking thresholds in ClickCease, controlling how many clicks an IP address is permitted before being blocked.

## Basic Configuration Steps

1. **Navigate to Settings:** Log in to the ClickCease dashboard and go to **Domain Settings** > **Manage Detection Rules** > **Click Fraud Threshold**.
2. **Define Rules:** You can set up to 5 different threshold rules. Specify the number of allowed clicks within a specific timeframe (e.g., 3 clicks within 7 days).
3. **Use Industry Suggestions:** If unsure, use the **Suggested Rules by Industry** feature to set a baseline based on similar businesses.
4. **Save Changes:** Click the **"Update Threshold Rules"** button to apply.

## Advanced Options

- **Advanced Mode (Google Ads):** Enable this under "Manage Detection Rules" to set campaign-level thresholds. IPs blocked for one campaign won't automatically be excluded from the entire account.
- **Campaign Groups:** Create groups to apply different threshold rules to specific traffic types (e.g., brand vs. competitive).
- **Aggressive Blocking:** For severe fraud, enable "Aggressive Blocking" under **Domain Settings** > **Manage Auto IP Blocking**.
- **IP Range Blocking:** Block entire IP ranges or botnets using an asterisk (e.g., `1.2.3.*`) in the "Manage Auto-IP Blocking" tab.

## Best Practices
- **Start Default:** Begin with ClickCease's default settings and let the algorithm adjust.
- **Monitor First:** Monitor traffic initially to prevent blocking legitimate users before activating strict blocks.
- **Avoid "1 Click" Rules:** Unless in extremely high-CPC industries, avoid blocking after a single click, as it may block genuine customers.
