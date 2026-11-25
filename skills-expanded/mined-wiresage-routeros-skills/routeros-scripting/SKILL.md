---
name: routeros-scripting
description: Writing and running scripts on MikroTik RouterOS 7. Covers the script language (command-line structure, scopes, local and global variables, data types, escapes, operators including the in and regex match operators, loops, conditions, functions with named or positional arguments, :onerror, :retry, arrays, JSON serialize and deserialize), find versus numeric ids, type conversion pitfalls, script permissions and policies (use-script-permissions), single-instance guards, background execution and jobs, the script repository, and events that run scripts (scheduler, Netwatch, DHCP lease scripts, VRRP, logging, MQTT, GPIO, hotspot). Includes a dry-run checker for .rsc files. Use when writing, debugging or reviewing a RouterOS script, generating configuration files for import, or wiring a script to an event.
---

# RouterOS scripting

A script is a list of console commands plus a small language (variables, conditions, loops, functions). Commands run line by line until the end or a runtime
error. Scripts live in `/system/script` or are written inline in event properties (`on-event`, `up-script`, ...). Use the CLI path style `/ip/firewall/filter/add ...`
(slash-separated, as everywhere in this repository) or the space style; both work.

## Check a script file before applying it

`.rsc` files (also what `/export` writes) are applied with `/import`. `verbose=yes dry-run` simulates it and reports syntax errors without changing the configuration;
`dry-run` works only in verbose mode.

```bash
bash scripts/dry-run-import.sh --host 192.0.2.1 --user admin my-config.rsc
```

```powershell
./scripts/dry-run-import.ps1 -HostName 192.0.2.1 -User admin my-config.rsc
```

The scripts upload the file under a temporary name, run `/import file-name=<tmp> verbose=yes dry-run`, print the report, delete the file, and exit 1 when the router
reports errors. A clean dry run proves syntax and command names only, not that every command succeeds at run time. Use `import ... from-line=<n>` to continue
from a failing line and `:onerror e in={ import test.rsc } do={ :put "Failure - $e" }` to catch failures.

## Language essentials

```ros
{
    :local name "ether1"
    :local ids [/interface/find where default-name=$name]
    :foreach id in=$ids do={ :put [/interface/get $id name] }
    :if ([:len $ids] = 0) do={ :log warning "no such interface" } else={ :log info "found" }
    :global counter; :if ([:typeof $counter] = "nothing") do={ :set counter 0 }
    :set counter ($counter + 1)
}
```

- **Structure:** `[prefix] [path] command [uparam] [param=value]...`; end a command with `;` or a newline. `[...]` substitutes a command's result, `(...)` groups an
  expression, `{...}` is a block and a scope. `#` starts a comment, a trailing `\` joins lines (not after a comment). No spaces around `=` in `param=value`, `from=`, `to=`,
  `do=`, `else=`.
- **Scopes:** every console line is its own scope. Declare before use: `:local x 1`, `:global g`; a global must be re-declared (`:global g`) in every script or function that
  uses it. A `:global` declared inside a nested block is not visible outside it. `:set x` with no value unsets a variable. Names are case sensitive, letters and digits only
  (quote others: `:global "my-var"`, reference with `$"my-var"`). Avoid names equal to RouterOS properties (`type`, `name`, `address`...): `:local type "ether1"` breaks `where name=$type`.
- **Types:** `num` (64-bit integer), `bool`, `str`, `ip`, `ip-prefix`, `ip6`, `ip6-prefix`, `id` (`*1F`), `time`, `array`, `nil`. Convert with `:tonum :tostr :toip :toip6 :tobool :toid :totime :toarray`;
  a failed conversion gives `nil`. `:typeof $x` shows the type.
- **Strings:** escapes `\"` `\\` `\n` `\r` `\t` `\$` and `\xx` hex. Write `\$` when a `$` must stay literal (for example inside `source=" ... "` of a script). `"text $var"` interpolates,
  `$[ ... ]` and `$( ... )` embed expressions. Concatenate with `.`.
- **Operators:** arithmetic `+ - * / %` (put spaces or parentheses around `/` so it is not read as an IP prefix), relational `< > = <= >= !=`, logical `! && || and or`, `in` (address in prefix),
  `~` regex match, bitwise `~ | ^ & << >>` on IP and IPv6 values, `->` array element by key, `,` array concatenation.
- **Loops and conditions:** `:for i from=1 to=10 step=1 do={}`, `:foreach x in=$array do={}` (or `:foreach k,v in=...`), `:while (cond) do={}`, `:do {} while=(cond)`, `:if (cond) do={} else={}`. `:return`, `:error "msg"` (stops the script).
- **Arrays:** `{1;2;3}`, `{a=1;b=2}`, `($arr->"b")`, `:set ($arr->"b") 5`, `[:len $arr]`, `[:pick $arr 0 2]`, `[:find $arr "x"]`. An empty array literal `{}` is a syntax error: use `[:toarray ""]`.
  Keys with anything other than lowercase letters need quotes.
- **Functions:** `:global f do={ :return ($a + $b) }`, call `[$f a=6 b=2]` or positionally `$1 $2`. Declare other functions you call (`:global g;`) inside the body. Avoid parameter names equal to global variable names.
  `:parse "..."` builds a function from a string; `:parse [/system/script/get myScript source]` reuses a stored script.
- **Errors:** `:onerror e in={ ... } do={ :log error $e }` catches runtime errors (for example `:resolve` failures); `:onerror e {:retry command={...} delay=1 max=3} do={...}` retries.
- **Output and logging:** `:put` prints, `:log info|warning|error|debug "text"` writes to the log (topic `script`), `/log/info "text"` is the CLI form.
- **JSON and DSV:** `:serialize $value to=json`, `:deserialize $text from=json`; `/tool/fetch ... as-value output=user` returns response data to scripts (`routeros-system-utilities`).
- **Time and misc:** `:delay 5s`, `:time { ... }`, `:timestamp`, `:rndnum from=1 to=9`, `:rndstr length=8`, `:resolve name`, `:execute { ... }` runs in the background, `:environment print` lists variables.

## Pitfalls that cause most bugs

1. **Never address items by printed number** in a script. `/ip/route/set 1 ...` fails because print numbers are not stored. Use `find`: `/ip/route/set [find dst-address=0.0.0.0/0] gateway=...`.
   Internal ids (`*1`) can change when items are re-added.
2. **String versus IP comparisons:** `where address=111.111.1.1/24` can match nothing because the left side is a string. Quote it (`address="111.111.1.1/24"`) or `[:tostr $ip]`.
3. **`find` returns an array**; wrap it in `[:len ...]` or a `:foreach` and handle zero or several results before calling `get` or `set`.
4. **Strip a mask:** `[:pick $addr 0 [:find $addr "/"]]`.
5. **Undeclared variable = compile error;** an undeclared `$name` in a lease script or similar refers to built-in variables supplied by the caller.
6. **Passwords and secrets in `source=`** stay in the configuration and exports. Read them from files or secrets handling instead, and mark scripts that handle them with minimal policies.
7. Files: you cannot create a file directly; `/file/print file=myFile` then `/file/set myFile.txt contents=""`. Append by reading `contents` and writing the concatenation.

## Permissions and jobs

- A script has `owner`, `policy` and `dont-require-permissions`. A script called by name from a scheduler entry (or `/system/script/run`) runs with the **caller's** permissions;
  `use-script-permissions` makes it run with its own. A caller cannot run a script whose policy needs permissions the caller lacks (`not enough permissions (9)`).
  Give event scripts only the policies they need (`read`, `write`, `test`, `reboot`, `policy`, `password`, `sensitive`, ...).
- Netwatch scripts run as an internal user with `read`, `write`, `test`, `reboot` only; CMR and SNMP scripts have restricted sets as well (`routeros-diagnostics-monitoring`, `routeros-management-tools`).
- Single-instance guard: `:if ([/system/script/job/print count-only as-value where script=[:jobname]] > 1) do={ :error "already running" }`. `/system/script/job` lists running jobs, `run-count` and `last-started` live on the script.
- Global variables belong to the user that runs the script (`/system/script/environment` lists them) and are not shared with Netwatch scripts.

## Events that run scripts

| Event | Where |
| --- | --- |
| Schedule | `/system/scheduler` `on-event` (`routeros-system-utilities`) |
| Host up/down | `/tool/netwatch` `up-script`, `down-script`, `test-script` |
| Rate threshold | `/tool/traffic-monitor` (`routeros-diagnostics-monitoring`) |
| Log message | `/system/logging/action` `target=script` |
| DHCP lease | `lease-script` with `$leaseBound`, `$leaseActIP`, `$leaseActMAC`, `$leaseServerName` (`routeros-dhcp`) |
| VRRP state | `on-master`, `on-backup`, `on-fail` (`routeros-high-availability`) |
| MQTT message, GPIO change | `on-message`, `script` (`routeros-iot`) |
| Hotspot login | `on-login`, `on-logout` with `$user` (`routeros-hotspot`) |
| Mode, reset and WPS buttons | `/system/routerboard/mode-button` `on-event` (`routeros-hardware`) |

## Where to look

| Need | Open |
| --- | --- |
| Complete language reference: global commands (convert, grep, onerror, retry, serialize, ...), print parameters, common commands | `references/guides/developer-guides/scripting.md` |
| Worked examples (files, IP change detection, DNS resolve, queue stats, e-mailed backup) | `.../scripting/scripting-examples.md` |
| Tips (ids, find, empty arrays, as-value, removing variables) | `.../scripting/scripting-tips-and-tricks.md` |
| Properties | `references/cli/system/script.md`, `.../script/job.md`, `.../script/environment.md` |
| Everything else | `references/INDEX.md` |

Related skills: `routeros-api` (drive the router from outside), `routeros-fundamentals` (CLI, safe mode, export/import), `routeros-system-utilities` (scheduler, fetch, e-mail),
`routeros-diagnostics-monitoring`, `routeros-initial-setup` (backups and exports).
