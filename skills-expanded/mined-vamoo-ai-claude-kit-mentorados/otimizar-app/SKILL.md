---
name: otimizar-app
description: >-
  App ou landing "pesado", "lento", "travando", "demora pra carregar", egress
  alto: mede antes, corrige na camada certa, mede depois e prova no ar, sem
  mudar o visual.
allowed-tools:
  - 'Bash(node "${CLAUDE_PLUGIN_ROOT}/skills/otimizar-app/scripts/runtime-bench.mjs" *)'
  - 'Bash(node ${CLAUDE_PLUGIN_ROOT}/skills/otimizar-app/scripts/runtime-bench.mjs *)'
  - 'Bash(node "${CLAUDE_PLUGIN_ROOT}/skills/otimizar-app/scripts/layout-snapshot.mjs" *)'
  - 'Bash(node ${CLAUDE_PLUGIN_ROOT}/skills/otimizar-app/scripts/layout-snapshot.mjs *)'
---

# Otimizar app — medir, corrigir, provar

> Origem: uma landing com a queixa "tá bem pesado, sem mexer no visual", somada a cerca de
> 50 otimizações feitas em apps reais ao longo de seis meses (dashboards, SaaS
> multi-tenant, landings, apps com WhatsApp). A técnica variou de caso para caso, e o
> erro se repetiu:
> - diagnóstico feito por leitura de código apresentado como medido;
> - fix sem ganho commitado como `perf:`;
> - otimização que nunca chegou ao ar.

## Fronteira: o que esta skill NÃO é

| Skill | Responde |
|---|---|
| **`otimizar-app`** (esta) | "Está pesado/lento. Onde, quanto, e quanto melhorou?" |
| `baseline` | "A plataforma está apta a produção?" É postura. O pilar 05 tem as queries de banco que esta skill usa. |
| `verificacao` | "Posso dizer pronto?" |
| nenhuma do kit | VPS, Docker ou Traefik lento, ou dockerd com CPU alta: é o host, não o app. Meça lá antes de abrir código. |
| `ship` | levar o fix para o ar. Se existir `.context/docs/deploy.md` no projeto, ele diz como. |

## 0. Triagem: "travando" quase nunca foi a CPU do app

Antes de abrir código, descarte o que já enganou em casos reais:

| Queixa | Causa real que já apareceu | Como descartar |
|---|---|---|
| "demora absurda pra trocar de página" | app rodando em `next dev`, que compila cada rota na primeira visita | Está em `dev`? Meça em `build` + `start`. |
| "trocar de aba trava", com servidor rápido | tempo morto: rota dinâmica (sessão no cookie) não é pré-carregada e nada muda na tela até o servidor responder | clique → 1ª mudança na tela vs clique → pronto, medidos separados |
| "travando", número parado ou errado | dado velho: memo congelou o intervalo de datas e não havia polling | É lentidão, ou é valor que não muda? |
| tudo lento, em toda rota | função Vercel em `iad1` com banco em `sa-east-1`, ~110 ms por ida e volta | header `x-vercel-id`: `gru1::iad1` quer dizer que atravessa o oceano |
| login preso em "Entrando..." | request pendurada: fetch sem timeout e sem `maxDuration` | requests concorrentes mais uma sonda direta no Supabase |
| "trava meu computador" | a máquina: disco cheio, Chrome escrevendo GB no SSD | Monitor de Atividade ou `iostat` antes de olhar o app |
| tela zera, "Algo deu errado", 503 | banco: `statement_timeout` (57014) com a view fria, sort derramando para disco | logs do Supabase e `pg_stat_statements` |

Se a causa é uma dessas, o fix é outro (build de prod, região, timeout, polling), e costuma
ser o maior ganho por linha mudada.

## 1. Número de partida, antes de qualquer edit

Impressão de lentidão sem medição não entra no relatório. Escolha a medida pela queixa:

| Queixa | Medida | Ferramenta |
|---|---|---|
| página pesada parada ou rolando, celular esquenta | CPU da main thread e do Chrome, por fase | `scripts/runtime-bench.mjs` |
| demora para aparecer | LCP/TBT/CLS e bytes por asset | `npx lighthouse@12.8.2` headless, `curl -w` |
| digitação ou filtro travando | ms por interação com CPU 4× | trace do DevTools, Playwright cronometrado |
| troca de página ou API lenta | TTFB com n ≥ 30, mediana e p95 | `curl -w` em laço |
| troca de aba "travando" no navegador | clique → 1ª mudança na tela **e** clique → pronto (sem skeleton, rede quieta), por aba | Playwright com clique no menu, receita em `medir-e-provar.md` |
| egress, Disk IO ou conta subindo | requests por minuto, top queries | delta de `pg_stat_statements` |
| bundle grande | o que carrega **no boot**, não o total do `dist` | build real + o que o `index.html` baixa |

Comandos, perfis e armadilhas do próprio instrumento estão em `references/medir-e-provar.md`.
Salve o número de partida num arquivo: o "antes" some quando o código muda.

## 2. Camada → reference

Carregue só a da camada que o número apontou:

- CPU contínua, animação, scroll, input travando, re-render, tempo morto no clique da aba → `references/front-runtime.md`
- bytes (bundle, imagens, fontes, cache HTTP) → `references/assets-bundle.md`
- lista inteira no cliente, N+1, realtime, egress, índice, região → `references/dados-rede.md`

## 3. Fix mais barato primeiro, dentro das restrições

Anote as restrições antes do primeiro edit. São as que o usuário repete:

- **Sem mudar o visual.** Não troque arte, cor, fonte, tamanho nem animação visível. Otimize
  o *como* (pausar o que está fora da tela, frequência, formato do arquivo), não o *quê*.
- **Não perder nada.** Não apague asset, rota ou dado, e não renomeie arquivo que o bundle referencia.
- **Sem custo.** Não suba plano ou compute sem avisar. Escala vertical compra tempo, não resolve.

Ordem de preferência:
1. configuração (build de prod, região, header de cache);
2. parar trabalho inútil (fora da tela, polling, invalidação ampla);
3. mover o trabalho para o lugar certo (agregar no banco, `sizes` na imagem);
4. reescrever.

**Um fix por vez, cada um medido.** Três hipóteses juntas escondem qual ganhou e qual piorou.

## 4. A mesma medição depois: "sem ganho" é resultado

Use o mesmo script, o mesmo perfil e o mesmo número de runs, comparando o mesmo tipo de
alvo (prod com prod, build local com build local). Se o resultado ficou dentro do ruído,
**não commite como otimização**:

- **Três hipóteses de bundle vindas de leitura de código** (barrel, lazy e preload). Medidas,
  nenhuma mexeu no que carrega no boot, e foram revertidas sem commit. O gargalo era dado.
- **Um dedupe correto de requests** deixou a mediana de TTFB igual à de antes, dentro do
  desvio, com n=30. Foi reportado como "indistinguível do ruído", não como "−1 s".

Código mais limpo pode entrar, com o nome certo: `refactor:`, não `perf:`.

**Retorno visual não é carregamento.** Esqueleto ou link marcado no clique muda o "1ª
mudança" e pode piorar o "pronto": o `loading.tsx` do Next (Suspense) deu 267 → 24 ms de
resposta com o pronto "igual" na mediana (n=3), e o A/B intercalado mostrou +150 ms no
pronto, porque o React segura o conteúdo ~300 ms depois do esqueleto. Mediana empatada com
n pequeno não descarta piora: antes de subir, A/B intercalado. Em navegação abaixo de
~300 ms, `useLinkStatus` no link dá a resposta sem Suspense. Reporte como "retorno visual",
nunca como "N× mais rápido". Detalhe em `references/front-runtime.md`.

## 5. Provar no ar, e sem mudança visual

- **Chegou ao ar?** Otimização pronta já ficou parada por deploy BLOCKED pelo autor do
  commit, por `.vercel/project.json` apontando para outro projeto e por PR aberto no repo
  errado. Confira os **bytes servidos** pelo domínio:
  - o marcador do fix no bundle;
  - o `content-length` de cada asset otimizado.

  Receita em `references/medir-e-provar.md`.
- **O visual ficou igual?** Rode `scripts/layout-snapshot.mjs` antes e depois, em desktop
  e mobile, e depois `--compare`. "0 diferenças" quer dizer estrutura igual. O que o
  snapshot não vê (cor, blur, a animação em si) pede um screenshot de cada lado, uma vez só.
  Se forem mais de 2, use um subagent.

## Relatório antes × depois

```
| Cenário (perfil)                  | Antes | Depois | Δ    |
|-----------------------------------|-------|--------|------|
| mobile, parado no meio — CPU main | 60,0% | 15,0%  | −75% |
```

- A linha acima é só o formato; os números são ilustrativos.
- Mesma métrica e mesmo perfil, com n de runs e mediana declarados.
- Uma linha por fix, com o número que ele moveu. Fix sem ganho aparece como "sem ganho medido".
- O que não foi medido aparece escrito como não medido. "Deve melhorar" não é linha de tabela.
- Onde está no ar: URL e evidência (marcador ou bytes).

## Regras duras

1. Nenhum "otimizei" sem número antes e depois, da mesma ferramenta.
2. Leitura de código gera **hipótese**, não achado. Subagent que "achou 4 ganhos rápidos"
   achou 4 hipóteses.
3. Valide o instrumento contra um caso conhecido antes de confiar nele: rastreador de
   imports, script de soma, bench.
4. Um fix por vez. O que não mexeu no número sai do PR.
5. "tsc sem erros" sem `node_modules` é falso verde: o runner nem rodou. Sem instalar,
   prove pelo build remoto e por um render headless, e diga que foi assim.
6. Otimização só existe quando está nos bytes que o domínio serve.
7. Escala vertical (compute, plano) não é otimização. Avise o custo e diga que só compra tempo.
8. Fix que pode ter piorado outra métrica não sobe "honesto com os dois números": sobe
   quando o A/B intercalado mostra que não piorou. Prazo e "a doc recomenda" não são prova.
