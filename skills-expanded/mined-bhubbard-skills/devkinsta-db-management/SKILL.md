---
name: devkinsta-db-management
description: Database management using DevKinsta's built-in tools.
---

# DevKinsta Database Management

DevKinsta utilizes MariaDB to run local WordPress databases. It provides a lightweight, built-in database manager (Adminer) for quick edits, but you can also connect using external database tools.

## Using the Built-in Database Manager
1. Open DevKinsta and navigate to your site's info page.
2. Locate the **Database** section.
3. Click the **Database Manager** button. 
4. This will open Adminer in your default web browser. You do not need to manually enter credentials; DevKinsta auto-logs you in.
5. From here, you can run SQL queries, modify rows, import/export `.sql` files, and manage tables.

## Connecting with External Database Tools
If you prefer a more robust tool like TablePlus, DBeaver, or Sequel Ace, you can connect directly to the DevKinsta MariaDB container:
1. Go to your site's info page in DevKinsta.
2. In the **Database** section, look for the connection details:
   - **Host**: Usually `127.0.0.1` or `localhost`.
   - **Port**: A dynamically mapped port assigned by Docker (e.g., `15100`).
   - **Database Name**: The specific name of the site's database.
   - **Username**: Usually `root`.
   - **Password**: The password provided in the DevKinsta UI.
3. Open your external client, enter these credentials, and connect.

## Importing and Exporting
- **Importing**: Use Adminer or your external tool to import an existing `.sql` dump. Ensure the file size does not exceed PHP upload limits if using Adminer.
- **Exporting**: You can export the database before making risky changes or to prepare for migration.
