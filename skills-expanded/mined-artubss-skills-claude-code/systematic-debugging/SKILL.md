---
name: systematic-debugging
description: Use quando encontrar um bug, falha em teste ou comportamento inesperado, antes de propor correções
---

# Depuração Sistemática

## Visão Geral

Correções aleatórias desperdiçam tempo e criam novos bugs. Patches rápidos mascaram problemas subjacentes.

**Princípio central:** SEMPRE encontre a causa raiz antes de tentar correções. Correções de sintomas são fracasso.

**Violar a letra deste processo é violar o espírito da depuração.**

## A Lei de Ferro

```
SEM CORREÇÕES SEM INVESTIGAÇÃO DE CAUSA RAIZ PRIMEIRO
```

Se você não completou a Fase 1, não pode propor correções.

## Quando Usar

Use para QUALQUER problema técnico:
- Falhas em testes
- Bugs em produção
- Comportamento inesperado
- Problemas de desempenho
- Falhas de build
- Problemas de integração

**Use isto ESPECIALMENTE quando:**
- Sob pressão de tempo (emergências tornam adivinhações tentadoras)
- "Apenas uma correção rápida" parece óbvia
- Você já tentou múltiplas correções
- A correção anterior não funcionou
- Você não compreende completamente o problema

**Não pule quando:**
- O problema parece simples (bugs simples têm causas raiz também)
- Você está com pressa (pressa garante retrabalho)
- O gerente quer resolvido AGORA (sistemático é mais rápido que caos)

## As Quatro Fases

Você DEVE completar cada fase antes de prosseguir para a próxima.

### Fase 1: Investigação de Causa Raiz

**ANTES de tentar QUALQUER correção:**

1. **Leia Mensagens de Erro Com Cuidado**
   - Não pule erros ou avisos
   - Frequentemente contêm a solução exata
   - Leia stack traces completamente
   - Anote números de linha, caminhos de arquivo, códigos de erro

2. **Reproduza Consistentemente**
   - Você consegue disparar o erro confiabilmente?
   - Quais são os passos exatos?
   - Acontece toda vez?
   - Se não for reproduzível → colete mais dados, não adivinhe

3. **Verifique Mudanças Recentes**
   - O que mudou que poderia causar isto?
   - Git diff, commits recentes
   - Novas dependências, mudanças de config
   - Diferenças ambientais

4. **Colete Evidências em Sistemas Multi-Componentes**

   **QUANDO o sistema tem múltiplos componentes (CI → build → signing, API → service → database):**

   **ANTES de propor correções, adicione instrumentação diagnóstica:**
   ```
   Para CADA limite de componente:
     - Log dos dados que entram no componente
     - Log dos dados que saem do componente
     - Verifique propagação de ambiente/config
     - Verifique estado em cada camada

   Execute uma vez para coletar evidências mostrando ONDE quebra
   ENTÃO analise as evidências para identificar qual componente falha
   ENTÃO investigue esse componente específico
   ```

   **Exemplo (sistema multi-camada):**
   ```bash
   # Camada 1: Workflow
   echo "=== Secrets disponíveis no workflow: ==="
   echo "IDENTITY: ${IDENTITY:+SET}${IDENTITY:-UNSET}"

   # Camada 2: Build script
   echo "=== Env vars no build script: ==="
   env | grep IDENTITY || echo "IDENTITY not in environment"

   # Camada 3: Signing script
   echo "=== Keychain state: ==="
   security list-keychains
   security find-identity -v

   # Camada 4: Signing atual
   codesign --sign "$IDENTITY" --verbose=4 "$APP"
   ```

   **Isto revela:** Qual camada falha (secrets → workflow ✓, workflow → build ✗)

5. **Trace Data Flow**

   **QUANDO erro é profundo na call stack:**

   Veja `root-cause-tracing.md` neste diretório para a técnica completa de tracing reverso.

   **Versão rápida:**
   - De onde vem o valor ruim?
   - O que chamou isto com valor ruim?
   - Continue tracendo para cima até encontrar a fonte
   - Corrija na fonte, não no sintoma

### Fase 2: Análise de Padrão

**Encontre o padrão antes de corrigir:**

1. **Encontre Exemplos Funcionando**
   - Localize código similar funcionando no mesmo codebase
   - O que funciona similar ao que está quebrado?

2. **Compare Contra Referências**
   - Se implementando padrão, leia implementação de referência COMPLETAMENTE
   - Não escaneie - leia cada linha
   - Entenda o padrão completamente antes de aplicar

3. **Identifique Diferenças**
   - O que é diferente entre funcionando e quebrado?
   - Liste cada diferença, por menor que seja
   - Não assuma "aquilo não pode importar"

4. **Entenda Dependências**
   - Quais outros componentes isto precisa?
   - Quais settings, config, ambiente?
   - Quais suposições faz?

### Fase 3: Hipótese e Testes

**Método científico:**

1. **Forme Hipótese Única**
   - Declare claramente: "Acho que X é a causa raiz porque Y"
   - Escreva
   - Seja específico, não vago

2. **Teste Minimamente**
   - Faça a MENOR mudança possível para testar hipótese
   - Uma variável por vez
   - Não corrija múltiplas coisas de uma vez

3. **Verifique Antes de Continuar**
   - Funcionou? Sim → Fase 4
   - Não funcionou? Forme NOVA hipótese
   - NÃO adicione mais correções por cima

4. **Quando Não Souber**
   - Diga "Não entendo X"
   - Não fingi saber
   - Peça ajuda
   - Pesquise mais

### Fase 4: Implementação

**Corrija a causa raiz, não o sintoma:**

1. **Crie Caso de Teste Falhando**
   - Reprodução mais simples possível
   - Teste automatizado se possível
   - Script único se sem framework
   - DEVE ter antes de corrigir
   - Use o skill `superpowers:test-driven-development` para escrever testes falhando apropriadamente

2. **Implemente Correção Única**
   - Endereça a causa raiz identificada
   - UMA mudança por vez
   - Sem melhorias "enquanto estou aqui"
   - Sem refatoração bundled

3. **Verifique Correção**
   - Teste passa agora?
   - Nenhum outro teste quebrado?
   - Problema realmente resolvido?

4. **Se Correção Não Funcionar**
   - PARE
   - Conte: Quantas correções você já tentou?
   - Se < 3: Retorne à Fase 1, reanalise com novas informações
   - **Se ≥ 3: PARE e questione a arquitetura (passo 5 abaixo)**
   - NÃO tente Correção #4 sem discussão arquitetural

5. **Se 3+ Correções Falharam: Questione Arquitetura**

   **Padrão indicando problema arquitetural:**
   - Cada correção revela novo estado compartilhado/acoplamento/problema em lugar diferente
   - Correções requerem "refatoração massiva" para implementar
   - Cada correção cria novos sintomas em outro lugar

   **PARE e questione fundamentos:**
   - Este padrão é fundamentalmente correto?
   - Estamos "nos agarrando a isto por inércia pura"?
   - Devemos refatorar arquitetura vs. continuar corrigindo sintomas?

   **Discuta com seu parceiro humano antes de tentar mais correções**

   Isto NÃO é uma hipótese falhada - isto é uma arquitetura errada.

## Red Flags - PARE e Siga o Processo

Se pegar a si mesmo pensando:
- "Correção rápida por enquanto, investigue depois"
- "Apenas tente mudar X e veja se funciona"
- "Adicione múltiplas mudanças, execute testes"
- "Pule o teste, vou verificar manualmente"
- "Provavelmente é X, deixa eu corrigir"
- "Não entendo completamente mas isto pode funcionar"
- "Padrão diz X mas vou adaptar diferentemente"
- "Aqui estão os principais problemas: [lista correções sem investigação]"
- Propondo soluções antes de traçar data flow
- **"Uma tentativa de correção a mais" (quando já tentou 2+)**
- **Cada correção revela novo problema em lugar diferente**

**TODOS estes significam: PARE. Retorne à Fase 1.**

**Se 3+ correções falharam:** Questione a arquitetura (veja Fase 4.5)

## Sinais do seu Parceiro Humano que Você Está Fazendo Errado

**Fique atento a estas redirecionamentos:**
- "Isto não está acontecendo?" - Você assumiu sem verificar
- "Vai mostrar para nós...?" - Você deveria ter adicionado coleta de evidências
- "Pare de adivinhar" - Você está propondo correções sem entender
- "Ultrapense isto" - Questione fundamentos, não apenas sintomas
- "Estamos presos?" (frustrado) - Sua abordagem não está funcionando

**Quando vir estes:** PARE. Retorne à Fase 1.

## Racionalizações Comuns

| Desculpa | Realidade |
|----------|-----------|
| "Problema é simples, não precisa processo" | Problemas simples têm causas raiz também. Processo é rápido para bugs simples. |
| "Emergência, sem tempo para processo" | Depuração sistemática é MAIS RÁPIDA que thrashing de adivinhação. |
| "Apenas tente isto primeiro, depois investigue" | Primeira correção define o padrão. Faça certo desde o início. |
| "Vou escrever teste depois de confirmar correção" | Correções não testadas não fixam. Teste primeiro prova. |
| "Múltiplas correções de uma vez economiza tempo" | Não consegue isolar o que funcionou. Causa novos bugs. |
| "Referência muito longa, vou adaptar padrão" | Entendimento parcial garante bugs. Leia completamente. |
| "Vejo o problema, deixa eu corrigir" | Ver sintomas ≠ entender causa raiz. |
| "Uma tentativa de correção a mais" (após 2+ falhas) | 3+ falhas = problema arquitetural. Questione padrão, não corrija novamente. |

## Referência Rápida

| Fase | Atividades Chave | Critérios de Sucesso |
|------|------------------|----------------------|
| **1. Causa Raiz** | Leia erros, reproduza, verifique mudanças, colete evidências | Entenda O QUÊ e POR QUÊ |
| **2. Padrão** | Encontre exemplos funcionando, compare | Identifique diferenças |
| **3. Hipótese** | Forme teoria, teste minimamente | Confirmada ou nova hipótese |
| **4. Implementação** | Crie teste, corrija, verifique | Bug resolvido, testes passam |

## Quando Processo Revela "Sem Causa Raiz"

Se investigação sistemática revelar que o problema é verdadeiramente ambiental, dependente de timing, ou externo:

1. Você completou o processo
2. Documente o que investigou
3. Implemente tratamento apropriado (retry, timeout, mensagem de erro)
4. Adicione monitoramento/logging para investigação futura

**Mas:** 95% dos casos "sem causa raiz" são investigação incompleta.

## Técnicas de Apoio

Estas técnicas são parte da depuração sistemática e disponíveis neste diretório:

- **`root-cause-tracing.md`** - Trace bugs para trás através de call stack para encontrar trigger original
- **`defense-in-depth.md`** - Adicione validação em múltiplas camadas após encontrar causa raiz
- **`condition-based-waiting.md`** - Substitua timeouts arbitrários por condition polling

**Skills relacionadas:**
- **superpowers:test-driven-development** - Para criar caso de teste falhando (Fase 4, Passo 1)
- **superpowers:verification-before-completion** - Verifique que correção funcionou antes de reclamar sucesso

## Impacto Real

De sessões de depuração:
- Abordagem sistemática: 15-30 minutos para corrigir
- Abordagem random fixes: 2-3 horas de caos
- Taxa de correção primeira vez: 95% vs 40%
- Novos bugs introduzidos: Próximo de zero vs comum