---
name: e2e-testing-patterns
description: "Crie suites de testes end-to-end confiáveis, rápidos e mantíveis que ofereçam segurança para fazer deploy de código rapidamente e capturem regressões antes que os usuários as encontrem."
risk: safe
source: community
date_added: "2026-02-27"
---

# Padrões de Testes E2E

Crie suites de testes end-to-end confiáveis, rápidos e mantíveis que ofereçam segurança para fazer deploy de código rapidamente e capturem regressões antes que os usuários as encontrem.

## Use esta skill quando

- Implementando automação de testes end-to-end
- Depurando testes instáveis ou não confiáveis
- Testando fluxos críticos de usuário
- Configurando pipelines de teste CI/CD
- Testando em múltiplos navegadores
- Validando requisitos de acessibilidade
- Testando designs responsivos
- Estabelecendo padrões de testes E2E

## Não use esta skill quando

- Você apenas precisa de testes unitários ou de integração
- O ambiente não consegue suportar automação UI estável
- Você não consegue provisionar contas de teste seguras ou dados

## Instruções

1. Identifique jornadas de usuário críticas e critérios de sucesso.
2. Construa seletores estáveis e estratégias de dados de teste.
3. Implemente testes com retentativas, rastreamento e isolamento.
4. Execute em CI com paralelização e captura de artefatos.

## Segurança

- Evite executar testes destrutivos contra produção.
- Use dados de teste dedicados e limpe saídas sensíveis.

## Recursos

- `resources/implementation-playbook.md` para padrões E2E detalhados e templates.