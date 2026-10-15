---
name: use-case-pattern-builder
description: 'Criação de guia de novo conteúdo padrão de caso de uso para o repositório de blueprints do Adobe Experience Platform. Use essa habilidade ao adicionar um novo padrão de caso de uso, criar conteúdo de orientação de implementação ou quando o usuário mencionar adicionar padrões ao site de blueprints. Lida com o fluxo de trabalho completo: coleta de informações de padrão, geração do arquivo do Markdown com a estrutura de modelo correta e atualização de todas as páginas de referência cruzada (TOC.md, overview.md).'
source-git-commit: ed8928687806b619e95d8d320478d27c13722a80
workflow-type: tm+mt
source-wordcount: '1096'
ht-degree: 0%

---


# Construtor de padrões de caso de uso

Essa habilidade orienta a criação de um novo padrão de caso de uso para o repositório de blueprints da Adobe Experience Platform. Ele lida com o fluxo de trabalho completo: coleta de informações de padrão do usuário, geração do arquivo de conteúdo do Markdown com a estrutura de modelo correta e atualização de todas as páginas de referência cruzada para que o novo padrão seja detectável.

Antes de iniciar, leia os seguintes arquivos de referência para a estrutura completa do modelo e a lista de verificação de páginas a serem atualizadas:

- `references/pattern-template.md` — o modelo de marcação completa com valores de espaço reservado
- `references/pages-to-update.md` — a lista de verificação de páginas que devem ser atualizadas ao adicionar um padrão

## Fase 1: Coleta de informações

Entrevistar o usuário para coletar todas as informações necessárias antes de gerar quaisquer arquivos. Solicite o seguinte e não prossiga para a geração de conteúdo até que cada item seja fornecido ou explicitamente adiado.

### Informações necessárias

1. **Nome do padrão** — O título legível (por exemplo, &quot;Mensagens Acionadas por Eventos&quot;).

2. **Categoria** — Exatamente um dos seguintes:
   - `audience-building-activation`
   - `personalization`
   - `campaign-management-orchestration`
   - `analysis`
   - `conversational-experience`

3. **Descrição de recurso principal** — Uma frase única que descreve o que este padrão faz (usado na tabela de visão geral e na descrição do frontmatter).

4. **Soluções Adobe principais** — Os produtos Adobe são fundamentais para esse padrão. Escolha entre: Journey Optimizer, Real-Time Customer Data Platform, Experience Platform, Customer Journey Analytics, Brand Concierge, Journey Optimizer B2B edition, Real-Time CDP B2B edition ou outros, conforme apropriado.

5. **Etapas da cadeia de funções** — 3-6 fases sequenciais que descrevem o fluxo de execução do padrão, separadas por `>`. Exemplo: &quot;Assimilação de evento > Entrada de Jornada > Avaliação de condição > Entrega de mensagem > Relatórios&quot;.

6. **Objetivos de negócios com suporte** — Um ou mais objetivos de negócios do conjunto existente em `/help/blueprints/business-objectives/`. Cada deve incluir o nome do objetivo, a subpasta de categoria e o nome do arquivo. Verifique se os arquivos referenciados existem antes de gerar o conteúdo.

7. **Exemplo de casos de uso tático** — 6 a 10 cenários com marcadores que descrevem como esse padrão pode ser aplicado em diferentes contextos comerciais. Cada deve ter um nome de cenário em negrito seguido por uma descrição.

8. **KPIs** — Uma tabela com três colunas: KPI (nome), Descrição (o que ele mede), Medida (fórmula ou abordagem).

9. **Opções de implementação** — 2-4 opções de implementação. Para cada opção, colete:
   - Nome da opção
   - Recomendado para (quando usar esta opção)
   - Como funciona (2-4 parágrafos)
   - Considerações principais (lista com marcadores)
   - Vantagens (lista com marcadores)
   - Limitações (lista com marcadores)
   - Links do Experience League (URLs da documentação relevante)

### Opcional, mas recomendado

- Parágrafos de visão geral do caso de uso (3-5 parágrafos; se não forem fornecidos, faça um rascunho deles das outras informações)
- Lista de aplicativos com descrições da função de cada aplicativo Adobe
- Tabela de funções básicas (função, status, o que deve estar em vigor, referência do Experience League)
- Tabela de funções de suporte (Função, Status, Por que é importante, Referência do Experience League)
- Tabelas de funções de aplicativos (uma por aplicativo, com Função, Fase de implementação, Descrição)
- Lista de verificação de pré-requisitos

Se o usuário não fornecer os itens opcionais, gere padrões razoáveis com base na categoria do padrão, nas soluções e na cadeia de funções.

## Fase 2: geração de conteúdo

Gere o arquivo de marcação padrão no seguinte caminho:

```
/help/blueprints/use-case-patterns/{category}/{kebab-case-pattern-name}.md
```

O nome do arquivo deve usar letras maiúsculas e minúsculas derivadas do nome do padrão. Por exemplo, &quot;Mensagens acionadas por evento&quot; torna-se `event-triggered-messaging.md`.

Use o modelo de `references/pattern-template.md` e preencha todos os valores de espaço reservado com as informações coletadas. O arquivo gerado deve incluir cada seção no modelo:

1. **Interface do YAML** — título, descrição, solução (separada por vírgulas), exl-id (gerar um espaço reservado de UUID como `xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx` — a equipe de publicação atribuirá o real).

2. **Seção de abertura** — cabeçalho `# {Pattern name}` seguido de um parágrafo de introdução e a mensagem &quot;Use este guia para entender...&quot; sentença.

3. **Visão geral do caso de uso** — 3 a 5 parágrafos que descrevem o escopo do padrão, quando ele se aplica, o que ele faz ou não faz e quem são os participantes típicos.

4. **Principais objetivos de negócios** — cada objetivo como um cabeçalho vinculado com uma breve descrição e uma linha de resumo de KPIs.

5. **Exemplo de casos de uso tático** — Lista com marcadores de 6 a 10 cenários.

6. **Indicadores-chave de desempenho** — Tabela com KPI, Descrição, Colunas de medição.

7. **Padrão de caso de uso** — Parágrafo de descrição e a cadeia de funções.

8. **Aplicativos** — Lista de aplicativos do Adobe com formatação e descrições `[!DNL ...]`.

9. **Funções de base** — Tabela com colunas: função de base, status, o que deve estar em vigor, referência do Experience League. Valores de status: Obrigatório, Presumido no Local, Não Aplicável.

10. **Funções de suporte** — Tabela com colunas: função de suporte, status, por que é importante, referência do Experience League. Valores de status: recomendado, incluído, não aplicável.

11. **Funções do aplicativo** — Uma tabela por aplicativo com colunas: Função, Fase de Implementação, Descrição.

12. **Pré-requisitos** — Lista de verificação usando a sintaxe `- [ ]`.

13. **Opções de implementação** — 2 a 4 opções detalhadas, cada uma com Best for, How it works, Key considered, Advantages, Limitations e links do Experience League.

14. **Comparação de opções** — Tabela de comparação de resumo no final.

## Fase 3: Atualizações de referência cruzada

Após gerar o arquivo de padrão, atualize os arquivos a seguir. Leia `references/pages-to-update.md` para obter a lista de verificação detalhada.

### TOC.md

**Arquivo:** `/help/blueprints/TOC.md`

Adicione uma nova entrada na seção de categoria correta. As categorias são mapeadas para estas seções de índice:

| Lesma da categoria | Cabeçalho da seção do índice |
| --- | --- |
| `audience-building-activation` | `+ Audience Building & Activation{#audience-building-activation}` |
| `personalization` | `+ Personalization{#personalization-patterns}` |
| `campaign-management-orchestration` | `+ Campaign Management & Orchestration{#campaign-orchestration-patterns}` |
| `analysis` | `+ Analysis{#analysis-patterns}` |
| `conversational-experience` | `+ Conversational Experience{#conversational-experience-patterns}` |

O formato da entrada é:

```
    + [{{Pattern Title}}](/help/blueprints/use-case-patterns/{{category}}/{{filename}}.md)
```

Adicione a nova entrada após a última entrada existente na seção correspondente. Preservar o recuo exato (quatro espaços antes de `+`).

### Página de visão geral

**Arquivo:** `/help/blueprints/use-case-patterns/overview.md`

Adicione uma nova linha à tabela de categorias correta. O formato é:

```
| [{{Pattern Title}}]({{category}}/{{filename}}.md) | {{Primary capability description}} | [!DNL {{Solution1}}], [!DNL {{Solution2}}] |
```

Adicionar a nova linha após a última linha existente na tabela de categorias correspondente.

## Fase 4: validação

Depois que todos os arquivos forem criados e atualizados, verifique o seguinte:

1. **Links de objetivo comercial** — Cada link de objetivo comercial no arquivo padrão aponta para um arquivo existente em `/help/blueprints/business-objectives/`. Use glob ou read para confirmar se cada arquivo de destino existe.

2. **Posicionamento da entrada do sumário** — A nova entrada do sumário está dentro da seção de categoria correta e usa o formato de recuo e caminho corretos.

3. **Linha de tabela de visão geral** — A nova linha de visão geral está na tabela de categoria correta e segue o mesmo formato de coluna das linhas existentes.

4. **Nomeação do arquivo** — O nome de arquivo padrão usa kebab-case e corresponde ao caminho referenciado em TOC.md e overview.md.

5. **Integridade do Frontmatter** — O arquivo padrão inclui título, descrição, solução e exl-id no frontmatter do YAML.

6. **Links do Experience League** — Verifique se todas as URLs do Experience League são plausíveis (comece com `https://experienceleague.adobe.com/pt-br`).

Relate quaisquer falhas de validação ao usuário e corrija-as antes de considerar a tarefa como concluída.

## Notas

- Sempre use a sintaxe `[!DNL ...]` para nomes de produtos Adobe em tabelas e corpo de texto, seguindo a convenção de arquivos de padrão existentes.
- O `exl-id` no front-matter deve ser um UUID de espaço reservado. O pipeline de publicação atribui o valor real.
- Se o usuário quiser criar vários padrões de uma só vez, repita as Fases 2 a 4 para cada padrão, mas colete todas as informações na Fase 1.
- Se for necessária uma nova categoria que não exista na lista acima, avise o usuário de que o TOC.md e o overview.md precisarão da criação de novas seções e lidarão com isso como uma etapa separada.
