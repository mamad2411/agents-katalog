---
name: tracking-script-installation
description: Guides the installation of the ClickCease tracking script on HTML websites and WordPress.
---

# ClickCease Tracking Script Installation

This skill covers the installation of the ClickCease tracking script to ensure proper tracking and bot zapping. It provides options for both WordPress and standard HTML setups.

## Option 1: WordPress Plugin (Recommended for WP)

Using the plugin is the simplest method and avoids manual edits to theme files.

1. Log in to the **WordPress Admin Dashboard**.
2. Navigate to **Plugins** > **Add New**.
3. Search for **"ClickCease"**.
4. Click **Install Now** and then **Activate**.
5. Go to the **ClickCease** menu in the dashboard.
6. Under "ClickCease Paid Marketing", click **Activate**.
   - *Note: For Bot Zapping, ensure you have your Authentication, Secret, and Domain keys from the ClickCease dashboard.*

## Option 2: Manual HTML Installation

If not using WordPress or preferring manual installation, follow these steps:

1. **Get the Tracking Code:** Log in to the ClickCease dashboard, go to **Domain Settings** > **Domain Tracking Setup**, and copy the tracking code.
2. **Access Website Files:** Open the source code of your website. For WordPress, this is usually the `header.php` file under **Appearance** > **Theme Editor**.
3. **Insert Code:** Locate the `<body>` tag in the HTML. Paste the ClickCease tracking code immediately **after** the opening `<body>` tag.
4. **Save:** Update the file to save changes.

## Important Tips
- **Avoid Duplicates:** Do not install the script both manually and via the plugin. Use one method.
- **Troubleshooting WordPress:** If you get an error saving `header.php`, temporarily deactivate security plugins.
- **Verification:** Always verify that the script is firing correctly by checking the ClickCease dashboard.
