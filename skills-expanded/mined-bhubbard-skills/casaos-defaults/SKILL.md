---
name: casaos-defaults
description: Essential information regarding CasaOS default settings, including first-time setup, default ports, and login credentials (Web UI vs SSH).
---

# CasaOS Defaults & First Setup

When setting up CasaOS for the first time, or troubleshooting login issues, it's critical to understand how CasaOS handles default credentials and networking.

## 1. First-Time Setup (No Default Password)
Unlike many hardware appliances or old router firmware, **CasaOS does not have a default web UI password** (e.g., admin/admin).
- After running the installation script, navigate to your server's local IP address (e.g., `http://192.168.x.x`).
- You will be immediately prompted to **create a new admin account** (username and password).
- This account is exclusively used for the CasaOS Web UI and App Store.

## 2. Web UI vs. SSH Credentials
A common point of confusion is the difference between the Web UI login and the system SSH login.
- **Web UI**: Managed entirely by CasaOS. Uses the account you created during the first setup.
- **SSH (System Login)**: Managed by the underlying Linux OS (e.g., Debian, Ubuntu, ZimaOS). 
  - If you are using a **ZimaBoard**, the default SSH system login is often:
    - **Username**: `casaos`
    - **Password**: `casaos`
  - If you open the "Terminal" app *inside* the CasaOS web UI, it is asking for your **SSH system credentials**, NOT your Web UI password.

## 3. Default Ports
- **Dashboard**: CasaOS runs its web interface on **Port 80** by default.
- If you install a Docker container that also wants to use Port 80 (like a reverse proxy or web server), you will encounter a port conflict.
- **How to change it**: You can change the CasaOS default port (e.g., to 8080) in the top-left Settings menu of the web dashboard.

## 4. Password Recovery
If you forget the Web UI password you created during setup, there is no email recovery.
- You must SSH into the machine and run community reset scripts, or manually delete/edit the CasaOS database file located at `/var/lib/casaos/db/user.db` to trigger the "First Setup" creation screen again.
