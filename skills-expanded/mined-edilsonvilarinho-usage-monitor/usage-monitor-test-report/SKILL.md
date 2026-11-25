---
name: usage-monitor-test-report
description: Run every usage-monitor test suite (Kotlin allTests + server vitest) with coverage and build an HTML report: counts, coverage per layer, failures, readiness gates. Use for "relatório de testes", "cobertura", "está seguro para PR/merge", before opening or merging a PR, or /usage-monitor-test-report.
---

# Usage Monitor — relatório de testes e cobertura

O dono do repositório delega o ciclo inteiro (código, PR, CI, merge) e precisa de uma medida, não de uma
impressão, de quanto a suíte protege o produto. Esta skill roda **todas** as suítes com cobertura e
escreve um relatório HTML no design system do app, mais um `report.json` para leitura por máquina.

O gerador **só lê** o que as suítes escreveram. Rodar a suíte é responsabilidade desta skill: o mesmo
script serve para Windows, Linux e para o artefato baixado do CI.

## 1. Rodar as suítes

Na raiz do repositório (ou da worktree). Não pare no primeiro vermelho: o relatório existe justamente
para mostrar a falha.

**Kotlin** (domínio, dados, view models, UI, terminal, arquitetura):

```bash
# Linux/macOS — `bash ./gradlew`, nunca `chmod +x`: o gradlew está no git sem o bit de execução
bash ./gradlew desktopTest --rerun -Pcoverage -PtestForks=4
bash ./gradlew koverXmlReport -Pcoverage
```

```bat
:: Windows
gradlew.bat desktopTest --rerun -Pcoverage -PtestForks=4
gradlew.bat koverXmlReport -Pcoverage
```

- `desktopTest`, e não `allTests`: no alvo único JVM os dois rodam a mesma suíte, mas `--rerun` só vale
  para a tarefa nomeada. Sem ele o build cache (`org.gradle.caching=true`) devolve XML de uma passada
  antiga e o relatório descreve outro código.
- `-PtestForks=4` só com `~/.skiko` já populado (ver CLAUDE.md). Cache frio: `-PtestForks=1`.
- Sem display (SSH, contêiner): prefixe `xvfb-run -a`. Parte dos testes consulta o `GraphicsEnvironment`.
- Medido em 2026-10-22, Linux, 16 processadores, 4 forks: ~55 s de suíte mais ~5 s de Kover.

**Servidor de time** (`server/`, vitest + supertest):

```bash
cd server && npm ci && npm run test:coverage
```

`test:coverage` escreve `test-results/junit.xml` e `coverage/coverage-summary.json` (v8 sobre `src/`).

## 2. Gerar o relatório

```bash
node .claude/skills/usage-monitor-test-report/scripts/build-test-report.mjs
```

- Saída: `build/test-report/index.html` e `build/test-report/report.json` (pasta ignorada pelo git).
- Imprime um resumo no console e **sai com 1** quando algum portão bloqueia (suíte não rodou, falha,
  regra de arquitetura quebrada). Quem automatiza decide pelo código de saída.
- Opções: `--root <repo>` (padrão: diretório atual) e `--out <pasta relativa>`.
- `--platform win32|linux|darwin` troca a plataforma do cabeçalho (padrão: a da máquina que gera).
- `--ci` só no CI: lá o `desktopTest` pode vir do build cache (`FROM-CACHE`) com o carimbo da execução
  original, e o portão "Resultado do código atual" deixa de comparar horário com o commit.
- **Todo run do CI em que a suíte do desktop roda já gera este relatório**: job `test-report` do
  `ci.yml`, com a suíte do Windows e a do servidor. O HTML fica no artefato `test-report` (14 dias) e
  os portões no resumo do run. Para ler o de um PR sem rodar nada:
  `gh run download <run-id> -n test-report -D build/test-report-ci`. Rodar localmente continua valendo
  antes do push, porque o CI só responde depois dele.

## 3. Mostrar e ler

1. Entregue o caminho absoluto do `index.html`; quando o usuário estiver em outro dispositivo, mande o
   arquivo com `SendUserFile`. Na resposta: veredito, totais, cobertura total/Kotlin/servidor e
   os portões que não estão `ok` — números do console, nunca de cabeça.
2. **Veredito** (faixa do topo): `Pronto` (todos os portões ok), `Atenção` (algum `warn`) ou `Bloqueia`
   (algum `crit`).
3. **Uso no fluxo automatizado:**
   - `Bloqueia` → não abrir PR nem fazer merge. Corrigir primeiro.
   - `Atenção` → pode seguir, mas a descrição do PR diz qual portão e por quê.
   - A seção **"O que a suíte não cobre"** vale sempre: mudança em host de janela, instalador ou
     integração externa precisa de verificação manual registrada no PR (CLAUDE.md, "CI e testes").
   - Cobertura de linhas tem **meta de 95%** por suíte e **catraca** (plano
     [`cobertura-95-execucao.md`](../../../docs/planos/cobertura-95-execucao.md)): o piso é
     `coverageLineFloorPercent` no `build.gradle.kts` (Kotlin, `koverVerify` no CI) e `thresholds.lines` no
     `server/vitest.config.ts`. Abaixo do piso o portão "Meta de cobertura" é `crit` e o CI reprova; entre o
     piso e a meta é `warn`. O piso só sobe, no mesmo commit dos testes que o elevam, para o valor medido
     arredondado para baixo. Arquivo novo que entra em "Arquivos sem cobertura" é lacuna do próprio PR.

## O que o relatório mede, e como

| Seção | Fonte | Regra |
|---|---|---|
| Testes por tipo | conteúdo do arquivo de teste | Compose = `runDesktopComposeUiTest`; HTTP simulado = `MockEngine`; integração local = arquivo temporário ou SQLite; arquitetura = pacote `architecture`; servidor `test/api` = supertest. O resto é unidade. A primeira regra que casa vence. |
| Testes por área | pacote da classe | `KOTLIN_AREAS` no script, em ordem fixa. |
| Cobertura por camada | `build/reports/kover/report.xml`, `server/coverage/coverage-summary.json` | Linhas, ramos e métodos; método do Kotlin somado pelas `<class>` (o `<sourcefile>` não traz o contador). |
| Faixas de cor | — | ≥ 80% `Saudável`, 60–80% `Atenção`, < 60% `Crítico`. São faixas de leitura, não portão. |
| Declarados × executados | contagem estática de `@Test` | Diferença vira `Atenção`: teste que existe e não rodou. |
| Resultado do código atual | `git log` × carimbo dos XML | XML anterior ao commit, ou árvore suja em `src/`/`server/`, vira `Atenção`. |
| Cobertura da mesma execução | mtime do relatório de cobertura × carimbo da suíte | Suíte vermelha pula o `koverXmlReport`; o XML antigo não pode passar por atual. |

## Regras

- **Visual pelo design system** ([`docs/design-system/`](../../../docs/design-system/), skill
  `usage-monitor-design`): os tokens entram inline, lidos do repositório a cada geração. Nenhuma cor,
  raio ou tamanho fora deles. Estado sempre com ponto **e** palavra. Números em pt-BR (vírgula decimal,
  espaço fino no milhar). Tema escuro primeiro, com seletor Sistema/Escuro/Claro.
- **Número que a ferramenta não deu não aparece.** Nada de estimar cobertura de arquivo sem medição nem
  somar ramos do v8 com ramos do Kover como se fossem a mesma unidade. A cobertura total soma só
  **linhas**, e o cartão diz de quais fontes.
- **Ordem determinística** em toda tabela: definição fixa ou desempate por caminho. Duas execuções
  iguais dão as mesmas linhas na mesma ordem; só tempos e carimbos mudam.
- Nova área, tipo ou ponto cego: altere a tabela no script (`KOTLIN_AREAS`, `KOTLIN_KINDS`,
  `KOTLIN_LAYERS`, `BLIND_SPOTS`), com a fonte da afirmação na linha de `BLIND_SPOTS`.
- Sem dependência npm no gerador (mesmo motivo de `tools/ci/test-summary.mjs`).
