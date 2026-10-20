# Secrets Module

This directory owns the `secrets` repo module — secure credential management with output masking.

- Registers `kota secrets set/get/list/remove` CLI commands.
- Registers the `get_secret` agent tool (injects secrets into a live session- and scope-local execution environment, returns a placeholder to the LLM, and erases the overlay at session teardown).
- Resolves every client, route, and tool operation through a validated scope selector; unknown scopes fail before store access.
- The scope-store registry and provider chain live in `src/core/config/secrets.ts`.
