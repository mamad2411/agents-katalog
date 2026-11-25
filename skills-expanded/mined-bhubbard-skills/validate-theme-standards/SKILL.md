---
name: validate-theme-standards
description: Use Theme Check to ensure a classic theme complies with WordPress.org review standards.
---

# Validate Theme Standards

Theme Check runs automated tests to verify a theme's compliance with the Theme Review guidelines.

## Process
1. Go to the Theme Check menu in the WordPress Admin.
2. Select your theme and run the checks.
3. Review the output:
    - **Required**: Must be fixed before submission to the directory.
    - **Warning/Recommended**: Best practices that should be considered.
4. Correct any flags related to deprecated functions, missing `wp_head()` or `wp_footer()` calls, and proper escaping.
