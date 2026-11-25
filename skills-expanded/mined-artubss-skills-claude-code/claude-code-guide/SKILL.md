---
name: Claude Code Guide
description: Guia completo para usar Claude Code de forma eficaz. Inclui templates de configuração, estratégias de prompting com keywords "Thinking", técnicas de debugging e melhores práticas para interagir com o agente.
---

# Claude Code Guide

## Propósito

Fornecer uma referência abrangente para configurar e usar Claude Code (a ferramenta de codificação agentic) em seu potencial máximo. Este skill sintetiza melhores práticas, templates de configuração e padrões avançados de uso.

## Configuração (`CLAUDE.md`)

Ao iniciar um novo projeto, crie um arquivo `CLAUDE.md` no diretório raiz para guiar o agente.

### Template (Geral)

```markdown
# Project Guidelines

## Commands

- Run app: `npm run dev`
- Test: `npm test`
- Build: `npm run build`

## Code Style

- Use TypeScript for all new code.
- Functional components with Hooks for React.
- Tailwind CSS for styling.
- Early returns for error handling.

## Workflow

- Read `README.md` first to understand project context.
- Before editing, read the file content.
- After editing, run tests to verify.
```

## Funcionalidades Avançadas

### Keywords de Thinking

Use estas palavras-chave em seus prompts para desencadear um raciocínio mais profundo do agente:

- "Think step-by-step"
- "Analyze the root cause"
- "Plan before executing"
- "Verify your assumptions"

### Debugging

Se o agente ficar travado ou tiver comportamento inesperado:

1. **Limpar Contexto**: Inicie uma nova sessão ou peça ao agente para "esquecer instruções anteriores" se estiver confuso.
2. **Instruções Explícitas**: Seja extremamente específico sobre paths, nomes de arquivos e resultados desejados.
3. **Logs**: Peça ao agente para "verificar os logs" ou "executar o comando com saída verbose".

## Melhores Práticas

1. **Contextos Pequenos**: Não coloque a base de código inteira no contexto. Use `grep` ou `find` para localizar arquivos relevantes primeiro.
2. **Desenvolvimento Iterativo**: Solicite pequenas mudanças, verifique, depois prossiga.
3. **Loop de Feedback**: Se o agente cometer um erro, corrija imediatamente e peça para "adicionar uma lição" à sua memória (se suportado) ou `CLAUDE.md`.

## Referência

Baseado em [Claude Code Guide by zebbern](https://github.com/zebbern/claude-code-guide).