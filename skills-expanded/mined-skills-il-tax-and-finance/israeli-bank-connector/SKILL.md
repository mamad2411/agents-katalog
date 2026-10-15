---
name: israeli-bank-connector
description: Analyze Israeli bank transactions, spending patterns, and financial data across Israeli banks and credit card companies. Use when user asks about bank transactions, spending analysis, "cheshbon bank", budget tracking, or needs to categorize Israeli banking data. Pairs with israeli-bank-mcp and il-bank-mcp servers (which wrap the israeli-bank-scrapers library) to add financial-analysis workflows. Supports Hapoalim, Leumi, Discount, Mercantile, Mizrahi-Tefahot, First International (FIBI), Otsar HaHayal, Pagi, Union, Yahav, Massad, OneZero, Behatsdaa, Beyahad Bishvilha, Visa Cal, Max, Isracard, and Amex. Do NOT use for payment initiation, money transfers, or investment advice.
license: MIT
compatibility: Requires israeli-bank-mcp or il-bank-mcp MCP server. Claude Code recommended.
---

# Israeli Bank Connector

## Instructions

### Step 1: Identify Connected Banks
Check which MCP server is available and what accounts are connected:
- israeli-bank-mcp: direct scraper integration
- il-bank-mcp: Docker-based with persistent analysis
- If no MCP: guide the user through a CSV or Excel export from the bank website

**Neither MCP is installable with `npx`.** `israeli-bank-mcp` is not published to npm and
declares no `bin`, so any instruction to run `npx israeli-bank-mcp` is wrong and will fail.
The real shapes, taken from each repository:

| Server | How it is actually installed and run |
|---|---|
| `israeli-bank-mcp` | Clone the repo, `npm install`, `npm run build`, then point the MCP client at `node /path/to/israeli-bank-mcp/build/server.js` |
| `il-bank-mcp` | Docker. `docker compose up -d` with the bank env vars set, and the client runs `docker compose -f /path/to/il-bank-mcp/docker-compose.yml run --rm -i mcp-server` |

**Run Node 22.22.2 or newer for `israeli-bank-mcp`, and Python 3.9 or newer for the bundled
script** (its date filter needs time-zone data; on Windows that means `pip install tzdata`). `israeli-bank-scrapers` declares `engines.node >= 22.22.2`, so Node 22.0 to 22.22.1
is below the floor too. On an older Node the user is outside what the library supports, so
check `node --version` first when a user reports that nothing works at all. `il-bank-mcp`
builds its own Node into its Docker image, so the host's Node does not matter there.

**`israeli-bank-mcp` exposes two tools and one resource, and that is the whole surface**:
`fetch-transactions`, `two-factor-auth`, and the `banks://list` resource that reports which
credential fields each bank needs. Everything in Steps 3 to 5 below is work the agent does
on the returned data. Do not expect the server to categorize, total, or export anything.

### Step 2: Retrieve Transactions
Fetch transaction data for the requested period:
- Pass a start date explicitly. `fetch-transactions` defaults `startDate` to today when it is
  omitted, which returns almost nothing. For "last month", start on the first of that month
  and filter the result to the month (the script's `--from` / `--to`), because the scrape
  runs up to today and card scrapers also return the next billing cycle
- Leave `combineInstallments` off (the server's default). With it on, the library keeps only
  the first instalment of each purchase, so a multi-month view undercounts
- History: the library's README caps most scrapers at one year back (Discount and
  Mercantile at one year minus a day, Yahav at six months). An older start date is not an
  error; Hapoalim, for one, silently raises it to the cap. Report what came back.
- Include: Bank accounts AND credit card transactions

**Read the fields the library actually returns.** `fetch-transactions` hands back the
library's scrape result: an object with `accounts`, each holding `txns`. A transaction has
no `amount` field. It has `chargedAmount` (what is billed this period) and `originalAmount`
(the purchase price, in `originalCurrency`). For a credit-card instalment purchase
(`type: "installments"`, תשלומים) a completed line's `chargedAmount` is the single
instalment, so use it for a monthly view and never sum `originalAmount`. The `installments`
object (`number`, `total`) gives the remaining commitment: about `chargedAmount` times
(`total` minus `number`), worth telling a user who asks what they still owe on a purchase.
Each line also carries `status` (`completed` or `pending`) and two dates, `date` and
`processedDate` (when it is billed). `date` is usually the purchase date, but for instalment
N of a purchase the library moves it forward to that instalment's month. Pick one field for
month attribution and say which, because a card purchase late in one month is usually billed
in the next.

**Pending lines are the unreliable ones.** A pending Visa Cal instalment purchase arrives at
the FULL purchase price, a pending Max line can arrive with a charged amount of 0, and a
pending Visa Cal refund can arrive with a negative charged amount while its original amount
is positive. The script handles all three (full-price lines and unknown amounts are listed,
not summed; a refund follows the original's sign), but anything you compute by hand must do
the same, and a closed month or an accountant export should leave pending lines out.

**A bank CSV or Excel export needs normalising before the script reads it.** The script takes
JSON, so convert the file first. Typical Israeli exports are not UTF-8 (the legacy Hebrew
Windows code page is common), use day/month/year dates, put debits and credits in separate
חובה / זכות columns instead of one signed amount, carry a running balance (יתרה) column that
is not a transaction, and have header and footer rows to drop. Merge the two columns into one
signed `amount` (debit negative, credit positive); a blank cell is not zero, and the script
stops on one. On a credit-card statement use the charged amount (סכום חיוב), not the deal
amount (סכום עסקה): the deal amount is the full price of an instalment purchase. Some card
exports show charges as positive numbers; the script warns when every line is positive.

### Step 3: Categorize and Analyze
Apply Israeli-specific categorization:
| Category | Hebrew | Examples |
|----------|--------|---------|
| Housing | דיור (diur) | Rent, arnona, vaad bayit |
| Groceries | מזון (mazon) | Shufersal, Rami Levy, Victory |
| Transportation | תחבורה (tahaburah) | Rav-Kav, fuel, Gett |
| Utilities | שירותים (shartuim) | Electric Company, Mekorot, Bezeq |
| Healthcare | בריאות (briut) | Kupat Cholim, pharmacy |
| Education | חינוך (chinuch) | Gan, school, courses |
| Entertainment | בילוי (bilui) | Restaurants, cinema, streaming |
| Insurance | ביטוח (bituach) | Health, car, home insurance |
| Savings | חיסכון (chisachon) | Pension, keren hishtalmut |

**Do not report money moved into savings as spending.** A pension contribution, keren
hishtalmut deposit, gemel transfer, bank deposit (פיקדון) or securities purchase is the
user's own money changing pocket, not an expense. The savings rule matches those words and
the pension products and fund managers that appear on a direct debit with no "pension" word
(מקפת, אלטשולר, ילין לפידות, מנורה מבטחים, מיטב דש). Because מיטב, מבטחים and פיקדון are
also ordinary words in shop names and bottle deposits, those three count as savings only
when they are the whole description or come with a fund or deposit word (מיטב גמל, הפקדה
לפיקדון, פיקדון שקלי). A fund name the rule misses lands in Other, so ask about large
monthly debits there. The script reports Total Spending (excluding
savings), Into Savings, and Total Outflow (the two combined). Quoting the outflow figure as
"you spent X" overstates spending by whatever the user is putting away, which on an Israeli
payslip with pension deductions is not a small amount.

**Own transfers and taxes are separated too.** A line naming another account in the same
scrape (its full number, or its last six digits as a separate number), or a foreign-currency
purchase (המרת / רכישת מט"ח) into the user's own forex account, is reported as Own Transfers,
both legs, in no other figure. That only works when both accounts were scraped and the bank
prints the number, so ask the user about any large transfer (העברה) left in Other before
calling it spending. Income tax, VAT (מע"מ), tax advance payments (מקדמות מס) and Bituach
Leumi go to a Taxes and BL category (a plain מקדמה, a down payment to a supplier, does not): they stay in Total Spending
because the money did leave, but they are remittances, not consumption, and never a business
expense. A transfer to another person (Bit, PayBox, a bank transfer to someone else) is not
detected and lands in Other.

**Do not count a card purchase twice.** The bank account shows the monthly credit-card bill
as one line (ישראכרט, מקס איט, כאל, לאומי קארד and so on), and the card company's own data
lists the same purchases one by one. The script puts that bank-side line in a separate
`Card Bills` figure, outside both Total Spending and Total Outflow. If the user connected only
the bank and not the card company, that line is the only record of their card spending: add
it to spending yourself and say that it is one undivided figure. Banks word this line
differently, so ask the user to confirm which line is the card bill when an "Other" line is a
large round monthly debit. A bare "Max" is matched only when it is the whole description,
because Max Brenner and Max Stock are shops.

**Categorisation is keyword matching, so review it before presenting it as fact.** The
script matches merchant descriptions against Hebrew and English keyword patterns, guarded on
both scripts so a pattern matches a whole token rather than a fragment: Hebrew-letter
lookbehind so `פז` does not fire inside `פזגז`, and Latin-letter guards on both sides so
`hot` does not fire inside `Hotel` or `PHOTO`. Hebrew one-letter prefixes are handled by
matching a de-prefixed copy of each token as well, which is why `הפקדה לפנסיה` reaches the
savings rule; without that the guard blocks the most natural Hebrew phrasing and files a
pension deposit as an insurance expense.

**Misclassifications remain, and this is a CLASS of failure, not a fixed list.** Any Hebrew
merchant string that contains a pattern token as a real word will match it: a mall called
קניון מגדל שלום matches the insurer מגדל, and מלון הוט matches the cable company הוט. Those
two are named because they are common, not because they are the only ones. Show the user the
category breakdown and invite corrections rather than asserting it is their spending, and
never present a category total as a fact about the person without them having seen the rows
behind it.

**Money coming in is not netted off spending, and no net view is offered.** Any positive
amount, whether a refund, a reversal, a salary, a transfer in or a loan drawdown, is reported
on its own `Credits In` line and excluded from every category total and every percentage.
Nothing in the data distinguishes a refund from a salary, so a "net" figure built from that
bucket subtracts the user's salary from a spending category and reports a negative total. If
the user wants refunds netted, net the specific rows they point at, by hand. Check the sign
convention of your source first: a feed that reports every line as positive produces an empty
spending total.

### Step 4: Present Insights
The script produces the category split and the top merchants. Everything else in this list
is the agent's own work over the transactions, so check the rows before asserting a pattern.
For recurring charges, look for the same payee at a similar amount about a month apart, and
say whether each one is a bank direct debit (it appears in the bank account) or a standing
charge on a card (it appears in the card company's data), because the user cancels them in
different places.
Provide:
1. Monthly spending summary by category
2. Top 10 merchants by spending
3. Month-over-month trends
4. Recurring charges identified
5. Unusual transactions flagged

### Step 5: Export for Tax (if requested)
Prepare transactions for the user's accountant, not a filing:
- Separate business vs personal expenses as the user identifies them, and ask about anything
  ambiguous
- Include only completed lines, and select the period by `processedDate` (the date the
  charge actually went through) unless the accountant asks otherwise: run the script with
  `--exclude-pending --date-field processedDate`. Pending lines can still change
- Mark lines the user says are business purchases as candidates for the accountant to
  review. Whether VAT on a purchase is deductible depends on a valid tax invoice and on the
  business, which a bank line cannot show, so do not compute or claim a deduction
- Leave tax and Bituach Leumi payments, savings deposits and own transfers out of the
  business-expense list, and list them separately for the accountant instead. A
  self-employed user's pension and keren hishtalmut deposits matter to their tax position,
  so flag them without computing anything
- Mark mixed-use items (car, phone, home office) for the accountant to apportion; do not
  split them yourself
- Export a CSV with the columns date, processedDate, description, chargedAmount, currency,
  originalAmount, instalment number and total, category. Save it as UTF-8 with a byte-order
  mark so Excel shows the Hebrew correctly. Neither MCP server nor the bundled script writes
  an accounting-software import format or this CSV; build it from the `--output-json` output

## Examples

### Example 1: Monthly Spending Summary
User says: "Show me my spending breakdown for January"
Result: Categorized breakdown with NIS amounts per category, top merchants, and comparison to December.

### Example 2: Subscription Audit
User says: "What recurring payments am I making?"
Result: List of detected recurring charges with amounts, frequency, and suggestion for potential savings.

### Example 3: Tax Expense Export
User says: "Export my business expenses for my accountant"
Result: A CSV of the transactions the user marked as business, with a note on which lines need a tax invoice checked by the accountant.

## Bundled Resources

### Scripts
- `scripts/categorize_transactions.py`, Categorizes Israeli bank transactions by spending category using Israeli-specific merchant pattern matching (Shufersal, Rami Levy, Rav-Kav, etc.). Accepts either a JSON array of `{description, amount}` objects (CSV-style) or the israeli-bank-scrapers scrape result as returned by `fetch-transactions` (`accounts[].txns[]`, read via `chargedAmount`), and outputs categorized spending summaries. Filter to a period with `--from` / `--to`
(YYYY-MM-DD) on `--date-field date` (default) or `processedDate`; library timestamps are read
in Israel time, and `--period` is only a label. The bank-side credit-card bill and own transfers are reported as separate figures, outside Total Spending and Total Outflow, so they are not counted on top of the card's itemised lines. Foreign-currency lines are listed apart and never summed into the NIS figures; pending lines and instalment lines are counted and flagged, with pending full-price instalment purchases and pending lines of unknown amount listed but not summed. A transaction with a missing, blank, null or non-numeric amount stops the run with an error rather than being read as zero. Run: `python3 scripts/categorize_transactions.py --example` for a demo, or `python3 scripts/categorize_transactions.py --json transactions.json` for real data. Add `--output-json` for machine-readable output.

### References
- `references/spending-categories.md`, Israeli spending category definitions with Hebrew terms and common merchant examples for each category (housing/diur, groceries/mazon, transportation/tahaburah, utilities/shartuim, etc.). Consult when customizing categorization rules or explaining categories to users.
- `references/supported-banks.md`, Full list of 14 banks (Hapoalim, Leumi, Discount, Mercantile, Mizrahi-Tefahot, FIBI, Otsar HaHayal, Pagi, Union, Yahav, Massad, OneZero, Behatsdaa, Beyahad Bishvilha) and 4 credit card companies (Visa Cal, Max, Isracard, Amex) from the `israeli-bank-scrapers` `CompanyTypes` enum, with BOI bank codes, library scraper IDs, and MCP server coverage notes. Consult when setting up bank connections or troubleshooting missing accounts.

## Reference Links

| Source | URL | What to Check |
|--------|-----|---------------|
| israeli-bank-scrapers (npm library) | https://github.com/eshaham/israeli-bank-scrapers | Authoritative list of supported banks, breaking changes, scraper limitations |
| israeli-bank-scrapers on npm | https://registry.npmjs.org/israeli-bank-scrapers | Current release, and the `engines.node` floor. Latest is 6.12.2 (2026-09-29), Node >= 22.22.2 |
| israeli-bank-mcp (Motti Bechhofer) | https://github.com/mottibec/israeli-bank-mcp | The more current MCP wrapper (last pushed May 2026). Not on npm: clone and build. Its README bank list is stale, but the server iterates the library's `SCRAPERS` map, so it covers whatever the installed library covers |
| il-bank-mcp (Gilad Lekner) | https://github.com/glekner/il-bank-mcp | Docker-based MCP with built-in spending analysis and SQLite storage. Last pushed June 2025. Its committed `yarn.lock` resolves `israeli-bank-scrapers` to 6.1.4 and the Dockerfile installs with `yarn install --immutable`, so a fresh build gets 6.1.4, below the Max and Isracard fixes in 6.7.9 and 6.7.10 and without anything from 6.9.0 on |
| Bank of Israel: Consumer Enquiries | https://www.boi.org.il/en/information-and-service-to-the-public/consumer-enquiries-and-inspections/ | Official BOI Public Inquiries Unit, banking customer service, complaint workflow |
| Bank of Israel: Directive 368 (open banking), v6 text in circular 2778 | https://www.boi.org.il/media/k1dl4le3/2778.pdf | The official open-banking standard: based on the Berlin Group NextGenPSD2 framework with Israeli adaptations, API access for licensed providers only |
| Financial Information Service Law, 2021 (official gazette) | https://fs.knesset.gov.il/24/law/24_lsr_611801.pdf | Licensing of financial information service providers, and section 60 on access with the customer's login credentials |
| Israel Securities Authority: licensed financial information service providers | https://www.new.isa.gov.il/nav-index/supervised-api/supervised-by-isa | The register of licensed providers, if the user wants an official aggregator instead of a scraper |
| Bank of Israel: Access to Payment Systems | https://www.boi.org.il/en/economic-roles/supervision-and-regulation/payment-systems-oversight/access-to-payment-systems/ | Payment-system access terms. NOTE: rendered in a browser on 27 August 2026 this is a landing page last updated 19/11/2023 with no identification-code list, so do not cite it for bank codes |

## Handling credentials and transaction data

This skill sits on top of a scraper that takes live Israeli bank usernames, passwords and
one-time codes, and it produces a complete transaction history. Treat both as sensitive.

- Credentials belong in the MCP server's own configuration or environment, never in the
  chat, never in a file you create, and never in a command you echo back to the user.
- `israeli-bank-mcp` reads credentials from environment variables and deliberately never
  from tool arguments, precisely so they do not end up in the LLM conversation history. Its
  variable names are derived from the bank id and the login field by camelCase-to-upper-snake,
  so `leumi` plus `username` gives `LEUMI_USERNAME`, and `otsarHahayal` plus `username` gives
  `OTSAR_HAHAYAL_USERNAME`. Ask the `banks://list` resource which fields a given bank needs
  rather than guessing, because the shape differs per bank: Hapoalim's field is `userCode`, so
  its variable is `HAPOALIM_USER_CODE`. A missing variable does NOT produce a helpful error:
  the server returns only a generic `BANK_SCRAPER_ERROR`, so check the `banks://list` output
  against the environment before suspecting the bank.
- OneZero needs a long-term two-factor token, and `israeli-bank-mcp` cannot obtain one: its
  `two-factor-auth` tool builds a fresh scraper on every call, so the `get-token` call never
  sees the state the `trigger` call created and fails ("triggerOtp was not called"), while
  `trigger` reports "2FA code sent" whatever happened. Get the token with the library
  directly, calling `triggerTwoFactorAuth` (phone number starting with `+`) and then
  `getLongTermTwoFactorToken` on the SAME scraper object, as its README shows. Treat the token
  as a password. The server then requires an environment variable for EVERY OneZero login
  field: `ONE_ZERO_EMAIL`, `ONE_ZERO_PASSWORD`, `ONE_ZERO_PHONE_NUMBER`,
  `ONE_ZERO_OTP_LONG_TERM_TOKEN` (the token) and `ONE_ZERO_OTP_CODE_RETRIEVER`, which the
  library ignores once a token is present but which must still be set to a placeholder, or
  the server returns only the generic error.
- Never ask for, or help pass on, the user's bank password to anyone else, including their
  accountant. An accountant or bookkeeper logging into a client's account with the client's
  password in the course of their work is the conduct section 60 (see Gotchas) addresses.
  Whether it applies to a particular arrangement is a question for a lawyer, so do not tell
  the user their accountant is or is not breaking the law.
- Do not print, log, or repeat a credential, an OTP, or a card number, even partially, and
  do not ask the user to paste one into the conversation.
- **Environment variables are not a vault.** Both upstream READMEs show the password typed
  in plain text: `israeli-bank-mcp` inside the MCP client's JSON config `env` block, and
  `il-bank-mcp` on the `docker compose up` command line. That leaves the password readable on
  disk in the config file, and in shell history for the command-line form. Do not copy those
  examples as-is. Tell the user the password sits in that file, keep the file out of any git
  repository or synced folder and readable only by their own account, and where their setup
  allows it, inject the variables at launch from a password manager or the OS keychain
  instead of pasting them in. A long-term two-factor token (OneZero) is a credential too.
- Do not persist raw transaction dumps beyond what the current task needs, and tell the
  user where anything you do write is stored. Note that `il-bank-mcp` keeps scraped data in
  a local SQLite database (via `better-sqlite3`, with no encryption layer declared), so a
  full financial history sits on disk in readable form and outlives the session by design.
- Transaction descriptions reveal health providers, political donations, and religious
  institutions. Summarise; do not volunteer inferences about the person from their
  spending.

## Gotchas
- `israeli-bank-scrapers` logs in with the user's own username and password and scrapes the
  bank website. It is not Israel's official open-banking channel, and agents routinely reach
  for UK Open Banking or generic PSD2 endpoints instead. The official channel exists: the
  Financial Information Service Law, 2021 (in force since 14 June 2022) and Bank of Israel
  Directive 368, whose technical standard is based on the Berlin Group NextGenPSD2 framework
  with Israeli adaptations. Its API is open only to providers licensed by the Israel
  Securities Authority (or, where the provider is itself a regulated institution such as a bank, approved by that institution's own regulator),
  so an individual cannot call a bank's open-banking API directly.
- **If the user is building a service that logs into other people's accounts, stop and say
  so.** Section 60 of that law prohibits accessing a customer's financial data in the course
  of business (דרך עיסוק), online, with the customer's own login credentials, to provide them
  a service, and the law's penalty provision makes a breach an offence punishable by up to a
  year in prison. That describes what a product built on this scraper for other people would
  do; the licensed API route exists for that, and anyone planning such a service should take
  legal advice before building it. The section does not address
  someone running the scraper on their own accounts for themselves, so do not tell a user that
  personal use is either legal or illegal.
- The scrapers differ per bank: each has its own login fields and its own history cap, so
  there is no single connection shape that covers all Israeli banks.
- Mercantile and Otsar HaHayal are SEPARATE scrapers in the upstream library even though they are subsidiaries of Discount and FIBI respectively. Treat them as their own connection (each has its own loginFields shape). Do not assume Discount credentials cover Mercantile or that FIBI credentials cover Otsar HaHayal.
- Transaction history depth is set per scraper. The library's README gives one year for most of them, one year minus a day for Discount and Mercantile, and six months for Yahav. A request for older data is clamped rather than refused, so tell the user what the scrape actually returned rather than what you asked for.
- What the library can retrieve depends on the installed version, so check the version before you debug. 6.9.0 (2026-07-22) added Leumi savings accounts and Max credit card balances, 6.10.0 added Isracard credit card balances, and 6.12.0 added Leumi foreign-currency accounts; the latest release is 6.12.2 (2026-09-29), which fixed Mizrahi's detection of the bank's change-password page. If a user reports one of those missing, check the installed version before assuming the scrape failed. Releases before 6.7.9 carry a Max login-page failure and releases before 6.7.10 an Isracard bot-detection problem (both fixed then, per the release notes), so an old install is likely to fail on those two providers rather than just return less.
- A Leumi foreign-currency account reports its transactions in that currency. Never add them to a shekel total; the bundled script lists foreign-currency lines apart for this reason.
- Check the INSTALLED scraper version, not the declared range. `israeli-bank-mcp` declares
  `^6.7.3`, so a fresh `npm install` resolves to the current release. `il-bank-mcp` declares
  `^6.1.4` but commits a `yarn.lock` that pins 6.1.4 and builds with `--immutable`, so every
  fresh Docker build runs 6.1.4 unless the lockfile is updated. For Max, Isracard or anything
  added from 6.9.0 on, prefer `israeli-bank-mcp`.
- Pending card lines are unreliable (see Step 2): a pending Visa Cal instalment purchase
  carries the full price, and a pending Max line can carry a charged amount of 0.
- Israeli bank account numbers include a branch number (snif) prefix. Agents may validate account numbers using international IBAN format, but Israeli domestic transfers use the local branch+account format.
- Credit card statements in Israel are issued by separate companies (Isracard, Max, CAL) and not directly by the banks. Agents may try to fetch credit card data from the bank API instead of the card company.

## Troubleshooting

`israeli-bank-mcp` reports a failed scrape as `{"error": "<errorType>", "message": "Bank scraper error occurred"}`, where errorType is one of the library's values. Any other failure, including a missing credential variable, arrives as the generic `BANK_SCRAPER_ERROR`.

### Error: INVALID_PASSWORD, CHANGE_PASSWORD or ACCOUNT_BLOCKED
Cause: the bank rejected the login, wants the password changed on its own site, or has blocked the account
Solution: Stop. Do not retry automatically: repeated failed logins are how an account ends up blocked, and ACCOUNT_BLOCKED is one of the outcomes the library reports. For CHANGE_PASSWORD the user logs in on the bank's website first, then updates the environment variable. For ACCOUNT_BLOCKED the user contacts the bank.

### Error: TWO_FACTOR_RETRIEVER_MISSING or TIMEOUT
Cause: the login needs a one-time code the server cannot supply (the server never prompts for one; OneZero needs a long-term token in the environment), or the bank site was slow or refused automated access
Solution: For two-factor, obtain the long-term token with the library directly, as described under Handling credentials (the server's own `two-factor-auth` tool cannot complete it). For a timeout, retry once after a few minutes, then check the israeli-bank-scrapers GitHub issues for that bank. How often a bank asks for a new code is not documented here, so do not promise the user it is a one-time step.

### Error: BANK_SCRAPER_ERROR
Cause: anything the server did not classify, most often a missing or misnamed credential variable
Solution: Compare the `banks://list` output for that bank with the variables actually set (for example `HAPOALIM_USER_CODE`, not `HAPOALIM_USERCODE`), and check `node --version`.

### Error: "Missing credit card transactions"
Cause: Credit card company is separate from bank in Israel
Solution: Add credit card company (Visa Cal, Max, Isracard) as a separate connection in the MCP server configuration.