---
name: domain-health-check
description: Check a list of domains for email blacklist listings (Spamhaus DBL, URIBL, SURBL + IP-based ZEN/SpamCop/Barracuda) and missing email-auth DNS records (SPF, DKIM, DMARC). Use when the user pastes a list of domains — bare, one-per-line, comma-separated, or a CSV column — with no other instruction, or asks to check domains for blacklisting, blocklists, missing records, SPF/DKIM/DMARC, or email deliverability health. Pure public DNS, no API keys, no cost.
---

# Domain Health Check

Checks every domain against 3 domain-reputation blacklists and 3 IP-reputation blacklists, plus SPF, DKIM (12 common selectors), and DMARC — using only public DNS. Requires Node 18+ on PATH (if `node -v` fails, tell the user Node 18+ is required and stop).

## Workflow

1. **Extract domains** from whatever the user provided: bare list, comma/space separated, CSV column, URLs, or messy text. Take anything that looks like a domain. Don't ask for confirmation — just run. (The script itself also lowercases, strips `https://`/`www.`/paths, dedupes, and skips invalid tokens.)
2. **Get the script**: if a `check.mjs` file exists in the same directory as this SKILL.md, use it directly. Otherwise write the script below verbatim to a temp/scratchpad file named `check.mjs`. Do not modify it.
3. **Run it once** for the whole batch: `node check.mjs domain1.com domain2.com ...` — it prints JSON. For very large lists (300+), split into runs of ~250 and merge results. Expect roughly 10–30 s per 50 domains.
4. **Render the two tables** (format below) from the JSON. Never show raw JSON.

## Output format

Start with a one-line summary, worst news first, e.g.:
> **2 listed · 3 missing SPF · 1 no DKIM · 14 fully clean** — all 6 blocklists reachable ✓

If any zone in `zoneStatus` is not `"ok"`, say instead: "⚠ <zone> unreachable from this network — its column is inconclusive, not clean." If `skipped` is non-empty, add one line listing the skipped tokens.

**Table 1 — Domain blacklists + email auth** (one row per domain, rows with any failure sorted to the top):

| Domain | Spamhaus DBL | URIBL | SURBL | SPF | DKIM | DMARC |
|---|---|---|---|---|---|---|

- Blacklist cells: `✅ clean`, `🚫 LISTED (reason)` (bold the row's domain), `⚠️ inconclusive`
- SPF: `✅ ok`, `❌ missing`, or `🚫 INVALID (multiple SPF records)` (two+ SPF records is an RFC violation — receivers treat it as permerror)
- DKIM: `✅ ok (selectors)` showing which selector(s) matched, or `❌ none found`
- DMARC: `✅ ok (p=policy)` or `❌ missing`

**Table 2 — IP-based blacklists** (checks the IPs behind each domain's MX records, falling back to A records):

| Domain | IPs checked (MX/A) | Spamhaus ZEN | SpamCop | Barracuda |
|---|---|---|---|---|

Use `—` when the domain has no MX/A records (`"no IPs"`).

## After the tables — fix guidance

For each *type* of failure present (once per type, not per domain), add a short remediation note:

- **Spamhaus DBL / ZEN listed** → look up & request removal at https://check.spamhaus.org/
- **URIBL listed** → check reason & removal at https://uribl.com/lookup.shtml (black = active spam sighting; grey = often just a young/parked domain)
- **SURBL listed** → https://surbl.org/surbl-lookup — fix the underlying cause first; delisting requests on unfixed domains are denied
- **SpamCop listed** → auto-expires ~24h after spam reports stop; details at https://www.spamcop.net/bl.shtml
- **Barracuda listed** → removal request at https://www.barracudacentral.org/rbl/removal-request
- **SPF missing** → add a TXT record on the root, e.g. Google Workspace: `v=spf1 include:_spf.google.com ~all`, Microsoft 365: `v=spf1 include:spf.protection.outlook.com ~all` (one record only — never add a second)
- **DKIM none found** → enable signing in the email provider's admin console (Google Admin → Apps → Gmail → Authenticate email; M365 → Defender → Email authentication) and publish the selector record it gives you
- **DMARC missing** → add TXT at `_dmarc.<domain>`, safe starter: `v=DMARC1; p=none; rua=mailto:you@yourdomain.com`, tighten to `p=quarantine`/`p=reject` once SPF+DKIM pass

## Caveats to keep in mind (mention only when relevant)

- **DKIM `none found` ≠ proof of no DKIM** — only 12 common selectors are swept; a custom selector may exist. If the user knows their selector, check `<selector>._domainkey.<domain>` TXT directly.
- **IP-list hits on shared hosting** (Cloudflare/parked IPs) are usually the host's problem, not the sender's — sending through Google/M365 uses Google/Microsoft IPs, not these. Say so if a hit looks like that.
- **`inconclusive`** means the blocklist refused/failed to answer this network, never "clean". Re-run on another network if it persists.
- Checking is passive: DNS lookups can never *cause* a listing, so it's safe to re-run as often as wanted.

## The script — write verbatim to `check.mjs`

```js
#!/usr/bin/env node
// domain-health-check — blacklists + SPF/DKIM/DMARC. Pure DNS, zero dependencies, Node 18+.
// Queries each DNSBL at its AUTHORITATIVE nameservers (bypasses public-resolver blocking:
// Google/Cloudflare DNS users would otherwise get false-clean from Spamhaus and false-listed
// from URIBL). Every zone is validated with a control query against a known-listed test point;
// zones whose control fails report "inconclusive" instead of lying.
// Usage: node check.mjs domain1.com domain2.com ...   (prints JSON)
import { Resolver } from 'node:dns/promises';

const TIMEOUT = 4000;
const sys = new Resolver({ timeout: TIMEOUT, tries: 1 });

const withTimeout = (p) => Promise.race([
  p, new Promise((_, rej) => setTimeout(() => rej(Object.assign(new Error('timeout'), { code: 'ETIMEOUT' })), TIMEOUT + 500)),
]);

// ---------- zone definitions ----------
const DOMAIN_ZONES = [
  { zone: 'dbl.spamhaus.org', label: 'Spamhaus DBL', control: 'dbltest.com', controlExpect: '127.0.1.',
    classify: (ip) => {
      if (ip.startsWith('127.255.255.')) return 'refused';
      const x = Number(ip.split('.')[3]);
      const kind = x === 2 ? 'spam' : x === 4 ? 'phishing' : x === 5 ? 'malware' : x === 6 ? 'botnet-C2'
        : x >= 102 && x <= 106 ? 'abused-legit' : 'listed';
      return `listed (${kind})`;
    } },
  { zone: 'multi.uribl.com', label: 'URIBL', control: 'test.uribl.com', controlExpect: '127.0.0.',
    classify: (ip) => {
      if (ip === '127.0.0.1' || ip === '127.0.0.255') return 'refused';
      const bits = Number(ip.split('.')[3]);
      const parts = [];
      if (bits & 2) parts.push('black');
      if (bits & 4) parts.push('grey');
      if (bits & 8) parts.push('red');
      return 'listed' + (parts.length ? ` (${parts.join(',')})` : '');
    } },
  { zone: 'multi.surbl.org', label: 'SURBL', control: 'test.multi.surbl.org', controlExpect: '127.0.0.', controlIsAbsolute: true,
    classify: (ip) => {
      const bits = Number(ip.split('.')[3]);
      const parts = [];
      if (bits & 8) parts.push('phishing');
      if (bits & 16) parts.push('malware');
      if (bits & 64) parts.push('abuse');
      if (bits & 128) parts.push('cracked');
      return 'listed' + (parts.length ? ` (${parts.join(',')})` : '');
    } },
];

const IP_ZONES = [
  { zone: 'zen.spamhaus.org', label: 'Spamhaus ZEN', control: '2.0.0.127', controlExpect: '127.0.0.',
    classify: (ip) => {
      if (ip.startsWith('127.255.255.')) return 'refused';
      const x = Number(ip.split('.')[3]);
      return x >= 10 ? 'listed (PBL/dynamic-IP)' : x >= 4 ? 'listed (XBL/botnet)' : 'listed (SBL/spam-source)';
    } },
  { zone: 'bl.spamcop.net', label: 'SpamCop', control: '2.0.0.127', controlExpect: '127.0.0.2', classify: () => 'listed' },
  { zone: 'b.barracudacentral.org', label: 'Barracuda', control: '2.0.0.127', controlExpect: '127.0.0.2', classify: () => 'listed' },
];

const DKIM_SELECTORS = ['google', 'selector1', 'selector2', 'default', 'k1', 'k2', 's1', 's2', 'mail', 'dkim', 'zoho', 'fm1'];

// ---------- one direct-to-authoritative resolver per zone, validated by control query ----------
async function initZones(zones) {
  await Promise.all(zones.map(async (z) => {
    try {
      const ns = await withTimeout(sys.resolveNs(z.zone));
      const ips = [];
      for (const h of ns.slice(0, 3)) {
        try { ips.push(...await withTimeout(sys.resolve4(h))); } catch {}
        if (ips.length >= 2) break;
      }
      if (ips.length) {
        z.resolver = new Resolver({ timeout: TIMEOUT, tries: 1 });
        z.resolver.setServers(ips.slice(0, 2));
      } else z.resolver = sys;
    } catch { z.resolver = sys; }
    const name = z.controlIsAbsolute ? z.control : `${z.control}.${z.zone}`;
    try {
      const a = await withTimeout(z.resolver.resolve4(name));
      z.usable = a.some((ip) => ip.startsWith(z.controlExpect));
    } catch { z.usable = false; }
  }));
}

async function dnsblQuery(z, name) {
  if (!z.usable) return 'inconclusive';
  try {
    const ips = await withTimeout(z.resolver.resolve4(name));
    if (!ips || !ips.length) return 'clean';
    const hit = ips.map(z.classify).find((v) => v.startsWith('listed'));
    return hit || 'inconclusive';
  } catch (e) {
    if (e && (e.code === 'ENOTFOUND' || e.code === 'ENODATA')) return 'clean';
    return 'inconclusive';
  }
}

async function txt(name) {
  try { return (await withTimeout(sys.resolveTxt(name))).map((c) => c.join('')); }
  catch { return []; }
}

async function checkDomain(domain) {
  const out = { domain, blacklists: {} };

  await Promise.all(DOMAIN_ZONES.map(async (z) => {
    out.blacklists[z.label] = await dnsblQuery(z, `${domain}.${z.zone}`);
  }));

  const rootTxt = await txt(domain);
  const spf = rootTxt.filter((t) => t.toLowerCase().startsWith('v=spf1'));
  out.spf = spf.length === 0 ? 'missing' : spf.length > 1 ? 'INVALID (multiple SPF records)' : 'ok';

  const dmarcTxt = await txt(`_dmarc.${domain}`);
  const dmarc = dmarcTxt.find((t) => t.toLowerCase().startsWith('v=dmarc1'));
  if (!dmarc) out.dmarc = 'missing';
  else { const p = /p=([a-z]+)/i.exec(dmarc); out.dmarc = `ok (p=${p ? p[1] : '?'})`; }

  const sel = await Promise.all(DKIM_SELECTORS.map(async (s) => {
    const recs = await txt(`${s}._domainkey.${domain}`);
    return recs.some((t) => t.includes('v=DKIM1') || t.includes('k=rsa')) ? s : null;
  }));
  const found = sel.filter(Boolean);
  out.dkim = found.length ? `ok (${found.join(',')})` : 'none found';

  // IP-based lists against the domain's MX (preferred) or A records
  let ips = []; out.mx = null;
  try {
    const mx = await withTimeout(sys.resolveMx(domain));
    const hosts = mx.sort((a, b) => a.priority - b.priority).slice(0, 2).map((m) => m.exchange);
    for (const h of hosts) { try { ips.push(...await withTimeout(sys.resolve4(h))); } catch {} }
    out.mx = hosts.join(', ') || null;
  } catch {}
  if (!ips.length) { try { ips = await withTimeout(sys.resolve4(domain)); out.mx = out.mx || '(A record)'; } catch {} }
  ips = [...new Set(ips)].slice(0, 2);
  out.ips = ips;
  out.ipLists = {};
  await Promise.all(IP_ZONES.map(async (z) => {
    if (!ips.length) { out.ipLists[z.label] = 'no IPs'; return; }
    const verdicts = await Promise.all(ips.map((ip) => dnsblQuery(z, `${ip.split('.').reverse().join('.')}.${z.zone}`)));
    const hit = verdicts.find((v) => v.startsWith('listed'));
    out.ipLists[z.label] = hit || (verdicts.includes('inconclusive') ? 'inconclusive' : 'clean');
  }));

  return out;
}

// ---------- input normalization ----------
const raw = process.argv.slice(2).filter((a) => !a.startsWith('--'));
const seen = new Set(); const domains = []; const skipped = [];
for (let d of raw) {
  d = d.trim().toLowerCase().replace(/^https?:\/\//, '').replace(/^www\./, '').replace(/[/,;].*$/, '');
  if (!d) continue;
  if (!/^[a-z0-9.-]+\.[a-z]{2,}$/i.test(d)) { skipped.push(d); continue; }
  if (!seen.has(d)) { seen.add(d); domains.push(d); }
}
if (!domains.length) { console.error('usage: node check.mjs domain1.com domain2.com ...'); process.exit(1); }

await initZones([...DOMAIN_ZONES, ...IP_ZONES]);
const zoneStatus = Object.fromEntries([...DOMAIN_ZONES, ...IP_ZONES].map((z) => [z.label, z.usable ? 'ok' : 'unreachable — column inconclusive']));

const CONC = 8;
const results = [];
for (let i = 0; i < domains.length; i += CONC) {
  results.push(...await Promise.all(domains.slice(i, i + CONC).map(checkDomain)));
}
console.log(JSON.stringify({ zoneStatus, skipped, results }, null, 2));
```
