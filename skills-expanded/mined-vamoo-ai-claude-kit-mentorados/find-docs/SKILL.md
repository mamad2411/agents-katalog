---
name: find-docs
description: >-
  Busca documentação oficial atualizada (API, config, exemplos) de lib/SDK/serviço
  via Context7 (ctx7). Use ANTES de escrever código com tecnologia externa, ao
  checar versão/breaking changes ou quando o modelo pode estar desatualizado.
  Gatilhos: dúvida de API/SDK/CLI, migração.
---

# Doc oficial pelo Context7

O kit fixa o `ctx7` na 0.5.13 e confere a versão, não a presença: um já instalado mais
velho (ou mais novo) é trocado pelo fixado. Sem instalar: `npx ctx7@0.5.13 <comando>`.

```bash
[ "$(ctx7 --version 2>/dev/null)" = "0.5.13" ] || npm install -g ctx7@0.5.13
ctx7 library nextjs "How to set up app router with middleware"   # ID /org/project e Versions
ctx7 docs /vercel/next.js "How to set up app router with middleware"
```

O `docs` falha sem ID com `/` na frente: o `library` vem antes, salvo se a pessoa deu o ID
(`/org/project` ou `/org/project/versão`). A query é a pergunta inteira ("hooks" devolve
resultado genérico) e nunca leva chave, senha, dado pessoal nem código proprietário.

Escolha o resultado pelo nome (exato primeiro), depois por `Code Snippets`, `Source
Reputation` e `Benchmark Score`, e diga qual ID usou. Nenhum serve: refaça a query. Só
pergunte à pessoa quando as leituras possíveis apontam para libs diferentes de verdade.
Versão dita pela pessoa: use o ID com versão da linha `Versions` (`/org/project/versão`).

## Projeto com `package.json`: a versão instalada escolhe o ID

Sem versão dita pela pessoa, a doc certa é a da versão que o projeto roda, não a última
indexada (`cookies()` virou async no Next 15; o Tailwind v4 trocou o config por `@theme`).
Antes do `ctx7 docs`:

1. Leia o campo `version` de `node_modules/<lib>/package.json` (abra o arquivo, não precisa
   de `jq`); sem `node_modules`, procure a lib no lockfile; sem os dois, use a faixa do
   `package.json`.
2. Na linha `Versions` do `ctx7 library`, escolha a mesma major, e dentro dela a minor mais
   próxima. A lista vem fora de ordem e mistura `canary` e `__branch__…`: ignore esses dois.
3. Diga qual ID usou. Sem versão da mesma major na lista, use o ID geral e avise que a doc é
   da última versão indexada, não da instalada.

## Teto e cota

Pare em 3 comandos por pergunta: a cota do Context7 é mensal. Não achou, use o melhor
resultado e diga o que a doc não cobriu. Erro de cota ("Monthly quota reached", "quota
exceeded"): avise a pessoa, sugira `ctx7 login` (ou `CONTEXT7_API_KEY`) para limite maior e,
se ela não quiser, responda do conhecimento do modelo dizendo que pode estar desatualizado.
Nunca caia no conhecimento do modelo calado.
