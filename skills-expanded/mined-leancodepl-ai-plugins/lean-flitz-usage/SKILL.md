---
name: lean-flitz-usage
description: Explain what the `lean-flitz` plugin does and how to use it. Use when someone invokes `/lean-flitz-usage`, asks what this plugin covers, or wants to know how to get a Flitz bundle of a Flutter app from Claude Tag or a local session.
---

# lean-flitz

One skill, one job: publish a Flitz bundle of a Flutter app and hand back the link a teammate
opens on their phone.

## What Flitz is

[Flitz](https://docs.flitz.dev) puts work-in-progress builds of a Flutter app on a real device
without a rebuild or a store round-trip. The app is split in two: the **host**, a normal signed
build of the app with the Flitz loader embedded, installed once; and the **bundle**, the app's
Dart code and assets, which `flitz publish` builds and uploads as often as needed. Opening the
publish link on a device with the host installed downloads the bundle and runs it.

## What it gives you

`/lean-flitz:publish-flitz-bundle`, or simply asking for a Flitz bundle, runs
`flitz publish --yes --json` in the project directory (the one holding `flitz.yaml`), installs the
`flitz` CLI first when it is missing, and reports the landing page. The bundle is built from the
working tree as it is.

## Where it runs

- **Claude Tag**, Claude in Slack. The Agent Proxy injects the organization API key into requests
  to `api.flitz.dev`, so the sandbox never holds the key; the skill gives the CLI a placeholder key
  to get past its local check.
- **Locally**, the CLI uses your `flitz login`, or a `FLITZ_APIKEY` already in the environment.
  The placeholder never shadows a real login.

## What it needs

- A Flitz organization with an active license.
- A project already set up for Flitz: a `flitz.yaml` pin from `flitz sdk use`, and a host build
  installed on the device that will open the link. The skill does neither.
- Linux x64 or an Apple Silicon Mac, which are the hosts the CLI supports.

Setup for Claude Tag (the Flitz connector and allowed domains on the channel's bundle) and for a
local session lives in the plugin `README.md`.

## When to reach for something else

- A pull request whose CI already publishes a bundle: the link is in the CI output.
- Setting up Flitz in an app (host build, loader plugins, `flitz sdk use`): the
  [Flitz docs](https://docs.flitz.dev/getting-started).
