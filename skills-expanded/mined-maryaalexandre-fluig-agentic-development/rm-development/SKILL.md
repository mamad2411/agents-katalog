---
name: rm-development
description: >
  Guia de desenvolvimento e troubleshooting para TOTVS RM com base nas fontes locais deste repositório.
  Cobre com mais força o RM Nucleus, especialmente movimento, parametrização, compras, estoque,
  contratos 2.0, workflow Fluig, TOTVS Colaboração, Fórmula Visual, IntelliTrace e o DataServer legado
  MOVMOVIMENTOTBCDATA. Use quando o usuário mencionar "TOTVS RM", "RM Nucleus", "tipo de movimento",
  "parametrização", "cotação", "estoque", "contrato 2.0", "workflow fluig", "Fórmula Visual",
  "IntelliTrace", "MOVMOVIMENTOTBCDATA", "ReadRecord", "SaveRecord", "ReadView" ou troubleshooting
  funcional e técnico sustentado pelas fontes locais.
---

# Diretrizes de Desenvolvimento RM

## Visão geral da plataforma

Esta skill cobre **TOTVS RM** em escopo amplo para descoberta, mas a cobertura factual forte das fontes locais está concentrada em **TOTVS Gestão de Estoque, Compras e Faturamento (RM Nucleus)**.

Dentro desse recorte, o acervo local sustenta principalmente:

- **Movimento e parametrização** — regras de tipo de movimento, etapas, validações, permissões e comportamento operacional
- **Cadastros** — produtos, séries, grade numerada, condição de pagamento, campos complementares e permissões associadas
- **Compras** — solicitação, cotação, quadro comparativo, ordem de compra, portal do fornecedor e processos correlatos
- **Estoque** — inventário, fechamento, custo médio, ficha física financeira, regeração de saldos e custos, consignação e industrialização
- **Contratos 2.0** — faturamento, previsão financeira, medição, aditivo, reajuste e cancelamentos
- **Integrações e automação** — Workflow Fluig, TOTVS Colaboração, Fórmula Visual, jobs, XML de processo, IntelliTrace e troubleshooting técnico
- **Legado técnico** — detalhamento local forte apenas para o DataServer `MOVMOVIMENTOTBCDATA`

Se a pergunta sair desse eixo, a resposta deve continuar útil, mas com limitação explícita.

---

## Regras de Escopo e Evidência

O paralelo aqui com o Fluig é simples: no Fluig a regra central é o Rhino/ECMA 5; no RM a regra central é **não extrapolar além das fontes locais**.

### Regras obrigatórias

- **SEMPRE** use apenas `totvs_rm_docs/` e `tmp_totvs_legado_single/` como base factual.
- **SEMPRE** diga explicitamente quando a resposta está no contexto de **RM Nucleus**.
- **SEMPRE** diferencie o que é **processo funcional**, **parametrização**, **integração**, **objeto gerencial** e **legado/DataServer**.
- **SEMPRE** priorize **menu, etapa, parâmetro, processo e dependência funcional** antes de citar tabela, XML ou DataServer.
- **SEMPRE** trate `MOVMOVIMENTOTBCDATA` como o único DataServer legado detalhado com segurança nesta skill.
- **NUNCA** generalize comportamento do Nucleus para todos os módulos do RM sem evidência local explícita.
- **NUNCA** invente endpoints, SDKs, wrappers, convenções técnicas ou regras universais não sustentadas pelas fontes.
- **NUNCA** trate nomes de DataServer observados em artigos de Fórmula Visual como documentação técnica completa.

### Como classificar a pergunta

Antes de responder, classifique o pedido em um destes blocos:

1. **Movimento e parametrização**
2. **Cadastros**
3. **Compras**
4. **Estoque**
5. **Contratos 2.0**
6. **Integrações e automação**
7. **Controle orçamentário e fiscal**
8. **Legado/DataServer**

### Formulações seguras

```text
Pelas fontes locais, eu consigo sustentar isso com segurança no contexto de RM Nucleus.
```

```text
No legado técnico desta base, a evidência detalhada está restrita ao DataServer MOVMOVIMENTOTBCDATA.
```

```text
Esse ponto extrapola o que as fontes locais mostram; eu consigo responder apenas a parte documentada neste acervo.
```

---

## Diretrizes de Movimento e Parametrização

Movimento e parametrização são o núcleo mais forte desta skill.

### Regras gerais

- Perguntas sobre movimento quase nunca devem ser respondidas sem identificar **tipo de movimento**, **classificação** e **etapa**.
- O caminho-base mais recorrente nas fontes é `Ambiente > Parâmetros > Gestão de Estoque, Compras e Faturamento`.
- Sempre valide se o comportamento depende de `Mov`, `Item`, `Fin`, `Fiscal`, `Estoque`, `Workflow`, `Workflow Fluig` ou integrações correlatas.
- Quando houver erro em movimento, verifique se o problema vem do **movimento em si** ou do **processo de origem**.

### Etapas e verificações recorrentes

As fontes sustentam checagens frequentes em etapas como:

- `Mov - Identificação`
- `Mov - Outros Dados`
- `Mov - Valores Financeiros`
- `Item - Identificação`
- `Item - Valores Financeiros`
- `Estoque - Estoque`
- `Compra/Venda - Características`
- `Compra/Venda - Outros Dados`
- `Fin - Condições de Pagamento`
- `Fin - Faturamento`
- `Workflow`
- `Workflow Fluig`

### Ordem recomendada de resposta

1. identificar o processo e o tipo de movimento
2. localizar o menu e a etapa correta
3. listar validações e dependências
4. só depois entrar em detalhe técnico

### Referências

- Referência principal: `references/nucleus-dominios.md`
- Referência complementar por artigos brutos: `references/movimento-e-parametrizacao-detalhada.md`

---

## Diretrizes de Cadastros

As fontes locais dão boa cobertura para cadastros que afetam diretamente o Nucleus.

### Escopos mais recorrentes

- produtos e serviços
- séries de movimentação
- grade numerada
- campos complementares
- condições de pagamento
- permissões por tipo de movimento
- dados fiscais do produto

### Regras práticas

- Em dúvidas de cadastro, confirme primeiro **qual cadastro** controla o comportamento do movimento.
- Se a pergunta envolver regra de movimento, não responda apenas pelo cadastro; conecte o cadastro à etapa de parâmetro relevante.
- Se a pergunta envolver produto, série ou grade numerada, valide se o reflexo aparece em movimento, estoque ou faturamento.

### Referências

- Referência principal: `references/nucleus-dominios.md`
- Referência complementar por artigos brutos: `references/cadastros-compras-estoque-contratos.md`

---

## Diretrizes de Compras

As fontes sustentam bem o fluxo operacional de compras no Nucleus.

### Fluxo de compras mais recorrente

1. **Solicitação de Compra**
2. **Cotação**
3. **Quadro Comparativo**
4. **Ordem de Compra**
5. movimento de compra/recebimento conforme parametrização

### Regras importantes

- Sempre confirme se a origem é **solicitação**, **cotação**, **orçamento** ou **ordem de compra**.
- Em dúvidas sobre geração de ordem, valide o tipo de movimento usado na geração.
- Em dúvidas de cotação, verifique julgamento, agrupamento, fornecedores, frete, moeda e quadro comparativo.
- Em problemas de portal do fornecedor, trate como fluxo de compras com componente de integração, não como problema puramente técnico.

### Referências

- Referência principal: `references/nucleus-dominios.md`
- Referência complementar por artigos brutos: `references/cadastros-compras-estoque-contratos.md`

---

## Diretrizes de Estoque

As fontes de estoque são fortemente orientadas a processo operacional e correção de inconsistência.

### Temas mais recorrentes

- inventário
- ficha física financeira
- fechamento de estoque
- regeração de saldos e custos
- custo médio
- saldo negativo
- lote, série e unidades de medida
- consignação
- industrialização

### Regras importantes

- Distinga sempre **inventário**, **fechamento** e **regeração**; as fontes tratam essas rotinas como coisas diferentes.
- Em problemas de saldo ou custo, valide primeiro data de fechamento, ficha física financeira e necessidade de regeração.
- Em processos especiais como consignação e industrialização, confirme qual é o papel da empresa no fluxo antes de orientar parametrização.

### Referências

- Referência principal: `references/nucleus-dominios.md`
- Referência complementar por artigos brutos: `references/cadastros-compras-estoque-contratos.md`

---

## Diretrizes de Contratos 2.0

A skill cobre Contratos 2.0 com foco em processos visíveis e regras práticas documentadas.

### Processos recorrentes

- faturar contrato
- cancelar faturamento
- gerar previsão financeira
- cancelar previsão financeira
- gerar medição
- cancelar medição
- gerar aditivo
- cancelar aditivo
- reajustar preço
- cancelar reajuste
- gerar abatimento ou acréscimo

### Regras importantes

- Sempre confirme o **tipo de faturamento**: periódico, não periódico ou medição.
- Se o movimento veio de contrato, não presuma correção direta no movimento; as fontes frequentemente mandam voltar ao contrato de origem.
- Em previsão financeira, valide tipo de documento, conta/caixa, moeda, classificação orçamentária/financeira e rateios.

### Referências

- Referência principal: `references/nucleus-dominios.md`
- Referência complementar por artigos brutos: `references/cadastros-compras-estoque-contratos.md`

---

## Diretrizes de Integrações e Automação

Este bloco equivale, em espírito, à seção de integrações da skill de Fluig: ele organiza Workflow Fluig, TOTVS Colaboração, Fórmula Visual, jobs e troubleshooting técnico.

### Integração com Fluig

Valide primeiro:

1. parâmetros globais
2. etapa `Workflow Fluig` do tipo de movimento
3. sincronização de usuário entre RM e Fluig
4. alias, host e autenticação quando houver erro técnico

Pontos recorrentes nas fontes:

- `Id da Empresa Centralizadora do Workflow do Fluig`
- `Usuário Padrão de Cancelamento`
- estados de aprovação
- sincronização de usuários
- `dsGetFormulaWf.js`
- alias `DefaultDB` em arquivos de host

### Integração com TOTVS Colaboração

Valide primeiro:

1. parâmetros de importação/envio de XML
2. ambiente em três camadas
3. host e compartilhamento de diretório
4. monitor de arquivos, jobs e status do XML
5. filial e parâmetros por filial

As fontes sustentam fortemente:

- `Monitor de Arquivos TOTVS Colaboração`
- XML de NF-e e CT-e
- importação automatizada
- status `Pendente`, `Inconsistente` e `Validado`
- dependência de diretório compartilhado e execução de jobs

### Fórmula Visual e objetos gerenciais

As fontes mostram Fórmula Visual como automação sobre processos existentes do sistema.

Sustentação local forte para:

- inclusão de movimento por atividades
- execução de processo via XML do job
- contexto de assinante
- consulta e atribuição de valores no contexto do movimento
- nomes de DataServer observados em formas diferentes de inclusão

### Referências

- Referência principal: `references/integracoes-e-objetos-gerenciais.md`
- Referência complementar por artigos brutos: `references/integracoes-backoffice-detalhadas.md`

---

## Diretrizes de Controle Orçamentário e Integração Fiscal

Esta seção não existia no RM inicial e precisava entrar para aproximar a organização da skill de Fluig: um bloco próprio para um domínio técnico-operacional relevante.

### Controle orçamentário

As fontes sustentam bem:

- classificação de período
- vínculo de natureza e centro de custo
- natureza orçamentária/financeira
- consulta de orçamento
- importação de orçamento
- regras de orçamento por tipo de movimento

### Integração fiscal

As fontes sustentam bem:

- escrituração de movimentos
- NFS-e
- erros de lote e apuração
- Bloco K
- parâmetros fiscais de integração
- menu e migração de processos de escrituração

### Regras importantes

- Separe orçamento, consulta/action, escrituração e obrigação fiscal antes de responder.
- Não confunda artigo fiscal do Nucleus com documentação universal de todo RM Fiscal.
- Quando houver `Action` ou `DataServer` citado em artigo de orçamento/fiscal, use isso como evidência local daquele processo específico.

### Referências

- Referência principal: `references/orcamento-e-integracao-fiscal.md`

---

## Diretrizes de DataServer Legado

Esta seção cumpre o papel do “bloco técnico duro” da skill, assim como Rhino/hAPI têm esse papel na skill de Fluig.

### Escopo disponível

A base legada local documenta somente:

- `MOVMOVIMENTOTBCDATA`

O que pode ser afirmado com segurança:

- `DataServerName`: `MOVMOVIMENTOTBCDATA`
- PK: `CODCOLIGADA;IDMOV`
- operações documentadas: `ReadRecord`, `SaveRecord`, `ReadView`
- envelope XML raiz: `MovMovimento`
- objetos centrais: `TMOV` e `TITMMOV`

### Regras importantes

- `TMOV` deve ser tratado como cabeçalho do movimento.
- `TITMMOV` representa itens do movimento.
- `ReadRecord` é leitura por PK e retorna XML do movimento.
- `ReadView` é mais adequado para filtro e listagem.
- `SaveRecord` trabalha sobre o XML inteiro do movimento.
- `Contexto`, `CODSISTEMA`, usuário, senha e endpoint variam nos exemplos; não fixe valores universais.

### Referência

- Referência principal: `references/movmovimentotbcdata.md`

---

## Diretrizes de Logging e Debug

O objetivo aqui é dar uma ordem estável de diagnóstico, como a skill de Fluig faz com logging e debug.

### Ordem recomendada de diagnóstico

1. classificar o erro como funcional, parametrização, integração ou legado
2. localizar a tela, rotina ou processo
3. identificar tipo de movimento, contrato, XML ou integração envolvida
4. revisar menu, etapa e escopo
5. revisar usuário, empresa, host, job, alias ou status
6. só então recorrer a XML, DataServer ou IntelliTrace

### Sinais recorrentes sustentados pelas fontes

- etapa errada do parâmetro
- estado de aprovação incorreto
- usuário não sincronizado
- processo de origem incorreto
- host, alias ou autenticação inconsistentes
- XML pendente ou inconsistente
- necessidade de rastreio com IntelliTrace

### Referências

- `references/integracoes-e-objetos-gerenciais.md`
- `references/integracoes-backoffice-detalhadas.md`
- `references/orcamento-e-integracao-fiscal.md`

---

## Estrutura Documental da Skill

Assim como a skill de Fluig organiza o conhecimento por blocos estáveis, a skill de RM deve usar as referências abaixo como “camadas”:

### Núcleo funcional

- `references/nucleus-dominios.md`
- `references/cadastros-compras-estoque-contratos.md`
- `references/movimento-e-parametrizacao-detalhada.md`

### Integrações e automação

- `references/integracoes-e-objetos-gerenciais.md`
- `references/integracoes-backoffice-detalhadas.md`

### Orçamento e fiscal

- `references/orcamento-e-integracao-fiscal.md`

### Escopo e navegação do acervo

- `references/fontes-e-limites.md`
- `references/mapa-backoffice-linha-rm.md`

### Legado técnico

- `references/movmovimentotbcdata.md`

---

## Snippets e Aceleradores de Desenvolvimento

### Delimitar escopo do RM

```text
Pelas fontes locais, eu trataria isso como RM Nucleus. Para outros módulos do RM, eu precisaria de documentação adicional para manter o mesmo nível de segurança.
```

### Enquadrar Workflow Fluig

```text
Neste acervo, a validação mais segura passa por parâmetros globais, etapa Workflow Fluig do tipo de movimento, estados de aprovação, sincronização de usuários e, em erro técnico, alias/host/autenticação.
```

### Enquadrar TOTVS Colaboração

```text
Pelas fontes locais, eu começaria por parâmetros de XML, ambiente em três camadas, diretório compartilhado, monitor de arquivos e jobs do TOTVS Colaboração antes de inferir problema no movimento.
```

### Enquadrar DataServer legado

```text
No legado técnico desta base, eu consigo detalhar apenas o MOVMOVIMENTOTBCDATA, com PK CODCOLIGADA;IDMOV e operações como ReadRecord, SaveRecord e ReadView.
```

### Enquadrar orçamento e fiscal

```text
Aqui eu separaria primeiro se o caso é orçamento, consulta/action, escrituração ou obrigação fiscal, porque as fontes locais tratam esses fluxos em trilhas diferentes.
```

---

## Exemplo Completo: Revisão de Movimento com Fluig e DataServer

### Visão geral

Pedido do usuário:

```text
Como revisar um tipo de movimento no RM, conferir por que a aprovação do Fluig não refletiu no RM e qual DataServer legado posso usar para ler o movimento?
```

### Resposta esperada

```text
Pelas fontes locais, eu trataria isso como RM Nucleus.

Primeiro revise o tipo de movimento e a etapa correta em Ambiente > Parâmetros > Gestão de Estoque, Compras e Faturamento, porque o comportamento costuma depender da combinação entre classificação, etapa do parâmetro e processo de origem.

Para o Workflow Fluig, as verificações mais seguras nesta base são: parâmetros globais, Id da Empresa Centralizadora, etapa Workflow Fluig do tipo de movimento, estados de aprovação e sincronização de usuários. Se houver erro técnico, vale revisar alias, host e autenticação conforme os artigos de integração.

Se a investigação precisar ir para o legado técnico, a evidência local detalhada aqui cobre apenas o DataServer MOVMOVIMENTOTBCDATA. Nele, a PK documentada é CODCOLIGADA;IDMOV, o envelope raiz é MovMovimento, TMOV representa o cabeçalho e TITMMOV representa os itens.
```

### Referências para esse cenário

- `references/movimento-e-parametrizacao-detalhada.md`
- `references/integracoes-backoffice-detalhadas.md`
- `references/movmovimentotbcdata.md`
- `references/fontes-e-limites.md`
