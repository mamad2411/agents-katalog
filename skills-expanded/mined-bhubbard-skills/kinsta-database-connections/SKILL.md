---
name: kinsta-database-connections
description: "Instructions for connecting to Kinsta Database Hosting. Use this when the user needs to connect applications to a Kinsta-hosted database (PostgreSQL, MySQL, Redis)."
---

# Kinsta Database Connections

Kinsta provides Database Hosting for PostgreSQL, MySQL, MariaDB, and Redis. Connecting an application to these databases securely is a critical step.

## 1. Internal vs. External Connections
- **Internal Connections**: Use this when connecting a Kinsta-hosted Application to a Kinsta-hosted Database within the same data center. Internal connections are fast, secure, and do not incur egress bandwidth charges.
  - To use internal connections, select "Add internal connection" in the MyKinsta dashboard for the Application.
  - This automatically injects environment variables like `DB_CONNECTION_STRING` into the app.
- **External Connections**: Use this when connecting from your local machine, a third-party app, or a Kinsta app in a different data center.
  - Requires connection details from the "External connections" section in MyKinsta (Host, Port, Username, Password, Database Name).

## 2. Connection Strings (URIs)
- Kinsta provides a standard connection string/URI for easy integration.
- Format typically looks like: `postgresql://user:password@host:port/database`
- Always use the provided URI or properly format it using the individual credentials.

## 3. Security
- Databases on Kinsta are not publicly accessible by default unless an external connection is explicitly enabled.
- External connections should always use SSL/TLS. Download the Kinsta provided CA Certificate if your client requires strict verification.

## 4. Connecting Specific Languages/Frameworks
- **Node.js (Prisma/TypeORM)**: Pass the internal connection string to your ORM via the `DATABASE_URL` environment variable.
- **Python (Django/SQLAlchemy)**: Parse the database URI or map the individual host, user, password, and port variables.
- **PHP (Laravel/WordPress)**: Configure `.env` or `wp-config.php` using the provided database credentials.

## 5. Troubleshooting
- If the connection times out, verify you are using the correct internal vs external hostname.
- Ensure the database is fully provisioned and running before attempting to connect.
