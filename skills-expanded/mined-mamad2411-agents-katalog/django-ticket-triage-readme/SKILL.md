# django-ticket-triage

A Claude Code command that helps you analyze Django Trac tickets before contributing.

## What it does

### `/triage` - Ticket Analysis

When you run `/triage <ticket_id>`, it automatically:

- Fetches ticket details, status, and comment history
- Searches for duplicate/related tickets across Trac, GitHub PRs, and Django Forum
- Locates relevant source code in the Django codebase
- Evaluates ticket validity (bug vs feature, reproducibility, scope)
- Generates a structured triage report with recommendations

### `/impl-plan` - Implementation Planning

When you run `/impl-plan <ticket_id>`, it automatically:

- Loads the existing triage report for context
- Performs deep analysis of target code and tests
- Generates 2-4 implementation options (A/B/C)
- Compares trade-offs (complexity, risk, backwards compatibility)
- Recommends the best approach with implementation checklist

## Installation

```bash
git clone https://github.com/2ykwang/django-ticket-triage.git
cd django-ticket-triage
uv sync

# Clone Django source for code-level analysis
git clone https://github.com/django/django.git
```

## Usage

Open Claude Code in the project directory:

```bash
cd django-ticket-triage
claude
```

### Workflow

```
/triage 36640           # Step 1: Generate triage report
/impl-plan 36640        # Step 2: Plan implementation approach
```

### Language Support

```
/triage 36640 ko        # Korean report
/impl-plan 36640 ko     # Korean report
```

### Output

| Command | Output Location |
|---------|-----------------|
| `/triage` | `triage-reports/<ticket_id>.md` |
| `/impl-plan` | `impl-reports/<ticket_id>.md` |

## Example Output

See [examples/](examples/) for sample reports.

## Limitations

- Final triage decisions should be made by humans
- Analysis quality depends on available ticket comments and history
- External context (W3C specs, screen reader support, etc.) may require manual verification
