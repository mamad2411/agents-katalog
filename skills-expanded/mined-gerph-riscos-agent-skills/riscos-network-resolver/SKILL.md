---
name: riscos-network-resolver
description: Use and explain the RISC OS Resolver module, including DNS lookups, SWIs, commands, configuration variables, cache control, service calls, and returned hostent data. Use when implementing, reviewing, documenting, or integrating with Resolver from applications or modules.
metadata:
  author: gerph@gerph.org
license: MIT
---
# RISC OS Resolver

Use this skill when the task is about the RISC OS `Resolver` module.
This skill is intended to stand alone, so it includes the operational details needed to use Resolver even when the original source tree is not available.

## What Resolver does

Resolver provides shared host name and address resolution for RISC OS.
It sits between applications and DNS servers, with local caching.

Typical lookup flow:

* The caller asks Resolver for a host lookup.
* Resolver checks its cache first.
* Resolver may satisfy the request from local sources such as `InetDBase:Hosts`.
* If needed, Resolver sends DNS queries to configured nameservers.
* The caller either blocks until completion or polls until the request completes, depending on which SWI is used.

Resolver returns results as NetBSD-style `struct hostent` data.
Treat returned `hostent` structures as read-only.

## Main interfaces

Resolver provides:

* `*ResolverConfig`
* `Resolver_GetHostByName`
* `Resolver_GetHost`
* `Resolver_CacheControl`
* `Resolver_DCI4Statistics`

Do not use `Resolver_GetCache` in new code.
It is treated as internal-only.

## SWI numbers

Resolver uses SWI chunk base `&46000`.

The SWIs are:

* `Resolver_GetHostByName = &46000`
* `Resolver_GetHost       = &46001`
* `Resolver_GetCache      = &46002`
* `Resolver_CacheControl  = &46003`
* `Resolver_DCI4Statistics = &46004`

The `X` forms are:

* `XResolver_GetHostByName = &66000`
* `XResolver_GetHost       = &66001`
* `XResolver_GetCache      = &66002`
* `XResolver_CacheControl  = &66003`
* `XResolver_DCI4Statistics = &66004`

## Which lookup SWI to use

Use `Resolver_GetHost` for new multitasking-aware code.
Use `Resolver_GetHostByName` only when a blocking compatibility interface is acceptable, such as ports of older Unix-style software.

## Returned data

Resolver returns a standard `hostent` structure.

Layout:

* Offset `0`: pointer to host name
* Offset `4`: pointer to zero-terminated list of alias pointers
* Offset `8`: address family, usually `AF_INET`
* Offset `12`: address length, usually `4`
* Offset `16`: pointer to zero-terminated list of address pointers

The address list normally contains IPv4 addresses.

## Resolver_GetHostByName

Purpose:

* Blocking name lookup.
* Mostly for compatibility with `gethostbyname()`-style callers.

On entry:

* `R1 = pointer to zero-terminated host name string`

On exit:

* If V clear:
  `R0 = errno-style status`
  `R1 = pointer to hostent if successful, else 0`
* If V set:
  `R0 = pointer to RISC OS error block`

Behaviour:

* Resolver internally keeps driving the asynchronous lookup machinery until a result or failure is available.
* This means the caller blocks until completion.

Use this when:

* Porting simple Unix software.
* You do not need foreground responsiveness during name resolution.

## Resolver_GetHost

Purpose:

* Non-blocking or polling-style lookup.
* Preferred for applications that must remain responsive.

Interface:

* Documented usage is by name lookup with `R1 = pointer to host name string`.
* In this implementation there is also reverse-lookup support:
  if `R0 = 0`, Resolver interprets `R1` as a pointer to an IPv4 address and performs a reverse lookup.

On exit:

* If successful:
  `R0 = 0`
  `R1 = pointer to hostent`
* If still in progress:
  `R0 = 36` (`EINPROGRESS`)
  `R1 = 0`
* If a cached or completed failure is returned without V set:
  `R0 = -1` for host not found
  `R0 = -2` for remote failure or resolver timeout
  `R1 = 0`
* If configuration or parameter handling fails:
  V is set and `R0` points to a RISC OS error block

Important points:

* Cached hits may return immediately.
* Requests found in local hosts sources may also return immediately.
* Remote DNS lookups usually return `EINPROGRESS` first.
* Callers must poll until the status changes from `EINPROGRESS`, or until V is set.

Typical polling pattern:

```text
repeat
    call Resolver_GetHost
    if V set:
        fail with RISC OS error
    if R0 == 36:
        keep UI alive and try again later
until R0 != 36

if R0 == 0 and R1 != 0:
    success
else:
    host not found or remote failure
```

BBC BASIC-style example:

```bbcbasic
REM EINPROGRESS = 36
REPEAT
  SYS "Resolver_GetHost", "host.example" TO status, hostent; flags
  error% = flags AND 1
  REM Update UI or continue other work here
UNTIL error% OR status <> 36
```

## Host name validation

Resolver validates the host name before starting a lookup.
Valid names are restricted to printable host-style characters, specifically alphanumeric characters plus:

* `-`
* `_`
* `.`

Invalid names fail immediately with a RISC OS error.

## Reverse lookups and numeric input

Resolver can perform reverse lookups.

In this implementation:

* Numeric dotted IPv4 strings such as `192.168.0.1` are internally converted to `in-addr.arpa` form.
* `Resolver_GetHost` also supports a reverse-lookup path where `R0 = 0` and `R1` points to an IPv4 address value.

If documenting Resolver for callers, make it clear whether you are describing:

* forward lookup by host name, or
* reverse lookup by IPv4 address

## Configuration variables

Resolver is configured through system variables.
These are normally set at startup but may be changed later.

Documented variables:

* `Inet$Resolvers`
  Space-separated dotted IPv4 addresses of DNS servers.
  Up to three are used.
* `Inet$Hostname`
  Local host name.
* `Inet$LocalDomain`
  Local domain name.
* `Inet$SearchDomains`
  Space-separated search domains for unqualified names.
* `Inet$ResolverRetries`
  Number of retry attempts for failed lookups.
* `Inet$ResolverDelay`
  Delay in seconds between retry attempts.
* `Inet$ResolverServer`
  Enables simple server behaviour when supported by the build.

Implementation details that matter in practice:

* `Inet$Resolvers` may also contain the token `auto`.
  This enables local nameserver auto-discovery instead of fixed DNS server addresses.
* Extra configuration variables may be supported:
  `Inet$ResolverFreewayHosts`, `Inet$ResolverNetBIOSHosts`, and `Inet$ResolverReorder`.
* If `Inet$SearchDomains` is not set, Resolver builds a search list from `Inet$LocalDomain` or from the domain part of `Inet$Hostname`.
* If no usable DNS servers are configured, local hosts-file lookups can still succeed, but remote DNS requests fail.

## Re-reading configuration

Configuration changes are not automatically applied just because a variable changed.
To force Resolver to re-read configuration, use one of:

* `*ResolverConfig`
* `Resolver_CacheControl` with reason `3`

Resolver also reacts to some service calls and variable-monitor events, especially around hosts database changes and network stack lifecycle.

## *ResolverConfig

`*ResolverConfig` re-reads Resolver configuration from the `Inet$...` variables.

Use it after changing variables such as:

* `Inet$Resolvers`
* `Inet$Hostname`
* `Inet$LocalDomain`
* `Inet$SearchDomains`
* `Inet$ResolverRetries`
* `Inet$ResolverDelay`

## Resolver_CacheControl

Use this SWI to control cache behaviour.

Entry:

* `R0 = reason code`

Reason codes:

* `0` flush failed lookups
* `1` flush all items
* `2` flush hosts-file items
* `3` re-read configuration
* `8` disable caching of failed lookups
* `9` enable caching of failed lookups

Exit:

* All registers preserved

Notes:

* Failed-lookup caching is disabled by default.
* Enabling failed-lookup caching is only sensible if failures are expected to be genuine and stable, rather than transient packet loss or DNS timeout.

## Cache behaviour

The cache stores:

* valid results
* failed results
* pending requests

Behaviour to account for:

* Cache hits return immediately.
* Pending entries cause `Resolver_GetHost` to return `EINPROGRESS`.
* Failed cached entries return `-1` or `-2` with `R1 = 0`.
* Failed cached entries may be removed immediately after being read if failed-lookup caching is disabled.

Important lifetimes from this implementation:

* Valid entries have a maximum lifetime of 24 hours.
* Failed entries last 90 seconds.
* Unused resolved entries can expire after 90 seconds.
* Expired entries are kept for a further 90 seconds after expiry so the returned `hostent` remains stable for callers.
* DNS server timeout is 15 seconds.
* Default retry count is 2.
* Default retry delay is 5 seconds.

When explaining behaviour, prefer the 90-second guaranteed post-lookup lifetime rather than assuming every result remains valid for 24 hours.

## Services

Resolver uses `Service_InternetVars` with service number `&80C41`.

Relevant reason codes:

* `0` database changed
* `1` hostname changed
* `2` local domain changed
* `3` resolvers changed
* `4` resolvers reordered

Practical meaning:

* `InetDBase$Path` changes notify Resolver that the hosts database may need refreshing.
* Hostname and domain changes can be broadcast to other consumers.
* Resolver itself may emit these notifications when monitored variables change.

Resolver also reacts to wider Internet stack and driver lifecycle services, including:

* interface-up/address-change conditions
* dynamic boot or DHCP-style configuration events
* link-active notifications for auto-resolver discovery

## Resolver_DCI4Statistics

Resolver exposes DCI4 statistics.
The statistics include:

* total SWI requests
* SWI cache hits
* SWI failures
* total cache entries
* active cache entries
* inactive cache entries
* pending cache entries
* expiring cache entries
* failed cache entries
* expired cache entries

Use this when monitoring Resolver behaviour or diagnosing cache efficiency.

## Error handling guidance

Distinguish carefully between:

* V set:
  a real RISC OS error block was returned
* V clear and `R0 = 36`:
  request still in progress
* V clear and `R0 = 0` with `R1 != 0`:
  success
* V clear and `R0 < 0` with `R1 = 0`:
  Resolver-level lookup failure

For user-facing software:

* treat `-1` as host not found
* treat `-2` as timeout or remote resolver failure
* present configuration errors separately from ordinary lookup failures

## Recommended advice to callers

When helping someone use Resolver:

* Recommend `Resolver_GetHost` for new applications.
* Tell them to poll on `EINPROGRESS` instead of blocking the desktop.
* Tell them to treat returned `hostent` data as read-only and short-lived.
* Tell them to run `*ResolverConfig` or `Resolver_CacheControl 3` after changing configuration variables.
* Tell them not to depend on internal cache structures or `Resolver_GetCache`.
* Call out the difference between documented interface behaviour and implementation-specific extras such as `auto` in `Inet$Resolvers` or reverse-lookup entry paths.

## What to include in answers

When using this skill, answers should usually cover:

* which SWI or command to use
* required registers on entry and exit
* how to handle `EINPROGRESS`
* the meaning of `-1`, `-2`, and V-set errors
* which `Inet$...` variables must be configured
* whether a configuration reload is required
* whether the caller is doing forward lookup or reverse lookup
