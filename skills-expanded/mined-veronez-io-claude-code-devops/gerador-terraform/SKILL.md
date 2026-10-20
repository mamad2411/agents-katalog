---
name: gerador-terraform
description: Gera a estrutura padrão de um projeto Terraform modularizado, ou audita um projeto existente e gera um relatório de conformidade. Use esta skill sempre que o usuário pedir para criar, gerar, organizar, padronizar ou revisar um projeto Terraform — mesmo que não use esses termos exatos. Também use quando o usuário mencionar "estrutura terraform", "configurar terraform", "montar terraform", "preparar infra com terraform", "iniciar projeto terraform", "projeto tf", ou qualquer variação que indique criação ou revisão de estrutura de projeto Terraform.
---

## O que esta skill faz

- **Projeto novo:** gera a estrutura de diretórios e arquivos padrão sem pedir confirmação, consultando a versão mais recente dos providers via Context7.
- **Projeto existente:** audita a conformidade com as regras abaixo e gera `terraform-audit.md` com os problemas encontrados. Nunca altera código existente.

Ao final, exibe um resumo das decisões tomadas.

---

## Detecção: novo ou existente?

Verifique se já existe um projeto Terraform no diretório atual:
- Se houver arquivos `.tf` ou diretórios `modules/` / `envs/` → **modo auditoria**
- Caso contrário → **modo geração**

---

## Regras obrigatórias

### 1. Ambientes flexíveis

Os ambientes são definidos pelo usuário no momento da execução — não há padrão fixo. Pode ser só `dev`, só `prod`, ou qualquer combinação. Pergunte quais ambientes criar antes de gerar (única pergunta permitida antes de executar).

### 2. Estrutura de diretórios

```
projeto/
├── modules/
│   └── <componente>/
│       ├── main.tf
│       ├── variables.tf
│       └── outputs.tf
├── envs/
│   └── <ambiente>/
│       ├── main.tf
│       ├── variables.tf
│       ├── outputs.tf
│       ├── terraform.tfvars
│       └── versions.tf
└── README.md
```

### 3. Contrato completo nos módulos

Todo módulo deve ter exatamente três arquivos: `main.tf`, `variables.tf` e `outputs.tf`. Sem esses três, o módulo não tem interface clara — o consumidor não sabe o que passa nem o que recebe. Nunca crie um módulo incompleto.

### 4. Providers sempre na versão mais recente via Context7

Antes de escrever qualquer bloco `required_providers` no `versions.tf`, consulte obrigatoriamente o Context7:

1. Use `mcp__context7__resolve-library-id` para encontrar o ID do provider (ex: `hashicorp/aws`, `hashicorp/google`, `hashicorp/kubernetes`)
2. Use `mcp__context7__query-docs` para obter a versão mais recente
3. Se o projeto usar múltiplos providers, consulte **cada um individualmente**

**Se o Context7 estiver indisponível:** pare e avise o usuário. Nunca invente ou assuma uma versão de provider.

### 5. Formato do versions.tf

```hcl
terraform {
  required_version = ">= 1.0"

  required_providers {
    <provider> = {
      source  = "<namespace>/<provider>"
      version = "~> <versão-consultada>"
    }
  }
}
```

Use `~>` para permitir patches, mas fixar minor version. Nunca use `latest` ou omita a versão.

### 6. Backend remoto fora do escopo

Não gere nem enforque configuração de backend. Se o usuário perguntar, informe que está fora do escopo desta skill.

---

## Modo geração (projeto novo)

1. **Pergunte os ambientes** que devem ser criados (única interação antes de executar)
2. **Identifique os providers** necessários a partir do contexto ou pergunte se não for possível inferir
3. **Consulte o Context7** para obter a versão mais recente de cada provider
4. **Gere a estrutura** completa conforme as regras acima
5. **Preencha os arquivos** com conteúdo mínimo funcional:
   - `main.tf` de módulo: bloco vazio com comentário indicando onde adicionar recursos
   - `variables.tf`: bloco vazio com comentário
   - `outputs.tf`: bloco vazio com comentário
   - `main.tf` de ambiente: chamada ao(s) módulo(s) com `source = "../../modules/<componente>"`
   - `terraform.tfvars`: variáveis de exemplo comentadas
   - `versions.tf`: bloco `terraform` com versão do provider consultada via Context7
   - `README.md`: nome do projeto, estrutura de diretórios, instrução de uso básica
6. **Exiba o resumo final**

---

## Modo auditoria (projeto existente)

Verifique e documente em `terraform-audit.md`:

| Verificação | O que checar |
|---|---|
| Estrutura de diretórios | Existência de `modules/` e `envs/` |
| Contrato dos módulos | Cada módulo tem `main.tf` + `variables.tf` + `outputs.tf` |
| `versions.tf` por ambiente | Existe em cada diretório dentro de `envs/` |
| Versões dos providers | Usam `~> x.y` (não `>= x` sem upper bound, não ausente) |
| `terraform.tfvars` por ambiente | Existe em cada diretório dentro de `envs/` |
| Ambientes isolados | Cada ambiente tem seu próprio diretório em `envs/` |

Formato do relatório:

```markdown
# Terraform Audit Report

**Data:** <data>
**Projeto:** <nome do diretório>

## Resumo

| Verificação | Status | Detalhes |
|---|---|---|
| Estrutura de diretórios | ✅ / ❌ | ... |
| Contrato dos módulos | ✅ / ❌ | ... |
| versions.tf por ambiente | ✅ / ❌ | ... |
| Versões dos providers | ✅ / ❌ | ... |
| terraform.tfvars por ambiente | ✅ / ❌ | ... |
| Ambientes isolados | ✅ / ❌ | ... |

## Problemas encontrados

### <problema 1>
- **Localização:** `<caminho>`
- **Problema:** <descrição>
- **Recomendação:** <o que fazer>

## Itens conformes

- <lista do que está correto>
```

Nunca altere arquivos existentes durante a auditoria.

---

## Resumo final (sempre exibir)

```
## Decisões aplicadas

| Regra | Situação | Ação |
|---|---|---|
| Modo de execução | [novo / existente] | [gerado / auditado] |
| Ambientes | [lista dos ambientes] | [criados / auditados] |
| Módulos | [lista dos módulos] | [criados / auditados] |
| Providers | [lista dos providers] | [versão consultada via Context7] |
| versions.tf | [presente em todos os ambientes?] | [ok / criado / problema reportado] |
| terraform.tfvars | [presente em todos os ambientes?] | [ok / criado / problema reportado] |
| Relatório de auditoria | [terraform-audit.md] | [gerado / n/a] |
```
