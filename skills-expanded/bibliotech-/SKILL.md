# Regras Específicas do Projeto Bibliotech

#aviso: apesar de colocar regras pra mensagem de commit, voce não deve dar commit, isso é só pra gerar a mensagem

## Sistema de Versionamento de Commits

### OBRIGATÓRIO: Incluir número da versão em TODOS os commits

TODOS os commits devem seguir o formato:
```
NUMERO_VERSAO - tipo: descrição em português
```

### Formato de Versionamento

- **Versão atual do projeto**: 0.1.0 (baseado no package.json)
- **Incremento automático**: Cada commit deve incrementar o último número (patch)
- **Exemplo de sequência**:
  - 0.1.0 - feat: adicionar sistema de login
  - 0.1.1 - fix: corrigir erro de validação no formulário
  - 0.1.2 - style: melhorar responsividade do dashboard
  - 0.1.3 - feat: implementar sistema de empréstimos

### Regras de Incremento de Versão

1. **Patch (0.1.X)**: Correções de bugs, ajustes de estilo, melhorias menores
2. **Minor (0.X.0)**: Novas funcionalidades, features significativas
3. **Major (X.0.0)**: Mudanças que quebram compatibilidade

### Instruções Especiais

- **Mudança manual de versão**: Se o usuário solicitar uma versão específica (ex: "1.3.0"), use exatamente essa versão
- **Próximo commit**: Após uma mudança manual, o próximo commit deve ser a versão subsequente (ex: 1.3.0 → 1.3.1)
- **Continuidade**: Sempre verificar o último commit para determinar a próxima versão
- **Histórico**: Manter sequência lógica de versionamento

### Exemplos Corretos

✅ `0.1.1 - feat: implementar dashboard do aluno`
✅ `0.1.2 - fix: corrigir erro de autenticação`
✅ `1.3.0 - feat: adicionar sistema de relatórios avançados`
✅ `1.3.1 - style: melhorar layout do dashboard`

### Exemplos Incorretos

❌ `feat: implementar dashboard do aluno` (sem versão)
❌ `0.1.1 - feat: implementar dashboard do aluno` (se a versão anterior foi 0.1.0)
❌ `0.1.0 - feat: implementar dashboard do aluno` (se já existe 0.1.0)

### Processo Obrigatório

1. **Antes de cada commit**: Verificar a versão do último commit
2. **Determinar próxima versão**: Incrementar patch por padrão
3. **Aplicar formato**: NUMERO_VERSAO - tipo: descrição
4. **Validar**: Confirmar que a versão é sequencial e lógica

### Casos Especiais

- **Primeiro commit**: Começar com 0.1.0
- **Reset de versão**: Se solicitado pelo usuário, usar a versão especificada
- **Múltiplos commits**: Cada um deve ter versão incremental
- **Hotfix**: Usar versão patch mesmo para correções críticas

### Tratamento de Inconsistências no Histórico

**PROBLEMA COMUM**: Commits sem número de versão no histórico

**SOLUÇÃO**: Quando encontrar commits sem versão no histórico, conte-os como se tivessem versão para manter a sequência lógica.

**Exemplo de Histórico com Inconsistência**:
```
1.2.1 - feat: implementar dashboard
descrição aleatória sem número
1.2.3 - fix: corrigir erro de login
```

**Como Proceder**:
- O commit "descrição aleatória sem número" deveria ser 1.2.2
- O próximo commit deve ser 1.2.4 (não 1.2.2)
- **SEMPRE**: Continuar a partir da última versão numérica encontrada

**Processo para Detectar Inconsistências**:
1. **Analisar histórico**: Ler os últimos commits para identificar padrões
2. **Identificar gaps**: Encontrar commits sem versão entre commits com versão
3. **Contar posições**: Cada commit sem versão ocupa uma posição na sequência
4. **Calcular próxima versão**: Usar a última versão numérica + número de commits sem versão + 1

**Exemplo Prático**:
```
Histórico encontrado:
1.2.1 - feat: implementar sistema
commit sem versão
commit sem versão  
1.2.4 - fix: corrigir bug

Próximo commit deve ser: 1.2.5
```

IMPORTANTE: Esta regra é OBRIGATÓRIA para todos os commits neste projeto. Nunca faça um commit sem incluir o número da versão no formato especificado.
