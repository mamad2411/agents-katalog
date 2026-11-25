---
name: localwp-installation
description: Guide to installing and setting up LocalWP across different operating systems and configuring initial preferences.
---

# LocalWP Installation and Setup

This skill provides guidance on installing and configuring LocalWP for local WordPress development.

## 1. System Requirements
- **macOS**: 10.15 (Catalina) or later. Intel or Apple Silicon (native builds available).
- **Windows**: Windows 10 or later.
- **Linux**: Debian/Ubuntu-based distributions (deb) or Red Hat-based distributions (rpm).

## 2. Installation Steps
1. Download the appropriate installer for your OS from the [LocalWP website](https://localwp.com/).
2. Run the installer:
   - **macOS**: Mount the DMG and drag Local to the Applications folder.
   - **Windows**: Run the `.exe` installer and follow the wizard.
   - **Linux**: Install via your package manager (e.g., `sudo apt install ./local-*.deb`).

## 3. Initial Configuration
When launching LocalWP for the first time:
- You may be prompted to accept terms of service.
- **Error Reporting**: Choose whether to send error reports to help improve Local.
- **Create Account**: You can log in or create a Local account to enable features like Live Links and Cloud Backups, but it is not strictly required for local development.

## 4. Advanced Preferences
Go to **Preferences** (Local > Preferences on macOS, or the hamburger menu on Windows/Linux):
- **New Site Defaults**: Set default admin email, password suffix, environment (Preferred or Custom), and site path. This speeds up future site creation.
- **Router Mode**:
  - **Site Domains** (Default): Uses `*.local` domains (e.g., `mysite.local`). Requires Local to have administrative privileges to edit the `hosts` file.
  - **localhost**: Uses `localhost:port` (e.g., `localhost:10004`). Good for environments where you don't have admin privileges or if conflicting software blocks port 80/443.
- **Advanced**: Option to toggle "Show Router Logs" or adjust how Local handles the `hosts` file.

## 5. Troubleshooting Common Installation Issues
- **Port Conflicts**: If another application (like Skype, MAMP, or IIS) is using port 80 or 443, Local will complain or fail to start the site. Solution: Find the conflicting app and stop it, or switch Local's Router Mode to "localhost".
- **Hosts File Permissions**: Antivirus software (especially on Windows) can block edits to the `hosts` file. You may need to whitelist Local in your antivirus settings.
- **Missing Visual C++ Redistributable (Windows)**: Some PHP versions require specific Visual C++ runtimes. Download and install them from Microsoft if prompted.
