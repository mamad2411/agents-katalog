---
name: openbullet2
description: Comprehensive OpenBullet 2 automation/testing framework skill — LoliCode syntax reference, block catalog, config authoring, C# interop, proxy patterns, execution model, pitfalls, and workflows.
version: 1.0.0
author: hermes
category: cybersecurity
tags: [openbullet, ob2, lolicode, automation, config-making, rurilib, credential-testing, web-automation]
---

# OpenBullet 2 — Comprehensive Reference

OpenBullet 2 (OB2) is an open-source automation/web-testing framework written in C# on .NET 8. It uses a visual block-stacking interface (Stacker) backed by a scripting language called **LoliCode**, which compiles to C# at runtime. OB2 is commonly used for credential validation, web scraping, and automated interaction with web targets.

**Repository:** https://github.com/openbullet/OpenBullet2
**Core Library:** RuriLib (contains all block definitions, LoliCode parser, transpilers, execution engine)
**Official Forum:** https://discourse.openbullet.dev (Cloudflare-gated)

---

## Architecture Overview

- **OpenBullet2.Web** — Angular web client + REST API (MCP-compatible endpoints for config making)
- **OpenBullet2.Native** — Avalonia desktop client
- **RuriLib** — Core engine: blocks, LoliCode, transpilers, BotData, proxies, HTTP client
- **RuriLib.Http** — Custom HTTP handler
- **RuriLib.Parallel** — Parallel execution engine
- **RuriLib.Proxies** — Proxy pool management

---

## Config Structure

An OB2 config is NOT just a script. It contains:

1. **Metadata** — name, author, category
2. **Settings** — allowed wordlist types, custom inputs, proxy defaults, resources, data rules, script usings
3. **Main Script** — per-bot logic (LoliCode + blocks + C#)
4. **Startup Script** (optional) — shared initialization before bots start
5. **Readme** (optional) — operator-facing usage notes

### Config Settings (ConfigSettings.cs fields)

- `AllowedWordlistTypes` — which wordlist types this config accepts
- `CustomInputs` — extra `input.*` variables the operator can provide (API keys, domains, etc.)
- `ProxySettings` — proxy suggestions, max uses, ban evasion, allowed types, ban statuses
- `DataRules` — post-slice validation rules per slice
- `Resources` — named resource pools (lines, combos, etc.)
- `CustomUsings` — extra C# namespace imports for compilation
- `SaveEmptyCaptures` — whether to capture empty strings

---

## Runtime Execution Model

### Script Lifecycle

1. **Startup script** runs once before bots start
   - Only `globals` is available (no `input`, no `data`)
   - Used for shared auth tokens, counters, caches
2. **Main script** runs once per bot
   - `input`, `data`, `globals` are all available
   - Many bots can execute in parallel in multi-run jobs

### Key Runtime Variables

#### `input` — Per-Bot Input Data
- `input.USERNAME`, `input.PASSWORD`, `input.DATA` — from wordlist slices
- Custom inputs also appear as `input.*` (e.g., `input.apiKey`, `input.baseUrl`)
- All values are **strings**

#### `data` — Per-Bot Runtime State
| Property | Type | Description |
|---|---|---|
| `data.STATUS` | string | Current bot status |
| `data.RAWSOURCE` | byte[] | Last HTTP response body (raw) |
| `data.SOURCE` | string | Last HTTP response body (text) |
| `data.ERROR` | string | Last caught safe-mode error |
| `data.ADDRESS` | string | Last absolute response URL |
| `data.RESPONSECODE` | int | Last HTTP status code |
| `data.COOKIES` | Dictionary | Cookies seen so far |
| `data.HEADERS` | Dictionary | Headers of last response |
| `data.Objects` | IDisposable | Shared disposable objects |
| `data.MarkedForCapture` | List | Variables marked for capture |
| `data.BOTNUM` | int | Bot number (0 in debugger) |
| `data.UseProxy` | bool | Whether bot is using a proxy |
| `data.Proxy` | Proxy | Current proxy or null |
| `data.Line.Data` | string | The whole unsplit data line |
| `data.Line.Retries` | int | Retry count |
| `data.ConfigSettings` | object | Current config settings |
| `data.Random` | Random | Per-bot RNG |
| `data.CancellationToken` | CancellationToken | Cancellation token |
| `data.AsyncLocker` | object | Async lock provider |
| `data.Logger` | Logger | Bot logger instance |

**Useful `data` methods:**
- `data.MarkForCapture(string varName)`
- `data.Logger.Log(...)`, `data.Logger.LogObject(...)`, `data.Logger.Clear()`

#### `globals` — Shared State (ExpandoObject)
- Shared across ALL bots of a run
- Add properties at runtime: `globals.Token = "abc"`
- **Reserved:** `globals.JobId`, `globals.Resources`, `globals.OwnerId`
- **MUST lock** when multiple bots mutate the same state

### End Statuses

| Status | Meaning | Hit? | Proxy Effect |
|---|---|---|---|
| `SUCCESS` | Positive checked outcome | Yes | None |
| `FAIL` | Negative checked outcome | No | None |
| `NONE` | Ambiguous / "to check" | Yes | None |
| `RETRY` | Transient issue, retry same data | No | None |
| `BAN` | Proxy is the problem | No | Bans proxy |
| `ERROR` | Runtime failure | No | None |
| `CUSTOM` | Named outcome | Yes | Varies |

**Critical:** `NONE` counts as a hit. Do NOT invent custom statuses unless defined in `Environment.ini`.

---

## LoliCode Language Reference

LoliCode is OB2's primary scripting language. It compiles to C# and can contain **inline C# directly**. Scripts can mix:
- **Blocks** — structured OB2 operations
- **LoliCode statements** — flow control, logging, variables
- **C# code** — any valid C# for custom logic

### Block Syntax

```loli
BLOCK:BlockId
[LABEL:Custom label]
[DISABLED]
[SAFE]
  settingName = settingValue
  => VAR @outputVariable
ENDBLOCK
```

- `BLOCK:Id` — block identifier (e.g., `BLOCK:HttpRequest`, `BLOCK:Keycheck`)
- `LABEL:` — optional custom label for logging/UI
- `DISABLED` — block is skipped entirely
- `SAFE` — exceptions are caught and stored in `data.ERROR`
- `=> VAR @var` — capture return value as variable
- `=> CAP @var` — capture return value AND mark for capture

**Setting value forms:**
- Fixed: `"hello"`, `123`, `true`, `GET`, `["a", "b"]`
- Interpolated: `$"Hello <input.USERNAME>"`
- Variable: `@token`

### LoliCode Statements

#### LOG — Print to debugger log
```loli
LOG "hello"
LOG $"Hello <input.USERNAME>"
```

#### CLOG — Colored log
```loli
CLOG YellowGreen "hello"
CLOG SkyBlue $"Token: <token>"
```
Color names use PascalCase (e.g., `YellowGreen`, `SkyBlue`, `Red`).

#### JUMP — Goto label
```loli
#HERE
LOG "loop"
JUMP #HERE
```
⚠️ Can create endless loops. Use carefully.

#### REPEAT — Fixed iteration loop
```loli
REPEAT 5
LOG "hello"
END
```

#### FOREACH — Iterate list
```loli
FOREACH elem IN list
  LOG elem
END
```

#### WHILE — Conditional loop
```loli
WHILE INTKEY 1 LessThan 2
  LOG "looping"
END
```

#### IF / ELSE IF / ELSE — Conditional branching
```loli
IF INTKEY 5 LessThan 1
  LOG "nope"
ELSE IF INTKEY 5 LessThan 3
  LOG "nope again"
ELSE
  LOG "yep"
END
```
The entire chain closes with a single `END`.

#### TRY / CATCH / FINALLY — Exception handling
```loli
TRY
  // code that may fail
CATCH
  // fallback path
FINALLY
  // cleanup
END
```
`FINALLY` is critical for async lock management.

#### LOCK — Synchronous critical section
```loli
LOCK globals
  TRY
    globals.Count++;
  CATCH
    globals.Count = 1;
  END
END
```

#### ACQUIRELOCK / RELEASELOCK — Async-safe critical section
```loli
ACQUIRELOCK globals
TRY
  // async operations
CATCH
  throw;
FINALLY
  RELEASELOCK globals
END
```
⚠️ **Always** pair `ACQUIRELOCK` with `RELEASELOCK`. Put `RELEASELOCK` in `FINALLY`.

#### SET VAR — Set string variable
```loli
SET VAR @myString "variable"
LOG myString
```

#### SET CAP — Set variable AND mark for capture
```loli
SET CAP @myCapture "capture"
LOG myCapture
```
Prefer `SET CAP` over `SET VAR` + `MARK` when capturing directly.

#### SET USEPROXY — Enable/disable proxy
```loli
SET USEPROXY TRUE
SET USEPROXY FALSE
```

#### SET PROXY — Explicitly set proxy
```loli
SET PROXY "127.0.0.1" 9050 SOCKS5
SET PROXY "127.0.0.1" 9050 SOCKS5 "username" "password"
```
Proxy types: `HTTP`, `SOCKS4`, `SOCKS4A`, `SOCKS5`

#### MARK / UNMARK — Add/remove capture variable
```loli
MARK @myVar
UNMARK @myVar
```

#### TAKEONE — Take one item from a config resource
```loli
TAKEONE FROM "resourceName" => @myString
```

#### TAKE — Take multiple items from a config resource
```loli
TAKE 5 FROM "resourceName" => @myList
```

### Inline C# Interop

LoliCode compiles to C#. You can mix C# directly:

```loli
// Define a C# helper method
int Add(int first, int second)
{
  return first + second;
}

// Use blocks
BLOCK:RandomInteger
  minimum = 0
  maximum = 10
  => VAR @num1
ENDBLOCK

// Mix C# with LoliCode
int result = Add(num1, 5);
LOG $"Result: {result}"
```

**Custom usings** are required for non-default namespaces:
- `System.Text.RegularExpressions` for `Regex`
- `System.Linq` for LINQ
- `System.Net` for `WebClient`, etc.

Add via Config Settings > Custom Usings.

### Script Block (Foreign Language Interop)

```loli
BLOCK:Script
INTERPRETER:Python
INPUT x,y
BEGIN SCRIPT
result = x + y
END SCRIPT
OUTPUT Int @result
ENDBLOCK
```

**Interpreters:**
| Interpreter | Status | Notes |
|---|---|---|
| `Python` | ✅ Preferred | CPython; auto-downloads 3.14 or uses `Scripts/.venv` |
| `NodeJS` | ✅ Preferred | Requires Node on system; packages from `Scripts/node_modules` |
| `IronPython` | ⚠️ Legacy | Python 2 semantics; planned deprecation |
| `Jint` | ⚠️ Legacy | Planned deprecation |

**Python details:**
- If `Scripts/.venv` exists → uses that venv
- Otherwise → auto-downloads Python 3.14 redistributable
- Shared CPython runtime across process; cannot switch without restart
- Prefer async libraries (`httpx`, `aiohttp`) for network-heavy scripts

**NodeJS details:**
- Requires Node installed on target system
- Third-party packages must be in `Scripts/node_modules`
- Do NOT assume Node/npm packages are available on unknown installations

**Supported INPUT/OUTPUT types:** `String`, `Int`, `Float`, `Bool`, `ListOfStrings`, `DictionaryOfStrings`, `ByteArray`

---

## Block Catalog (RuriLib Source)

All blocks live under `RuriLib/Blocks/{Category}/`. Each has a `[BlockCategory]` attribute and `[Block]` methods.

### Block Categories

| Category | Color | Description |
|---|---|---|
| **Requests** | — | HTTP requests (GET, POST, PUT, etc.) |
| **Parsing** | — | Regex, JSON, HTML, CSS parsing |
| **Captchas** | — | CAPTCHA solving (reCAPTCHA, hCaptcha, FunCaptcha, etc.) |
| **Browser** | — | Selenium/Puppeteer/Playwright browser automation |
| **Functions** | — | Crypto, String, Conversions, Time, Files, SQL, Images |
| **Conditions** | — | IF branching with typed comparisons |
| **Utility** | — | Sleep, Write/Append file, process execution |
| **Interop** | — | Script interpreters, DLL calls, custom C# |
| **LoliCode** | #303030 | Raw LoliCode script block |

### HTTP Request Blocks (Requests/Http/Methods.cs)

```loli
BLOCK:HttpRequest
  url = "https://example.com/api"
  method = GET
  [headers = {"Key": "Value"}]
  [cookies = ""]
  [content = ""]
  [contentType = "application/x-www-form-urlencoded"]
  [timeout = 10000]
  => VAR @response
ENDBLOCK
```

Key methods:
- `HttpRequest` — Standard HTTP request (GET, POST, PUT, DELETE, PATCH, HEAD, OPTIONS)
- `RecaptchaV2` — Solve reCAPTCHA v2
- `RecaptchaV3` — Solve reCAPTCHA v3
- `Hcaptcha` — Solve hCaptcha
- `Funcaptcha` — Solve FunCaptcha
- `GeeTest` — Solve GeeTest
- `Cloudflare` — Handle CF challenges
- `AwsWaf` — Handle AWS WAF

### Parsing Blocks (Parsing/Methods.cs)

- `RegexMatch` — Match regex pattern, return first match
- `RegexMatchAll` — Match regex pattern, return all matches
- `ParseJson` — Parse JSON with JToken path
- `CssSelector` — Select HTML elements with CSS selector
- `Xpath` — Select XML/HTML elements with XPath
- `Linq` — Use LINQ-to-JSON for complex JSON queries
- `Split` — Split string by delimiter
- `Base64Decode` / `Base64Encode`
- `HtmlDecode` / `HtmlEncode`

### Condition Blocks (Conditions/Methods.cs)

```loli
BLOCK:Keycheck
  KEYCHAIN SUCCESS OR
    STRINGCONTAINS @data.SOURCE "Welcome"
    KEYCHECK 200 LESS @data.RESPONSECODE
  KEYCHAIN FAIL OR
    STRINGCONTAINS @data.SOURCE "Invalid"
    KEYCHECK 403 EQUAL @data.RESPONSECODE
  KEYCHAIN BAN OR
    KEYCHECK 403 EQUAL @data.RESPONSECODE
  KEYCHAIN RETRY OR
    KEYCHECK 502 EQUAL @data.RESPONSECODE
ENDBLOCK
```

Condition types:
- `STRINGCONTAINS` — Substring check
- `KEYCHECK` — Numeric comparison (EQUAL, NOTEQUAL, LESS, GREATERTHAN, LESSEQUAL, GREATEREQUAL)
- `REGEXMATCH` — Regex match check
- `ISEMPTY` / `ISNOTEMPTY` — Null/empty check

### Crypto Blocks (Functions/Crypto/Methods.cs)

| Block | Parameters | Returns |
|---|---|---|
| `XOR` | bytes, key | byte[] |
| `XOR Strings` | text, key | string |
| `Hash` | input, HashFunction | byte[] |
| `HashString` | input, HashFunction | string (HEX lowercase) |
| `NTLM Hash` | input | byte[] |
| `Hmac` | input, key, HashFunction | byte[] |
| `HmacString` | input, key, HashFunction | string (HEX lowercase) |
| `ScryptString` | password, salt, iterationCount, blockSize, threadCount | string |
| `Scrypt Derive Key` | password, salt, outputSize, iterationCount, blockSize, threadCount | string (HEX) |
| `RSA Encrypt` | plainText, modulus, exponent, useOAEP | byte[] |
| `RSA Decrypt` | cipherText, modulus, d, useOAEP | byte[] |
| `RSA PKCS1PAD2` | plainText, hexModulus, hexExponent | byte[] |
| `PBKDF2PKCS5` | password, salt, saltSize, iterations, keyLength, HashFunction | byte[] |
| `AES Encrypt` | plainText, key, iv, mode, padding, keySize | byte[] |
| `AES Encrypt String` | plainText, key, iv, mode, padding, keySize | byte[] |
| `AES Decrypt` | cipherText, key, iv, mode, padding, keySize | byte[] |
| `AES Decrypt String` | cipherText, key, iv, mode, padding, keySize | string |
| `JWT Encode` | algorithm, secret, extraHeaders, payload | string |
| `BCrypt Hash` | input, salt | string |
| `BCrypt Hash (Gen Salt)` | input, workFactor | string |
| `BCrypt Verify` | input, hash | bool |

**HashFunction enum:** `MD4`, `MD5`, `SHA1`, `SHA256`, `SHA384`, `SHA512`

**CipherMode:** `CBC`, `ECB`, `CFB`, `OFB`, `CTS`

**PaddingMode:** `None`, `PKCS7`, `Zeros`, `ANSIX923`, `ISO10126`

**JwtAlgorithmName:** `HS256`, `HS384`, `HS512`, `RS256`, `RS384`, `RS512`, `ES256`, `ES384`, `ES512`

### String Function Blocks (Functions/StringFunctions/Methods.cs)

| Block | Parameters | Returns |
|---|---|---|
| `CountOccurrences` | input, word | int |
| `Substring` | input, index, length | string |
| `Reverse` | input | string |
| `Trim` | input | string |
| `Length` | input | int |
| `ToUppercase` | input | string |
| `ToLowercase` | input | string |
| `Replace` | original, toReplace, replacement | string |
| `RegexReplace` | original, pattern, replacement | string |
| `Translate` | input, translations dict, replaceOne | string |
| `UrlEncode` | input | string |
| `UrlDecode` | input | string |
| `EncodeHTMLEntities` | input | string |
| `DecodeHTMLEntities` | input | string |
| `RandomString` | mask, customCharset | string |
| `Generate GUID` | version (V4/V7), format (D/N/B/P) | string |

**RandomString mask tokens:**
| Token | Charset |
|---|---|
| `?l` | lowercase (a-z) |
| `?u` | uppercase (A-Z) |
| `?d` | digits (0-9) |
| `?s` | symbols |
| `?h` | hex lowercase (0-9a-f) |
| `?H` | hex uppercase (0-9A-F) |
| `?f` | upper + lower |
| `?i` | upper + lower + digits |
| `?a` | all (upper + lower + digits + symbols) |
| `?m` | upper + digits |
| `?n` | lower + digits |
| `?c` | custom charset |
| `{N}` | repeat token N times (e.g., `?d{10}`) |

Example: `?u?l?d{6}?s{2}` = 1 uppercase + 1 lowercase + 6 digits + 2 symbols

### Captcha Blocks (Captchas/Methods.cs)

| Block | Service | Parameters |
|---|---|---|
| `RecaptchaV2` | 2Captcha, AntiCaptcha, CapMonster, CapSolver, CaptchaAI, EzCaptcha, HumanCaptcha, NextCaptcha, NoCaptchaAI, CapGuru, BestCaptchaSolver, DeathByCaptcha, SolveCaptcha, TrueCaptcha, Yescaptcha | siteKey, siteUrl, service, apiKey |
| `RecaptchaV3` | Same services | siteKey, siteUrl, action, minScore, service, apiKey |
| `Hcaptcha` | Same services | siteKey, siteUrl, service, apiKey |
| `Funcaptcha` | Same services | publicKey, serviceUrl, service, apiKey |
| `GeeTest` | Same services | gt, challenge, apiServer, service, apiKey |
| `Turnstile` | Same services | siteKey, siteUrl, service, apiKey |
| `AmazonWaf` | Same services | siteKey, siteUrl, service, apiKey |
| `LeminCaptcha` | Same services | captchaId, service, apiKey |
| `CapyCaptcha` | Same services | captchKey, service, apiKey |
| `DataDome` | Same services | captchaUrl, service, apiKey |
| `CyberSiAra` | Same services | masterUrl, service, apiKey |

### Interop Blocks (Interop/Methods.cs)

| Block | Description |
|---|---|
| `Script` | Run Python, NodeJS, IronPython, Jint scripts |
| `DllCall` | Call native DLL functions |
| `ExecuteCSharp` | Compile and run arbitrary C# code |

### Utility Blocks (Utility/Methods.cs)

| Block | Description |
|---|---|
| `Sleep` | Wait N milliseconds |
| `WriteFile` | Write text to file |
| `AppendFile` | Append text to file |
| `StartProcess` | Launch external process |
| `SetVariable` | Set a named variable |
| `IncrementVariable` | Increment numeric variable |

---

## Wordlists & Environment

### Wordlist Type Definition (Environment.ini)

```ini
[WORDLIST TYPE]
Name=Credentials
Regex=^.*:.*$
Verify=True
Separator=:
Slices=USERNAME,PASSWORD
```

- `Name` — wordlist type identifier
- `Regex` — raw line validation pattern
- `Verify` — enforce regex before execution
- `Separator` — character to split lines on
- `Slices` — comma-separated `input.*` variable names

**Validation order:** Regex → Split → Data Rules → Script

**Changes to Environment.ini require OB2 restart.**

### Data Rules (Config-level)

Applied after slicing. Use for:
- Stricter constraints than the base wordlist type
- Per-slice validation
- Rejecting known-bad patterns before making requests

Failed data rule → line marked `INVALID` in multi-run.

---

## Proxy System

### Config-Level Proxy Settings
- Whether proxies are suggested by default
- Maximum uses per proxy
- Ban loop evasion
- Which end statuses ban a proxy
- Allowed proxy types

### Script-Level Proxy Control

```loli
SET USEPROXY TRUE
SET PROXY "127.0.0.1" 9050 SOCKS5 "username" "password"
```

### `data.Proxy` Fields
- `Type`, `Host`, `Port`, `Username`, `Password`
- `WorkingStatus`, `Country`, `Ping`, `LastUsed`, `ProxyStatus`

⚠️ `data.Proxy` can be `null` — always null-check before using in C#.

### Debugger Proxy syntax:
- `127.0.0.1:8000`
- `127.0.0.1:8000:username:password`
- `(socks5)127.0.0.1:8000`
- `(http)127.0.0.1:8000:username:password`

---

## Keycheck Patterns

The Keycheck block is the central decision-making block:

```loli
BLOCK:Keycheck
  KEYCHAIN SUCCESS OR
    STRINGCONTAINS @data.SOURCE "Welcome"
  KEYCHAIN FAIL OR
    STRINGCONTAINS @data.SOURCE "Invalid"
    STRINGCONTAINS @data.SOURCE "not found"
  KEYCHAIN NONE OR
    STRINGCONTAINS @data.SOURCE "pending"
  KEYCHAIN BAN OR
    KEYCHECK 403 EQUAL @data.RESPONSECODE
  KEYCHAIN RETRY OR
    KEYCHECK 502 EQUAL @data.RESPONSECODE
  KEYCHAIN ERROR OR
    KEYCHECK 0 EQUAL @data.RESPONSECODE
ENDBLOCK
```

**Rules:**
- `OR` = any condition matches → status applied
- `AND` = all conditions must match
- Order matters: first matching keychain wins
- Use `BAN` only for actual proxy issues, not catch-all
- Overusing `BAN` causes ban loops

---

## External Libraries / Plugins

- Place `.dll` + dependencies in `UserData/Plugins/`
- Restart OB2
- Import namespace via custom usings
- Do NOT add duplicate copies of already-bundled libraries
- Document plugin dependencies in config readme

---

## Complete Config-Making Workflow

1. **Create config** — define metadata, category
2. **Get environment** — inspect wordlist types, custom statuses
3. **Plan script** — determine blocks, C#, LoliCode mix
4. **List blocks** — discover candidate blocks by category
5. **Get block details** — exact parameter names, types, enums, return type
6. **Configure settings** — wordlist types, custom inputs, proxy behavior, data rules, usings
7. **Write script** — LoliCode + blocks + C#
8. **Convert to C#** — inspect emitted code if behavior is unclear
9. **Debug** — test with `debug_config`, test data, and test proxy
10. **Finalize** — metadata, readme, document dependencies

---

## Common Patterns

### Login Check Pattern
```loli
BLOCK:HttpRequest
  url = $"https://example.com/login"
  method = POST
  content = $"username=<input.USERNAME>&password=<input.PASSWORD>"
  contentType = "application/x-www-form-urlencoded"
ENDBLOCK

BLOCK:Keycheck
  KEYCHAIN SUCCESS OR
    STRINGCONTAINS @data.SOURCE "dashboard"
  KEYCHAIN FAIL OR
    STRINGCONTAINS @data.SOURCE "invalid credentials"
  KEYCHAIN BAN OR
    KEYCHECK 429 EQUAL @data.RESPONSECODE
ENDBLOCK
```

### Token Extraction Pattern
```loli
BLOCK:HttpRequest
  url = "https://api.example.com/auth"
  method = POST
  content = $"{{\"user\":\"<input.USERNAME>\",\"pass\":\"<input.PASSWORD>\"}}"
  contentType = "application/json"
ENDBLOCK

BLOCK:ParseJson
  json = @data.SOURCE
  jTokenPath = "access_token"
  => CAP @token
ENDBLOCK
```

### Shared State Pattern (Startup + Main)
```loli
// STARTUP SCRIPT
BLOCK:HttpRequest
  url = "https://api.example.com/init"
  method = GET
  => VAR @initResponse
ENDBLOCK

BLOCK:ParseJson
  json = @initResponse
  jTokenPath = "session_token"
  => VAR @sessionToken
ENDBLOCK

SET VAR @globals.SessionToken sessionToken

// MAIN SCRIPT
LOG $"Using session: <globals.SessionToken>"
```

### Async Lock Pattern
```loli
ACQUIRELOCK globals
TRY
  globals.Counter = globals.Counter + 1;
CATCH
  throw;
FINALLY
  RELEASELOCK globals
END
```

---

## Pitfalls & Common Mistakes

### ❌ Variable Scope in Inner Blocks
Variables created inside `IF`, `REPEAT`, `FOREACH`, `WHILE` may NOT persist to script end for capture.
**Fix:** Define variable in outer scope first, then assign inside.

### ❌ Using `data` in Startup Script
`data` and `input` are NOT available in startup. Only `globals` exists.
**Fix:** Use `globals` for startup results, read them in main script.

### ❌ Overusing BAN Status
Broad BAN keychains cause ban loops that burn through all proxies.
**Fix:** Make BAN conditions specific. Use `NONE` for ambiguous cases.

### ❌ Assuming Wordlist Slices Exist
Not all wordlist types define the same slices.
**Fix:** Always check `Environment.ini` for the selected type's `Slices` field.

### ❌ Inventing Custom Statuses
Custom statuses must be defined in `Environment.ini`.
**Fix:** Use `get_environment` first; only use defined statuses.

### ❌ Missing Custom Usings
C# code using non-default namespaces will fail compilation.
**Fix:** Add required namespaces to config's custom usings.

### ❌ Null Proxy Access
`data.Proxy` is `null` when proxies are disabled.
**Fix:** Null-check: `if (data.Proxy != null) { ... }`

### ❌ Blocking Python in Parallel
CPython runtime is shared; blocking code bottlenecks all bots.
**Fix:** Use async libraries (`httpx`, `aiohttp`) for network I/O.

### ❌ Assuming Node/npm Available
NodeJS interpreter requires system Node installation.
**Fix:** Document dependency in config readme; prefer built-in blocks or C#.

### ❌ SAFE Mode Swallowing Errors
`SAFE` catches exceptions silently into `data.ERROR`. If you forget to check `data.ERROR`, failures are invisible.
**Fix:** After SAFE blocks, check `data.ERROR` if logic depends on success.

### ❌ FOREACH Variable Not Persisting
The loop variable from `FOREACH elem IN list` doesn't survive after `END`.
**Fix:** Copy to outer-scope variable if needed later.

### ❌ Globals Without Locking
Multiple bots mutating `globals` without locks = race conditions.
**Fix:** Use `LOCK globals` (sync) or `ACQUIRELOCK globals`/`RELEASELOCK globals` (async).

### ❌ Debugger ≠ Multi-Run
Debugger uses 1 bot. Concurrency bugs don't show up in debugger.
**Fix:** Always validate shared-state logic conceptually, not just via debugger.

### ❌ Environment.ini Changes
Editing `Environment.ini` requires OB2 restart to take effect.
**Fix:** Restart after modifying environment config.

---

## Transpiler Architecture

OB2 converts LoliCode through these transpilers:

1. **LoliCode → Stack** (`Loli2StackTranspiler`) — Parses LoliCode text into a stack of BlockInstance objects
2. **Stack → C#** (`Stack2CSharpTranspiler`) — Compiles block stack into executable C#
3. **Stack → LoliCode** (`Stack2LoliTranspiler`) — Serializes block stack back to LoliCode text
4. **LoliCode → C#** (chained: Loli→Stack→C#) — Full compilation pipeline

Use `convert_lolicode_to_csharp` to inspect emitted C# when behavior is unclear.

---

## MCP API Endpoints (OpenBullet2.Web)

OB2 exposes MCP-compatible REST endpoints for config making:

| Endpoint | Purpose |
|---|---|
| `create_config` | Create a new config |
| `get_environment` | Get wordlist types, custom statuses |
| `get_config_making_guide` | Get this guide |
| `get_config_making_topic` | Get deep-dive topic by id |
| `list_blocks` | List blocks by category |
| `get_block_details` | Get block parameter details |
| `get_config_settings` | Read config settings |
| `update_config_settings` | Update config settings |
| `get_config_lolicode` | Read main/startup script |
| `update_config_lolicode` | Write main/startup script |
| `convert_lolicode_to_csharp` | Inspect emitted C# |
| `debug_config` | Run config with test data |
| `get_config_metadata` / `update_config_metadata` | Config metadata |
| `get_config_readme` / `update_config_readme` | Config readme |

---

## Version History

- **0.1.x** — Initial releases, SilverBullet fork era
- **0.2.0** — Major rewrite, new block system
- **0.3.0** — Migration to .NET 8, Angular web client, REST API, MCP integration, Playwright support
- **Latest** — .NET 8, cross-platform, MCP-compatible API, Python 3.14 auto-download, GUID v7

---

## Quick Reference Card

```
┌─────────────────────────────────────────────────┐
│ LoliCode Quick Syntax                           │
├─────────────────────────────────────────────────┤
│ LOG "text" / LOG $"<var>"                       │
│ CLOG Color "text"                               │
│ SET VAR @name "value"                           │
│ SET CAP @name "value"  (capture)                │
│ MARK @name / UNMARK @name                       │
│ SET USEPROXY TRUE/FALSE                         │
│ SET PROXY "host" port TYPE ["user" "pass"]      │
│ IF/ELSE IF/ELSE ... END                         │
│ WHILE INTKEY x LessThan y ... END               │
│ REPEAT N ... END                                │
│ FOREACH item IN list ... END                    │
│ TRY/CATCH/FINALLY ... END                       │
│ LOCK globals ... END                            │
│ ACQUIRELOCK globals / RELEASELOCK globals       │
│ JUMP #LABEL / #LABEL                            │
│ TAKEONE FROM "res" => @var                      │
│ TAKE N FROM "res" => @var                       │
│ BLOCK:Id settings => VAR/CAP @var ENDBLOCK      │
│ SAFE = catch errors into data.ERROR             │
│ DISABLED = skip block                           │
└─────────────────────────────────────────────────┘
```
