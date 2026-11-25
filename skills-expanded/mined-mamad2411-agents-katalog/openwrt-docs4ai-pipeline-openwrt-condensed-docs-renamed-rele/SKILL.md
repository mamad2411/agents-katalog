# AGENTS.md — ucode module

## Scope
ucode is a lightweight scripting language for OpenWrt, similar to JavaScript but NOT JavaScript.

## Language Warning
ucode has JavaScript-like syntax but is a distinct language. Do NOT use Node.js APIs, browser APIs, or ES module syntax.
The runtime is C-based with embedded modules: fs, ubus, uci, uloop, nl80211, rtnl.

## Start Here
- `map.md` → overview of all ucode stdlib and module APIs
- `chunked-reference/c_source-api-module-uci.md` → ucode UCI bindings
- `types/ucode.d.ts` → IDE type definitions for autocompletion
