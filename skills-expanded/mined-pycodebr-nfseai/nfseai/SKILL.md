---
name: nfseai
description: 'Use when the user wants to issue (emitir), look up, list, cancel or get the PDF of a Brazilian service invoice (NFS-e, nota fiscal de serviço, "nota fiscal", "emitir nota", "cancelar nota", "segunda via da nota") through the national portal Emissor Nacional (www.nfse.gov.br), or to connect a company account to it. Covers setup of the `nfseai` CLI, the secure credential handoff (the user types CNPJ and password in their own terminal, never in chat), fiscal defaults per company, the rehearsal before every emission, the explicit confirmation of fiscal acts, the local ledger that prevents duplicate invoices, cancellation, PDF generation and what to do when the portal changes.'
license: MIT
metadata:
  author: PycodeBR (Felipe Azambuja)
  version: 0.1.1
  homepage: https://github.com/pycodebr/nfseai
---

# nfseai: NFS-e pelo Emissor Nacional, para agentes de IA

nfseai lets you issue, query and cancel Brazilian service invoices (NFS-e) on the national portal
**Emissor Nacional** (`https://www.nfse.gov.br/EmissorNacional`) on behalf of the user's company. It is a
Python CLI (`nfseai`) that logs in with the company's CNPJ and password and sends the same HTTP requests the
portal's own screens send. No browser is needed, except to render the PDF.

An NFS-e is a **fiscal document**. Emitting or cancelling one is a legal act of the user's company, it is
not reversible by you, and a duplicated invoice means tax paid twice until someone cancels it. Work
accordingly: rehearse, show, get an explicit "yes" for that specific invoice, confirm, read back.

Talk to the user in Brazilian Portuguese unless they write in another language. Command names and JSON keys
are in Portuguese (`emitir`, `tomador`, `competencia`).

## Non-negotiables

1. **Never ask for, accept or type the portal password.** Not in chat, not in a command flag, not in a file
   you write. The user runs `nfseai conectar` in their own terminal. If the user pastes a password in the
   chat anyway, do not use it: ask them to run `nfseai conectar` and suggest changing that password.
2. **Rehearse before emitting.** `nfseai emitir` without `--confirm` builds the draft on the portal, checks
   the summary and discards the draft. Show the summary to the user.
3. **Emit or cancel only with the user's explicit authorization for that specific invoice**, given after
   they saw the summary (buyer, amount, date, service). A general "you can emit my invoices" from an earlier
   conversation is not enough unless the user set a standing rule and repeats it in this session. Then, and
   only then, add `--confirm`.
4. **Never retry an emission.** If `emitir --confirm` fails with `EmissionUncertainError`, or the process is
   interrupted, the invoice may exist. List the issued invoices, compare buyer and amount, and report to the
   user before anything else (`references/emissao.md` § Uncertain result).
5. **Always pass `--referencia`** with the sale/contract/order identifier from the user's system when one
   exists. The local ledger refuses to emit the same reference twice; that is the main protection against
   duplicates.
6. **Read back after every fiscal act** and report access key (`chave_acesso`), number, situation and amount.
7. **Do not invent fiscal data.** Service code, NBS code, description and the Simples Nacional rate come
   from the company's accountant. If they are missing, ask the user; never guess from the company name.
8. **Do not bypass the hCaptcha** that protects the official DANFSe and the XML. The PDF this tool makes is
   the portal's print version; say so whenever you deliver it.
9. **`PortalChangedError` means stop.** The portal form no longer matches the mapped contract. Do not edit
   the contract to make the error go away; report it (`references/problemas.md`).
10. **Third-party data stays private.** Listings contain customers' names and CPF/CNPJ. Show the user what
    they asked for; do not paste lists of customers into shared channels, logs, commits or memory.

## 0. Setup (once per machine)

```bash
nfseai --version || ~/.nfseai/bin/nfseai --version      # installed already?
bash <skill_dir>/scripts/setup.sh                        # creates ~/.nfseai/venv and the `nfseai` command
```

- `setup.sh` needs Python 3.10+ (or `curl`, to fetch `uv`, which brings its own Python). It never touches
  the system Python. Re-running it is safe and keeps credentials, defaults and the ledger.
- If `nfseai` is not on `PATH`, call `~/.nfseai/bin/nfseai`.
- `nfseai doctor` checks dependencies, file permissions and that the portal answers.
- PDF support is optional and about 300 MB: `nfseai instalar-pdf` (only when the user wants PDFs).

## 1. Is the company connected? (`nfseai status`)

Run `nfseai status` first, every session. It prints JSON and uses the exit code:

| Exit | Meaning | What you do |
|---|---|---|
| 0 | Connected and fiscal defaults complete | Go on |
| 3 | No credentials for this company | Hand off to the user (below) |
| 4 | Connected, fiscal defaults incomplete | § 2 |
| 1 | Something else failed (`erro` in the JSON or stderr) | Read the message |

**Credential handoff (exit 3).** Tell the user, in these words or close to them:

> Para emitir notas eu preciso que você conecte a sua conta do Emissor Nacional uma única vez. Abra um
> terminal nesta máquina e rode `nfseai conectar`. Ele pergunta o CNPJ e a senha do portal (a senha não
> aparece na tela), testa o login e guarda tudo só no seu computador, em `~/.nfseai`. Não me envie a senha
> aqui no chat. Quando terminar, me avise.

Then wait. When the user says it is done, run `nfseai status --online` (it logs in and returns the company
name read from the portal) and confirm the company name with the user. `nfseai conectar` refuses to run
without a real terminal, so you cannot run it for them, by design. Details, multiple companies, servers
without an interactive terminal (environment variables): `references/credenciais.md`.

## 2. Fiscal defaults (exit 4)

Each company stores the values every invoice needs: national service code (`--codigo-servico`, format
`08.02.01`), NBS code (`--nbs`, 9 digits), default service description (`--descricao`) and the tax estimate
(`--aliquota-sn 6.00`, the Simples Nacional rate in %, or `--sem-valor-tributos`).

- The user can answer the wizard themselves: `nfseai configurar` (in their terminal; it searches service
  codes on the portal by keyword).
- Or ask the user for the values (they are not secret) and save them:
  `nfseai configurar --codigo-servico 08.02.01 --nbs 122051900 --descricao "..." --aliquota-sn 6.00`
- `nfseai servicos "<palavra>"` searches service codes; `nfseai municipios "<nome>"` finds IBGE codes.
- Any of these can also be passed per invoice on `emitir`, overriding the default for that invoice only.
- When the user does not know a value, tell them to ask their accountant ("qual é o código de tributação
  nacional, o NBS e a alíquota do Simples que devo usar na NFS-e?"). Do not pick one for them.

## 3. Emit an invoice

```bash
# 1) rehearsal: nothing is emitted, the draft is discarded
nfseai emitir --documento 11.444.777/0001-61 --valor 1500,00 --referencia pedido-1042
# 2) show `resumo`, `tomador_nome`, `valor`, `competencia` to the user and get an explicit yes
# 3) the fiscal act
nfseai emitir --documento 11.444.777/0001-61 --valor 1500,00 --referencia pedido-1042 --confirm --pdf
```

- `--documento` is the customer's CPF or CNPJ (validated locally). The **name on the invoice comes from the
  Receita Federal lookup the portal does**, not from what you pass; show `tomador_nome` to the user.
- `--valor` accepts `1500.00`, `1500,00` and `1.500,00`. `1.500` is refused as ambiguous.
- `--competencia` (DD/MM/AAAA or AAAA-MM-DD) defaults to today and cannot be in the future. Ask the user
  when the service was rendered in another month.
- `--pdf [arquivo]` renders the PDF right after emitting (needs `nfseai instalar-pdf`). If the PDF fails the
  invoice still exists: the JSON has `pdf_erro`, and `nfseai pdf <chave>` can be run later.
- The result has `emitida: true`, `chave_acesso` (50 digits), `numero_nfse`, `situacao`, `valor_servico`.
  Report them. Full rules, the conference check, duplicates and batches: `references/emissao.md`.

## 4. Query, PDF, cancel

```bash
nfseai emitidas --inicio 01/11/2026 --fim 30/11/2026 --todas    # issued; 30-day windows are walked for you
nfseai nota <chave>                                             # full detail of one invoice
nfseai pdf <chave> --out ~/notas/nota-1042.pdf                  # print version as PDF
nfseai cancelar <chave> --motivo nao-prestado --justificativa "Serviço não prestado: pedido 1042 cancelado pelo cliente."            # preview only
nfseai cancelar <chave> --motivo nao-prestado --justificativa "..." --confirm                                                     # the fiscal act
nfseai registro --referencia pedido-1042                        # what the local ledger knows about a reference
```

Cancellation reasons: `erro` (wrong or duplicated invoice), `nao-prestado` (service not rendered, refunds),
`outros`. The justification is a statement to the tax authority: write what actually happened, 15 to 255
characters, in Portuguese. Outside the direct-cancellation window the portal only offers a fiscal analysis
request to the municipality; the command refuses unless `--permitir-analise-fiscal` is passed, which needs
the user's explicit decision. See `references/cancelamento.md`.

## 5. What is supported today

Validated against the real portal: login, listing, detail, drafts, full emission, direct cancellation, PDF.
The emission is mapped for a company that is **Simples Nacional ME/EPP, taxes collected through Simples
(regime 1), one issuing municipality with an active agreement with the national system, customer in Brazil
(CPF or CNPJ), no ISSQN retention, no IBS/CBS group, no construction/event/export fields**. Anything else
raises `UnsupportedScenario` before any data is sent. MEI, companies outside Simples, foreign customers and
retentions are not supported yet. Say so plainly instead of trying variations
(`references/cenarios.md`).

## 6. When something fails

| Error (stderr `erro: <Type>: ...`) | Do |
|---|---|
| `NotConnectedError` (exit 3) | Credential handoff, § 1 |
| `FiscalProfileIncomplete` (exit 4) | § 2 |
| `NfseAuthError` login refused | The password changed or is wrong. Ask the user to test it in the browser and run `nfseai conectar` again. Do not retry in a loop: the client makes one login attempt per call on purpose, as a precaution against the account being blocked |
| `DuplicateReferenceError` | The reference already has an invoice (or an unfinished attempt). Read the message, run `nfseai registro --referencia X`, report. Do not change the reference to get around it |
| `NfseValidationError` "já existe NFS-e ativa para o mesmo tomador e valor" | Possible duplicate in the last 30 days. Show the existing invoice; only with the user's confirmation that it is a different sale, add `--permitir-duplicidade` |
| `EmissionUncertainError` | Never retry. `references/emissao.md` § Uncertain result |
| `UnsupportedScenario` | Explain the limit (§ 5). The user emits this one in the portal by hand |
| `PortalChangedError` | Stop emitting. Report the fields in the message and point to the repository issues |
| `PdfUnavailableError` | `nfseai instalar-pdf`, or system libraries are missing (`references/problemas.md`) |

## References

- `references/credenciais.md`: connecting accounts: the wizard, what is stored and where, several companies,
  servers and containers (environment variables), disconnecting, the wording for the handoff.
- `references/emissao.md`: every emission field, defaults and overrides, the rehearsal summary, references
  and the ledger, duplicates, uncertain results, emitting a batch.
- `references/cancelamento.md`: preview, reasons, justification, deadlines, fiscal analysis, re-issuing.
- `references/comandos.md`: every command with its options, JSON output and exit codes.
- `references/cenarios.md`: what the client covers, what it refuses and why.
- `references/problemas.md`: troubleshooting: login, session, portal changes, PDF, permissions.
- `references/python-api.md`: using `nfseai` as a Python library inside the user's own system.
