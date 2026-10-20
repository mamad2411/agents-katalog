# Claude Command: Jurisprudence Search

Execute the Jurisprudence Research Agent for iterative deep research on Brazilian court jurisprudence.

## Usage

```
/jurisprudence-search "Seu tema de pesquisa juridica"
```

Or with arguments:
```
/jurisprudence-search --check   # Check dependencies only
/jurisprudence-search --help    # Show available courts
```

## What This Command Does

1. Validates that the Gemini ADK environment is properly configured
2. Executes the Jurisprudence Research Agent with the provided topic
3. The agent autonomously:
   - Decomposes the legal topic into sub-vectors
   - Executes iterative searches with site restrictions (whitelist of court domains)
   - Extracts jurisprudence metadata (processo, relator, data)
   - Analyzes gaps and refines queries
   - Synthesizes findings into a structured legal report
4. Saves results to `adk-agents/jurisprudence_agent/research_output/`

## Court Domains (Whitelist)

The agent restricts searches to official Brazilian court domains:

| Code | Court | Domain |
|------|-------|--------|
| STJ | Superior Tribunal de Justica | stj.jus.br |
| STF | Supremo Tribunal Federal | stf.jus.br |
| TJSP | TJ Sao Paulo | tjsp.jus.br |
| TJMG | TJ Minas Gerais | tjmg.jus.br |
| TJRJ | TJ Rio de Janeiro | tjrj.jus.br |
| TRF1-5 | Tribunais Regionais Federais | trf1-5.jus.br |

## Execution

When the user invokes this command, execute:

```bash
REPO_ROOT=$(git rev-parse --show-toplevel 2>/dev/null || echo "/home/cmr-auto/claude-work/repos/lex-vector")
cd "$REPO_ROOT/adk-agents/jurisprudence_agent" && source .venv/bin/activate && python agent.py "$ARGUMENTS"
```

If `$ARGUMENTS` is empty, ask the user for a legal research topic in Portuguese.

If `$ARGUMENTS` is `--check`, run:
```bash
REPO_ROOT=$(git rev-parse --show-toplevel 2>/dev/null || echo "/home/cmr-auto/claude-work/repos/lex-vector")
cd "$REPO_ROOT/adk-agents/jurisprudence_agent" && source .venv/bin/activate && python -c "from agent import JurisprudenceAgent; print('OK')"
```

If `$ARGUMENTS` is `--help`, show available courts:
```bash
REPO_ROOT=$(git rev-parse --show-toplevel 2>/dev/null || echo "/home/cmr-auto/claude-work/repos/lex-vector")
cd "$REPO_ROOT/adk-agents/jurisprudence_agent" && source .venv/bin/activate && python agent.py
```

## Prerequisites

- `GOOGLE_API_KEY` environment variable (loaded from `.env` files)
- Python virtual environment at `adk-agents/jurisprudence_agent/.venv/`
- Required packages: `google-adk`, `google-genai`, `tenacity`

## Output Format

Research results are saved as Markdown with:
- **Principais Entendimentos**: Posicao majoritaria e minoritaria
- **Casos Paradigmaticos**: Tabela com processo, tribunal, tese
- **Sumulas e Teses Vinculantes**: Lista de sumulas relevantes
- **Lacunas e Limitacoes**: O que nao foi encontrado
- **Indice de Fontes**: URLs por tribunal

## Examples

Basic jurisprudence research:
```
/jurisprudence-search "Responsabilidade civil por dano moral em relacoes de consumo"
```

Specific legal topic:
```
/jurisprudence-search "Prazo prescricional para acao de cobranca de honorarios advocaticios"
```

Tax law research:
```
/jurisprudence-search "ICMS-ST restituicao base de calculo presumida superior efetiva"
```

Check setup:
```
/jurisprudence-search --check
```

## Troubleshooting

| Issue | Solution |
|-------|----------|
| "No API key found" | Check `.env` has `GOOGLE_API_KEY` |
| "Agent initialization failed" | Run `/jurisprudence-search --check` |
| Timeout | Simplify the research topic |
| Rate limit (429) | Wait and retry, or reduce query complexity |
| Few results | Broaden the search terms |

## Notes

- Research typically takes 30-90 seconds depending on topic complexity
- The agent uses `gemini-2.5-flash` model by default
- Output directory: `adk-agents/jurisprudence_agent/research_output/`
- Default domains: STJ, TJSP, TJMG, TJRJ, TRF4
- All searches use Google Search with site: restrictions for accuracy
