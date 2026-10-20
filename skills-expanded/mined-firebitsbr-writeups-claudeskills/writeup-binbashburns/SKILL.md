<!--
LICENSE UPL
Author: Mauro Risonho de Paula Assumpção
Data Create: 2026-03-16
Data Update: 2026-03-16
-->

---
name: writeup-binbashburns
description: CTF writeups and security challenges by binbashburns.
---

# Writeups by binbashburns

Source repository: `/repos/binbashburns`

## Repository Index

- recon2report/README.md
- recon2report/adrs/0000-architecture-overview.md
- recon2report/adrs/0001-adding-services.md
- recon2report/adrs/0002-web-frontend.md
- recon2report/adrs/0003-web-ui-development.md
- recon2report/assets/TESTING-EVIDENCE.md

## Writeup Content


### File: recon2report/README.md

# recon2report ⓡ②ⓡ
![img1](./assets/r2r-logo.png)

Better pentesting, from reconnaissance to reporting.

## Project Purpose

recon2report transforms Nmap scan results into context-aware penetration testing commands. The system automatically suggests relevant attack vectors based on detected services, current penetration testing phase, and acquired access.

**Phase 1 Scope**: CLI and web UI workflows with intelligent attack path suggestions. All data is stored in-memory (no persistence). Future phases will add persistent storage and report generation.

## Getting Started

### Option 1: Web Interface (Recommended)

1. Start the API:
   ```bash
   dotnet run --project R2R.Api
   ```
   API runs on `http://localhost:5258`

2. Start the web frontend (in a separate terminal):
   ```bash
   cd R2R.Web
   npm install
   npm run dev
   ```
   Web UI opens at `http://localhost:5173`

3. Use the browser interface to:
   - Create sessions and targets
   - Get Nmap scan suggestions
   - Paste scan results
   - View parsed ports from multiple hosts
   - Explore attack vectors by phase

### Screenshots:

#### Session creation and Nmap suggestions
<p align="center">
  <img src="./assets/web-session.png" alt="Web UI Session Form" width="800">
</p>

#### Multi-host scan results with nested ports
<p align="center">
  <img src="./assets/web-ports.png" alt="Web UI Parsed Ports" width="800">
</p>

#### Phase-based attack suggestions
<p align="center">
  <img src="./assets/web-vectors.png" alt="Web UI Attack Vectors" width="800">
</p>

### Option 2: CLI Workflow

1. Start the API in one terminal:
   ```bash
   dotnet run --project R2R.Api
   ```
   
2. Launch the CLI in a separate terminal:
   ```bash
   dotnet run --project R2R.Cli
   ```

3. Follow the prompts to create a session, run Nmap scans, and get attack suggestions.

All data lives in memory; restarting the API clears it.

> **For Web UI development setup, configuration, and troubleshooting**, see [adrs/0003-web-ui-development.md](./adrs/0003-web-ui-development.md)

## Attack Path System

The system uses **service-based JSON files** in `/services/` to define attack paths dynamically. This allows you to maintain attack techniques without changing code, with better organization and performance.

### How It Works
1. **Nmap scan** detects open ports and services on target
2. **Port-to-service mapping** loads only relevant JSON files
   - Port 445 → Load `smb.json`
   - Port 80/443 → Load `http.json`
   - Port 389 → Load `active-directory.json`
   - Always load `network-general.json`
3. **Rule engine** filters vectors by:
   - **Phase** (reconnaissance → credential_access → lateral_movement → privilege_escalation → persistence)
   - **Prerequisites** (what you've already obtained)
   - **Target OS** (Windows/Linux/Any)
4. **Variable substitution** fills in `<ip>`, `<domain>`, `<ip_range>` placeholders with real values

### Service-Based Architecture

Attack vectors are organized by service/protocol rather than by phase:

```
services/
├── Network Services
│   ├── smb.json          # SMB/CIFS attacks (ports 445, 139)
│   ├── http.json         # Web attacks (ports 80, 443, 8080)
│   ├── dns.json          # DNS attacks (port 53)
│   ├── ldap.json         # LDAP attacks (ports 389, 636)
│   ├── kerberos.json     # Kerberos attacks (port 88)
│   ├── ssh.json          # SSH attacks (port 22)
│   ├── rdp.json          # RDP attacks (port 3389)
│   ├── winrm.json        # WinRM attacks (ports 5985, 5986)
│   ├── ftp.json          # FTP attacks (port 21)
│   └── network-general.json  # Network-level attacks
│
├── Active Directory
│   ├── active-directory.json  # ACLs, delegation, trusts
│   ├── adcs.json              # Certificate Services (ESC1-ESC15)
│   └── sccm.json              # SCCM/MECM exploitation
│
├── Windows
│   ├── windows-admin.json      # Credential extraction
│   ├── windows-privesc.json    # Local privilege escalation
│   └── windows-persistence.json # Persistence mechanisms
│
└── Techniques
    ├── vulnerabilities.json     # Known CVE exploits
    ├── password-cracking.json   # Hash cracking
    └── ntlm-relay.json          # NTLM relay attacks
```

### JSON Schema

Each service file follows this structure:

```json
{
  "service": "smb",
  "description": "SMB/CIFS attacks for Windows file sharing",
  "ports": [139, 445],
  "serviceNames": ["microsoft-ds", "netbios-ssn"],
  "targetOs": ["windows"],
  "vectors": [
    {
      "id": "smb-anonymous-enum",
      "name": "Anonymous SMB Enumeration",
      "phase": "reconnaissance",
      "prerequisites": ["network_access"],
      "description": "Enumerate SMB shares without authentication",
      "commands": [
        {
          "tool": "smbclient",
          "command": "smbclient -L //<ip> -N",
          "description": "List SMB shares anonymously"
        }
      ],
      "outcomes": ["information_gathered"]
    }
  ]
}
```

### Example: HTTP-Only Host

**Scenario**: Nmap detects ports 80 and 443 open

**System loads**: `http.json`, `network-general.json` (only 2 files instead of all services)

**Filters by phase**: `reconnaissance` (initial stage)

**Returns vectors**:
- Web Service Discovery
- Directory Bruteforcing  
- Vulnerability Scanning
- Network Discovery
- LLMNR Poisoning


### Kill Chain Phases

Attack paths follow standard penetration testing methodology:

1. **reconnaissance** - Initial discovery, no credentials required
2. **credential_access** - Obtaining credentials (bruteforce, poisoning, etc.)
3. **lateral_movement** - Moving through network with valid credentials
4. **privilege_escalation** - Elevating privileges
5. **persistence** - Maintaining access

### Benefits

-  **Simple Logic** - No complex port filtering in code, just load relevant files
-  **Fast Performance** - Only parse 2-4 relevant services instead of all attack vectors
-  **Easy Maintenance** - All SMB attacks in one place, edit JSON without touching code
-  **Accurate Filtering** - Port-based loading prevents irrelevant suggestions
-  **Machine Readable** - JSON is structured, parseable, and efficient
-  **Clear Dependencies** - Prerequisites explicitly defined in each vector

## API Surface
| Method & Path            | Description                                              |
| ------------------------ | -------------------------------------------------------- |
| `POST /sessions`         | Creates a new recon session.                             |
| `GET /sessions/{id}`     | Fetches a previously created session.                    |
| `DELETE /sessions/{id}`  | Removes a session (and implicitly its targets).          |
| `POST /targets`          | Adds a target tied to a session.                         |
| `GET /targets/{id}`      | Retrieves target metadata.                               |
| `PUT /targets/{id}`      | Updates target details.                                  |
| `DELETE /targets/{id}`   | Deletes a target.                                        |
| `POST /targets/{id}/scan`| Uploads and stores parsed Nmap scan results for a target.|
| `GET /targets/{id}/scan` | Retrieves stored scan results for a target.              |
| `POST /nmap/suggest`     | Returns curated Nmap commands for the given IP/OS.       |
| `POST /nmap/parse`       | Parses Nmap "normal" output into `OpenPort` records.     |
| `POST /attack-paths/suggest` | **NEW**: Suggests attack vectors based on current phase, ports, and services using markdown rule sets. |

## Running Tests
```bash
dotnet test
```

## Project Layout
```
R2R.Api/                  Minimal API (endpoints + helpers)
R2R.Cli/                  Console workflow client
R2R.Web/                  Static web frontend (Vite + Vanilla JS)
  ├── index.html         Single-page application
  ├── main.js            Application logic and API integration
  ├── style.css          Custom styling
  └── package.json       Vite dev server
R2R.Core.Domain/          Domain models (AttackVector, Command, Outcome, ServiceRuleSet, AttackState)
R2R.Core.Parsing/         JSON parser for service rule files
R2R.Core.Rules/           Service-aware rule engine for evaluating attack states
R2R.Tests/                xUnit test project
services/                 JSON files defining service-based attack vectors
  ├── smb.json           SMB/CIFS attacks
  ├── http.json          Web application attacks
  ├── active-directory.json  AD attacks (ACLs, delegation, trusts)
  ├── adcs.json          Certificate Services attacks
  ├── vulnerabilities.json   Known CVE exploits
  └── ...                19 service files total
adrs/                     Architecture Decision Records
  ├── 0000-architecture-overview.md
  ├── 0001-adding-services.md
  ├── 0002-web-frontend.md
  └── 0003-web-ui-development.md
```

## Troubleshooting
- **403 from CLI**: Ensure the API is running and that `R2R_API_BASE` matches its URL (defaults to `http://localhost:5258/`).
- **Web UI issues**: See [Web UI Development Guide](./adrs/0003-web-ui-development.md#common-issues) for CORS errors, port conflicts, and configuration.
- **Swagger/Swashbuckle build errors**: The project relies on `Microsoft.AspNetCore.OpenApi` only; make sure no other Swagger packages are referenced.
- **dotnet test errors**: Confirm the API project builds; missing types are usually due to visibility changes in `Program.cs`.

## License

This project is licensed under the **Business Source License 1.1 (BSL)**. See [LICENSE](./LICENSE) for full text.

**Summary**:
- Free for testing, development, and educational use
- Free for penetration testing labs and CTF competitions
- NOT for production use without a commercial license
- Converts to Apache 2.0 license after 4 years

## Safety Warning

**FOR AUTHORIZED TESTING ONLY**

This tool is designed for:
- Penetration testing labs (HackTheBox, TryHackMe, OSCP)
- CTF competitions
- Security research and education
- Authorized penetration testing engagements with written permission

**NEVER use this tool against systems you don't own or have explicit written permission to test.** Unauthorized access to computer systems is illegal.



### File: recon2report/adrs/0000-architecture-overview.md

# ADR 0000: Architecture Overview

**Status**: Accepted  
**Date**: 2025-10-31  
**Deciders**: @binbashburns

## Context

Penetration testers need a structured way to move from reconnaissance data (Nmap scans) to actionable attack commands, with context-aware suggestions based on what services are running and what access has been obtained.

## Decision

We will build **recon2report** as a service-based attack path suggestion system with these architectural principles:

### Core Architecture

```
┌─────────────────┐
│   R2R.Cli       │  Interactive CLI for pentesters
│  (Console UI)   │
└────────┬────────┘
         │ HTTP
         ▼
┌─────────────────┐
│   R2R.Api       │  RESTful API (ASP.NET Core Minimal API)
│  (HTTP Server)  │
└────────┬────────┘
         │
    ┌────┴────┐
    ▼         ▼
┌─────────┐ ┌──────────────┐
│ Parsing │ │ Rule Engine  │
└─────────┘ └──────────────┘
    │              │
    ▼              ▼
┌──────────────────────────┐
│  Service JSON Files      │
│  (smb.json, http.json)   │
└──────────────────────────┘
```

### Key Components

1. **Domain Layer** (`R2R.Core.Domain`)
   - Pure domain models: `AttackVector`, `Command`, `Outcome`, `ServiceRuleSet`
   - No dependencies on infrastructure

2. **Parsing Layer** (`R2R.Core.Parsing`)
   - Loads JSON service definitions from disk
   - Converts DTOs to domain models

3. **Rules Layer** (`R2R.Core.Rules`)
   - `ServiceRuleEngine` filters attack vectors based on:
     - Open ports (only loads relevant services)
     - Current phase (reconnaissance → privilege_escalation)
     - Prerequisites (what items have been acquired)
     - Target OS (Windows/Linux/Any)

4. **API Layer** (`R2R.Api`)
   - Exposes RESTful endpoints
   - In-memory data storage (sessions, targets, scan results)
   - Variable substitution for commands (`<ip>`, `<domain>`, etc.)

5. **CLI Layer** (`R2R.Cli`)
   - Interactive terminal workflow
   - Guides user through scan → parse → suggest cycle

### Service-Based Organization

Attack vectors are organized by **service/protocol** rather than by phase:

- **Port-to-service mapping**: Port 445 → Load `smb.json` only
- **Lazy loading**: Only parse relevant JSON files
- **Clean separation**: All SMB attacks in one file, easy to maintain

## Consequences

### Positive
-  Fast performance (only loads 2-4 services per scan)
-  Easy to maintain (edit JSON without touching code)
-  Accurate suggestions (no irrelevant attack vectors)
-  Testable (clear separation of concerns)

### Negative
-  Requires discipline to keep JSON files well-organized
-  No persistence (in-memory only for Phase 1)

## References
- Service JSON schema in ADR 0001
- Adding new services in ADR 0001



### File: recon2report/adrs/0001-adding-services.md

# ADR 0001: Adding New Services

**Status**: Accepted  
**Date**: 2025-10-31  
**Deciders**: @binbashburns

## Context

As new protocols and attack techniques emerge, we need a straightforward way to add them to the system without modifying application code.

## Decision

All attack vectors are defined in **JSON service files** under `/services/`. Each file represents a single service or protocol (e.g., SMB, HTTP, Kerberos).

## JSON Schema

```json
{
  "service": "string",              // Service name (e.g., "SMB", "HTTP")
  "description": "string",          // Brief description
  "ports": [int, int],              // Ports this service runs on
  "serviceNames": ["string"],       // Nmap service names that match
  "targetOs": ["string"],           // "Windows", "Linux", or "Any"
  "vectors": [
    {
      "id": "string",               // Unique identifier (kebab-case)
      "name": "string",             // Display name
      "phase": "string",            // "reconnaissance", "credential_access", etc.
      "prerequisites": ["string"],  // What you need to run this (e.g., ["network_access"])
      "description": "string",      // What this vector does
      "commands": [
        {
          "tool": "string",         // Tool name (e.g., "nmap", "smbclient")
          "syntax": "string",       // Command with placeholders (<ip>, <domain>)
          "description": "string"   // What this command does
        }
      ],
      "outcomes": ["string"]        // What you might obtain (e.g., ["credentials", "admin_access"])
    }
  ]
}
```

## Adding a New Service

### 1. Create the JSON file

```bash
touch services/new-service.json
```

### 2. Define the service metadata

```json
{
  "service": "PostgreSQL",
  "description": "PostgreSQL database attacks",
  "ports": [5432],
  "serviceNames": ["postgresql"],
  "targetOs": ["Any"],
  "vectors": []
}
```

### 3. Add attack vectors

Each vector represents a specific technique:

```json
{
  "id": "psql-default-creds",
  "name": "PostgreSQL Default Credentials",
  "phase": "credential_access",
  "prerequisites": ["network_access"],
  "description": "Test for default PostgreSQL credentials",
  "commands": [
    {
      "tool": "psql",
      "syntax": "psql -h <ip> -U postgres -W",
      "description": "Connect with default postgres user"
    }
  ],
  "outcomes": ["database_access"]
}
```

### 4. Test your service

The API automatically loads all JSON files from `/services/` at startup. Check the console output:

```
Loaded 20 service rule set(s)
  ✓ PostgreSQL: 1 vectors (Ports: 5432)
```

### 5. Verify in Swagger

Use the `/debug/services` endpoint to see all loaded services and their vectors.

## Variable Substitution

The API automatically replaces these placeholders in command syntax:

| Placeholder | Replaced With | Example |
|-------------|---------------|---------|
| `<ip>`, `<target>` | Target IP address | `192.168.1.10` |
| `<domain>` | Domain name | `CORP.LOCAL` |
| `<ip_range>` | IP range | `192.168.1.0/24` |
| `<port>` | Detected open port(s) | `80` or `80,443` |

## Phase Definitions

| Phase | Description | Examples |
|-------|-------------|----------|
| `reconnaissance` | Initial discovery, no credentials | Port scanning, DNS enumeration |
| `credential_access` | Obtaining credentials | Password spraying, hash dumping |
| `lateral_movement` | Moving through network | Pass-the-hash, remote execution |
| `privilege_escalation` | Elevating privileges | UAC bypass, kernel exploits |
| `persistence` | Maintaining access | Backdoors, scheduled tasks |

## Best Practices

###  Do
- Group related attacks in one service file
- Use descriptive `id` values (kebab-case)
- Include helpful `description` fields
- Test your JSON for validity

###  Don't
- Mix multiple unrelated services in one file
- Hardcode IP addresses or domains in commands
- Leave out `prerequisites` (use `[]` for no requirements)
- Forget to specify `targetOs` (use `["Any"]` if applicable)

## Example: Complete Service File

See `/services/smb.json` for a production example with:
- Anonymous enumeration
- Authenticated enumeration
- Vulnerability scanning
- Relay attacks
- Share access

## Consequences

### Positive
-  Non-developers can add new attacks
-  No code changes or recompilation needed
-  Easy to share attack definitions between teams
-  Git-friendly (JSON diffs are readable)

### Negative
-  Must maintain JSON schema consistency
-  No compile-time checking of syntax errors



### File: recon2report/adrs/0002-web-frontend.md

# ADR 0002: Web Frontend

**Status**: Accepted  
**Date**: 2025-10-31  
**Deciders**: @binbashburns

## Overview

Added a static web frontend using Vite + Vanilla JavaScript. Provides visual interface for creating sessions, viewing scan results, and exploring attack vectors.

## Implementation

### Stack

- **Vite** - Dev server and build tool
- **Vanilla JavaScript** - No framework dependencies
- **Custom CSS** - CSS variables for theming
- **Fetch API** - HTTP requests to R2R.Api

### Architecture

```
┌──────────────┐         ┌──────────────┐
│  R2R.Web     │  HTTP   │   R2R.Api    │
│  (Vite)      ├────────→│  (.NET 9)    │
│  Port 5173   │  CORS   │  Port 5258   │
└──────────────┘         └──────────────┘
```

### Running the Frontend

```bash
cd R2R.Web
npm install
npm run dev
```

Browser opens at `http://localhost:5173`

### Project Structure

```
R2R.Web/
├── index.html       # Single-page app structure
├── main.js          # API integration and UI logic
├── style.css        # Styling with CSS variables
└── package.json     # Vite dependency
```

### Screens

1. **Session + Target Form** - Create session with IP/OS
2. **Nmap Suggestions** - Show scan commands from API (`/nmap/suggest`)
3. **Paste Nmap XML** - Upload scan results
4. **Parsed Ports** - Display all hosts with nested port lists, per-host attack vector buttons
5. **Attack Suggestions** - Show phase-based vectors for selected host (`/attack-paths/suggest`)
6. **Attack Vector Reference** - Dictionary view of all vectors by phase with raw syntax (`/attack-paths/all`)

### Key Features

- **Multi-host support** - Single scan displays all discovered hosts
- **Per-host attack vectors** - Each host has its own "Get Attack Vectors" button
- **Reference dictionary** - Browse all attack vectors without filtering by target
- **Nested port display** - Each host card shows ports, services, versions
- **Phase selector** - Switch between recon/creds/lateral/privesc/persistence
- **Click-to-copy** - Copy commands to clipboard
- **Variable substitution** - Commands use actual IPs (not `<ip>` placeholders)

### API Endpoints Used

- `POST /sessions` - Create session
- `POST /targets` - Create target
- `POST /nmap/suggest` - Get scan commands
- `POST /targets/{id}/scan` - Upload Nmap XML
- `POST /attack-paths/suggest` - Get filtered attack vectors for specific host
- `GET /attack-paths/all?phase={phase}` - Get all vectors for reference mode

## Notes

- CORS configured in API for `http://localhost:5173`
- Refreshing page loses state (matches in-memory API design)
- Reference page shows raw command syntax with `<target>`, `<domain>` placeholders
- Attack suggestions page substitutes actual values into commands
- Multi-host scans display all hosts; attack suggestions use first host by default

## Future

- Target selector for multi-host attack suggestions
- Export to markdown/PDF
- Session persistence
- Dark mode

## References

- [ADR 0000: Architecture Overview](./0000-architecture-overview.md)
- [Vite Documentation](https://vitejs.dev/)



### File: recon2report/adrs/0003-web-ui-development.md

# Web UI Development Guide

## Quick Start (< 5 minutes)

1. **Start the API** (Terminal 1):
   ```bash
   cd R2R.Api
   dotnet run
   ```
   - API runs on: `http://localhost:5258`
   - Swagger UI: `http://localhost:5258/swagger`

2. **Start the Web UI** (Terminal 2):
   ```bash
   cd R2R.Web
   npm install  # First time only
   npm run dev
   ```
   - Web UI runs on: `http://localhost:5173`
   - Opens automatically in your browser

3. **Test the workflow**:
   - Create a session and target
   - Get Nmap suggestions
   - Paste scan XML results
   - View attack vectors

## Configuration

### API URL
The frontend connects to the API at `http://localhost:5258`. To change this:

**File**: `R2R.Web/main.js`
```javascript
const API_BASE = 'http://localhost:5258';  // Line 1
```

### CORS Origins
The API allows requests from `http://localhost:5173` by default.

**File**: `R2R.Api/Program.cs` (lines 13-19)
```csharp
builder.Services.AddCors(options =>
{
    options.AddPolicy("AllowFrontend", policy =>
    {
        policy.WithOrigins("http://localhost:5173")  // Add more origins here
              .AllowAnyHeader()
              .AllowAnyMethod();
    });
});
```

To allow multiple origins (e.g., production deployment):
```csharp
policy.WithOrigins(
    "http://localhost:5173",
    "https://your-domain.com"
)
```

### Vite Dev Server Port
To change the frontend port from 5173:

**File**: `R2R.Web/vite.config.js` (create if missing)
```javascript
import { defineConfig } from 'vite'

export default defineConfig({
  server: {
    port: 3000  // Your preferred port
  }
})
```

**Remember**: Update CORS origins in the API if you change the frontend port!

## Development Workflow

**Hot Reload**: Both API and frontend support hot reload
- API: Watches for file changes (dotnet watch)
- Frontend: Vite auto-refreshes on save

**Run with hot reload**:
```bash
# Terminal 1 - API with auto-reload
cd R2R.Api
dotnet watch run

# Terminal 2 - Frontend (already has hot reload)
cd R2R.Web
npm run dev
```

## Common Issues

| Issue | Solution |
|-------|----------|
| CORS errors in browser console | Verify API is running and frontend URL matches CORS policy |
| "Failed to fetch" errors | Check API is running on `http://localhost:5258` |
| Web UI shows blank screen | Run `npm install` in R2R.Web, check browser console for errors |
| Port 5173 already in use | Change Vite port in `vite.config.js`, update CORS in API |
| Swagger not loading | Navigate to `http://localhost:5258/swagger` (not /swagger/index.html) |

## Production Build

```bash
cd R2R.Web
npm run build
```
- Outputs to `R2R.Web/dist/`
- Optimized, minified assets
- Serve with any static file server (Nginx, Apache, etc.)

## Architecture

### Frontend Stack
- **Vite**: Fast dev server with hot module replacement
- **Vanilla JavaScript**: No framework dependencies, simple and fast
- **CSS Variables**: Centralized theming for consistent UI

### State Management
- Single `state` object tracks sessions, targets, hosts, and context
- `hostContexts` object stores per-host information (credentials, OS, notes)
- No external state management library needed

### Navigation
- Single-page application with 7 screens
- Two-tier navigation: Main nav + sub-nav for workflow screens
- `goToScreen()` function manages screen transitions

### API Integration
- All API calls use native `fetch()`
- Base URL configurable via `API_BASE` constant
- Automatic variable substitution for attack commands

### Features
- Multi-host support with individual attack vector buttons
- Service-grouped attack vectors (DNS, SMB, HTTP sections)
- Click-to-copy for all commands
- Host context tracking (credentials, domain info, notes)
- Reference dictionary mode for all attack vectors
- Phase-aware filtering



### File: recon2report/assets/TESTING-EVIDENCE.md

# Testing Evidence Upload

## Quick Test with Swagger

The POST /evidence endpoint in Swagger already includes a working example with a small test image.

1. Start the API: `dotnet run --project R2R.Api`
2. Open Swagger: `http://localhost:5258/swagger`
3. Expand `POST /evidence`
4. Click "Try it out"
5. The example request is pre-filled with:
   - A valid target ID (you'll need to create a session and target first)
   - A valid base64 PNG image
   - A stage and caption

## Using Real Screenshots

### Option 1: Convert Script (Recommended)

Use the provided script to convert any image:

```bash
cd assets
chmod +x convert-to-base64.sh
./convert-to-base64.sh your-screenshot.png
```

This creates a `.json` file ready to paste into Swagger:
- Validates image size (warns if > 5MB)
- Validates image type (PNG, JPG, GIF)
- Outputs properly formatted JSON

### Option 2: Manual Conversion

**macOS/Linux:**
```bash
base64 -i screenshot.png | tr -d '\n' > base64.txt
```

**Windows (PowerShell):**
```powershell
[Convert]::ToBase64String([IO.File]::ReadAllBytes("screenshot.png")) > base64.txt
```

Then format as:
```
data:image/png;base64,{paste base64.txt contents here}
```

## Testing Workflow

### 1. Create Session
```bash
curl -X POST http://localhost:5258/sessions \
  -H "Content-Type: application/json" \
  -d '{"name": "Test Session", "ipRange": "192.168.1.0/24"}'
```
Save the returned `id` (session ID).

### 2. Create Target
```bash
curl -X POST http://localhost:5258/targets \
  -H "Content-Type: application/json" \
  -d '{"sessionId": "YOUR_SESSION_ID", "ip": "192.168.1.10", "os": "Windows"}'
```
Save the returned `id` (target ID).

### 3. Upload Evidence
Use the target ID in your evidence request:
```bash
curl -X POST http://localhost:5258/evidence \
  -H "Content-Type: application/json" \
  -d @screenshot.json
```

### 4. Retrieve Evidence
```bash
# Get single evidence
curl http://localhost:5258/evidence/EVIDENCE_ID

# Get all evidence for target
curl http://localhost:5258/targets/TARGET_ID/evidence

# Get all evidence for session
curl http://localhost:5258/sessions/SESSION_ID/evidence
```

## Valid Stages

Evidence must have one of these stages (matching OSCP report structure):
- `information_gathering`
- `enumeration`
- `exploitation`
- `privilege_escalation`
- `post_exploitation`
- `maintaining_access`
- `house_cleaning`

## Size Limits

- **Minimum**: 100 bytes (prevents empty/corrupt images)
- **Maximum**: 5MB (prevents memory issues)
- **Recommended**: Resize screenshots to 1920x1080 or smaller before uploading

## Tips

- Use PNG for screenshots (lossless, good compression)
- Use JPG for photos (better compression, slightly lossy)
- Compress images before converting: `pngquant screenshot.png` (macOS: `brew install pngquant`)
- For large uploads, consider resizing: `sips -Z 1920 screenshot.png` (macOS built-in)

