---
name: odoo-service
description: |
  Complete Odoo server lifecycle manager — run, deploy, initialize, and manage Odoo across local venv, Docker, and any IDE. Handles server startup/shutdown, environment initialization, database management, Docker orchestration, and IDE configuration for Odoo 14-19.


  <example>
  Context: User wants to start the Odoo server
  user: "Start the Odoo 17 server for my TAQAT project"
  assistant: "I will activate the virtual environment, locate the TAQAT17.conf config, and start the server with the correct addons path."
  <commentary>Server start trigger.</commentary>
  </example>

  <example>
  Context: User wants to stop the server
  user: "Stop the Odoo server"
  assistant: "I will find and kill the process on port 8069/8072."
  <commentary>Server stop trigger.</commentary>
  </example>

  <example>
  Context: User wants database backup
  user: "Backup the taqat17 database"
  assistant: "I will use pg_dump to create a backup of the taqat17 database with custom format."
  <commentary>Database operation trigger.</commentary>
  </example>

  <example>
  Context: User wants IDE configuration
  user: "Set up VSCode for my Odoo 17 project with debug configs"
  assistant: "I will generate .vscode/launch.json, tasks.json, settings.json, and extensions.json with Odoo-specific configurations."
  <commentary>IDE config trigger - generates full VSCode workspace setup.</commentary>
  </example>

  <example>
  Context: User wants to initialize a new environment
  user: "Initialize a new Odoo 17 environment with database"
  assistant: "I will create a venv, install requirements, configure PostgreSQL, generate .conf, and create the database."
  <commentary>Environment init trigger.</commentary>
  </example>

  <example>
  Context: User wants to create a new module
  user: "Create a new module called hr_overtime in the TAQAT project"
  assistant: "I will scaffold a complete module with models, views, security, and tests."
  <commentary>Module scaffold trigger.</commentary>
  </example>

  <example>
  Context: User wants to check if module is production-ready
  user: "Is my module ready for production?"
  assistant: "I will run tests, security audit, translation validation, and template checks to generate a GO/NO-GO verdict."
  <commentary>Quality gate trigger.</commentary>
  </example>
version: "2.0.0"
author: "TaqaTechno"
license: "MIT"
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - Glob
  - Grep
metadata:
  mode: codebase
  odoo-versions: ["14", "15", "16", "17", "18", "19"]
  environments: ["local-venv", "docker", "bare-python"]
  ide-support: ["pycharm", "vscode", "any"]
  categories: [server-management, deployment, database, docker, ide-integration]
---

# Odoo Service Skill

## Capabilities

This skill manages the complete Odoo server lifecycle:

- **Server**: Start, stop, restart, status check (Windows/Linux/macOS)
- **Environment**: Auto-detect venv/Docker/bare Python; initialize new environments
- **Database**: Backup, restore, create, drop, list, reset admin password
- **Docker**: Generate Dockerfiles/compose, manage containers, exec into shells
- **IDE**: Generate VSCode and PyCharm configurations with debug support
- **Module**: Install, update, scaffold, refresh module list
- **Readiness**: Production quality gate (tests, security, translations, manifest)

## Environment Detection

Priority order: Docker > venv > bare Python.

| Signal | Environment |
|--------|-------------|
| `docker-compose.yml` or `Dockerfile` present | Docker |
| `.venv/`, `venv/`, or `env/` with Python executable | Local venv |
| None of the above | Bare Python |

Override with flags: `--docker`, `--venv`, `--env bare`.

## Odoo Version Matrix

| Version | Python | Longpolling Key | Extra Deps |
|---------|--------|----------------|------------|
| 14 | 3.7 - 3.10 | `longpolling_port` | - |
| 15 | 3.8 - 3.11 | `longpolling_port` | - |
| 16 | 3.9 - 3.12 | `gevent_port` | - |
| 17 | 3.10 - 3.13 | `gevent_port` | - |
| 18 | 3.10 - 3.13 | `gevent_port` | cbor2 |
| 19 | 3.10 - 3.13 | `gevent_port` | cbor2, python-magic |

## Quick Reference

### Server

```bash
# Start (dev mode)
python -m odoo -c conf/PROJECT.conf --dev=all

# Start (production)
python -m odoo -c conf/PROJECT.conf --workers=4

# Stop (Windows)
FOR /F "tokens=5" %P IN ('netstat -ano ^| findstr :8069') DO taskkill /PID %P /F

# Stop (Linux/Mac)
lsof -ti:8069 | xargs kill -9
```

### Module Operations

```bash
# Install
python -m odoo -c conf/PROJECT.conf -d DB -i MODULE --stop-after-init

# Update (most common after code changes)
python -m odoo -c conf/PROJECT.conf -d DB -u MODULE --stop-after-init

# Refresh module list (before installing NEW modules)
python -m odoo -c conf/PROJECT.conf -d DB --update-list
```

### Database

```bash
# Backup (compressed custom format - recommended)
pg_dump -U odoo -h localhost -Fc DBNAME -f backups/DBNAME_YYYYMMDD.dump

# Restore
createdb -U odoo NEWDB && pg_restore -U odoo -d NEWDB backup.dump

# Reset admin password
psql -U odoo -d DBNAME -c "UPDATE res_users SET password='newpass' WHERE login='admin';"
```

### Docker

```bash
docker-compose up -d              # Start
docker-compose down               # Stop
docker-compose up -d --build      # Rebuild and start
docker-compose exec odoo bash     # Shell into container
```

## Scripts

Located in `odoo-service/scripts/` — all standalone, stdlib-only (optional `psutil`):

| Script | Purpose |
|--------|---------|
| `server_manager.py` | Start/stop/restart/status, module install/update |
| `env_initializer.py` | Venv creation, PostgreSQL check, config generation |
| `db_manager.py` | Backup/restore/create/drop, admin password reset |
| `docker_manager.py` | Dockerfile/compose generation, container lifecycle |
| `ide_configurator.py` | VSCode/PyCharm config generation |

## Config File Format

```ini
[options]
addons_path = odoo/addons,projects/PROJECTNAME
admin_passwd = 123
db_host = localhost
db_port = 5432
db_user = odoo
db_password = odoo
dbfilter = PROJECTNAME.*
http_port = 8069
gevent_port = 8072
workers = 0
```

Naming convention: `conf/{PROJECT}{VERSION}.conf` (e.g., `conf/myproject17.conf`).
