---
description: "camofox CLI command reference — all 43+ commands with usage examples"
alwaysApply: false
---

# CLI Command Reference (Source-Verified)

Global options:
```bash
--user <user>                    # default user id (overrides CAMOFOX_CLI_USER)
--port <port>                    # server port (overrides CAMOFOX_PORT)
--format <format>                # json|text|plain
--local                          # reserved for v2
-V, --version                    # CLI version
-h, --help                       # help
```

## Core
```bash
camofox open <url> [--user <user>] [--viewport <WxH>] [--geo <preset>]              # create tab
camofox close [tabId] [--user <user>]                                                 # close tab
camofox snapshot [tabId] [--user <user>]                                              # accessibility snapshot
camofox click <ref> [tabId] [--user <user>]                                           # click element
camofox type <ref> <text> [tabId] [--user <user>]                                     # type text
```

## Navigation
```bash
camofox navigate <url> [tabId] [--user <user>]                                        # navigate tab
camofox screenshot [tabId] [--path <file>|--output <file>] [--full-page] [--user <user>]  # screenshot
camofox go-back [tabId] [--user <user>]                                               # history back
camofox go-forward [tabId] [--user <user>]                                            # history forward
```

## Interaction
```bash
camofox fill <assignments> [tabId] [--user <user>]                                    # [e1]="x" [e2]="y"
camofox scroll [direction] [tabId] [--amount <N>] [--user <user>]                     # up|down|left|right
camofox select <ref> <value> [tabId] [--user <user>]                                  # select option
camofox hover <ref> [tabId] [--user <user>]                                           # hover
camofox press <key> [tabId] [--user <user>]                                           # key press
camofox drag <fromRef> <toRef> [tabId] [--user <user>]                                # drag/drop
```

## Content & Inspection
```bash
camofox get-text [tabId] [--selector <selector>] [--user <user>]                      # extract text
camofox get-url [tabId] [--user <user>]                                               # current URL
camofox get-links [tabId] [--user <user>]                                             # links
camofox get-tabs [--user <user>]                                                      # tab list
camofox eval <expression> [tabId] [--user <user>]                                     # evaluate JS
camofox wait <condition> [tabId] [--timeout <ms>] [--user <user>]                     # selector|navigation|networkidle
camofox search <query> [tabId] [--engine <engine>] [--user <user>]                    # google|youtube|amazon|bing|reddit|duckduckgo|github|stackoverflow
```

## Session
```bash
camofox session save <name> [tabId] [--user <user>]                                   # save session cookies
camofox session load <name> [tabId] [--user <user>]                                   # load session cookies
camofox session list [--format <format>]                                              # list sessions
camofox session delete <name> [--force]                                               # delete session
```

## Auth Vault
```bash
camofox auth save <profile-name> [--url <url>] [--notes <notes>]                      # save encrypted credentials
camofox auth load <profile-name>                                                       # output username only
camofox auth load <profile-name> --inject [tabId] --username-ref <ref> --password-ref <ref> [--user <user>]  # inject secrets
camofox auth list [--format <format>]                                                  # list profiles
camofox auth delete <profile-name>                                                     # delete profile
camofox auth change-password <profile-name>                                            # rotate profile master password
```

## Cookie & Downloads
```bash
camofox cookie export [tabId] [--path <file>] [--user <user>]                         # export cookies
camofox cookie import <file> [tabId] [--user <user>]                                  # import cookies
camofox download [url] [--path <dir>] [--user <user>]                                 # placeholder command
camofox downloads [--user <user>] [--format <format>]                                 # list downloads
```

## Server
```bash
camofox server start [--port <port>] [--background] [--idle-timeout <minutes>]        # start server
camofox server stop                                                                     # stop server
camofox server status [--format <format>]                                              # status
```

## Pipeline
```bash
camofox run <script-file> [--continue-on-error]                                        # run script file or '-'
```

## Diagnostics
```bash
camofox annotate [tabId] [--user <user>] [--output <file>] [--format <format>]        # screenshot + refs
camofox health [--format <format>]                                                      # health report
camofox version [--format <format>]                                                     # version matrix
camofox info [--format <format>]                                                        # config paths/state
```
