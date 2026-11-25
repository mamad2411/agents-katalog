---
name: casaos-docker-compose
description: Using custom Docker Compose configurations in CasaOS to deploy unlisted applications and manage multi-container stacks.
---

# Advanced App Deployment in CasaOS

While the CasaOS App Store is convenient, you may need to host applications that are not listed or require complex, multi-container configurations. CasaOS fully supports standard Docker Compose files, allowing you to deploy anything the Docker ecosystem has to offer.

## 1. Using the Custom Install Feature
CasaOS provides a UI for importing Docker Compose files directly.
1. Open the **App Store** and click the **Custom Install** button (usually at the top right).
2. Look for the "Import" button to paste a raw `docker-compose.yml` file.
3. CasaOS will parse the YAML and attempt to fill in the UI fields automatically.
4. **App Icon**: Add a URL to a `.png` or `.svg` icon so it looks native on the CasaOS dashboard.

## 2. Managing Volumes and Bind Mounts
When writing Docker Compose files for CasaOS, it is crucial to map volumes correctly.
- Use absolute paths that point to your mounted drives.
- **Default Storage Path**: CasaOS usually mounts extra drives under `/DATA/` or `/media/devmon/`.
- **Example**:
  ```yaml
  volumes:
    - /DATA/AppData/myapp:/config
    - /DATA/Media/Movies:/movies
  ```

## 3. Command Line Management
Because CasaOS simply wraps the standard Docker engine, you can bypass the UI entirely if needed.
- SSH into the ZimaBoard.
- Create a directory for your stack: `mkdir -p /DATA/AppData/mystack`.
- Create a `docker-compose.yml` file inside the directory.
- Run `docker compose up -d`.
- *Note: Containers started via CLI will still appear in the CasaOS UI as generic widgets, but their configuration cannot be edited via the UI.*

## 4. Troubleshooting
- **Port Conflicts**: Ensure the ports specified in your compose file do not conflict with CasaOS itself (e.g., port 80).
- **Permissions**: If a container fails to start, verify that the UID/GID specified in the compose file has read/write access to the bind-mounted directories.
