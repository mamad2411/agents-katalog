---
name: network-map
description: Map what a program does on the network. Which functions open connections, what hosts and URLs it talks to, and what it sends.
---

# Network map

Goal: show the user every place the program touches the network, and what it says there.

1. In `list_procedures`, find the networking imports: sockets (connect, send, recv), higher-level clients (NSURLSession, CFNetwork, curl, libcurl), and DNS calls.
2. For each, use `procedure_callers` to find the functions in this program that call it. Those are the call sites that matter.
3. In `list_strings`, find hosts, URLs, schemes, ports and request paths. Follow `xrefs` from each to the code that uses it, and `resolve_containing_procedure` to name that function.
4. Read the call sites. Work out what each request sends and when it fires (at launch, on a timer, on a user action).

For each endpoint, `rename_function` the function that talks to it and `add_note` what it sends. `open_function` the most important one.

Report a short table: host or URL, which function calls it, what it sends, and when. Flag anything sent in the clear or anything that looks like it leaves the machine without the user knowing.
