---
name: gerador-workflow
description: Gera ou audita e corrige workflows do GitHub Actions seguindo boas práticas de versionamento, uso de actions oficiais e pinning de versões. Use esta skill sempre que o usuário pedir para criar, gerar, auditar, revisar, corrigir ou padronizar um workflow ou pipeline do GitHub Actions — mesmo que não use esses termos exatos. Também use quando o usuário mencionar "cria workflow", "gera workflow", "workflow do github actions", "cria pipeline", "audita workflow", "revisa workflow", "corrige workflow", "boas práticas no workflow", "padroniza workflow", "criar CI", "criar CD", "criar CI/CD", "pipeline de deploy", "pipeline de build", "automatizar build", "automatizar deploy", ou qualquer variação que indique configuração de automação com GitHub Actions.
---

## O que esta skill faz

Gera workflows GitHub Actions do zero ou audita e corrige arquivos existentes em `.github/workflows/`, aplicando as regras abaixo. No modo auditoria, exibe o diff completo das mudanças propostas e aguarda confirmação explícita antes de sobrescrever. No modo geração, escreve o arquivo diretamente. Ao final, exibe um resumo das decisões tomadas.

---

## Regras obrigatórias

### 1. Versionamento via `run_number`

- Se o workflow constrói uma imagem Docker ou define uma versão de release e **nenhuma outra estratégia de versionamento** está presente (ex: tag semver manual, git tag, variável de versão explícita), use `${{ github.run_number }}` como versão/tag.
- **Não sobrescreva** estratégias de versionamento já existentes no workflow.
- **Avise o usuário** sempre que usar `run_number`: esse valor é um inteiro crescente e não segue semver. Se o destino for um registry que exige semver (Docker Hub com contratos de versão, Helm chart), isso pode ser um problema.

### 2. Busca de actions via context7 antes de qualquer script manual

Para cada step identificado (novo ou existente como script manual), **consulte o context7 MCP** para verificar se existe uma action oficial equivalente:

- Use `mcp__context7__resolve-library-id` para encontrar o ID da action/biblioteca.
- Use `mcp__context7__query-docs` para obter documentação e versão mais recente.
- Se encontrar uma action oficial: use-a no lugar do script manual.
- Se não encontrar: mantenha o script manual e registre o motivo no resumo final.

O objetivo é evitar reinventar o que já existe. Scripts manuais têm custo de manutenção — actions oficiais são mantidas pelos próprios fornecedores.

### 3. Apenas actions de fornecedores oficiais

Use somente actions de organizações oficiais conhecidas:

- `actions/` — GitHub oficial
- `docker/` — Docker oficial
- `aws-actions/` — AWS oficial
- `google-github-actions/` — Google oficial
- `azure/` — Microsoft/Azure oficial
- `hashicorp/` — HashiCorp oficial

**Nunca use** actions de usuários individuais desconhecidos (ex: `algum-usuario/minha-action`). Se não houver action oficial para a tarefa, use script manual documentado.

### 4. Pinning de versão das actions

- Toda action deve ser pinada com ao menos a versão major: `uses: actions/checkout@v4`
- Prefira versão exata quando disponível via context7: `uses: actions/checkout@v4.2.0`
- **Proibido** usar `@main`, `@master` ou `@latest` — essas referências são mutáveis e representam risco de supply chain.

### 5. Scripts manuais são último recurso

Scripts inline (`run: |`) devem ser usados somente quando nenhuma action oficial equivalente for encontrada. Quando necessário, documente no resumo final qual action foi buscada e por que não foi utilizada.

---

## Processo de execução

### Fase 1 — Detecção de modo

Verifique se `.github/workflows/` contém arquivos `.yml` ou `.yaml`:

- **Sem arquivos existentes:** modo geração — crie o workflow do zero e escreva o arquivo diretamente.
- **Com arquivos existentes:** modo auditoria — leia todos os arquivos, identifique violações das regras acima, calcule as correções necessárias, exiba o diff e aguarde confirmação antes de sobrescrever.

### Fase 2 — Consulta ao context7

Para cada step (novo ou existente):

1. Identifique a intenção do step (ex: checkout, build Docker, push registry, deploy k8s).
2. Consulte o context7 MCP para encontrar a action oficial correspondente e sua versão mais recente.
3. Decida: usar action oficial ou manter/criar script manual com justificativa.

### Fase 3 — Geração ou correção

- **Modo geração:** escreva o arquivo `.github/workflows/<nome>.yml` diretamente.
- **Modo auditoria:** exiba o diff completo das mudanças propostas. Aguarde o usuário confirmar (`sim`, `pode aplicar`, ou similar) antes de sobrescrever os arquivos.

### Fase 4 — Resumo final

Sempre exiba a tabela de decisões ao final.

---

## Resumo final (sempre exibir)

```
## Decisões aplicadas

| Step | Decisão | Action utilizada | Motivo |
|---|---|---|---|
| [nome do step] | [action oficial / script manual / mantido] | [ex: actions/checkout@v4] | [encontrado via context7 / não encontrado / já estava correto] |
```

Se `run_number` foi utilizado como estratégia de versionamento, adicione ao final do resumo:

> ⚠️ **Versionamento:** `github.run_number` é um inteiro crescente e não segue semver. Se o destino exigir semver, defina uma estratégia de versionamento explícita.

---

## Escopo

Esta skill atua **apenas** em `.github/workflows/*.yml`. Não audita nem modifica `action.yml` de composite actions locais, scripts externos referenciados nos workflows, ou configurações de ambiente do repositório.
