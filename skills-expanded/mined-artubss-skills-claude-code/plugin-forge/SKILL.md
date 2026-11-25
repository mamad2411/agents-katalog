---
name: plugin-forge
description: Criar e gerenciar plugins do Claude Code com estrutura adequada, manifestos e integração com marketplace. Use ao criar plugins para um marketplace, adicionar componentes de plugins (comandos, agentes, hooks), atualizar versões de plugins ou trabalhar com manifestos plugin.json/marketplace.json.
---

# CC Plugin Forge

## Propósito

Construir e gerenciar plugins do Claude Code com estrutura correta, manifestos e integração com marketplace. Inclui workflows, scripts de automação e documentação de referência.

## Quando Usar

- Criando novos plugins para um marketplace
- Adicionando/modificando componentes de plugins (comandos, skills, agentes, hooks)
- Atualizando versões de plugins
- Trabalhando com manifestos de plugin ou marketplace
- Configurando testes locais de plugin
- Publicando plugins

## Primeiros Passos

### Criar Novo Plugin

Use `create_plugin.py` para gerar a estrutura do plugin:

```bash
python scripts/create_plugin.py plugin-name \
  --marketplace-root /path/to/marketplace \
  --author-name "Your Name" \
  --author-email "your.email@example.com" \
  --description "Plugin description" \
  --keywords "keyword1,keyword2" \
  --category "productivity"
```

Isso automaticamente:

- Cria a estrutura de diretórios do plugin
- Gera manifesto `plugin.json`
- Cria template README
- Atualiza `marketplace.json`

### Atualizar Versão

Use `bump_version.py` para atualizar versões em ambos os manifestos:

```bash
python scripts/bump_version.py plugin-name major|minor|patch \
  --marketplace-root /path/to/marketplace
```

Versionamento semântico:

- **major**: Mudanças que quebram compatibilidade (1.0.0 → 2.0.0)
- **minor**: Novas funcionalidades, refatoração (1.0.0 → 1.1.0)
- **patch**: Correções de bugs, documentação (1.0.0 → 1.0.1)

## Workflow de Desenvolvimento

### 1. Criar Estrutura

Abordagem manual (se não usar script):

```bash
mkdir -p plugins/plugin-name/.claude-plugin
mkdir -p plugins/plugin-name/commands
mkdir -p plugins/plugin-name/skills
```

### 2. Manifesto do Plugin

Arquivo: `plugins/plugin-name/.claude-plugin/plugin.json`

```json
{
  "name": "plugin-name",
  "version": "0.1.0",
  "description": "Plugin description",
  "author": {
    "name": "Your Name",
    "email": "your.email@example.com"
  },
  "keywords": ["keyword1", "keyword2"]
}
```

### 3. Registrar no Marketplace

Atualize `.claude-plugin/marketplace.json`:

```json
{
  "name": "plugin-name",
  "source": "./plugins/plugin-name",
  "description": "Plugin description",
  "version": "0.1.0",
  "keywords": ["keyword1", "keyword2"],
  "category": "productivity"
}
```

### 4. Adicionar Componentes

Crie nos diretórios respectivos:

| Componente | Localização | Formato |
|-----------|----------|--------|
| Comandos | `commands/` | Markdown com frontmatter |
| Skills | `skills/<name>/` | Diretório com `SKILL.md` |
| Agentes | `agents/` | Definições em Markdown |
| Hooks | `hooks/hooks.json` | Manipuladores de eventos |
| Servidores MCP | `.mcp.json` | Integrações externas |

### 5. Testes Locais

```bash
# Adicionar marketplace
/plugin marketplace add /path/to/marketplace-root

# Instalar plugin
/plugin install plugin-name@marketplace-name

# Após mudanças: reinstalar
/plugin uninstall plugin-name@marketplace-name
/plugin install plugin-name@marketplace-name
```

## Padrões de Plugin

### Plugin de Framework

Para orientação específica de framework (React, Vue, etc.):

```
plugins/framework-name/
├── .claude-plugin/plugin.json
├── skills/
│   └── framework-name/
│       ├── SKILL.md
│       └── references/
├── commands/
│   └── prime/
│       ├── components.md
│       └── framework.md
└── README.md
```

### Plugin de Utilidade

Para ferramentas e comandos:

```
plugins/utility-name/
├── .claude-plugin/plugin.json
├── commands/
│   ├── action1.md
│   └── action2.md
└── README.md
```

### Plugin de Domínio

Para conhecimento específico de domínio:

```
plugins/domain-name/
├── .claude-plugin/plugin.json
├── skills/
│   └── domain-name/
│       ├── SKILL.md
│       ├── references/
│       └── scripts/
└── README.md
```

## Nomenclatura de Comandos

Namespace baseado em subdiretório com separador `:`:

- `commands/namespace/command.md` → `/namespace:command`
- `commands/simple.md` → `/simple`

Exemplos:

- `commands/prime/vue.md` → `/prime:vue`
- `commands/docs/generate.md` → `/docs:generate`

## Gerenciamento de Versão

**Importante:** Atualize a versão em AMBOS os locais:

1. `plugins/<name>/.claude-plugin/plugin.json`
2. `.claude-plugin/marketplace.json`

Use `bump_version.py` para automatizar.

## Commits Git

Use conventional commits:

```bash
git commit -m "feat: add new plugin"
git commit -m "fix: correct plugin manifest"
git commit -m "docs: update plugin README"
git commit -m "feat!: breaking change"
```

## Documentação de Referência

Documentação detalhada incluída:

| Referência | Conteúdo |
|-----------|---------|
| `references/plugin-structure.md` | Estrutura de diretórios, schema de manifesto, componentes |
| `references/marketplace-schema.md` | Formato de marketplace, entradas de plugin, distribuição |
| `references/workflows.md` | Workflows passo a passo, padrões, publicação |

### Scripts

| Script | Propósito |
|--------|---------|
| `scripts/create_plugin.py` | Scaffolding de novo plugin |
| `scripts/bump_version.py` | Atualizar versões |