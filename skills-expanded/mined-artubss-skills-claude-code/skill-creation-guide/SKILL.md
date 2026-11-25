---
name: skill-creation-guide
description: Guia para criar skills eficazes. Este skill deve ser usado quando usuários querem criar um novo skill (ou atualizar um existente) que estenda as capacidades do Claude com conhecimento especializado, workflows ou integrações de ferramentas.
license: Complete terms in LICENSE.txt
---

# Skill Creator

Este skill fornece orientação para criar skills eficazes.

## Sobre Skills

Skills são pacotes modulares e autossuficientes que estendem as capacidades do Claude fornecendo
conhecimento especializado, workflows e ferramentas. Pense neles como "guias de integração" para domínios
ou tarefas específicas—transformam o Claude de um agente de propósito geral em um agente especializado
equipado com conhecimento processual que nenhum modelo pode possuir completamente.

### O que Skills Fornecem

1. Workflows especializados - Procedimentos multi-etapa para domínios específicos
2. Integrações de ferramentas - Instruções para trabalhar com formatos de arquivo ou APIs específicas
3. Expertise de domínio - Conhecimento específico da empresa, schemas, lógica de negócio
4. Recursos agregados - Scripts, referências e assets para tarefas complexas e repetitivas

## Princípios Fundamentais

### Concisão é Fundamental

A janela de contexto é um bem público. Skills compartilham a janela de contexto com tudo mais que o Claude precisa: prompt do sistema, histórico de conversa, metadados de outros Skills, e a solicitação real do usuário.

**Suposição padrão: Claude já é muito inteligente.** Adicione apenas contexto que o Claude não possui. Questione cada informação: "Claude realmente precisa desta explicação?" e "Este parágrafo justifica seu custo em tokens?"

Prefira exemplos concisos a explicações verbosas.

### Defina Graus de Liberdade Apropriados

Corresponda o nível de especificidade à fragilidade e variabilidade da tarefa:

**Alta liberdade (instruções baseadas em texto)**: Use quando múltiplas abordagens são válidas, decisões dependem de contexto, ou heurísticas guiam a abordagem.

**Liberdade média (pseudocódigo ou scripts com parâmetros)**: Use quando um padrão preferido existe, alguma variação é aceitável, ou configuração afeta o comportamento.

**Baixa liberdade (scripts específicos, poucos parâmetros)**: Use quando operações são frágeis e propensas a erros, consistência é crítica, ou uma sequência específica deve ser seguida.

Pense no Claude explorando um caminho: uma ponte estreita com abismos precisa de guardrails específicos (baixa liberdade), enquanto um campo aberto permite muitos caminhos (alta liberdade).

### Anatomia de um Skill

Todo skill consiste em um arquivo SKILL.md obrigatório e recursos opcionais agregados:

```
skill-name/
├── SKILL.md (obrigatório)
│   ├── Frontmatter YAML (obrigatório)
│   │   ├── name: (obrigatório)
│   │   └── description: (obrigatório)
│   └── Instruções Markdown (obrigatório)
└── Recursos Agregados (opcional)
    ├── scripts/          - Código executável (Python/Bash/etc.)
    ├── references/       - Documentação destinada a ser carregada no contexto conforme necessário
    └── assets/           - Arquivos usados na saída (templates, ícones, fontes, etc.)
```

#### SKILL.md (obrigatório)

Todo SKILL.md consiste em:

- **Frontmatter** (YAML): Contém os campos `name` e `description`. Estes são os únicos campos que o Claude lê para determinar quando o skill é acionado, por isso é muito importante ser claro e abrangente ao descrever o que o skill é e quando deve ser usado.
- **Body** (Markdown): Instruções e orientação para usar o skill. Carregado apenas DEPOIS que o skill é acionado (se for).

#### Recursos Agregados (opcional)

##### Scripts (`scripts/`)

Código executável (Python/Bash/etc.) para tarefas que requerem confiabilidade determinística ou são repetidamente reescritas.

- **Quando incluir**: Quando o mesmo código está sendo reescrito repetidamente ou confiabilidade determinística é necessária
- **Exemplo**: `scripts/rotate_pdf.py` para tarefas de rotação de PDF
- **Benefícios**: Eficiente em tokens, determinístico, pode ser executado sem ser carregado no contexto
- **Nota**: Scripts ainda podem precisar ser lidos pelo Claude para patches ou ajustes específicos do ambiente

##### Referências (`references/`)

Documentação e material de referência destinados a serem carregados conforme necessário no contexto para informar o processo e pensamento do Claude.

- **Quando incluir**: Para documentação que o Claude deve consultar enquanto trabalha
- **Exemplos**: `references/finance.md` para schemas financeiros, `references/mnda.md` para template de NDA da empresa, `references/policies.md` para políticas da empresa, `references/api_docs.md` para especificações de API
- **Casos de uso**: Schemas de banco de dados, documentação de API, conhecimento de domínio, políticas da empresa, guias de workflow detalhados
- **Benefícios**: Mantém SKILL.md enxuto, carregado apenas quando o Claude determina ser necessário
- **Melhor prática**: Se arquivos são grandes (>10k palavras), inclua padrões de busca grep em SKILL.md
- **Evite duplicação**: Informações devem residir em SKILL.md ou arquivos de referência, não em ambos. Prefira arquivos de referência para informações detalhadas a menos que seja verdadeiramente central para o skill—isso mantém SKILL.md enxuto enquanto torna a informação descobrível sem ocupar a janela de contexto. Mantenha apenas instruções procedurais essenciais e orientação de workflow em SKILL.md; mova material de referência detalhado, schemas e exemplos para arquivos de referência.

##### Assets (`assets/`)

Arquivos não destinados a serem carregados no contexto, mas sim usados dentro da saída que o Claude produz.

- **Quando incluir**: Quando o skill precisa de arquivos que serão usados na saída final
- **Exemplos**: `assets/logo.png` para assets de marca, `assets/slides.pptx` para templates PowerPoint, `assets/frontend-template/` para boilerplate HTML/React, `assets/font.ttf` para tipografia
- **Casos de uso**: Templates, imagens, ícones, código boilerplate, fontes, documentos de exemplo que são copiados ou modificados
- **Benefícios**: Separa recursos de saída de documentação, permite que o Claude use arquivos sem carregá-los no contexto

#### O que Não Incluir em um Skill

Um skill deve conter apenas arquivos essenciais que suportam diretamente sua funcionalidade. NÃO crie documentação extraneous ou arquivos auxiliares, incluindo:

- README.md
- INSTALLATION_GUIDE.md
- QUICK_REFERENCE.md
- CHANGELOG.md
- etc.

O skill deve conter apenas as informações necessárias para um agente IA fazer o trabalho em questão. Não deve conter contexto auxiliar sobre o processo que foi realizado para criá-lo, procedimentos de configuração e teste, documentação voltada ao usuário, etc. Criar arquivos de documentação adicionais apenas adiciona desorganização e confusão.

### Princípio de Design de Divulgação Progressiva

Skills usam um sistema de carregamento em três níveis para gerenciar o contexto eficientemente:

1. **Metadados (name + description)** - Sempre no contexto (~100 palavras)
2. **Body do SKILL.md** - Quando skill é acionado (<5k palavras)
3. **Recursos agregados** - Conforme necessário pelo Claude (Ilimitado porque scripts podem ser executados sem serem lidos na janela de contexto)

#### Padrões de Divulgação Progressiva

Mantenha o body do SKILL.md ao essencial e abaixo de 500 linhas para minimizar inchaço de contexto. Divida o conteúdo em arquivos separados ao se aproximar desse limite. Ao dividir conteúdo em outros arquivos, é muito importante referenciá-los a partir do SKILL.md e descrever claramente quando lê-los, para garantir que o leitor do skill saiba que existem e quando usá-los.

**Princípio chave:** Quando um skill suporta múltiplas variações, frameworks ou opções, mantenha apenas o workflow principal e orientação de seleção em SKILL.md. Mova detalhes específicos de variantes (padrões, exemplos, configuração) em arquivos de referência separados.

**Padrão 1: Guia de alto nível com referências**

```markdown
# PDF Processing

## Quick start

Extract text with pdfplumber:
[code example]

## Advanced features

- **Form filling**: See [FORMS.md](FORMS.md) for complete guide
- **API reference**: See [REFERENCE.md](REFERENCE.md) for all methods
- **Examples**: See [EXAMPLES.md](EXAMPLES.md) for common patterns
```

O Claude carrega FORMS.md, REFERENCE.md ou EXAMPLES.md apenas quando necessário.

**Padrão 2: Organização específica de domínio**

Para Skills com múltiplos domínios, organize o conteúdo por domínio para evitar carregar contexto irrelevante:

```
bigquery-skill/
├── SKILL.md (overview and navigation)
└── reference/
    ├── finance.md (revenue, billing metrics)
    ├── sales.md (opportunities, pipeline)
    ├── product.md (API usage, features)
    └── marketing.md (campaigns, attribution)
```

Quando um usuário pergunta sobre métricas de vendas, o Claude lê apenas sales.md.

Similarmente, para skills que suportam múltiplos frameworks ou variantes, organize por variante:

```
cloud-deploy/
├── SKILL.md (workflow + provider selection)
└── references/
    ├── aws.md (AWS deployment patterns)
    ├── gcp.md (GCP deployment patterns)
    └── azure.md (Azure deployment patterns)
```

Quando o usuário escolhe AWS, o Claude lê apenas aws.md.

**Padrão 3: Detalhes condicionais**

Mostre conteúdo básico, link para conteúdo avançado:

```markdown
# DOCX Processing

## Creating documents

Use docx-js for new documents. See [DOCX-JS.md](DOCX-JS.md).

## Editing documents

For simple edits, modify the XML directly.

**For tracked changes**: See [REDLINING.md](REDLINING.md)
**For OOXML details**: See [OOXML.md](OOXML.md)
```

O Claude lê REDLINING.md ou OOXML.md apenas quando o usuário precisa desses recursos.

**Diretrizes importantes:**

- **Evite referências profundamente aninhadas** - Mantenha referências um nível acima de SKILL.md. Todos os arquivos de referência devem vincular diretamente de SKILL.md.
- **Estruture arquivos de referência mais longos** - Para arquivos mais longos que 100 linhas, inclua um índice no topo para que o Claude veja o escopo completo ao fazer a prévia.

## Processo de Criação de Skill

A criação de skill envolve estas etapas:

1. Compreender o skill com exemplos concretos
2. Planejar conteúdos reutilizáveis do skill (scripts, referências, assets)
3. Inicializar o skill (executar init_skill.py)
4. Editar o skill (implementar recursos e escrever SKILL.md)
5. Empacotar o skill (executar package_skill.py)
6. Iterar baseado em uso real

Siga estas etapas em ordem, pulando apenas se houver uma razão clara de porque não se aplicam.

### Etapa 1: Compreender o Skill com Exemplos Concretos

Pule esta etapa apenas quando os padrões de uso do skill já são claramente compreendidos. Permanece valiosa mesmo ao trabalhar com um skill existente.

Para criar um skill eficaz, compreenda claramente exemplos concretos de como o skill será usado. Esta compreensão pode vir de exemplos diretos do usuário ou exemplos gerados que são validados com feedback do usuário.

Por exemplo, ao construir um skill de editor de imagem, questões relevantes incluem:

- "Que funcionalidade o skill de editor de imagem deve suportar? Edição, rotação, algo mais?"
- "Você pode dar alguns exemplos de como este skill seria usado?"
- "Posso imaginar usuários pedindo coisas como 'Remove o olho vermelho desta imagem' ou 'Rotacione esta imagem'. Há outras formas que você imagina este skill sendo usado?"
- "O que um usuário diria que deveria acionar este skill?"

Para evitar sobrecarregar usuários, evite fazer muitas questões em uma única mensagem. Comece com as questões mais importantes e continue conforme necessário para melhor eficácia.

Conclua esta etapa quando houver uma compreensão clara da funcionalidade que o skill deve suportar.

### Etapa 2: Planejar os Conteúdos Reutilizáveis do Skill

Para transformar exemplos concretos em um skill eficaz, analise cada exemplo por:

1. Considerar como executar o exemplo do zero
2. Identificar que scripts, referências e assets seriam úteis ao executar estes workflows repetidamente

Exemplo: Ao construir um skill `pdf-editor` para lidar com solicitações como "Me ajude a rotacionar este PDF", a análise mostra:

1. Rotacionar um PDF requer reescrever o mesmo código cada vez
2. Um script `scripts/rotate_pdf.py` seria útil armazenar no skill

Exemplo: Ao projetar um skill `frontend-webapp-builder` para solicitações como "Construa um app de tarefas" ou "Construa um dashboard para rastrear meus passos", a análise mostra:

1. Escrever um webapp frontend requer o mesmo boilerplate HTML/React cada vez
2. Um template `assets/hello-world/` contendo os arquivos de projeto boilerplate HTML/React seria útil armazenar no skill

Exemplo: Ao construir um skill `big-query` para lidar com solicitações como "Quantos usuários fizeram login hoje?", a análise mostra:

1. Consultar BigQuery requer redescobrir os schemas de tabela e relacionamentos cada vez
2. Um arquivo `references/schema.md` documentando os schemas de tabela seria útil armazenar no skill

Para estabelecer os conteúdos do skill, analise cada exemplo concreto para criar uma lista dos recursos reutilizáveis a incluir: scripts, referências e assets.

### Etapa 3: Inicializar o Skill

Neste ponto, é hora de realmente criar o skill.

Pule esta etapa apenas se o skill sendo desenvolvido já existe, e iteração ou empacotamento é necessário. Neste caso, continue para a próxima etapa.

Ao criar um novo skill do zero, sempre execute o script `init_skill.py`. O script convenientemente gera um novo diretório de template de skill que inclui automaticamente tudo que um skill requer, tornando o processo de criação de skill muito mais eficiente e confiável.

Uso:

```bash
scripts/init_skill.py <skill-name> --path <output-directory>
```

O script:

- Cria o diretório do skill no caminho especificado
- Gera um template SKILL.md com frontmatter apropriado e placeholders TODO
- Cria diretórios de recurso de exemplo: `scripts/`, `references/`, e `assets/`
- Adiciona arquivos de exemplo em cada diretório que podem ser customizados ou deletados

Após inicialização, customize ou remova os arquivos SKILL.md gerados e arquivos de exemplo conforme necessário.

### Etapa 4: Editar o Skill

Ao editar o skill (recém-gerado ou existente), lembre-se que o skill está sendo criado para outra instância do Claude usar. Inclua informações que seriam benéficas e não-óbvias para o Claude. Considere que conhecimento processual, detalhes específicos de domínio, ou assets reutilizáveis ajudariam outra instância do Claude executar estas tarefas de forma mais eficaz.

#### Aprenda Padrões de Design Comprovados

Consulte estes guias úteis baseado nas necessidades do seu skill:

- **Processos multi-etapa**: Veja references/workflows.md para workflows sequenciais e lógica condicional
- **Formatos de saída específicos ou padrões de qualidade**: Veja references/output-patterns.md para padrões de template e exemplo

Estes arquivos contêm melhores práticas estabelecidas para design eficaz de skill.

#### Comece com Conteúdos Reutilizáveis do Skill

Para iniciar implementação, comece com os recursos reutilizáveis identificados acima: `scripts/`, `references/`, e arquivos `assets/`. Note que esta etapa pode requerer entrada do usuário. Por exemplo, ao implementar um skill `brand-guidelines`, o usuário pode precisar fornecer assets de marca ou templates para armazenar em `assets/`, ou documentação para armazenar em `references/`.

Scripts adicionados devem ser testados executando-os de fato para garantir que não há bugs e que a saída corresponde ao esperado. Se houver muitos scripts similares, apenas uma amostra representativa precisa ser testada para garantir confiança que todos funcionam enquanto balanceia tempo para conclusão.

Qualquer arquivo de exemplo e diretórios não necessários para o skill devem ser deletados. O script de inicialização cria arquivos de exemplo em `scripts/`, `references/`, e `assets/` para demonstrar estrutura, mas a maioria dos skills não precisará de todos eles.

#### Atualizar SKILL.md

**Diretrizes de Escrita:** Sempre use forma imperativa/infinitiva.

##### Frontmatter

Escreva o frontmatter YAML com `name` e `description`:

- `name`: O nome do skill
- `description`: Este é o mecanismo principal de acionamento do seu skill, e ajuda o Claude a compreender quando usar o skill.
  - Inclua tanto o que o Skill faz quanto triggers/contextos específicos para quando usá-lo.
  - Inclua toda informação "quando usar" aqui - Não no body. O body é carregado apenas após acionamento, então seções "Quando Usar Este Skill" no body não são úteis para o Claude.
  - Exemplo de descrição para um skill `docx`: "Comprehensive document creation, editing, and analysis with support for tracked changes, comments, formatting preservation, and text extraction. Use when Claude needs to work with professional documents (.docx files) for: (1) Creating new documents, (2) Modifying or editing content, (3) Working with tracked changes, (4) Adding comments, or any other document tasks"

Não inclua nenhum outro campo no frontmatter YAML.

##### Body

Escreva instruções para usar o skill e seus recursos agregados.

### Etapa 5: Empacotar um Skill

Uma vez que desenvolvimento do skill está completo, deve ser empacotado em um arquivo .skill distribuidível que é compartilhado com o usuário. O processo de empacotamento automaticamente valida o skill primeiro para garantir que atende todos os requisitos:

```bash
scripts/package_skill.py <path/to/skill-folder>
```

Especificação opcional de diretório de saída:

```bash
scripts/package_skill.py <path/to/skill-folder> ./dist
```

O script de empacotamento irá:

1. **Validar** o skill automaticamente, checando:

   - Formato de frontmatter YAML e campos obrigatórios
   - Convenções de nomenclatura de skill e estrutura de diretório
   - Completude e qualidade de descrição
   - Organização de arquivo e referências de recurso

2. **Empacotar** o skill se validação passar, criando um arquivo .skill nomeado de acordo com o skill (ex. `my-skill.skill`) que inclui todos os arquivos e mantém a estrutura de diretório apropriada para distribuição. O arquivo .skill é um arquivo zip com extensão .skill.

Se validação falha, o script reportará os erros e sairá sem criar um pacote. Corrija quaisquer erros de validação e execute o comando de empacotamento novamente.

### Etapa 6: Iterar

Após testar o skill, usuários podem solicitar melhorias. Frequentemente isso acontece logo após usar o skill, com contexto fresco de como o skill se saiu.

**Workflow de iteração:**

1. Use o skill em tarefas reais
2. Perceba dificuldades ou ineficiências
3. Identifique como SKILL.md ou recursos agregados devem ser atualizados
4. Implemente mudanças e teste novamente