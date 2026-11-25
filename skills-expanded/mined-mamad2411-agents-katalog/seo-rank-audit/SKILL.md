---
name: seo-rank-audit
description: >-
  Audita um site ou blog e dá notas (0-100) por critério segundo os fatores de
  ranqueamento documentados do Google e do Bing, com nota separada por buscador,
  nota geral e lista priorizada de correções. Use esta skill sempre que o
  usuário pedir auditoria de SEO, análise de site/blog, "por que não ranqueio",
  nota de SEO, revisão de página para Google/Bing, ou comparação de SEO entre
  páginas ou concorrentes — mesmo que não use a palavra "auditoria".
---

# SEO Rank Audit

Audita um site com dados coletados deterministicamente + avaliação qualitativa,
e produz um relatório com notas Google, Bing e geral.

## Fluxo

1. **Coleta** — rode o script (só biblioteca padrão, sem instalar nada):
   ```bash
   python3 scripts/audit.py https://site-do-usuario.com --pages 8 --output audit.json
   ```
   Ele analisa a URL informada + amostra de 5–10 páginas internas e salva o
   JSON com todos os fatores mensuráveis (title, metas, headings, canonical,
   schema, robots, sitemap, HTTPS, alt, links, peso, tempo de resposta).

1b. **Core Web Vitals reais** — rode também o PageSpeed Insights (API
   gratuita do Google; funciona mesmo quando o site bloqueia bots, porque
   quem acessa é o Google):
   ```bash
   python3 scripts/pagespeed.py https://site-do-usuario.com --strategy both
   ```
   O resultado traz a nota Lighthouse (laboratório) e os dados CrUX de
   usuários reais (LCP, CLS, INP no p75). **Quando disponíveis, esses dados
   substituem os proxies de tempo/peso nas duas rubricas** — nada de proxy
   nem "não verificado" para velocidade. Se o site for pequeno demais para
   ter CrUX, use a nota Lighthouse e diga que é dado de laboratório.

   Funciona **sem chave e sem cadastro** — não mencione chaves de API ao
   usuário. Rode em no máximo 2 URLs (home + 1 página-modelo): CWV vêm do
   template, medir a amostra toda desperdiça cota sem ganhar informação.
   Se a cota por IP estourar, o próprio script orienta; o plano B sem chave
   é Lighthouse local:
   ```bash
   npx lighthouse URL --only-categories=performance --output=json --quiet
   ```

2. **Leitura qualitativa** — busque o conteúdo de 2–3 páginas amostradas
   (as mais representativas: home + 1 página de conteúdo + 1 página de
   conversão) e avalie o que o script não mede: utilidade real do conteúdo,
   E-E-A-T, intenção de busca, clickbait, densidade de anúncios.

3. **Pontuação** — leia `references/google.md` e `references/bing.md` e aplique
   os pesos de cada um sobre os dados do JSON + sua leitura qualitativa.
   As duas rubricas são diferentes de propósito: não copie a nota de um
   buscador para o outro.

4. **Relatório** — use o formato abaixo.

5. **Relatório visual (opcional)** — NÃO gere por padrão. Só quando o usuário
   pedir ("gera um relatório", "quero em HTML/PDF") ou quando for auditoria
   completa de site inteiro. Monte um JSON com o esquema documentado no topo de
   `scripts/render_report.py` e renderize:
   ```bash
   python3 scripts/render_report.py --data relatorio.json --output auditoria-SITE-DATA.html
   ```
   Regras do relatório visual, sem exceção:
   - Categorias não medidas vão com `"verified": false` — aparecem como "não
     verificado" na mesma linha da nota, não escondidas no rodapé. Nunca
     invente pontuação para preencher a tabela.
   - `collection_note` é obrigatório quando a coleta foi parcial.
   - `unverified` lista cada item fora do alcance E como o usuário pode checar.
   - O layout é fixo: preencha o JSON, não reescreva o template. Isso mantém
     todos os relatórios consistentes e economiza tokens.
   - **Sempre termine mostrando o caminho absoluto do arquivo gerado como link
     `file://`**, para o usuário abrir com um clique — ex:
     `file:///home/usuario/auditoria-exemplo-com-2026-07-24.html`. Resolva o
     caminho absoluto real (não relativo) antes de mostrar. Isso não é um
     link compartilhável na internet — só abre no navegador de quem rodou a
     skill, no computador onde ela rodou.

O fluxo acima é 100% sem chave, sem cadastro e sem configuração. Não
mencione chaves de API a menos que o usuário peça mais profundidade ou a
cota do PSI estoure.

## Extra opcional: dados privados do Bing (exige chave, só sites do usuário)

Só ofereça se o usuário pedir dados de dentro do Bing Webmaster Tools
(tráfego, crawl, backlinks) para um site **verificado na conta dele**:
```bash
python3 scripts/bing_wmt.py https://site-do-usuario.com --key CHAVE
```
Chave em: Bing Webmaster Tools → Configurações → Acesso de API (ou variável
`BING_WMT_KEY`). Com esses dados, "Bing WMT configurado" sai do "não
verificado" e os problemas de crawl do próprio Bingbot viram evidência
primária da Técnica. Nunca peça chave para auditar site de terceiros — a
API só responde para sites da conta. Sem a chave, a auditoria continua
completa: os itens ficam "não verificado" e são renormalizados.

## Regras de honestidade

- Os algoritmos reais não são públicos. Diga isso na primeira linha do
  relatório: as notas refletem fatores **documentados**, não o ranking real.
- Todo dado citado deve vir do `audit.json` ou da leitura das páginas. O que
  não puder ser medido (backlinks, Core Web Vitals reais, penalidades,
  IndexNow, Bing WMT) entra como **"não verificado"** com recomendação de como
  o usuário pode checar — nunca chute uma nota para esses itens.
- Tempo de resposta e peso de página são **proxies** de Core Web Vitals;
  rotule-os como proxies.
- Se uma página amostrada falhar (erro/timeout), reporte a falha — isso é
  achado de auditoria, não ruído.
- **Renormalização**: itens marcados como "não verificado" saem da base de
  cálculo da categoria — nota = pontos obtidos ÷ pontos verificáveis × máximo
  da categoria. Informe no relatório quantos pontos foram renormalizados,
  para a nota não punir o que a auditoria não alcança.

## Fallback quando o site bloqueia o script (WAF/Cloudflare)

Se o `audit.py` retornar 403 ou páginas vazias, o site está bloqueando bots.
Não desista nem invente dados:

1. Colete os mesmos fatores buscando as páginas com a ferramenta de fetch/web
   do próprio ambiente (que costuma passar por WAFs) — title, metas, headings,
   canonical, schema, links — manualmente para a home + 3-4 páginas.
2. Reduza a amostra e declare no relatório: "coleta parcial via fallback
   (site bloqueou o coletor automático); amostra reduzida".
3. Fatores que dependem do coletor (tempo de resposta, peso transferido,
   gzip) entram como "não verificado" e são renormalizados.

## Formato do relatório

SEMPRE use este template:

```markdown
# Auditoria SEO — {domínio}
*Notas baseadas em fatores de ranqueamento documentados (não no algoritmo real).
Amostra: {n} páginas em {data}.*

## Placar
| | Google | Bing |
|---|---|---|
| Conteúdo/Qualidade | x/25 | x/25 |
| Relevância on-page | x/20 | x/25 |
| Experiência/Velocidade | x/15 | x/15 |
| Mobile | x/10 | — |
| Frescor | — | x/15 |
| Técnica | x/15 | x/20 |
| Links | x/15 | — |
| **Total** | **x/100** | **x/100** |

**Nota geral: x/100** (média das duas)

## Divergências Google × Bing
{onde o site pontua diferente em cada buscador e por quê}

## Top 5 correções por impacto
1. {correção} — afeta {categoria}, impacto estimado {alto/médio}
...

## Detalhe por categoria
{nota + evidência concreta com URL + correção, para cada categoria}

## Não verificado
{itens fora do alcance da auditoria e como checá-los}
```

## Exemplos de disparo

- "Analisa o SEO do meusite.com.br" → fluxo completo
- "Por que essa página não ranqueia no Bing?" → fluxo completo com foco no
  detalhamento Bing
- "Compara o SEO do meu site com o do concorrente X" → rode o fluxo para os
  dois domínios e apresente os placares lado a lado
