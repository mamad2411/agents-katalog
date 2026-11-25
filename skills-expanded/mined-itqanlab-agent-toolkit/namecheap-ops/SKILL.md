---
name: namecheap-ops
description: "Connect one or more Namecheap accounts once, then run the domains from the agent. Triggers: 'connect my Namecheap', 'list my domains', 'when do my domains expire', 'is this domain available', 'point this domain at Cloudflare', 'change the nameservers', 'add a DNS record on Namecheap', 'how much does a .com cost to renew', 'namecheap'. List them, see what expires and what will not renew by itself, check the balance, look up nameservers, check whether a name is free, see registration and renewal prices, change nameservers, and edit DNS records for domains that use Namecheap's own DNS — without opening the dashboard. Setup adopts a key the machine already has, and handles Namecheap's address whitelist, including sending requests through an SSH server with a fixed address when the machine's own address keeps changing. Several accounts are kept apart by name. Works on macOS, Windows and Linux."
license: MIT
compatibility: "Requires Node 18 or newer — run scripts/setup-deps.sh (or scripts/setup-deps.ps1 on Windows) to check for it and install it if missing. Needs network access to the Namecheap API. Namecheap must have API access switched on for the account and the calling address on its whitelist; a relay needs an ssh client and a server reachable without a password prompt. Covers domains, DNS and pricing only — not hosting, email or SSL products, and it does not register, renew or transfer domains."
metadata:
  author: itqanlab
  version: 2.1.2
  category: devops
  short: "Domains, nameservers and DNS on Namecheap"
  starter: "list my domains and when they expire"
---

# Namecheap

Three scripts. `scripts/setup.mjs` connects accounts, `scripts/nc.mjs` does the work, and `nc.mjs call` reaches any Namecheap command the others do not wrap.

## Who you are doing this for

Assume the person asking has never opened a terminal. **You run the commands; they never do.** They are asked to do only what cannot be done for them: switch API access on in the Namecheap dashboard, add an address to its whitelist, and paste the key into a file so it never passes through the conversation.

Everything else is yours. Report it in plain words. "example.com expires in 14 days and will not renew by itself" is the result they asked for; an XML attribute is not.

If they are clearly comfortable with a terminal, stop narrating and let them drive.

## Before anything else: check the dependencies

These scripts need Node 18 or newer:

```
sh scripts/setup-deps.sh --check
```

Non-zero exit means missing or too old. `sh scripts/setup-deps.sh` (Windows: `.\scripts\setup-deps.ps1`) prints the right install command for that machine and asks before running it.

## Namecheap has no tokens

Read this before setting anything up, because it is what makes Namecheap different from the other providers here.

A request carries a username, an API key, and **the address it comes from**. Namecheap refuses it unless that address is on a whitelist the account owner keeps by hand in the dashboard. **Nothing in the API edits that list**, so it cannot be done for the user, and it is the step most likely to go wrong.

Two ways to deal with it:

| | What Namecheap sees | Good for | Costs |
| :-- | :-- | :-- | :-- |
| **Direct** | This machine's own public address | A fixed connection | On home or mobile internet the address changes, and each change means editing the whitelist again |
| **Relay** | The address of an SSH server | A laptop that moves, or anyone with a server | Needs a server the machine can `ssh` into without a password prompt |

Prefer the relay when the person has a server. Requests are then made from there, the address never changes, and the whitelist is edited once.

Switching API access on has conditions Namecheap sets and can refuse; it is not something to work around. As far as I know the rule is roughly a balance, or enough spend, or enough domains, but I could not open Namecheap's help pages to confirm the exact numbers, so do not quote them as fact.

## Connect an account first

```
node scripts/setup.mjs status
```

If nothing is connected, **look before asking for anything**:

```
node scripts/setup.mjs import                       what this machine already has; changes nothing
node scripts/setup.mjs import --file <path>         a .env file that holds NAMECHEAP_API_USER and NAMECHEAP_API_KEY
node scripts/setup.mjs import --file <path> --yes   adopt it
```

`import` notices when the old setup was whitelisted for an address other than this machine's, and looks for an SSH server already configured for that address. If it finds one it proposes it as the relay. If it finds none, it says so rather than guessing.

If there is nothing to adopt, run the guided setup and follow what it prints:

```
node scripts/setup.mjs add <a-name-for-it>
node scripts/setup.mjs add <a-name-for-it> --relay "-i ~/.ssh/id_ed25519 user@203.0.113.5"
node scripts/setup.mjs verify <that-name>
```

`add` prints this machine's address (or the relay's) so the person knows exactly what to put on the whitelist. **Never ask for the key in the conversation.** They paste it into the file the script names. `verify` then checks it and says what Namecheap answered, and if the answer is a refused address it says which address and where to add it.

```
node scripts/setup.mjs relay <name> "-i ~/.ssh/key user@host"   send this account's requests through a server
node scripts/setup.mjs relay <name> none                        back to direct
node scripts/setup.mjs status            every account, and whether Namecheap accepts it from here
node scripts/setup.mjs use <name>        make one the default
node scripts/setup.mjs rename <old> <new>
node scripts/setup.mjs forget <name> --yes
```

### Why the name matters

Namecheap will not say which account a key belongs to. The name given at setup is the only label there is, so choose one the person will recognise. Every command that changes something prints it. Do not remove that.

Any command runs against another account with `--account <name>`. With several accounts and no default, commands refuse to run rather than guess.

## Commands

```
node scripts/nc.mjs whoami                       account, route Namecheap sees, domain count, balance
node scripts/nc.mjs balance
node scripts/nc.mjs domains [--expiring 90]      every domain: expiry, auto-renew, where its DNS lives
node scripts/nc.mjs domain <name>                one in full
node scripts/nc.mjs check <name> [<name> ...]    free or taken
node scripts/nc.mjs price <tld> [<tld> ...]      register and renew price per year
```

Nameservers, and DNS records for domains that use Namecheap's own DNS:

```
node scripts/nc.mjs nameservers <domain>
node scripts/nc.mjs nameservers-set <domain> <ns1> <ns2> [...] --yes
node scripts/nc.mjs nameservers-default <domain> --yes
node scripts/nc.mjs dns <domain>
node scripts/nc.mjs dns-add <hostname> <type> <value> [--ttl 1800] [--priority 10] [--append] --yes
node scripts/nc.mjs dns-remove <hostname> --type A [--value <v>] --yes
```

Any name under a registered domain works: `dns-add app.example.com A 203.0.113.9` finds `example.com` itself.

## Things that are easy to get wrong

**Most domains have no DNS at Namecheap.** Anyone who put a domain behind Cloudflare, or on a hosting plan, has their records there. Namecheap then holds none, and `dns`, `dns-add` and `dns-remove` fail with an explanation. That is the correct answer, not a fault. `domains` shows a `DNS here` / `DNS elsewhere` column so this is visible before anyone tries. To see where a domain's records really are, run `nameservers <domain>`.

**Changing DNS records replaces the whole list.** Namecheap has no "add a record" call. Its one write command takes the complete list and deletes whatever is not in it. `dns-add` and `dns-remove` therefore read the current list, change it in memory, show every line that will be added or removed, and only then send everything back, then read it again to confirm the count. Without `--yes` they stop after showing the plan. `call` refuses that command outright, because sent by hand it deletes every record it is not given.

**`nameservers-set` can take a site and its email offline.** Once the nameservers change, the domain answers only from the new ones. If they do not already hold the records, nothing resolves until they do. Add the records at the new place first. The change is instant at Namecheap and can take up to a day to spread.

**`nameservers-default` abandons any records kept elsewhere.** It hands DNS back to Namecheap. Records at the previous nameservers stop being used.

**Auto-renew off means the domain lapses.** `domains` lists anything expiring within 60 days with auto-renew off. Namecheap does not warn about this by API. The balance matters too: a domain set to auto-renew with too little balance also lapses. As far as I know the API cannot switch auto-renew on or off, so that is done in the dashboard.

**Premium names cost far more.** `check` marks them. A premium name can cost hundreds of times a normal one.

**Prices per year are for one year.** `price` shows registration and renewal separately because they often differ a lot, and renewal is the one that repeats.

## Before changing anything

**Show the current state first.** Run `domain <name>` or `dns <domain>` and show the person what is there. Say which account it is in.

**Changes require confirmation.** `nameservers-set`, `nameservers-default`, `dns-add` and `dns-remove` print what they matched and refuse to act without `--yes`. Show that to the person and get an explicit yes before re-running with the flag. Never pass `--yes` on the first attempt.

## Anything not wrapped above

```
node scripts/nc.mjs call namecheap.domains.getContacts DomainName=example.com
node scripts/nc.mjs call namecheap.users.getPricing ProductType=DOMAIN ProductCategory=DOMAINS ActionName=RENEW ProductName=COM
```

`call` takes a Namecheap command name and `Key=value` pairs, adds the credentials and address itself, and prints the XML answer. Commands that change something or spend money (`set`, `create`, `renew`, `transfer`, `delete`, `update`, `register`, `push`) are held back until `--yes`. Namecheap publishes the command list on its own API documentation pages, which could not be opened while this was written, so check a command's parameters there before using one this skill does not wrap. Do not guess parameters for something that spends money.

`references/playbooks.md` has the multi-step jobs.

## What this cannot do

It does not register, renew or transfer domains. Those spend money, and a mistake in one is not something to find out by trying. `call` can reach them behind `--yes`, with the care above.

It covers domains, DNS and pricing. Namecheap hosting, Private Email, SSL certificates and cPanel are separate products with their own credentials.

It cannot edit the IP whitelist. Namecheap offers no way to do that except by hand in the dashboard.

## What has been checked, and what has not

Checked against a live account, through a relay: connecting, listing, `domain`, `nameservers`, `check`, `price`, `balance`, the address-refused and wrong-key errors, and every refusal that stops a change without `--yes`.

Checked offline only: the record-merging logic behind `dns-add` and `dns-remove`, and the request it builds for `setHosts`. **It has not been run against a real domain**, because the account it was built on keeps all its DNS elsewhere. The parts that rest on memory of Namecheap's format, not on a live answer, are the record element and attribute names in `getHosts`, and how the email setting is carried through `setHosts`. The read-back after each write is there to catch a mistake in either, and the first real use should be on a domain that can afford it.

Not run at all: `nameservers-set` and `nameservers-default` writes.

## Failure messages

Errors are rewritten for people who do not know Namecheap's numbers. Only codes seen from the live API get their own wording; the rest keep Namecheap's text and its number. Keep that habit for anything added here: say what happened, then what to do next, and do not present a guess as an explanation.

## Updates

This skill is versioned. Its version is `metadata.version` in the header of this file. `CHANGELOG.md` in this folder lists what changed in each version, newest first.

To check for a newer version, open the address on the `Latest:` line of `CHANGELOG.md` and compare its top version with the installed one. If the newer one is ahead, read every entry between the two and tell the user what changed before anything is updated. A `Breaking` section means the user has to do something. To update, reinstall the skill from its source repository, the same way it was installed.
