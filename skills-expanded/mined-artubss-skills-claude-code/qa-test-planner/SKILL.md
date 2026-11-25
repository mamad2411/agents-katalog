---
name: qa-test-planner
description: Gere planos de teste abrangentes, casos de teste manual, suítes de teste de regressão e relatórios de bugs para engenheiros de QA. Inclui integração Figma MCP para validação de design.
trigger: explicit
---

# Planejador de Testes QA

Uma habilidade abrangente para engenheiros de QA criar planos de teste, gerar casos de teste manual, construir suítes de teste de regressão, validar designs contra Figma e documentar bugs efetivamente.

> **Ativação:** Esta habilidade é acionada apenas quando explicitamente chamada por nome (por exemplo, `/qa-test-planner`, `qa-test-planner` ou `usar a habilidade qa-test-planner`).

---

## Início Rápido

**Criar um plano de teste:**
```
"Criar um plano de teste para a funcionalidade de autenticação de usuário"
```

**Gerar casos de teste:**
```
"Gerar casos de teste manual para o fluxo de checkout"
```

**Construir suíte de regressão:**
```
"Construir uma suíte de teste de regressão para o módulo de pagamento"
```

**Validar contra Figma:**
```
"Comparar a página de login contra o design Figma em [URL]"
```

**Criar relatório de bug:**
```
"Criar um relatório de bug para o problema de validação de formulário"
```

---

## Referência Rápida

| Tarefa | O que você recebe | Tempo |
|--------|-------------------|-------|
| Plano de Teste | Estratégia, escopo, cronograma, riscos | 10-15 min |
| Casos de Teste | Instruções passo a passo, resultados esperados | 5-10 min cada |
| Suíte de Regressão | Testes de fumaça, caminhos críticos, ordem de execução | 15-20 min |
| Validação Figma | Comparação design-implementação, lista de discrepâncias | 10-15 min |
| Relatório de Bug | Passos reproduzíveis, ambiente, evidências | 5 min |

---

## Como Funciona

```
Sua Solicitação
    │
    ▼
┌─────────────────────────────────────────────────────┐
│ 1. ANALISAR                                         │
│    • Analisar funcionalidade/requisito              │
│    • Identificar tipos de teste necessários         │
│    • Determinar escopo e prioridades                │
├─────────────────────────────────────────────────────┤
│ 2. GERAR                                            │
│    • Criar entregas estruturadas                    │
│    • Aplicar templates e melhores práticas          │
│    • Incluir casos extremos e variações             │
├─────────────────────────────────────────────────────┤
│ 3. VALIDAR                                          │
│    • Verificar completude                           │
│    • Verificar rastreabilidade                      │
│    • Garantir passos acionáveis                     │
└─────────────────────────────────────────────────────┘
    │
    ▼
Entrega QA Pronta
```

---

## Comandos

### Scripts Interativos

| Script | Propósito | Uso |
|--------|-----------|-----|
| `./scripts/generate_test_cases.sh` | Criar casos de teste interativamente | Prompts passo a passo |
| `./scripts/create_bug_report.sh` | Gerar relatórios de bug | Coleta de entrada guiada |

### Linguagem Natural

| Solicitação | Resultado |
|------------|-----------|
| "Criar plano de teste para {funcionalidade}" | Documento de plano de teste completo |
| "Gerar {N} casos de teste para {funcionalidade}" | Casos de teste numerados com passos |
| "Construir suíte de teste de fumaça" | Testes de caminho crítico |
| "Comparar com Figma em {URL}" | Checklist de validação visual |
| "Documentar bug: {descrição}" | Relatório de bug estruturado |

---

## Entregas Principais

### 1. Planos de Teste
- Escopo e objetivos do teste
- Abordagem e estratégia de teste
- Requisitos de ambiente
- Critérios de entrada/saída
- Avaliação de risco
- Timeline e marcos

### 2. Casos de Teste Manual
- Instruções passo a passo
- Resultados esperados vs. reais
- Pré-condições e setup
- Requisitos de dados de teste
- Prioridade e severidade

### 3. Suítes de Regressão
- Testes de fumaça (15-30 min)
- Regressão completa (2-4 horas)
- Regressão direcionada (30-60 min)
- Ordem de execução e dependências

### 4. Validação Figma
- Comparação componente por componente
- Verificações de espaçamento e tipografia
- Consistência de cor e visual
- Validação de estado interativo

### 5. Relatórios de Bug
- Passos de reprodução claros
- Detalhes do ambiente
- Evidência (screenshots, logs)
- Severidade e prioridade

---

## Padrões a Evitar

| Evite | Por Quê | Em Vez Disso |
|------|---------|-------------|
| Passos de teste vagos | Não é possível reproduzir | Ações específicas + resultados esperados |
| Pré-condições faltando | Testes falham inesperadamente | Documentar todos os requisitos de setup |
| Sem dados de teste | Testador bloqueado | Fornecer dados de amostra ou geração |
| Títulos genéricos de bug | Difícil rastrear | Específico: "[Funcionalidade] problema quando [ação]" |
| Pular casos extremos | Perder bugs críticos | Incluir valores limite, nulos |

---

## Checklist de Verificação

**Plano de Teste:**
- [ ] Escopo claramente definido (dentro/fora)
- [ ] Critérios de entrada/saída especificados
- [ ] Riscos identificados com mitigações
- [ ] Timeline realista

**Casos de Teste:**
- [ ] Cada passo tem resultado esperado
- [ ] Pré-condições documentadas
- [ ] Dados de teste disponíveis
- [ ] Prioridade atribuída

**Relatórios de Bug:**
- [ ] Passos reproduzíveis
- [ ] Ambiente documentado
- [ ] Screenshots/evidência anexados
- [ ] Severidade/prioridade definida

---

## Referências

- [Templates de Caso de Teste](references/test_case_templates.md) - Formatos padrão para todos os tipos de teste
- [Templates de Relatório de Bug](references/bug_report_templates.md) - Templates de documentação
- [Guia de Teste de Regressão](references/regression_testing.md) - Construção e execução de suíte
- [Guia de Validação Figma](references/figma_validation.md) - Validação design-implementação

---

<details>
<summary><strong>Aprofundamento: Estrutura de Caso de Teste</strong></summary>

### Formato Padrão de Caso de Teste

```markdown
## TC-001: [Título do Caso de Teste]

**Prioridade:** Alta | Média | Baixa
**Tipo:** Funcional | UI | Integração | Regressão
**Status:** Não Executado | Passou | Falhou | Bloqueado

### Objetivo
[O que estamos testando e por quê]

### Pré-condições
- [Requisito de setup 1]
- [Requisito de setup 2]
- [Dados de teste necessários]

### Passos do Teste
1. [Ação a realizar]
   **Esperado:** [O que deve acontecer]

2. [Ação a realizar]
   **Esperado:** [O que deve acontecer]

3. [Ação a realizar]
   **Esperado:** [O que deve acontecer]

### Dados de Teste
- Entrada: [Valores de dados de teste]
- Usuário: [Detalhes de conta de teste]
- Configuração: [Configurações de ambiente]

### Pós-condições
- [Estado do sistema após o teste]
- [Limpeza necessária]

### Notas
- [Casos extremos a considerar]
- [Casos de teste relacionados]
- [Problemas conhecidos]
```

### Tipos de Teste

| Tipo | Foco | Exemplo |
|------|------|---------|
| Funcional | Lógica de negócio | Login com credenciais válidas |
| UI/Visual | Aparência, layout | Botão corresponde ao design Figma |
| Integração | Interação de componentes | API retorna dados para frontend |
| Regressão | Funcionalidade existente | Funcionalidades anteriores ainda funcionam |
| Performance | Velocidade, capacidade de carga | Página carrega em menos de 3 segundos |
| Segurança | Vulnerabilidades | Injeção SQL prevenida |

</details>

<details>
<summary><strong>Aprofundamento: Template de Plano de Teste</strong></summary>

### Estrutura de Plano de Teste

```markdown
# Plano de Teste: [Nome da Funcionalidade/Release]

## Resumo Executivo
- Funcionalidade/produto sendo testado
- Objetivos de teste
- Riscos principais
- Visão geral da timeline

## Escopo de Teste

**Dentro do Escopo:**
- Funcionalidades a testar
- Tipos de teste (funcional, UI, performance)
- Plataformas e ambientes
- Fluxos de usuário e cenários

**Fora do Escopo:**
- Funcionalidades não sendo testadas
- Limitações conhecidas
- Integrações de terceiros (se aplicável)

## Estratégia de Teste

**Tipos de Teste:**
- Teste manual
- Teste exploratório
- Teste de regressão
- Teste de integração
- Teste de aceitação do usuário

**Abordagem de Teste:**
- Teste caixa-preta
- Teste positivo e negativo
- Análise de valor limite
- Particionamento de equivalência

## Ambiente de Teste
- Sistemas operacionais
- Navegadores e versões
- Dispositivos (celular, tablet, desktop)
- Requisitos de dados de teste
- Ambientes de backend/API

## Critérios de Entrada
- [ ] Requisitos documentados
- [ ] Designs finalizados
- [ ] Ambiente de teste pronto
- [ ] Dados de teste preparados
- [ ] Build implantado

## Critérios de Saída
- [ ] Todos os casos de teste de alta prioridade executados
- [ ] Taxa de aprovação de 90%+ dos casos de teste
- [ ] Todos os bugs críticos corrigidos
- [ ] Nenhum bug aberto de severidade alta
- [ ] Suíte de regressão aprovada

## Avaliação de Risco

| Risco | Probabilidade | Impacto | Mitigação |
|-------|---------------|---------|-----------|
| [Risco 1] | A/M/B | A/M/B | [Mitigação] |

## Entregas de Teste
- Documento de plano de teste
- Casos de teste
- Relatórios de execução de teste
- Relatórios de bug
- Relatório resumido de teste
```

</details>

<details>
<summary><strong>Aprofundamento: Relatório de Bug</strong></summary>

### Template de Relatório de Bug

```markdown
# BUG-[ID]: [Título claro e específico]

**Severidade:** Crítica | Alta | Média | Baixa
**Prioridade:** P0 | P1 | P2 | P3
**Tipo:** Funcional | UI | Performance | Segurança
**Status:** Aberto | Em Progresso | Corrigido | Fechado

## Ambiente
- **SO:** [Windows 11, macOS 14, etc.]
- **Navegador:** [Chrome 120, Firefox 121, etc.]
- **Dispositivo:** [Desktop, iPhone 15, etc.]
- **Build:** [Versão/commit]
- **URL:** [Página onde o bug ocorre]

## Descrição
[Descrição clara e concisa do problema]

## Passos para Reproduzir
1. [Passo específico]
2. [Passo específico]
3. [Passo específico]

## Comportamento Esperado
[O que deveria acontecer]

## Comportamento Atual
[O que realmente acontece]

## Evidência Visual
- Screenshot: [anexado]
- Vídeo: [link se aplicável]
- Erros do console: [colar erros]

## Impacto
- **Impacto do Usuário:** [Quantos usuários afetados]
- **Frequência:** [Sempre, Às vezes, Raramente]
- **Solução Alternativa:** [Se uma existir]

## Contexto Adicional
- Relacionado a: [Funcionalidade/ticket]
- Regressão: [Sim/Não]
- Design Figma: [Link se bug de UI]
```

### Definições de Severidade

| Nível | Critério | Exemplos |
|-------|----------|----------|
| **Crítica (P0)** | Crash do sistema, perda de dados, segurança | Pagamento falha, login quebrado |
| **Alta (P1)** | Funcionalidade principal quebrada, sem solução | Busca não funciona |
| **Média (P2)** | Funcionalidade parcial, existe solução | Filtro perdendo uma opção |
| **Baixa (P3)** | Cosmético, casos extremos raros | Typo, alinhamento menor |

</details>

<details>
<summary><strong>Aprofundamento: Integração Figma MCP</strong></summary>

### Workflow de Validação de Design

**Pré-requisitos:**
- Servidor Figma MCP configurado
- Acesso aos arquivos de design Figma
- URLs Figma para componentes/páginas

**Processo:**

1. **Obter Especificações de Design do Figma**
```
"Obter as especificações de botão do arquivo Figma [URL]"

Resposta inclui:
- Dimensões (largura, altura)
- Cores (fundo, texto, borda)
- Tipografia (fonte, tamanho, peso)
- Espaçamento (padding, margin)
- Border radius
- Estados (padrão, hover, ativo, desabilitado)
```

2. **Comparar Implementação**
```
TC: Validação Visual de Botão Primário
1. Inspecionar botão primário nas ferramentas de desenvolvedor
2. Comparar contra especificações Figma:
   - Dimensões: 120x40px
   - Border-radius: 8px
   - Cor de fundo: #0066FF
   - Fonte: 16px Médio #FFFFFF
3. Documentar discrepâncias
```

3. **Criar Bug se Houver Incompatibilidade**
```
BUG: Cor do botão primário não corresponde ao design
Severidade: Média
Esperado (Figma): #0066FF
Real (Implementação): #0052CC
Screenshot: [anexado]
Link Figma: [componente específico]
```

### O Que Validar

| Elemento | O Que Verificar | Ferramenta |
|----------|-----------------|------------|
| Cores | Valores hex exatos | Seletor de cor do navegador |
| Espaçamento | Padding/margin px | DevTools estilos computados |
| Tipografia | Fonte, tamanho, peso | Painel de fonte DevTools |
| Layout | Largura, altura, posição | Box model DevTools |
| Estados | Hover, ativo, foco | Interação manual |
| Responsivo | Comportamento em breakpoint | Modo de dispositivo DevTools |

### Exemplos de Consultas
```
"Obter especificações de botão do design Figma [URL]"
"Comparar implementação do menu de navegação contra design Figma"
"Extrair valores de espaçamento do layout do dashboard do Figma"
"Listar todos os tokens de cor usados no sistema de design Figma"
```

</details>

<details>
<summary><strong>Aprofundamento: Teste de Regressão</strong></summary>

### Estrutura de Suíte

| Tipo de Suíte | Duração | Frequência | Cobertura |
|---------------|---------|-----------|-----------|
| Fumaça | 15-30 min | Diariamente | Apenas caminhos críticos |
| Direcionada | 30-60 min | Por mudança | Áreas afetadas |
| Completa | 2-4 horas | Semanal/Release | Abrangente |
| Sanidade | 10-15 min | Após hotfix | Validação rápida |

### Construindo uma Suíte de Regressão

**Passo 1: Identificar Caminhos Críticos**
- O que os usuários NÃO conseguem viver sem?
- O que gera receita?
- O que trata dados sensíveis?
- O que é usado com mais frequência?

**Passo 2: Priorizar Casos de Teste**

| Prioridade | Descrição | Deve Executar |
|------------|-----------|---------------|
| P0 | Crítico para negócios, segurança | Sempre |
| P1 | Funcionalidades principais, fluxos comuns | Semanal+ |
| P2 | Funcionalidades menores, casos extremos | Releases |

**Passo 3: Ordem de Execução**
1. Fumaça primeiro - se falhar, parar e corrigir build
2. Testes P0 a seguir - devem passar antes de prosseguir
3. P1 depois P2 - rastrear todas as falhas
4. Exploratória - encontrar problemas inesperados

### Critérios de Aprovação/Reprovação

**APROVAÇÃO:**
- Todos os testes P0 aprovam
- 90%+ dos testes P1 aprovam
- Nenhum bug crítico aberto

**REPROVAÇÃO (Bloqueia Release):**
- Qualquer teste P0 falha
- Bug crítico descoberto
- Vulnerabilidade de segurança
- Cenário de perda de dados

**CONDICIONAL:**
- Falhas P1 com soluções alternativas
- Problemas conhecidos documentados
- Plano de correção em lugar

</details>

<details>
<summary><strong>Aprofundamento: Rastreamento de Execução de Teste</strong></summary>

### Template de Relatório de Execução de Teste

```markdown
# Execução de Teste: [Versão da Release]

**Data:** 2024-01-15
**Build:** v2.5.0-rc1
**Testador:** [Nome]
**Ambiente:** Staging

## Resumo
- Total de Casos de Teste: 150
- Executados: 145
- Aprovados: 130
- Falhados: 10
- Bloqueados: 5
- Não Executados: 5
- Taxa de Aprovação: 90%

## Casos de Teste por Prioridade

| Prioridade | Total | Aprovação | Falha | Bloqueado |
|------------|-------|-----------|-------|-----------|
| P0 (Crítico) | 25 | 23 | 2 | 0 |
| P1 (Alto) | 50 | 45 | 3 | 2 |
| P2 (Médio) | 50 | 45 | 3 | 2 |
| P3 (Baixo) | 25 | 17 | 2 | 1 |

## Falhas Críticas
- TC-045: Processamento de pagamento falha
  - Bug: BUG-234
  - Status: Aberto

## Testes Bloqueados
- TC-112: Widget do dashboard (endpoint da API inativo)

## Riscos
- 2 bugs críticos bloqueando release
- Integração de pagamento precisa de atenção

## Próximos Passos
- Reteste após correção de BUG-234
- Completar os 5 casos de teste restantes
- Executar regressão completa antes da aprovação final
```

### Rastreamento de Cobertura

```markdown
## Matriz de Cobertura

| Funcionalidade | Requisitos | Casos de Teste | Status | Lacunas |
|---|---|---|---|---|
| Login | 8 | 12 | Completo | Nenhuma |
| Checkout | 15 | 10 | Parcial | Erros de pagamento |
| Dashboard | 12 | 15 | Completo | Nenhuma |
```

</details>

<details>
<summary><strong>Workflow de Processo QA</strong></summary>

### Fase 1: Planejamento
- [ ] Revisar requisitos e designs
- [ ] Criar plano de teste
- [ ] Identificar cenários de teste
- [ ] Estimar esforço e timeline
- [ ] Configurar ambiente de teste

### Fase 2: Design de Teste
- [ ] Escrever casos de teste
- [ ] Revisar casos de teste com time
- [ ] Preparar dados de teste
- [ ] Construir suíte de regressão
- [ ] Obter acesso ao design Figma

### Fase 3: Execução
- [ ] Executar casos de teste
- [ ] Registrar bugs com passos claros
- [ ] Validar contra Figma (testes de UI)
- [ ] Rastrear progresso do teste
- [ ] Comunicar bloqueadores

### Fase 4: Relatório
- [ ] Compilar resultados de teste
- [ ] Analisar cobertura
- [ ] Documentar riscos
- [ ] Fornecer recomendação go/no-go
- [ ] Arquivar artefatos de teste

</details>

<details>
<summary><strong>Melhores Práticas</strong></summary>

### Escrita de Casos de Teste

**FAÇA:**
- Seja específico e inequívoco
- Inclua resultados esperados para cada passo
- Teste uma coisa por caso de teste
- Use convenções de nomenclatura consistentes
- Mantenha casos de teste fáceis de manter

**NÃO FAÇA:**
- Assuma conhecimento
- Faça casos de teste muito longos
- Pule pré-condições
- Esqueça casos extremos
- Deixe resultados esperados vagos

### Relatório de Bug

**FAÇA:**
- Forneça passos claros de reprodução
- Inclua screenshots/vídeos
- Especifique detalhes exatos do ambiente
- Descreva impacto nos usuários
- Vincule a Figma para bugs de UI

**NÃO FAÇA:**
- Relate sem passos de reprodução
- Use descrições vagas
- Pule detalhes do ambiente
- Esqueça de atribuir prioridade
- Duplique bugs existentes

### Teste de Regressão

**FAÇA:**
- Automatize testes repetitivos quando possível
- Mantenha suíte de regressão regularmente
- Priorize caminhos críticos
- Execute testes de fumaça frequentemente
- Atualize suíte após cada release

**NÃO FAÇA:**
- Pule regressão antes de releases
- Deixe suíte desatualizada
- Teste tudo toda vez
- Ignore testes de regressão falhados

</details>

---

## Exemplos

<details>
<summary><strong>Exemplo: Caso de Teste de Fluxo de Login</strong></summary>

```markdown
## TC-LOGIN-001: Login de Usuário Válido

**Prioridade:** P0 (Crítica)
**Tipo:** Funcional
**Tempo Estimado:** 2 minutos

### Objetivo
Verificar que usuários conseguem fazer login com sucesso com credenciais válidas

### Pré-condições
- Conta de usuário existe (teste@exemplo.com / Teste123!)
- Usuário ainda não está logado
- Cookies do navegador limpos

### Passos do Teste
1. Navegar para https://app.exemplo.com/login
   **Esperado:** Página de login exibe com campos de email e senha

2. Inserir email: teste@exemplo.com
   **Esperado:** Campo de email aceita entrada

3. Inserir senha: Teste123!
   **Esperado:** Campo de senha mostra caracteres mascarados

4. Clicar no botão "Login"
   **Esperado:**
   - Indicador de carregamento aparece
   - Usuário redirecionado para /dashboard
   - Mensagem de boas-vindas mostrada: "Bem-vindo de volta, Usuário Teste"
   - Avatar/imagem de perfil exibida no header

### Pós-condições
- Sessão de usuário criada
- Token de autenticação armazenado
- Evento de analytics registrado

### Casos Extremos a Considerar
- TC-LOGIN-002: Senha inválida
- TC-LOGIN-003: Email inexistente
- TC-LOGIN-004: Tentativa de injeção SQL
- TC-LOGIN-005: Senha muito longa
```

</details>

<details>
<summary><strong>Exemplo: Caso de Teste de Design Responsivo</strong></summary>

```markdown
## TC-UI-045: Menu de Navegação Mobile

**Prioridade:** P1 (Alta)
**Tipo:** UI/Responsivo
**Dispositivos:** Mobile (iPhone, Android)

### Objetivo
Verificar que menu de navegação funciona corretamente em dispositivos mobile

### Pré-condições
- Acesso em dispositivo mobile ou modo responsivo
- Largura de viewport: 375px (iPhone SE) a 428px (iPhone Pro Max)

### Passos do Teste
1. Abrir homepage em dispositivo mobile
   **Esperado:** Ícone de menu hamburger visível (canto superior direito)

2. Tocar no ícone hamburger
   **Esperado:**
   - Menu desliza de dentro para fora pela direita
   - Overlay aparece sobre o conteúdo
   - Botão fechar (X) visível

3. Tocar no item de menu
   **Esperado:** Navega para a seção, menu fecha

4. Comparar contra design mobile Figma [link]
   **Esperado:**
   - Largura do menu: 280px
   - Animação de deslize: 300ms ease-out
   - Opacidade do overlay: 0,5, cor #000000
   - Tamanho da fonte: 16px, line-height 24px

### Breakpoints a Testar
- 375px (iPhone SE)
- 390px (iPhone 14)
- 428px (iPhone 14 Pro Max)
- 360px (Galaxy S21)
```

</details>

---

**"Testes mostram a presença, não a ausência de bugs." - Edsger Dijkstra**

**"Qualidade não é um ato, é um hábito." - Aristóteles**