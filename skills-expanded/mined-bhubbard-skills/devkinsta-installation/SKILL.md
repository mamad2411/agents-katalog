---
name: devkinsta-installation
description: Guide for installing and setting up Kinsta's DevKinsta local development environment.
---

# DevKinsta Installation

DevKinsta is a local development suite for WordPress sites. It uses Docker behind the scenes to run Nginx, PHP, and MariaDB containers.

## System Requirements
- **macOS**: macOS 10.14 or higher. Intel or Apple Silicon (via Rosetta 2 for some older Docker images, though native is increasingly supported).
- **Windows**: Windows 10/11 Pro, Enterprise, or Education (Hyper-V required) or WSL2.
- **Ubuntu**: Modern Ubuntu distribution.
- **Docker**: DevKinsta will attempt to install Docker Desktop if it is not already installed.

## Installation Steps
1. Download DevKinsta from the official Kinsta website (`https://kinsta.com/devkinsta/`).
2. Run the installer for your OS.
3. Open DevKinsta. On the first launch, it will download the necessary Docker images (PHP, Nginx, MariaDB, etc.). This may take some time depending on network speed.
4. If prompted, grant Docker the necessary permissions to bind to ports (80, 443).
5. Once initialization is complete, you can click "New WordPress site" to begin developing locally.

## Troubleshooting
- **Docker Issues**: Ensure Docker Desktop is running and has sufficient resources allocated (RAM/CPU).
- **Port Conflicts**: Ensure no other local servers (like MAMP, XAMPP, or Valet) are listening on ports 80 or 443.
