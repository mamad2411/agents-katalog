---
name: riscos-network-dcistatistics
description: Describe and work with the general DCI4 statistics interface on RISC OS, including how suppliers enumerate themselves, how gatherers describe and read statistics, the provider and description structures, and common implementation patterns. Use when implementing, reviewing, documenting, or querying DCI4 statistics suppliers.
metadata:
  author: gerph@gerph.org
license: MIT
---
# RISC OS DCI4 statistics

Use this skill when the task is about the generic DCI4 statistics interface,
not just one module's private counters.

This includes:

* Implementing a statistics supplier in a module or driver.
* Writing or reviewing a statistics gatherer.
* Understanding `Service_StatisticEnumerate`.
* Working with the supplier SWI used for `SA_DESCRIBE` and `SA_READ`.
* Documenting or debugging `dci4_spctl` and `dci4_stdesc` structures.
* Checking atomicity, volatility, or dynamic-supplier behaviour.

## Core model

The interface has two roles:

* supplier: software that owns and exports statistics
* gatherer: software that enumerates suppliers and presents or consumes them

The protocol has two phases:

1. enumerate suppliers through `Service_StatisticEnumerate`
2. use each supplier's SWI to describe statistics with `SA_DESCRIBE` and read
   values with `SA_READ`

The interface is polled, not event driven, and is not re-entrant.

## Primary source

The authoritative public specification is:

* https://gerph.github.io/riscos-prm-dci4/prm/html/networking/dci4/dcistatistics.html

This skill captures the operational details you usually need so it can be
used on its own, but prefer the public specification if you need to verify an
edge case.

## Working rules

When using this skill:

* distinguish clearly between supplier-side and gatherer-side behaviour
* separate the enumeration phase from the per-supplier SWI phase
* be explicit about buffer sizing, alignment, and partial-range returns
* call out which fields must be static, zero, or RMA-allocated
* mention the non-re-entrant and polled nature of the interface
* do not assume any particular local gatherer or supplier implementation

## Supplier enumeration

Suppliers are discovered with `Service_StatisticEnumerate` (`&A1`).

The gatherer issues the service call and receives a linked list of
`dci4_spctl` structures in `R0`. Each supplier allocates its own structure in
the RMA, fills it in, links it to the list, and returns the updated head
pointer. The gatherer is responsible for freeing those returned structures
after use.

Important `dci4_spctl` fields:

* `next`: linked-list pointer
* `i_version`: statistics interface version implemented by the supplier
* `features`: feature bits; if no defined feature contract is in use, this
  should be zero
* `swinumber`: supplier SWI used for later `SA_DESCRIBE` and `SA_READ` calls
* `max_stat`: highest statistic number, inclusive
* `type`: classification such as general supplier, network protocol, network
  driver, or mbuf manager
* `s_version`: supplier's own version number
* `module`: supplier module title
* `title`: short user-facing title
* `description`: longer user-facing description
* `reset[8]`: unique per supplier initialisation so a gatherer can detect that
  the supplier has restarted

Do not cache supplier SWI numbers across separate enumerations. The interface
allows dynamic SWI assignment, especially when one module exposes multiple
effective suppliers.

## Supplier SWI contract

After enumeration, all communication uses the supplier SWI from `dci4_spctl`:

* `R0 = SA_DESCRIBE (0)` or `SA_READ (1)`
* `R1 = first statistic number`, inclusive
* `R2 = last statistic number`, inclusive
* `R3 = output buffer pointer`
* `R4 = output buffer size in bytes`
* `R5 = number of statistics processed` on exit
* `R6 = number of bytes written` on exit

The buffer must be word aligned.

If the buffer is too small for the whole requested range, the supplier may
return only a prefix of the range. `R5` and `R6` tell the gatherer how much
was actually processed.

## Descriptions before values

A gatherer should normally describe statistics before reading them.

`SA_DESCRIBE` returns one fixed-size `dci4_stdesc` for each statistic:

* `type`: `ST_...`
* `format`: `SxF_...`
* `presentation`: `SxP_...`
* `size`: bytes reserved for the value on `SA_READ`; always a multiple of 4
* `volatility`: `SV_STATIC`, `SV_VARIABLE`, or `SV_VOLATILE`
* `name`: static string pointer
* `name_tag`: currently reserved; should normally be zero
* `spare`: reserved; should be zero

`ST_UNUSED` is special:

* it reserves a statistic number
* it occupies zero bytes when read
* only the type and size fields are meaningful
* gatherers should skip it when presenting results

## Types, formats, and presentation

The main value types are:

* `ST_BOOLEAN`
* `ST_STRING`
* `ST_INTEGER8`
* `ST_INTEGER16`
* `ST_INTEGER32`
* `ST_INTEGER64`
* `ST_ADDRESS`
* `ST_TIME`

Key format and presentation families:

* booleans: normal or inverted values, with presentations such as on/off,
  yes/no, true/false
* strings: zero-terminated string values
* integers: signed or unsigned, optional big-endian layout, with
  hexadecimal/decimal/dotted presentation
* addresses: address-family-specific formats such as Ethernet, IP, or Econet
* times: absolute or relative values in one of the supported time encodings

When reviewing a supplier, check that the declared `size`, `type`, `format`,
and `presentation` match what `SA_READ` really writes.

## Atomicity and volatility

A supplier must perform each requested read atomically for the requested
range, so the gatherer sees a consistent set of related values from that call.

Avoid long interrupt-disabled regions. A common design is:

* keep accumulated totals in one buffer
* keep live deltas in another buffer
* atomically swap the live and merge pointers
* merge outside the critical section
* clear the reused delta buffer afterwards

Volatility is part of the contract:

* `SV_STATIC`: constant for the supplier invocation
* `SV_VARIABLE`: unlikely to change within about five minutes
* `SV_VOLATILE`: may change rapidly

Suppliers should group statistics of similar volatility together where
possible.

## Typical gatherer workflow

For a gatherer, the normal sequence is:

1. issue `Service_StatisticEnumerate`
2. walk the returned `dci4_spctl` list
3. for each supplier, call the SWI with `SA_DESCRIBE`
4. size read buffers from the returned `dci4_stdesc` values
5. call the SWI again with `SA_READ`
6. interpret the values using the previously returned descriptions
7. free the enumeration structures from the RMA

If a supplier only partially satisfies a request because the buffer is too
small, continue from the next unread statistic number.

## Common review points

When reviewing a DCI4 statistics implementation, check for these issues:

* enumeration block not allocated from the RMA
* `features` set without a defined feature contract
* `module`, `title`, `description`, or `name` pointing at transient storage
* `reset` not changing across supplier reinitialisation
* `size` not a multiple of 4
* `SA_READ` writing a different layout from what `SA_DESCRIBE` promises
* `name_tag` or `spare` not zero when no extension defines them
* `ST_UNUSED` treated like an ordinary readable statistic
* gatherer caching SWI numbers across separate enumeration passes
* read path not atomic for logically related counters

## Minimal supplier pattern

A supplier normally does two things:

1. On `Service_StatisticEnumerate`, allocate and link a `dci4_spctl` in the
   RMA.
2. In its supplier SWI, implement `SA_DESCRIBE` and `SA_READ` over a numbered
   statistic range.

The supplier SWI usually follows this pattern:

* validate `R0`
* initialise `R5` and `R6` to 0
* iterate from `R1` to `R2`
* for `SA_DESCRIBE`, write one `dci4_stdesc` per statistic
* for `SA_READ`, write the value layout promised by the matching description
* stop early if the caller's buffer in `R3`/`R4` is exhausted
* leave `R0` to `R4` unchanged and report progress in `R5` and `R6`

## Output expectations

Answers should usually cover:

1. how suppliers are discovered
2. how descriptions and values are fetched
3. what the structures and constants mean
4. what atomicity and volatility require in practice
5. any generic implementation or review guidance that helps the current task
