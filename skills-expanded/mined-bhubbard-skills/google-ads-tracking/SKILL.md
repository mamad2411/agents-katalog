---
name: google-ads-tracking
description: Guides the setup and integration of the ClickCease tracking template in Google Ads.
---

# ClickCease Google Ads Tracking Template Integration

This skill provides the steps required to properly integrate the ClickCease tracking template with a Google Ads account. ClickCease uses this template to monitor traffic, gather data, and identify invalid clicks.

## Setup Instructions

### 1. Retrieve the Tracking Template
- Log in to the **ClickCease dashboard**.
- Navigate to **Domain Settings** > **Domain Tracking Setup**.
- Locate the **Tracking Template** section and copy the provided tracking URL code.

### 2. Apply the Template in Google Ads
- Log in to your **Google Ads account**.
- Ensure **Auto-tagging** is enabled in the Account Settings.
- Navigate to **Account Settings** (or at the specific campaign level) and find the **Tracking** section.
- Paste the copied ClickCease code into the **Tracking template** field.
- **Important:** If you are already using other custom parameters, you may need to append the ClickCease parameters or move existing parameters to the "Final URL suffix" field to prevent conflicts.
- Click **Save**.

### 3. Considerations and Merging Platforms
- **HTML Tracking Code:** The tracking template is only part of the setup. Ensure the ClickCease HTML tracking code or plugin is installed on the website's landing pages.
- **SA360 or HubSpot:** If using platforms like SA360, merge your ClickCease template by adding `&t_url={unescapedlpurl}` to the end of the template.
- **Automatic Integration:** Connecting the Google Ads account directly via the ClickCease dashboard's onboarding can often handle configuration automatically.
