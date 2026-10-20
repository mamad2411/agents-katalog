---
name: hermes-profile-evolution
description: Route proposed Team Mimir profile behavior changes to target-owned Hermes dialogue.
---

# Hermes Profile Evolution

Use this skill when a requested Team Mimir change may affect a profile's own behavior. Run the
bundled `profile_request.py request` action with bounded JSON on standard input before editing.

Resolve the bundled adapter from the active or installed Antigravity plugin root, and pass the Team
Mimir checkout separately:

```bash
TEAM_MIMIR_ROOT="${TEAM_MIMIR_ROOT:-$PWD}"
HERMES_PROFILE_EVOLUTION_PLUGIN_ROOT="${AGY_PLUGIN_ROOT:-$HOME/.gemini/config/plugins/hermes-profile-evolution}"
python3 "$HERMES_PROFILE_EVOLUTION_PLUGIN_ROOT/scripts/profile_request.py" \
  --team-mimir-root "$TEAM_MIMIR_ROOT" request
```

Send the bounded proposal JSON on standard input. Do not search the Team Mimir checkout for plugin
source.

The adapter calls Team Mimir's producer-owned classifier. If it reports ordinary repository work,
continue through normal repository review. If it reports one target's profile-owned behavior, or a
mixed request with exactly one profile-owned target, let the adapter send the canonical suggestion
to `hermes profile-request`. Do not reinterpret the classifier result.

Use `reply` and `resume` to continue the same live dialogue. The profile is autonomous: a suggestion
is not approval, mutation authority, a queued job, or evidence that a change occurred.

Stop on prohibited, unknown, custodian-owned, external-custody, cross-target, health, service,
provenance, or response failures. Never bypass a failure with a direct profile edit. Do not include
credentials, hosts, API keys, tokens, model or provider overrides, system prompts, tool overrides,
private runtime paths, sessions, transcripts, databases, or logs.

Antigravity exposes no supported hook contract for this plugin. This skill provides guidance and a
native command; it does not claim to intercept all writes.
