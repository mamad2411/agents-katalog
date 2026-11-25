---
name: forge-curate
description: "Arbitra clusters de memória em lotes com decisão humana antes da curadoria semântica."
allowed-tools: Read, Bash, AskUserQuestion
disable-model-invocation: true
---

## Invocation policy

Esta skill é de **invocação HUMANA**. A arbitragem semântica é uma decisão destrutiva do
operador: recomendações são apenas advisory e nenhuma fusão pode ser aplicada sem o
veredito explícito de uma pessoa. O operador deve validar o preview antes de continuar.

O fluxo interativo **não roda em `/forge-auto`**: a regra de autonomia nunca pausa o loop
para abrir uma pergunta. O caminho suportado é `/forge-next` ou a invocação direta do
operador, por exemplo `/forge-curate --cwd .`.

## Args

Interprete `$ARGUMENTS`:

- `--cwd <dir>`: raiz do projeto; use `.` quando omitido.
- `--min-score <0..1>`: limiar opcional repassado ao inventário de clusters.
- `--apply`: aplica os vereditos do arquivo somente depois da arbitragem humana.
- `--arbitration <arquivo>`: arquivo JSON produzido no Step 5 e consumido no Step 6.
- `--yes`: usado somente quando a CLI exigir confirmação não-interativa, conforme o
  operador decidir; nunca substitui a decisão por lote abaixo.
- `--json`: solicita saída estruturada dos CLIs quando isso ajudar a registrar o preview.
- `--undo`: desfaz a última aplicação curatorial quando o operador solicitar explicitamente.
- `--help`: mostra o uso de cada comando.

Sem `--apply`, esta skill termina em preview. O arquivo de arbitragem é temporário ou
revisável e deve ficar dentro da raiz indicada por `--cwd`.

## Fluxo

### Step 1 — Bootstrap e escopo

1. Resolva `--cwd` e confirme que é um diretório acessível.
2. Leia apenas os artefatos necessários para esta operação. Não edite a skill
   `forge-sweep`, manifestos ou qualquer fragmento durante a preparação.
3. Se o projeto não estiver inicializado, pare e informe o caminho de inicialização.

### Step 2 — Inventário

Execute o inventário determinístico, sempre incluindo JSON:

```bash
node scripts/forge-memory-clusters.js --cwd . --json
```

Quando `--cwd` não for `.`, substitua o valor pelo diretório resolvido. Se necessário,
inclua `--min-score <valor>` no mesmo comando. Preserve o JSON retornado como a fonte
do preview; não reconstrua clusters à mão.

### Step 3 — Classificação e preview

1. Imprima o preview vindo de `forge-memory-clusters.js --json` antes de perguntar algo.
2. Mostre o veredito (`TARGETS`, `NO-TARGET`, `NO-PAIRS` ou `EMPTY-STORE`), o censo,
   cada cluster, seus itens e a recomendação advisory individual.
3. Para cada item, imprima a recomendação antes da pergunta correspondente. A pessoa
   pode discordar de qualquer recomendação.
4. Não transforme recomendação em mutação: neste ponto nada é aplicado e nenhum
   fragmento é escrito diretamente.

### Step 4 — Preparar os lotes

Use os `batches` do JSON, respeitando as constantes do produtor: cada popup contém no
máximo 3 clusters (`CLUSTERS_PER_BATCH`) e cada cluster contém no máximo 8 itens
(`ITEMS_PER_CLUSTER`). Se a fonte mudar esses limites, releia o JSON e ajuste o fluxo;
não redigite limites alternativos nesta skill.

Antes de cada popup, apresente o número do lote, os clusters, a recomendação de cada
item e o que será registrado para cada opção. Um lote vazio não abre pergunta.

### Step 5 — Perguntar uma vez por lote

Use **um `AskUserQuestion` por lote**, depois de imprimir todas as recomendações daquele
lote. Cada pergunta deve oferecer exatamente estas decisões conceituais:

- **aplicar recomendações do lote** — aceitar os vereditos advisory exibidos;
- **revisar um a um** — abrir a arbitragem item a item antes de registrar o lote;
- **cancelar** — abandonar o fluxo sem criar um arquivo aplicável.

As opções **“revisar um a um”** e **“cancelar”** devem aparecer em TODO lote, inclusive
quando o lote tiver um único cluster. Ao escolher revisão individual, confirme para cada
item `manter` ou `fundir-no-sobrevivente`, garantindo exatamente um sobrevivente por
cluster. Cancelamento encerra sem `--apply`.

### Step 6 — Escrever arbitragem e aplicar

Depois que todos os lotes forem decididos, escreva o JSON no arquivo de arbitragem.
Escrever esse arquivo de decisões é a única escrita desta skill; ela **nunca escreve
fragmento diretamente**. O formato precisa conter todos os clusters e todos os itens,
com `cluster_id`, `storage_key`, `mem_id` e `verdict`.

Exemplo mínimo válido (o `cluster_id` e os endereços devem vir do preview atual):

```json
{
  "clusters": [
    {
      "cluster_id": "M001::MEM001|M002::MEM002",
      "items": [
        { "storage_key": "M001", "mem_id": "MEM001", "verdict": "manter" },
        { "storage_key": "M002", "mem_id": "MEM002", "verdict": "fundir-no-sobrevivente" }
      ]
    }
  ]
}
```

Valide o arquivo contra o plano vivo antes de aplicar. A execução autorizada é:

```bash
node scripts/forge-sweep-curate.js --apply --arbitration <file>
```

Use `--cwd <dir>` quando a raiz não for o diretório atual. O comando re mede o plano,
confere a impressão digital e só então passa pela fronteira de escrita compartilhada.
Não contorne `forge-sweep-curate.js` com `rm`, `sed`, serializer local ou edição de
`.gsd/memory`.

### Step 7 — Relatório final e desfazer

Registre a saída do comando, incluindo o `journal id`, arquivos escritos, itens pulados
e o veredito aplicado. Informe ao operador que a operação pode ser desfeita com o comando
exato abaixo, após confirmação:

```bash
node scripts/forge-sweep-curate.js --undo --yes
```

Se nada foi aplicado, diga explicitamente “nenhuma mutação”. Se a CLI retornar erro de
plano obsoleto, não tente corrigir silenciosamente: refaça o inventário, mostre outro
preview e repita a arbitragem humana.

## Segurança operacional

Recomendações nunca são autorização. Não invente itens ausentes, não omita clusters,
não aceite dois sobreviventes e não aplique um JSON cuja forma o validador rejeite.
Mantenha a pergunta em pt-BR e descreva cancelamento como saída segura.

O arquivo de arbitragem pode ser removido pelo operador depois do relatório; isso não
desfaz uma aplicação já concluída. Para desfazer, use exclusivamente o `--undo` do CLI,
que consulta o journal e restaura somente o vault correspondente.
