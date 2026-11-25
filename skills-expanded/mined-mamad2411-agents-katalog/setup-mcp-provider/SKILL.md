---
name: setup-mcp-PROVIDER
description: Configura o MCP oficial do PROVIDER. Coleta credenciais, gera uma especificação MCP portável e aplica no cliente escolhido pelo dev (Claude Code, Cursor, Gemini CLI, GitHub Copilot/VS Code ou outro cliente compatível).
---

# Skill: Setup MCP — PROVIDER

## Trigger
`/setup-mcp-PROVIDER` · "configurar mcp PROVIDER" · "setup PROVIDER mcp"

---

## Pré-requisitos

Listar pré-requisitos do MCP:
- [ ] [Pré-requisito 1 — ex: Node.js >= 20]
- [ ] [Pré-requisito 2 — ex: Docker]
- [ ] [Pré-requisito 3 — conta no serviço]

```bash
COMANDO_VERIFICACAO --version
```

---

## Processo

### Passo 1: Carregar Contexto do Projeto

Verificar se existe `.ai-project` para identificar o projeto ativo.
Extrair de `{slug}-map.json` os valores relevantes para pré-preencher a configuração:
- [Campo do {slug}-map.json relevante]

---

### Passo 2: Coletar Informações do Provider

Confirmar/solicitar os parâmetros de configuração do MCP.

Orientar criação de token/credenciais quando necessário:

```text
Você precisará de [tipo de credencial].

Acesse: [URL para criação]
[Instruções de escopos/permissões mínimas]

O token não deve ser salvo em arquivo versionável.
```

---

### Passo 3: Escolher Cliente MCP

Perguntar:

```text
Em qual cliente você quer configurar este MCP?

1. Claude Code
2. Cursor
3. Gemini CLI
4. GitHub Copilot / VS Code
5. Outro cliente MCP compatível
```

Usar `MCP/CLIENTS.md` como referência obrigatória para formatos, paths e comandos.

---

### Passo 4: Escolher Escopo

Perguntar o escopo conforme o cliente escolhido:

- Claude Code: `local`, `project` ou `user`
- Cursor: projeto (`.cursor/mcp.json`) ou global (`~/.cursor/mcp.json`)
- Gemini CLI: `project` ou `user`
- GitHub Copilot / VS Code: workspace (`.vscode/mcp.json`) ou user profile
- Outro: gerar instrução portável

Para qualquer escopo versionável, nunca inserir segredo real no arquivo.

---

### Passo 5: Gerar Especificação Portável

Gerar primeiro a especificação MCP portável:

```json
{
  "name": "PROVIDER-{slug}",
  "transport": "stdio",
  "command": "COMANDO",
  "args": ["ARGS"],
  "env": {}
}
```

Para HTTP, usar:

```json
{
  "name": "PROVIDER-{slug}",
  "transport": "http",
  "url": "https://example.com/mcp",
  "headers": {}
}
```

Exibir ao dev com segredos mascarados e pedir confirmação antes de aplicar.

---

### Passo 6: Aplicar no Cliente Escolhido

Aplicar seguindo `MCP/CLIENTS.md`:

- Se o cliente tem CLI de gerenciamento, preferir CLI quando ela preservar corretamente o escopo escolhido.
- Se for editar JSON, ler arquivo atual, fazer merge preservando outros servidores e gravar JSON válido.
- Se o servidor já existir, perguntar antes de sobrescrever.
- Se for configuração de projeto, verificar `.gitignore` quando houver risco de segredo.

---

### Passo 7: Verificar e Orientar Reinício

Executar a verificação adequada ao cliente:

- Claude Code: `claude mcp list` e `/mcp`
- Cursor: Settings > MCP ou `Available Tools` no Agent
- Gemini CLI: `gemini mcp list` e `/mcp`
- GitHub Copilot / VS Code: `MCP: List Servers`
- Outro: comando/documentação do cliente

Orientar reinício/reload do cliente quando necessário.

---

### Passo 8: Relatório Final

```text
MCP PROVIDER configurado.

Resumo:
  - Cliente: {cliente}
  - Escopo: {escopo}
  - Servidor: {name}
  - Transporte: {stdio|http|sse}
  - Local/Comando: {path ou comando usado}

Teste sugerido:
  - [prompt ou comando de teste]
```

---

## Troubleshooting

- **MCP não aparece:** verificar arquivo/escopo correto, recarregar cliente e listar servidores.
- **Erro de autenticação:** token expirado, conta errada ou permissões insuficientes.
- **Servidor stdio não conecta:** testar `{command} {args...}` manualmente.
- **Docker não conecta:** verificar `docker info`.
- **Node/npx não conecta:** verificar `node --version` e `npx --version`.

---

## Referências

- Guia de clientes: `MCP/CLIENTS.md`
- Pacote/servidor oficial: [URL]
- Documentação de autenticação: [URL]
