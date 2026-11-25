---
name: software-architecture
description: Guia para arquitetura de software focada em qualidade. Esta skill deve ser usada quando usuários desejam escrever código, projetar arquitetura, analisar código, ou em qualquer caso que se relate ao desenvolvimento de software.
---

# Skill de Desenvolvimento de Arquitetura de Software

Esta skill fornece orientação para desenvolvimento de software e arquitetura focados em qualidade. É baseada em princípios de Clean Architecture e Domain Driven Design.

## Regras de Estilo de Código

### Princípios Gerais

- **Padrão de retorno antecipado**: Sempre use retornos antecipados quando possível, em vez de condições aninhadas, para melhor legibilidade
- Evite duplicação de código através da criação de funções e módulos reutilizáveis
- Decomponha componentes e funções longas (mais de 80 linhas de código) em múltiplos componentes e funções menores. Se não puderem ser usados em outro lugar, mantenha no mesmo arquivo. Mas se o arquivo tiver mais de 200 linhas de código, deve ser dividido em múltiplos arquivos.
- Use arrow functions em vez de declarações de função quando possível

### Melhores Práticas

#### Abordagem Orientada por Bibliotecas

- **SEMPRE procure por soluções existentes antes de escrever código personalizado**
  - Verifique npm para bibliotecas existentes que resolvem o problema
  - Avalie serviços/soluções SaaS existentes
  - Considere APIs de terceiros para funcionalidades comuns
- Use bibliotecas em vez de escrever seus próprios utils ou helpers. Por exemplo, use `cockatiel` em vez de escrever sua própria lógica de retry.
- **Quando código personalizado É justificado:**
  - Lógica de negócio específica única para o domínio
  - Caminhos críticos em performance com requisitos especiais
  - Quando dependências externas seriam excessivas
  - Código sensível à segurança que requer controle total
  - Quando soluções existentes não atendem aos requisitos após avaliação minuciosa

#### Arquitetura e Design

- **Princípios de Clean Architecture & DDD:**
  - Siga design orientado por domínio e linguagem ubíqua
  - Separe entidades de domínio de preocupações de infraestrutura
  - Mantenha lógica de negócio independente de frameworks
  - Defina casos de uso claramente e mantenha-os isolados
- **Convenções de Nomenclatura:**
  - **EVITE** nomes genéricos: `utils`, `helpers`, `common`, `shared`
  - **USE** nomes específicos do domínio: `OrderCalculator`, `UserAuthenticator`, `InvoiceGenerator`
  - Siga padrões de nomenclatura de bounded context
  - Cada módulo deve ter um propósito único e claro
- **Separação de Responsabilidades:**
  - NÃO misture lógica de negócio com componentes de UI
  - Mantenha consultas ao banco de dados fora dos controllers
  - Mantenha limites claros entre contextos
  - Garanta separação apropriada de responsabilidades

#### Anti-Patterns a Evitar

- **Síndrome de NIH (Not Invented Here):**
  - Não construa autenticação personalizada quando Auth0/Supabase existe
  - Não escreva gerenciamento de estado personalizado em vez de usar Redux/Zustand
  - Não crie validação de formulário personalizada em vez de usar bibliotecas estabelecidas
- **Escolhas Arquiteturais Pobres:**
  - Misturar lógica de negócio com componentes de UI
  - Consultas ao banco de dados diretamente em controllers
  - Falta de separação clara de responsabilidades
- **Anti-Patterns de Nomenclatura Genérica:**
  - `utils.js` com 50 funções não relacionadas
  - `helpers/misc.js` como depósito geral
  - `common/shared.js` com propósito pouco claro
- Lembre-se: Cada linha de código personalizado é um passivo que requer manutenção, testes e documentação

#### Qualidade de Código

- Manipulação apropriada de erros com typed catch blocks
- Divida lógica complexa em funções menores e reutilizáveis
- Evite aninhamento profundo (máximo 3 níveis)
- Mantenha funções focadas e com menos de 50 linhas quando possível
- Mantenha arquivos focados e com menos de 200 linhas de código quando possível