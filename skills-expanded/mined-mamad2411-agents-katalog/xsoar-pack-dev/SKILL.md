---
name: xsoar-pack-dev
description: Cortex XSOAR content pack development lifecycle - create packs, integrations, scripts, playbooks, run demisto-sdk lint/validate/pre-commit, build zip packs, manage versions and release notes, run unit tests, deploy to XSOAR instances, manage git branches/tags, handle marketplace vs local pack workflows. Use when the user wants to develop, test, build, validate, deploy, or manage XSOAR content packs.
argument-hint: [action] [pack-name]
allowed-tools: Bash, Read, Write, Edit, Glob, Grep, Agent, WebFetch, WebSearch
---

# Cortex XSOAR Pack Development Skill

You are an expert Cortex XSOAR content developer. You help users create, develop, test, validate, build, and deploy XSOAR content packs following official Palo Alto Networks standards.

**Target Platform**: XSOAR 6.x (demisto-py API). XSOAR 8/XSIAM UI API is NOT supported by this skill yet.

## MANDATORY WORKFLOW ORDER

**NEVER skip or reorder these steps:**

1. **Survey** (Phase 0) -> ASK user: local or marketplace? XSOAR type? Get all config. STOP and WAIT for answers.
2. **Repo Setup** (Phase 1) -> Clone content fork OR content-ci-cd-template. Git init, origin remote, feature branch.
3. **Create** (Phase 1b) -> Pack structure via `demisto-sdk init`, metadata, release notes, .pack-ignore, .secrets-ignore
4. **Develop** (Phase 2) -> Write code AND unit tests TOGETHER. Every new function gets a test.
5. **Docs** (Phase 2b) -> Update README.md + _description.md + release notes for EVERY feature/change. Detailed markdown with tables.
6. **Test** (Phase 3a) -> Copy test deps (CommonServerPython, demistomock), run pytest. ALL must pass.
7. **Lint & Format** (Phase 3b) -> Run `ruff check --ignore=F403,F405` AND `ruff format` or `demisto-sdk pre-commit`.
8. **Validate** (Phase 3c) -> Run `demisto-sdk validate`. Fix all errors.
9. **Commit** (Phase 4) -> ONLY after all above pass. Never commit before tests/lint/validate.
10. **Merge + Tag** (Phase 5) -> Merge feature branches to main. Tag release on main. Bump version.
11. **Build/Deploy** (Phase 6) -> `demisto-sdk zip-packs` ONLY after tagging. Deploy to XSOAR instance.

**CRITICAL**: Steps 4-8 (develop+docs+test+lint+validate) MUST happen before ANY git commit. Writing code without tests is NOT allowed.
**CRITICAL**: Zip pack is ONLY built after a git tag on main. Never build zip from a feature branch.
**CRITICAL**: README.md, _description.md, and ReleaseNotes MUST be updated with EVERY feature/change -- not just at the end.

## CRITICAL: Read Project CLAUDE.md First

Before any action, read the project's `CLAUDE.md` file (in the working directory or parent dirs) for project-specific configuration like:
- XSOAR instance URL and API key location
- Pack-specific conventions
- Deployment targets
- MCP server location

## Phase 0: Environment Survey (MANDATORY - Run on First Invocation)

**STOP AND ASK**: Before creating ANY files or writing ANY code, you MUST complete Phase 0 and get answers from the user. Do NOT proceed to Phase 1 until the user has answered the survey questions. Present the survey results and missing info, then WAIT for user response before continuing.

### Check Prerequisites
```bash
# Check each tool
git --version 2>/dev/null || echo "MISSING: git"
python3 --version 2>/dev/null || echo "MISSING: python3"
pip3 --version 2>/dev/null || echo "MISSING: pip3"
docker --version 2>/dev/null || echo "MISSING: docker"
demisto-sdk --version 2>/dev/null || echo "MISSING: demisto-sdk"
poetry --version 2>/dev/null || echo "MISSING: poetry"
pyenv --version 2>/dev/null || echo "MISSING: pyenv"
node --version 2>/dev/null || echo "MISSING: node"
```

### Install Missing Dependencies
If git is missing, install it: `sudo apt-get install -y git`
If demisto-sdk is missing: `pip3 install demisto-sdk`
If poetry is missing: `pip3 install poetry`
If Docker is missing, inform user it's needed for `demisto-sdk pre-commit` (runs linting/tests in Docker).

### Survey the User (MANDATORY - DO NOT SKIP)
After running prereq checks, present findings and ask ALL of these questions. WAIT for answers before proceeding. Skip only if answers are explicitly found in CLAUDE.md or environment variables:

1. **Pack type**: Is this a **marketplace** (public, push to demisto/content fork) or **local** (private, internal deployment) pack?
   - This determines version strategy, git workflow, and deployment method
2. **XSOAR instance**: Do you have a dev/test XSOAR instance?
   - **Instance URL**: What is the IP/hostname? Check env: `DEMISTO_BASE_URL`
   - **API Key**: What is the API key? Check env: `DEMISTO_API_KEY`
   - **Instance type**: Is it **XSOAR 6**, **XSOAR 8**, or **XSIAM**?
     - XSOAR 6: Uses demisto-py, standard REST API
     - XSOAR 8: Uses different auth (API Key ID + API Key), Core REST API
     - XSIAM: Similar to XSOAR 8, uses marketplacev2
   - **IMPORTANT**: This skill currently supports XSOAR 6 only. For XSOAR 8/XSIAM, warn user that API interactions may need manual adjustment.
   - If not set, ask: "Do you have a dev XSOAR instance to test against? What type is it?"
3. **Git remote**: What's the git remote URL? (For marketplace: fork of demisto/content. For local: private repo)
4. **Pack name**: What's the pack name? (PascalCase, e.g., `MyIntegration`)
5. **Author**: Author name for pack_metadata.json
6. **Category**: Which category? (Analytics & SIEM, Case Management, Data Enrichment & Threat Intelligence, Endpoint, Forensics & Malware Analysis, IT Services, Messaging, Network Security, Utilities, Vulnerability Management)
7. **Support type**: xsoar, partner, developer, or community?
8. **Zip storage** (local packs only): Where should built zip packs be stored? (e.g., `/var/www/packs/`, custom path)

## Phase 1: Content Repository Setup (MANDATORY BEFORE DEVELOPMENT)

### CRITICAL: Establish Content Repo Structure First

Development can ONLY begin after the working directory is one of:

**Option A: Marketplace pack** - Work inside a fork of `demisto/content`:
```bash
# Fork demisto/content on GitHub, then clone
git clone https://github.com/<your-user>/content.git
cd content
git checkout -b feature/<pack-name>
```

**Option B: Local pack** - Use content-ci-cd-template structure:
```bash
# Clone the template
git clone https://github.com/demisto/content-ci-cd-template.git <repo-name>
cd <repo-name>
# OR if repo already exists, ensure it has Packs/ directory at root
```

**Option C: Existing local repo** - Verify structure:
```bash
# Must have Packs/ at root, git initialized, and origin remote
ls Packs/ || mkdir Packs
git remote -v  # Must have origin set
```

**DO NOT start development in a bare/empty directory.** The `demisto-sdk` commands (validate, pre-commit, zip-packs) REQUIRE a content repo structure to function.

### Initialize Git (if needed)
```bash
git init
git remote add origin <url>  # Required for demisto-sdk
git checkout -b main 2>/dev/null || true
```

### Create Feature Branch
For EVERY new feature or pack, create a feature branch:
```bash
git checkout -b feature/<descriptive-name>
```

### Create Pack Structure (MUST use demisto-sdk init)

**CRITICAL:** Always use `demisto-sdk init` to create the pack scaffold. This ensures correct structure, generates pack_metadata.json with proper fields, creates .pack-ignore/.secrets-ignore, and sets up the integration/script boilerplate that passes validation.

```bash
# Create a new pack (interactive - prompts for name, description, etc.)
cd <content-repo-root>
demisto-sdk init --pack

# Create a new integration inside an existing pack
demisto-sdk init --integration -n <IntegrationName> --pack Packs/<PackName>

# Create a new script inside an existing pack
demisto-sdk init --script -n <ScriptName> --pack Packs/<PackName>
```

**What `demisto-sdk init --pack` creates:**
```
Packs/<PackName>/
├── pack_metadata.json          # Auto-generated with prompted values
├── README.md                   # Stub README
├── .pack-ignore                # With default RM104 ignore
├── .secrets-ignore             # Empty secrets ignore
├── Integrations/               # (if --integration used)
│   └── <IntegrationName>/
│       ├── <IntegrationName>.py
│       ├── <IntegrationName>.yml
│       ├── <IntegrationName>_test.py
│       ├── <IntegrationName>_description.md
│       ├── <IntegrationName>_image.png (optional)
│       ├── README.md
│       └── command_examples.txt
├── Scripts/                    # (if --script used)
│   └── <ScriptName>/
│       ├── <ScriptName>.py
│       ├── <ScriptName>.yml
│       └── <ScriptName>_test.py
├── Playbooks/
│   └── <PlaybookName>.yml
├── ReleaseNotes/
│   └── 1_0_0.md
├── IncidentFields/
├── IncidentTypes/
├── Classifiers/
├── Layouts/
└── TestPlaybooks/
```

**After `demisto-sdk init`:** Replace the generated boilerplate Python/YAML with actual integration code. The init command creates a working skeleton but you must customize it.

### pack_metadata.json Template
```json
{
    "name": "<Pack Display Name>",
    "description": "<Short description of the pack>",
    "support": "community",
    "currentVersion": "1.0.0",
    "author": "<Author Name>",
    "url": "",
    "email": "",
    "created": "<YYYY-MM-DDTHH:MM:SSZ>",
    "categories": ["<Category>"],
    "tags": [],
    "useCases": [],
    "keywords": [],
    "dependencies": {},
    "displayedImages": [],
    "marketplaces": ["xsoar", "marketplacev2"],
    "githubUser": [],
    "devEmail": []
}
```

**CRITICAL**: Version MUST start at `1.0.0`.

### Initial ReleaseNotes (1_0_0.md)
```markdown
#### Integrations

##### <IntegrationName>

- Initial release of **<Integration Display Name>**.
```

## Phase 2: Integration/Script Development

### Python File Template
```python
import demistomock as demisto
from CommonServerPython import *
from CommonServerUserPython import *

import urllib3

# Disable insecure warnings
urllib3.disable_warnings()

''' CONSTANTS '''

DATE_FORMAT = '%Y-%m-%dT%H:%M:%SZ'

''' CLIENT CLASS '''

class Client(BaseClient):
    """Client class to interact with the service API."""

    def __init__(self, base_url: str, verify: bool, proxy: bool, headers: dict):
        super().__init__(base_url=base_url, verify=verify, proxy=proxy, headers=headers)

    def example_request(self, param: str) -> dict:
        return self._http_request(method='GET', url_suffix=f'/api/endpoint/{param}')


''' COMMAND FUNCTIONS '''

def test_module(client: Client) -> str:
    """Tests API connectivity and authentication."""
    try:
        client.example_request('test')
        return 'ok'
    except Exception as e:
        raise DemistoException(f'Test failed: {str(e)}')


def example_command(client: Client, args: dict) -> CommandResults:
    """Example command implementation."""
    param = args.get('param', '')
    result = client.example_request(param)

    return CommandResults(
        outputs_prefix='Integration.Object',
        outputs_key_field='id',
        outputs=result,
        readable_output=tableToMarkdown('Results', result),
        raw_response=result
    )


''' MAIN FUNCTION '''

def main() -> None:
    params = demisto.params()
    command = demisto.command()
    args = demisto.args()

    base_url = params.get('url', '').rstrip('/')
    verify_certificate = not params.get('insecure', False)
    proxy = params.get('proxy', False)
    api_key = params.get('apikey', {}).get('password', '')

    headers = {'Authorization': f'Bearer {api_key}'}

    demisto.debug(f'Command being called is {command}')

    try:
        client = Client(base_url=base_url, verify=verify_certificate, proxy=proxy, headers=headers)

        if command == 'test-module':
            return_results(test_module(client))
        elif command == 'integration-command-name':
            return_results(example_command(client, args))
        else:
            raise NotImplementedError(f'Command {command} is not implemented.')

    except Exception as e:
        return_error(f'Failed to execute {command} command.\nError:\n{str(e)}')


if __name__ in ('__main__', '__builtin__', 'builtins'):
    main()
```

### YAML File Structure (Integration)
The YAML must define:
- `commonfields.id` and `commonfields.version: -1`
- `name`, `display`, `category`, `description`
- `configuration` parameters (each with display, name, type, required, section)
- `script.type: python`, `script.subtype: python3`
- `script.dockerimage` (e.g., `demisto/python3:3.10.14.100715`)
- `script.commands[]` with name, description, arguments[], outputs[]

### YAML Argument Types
- 0: Short text
- 4: Encrypted (passwords)
- 8: Boolean
- 9: Authentication (user+password)
- 12: JSON
- 13: Incident type
- 15: Single select
- 16: Multi select
- 17: Long text

### MANDATORY: Integration Logo

Every integration MUST have a logo image. This is a development requirement, not a post-release task.

**File**: `Packs/<PackName>/Integrations/<IntName>/<IntName>_image.png`
**Format**: PNG, recommended 120x50 pixels

**Step 1: Try to find the official logo (ALWAYS do this first for public services)**

For integrations wrapping a known public service, company, or product, you MUST use `WebSearch` and `WebFetch` to find and download the official logo before falling back to generating one. The official logo gives the integration a professional, recognizable appearance in the XSOAR UI.

```
1. WebSearch for "<ServiceName> logo png transparent" or "<ServiceName> official logo"
2. Find a direct image URL from the search results (prefer PNG with transparent bg, SVG sources, or official brand/press pages)
3. WebFetch the image URL to download it
4. Save the downloaded image, then resize to 120x50
```

If WebSearch/WebFetch cannot retrieve a usable image (network issues, no results, CAPTCHA), proceed to Step 2.

**Step 2: Fallback - AI-generated logo (ONLY for custom/internal integrations or when Step 1 fails)**

Only generate a logo if:
- The integration is custom/internal with no public brand
- Step 1 failed after a genuine attempt to find the official logo

**CRITICAL**: Do NOT use a simple text-on-rectangle placeholder. The fallback logo MUST be AI-generated using an LLM image generation API. Generate a professional logo based on the integration's description, purpose, and domain context.

**Option A: Use Claude API image generation (preferred if available)**
```python
# Use the Anthropic API to generate a logo based on integration context
# Prompt should describe: what the integration does, its domain, visual style
# Example prompt: "Generate a clean, minimal 120x50 pixel logo icon for a
# cybersecurity integration that monitors network traffic. Use a shield
# with data flow lines. Dark background, blue accent color, professional style."
```

**Option B: Use any available AI image generation API**
```python
# If Claude image gen is not available, use DALL-E, Stable Diffusion, or similar
# The key is: the logo must be contextually relevant to the integration's purpose
# NOT just text on a colored rectangle
```

**Option C: Last resort - styled text logo with contextual design**

Only if no AI image generation API is available, create a styled logo using Pillow that incorporates visual elements relevant to the integration's domain (not just plain text):

```python
# Generate a contextually-designed logo with Pillow
# Include domain-relevant visual elements (shapes, icons, gradients)
# Example: network integration -> include network/connection shapes
# Example: security integration -> include shield or lock shapes
# The design should reflect what the integration DOES, not just its name
python3 -c "
from PIL import Image, ImageDraw, ImageFont
width, height = 120, 50
img = Image.new('RGBA', (width, height), (0, 0, 0, 0))
draw = ImageDraw.Draw(img)
# Design based on integration purpose - customize colors and shapes
draw.rounded_rectangle([(0, 0), (width-1, height-1)], radius=8, fill=(33, 37, 41))
# Add domain-relevant visual elements here (not just text)
try:
    font = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', 16)
except:
    font = ImageFont.load_default()
text = '<SHORT_NAME>'
bbox = draw.textbbox((0, 0), text, font=font)
tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
draw.text(((width - tw) // 2, (height - th) // 2 - 2), text, fill=(255, 255, 255), font=font)
img.save('Packs/<PackName>/Integrations/<IntName>/<IntName>_image.png')
"
```

**Step 3: Resize downloaded logo (if Step 1 succeeded)**

```bash
# Resize with Python Pillow (preserves aspect ratio, centers on 120x50 canvas)
python3 -c "
from PIL import Image
img = Image.open('downloaded_logo.png')
img.thumbnail((120, 50), Image.LANCZOS)
new_img = Image.new('RGBA', (120, 50), (0, 0, 0, 0))
offset = ((120 - img.width) // 2, (50 - img.height) // 2)
new_img.paste(img, offset)
new_img.save('Packs/<PackName>/Integrations/<IntName>/<IntName>_image.png')
"

# Or with ImageMagick
convert downloaded_logo.png -resize 120x50 -background none -gravity center -extent 120x50 Packs/<PackName>/Integrations/<IntName>/<IntName>_image.png
```

**CRITICAL**: Do NOT skip the logo. Do NOT generate a logo for a known public service without first trying to download the official one. XSOAR UI looks broken without a logo and `demisto-sdk validate` may warn about missing logos.

### Unit Test Template
```python
"""Unit tests for <IntegrationName>."""
import json
import pytest
import demistomock as demisto
from CommonServerPython import CommandResults, DemistoException
from <IntegrationName> import Client, example_command, test_module


def util_load_json(path: str) -> dict:
    with open(path) as f:
        return json.load(f)


@pytest.fixture
def client():
    return Client(base_url='https://test.com', verify=False, proxy=False, headers={'Authorization': 'Bearer test'})


def test_test_module(requests_mock, client):
    """Test the test-module command."""
    requests_mock.get('https://test.com/api/endpoint/test', json={'status': 'ok'})
    result = test_module(client)
    assert result == 'ok'


def test_example_command(requests_mock, client):
    """Test example command - Given valid args, When called, Then returns expected results."""
    mock_response = {'id': '1', 'name': 'test'}
    requests_mock.get('https://test.com/api/endpoint/value', json=mock_response)

    args = {'param': 'value'}
    result = example_command(client, args)

    assert isinstance(result, CommandResults)
    assert result.outputs == mock_response
    assert result.outputs_prefix == 'Integration.Object'
```

### command_examples.txt
One command per line, used by `demisto-sdk generate-docs`:
```
!integration-command-name param=value
!integration-another-command arg1=val1 arg2=val2
```

### Description File (_description.md) - MUST BE DETAILED

The description file is shown in the XSOAR UI configuration panel. It MUST be comprehensive -- not a stub. Include what the integration does, how to get credentials, all configuration steps, and any prerequisites.

```markdown
### <Integration Name>

<One paragraph explaining what this integration does and what service it connects to.>

#### Prerequisites

- A valid **<Service Name>** account with API access.
- An API token/key generated from the <Service Name> dashboard.
- Network access from the XSOAR server to `<service-url>`.

#### How to Get an API Token

1. Log in to your **<Service Name>** account at `<service-url>`.
2. Navigate to **Settings** -> **API Keys** (or equivalent).
3. Click **Create Token** and copy the token immediately (it is shown only once).
4. Assign the required permissions: `<list required permissions/scopes>`.

#### Configuration Steps

1. Enter the **Server URL** (default: `<default-url>`).
2. Enter the **API Token** obtained above.
3. (Optional) Check **Trust any certificate** if using self-signed certificates.
4. (Optional) Check **Use system proxy** if your XSOAR server uses a proxy.
5. Click **Test** to validate connectivity.

#### Rate Limits

<Document any API rate limits, credit systems, or throttling behavior.>

#### Troubleshooting

- **401 Unauthorized**: Verify your API token is valid and has not expired.
- **403 Forbidden**: Check that your token has the required permissions.
- **Connection timeout**: Verify network connectivity to `<service-url>`.
```

**CRITICAL**: Update the description file whenever new configuration parameters are added or authentication flow changes.

## Phase 2c: Fetch Incidents

When an integration fetches incidents, it periodically polls an external API and creates XSOAR incidents from the results. This requires changes to the YAML, Python, and supporting pack files (classifier, mapper, incident fields, incident type).

### YAML Changes for Fetch

Add to the integration YAML:

```yaml
script:
  isfetch: true                    # Enables the "Fetches incidents" checkbox in XSOAR UI
  ...

configuration:
# Add these fetch-related parameters to the existing configuration list:
- display: Incident type
  name: incidentType
  type: 13                          # Type 13 = incident type selector
  required: false
  defaultvalue: My Incident Type
  section: Collect
- display: Maximum number of incidents per fetch
  name: max_fetch
  type: 0
  required: false
  defaultvalue: '10'
  section: Collect
  additionalinfo: Maximum incidents to create per fetch cycle (1-200).
- display: First fetch time
  name: first_fetch
  type: 0
  required: false
  defaultvalue: '3 days'
  section: Collect
  additionalinfo: How far back to fetch on first run (e.g., 3 days, 1 hour, 7 days).
- display: Classifier
  name: feedClassifier
  type: 0
  required: false
  hidden: true
  defaultvalue: MyIntegration
  section: Collect
- display: Mapper (incoming)
  name: feedMapper
  type: 0
  required: false
  hidden: true
  defaultvalue: MyIntegration-mapper
  section: Collect
```

### Python Fetch Implementation

```python
import dateparser

def fetch_incidents(client, last_run, first_fetch_time, max_results, incident_type, **kwargs):
    """Fetch incidents from external API.

    Args:
        client: Client instance.
        last_run: dict from demisto.getLastRun() with state between fetches.
        first_fetch_time: Human-readable time string (e.g., '3 days').
        max_results: Maximum incidents per fetch cycle.
        incident_type: XSOAR incident type name.
        **kwargs: Additional integration-specific parameters.

    Returns:
        Tuple of (next_run dict, incidents list).
    """
    last_fetch = last_run.get('last_fetch', None)
    last_ids = last_run.get('last_ids', [])  # For deduplication

    if last_fetch is None:
        # First fetch - parse the human-readable first_fetch_time
        first_fetch_dt = dateparser.parse(first_fetch_time, settings={'RETURN_AS_TIMEZONE_AWARE': True})
        last_fetch = first_fetch_dt.strftime('%Y-%m-%dT%H:%M:%SZ')

    # Query the external API for events since last_fetch
    events = client.get_events(since=last_fetch, limit=max_results)

    incidents = []
    new_last_fetch = last_fetch
    new_ids = []

    for event in events:
        event_id = str(event.get('id', ''))
        event_time = event.get('timestamp', '')

        # Deduplication: skip events we already processed
        if event_id in last_ids:
            continue

        incident = {
            'name': f'Event: {event.get("name", event_id)}',
            'occurred': event_time,
            'rawJSON': json.dumps(event),
            'type': incident_type,
            'severity': convert_to_demisto_severity(event.get('severity', 'low')),
        }
        incidents.append(incident)
        new_ids.append(event_id)

        # Track the latest timestamp for next fetch
        if event_time > new_last_fetch:
            new_last_fetch = event_time

    # next_run preserves state between fetch cycles
    next_run = {
        'last_fetch': new_last_fetch,
        'last_ids': new_ids[-max_results:],  # Keep bounded for memory
    }
    return next_run, incidents


def convert_to_demisto_severity(severity_str):
    """Map external severity to XSOAR severity (1-4)."""
    severity_map = {
        'low': 1,       # IncidentSeverity.LOW
        'medium': 2,    # IncidentSeverity.MEDIUM
        'high': 3,      # IncidentSeverity.HIGH
        'critical': 4,  # IncidentSeverity.CRITICAL
    }
    return severity_map.get(severity_str.lower(), 0)  # 0 = Unknown
```

### main() Integration for Fetch

```python
def main():
    params = demisto.params()
    command = demisto.command()
    ...

    if command == 'test-module':
        return_results(test_module(client))
    elif command == 'fetch-incidents':
        max_fetch = arg_to_number(params.get('max_fetch', 10)) or 10
        max_fetch = min(max_fetch, 200)

        next_run, incidents = fetch_incidents(
            client=client,
            last_run=demisto.getLastRun(),
            first_fetch_time=params.get('first_fetch', '3 days'),
            max_results=max_fetch,
            incident_type=params.get('incidentType', 'My Incident Type'),
        )
        demisto.setLastRun(next_run)
        demisto.incidents(incidents)
    elif command == 'my-command':
        ...
```

### Fetch Key Rules

- **Deduplication**: Always track processed event IDs in `last_run` to avoid duplicates across fetch cycles.
- **Bounded state**: Keep `last_ids` list bounded (e.g., last N IDs) to prevent unbounded memory growth.
- **Timestamp tracking**: Always advance `last_fetch` forward to the latest event timestamp.
- **First fetch**: Parse human-readable time (e.g., "3 days") with `dateparser.parse()` for the initial fetch window.
- **Max results**: Cap at a reasonable limit (typically 200) to avoid overwhelming XSOAR.
- **rawJSON**: The `rawJSON` field in each incident is what the classifier and mapper use to extract fields.
- **demisto.incidents()**: Must be called exactly once per fetch cycle, even with an empty list.

## Phase 2d: Long-Running Integrations

Long-running integrations maintain a persistent process that runs indefinitely inside XSOAR. Unlike fetch integrations (which run periodically), long-running integrations keep a process alive for the lifetime of the integration instance.

### When Long-Running Mode is REQUIRED

An integration MUST be long-running if any of the following apply:

1. **Hosting a TCP port / receiving inbound data** (webhook server, SYSLOG listener, HTTP endpoint, TCP/UDP socket) -- the integration needs to bind to a port and accept incoming connections or data. This is the ONLY case where `longRunningPort: true` is needed. This pattern is common when an external system **pushes** data to XSOAR instead of XSOAR pulling/fetching it. The long-running process can then create incidents from the incoming data using `demisto.createIncidents()`.
2. **Maintaining persistent sessions or connections** -- e.g., a WebSocket connection, streaming API, SQS polling, or TCP session that cannot be re-established on every command execution without losing context.
3. **Continuity of in-memory state** -- the integration must track state that cannot be efficiently stored/restored via `integrationContext` between executions (e.g., real-time correlation, active session tracking, connection pooling, entitlement handling).

**Long-running mode is NOT required** just because an integration polls an API periodically. Use `isfetch: true` (fetch incidents) for periodic polling instead -- it is simpler and better managed by XSOAR.

**`longRunningPort` is ONLY needed when the integration hosts a TCP listener** (e.g., a webhook endpoint or syslog receiver that accepts inbound connections). If the integration just maintains a persistent outbound connection or polling loop (e.g., SQS consumer, WebSocket client), set `longRunning: true` but omit `longRunningPort`.

### Long-Running with Inbound Data (Push Model)

When an external system pushes data to XSOAR (e.g., webhook, syslog, SNS notifications), the long-running integration hosts a listener and creates incidents from incoming data:

```python
from http.server import HTTPServer, BaseHTTPRequestHandler
import json

class WebhookHandler(BaseHTTPRequestHandler):
    """HTTP handler for incoming webhook data."""

    def do_POST(self):
        content_length = int(self.headers.get('Content-Length', 0))
        body = self.rfile.read(content_length)
        event = json.loads(body)

        # Create incident from inbound data
        demisto.createIncidents([{
            'name': f'Webhook Event: {event.get("type", "unknown")}',
            'rawJSON': json.dumps(event),
            'type': 'My Webhook Event',
        }])

        self.send_response(200)
        self.end_headers()
        self.wfile.write(b'OK')

def long_running_execution_command(params):
    """Start HTTP server to receive inbound webhooks."""
    port = int(demisto.params().get('longRunningPort', 8443))
    server = HTTPServer(('0.0.0.0', port), WebhookHandler)
    demisto.updateModuleHealth(f'Listening on port {port}')
    server.serve_forever()
```

This pattern differs from `isfetch` in that data is **pushed** to XSOAR rather than **pulled** by XSOAR on a schedule. Use this when the external system initiates the connection.

### Long-Running + Fake Fetch Pattern (Push with Classifier Support)

Some long-running integrations (e.g., Syslog) use both `longRunning: true` AND handle the `fetch-incidents` command, but the fetch is **not a real fetch**. Here is how it works:

1. **`long-running-execution`**: Listens for inbound data (syslog messages, webhooks, etc.) and creates incidents immediately via `demisto.createIncidents()`. Also stores **sample incidents** in the integration context.
2. **`fetch-incidents`**: Does NOT actually poll for data. Instead, it returns the stored **samples** via `demisto.incidents()`. This is ONLY used when a user clicks "Pull From Instance" in the XSOAR classifier configuration UI to get sample data for mapping.

```python
def fetch_samples():
    """Returns sample incidents for classifier/mapper configuration UI.
    Not a real fetch -- incidents are created in the long-running loop."""
    demisto.incidents(get_integration_context().get('samples', []))


def handle_inbound_data(raw_data):
    """Called from the long-running listener when data arrives."""
    incident = create_incident_from_data(raw_data)

    # Store sample for classifier UI
    update_integration_context_samples(incident)

    # Create incident immediately (NOT via fetch)
    demisto.createIncidents([incident])


def main():
    command = demisto.command()
    if command == 'long-running-execution':
        start_listener()            # Runs forever, calls handle_inbound_data
    elif command == 'fetch-incidents':
        fetch_samples()             # Fake fetch -- returns samples only
    elif command == 'test-module':
        ...
```

**YAML for this pattern:**
```yaml
script:
  longRunning: true
  longRunningPort: true            # Because it hosts a listener
  # NOTE: isfetch is NOT set to true -- it is implied by handling 'fetch-incidents'
```

**When to use this pattern:**
- The integration receives pushed data (syslog, webhook, SNS)
- You want classifier/mapper support in the XSOAR UI (which requires `fetch-incidents` to return samples)
- The actual incident creation happens in the long-running loop, not in fetch

This is a common pattern in: Syslog, AWS-SNS-Listener, Generic Webhook, and similar push-based integrations.

### YAML Changes for Long-Running

```yaml
script:
  longRunning: true
  longRunningPort: true            # ONLY if hosting a TCP listener (webhook, syslog, etc.)
  ...

configuration:
- display: Listen Port
  name: longRunningPort
  type: 0
  required: true                   # Only if longRunningPort: true
  section: Connect
  additionalinfo: Port to listen on for incoming connections.
- display: Polling Interval (seconds)
  name: polling_interval
  type: 0
  required: false
  defaultvalue: '60'
  section: Collect
```

### Python Long-Running Implementation

```python
import time

def long_running_execution_command(client, params):
    """Main loop for long-running integration.

    This function runs indefinitely. XSOAR manages the process lifecycle.
    Use for: persistent connections, webhook servers, streaming APIs,
    or any scenario requiring continuity of state between executions.
    """
    interval = int(params.get('polling_interval', 60))

    while True:
        try:
            # Poll for new events, process data, etc.
            events = client.poll_events()

            for event in events:
                # Create incidents directly via createIncidents
                demisto.createIncidents([{
                    'name': f'Event: {event["id"]}',
                    'rawJSON': json.dumps(event),
                    'type': 'My Incident Type',
                }])

            demisto.updateModuleHealth('Polling OK')
        except Exception as e:
            demisto.updateModuleHealth(f'Error: {str(e)}')
            demisto.error(f'Long-running error: {str(e)}')

        time.sleep(interval)


def main():
    ...
    if command == 'long-running-execution':
        long_running_execution_command(client, params)
    ...
```

### Long-Running Key Rules

- **Infinite loop**: The function must never return (XSOAR manages the process lifecycle).
- **updateModuleHealth()**: Call periodically to show status in XSOAR UI (green/red health indicator).
- **Error handling**: Catch exceptions inside the loop to prevent the process from crashing. Log errors with `demisto.error()`.
- **Sleep interval**: Use `time.sleep()` between iterations. Make the interval configurable via params.
- **createIncidents()**: Use this instead of `demisto.incidents()` (which is for fetch-incidents only).
- **Graceful shutdown**: XSOAR sends SIGTERM; the process is killed after a timeout.
- **Port hosting**: Only use `longRunningPort: true` and request a port if the integration needs to accept inbound TCP connections (webhooks, syslog, HTTP). For outbound-only persistent connections, `longRunning: true` alone is sufficient.

### CRITICAL: demisto.createIncidents() vs demisto.incidents()

These are two different functions for creating incidents and must NOT be confused:

| Function | Used In | When Called | Behavior |
|----------|---------|-------------|----------|
| `demisto.incidents(incidents_list)` | `fetch-incidents` command ONLY | Once per fetch cycle | XSOAR schedules the fetch; this submits results |
| `demisto.createIncidents(incidents_list)` | Long-running integrations ONLY | Anytime during execution | Creates incidents immediately from the persistent process |

- **fetch-incidents**: XSOAR calls your function periodically. You return incidents via `demisto.incidents()`. This is the **pull** model.
- **long-running-execution**: Your function runs forever. You create incidents on-demand via `demisto.createIncidents()`. This is the **push** model (or continuous polling model).

**Never use `demisto.incidents()` in a long-running integration.** Never use `demisto.createIncidents()` in a fetch-incidents handler.

### Entitlements and Ask Tasks (Two-Way Communication)

Entitlements enable two-way communication between external messaging systems (Slack, Mattermost, email) and XSOAR incidents/tasks. They are used primarily in long-running messaging integrations.

#### What Are Entitlements?

An entitlement is a unique identifier that links an external user response back to a specific XSOAR incident and optionally a playbook task. Format: `<GUID>@<incident_id>|<task_id>`

- `GUID` -- generated by XSOAR via the `addEntitlement` command
- `incident_id` -- the incident being questioned
- `task_id` (optional) -- specific playbook task waiting for a response

#### What Are Ask Tasks?

Ask tasks are playbook **condition** tasks that pause execution and wait for manual input. They present options (e.g., "Approve" / "Reject") and block the playbook until answered. Entitlements link external responses to these tasks.

#### Entitlement Flow

1. **Playbook sends question** via integration (e.g., Slack `send-notification` with entitlement)
2. **Integration stores the entitlement** in integration context with the message ID
3. **User replies** in the external system
4. **Long-running integration receives reply**, matches it to the stored entitlement
5. **Integration calls `demisto.handleEntitlementForUser()`** to close the task

#### Creating Entitlements

```python
# In a script or command that sends an ask question
res = demisto.executeCommand('addEntitlement', {
    'persistent': False,            # True = survives first response
    'replyEntriesTag': 'my_tag',   # Tag for organizing replies
})
guid = res[0]['Contents']
entitlement_string = f'{guid}@{incident_id}|{task_id}'

# Store in integration context for the long-running process to track
```

#### Handling Entitlement Responses (in Long-Running Integration)

```python
def handle_user_response(answer_text, message_id, user_name):
    """Process a user reply to an entitlement-based question."""
    context = demisto.getIntegrationContext()
    messages = json.loads(context.get('messages', '[]'))

    # Find the original question by message ID
    for msg in messages:
        if msg.get('message_id') == message_id:
            entitlement = msg.get('entitlement', '')
            parts = entitlement.split('@')
            guid = parts[0]
            id_and_task = parts[1].split('|')
            incident_id = id_and_task[0]
            task_id = id_and_task[1] if len(id_and_task) > 1 else ''

            # This closes the ask task and records the answer
            demisto.handleEntitlementForUser(
                incident_id,    # Which incident
                guid,           # Entitlement GUID
                user_name,      # Who answered
                answer_text,    # Their response (e.g., 'Approve')
                task_id         # Which task to close
            )
            break
```

#### When to Implement Entitlements

- Messaging integrations (Slack, Mattermost, Teams) that support ask tasks
- Any integration where playbooks need to ask external users for input
- Typically combined with long-running mode (to listen for replies in real-time)

## Phase 2e: Classifiers, Mappers, Incident Fields, and Incident Types

When an integration fetches incidents, it needs supporting artifacts to properly classify events, map raw fields to XSOAR fields, and define custom incident types with custom fields.

**Required artifacts for a fetching integration:**

1. **Incident Type** - Defines the XSOAR incident type created by fetch
2. **Incident Fields** - Custom fields specific to the integration's data
3. **Classifier** - Routes raw events to the correct incident type
4. **Mapper (Incoming)** - Maps raw JSON fields from `rawJSON` to XSOAR incident fields
5. **Mapper (Outgoing)** (optional) - Maps XSOAR fields back to external system fields

### Pack Directory Structure with Fetch Artifacts

```
Packs/<PackName>/
  Classifiers/
    classifier-<IntegrationName>.json              # Classifier
    classifier-mapper-incoming-<IntegrationName>.json  # Incoming mapper
    classifier-mapper-outgoing-<IntegrationName>.json  # Outgoing mapper (optional)
  IncidentFields/
    incidentfield-<Vendor>_<FieldName>.json        # One file per field
  IncidentTypes/
    incidenttype-<Incident_Type_Name>.json         # One file per type
```

### Incident Type JSON

File: `IncidentTypes/incidenttype-<Name_With_Underscores>.json`

```json
{
    "id": "My Integration Event",
    "name": "My Integration Event",
    "version": -1,
    "fromVersion": "6.0.0",
    "playbookId": "",
    "color": "#6A45D1",
    "hours": 0,
    "days": 0,
    "weeks": 0,
    "hoursR": 0,
    "daysR": 0,
    "weeksR": 0,
    "closureScript": "",
    "layout": "",
    "detached": false,
    "disabled": false,
    "reputationCalc": 0,
    "system": false,
    "readonly": false,
    "default": false,
    "autorun": true
}
```

Key fields:
- `id` and `name`: Must match the incident type name used in fetch and classifier
- `playbookId`: Optional -- auto-run a playbook when this incident type is created
- `color`: Hex color for the incident type in XSOAR UI
- `autorun`: If true, automatically runs the associated playbook
- `hours/days/weeks`: SLA timer settings (0 = no SLA)
- `hoursR/daysR/weeksR`: Remediation SLA settings

### Incident Fields JSON

File: `IncidentFields/incidentfield-<vendor>_<field_name>.json` (one file per field)

```json
{
    "id": "incident_myvendorflightid",
    "name": "MyVendor Flight ID",
    "cliName": "myvendorflightid",
    "type": "shortText",
    "description": "Unique flight identifier from MyVendor API.",
    "version": -1,
    "fromVersion": "6.0.0",
    "content": true,
    "group": 0,
    "associatedTypes": ["My Integration Event"],
    "associatedToAll": false,
    "system": false,
    "required": false,
    "openEnded": false,
    "sla": 0,
    "threshold": 0
}
```

Key fields:
- `id`: Must be `incident_<cliname>` (XSOAR convention). Use vendor prefix to avoid collisions.
- `cliName`: Snake-case identifier used in code and API. Must match the `id` suffix after `incident_`.
- `name`: Human-readable display name in XSOAR UI.
- `type`: Field data type -- one of:
  - `shortText` -- Single line text (most common)
  - `longText` -- Multi-line text
  - `number` -- Numeric value
  - `boolean` -- True/false
  - `date` -- Date/time value
  - `grid` -- Table/grid (structured data)
  - `singleSelect` -- Dropdown single selection
  - `multiSelect` -- Dropdown multi selection
  - `url` -- URL field
  - `html` -- HTML content
- `associatedTypes`: Array of incident type names this field applies to. Use `["all"]` for all types.
- `group`: `0` = incident field, `1` = evidence field, `2` = indicator field
- `content`: Must be `true` for pack content fields

### Classifier JSON

File: `Classifiers/classifier-<IntegrationName>.json`

The classifier examines the `rawJSON` of each fetched event and routes it to the correct incident type.

```json
{
    "id": "MyIntegration",
    "name": "MyIntegration - Classifier",
    "type": "classification",
    "version": -1,
    "fromVersion": "6.0.0",
    "defaultIncidentType": "My Integration Event",
    "keyTypeMap": {
        "event_type_value_1": "My Integration Event",
        "event_type_value_2": "My Integration Alert"
    },
    "transformer": {
        "simple": "rawJSON.event_type"
    }
}
```

How it works:
1. `transformer` extracts a value from the raw event (e.g., `rawJSON.event_type` -> `"alert"`)
2. `keyTypeMap` maps that extracted value to an XSOAR incident type name
3. `defaultIncidentType` is used when the extracted value doesn't match any key

**Single incident type (simple case):** If all events map to one type, set `defaultIncidentType` and leave `transformer` and `keyTypeMap` empty:
```json
{
    "id": "MyIntegration",
    "name": "MyIntegration - Classifier",
    "type": "classification",
    "version": -1,
    "fromVersion": "6.0.0",
    "defaultIncidentType": "My Integration Event",
    "keyTypeMap": {},
    "transformer": {}
}
```

### Mapper (Incoming) JSON

File: `Classifiers/classifier-mapper-incoming-<IntegrationName>.json`

The incoming mapper extracts values from `rawJSON` and maps them to XSOAR incident fields.

```json
{
    "id": "MyIntegration-mapper",
    "name": "MyIntegration - Incoming Mapper",
    "type": "mapping-incoming",
    "version": -1,
    "fromVersion": "6.0.0",
    "mapping": {
        "My Integration Event": {
            "dontMapEventToLabels": false,
            "internalMapping": {
                "MyVendor Flight ID": {
                    "simple": "rawJSON.flight_id"
                },
                "MyVendor Status": {
                    "simple": "rawJSON.status"
                },
                "Occurred": {
                    "simple": "rawJSON.timestamp"
                },
                "Severity": {
                    "complex": {
                        "root": "rawJSON.severity",
                        "filters": [],
                        "transformers": [
                            {
                                "operator": "MapValuesTransformer",
                                "args": {
                                    "input_values": {"value": "low,medium,high,critical"},
                                    "mapped_values": {"value": "1,2,3,4"}
                                }
                            }
                        ]
                    }
                },
                "Details": {
                    "simple": "rawJSON.description"
                }
            }
        }
    }
}
```

Key concepts:
- `mapping` is keyed by incident type name (must match classifier output and incident type `id`)
- `internalMapping` maps XSOAR field names (left side) to raw JSON paths (right side)
- **Simple mapping**: `"simple": "rawJSON.field_name"` -- direct field extraction
- **Complex mapping**: Uses `transformers` to convert values:
  - `MapValuesTransformer` -- maps input values to output values
  - `number.TimeStampToDate` -- converts Unix timestamps to date strings
  - `general.join` -- joins array values with a separator
  - `RegexExtractAll` -- regex extraction
  - `substring` -- extract substring
  - `concat` -- concatenate values
- Built-in XSOAR fields: `Occurred`, `Severity`, `Details`, `Name`, `Source Brand`, `Source Instance`
- Custom fields: Use the field `name` from the incident field JSON (not the `cliName`)

### Mapper (Outgoing) JSON (Optional)

File: `Classifiers/classifier-mapper-outgoing-<IntegrationName>.json`

Used for mirror-out scenarios (bidirectional sync). Maps XSOAR fields back to external system fields.

```json
{
    "id": "MyIntegration-outgoing-mapper",
    "name": "MyIntegration - Outgoing Mapper",
    "type": "mapping-outgoing",
    "version": -1,
    "fromVersion": "6.0.0",
    "mapping": {
        "My Integration Event": {
            "dontMapEventToLabels": false,
            "internalMapping": {
                "external_status": {
                    "simple": "closeReason"
                },
                "external_notes": {
                    "simple": "closeNotes"
                }
            }
        }
    }
}
```

### Naming Conventions for Fetch Artifacts

| Artifact | File Pattern | ID Pattern |
|----------|-------------|------------|
| Classifier | `classifier-<Integration>.json` | `<Integration>` |
| Incoming Mapper | `classifier-mapper-incoming-<Integration>.json` | `<Integration>-mapper` |
| Outgoing Mapper | `classifier-mapper-outgoing-<Integration>.json` | `<Integration>-outgoing-mapper` |
| Incident Type | `incidenttype-<Type_Name>.json` | `<Type Display Name>` |
| Incident Field | `incidentfield-<vendor>_<field>.json` | `incident_<vendor><field>` |

### Complete Fetch Integration Checklist

When adding fetch capability to an integration:

- [ ] YAML: Set `isfetch: true`, add `incidentType`, `max_fetch`, `first_fetch` params
- [ ] YAML: Add hidden `feedClassifier` and `feedMapper` params with default values
- [ ] Python: Implement `fetch_incidents()` function with dedup, state management, `rawJSON`
- [ ] Python: Add `fetch-incidents` case to `main()` with `demisto.getLastRun()`/`setLastRun()`/`incidents()`
- [ ] Create incident type JSON in `IncidentTypes/`
- [ ] Create incident field JSONs in `IncidentFields/` (one per custom field)
- [ ] Create classifier JSON in `Classifiers/`
- [ ] Create incoming mapper JSON in `Classifiers/`
- [ ] Write unit tests for `fetch_incidents()` (empty fetch, first fetch, dedup, pagination)
- [ ] Update README with fetch configuration, incident type, and field descriptions
- [ ] Update `_description.md` with fetch setup instructions
- [ ] Update `ReleaseNotes` with fetch feature documentation

## Phase 3: Validation and Testing

### CRITICAL: demisto-sdk Repository Requirements

`demisto-sdk validate` and `demisto-sdk pre-commit` **MUST** run from inside either:
1. A clone/fork of `demisto/content` (marketplace workflow)
2. A repo structured like `content-ci-cd-template` (local workflow)

They will NOT work in a standalone directory. The SDK imports `CONTENT_PATH` at module level and expects the full content repo structure.

**For standalone repos**: Set `DEMISTO_SDK_CONTENT_PATH` env var BEFORE running:
```bash
DEMISTO_SDK_CONTENT_PATH=$(pwd) DEMISTO_SDK_IGNORE_CONTENT_WARNING=1 demisto-sdk validate -i Packs/<PackName>
```

**Note**: `demisto-sdk lint` was REMOVED in SDK >= 1.38. Use `demisto-sdk pre-commit` instead (runs lint+tests in Docker).

### Run demisto-sdk Validation Suite
```bash
# Validate pack structure and metadata
# Inside demisto/content fork: no env vars needed
demisto-sdk validate -i Packs/<PackName>

# Inside content-ci-cd-template or standalone repos: set CONTENT_PATH
DEMISTO_SDK_CONTENT_PATH=$(pwd) DEMISTO_SDK_IGNORE_CONTENT_WARNING=1 demisto-sdk validate -i Packs/<PackName>

# Full pre-commit (includes ruff lint + format + validate + tests in Docker)
# IMPORTANT: Files must be staged (git add) before running pre-commit
git add Packs/<PackName>/
demisto-sdk pre-commit -i Packs/<PackName> --show-diff-on-failure

# Format code (auto-fixes many issues)
demisto-sdk format -i Packs/<PackName>
```

### Pre-commit Hook Results
When running `demisto-sdk pre-commit` locally, some hooks are CI-only and will fail:
- **PASS locally**: pylint-in-docker, mypy-in-docker, pytest-in-docker, markdownlint, brack, Validate README
- **FAIL locally** (expected, CI-only): xsoar-lint, validate-deleted-files, validate-content-paths, secrets, merge-pytest-reports, coverage-pytest-analyze
- **ruff hook**: May fail if `python` symlink is missing (only `python3` exists). Use manual ruff fallback below.

The important quality checks (pylint, mypy, pytest) run in Docker and will work locally if Docker is available.

### CRITICAL: Run ruff format Before Pushing
The CI pre-commit pipeline runs `ruff format` which enforces code formatting (not just linting). If your code is not formatted correctly, CI will fail even if lint passes. **Always run ruff format before pushing:**

```bash
# Run ruff format on changed Python files (REQUIRED before pushing)
# This auto-fixes formatting: function signature line wrapping, dict formatting, blank lines after imports, etc.
pip3 install ruff 2>/dev/null
ruff format Packs/<PackName>/Integrations/<IntName>/<IntName>.py Packs/<PackName>/Integrations/<IntName>/<IntName>_test.py

# Common formatting issues ruff format fixes:
# - Function signatures unnecessarily wrapped across multiple lines (should be single line if under 130 chars)
# - Dict literals passed to .append() need hanging indent style
# - Missing blank line after inline import statements
# - Trailing whitespace
```

### Fallback: Manual Linting (when pre-commit is unavailable)
If pre-commit fails due to repo structure or Docker issues, run linting manually:
```bash
# Preferred: flake8 with XSOAR standard ignores (most reliable)
pip3 install flake8 && flake8 --max-line-length=130 --ignore=W605,F403,F405,W503,BA107 Packs/<PackName>/Integrations/<IntName>/<IntName>.py

# Alternative: ruff check (linting only - does NOT check formatting)
# NOTE: ruff >= 0.15 removed UP038 rule; content repo pyproject.toml still references it
# Use --isolated to avoid config conflicts, or prefer flake8
ruff check --isolated --select=E,W,F --ignore=F403,F405 Packs/<PackName>/Integrations/<IntName>/<IntName>.py

# IMPORTANT: Also run ruff format (see section above) - ruff check alone is NOT sufficient
```
**Note**: F403/F405 (star imports) are EXPECTED in XSOAR code due to `from CommonServerPython import *` being mandatory.

### Set Up Test Dependencies
Before running tests, copy shared XSOAR modules into the integration directory:
```bash
# Required files (from a clone of demisto/content repo)
# If you don't have demisto/content cloned, clone it first:
#   git clone --depth 1 https://github.com/demisto/content.git /tmp/content
CONTENT_REPO="${DEMISTO_CONTENT_PATH:-/tmp/content}"
cp "${CONTENT_REPO}/Packs/Base/Scripts/CommonServerPython/CommonServerPython.py" Packs/<PackName>/Integrations/<IntName>/
cp "${CONTENT_REPO}/Tests/demistomock/demistomock.py" Packs/<PackName>/Integrations/<IntName>/
cp "${CONTENT_REPO}/Packs/ApiModules/Scripts/DemistoClassApiModule/DemistoClassApiModule.py" Packs/<PackName>/Integrations/<IntName>/
echo "" > Packs/<PackName>/Integrations/<IntName>/CommonServerUserPython.py  # Empty stub

# Install pytest dependencies
pip3 install pytest requests-mock
```
These files are NOT committed to git - add them to .gitignore.

### Run Unit Tests
```bash
# Direct pytest (fast, for development iteration)
cd Packs/<PackName>/Integrations/<IntName>/
python3 -m pytest <IntName>_test.py -v

# Via demisto-sdk (recommended - runs in Docker with correct deps)
demisto-sdk pre-commit -i Packs/<PackName>
```

**CRITICAL**: ALL tests must pass before proceeding to lint/validate/commit.

### Validation Checklist
Before committing, verify:
- [ ] All `args.get()` calls have matching YAML argument definitions
- [ ] Any command argument that accepts a list (comma-separated values) MUST have `isArray: true` in the YAML definition
- [ ] All markdown files use ASCII only (no UTF-8 special chars)
- [ ] pack_metadata.json has valid JSON and correct version
- [ ] ReleaseNotes file exists matching the version
- [ ] Unit tests pass
- [ ] `demisto-sdk validate` passes (set DEMISTO_SDK_CONTENT_PATH if standalone repo)
- [ ] `demisto-sdk pre-commit` passes (requires content repo structure), or manual ruff/flake8 lint passes

## Phase 4: Version Management

### Version Rules

**Local packs:**
- Start at `1.0.0`
- Bump `0.0.1` (patch) on every feature aggregation after tagging
- If many changes accumulated since last tag, suggest tagging and bumping

**Marketplace packs (first push to public GitHub):**
- Version MUST be `1.0.0` on first PR to demisto/content
- Concatenate all changelog entries into the `1_0_0.md` release notes
- After first PR is merged and reviewer feedback comes, bump `0.0.1` per review cycle
- Ask user: "Has an initial PR been filed? Is this feedback from an XSOAR developer review?"

### Bumping Version
When ANY pack file changes:
1. Increment `currentVersion` in `pack_metadata.json` by `0.0.1`
2. Create `ReleaseNotes/<new_version_underscored>.md`
3. Document ALL changes in release notes using official format

### CRITICAL: Documentation Updates with EVERY Feature

**Every feature, bug fix, or change MUST include updates to ALL THREE doc files in the SAME commit:**

1. **ReleaseNotes/<version>.md** -- What changed and why (bullet points per component)
2. **Packs/<PackName>/README.md** -- Full pack documentation (commands, args, outputs, examples)
3. **Integrations/<IntName>/<IntName>_description.md** -- UI configuration panel help text

**This is NOT optional.** Code changes without corresponding doc updates are incomplete. If you add a command, the README must document it. If you change an argument, the README table must reflect it. If you add a config parameter, the description file must explain it.

### Release Notes Format
```markdown
#### Integrations

##### <Integration Display Name>

- Added **new-command-name** command to retrieve X.
- Fixed an issue where Y did not work correctly.
- Updated Docker image to *demisto/python3:3.10.14.100715*.

#### Scripts

##### <Script Display Name>

- Improved performance of Z processing.

#### Playbooks

##### <Playbook Display Name>

- Added new sub-playbook for handling W.
```

**CRITICAL**: Use pure ASCII in release notes. No arrows, smart quotes, em dashes.

## Phase 5: README Generation - MUST BE COMPREHENSIVE

**CRITICAL**: The pack README.md is the primary documentation. It MUST be updated with EVERY feature or change -- not just at tag time. Every command, argument, output, and configuration option must be fully documented with markdown tables.

### When to Update README
- Adding a new command -> Add full command section with args table, outputs table, example
- Changing an argument -> Update the args table
- Adding a config parameter -> Update the Configuration table
- Adding a script or playbook -> Add new section
- Any user-visible change -> Update relevant README section

### Pack README Structure (MANDATORY - all sections required)
```markdown
# <Pack Name>

<Detailed paragraph explaining what this pack does, what service it integrates with,
what use cases it supports (e.g., threat intelligence enrichment, incident response,
asset tracking), and why a security team would use it.>

## Dependencies

This pack requires the following packs:
- **<PackName>** (mandatory/optional) -- <brief reason>

*No dependencies* if none are needed.

## Integrations

### <Integration Name>

<Detailed description: what the integration connects to, what capabilities it provides,
what API it wraps, any subscription or license requirements.>

#### Authentication

<Explain the auth method: API key, OAuth, basic auth, etc.>
<How to obtain credentials step by step.>
<Required permissions or scopes.>

#### Configuration

| Parameter | Description | Required | Default |
| --- | --- | --- | --- |
| Server URL | Base URL of the <service> API | True | `https://api.example.com` |
| API Key | API authentication token | True | |
| Trust any certificate | Skip SSL verification | False | False |
| Use system proxy | Route through system proxy | False | False |

#### Commands

| Command | Description |
| --- | --- |
| prefix-command-one | Brief description of what it does |
| prefix-command-two | Brief description of what it does |

---

### prefix-command-one

<Full description of what this command does, when to use it, and any important behavior notes.>

#### Input

| Argument | Description | Required | Default |
| --- | --- | --- | --- |
| arg1 | What this argument controls | True | |
| arg2 | Filter or limit option | False | `50` |
| arg3 | Comma-separated list of values | False | |

#### Context Output

| Path | Type | Description |
| --- | --- | --- |
| Prefix.Object.Field1 | String | What this field contains |
| Prefix.Object.Field2 | Number | What this number represents |
| Prefix.Object.Field3 | Boolean | What this flag indicates |

#### Command Example

\`\`\`
!prefix-command-one arg1=value arg2=10
\`\`\`

#### Human Readable Output

> Show a realistic example of the markdown table output the user will see in the War Room.

---

### prefix-command-two

<Repeat the same detailed structure for every command.>

(... repeat for ALL commands ...)

## Scripts

### <Script Name>

<What the script does, when it runs, what inputs/outputs it has.>

| Argument | Description |
| --- | --- |
| arg1 | Description |

## Playbooks

### <Playbook Name>

<Description of the playbook flow, what triggers it, what it automates, and the expected outcome.>

#### Playbook Flow

1. Step one -- what happens
2. Step two -- what happens
3. Step three -- what happens

## Known Limitations

- <Any API rate limits, unsupported features, or platform restrictions.>

## Troubleshooting

| Issue | Solution |
| --- | --- |
| Error message X | How to fix it |
```

### Auto-generate Docs (Starting Point Only)
Use `demisto-sdk generate-docs` to scaffold the README, then **you MUST review and enhance** the output:
```bash
demisto-sdk generate-docs -i Packs/<PackName>/Integrations/<IntName>
```
This requires `command_examples.txt` to exist with example commands.

**After running generate-docs, you MUST:**
1. Review the generated README.md for accuracy and completeness
2. Add detailed descriptions to every command (not just the one-liners from YAML)
3. Add an **Authentication** section explaining how to get credentials
4. Add a **Known Limitations** section if applicable
5. Add a **Troubleshooting** section with common errors
6. Add realistic **Command Example** output for each command
7. Verify all argument tables match the current YAML definitions
8. Ensure the description paragraph at the top is informative (not a generic stub)
9. Fix any formatting issues or missing markdown tables

**generate-docs creates a skeleton -- you create the documentation.**

## Phase 6: Git Workflow

### CRITICAL: Exclude Zip Build Artifacts from Git

Pack zip files produced by `demisto-sdk zip-packs` MUST NEVER be committed or pushed to any git repository (marketplace or local). They are build artifacts only.

**Before any commit, ensure .gitignore excludes zip output:**
```bash
# Add to .gitignore at repo root (if not already present)
echo '*_build/' >> .gitignore
echo '*.zip' >> .gitignore
echo 'uploadable_packs/' >> .gitignore
```

**Verify before staging:**
```bash
# Check that no zip files or build dirs are staged
git status | grep -E '\.zip|_build|uploadable_packs' && echo "WARNING: zip artifacts staged!" || echo "OK: no zip artifacts"
```

If a zip file is accidentally staged, remove it:
```bash
git rm --cached <PackName>*.zip
git rm --cached -r <PackName>_build/
```

### Feature Branch Workflow

**Each feature gets its own branch. Zip is ONLY built after tagging on main.**

```
main ─────────────────────────────────*──── tag v1.0.0 ──── BUILD ZIP
  \              \                   /
   feature/feat1  feature/feat2     / (merge all to main)
   (develop,      (develop,        /
    test, lint,    test, lint,    /
    validate,      validate,    /
    commit)        commit)     /
```

#### Step-by-step for each feature:
```bash
# 1. Create feature branch from main
git checkout main
git checkout -b feature/<feature-name>

# 2. Develop (code + tests + docs in same commit)
#    - Write integration/script code
#    - Write unit tests
#    - Update README.md with new commands/args/outputs
#    - Update _description.md if config changed
#    - Update ReleaseNotes (or create new version file)

# 3. Test + lint + validate (must all pass)

# 4. Stage and commit (specific files, never git add -A)
git add Packs/<PackName>/
git commit -m "feat(<PackName>): add <feature description>"
```

#### Merging features and tagging:
```bash
# 5. When all features for this release are done, merge to main
git checkout main
git merge feature/feat1
git merge feature/feat2
# Resolve any conflicts

# 6. Final validation on main
demisto-sdk validate -i Packs/<PackName>

# 7. Tag the release on main
VERSION=$(python3 -c "import json; print(json.load(open('Packs/<PackName>/pack_metadata.json'))['currentVersion'])")
git tag -a v${VERSION} -m "<PackName> v${VERSION}: <summary of all features in this release>"

# 8. NOW build the zip (only after tagging)
# See Phase 7 for build commands

# 9. Bump version for next dev cycle
# Edit pack_metadata.json: 1.0.0 -> 1.0.1
# Create empty ReleaseNotes/1_0_1.md stub
git add Packs/<PackName>/pack_metadata.json Packs/<PackName>/ReleaseNotes/
git commit -m "version(<PackName>): bump to v1.0.1 for next development cycle"
```

#### Cleanup feature branches:
```bash
git branch -d feature/feat1
git branch -d feature/feat2
```

### Marketplace Git Workflow
1. Fork demisto/content on GitHub
2. Clone fork locally
3. Create feature branch from master
4. Develop pack in `Packs/<PackName>/` (code + tests + docs together)
5. Run full validation suite
6. Commit and push to fork
7. Open PR against demisto/content
8. Address reviewer feedback (bump version 0.0.1 per review cycle)
9. Do NOT build zip -- marketplace CI handles it

### Local Git Workflow
1. Work in private repository (content-ci-cd-template or content fork)
2. Create feature branch for EACH feature
3. Develop + test + lint + validate + update docs on each branch
4. Merge all feature branches to main when validated
5. Tag release on main
6. Build zip ONLY after tagging
7. Deploy zip to XSOAR instance

## Phase 7: Build and Deploy

### CRITICAL: Zip is ONLY Built After a Git Tag

**DO NOT build a zip pack from a feature branch or untagged main.** The build process is:

1. All features merged to main
2. `demisto-sdk validate` passes on main
3. Git tag created (e.g., `v1.0.0`)
4. **THEN** build the zip

If the user asks to build a zip and there is no tag, ask: "Should I tag this release first?"

### Build Zip Pack

**ALWAYS use demisto-sdk zip-packs** (not regular zip). Output filename MUST include the version:

```bash
# Verify we are on a tagged commit
git describe --exact-match --tags HEAD || echo "WARNING: HEAD is not tagged! Tag first."

# Get version from pack_metadata.json
VERSION=$(python3 -c "import json; print(json.load(open('Packs/<PackName>/pack_metadata.json'))['currentVersion'])")

# Handle Lists bug workaround
if [ -d "Packs/<PackName>/Lists" ]; then
    mv Packs/<PackName>/Lists Packs/<PackName>/Lists.bak
fi

demisto-sdk zip-packs -i Packs/<PackName> -o <PackName>_build

# Restore Lists
if [ -d "Packs/<PackName>/Lists.bak" ]; then
    mv Packs/<PackName>/Lists.bak Packs/<PackName>/Lists
fi

# MUST rename with version in filename
cp <PackName>_build/uploadable_packs/<PackName>.zip <PackName>-${VERSION}.zip

# Clean up build directory (do NOT commit it)
rm -rf <PackName>_build

echo "Built: <PackName>-${VERSION}.zip"
```

**Zip filename format**: `<PackName>-<version>.zip` (e.g., `MyIntegration-1.0.0.zip`)
**For marketplace packs**: Do NOT store the zip in the git repo that will be pushed. CI handles zip building.
**For local packs**: Ask user where to store the zip. Common: `/var/www/packs/` or custom path.
**NEVER commit zip files or build directories to git** (see Phase 6 .gitignore rules).

### MANDATORY: Post-Build Deployment Prompt

**After EVERY zip build, ALWAYS ask the user these questions (do NOT skip):**

1. "Should I upload this pack to your XSOAR instance?"
2. "Should I create/update an integration instance and test it?"

Only proceed with deployment if the user confirms. If the user says yes, use the appropriate deployment method below.

### Deploy to XSOAR Instance

**ALWAYS use `demisto-sdk upload` as the primary upload method.** Only fall back to alternatives if demisto-sdk upload fails.

#### Primary Method: demisto-sdk upload (ALWAYS USE THIS)
```bash
# Set env vars (check CLAUDE.md or ask user for values)
export DEMISTO_BASE_URL=<url>
export DEMISTO_API_KEY=<key>

# Upload the pack directly (uploads source, not zip)
demisto-sdk upload -i Packs/<PackName> --insecure

# OR upload a built zip file
demisto-sdk upload -i <PackName>-<version>.zip --insecure
```

**CRITICAL**: This is the ONLY recommended method for uploading packs. It handles unification, signature issues, and content validation automatically.

#### Alternative: Upload via demisto-client (Python API) -- ONLY if demisto-sdk upload fails
```python
import demisto_client

# Configure client (see XSOAR API Reference for auth differences)
api_instance = demisto_client.configure(
    base_url="https://<xsoar-url>",
    api_key="<api-key>",
    verify_ssl=False
)

# Upload pack zip file
with open('<PackName>-<version>.zip', 'rb') as f:
    zip_content = f.read()

response, status, _ = demisto_client.generic_request_func(
    self=api_instance,
    method="POST",
    path="/contentpacks/installed/upload",
    body=zip_content,
    content_type="application/zip",
    response_type="object"
)
print(f"Upload status: {status}")
```

#### Method 3: Create Integration Instance via demisto-client
After uploading a pack, create and test an integration instance:

```python
import demisto_client

api_instance = demisto_client.configure(
    base_url="https://<xsoar-url>",
    api_key="<api-key>",
    verify_ssl=False
)

# 1. Search for the integration to get its full configuration schema
response, status, _ = demisto_client.generic_request_func(
    self=api_instance,
    method="POST",
    path="/settings/integration/search",
    body={"query": "<IntegrationName>"},
    response_type="object"
)

# 2. Get the integration configuration from search results
integrations = response.get("configurations", [])
integration_config = None
for config in integrations:
    if config.get("display") == "<Integration Display Name>":
        integration_config = config
        break

# 3. Build the instance payload
# CRITICAL: Instance structure is DIFFERENT from integration definition structure
# - "enabled" must be string "true", not boolean
# - "version" must be 0 for new instances
# - "configuration" is a NESTED OBJECT (integration reference), NOT the params array
# - "data" is the params array (from search response's "configuration" array)
# - "configvalues" is a simple dict of param_name -> value
# - "configtypes" is a simple dict of param_name -> type_int

# The search response has "configuration" as an ARRAY of param defs.
# For the instance PUT, those param defs go into "data" (not "configuration")
config_params = integration_config.get("configuration", [])

# Build data array with values set
data_array = []
configvalues = {}
configtypes = {}

for param in config_params:
    item = param.copy()
    pname = param.get("name", "")
    ptype = param.get("type", 0)

    if pname == "url":
        item["value"] = "https://api.example.com"
        item["hasvalue"] = True
        configvalues["url"] = "https://api.example.com"
        configtypes["url"] = ptype
    elif pname == "insecure":
        item["value"] = True
        item["hasvalue"] = True
        configvalues["insecure"] = True
        configtypes["insecure"] = ptype
    # Type 4 (encrypted) params: set value directly in configvalues
    elif pname == "apikey" and ptype == 4:
        item["hasvalue"] = True
        configvalues["apikey"] = "<api-key-value>"
        configtypes["apikey"] = ptype
    # Type 9 (auth) params: set identifier+password in configvalues
    elif pname == "credentials" and ptype == 9:
        item["hasvalue"] = True
        configvalues["credentials"] = {"identifier": "user@email.com", "password": "<pass>"}
        configtypes["credentials"] = ptype

    data_array.append(item)

# Build nested configuration (integration definition reference - mostly empty)
nested_config = {
    "id": "", "version": 0, "cacheVersn": 0,
    "modified": "0001-01-01T00:00:00Z", "created": "0001-01-01T00:00:00Z",
    "sizeInBytes": 0, "packID": "", "packName": "", "itemVersion": "",
    "fromServerVersion": "", "toServerVersion": "", "definitionId": "",
    "vcShouldIgnore": False, "vcShouldKeepItemLegacyProdMachine": False,
    "commitMessage": "", "shouldCommit": False, "name": "", "prevName": "",
    "display": integration_config.get("display", ""),
    "brand": "", "category": "", "icon": "", "description": "",
    "configuration": None, "integrationScript": None,
    "hidden": False, "canGetSamples": False,
}

instance_payload = {
    "id": "", "version": 0, "enabled": "true",
    "name": "<instance-name>",
    "brand": integration_config["id"],  # Must match integration ID
    "category": integration_config.get("category", ""),
    "configuration": nested_config,     # Nested integration ref (object, NOT array)
    "data": data_array,                 # Param values (array from search "configuration")
    "configvalues": configvalues,       # Simple key-value param map
    "configtypes": configtypes,         # Simple key-type param map
    "isIntegrationScript": True,
    "propagationLabels": ["all"],
}

# 4. Create the instance
response, status, _ = demisto_client.generic_request_func(
    self=api_instance,
    method="PUT",
    path="/settings/integration",
    body=instance_payload,
    response_type="object"
)
print(f"Instance creation status: {status}")
# status 200 = success, response contains instance ID

# 5. Test the instance
response, status, _ = demisto_client.generic_request_func(
    self=api_instance,
    method="POST",
    path="/settings/integration/test",
    body=instance_payload,
    response_type="object"
)
print(f"Test result: {response}")
```

**Key gotchas for instance creation:**
- `enabled` MUST be string `"true"`, not boolean `True`
- Credential parameters use `{"identifier": "", "password": "<value>"}` format in `configvalues`
- `version: 0` for new instances, `version: -1` for updating existing ones
- The full integration config from search results provides the required schema -- modify it, don't build from scratch
- Parameter values go in the `data` array items (set `value` and `hasvalue: True`)

#### Method 4: API install via CoreRESTAPI
If CoreRESTAPI integration is configured on XSOAR:
```
!core-api-post uri=/contentpacks/installed/upload body=<zip-file-content>
```

#### Method 5: Manual zip upload
Upload via XSOAR UI: Settings -> Marketplace -> Upload custom pack

#### Method 6: Web server deployment (local)
```bash
sudo cp <PackName>-<version>.zip /var/www/packs/
# Pack available at http://<server>/packs/<PackName>-<version>.zip
```

#### Method 7: Create incident with pack info
Using the MCP server or API to create an incident that triggers pack installation.

### Install Pack Dependencies
Check pack_metadata.json dependencies and ensure they're installed on the XSOAR instance.

## Phase 8: Continuous Validation

### Pre-commit Checks (mirroring CI/CD)
Run before every commit:
```bash
demisto-sdk pre-commit -i Packs/<PackName> --show-diff-on-failure
```

This runs:
- check-json, check-yaml, check-ast
- check-merge-conflict, debug-statements
- name-tests-test (validates test file naming)
- ruff (linting and formatting)
- mypy (type checking)
- pycln (unused import removal)
- Unit tests in Docker

### CI/CD Pipeline Checks (what GitHub Actions run)
The content-ci-cd-template runs on push:
1. Checkout repo + demisto/content reference
2. Install poetry + Python 3.9+ + node
3. Copy CommonServerPython.py and demistomock.py
4. `demisto-sdk pre-commit -g --prev-version ${DEFAULT_BRANCH}`
5. `demisto-sdk prepare-content` (builds uploadable packs)
6. On merge to default branch: upload to artifact server or direct upload

## Important Conventions

### Code Conventions
- Import order: `demistomock`, `CommonServerPython`, `CommonServerUserPython`, then stdlib, then third-party
- Use `snake_case` for variables and functions
- Command functions: `<command_name>_command(client, args)`
- Commands: `<prefix>-<action>` (hyphenated lowercase)
- Use `CommandResults` with `return_results()` for all command output
- Output keys: CamelCase (e.g., `Integration.Object.FieldName`)
- **CRITICAL**: If a command argument expects a list (comma-separated), set `isArray: true` in the YAML argument definition. Use `argToList()` in Python to parse it.
- Error handling: `return_error()` in main, never let stack traces reach War Room
- Logging: `demisto.debug()`, `demisto.info()`, `demisto.error()` - never `print()`
- Keep functions small (~30 lines), use early returns
- Type hints on all functions
- Stateless - no shared state between executions

### Naming Conventions
- Pack directory: PascalCase (`MyPackName`)
- Integration/Script files: PascalCase matching directory name
- Commands: `prefix-action-noun` (e.g., `qradar-offenses-list`)
- Context paths: `Vendor.Entity.Field` (CamelCase)
- Test files: `<Name>_test.py`

### Docker Images
- Default: `demisto/python3:3.10.14.100715` (check for latest)
- Dependencies managed via Docker, not local pip
- Specified in YAML: `script.dockerimage`

### File Encoding
- ALL markdown files MUST use pure ASCII
- No UTF-8 special chars (no arrows, smart quotes, em dashes)
- Replace: `->` not arrow, `'` not smart quote, `--` not em dash

## Quick Reference: Common Actions

| Action | Command |
|--------|---------|
| Create new pack | `demisto-sdk init --pack` |
| Validate | `DEMISTO_SDK_CONTENT_PATH=$(pwd) demisto-sdk validate -i Packs/<Pack>` |
| Lint + Test | `demisto-sdk pre-commit -i Packs/<Pack>` (requires content repo) |
| Format | `demisto-sdk format -i Packs/<Pack>` |
| Build zip | `demisto-sdk zip-packs -i Packs/<Pack> -o output/` |
| Upload | `demisto-sdk upload -i Packs/<Pack> --insecure` |
| Generate docs | `demisto-sdk generate-docs -i Packs/<Pack>/Integrations/<Int>` |
| Split unified YAML | `demisto-sdk split -i <unified.yml>` |
| Download from XSOAR | `demisto-sdk download -o Packs/<Pack>` |

## Decision Tree: Marketplace vs Local

```
User wants to develop a pack
    |
    +--> Marketplace (public)
    |       |
    |       +--> Fork demisto/content
    |       +--> Version MUST be 1.0.0 on first PR
    |       +--> Consolidate all changes into 1_0_0.md
    |       +--> Do NOT include zip in git repo
    |       +--> Run full demisto-sdk pre-commit
    |       +--> Open PR, address feedback
    |       +--> Bump 0.0.1 per review cycle
    |       +--> Sign CLA
    |
    +--> Local (private)
            |
            +--> Private git repo (or content-ci-cd-template)
            +--> Start at 1.0.0, bump 0.0.1 per feature
            +--> Tag releases
            +--> Build zip with demisto-sdk zip-packs
            +--> Deploy via upload/API/web server
            +--> Ask user for zip storage location
```

## XSOAR API Reference

### Authentication by Platform

| Platform | Auth Method | `demisto_client.configure()` | Notes |
|----------|-------------|------------------------------|-------|
| **XSOAR 6** | API Key only | `api_key="<key>"` | Standard REST API. Generate key in Settings -> API Keys |
| **XSOAR 8** | API Key + Key ID | `api_key="<key>", auth_id="<key-id>"` | Uses Core REST API. Key ID is shown when creating the key |
| **XSIAM** | API Key + Key ID | `api_key="<key>", auth_id="<key-id>"` | URL format: `api-<tenant>.xdr.<region>.paloaltonetworks.com`. Uses marketplacev2 |

The skill survey (Phase 0) already asks which instance type. Use that info to configure authentication.

### demisto-client Configuration

```python
import demisto_client

# XSOAR 6
api_instance = demisto_client.configure(
    base_url="https://<xsoar6-url>",
    api_key="<api-key>",
    verify_ssl=False
)

# XSOAR 8
api_instance = demisto_client.configure(
    base_url="https://<xsoar8-url>",
    api_key="<api-key>",
    auth_id="<key-id>",        # Required for XSOAR 8
    verify_ssl=False
)

# XSIAM
api_instance = demisto_client.configure(
    base_url="https://api-<tenant>.xdr.<region>.paloaltonetworks.com",
    api_key="<api-key>",
    auth_id="<key-id>",        # Required for XSIAM
    verify_ssl=False
)
```

### Common API Endpoints

```python
# Generic request helper
response, status, _ = demisto_client.generic_request_func(
    self=api_instance,
    method="<METHOD>",
    path="<path>",
    body=<payload>,
    response_type="object"
)
```

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/contentpacks/installed/upload` | POST | Upload pack zip file |
| `/settings/integration/search` | POST | Search integrations (body: `{"query": "name"}`) |
| `/settings/integration` | PUT | Create/update integration instance |
| `/settings/integration/test` | POST | Test integration instance connectivity |
| `/incident/search` | POST | Search incidents |
| `/entry` | POST | Create war room entry / run command |
| `/lists/save` | POST | Save/update an XSOAR list |
| `/health` | GET | Health check |

### demisto-py (Alternative)

For simpler API interactions without instance management:
```python
import demisto_client
# or
import requests

# Direct REST with requests
headers = {"Authorization": "<api-key>", "Content-Type": "application/json"}
response = requests.post(f"{base_url}/incident/search", headers=headers, json={"query": ""}, verify=False)
```

### MCP Server

### MCP Server for XSOAR

If an XSOAR MCP server is configured in the project (check CLAUDE.md for location), use it for interactive XSOAR operations. A typical MCP server provides tools across categories: incidents, automations, integrations, lists, indicators, logs, migration, and utilities.

If no MCP server is available, use `demisto-client` or direct REST API calls as shown above.

## Error Recovery

| Error | Solution |
|-------|----------|
| `UnicodeDecodeError` in demisto-sdk | Non-ASCII chars in markdown - replace with ASCII equivalents |
| Lists processing bug in zip-packs | Move Lists dir out, zip, restore |
| `demisto-sdk upload` fails with IP URL | Use zip method and upload via UI |
| Pre-commit fails on Docker | Ensure Docker daemon is running |
| Missing CommonServerPython in tests | Copy from demisto/content repo clone (see test deps setup) |
| Missing DemistoClassApiModule | Copy from `<content-repo>/Packs/ApiModules/Scripts/DemistoClassApiModule/` |
| Missing CommonServerUserPython | Create empty stub: `echo "" > CommonServerUserPython.py` |
| mypy errors | Add type hints, use `--ignore-missing-imports` |
| `demisto-sdk validate` CONTENT_PATH error | Set env: `DEMISTO_SDK_CONTENT_PATH=$(pwd)` before running |
| `demisto-sdk lint` not found (SDK >= 1.38) | Use `demisto-sdk pre-commit` instead (lint was removed) |
| `demisto-sdk pre-commit` path error | Must run from content repo root or content-ci-cd-template structure |
| Git HEAD not found by SDK | Must have at least one commit before running validate |
| No origin remote error | Add remote: `git remote add origin <url>` |
| pytest collects imported `test_module` | Import as alias: `from Module import test_module as _test_module` |
| `demisto-sdk` outdated | Upgrade: `pip3 install --upgrade demisto-sdk` |
| Pre-commit "No files were changed" | Files must be staged first: `git add Packs/<Pack>/` before running pre-commit |
| ruff UP038 error in content repo | Content pyproject.toml references removed rule; use flake8 instead or `ruff --isolated` |
| Pre-commit xsoar-lint/secrets/validate-deleted-files fail | These hooks are CI-only (need `/usr/bin/demisto-sdk`); safe to ignore locally |
| ruff "Executable python not found" | Only `python3` exists; use flake8 fallback or create `python` symlink |
