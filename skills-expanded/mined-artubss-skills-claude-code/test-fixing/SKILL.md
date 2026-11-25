---
name: test-fixing
description: Execute testes e corrija sistematicamente todos os testes com falha usando agrupamento inteligente de erros. Use quando o usuário solicitar correção de testes, mencionar falhas de teste, executar suite de testes com falhas ou solicitar tornar os testes aprovados.
---

# Correção de Testes

Identifique e corrija sistematicamente todos os testes com falha usando estratégias de agrupamento inteligente.

## Quando Usar

- Solicita explicitamente correção de testes ("corrija estes testes", "faça os testes passar")
- Relata falhas de testes ("testes estão falhando", "suite de testes está quebrada")
- Completa implementação e quer testes passando
- Menciona falhas de CI/CD devido a testes

## Abordagem Sistemática

### 1. Execução Inicial de Testes

Execute `make test` para identificar todos os testes com falha.

Analise o resultado para:

- Número total de falhas
- Tipos e padrões de erro
- Arquivos/módulos afetados

### 2. Agrupamento Inteligente de Erros

Agrupe falhas similares por:

- **Tipo de erro**: ImportError, AttributeError, AssertionError, etc.
- **Arquivo/módulo**: Mesmo arquivo causando múltiplas falhas de testes
- **Causa raiz**: Dependências ausentes, mudanças de API, impactos de refatoração

Priorize grupos por:

- Número de testes afetados (maior impacto primeiro)
- Ordem de dependência (corrija infraestrutura antes de funcionalidade)

### 3. Processo de Correção Sistemática

Para cada grupo (começando com maior impacto):

1. **Identifique a causa raiz**

   - Leia o código relevante
   - Verifique mudanças recentes com `git diff`
   - Compreenda o padrão de erro

2. **Implemente a correção**

   - Use a ferramenta Edit para mudanças de código
   - Siga convenções do projeto (veja CLAUDE.md)
   - Faça alterações mínimas e focadas

3. **Verifique a correção**

   - Execute subset de testes para este grupo
   - Use marcadores pytest ou padrões de arquivo:
     ```bash
     uv run pytest tests/path/to/test_file.py -v
     uv run pytest -k "pattern" -v
     ```
   - Garanta que o grupo passa antes de prosseguir

4. **Mude para o próximo grupo**

### 4. Estratégia de Ordem de Correção

**Infraestrutura primeiro:**

- Erros de import
- Dependências ausentes
- Problemas de configuração

**Depois mudanças de API:**

- Mudanças de assinatura de função
- Reorganização de módulo
- Variáveis/funções renomeadas

**Finalmente, problemas de lógica:**

- Falhas de assertion
- Bugs de lógica de negócio
- Tratamento de casos extremos

### 5. Verificação Final

Após todas as correções de grupo:

- Execute suite completa de testes: `make test`
- Verifique ausência de regressões
- Confirme que cobertura de testes permanece intacta

## Melhores Práticas

- Corrija um grupo por vez
- Execute testes focados após cada correção
- Use `git diff` para compreender mudanças recentes
- Procure por padrões nas falhas
- Não mude para o próximo grupo até que o atual passe
- Mantenha mudanças mínimas e focadas

## Exemplo de Fluxo de Trabalho

Usuário: "Os testes estão falhando após meu refactor"

1. Execute `make test` → 15 falhas identificadas
2. Agrupe erros:
   - 8 ImportErrors (módulo renomeado)
   - 5 AttributeErrors (assinatura de função alterada)
   - 2 AssertionErrors (bugs de lógica)
3. Corrija ImportErrors primeiro → Execute subset → Verifique
4. Corrija AttributeErrors → Execute subset → Verifique
5. Corrija AssertionErrors → Execute subset → Verifique
6. Execute suite completa → Todos passam ✓