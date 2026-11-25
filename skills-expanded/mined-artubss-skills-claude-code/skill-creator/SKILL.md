---
name: skill-creator
description: Crie novas skills, modifique e melhore skills existentes e meça o desempenho delas. Use quando usuários querem criar uma skill do zero, editar ou otimizar uma skill existente, executar avaliações para testar uma skill, fazer benchmark de desempenho com análise de variância, ou otimizar a descrição da skill para melhor precisão de disparo.
---

# Skill Creator

Uma skill para criar novas skills e melhorá-las iterativamente.

Em alto nível, o processo de criar uma skill funciona assim:

- Decida o que você quer que a skill faça e aproximadamente como ela deve fazer
- Escreva um rascunho da skill
- Crie alguns prompts de teste e execute claude-com-acesso-à-skill neles
- Ajude o usuário a avaliar os resultados tanto qualitativamente quanto quantitativamente
  - Enquanto as execuções acontecem em segundo plano, crie algumas avaliações quantitativas se não existirem (se existirem, você pode usar como está ou modificar se sentir que algo precisa mudar). Depois explique para o usuário (ou se já existirem, explique as que já existem)
  - Use o script `eval-viewer/generate_review.py` para mostrar os resultados ao usuário, e também deixe-o consultar as métricas quantitativas
- Reescreva a skill com base no feedback da avaliação dos resultados pelo usuário (e também se houver falhas óbvias que se tornem aparentes nos benchmarks quantitativos)
- Repita até estar satisfeito
- Expanda o conjunto de testes e tente novamente em escala maior

Seu trabalho ao usar esta skill é descobrir em que estágio do processo o usuário está e então intervir e ajudá-lo a avançar por essas etapas. Por exemplo, talvez ele diga "Quero fazer uma skill para X". Você pode ajudar a refinar o que ele quer dizer, escrever um rascunho, escrever os casos de teste, descobrir como ele quer avaliar, executar todos os prompts e repetir.

Por outro lado, talvez ele já tenha um rascunho da skill. Nesse caso, você pode ir direto para a parte de avaliação/iteração do loop.

É claro que você deve ser sempre flexível e se o usuário disser "Não preciso executar um monte de avaliações, só conversa mesmo", você pode fazer isso em vez disso.

Depois que a skill estiver pronta (mas novamente, a ordem é flexível), você também pode executar a skill de melhoria de descrição, que temos um script separado para isso, para otimizar o disparo da skill.

Legal? Legal.

## Comunicando com o usuário

A skill creator provavelmente será usada por pessoas com uma ampla gama de familiaridade com jargão técnico. Se você ainda não ouviu falar (e como poderia, é só muito recentemente que começou), há uma tendência agora em que o poder do Claude está inspirando encanadores a abrirem seus terminais, pais e avós a buscarem "como instalar npm". Por outro lado, a maioria dos usuários provavelmente é bastante letrada em computador.

Então, por favor, preste atenção a pistas de contexto para entender como formular sua comunicação! No caso padrão, só para dar uma ideia:

- "avaliação" e "benchmark" são borderline, mas OK
- para "JSON" e "assertion" você quer ver sinais sérios do usuário de que ele sabe o que essas coisas são antes de usá-las sem explicar

Tudo bem explicar termos brevemente se estiver em dúvida, e sinta-se à vontade para esclarecer termos com uma definição curta se não tiver certeza se o usuário vai entender.

---

## Criando uma skill

### Capturar Intenção

Comece entendendo a intenção do usuário. A conversa atual pode já conter um workflow que o usuário quer capturar (por exemplo, ele diz "transformar isso em uma skill"). Se for o caso, extraia as respostas do histórico de conversa primeiro — as ferramentas usadas, a sequência de etapas, correções que o usuário fez, formatos de entrada/saída observados. O usuário pode precisar preencher as lacunas e deve confirmar antes de prosseguir para a próxima etapa.

1. O que essa skill deve permitir que Claude faça?
2. Quando essa skill deve disparar? (que frases/contextos do usuário)
3. Qual é o formato de saída esperado?
4. Devemos configurar casos de teste para verificar se a skill funciona? Skills com saídas objetivamente verificáveis (transformação de arquivo, extração de dados, geração de código, etapas de workflow fixo) se beneficiam de casos de teste. Skills com saídas subjetivas (estilo de escrita, arte) geralmente não precisam deles. Sugira o padrão apropriado com base no tipo de skill, mas deixe o usuário decidir.

### Entrevista e Pesquisa

Faça perguntas proativas sobre casos extremos, formatos de entrada/saída, arquivos de exemplo, critérios de sucesso e dependências. Espere para escrever prompts de teste até ter essa parte resolvida.

Verifique MCPs disponíveis — se forem úteis para pesquisa (pesquisar documentação, encontrar skills similares, consultar boas práticas), pesquise em paralelo via subagentos se disponíveis, caso contrário inline. Venha preparado com contexto para reduzir o ônus no usuário.

### Escreva o SKILL.md

Com base na entrevista do usuário, preencha estes componentes:

- **name**: Identificador da skill
- **description**: Quando disparar, o que ela faz. Este é o mecanismo de disparo primário — inclua tanto o que a skill faz QUANTO contextos específicos para quando usá-la. Todas as informações de "quando usar" vão aqui, não no corpo. Nota: atualmente Claude tem tendência a "subdisparar" skills — a não usá-las quando seriam úteis. Para combater isso, por favor, faça as descrições das skills um pouco mais "insistentes". Por exemplo, em vez de "Como construir um dashboard simples e rápido para exibir dados internos do Anthropic.", você poderia escrever "Como construir um dashboard simples e rápido para exibir dados internos do Anthropic. Certifique-se de usar essa skill sempre que o usuário mencionar dashboards, visualização de dados, métricas internas, ou quiser exibir qualquer tipo de dado da empresa, mesmo que não peça explicitamente por um 'dashboard'."
- **compatibility**: Ferramentas necessárias, dependências (opcional, raramente necessário)
- **o resto da skill :)**

### Guia de Escrita de Skill

#### Anatomia de uma Skill

```
nome-da-skill/
├── SKILL.md (obrigatório)
│   ├── YAML frontmatter (name, description obrigatórios)
│   └── Instruções Markdown
└── Recursos Agrupados (opcional)
    ├── scripts/    - Código executável para tarefas determinísticas/repetitivas
    ├── references/ - Documentos carregados no contexto conforme necessário
    └── assets/     - Arquivos usados na saída (templates, ícones, fontes)
```

#### Divulgação Progressiva

Skills usam um sistema de carregamento em três níveis:
1. **Metadados** (name + description) - Sempre no contexto (~100 palavras)
2. **Corpo do SKILL.md** - No contexto sempre que a skill dispara (<500 linhas ideal)
3. **Recursos agrupados** - Conforme necessário (ilimitado, scripts podem executar sem carregar)

Essas contagens de palavras são aproximadas e você pode ficar à vontade para ir mais longe se necessário.

**Padrões-chave:**
- Mantenha SKILL.md abaixo de 500 linhas; se estiver se aproximando desse limite, adicione uma camada adicional de hierarquia junto com apontadores claros sobre onde o modelo usando a skill deve ir a seguir
- Referencie arquivos claramente do SKILL.md com orientação sobre quando lê-los
- Para arquivos de referência grandes (>300 linhas), inclua um índice

**Organização de domínio**: Quando uma skill suporta múltiplos domínios/frameworks, organize por variante:
```
cloud-deploy/
├── SKILL.md (workflow + seleção)
└── references/
    ├── aws.md
    ├── gcp.md
    └── azure.md
```
Claude lê apenas o arquivo de referência relevante.

#### Princípio da Falta de Surpresa

Isso dispensa dizer, mas skills não devem conter malware, código de exploração, ou qualquer conteúdo que pudesse comprometer a segurança do sistema. O conteúdo de uma skill não deve surpreender o usuário em sua intenção se descrito. Não vá com pedidos para criar skills enganosas ou skills projetadas para facilitar acesso não autorizado, exfiltração de dados, ou outras atividades maliciosas. Coisas como "simular o papel de um XYZ" estão OK.

#### Padrões de Escrita

Prefira usar a forma imperativa nas instruções.

**Definindo formatos de saída** - Você pode fazer assim:
```markdown
## Estrutura do relatório
SEMPRE use este template exato:
# [Título]
## Resumo executivo
## Principais descobertas
## Recomendações
```

**Padrão de exemplos** - É útil incluir exemplos. Você pode formatá-los assim (mas se "Input" e "Output" estão nos exemplos, você pode querer desviar um pouco):
```markdown
## Formato de mensagem de commit
**Exemplo 1:**
Input: Added user authentication with JWT tokens
Output: feat(auth): implement JWT-based authentication
```

### Estilo de Escrita

Tente explicar ao modelo por que as coisas são importantes em vez de usar linguagem pesada e imperiosa. Use teoria da mente e tente tornar a skill geral e não super-restrita a exemplos específicos. Comece escrevendo um rascunho e depois releia-o com olhos frescos e melhore-o.

### Casos de Teste

Após escrever o rascunho da skill, crie 2-3 prompts de teste realistas — o tipo de coisa que um usuário real realmente diria. Compartilhe-os com o usuário: [você não precisa usar exatamente essa linguagem] "Aqui estão alguns casos de teste que gostaria de tentar. Estes parecem corretos, ou você quer adicionar mais?" Depois execute-os.

Salve os casos de teste em `evals/evals.json`. Não escreva assertions ainda — apenas os prompts. Você vai criar assertions na próxima etapa enquanto as execuções estão em andamento.

```json
{
  "skill_name": "exemplo-skill",
  "evals": [
    {
      "id": 1,
      "prompt": "Prompt da tarefa do usuário",
      "expected_output": "Descrição do resultado esperado",
      "files": []
    }
  ]
}
```

Veja `references/schemas.md` para o schema completo (incluindo o campo `assertions`, que você vai adicionar depois).

## Executando e avaliando casos de teste

Esta seção é uma sequência contínua — não pare no meio. NÃO use `/skill-test` ou qualquer outra skill de teste.

Coloque resultados em `<skill-name>-workspace/` como sibling do diretório da skill. Dentro do workspace, organize resultados por iteração (`iteration-1/`, `iteration-2/`, etc.) e dentro disso, cada caso de teste fica em um diretório (`eval-0/`, `eval-1/`, etc.). Não crie tudo isso antecipadamente — apenas crie diretórios conforme avança.

### Etapa 1: Spawnar todas as execuções (com-skill E baseline) na mesma vez

Para cada caso de teste, spawne dois subagentos na mesma vez — um com a skill, um sem. Isso é importante: não spawne as execuções com-skill primeiro e depois volte para baselines depois. Lance tudo de uma vez para que tudo termine aproximadamente ao mesmo tempo.

**Execução com-skill:**

```
Execute esta tarefa:
- Caminho da skill: <caminho-para-skill>
- Tarefa: <prompt da avaliação>
- Arquivos de entrada: <arquivos da avaliação se houver, ou "nenhum">
- Salvar saídas em: <workspace>/iteration-<N>/eval-<ID>/with_skill/outputs/
- Saídas para salvar: <o que o usuário se importa — ex: "o arquivo .docx", "o CSV final">
```

**Execução baseline** (mesmo prompt, mas o baseline depende do contexto):
- **Criando uma skill nova**: nenhuma skill. Mesmo prompt, nenhum caminho de skill, salvar em `without_skill/outputs/`.
- **Melhorando uma skill existente**: a versão antiga. Antes de editar, faça snapshot da skill (`cp -r <caminho-da-skill> <workspace>/skill-snapshot/`), depois aponte o subagentos baseline para o snapshot. Salve em `old_skill/outputs/`.

Escreva um `eval_metadata.json` para cada caso de teste (assertions pode estar vazio por enquanto). Dê a cada avaliação um nome descritivo com base no que está sendo testado — não apenas "eval-0". Use este nome para o diretório também. Se esta iteração usa prompts de avaliação novos ou modificados, crie esses arquivos para cada diretório de avaliação novo — não assuma que eles carregam da iteração anterior.

```json
{
  "eval_id": 0,
  "eval_name": "nome-descritivo-aqui",
  "prompt": "O prompt da tarefa do usuário",
  "assertions": []
}
```

### Etapa 2: Enquanto as execuções estão em andamento, crie assertions

Não apenas fique esperando as execuções terminarem — você pode usar esse tempo produtivamente. Crie assertions quantitativas para cada caso de teste e explique-as ao usuário. Se assertions já existem em `evals/evals.json`, revise-as e explique o que elas verificam.

Boas assertions são objetivamente verificáveis e têm nomes descritivos — devem ler claramente no visualizador de benchmark para que alguém que dê uma olhada rápida imediatamente entenda o que cada uma verifica. Skills subjetivas (estilo de escrita, qualidade de design) são melhor avaliadas qualitativamente — não force assertions em coisas que precisam de julgamento humano.

Atualize os arquivos `eval_metadata.json` e `evals/evals.json` com as assertions uma vez criadas. Também explique ao usuário o que ele verá no visualizador — tanto as saídas qualitativas quanto o benchmark quantitativo.

### Etapa 3: Conforme as execuções se completarem, capture dados de timing

Quando cada tarefa do subagentos se completa, você recebe uma notificação contendo `total_tokens` e `duration_ms`. Salve esses dados imediatamente em `timing.json` no diretório de execução:

```json
{
  "total_tokens": 84852,
  "duration_ms": 23332,
  "total_duration_seconds": 23.3
}
```

Esta é a única oportunidade para capturar esses dados — ele vem através da notificação de tarefa e não é persistido em outro lugar. Processe cada notificação conforme ela chega em vez de tentar agrupar.

### Etapa 4: Classificar, agregar e iniciar o visualizador

Uma vez que todas as execuções estão feitas:

1. **Classificar cada execução** — spawne um subagentos grader (ou classifique inline) que leia `agents/grader.md` e avalie cada assertion contra as saídas. Salve resultados em `grading.json` no diretório de execução. O array expectations em grading.json deve usar os campos `text`, `passed`, e `evidence` (não `name`/`met`/`details` ou outras variantes) — o visualizador depende desses nomes de campo exatos. Para assertions que possam ser verificadas programaticamente, escreva e execute um script em vez de apenas olhar — scripts são mais rápidos, mais confiáveis e podem ser reutilizados em iterações.

2. **Agregar em benchmark** — execute o script de agregação do diretório da skill-creator:
   ```bash
   python -m scripts.aggregate_benchmark <workspace>/iteration-N --skill-name <nome>
   ```
   Isso produz `benchmark.json` e `benchmark.md` com pass_rate, tempo e tokens para cada configuração, com média ± desvio padrão e o delta. Se gerar benchmark.json manualmente, veja `references/schemas.md` para o schema exato que o visualizador espera.
Coloque cada versão with_skill antes de seu contrapartida baseline.

3. **Faça uma análise** — leia os dados de benchmark e destaque padrões que as estatísticas agregadas podem esconder. Veja `agents/analyzer.md` (a seção "Analyzing Benchmark Results") para o que procurar — coisas como assertions que sempre passam independentemente de skill (não-discriminante), avaliações com alta variância (possivelmente instáveis), e trade-offs tempo/token.

4. **Inicialize o visualizador** com ambas as saídas qualitativas e dados quantitativos:
   ```bash
   nohup python <caminho-skill-creator>/eval-viewer/generate_review.py \
     <workspace>/iteration-N \
     --skill-name "minha-skill" \
     --benchmark <workspace>/iteration-N/benchmark.json \
     > /dev/null 2>&1 &
   VIEWER_PID=$!
   ```
   Para iteração 2+, também passe `--previous-workspace <workspace>/iteration-<N-1>`.

   **Ambientes Cowork / headless:** Se `webbrowser.open()` não está disponível ou o ambiente não tem display, use `--static <caminho-saída>` para escrever um arquivo HTML autossuficiente em vez de iniciar um servidor. Feedback será baixado como um arquivo `feedback.json` quando o usuário clicar em "Submit All Reviews". Depois de baixado, copie `feedback.json` para o diretório do workspace para a próxima iteração pegar.

Nota: por favor, use generate_review.py para criar o visualizador; não há necessidade de escrever HTML customizado.

5. **Conte ao usuário** algo como: "Abri os resultados em seu navegador. Há duas abas — 'Outputs' permite que você clique em cada caso de teste e deixe feedback, 'Benchmark' mostra a comparação quantitativa. Quando terminar, volte aqui e me avise."

### O que o usuário vê no visualizador

A aba "Outputs" mostra um caso de teste por vez:
- **Prompt**: a tarefa que foi dada
- **Output**: os arquivos que a skill produziu, renderizados inline quando possível
- **Previous Output** (iteração 2+): seção contraída mostrando saída da última iteração
- **Formal Grades** (se grading foi executado): seção contraída mostrando assertion pass/fail
- **Feedback**: uma caixa de texto que salva automaticamente conforme você digita
- **Previous Feedback** (iteração 2+): seus comentários de última vez, mostrados abaixo da caixa de texto

A navegação é via botões anterior/próximo ou setas. Quando terminar, ele clica "Submit All Reviews" que salva todo feedback em `feedback.json`.

### Etapa 5: Leia o feedback

Quando o usuário disser que está feito, leia `feedback.json`:

```json
{
  "reviews": [
    {"run_id": "eval-0-with_skill", "feedback": "o gráfico está sem labels nos eixos", "timestamp": "..."},
    {"run_id": "eval-1-with_skill", "feedback": "", "timestamp": "..."},
    {"run_id": "eval-2-with_skill", "feedback": "perfeito, amei isto", "timestamp": "..."}
  ],
  "status": "complete"
}
```

Feedback vazio significa que o usuário achou que estava bom. Foque suas melhorias nos casos de teste onde o usuário teve reclamações específicas.

Mate o servidor de visualizador quando terminar com ele:

```bash
kill $VIEWER_PID 2>/dev/null
```

---

## Melhorando a skill

Este é o coração do loop. Você executou os casos de teste, o usuário revisou os resultados, e agora você precisa melhorar a skill com base no feedback dele.

### Como pensar sobre melhorias

1. **Generalize a partir do feedback.** A grande ideia que está acontecendo aqui é que estamos tentando criar skills que possam ser usadas um milhão de vezes (talvez literalmente, talvez até mais) em muitos prompts diferentes. Aqui você e o usuário estão iterando apenas em alguns exemplos repetidamente porque ajuda a se mover mais rápido. O usuário conhece esses exemplos de dentro para fora e é rápido para eles avaliarem novas saídas. Mas se a skill que você e o usuário estão codesenvolvendo funciona apenas para esses exemplos, é inútil. Em vez de fazer mudanças fiddly e overfitty, ou restrições opressivamente limitantes, se há algum problema teimoso, você pode tentar ramificar e usar metáforas diferentes, ou recomendar padrões diferentes de trabalho. É relativamente barato tentar e talvez você pouse em algo ótimo.

2. **Mantenha o prompt enxuto.** Remova coisas que não estão puxando seu peso. Certifique-se de ler as transcrições, não apenas as saídas finais — se parecer que a skill está fazendo o modelo desperdiçar um monte de tempo fazendo coisas que são improdutivas, você pode tentar se livrar das partes da skill que estão fazendo isso e ver o que acontece.

3. **Explique o porquê.** Tente muito explicar o **por que** por trás de tudo que você está pedindo ao modelo para fazer. Os LLMs de hoje são *inteligentes*. Eles têm boa teoria da mente e quando dado um bom harness podem ir além de instruções por rote e realmente fazer as coisas acontecerem. Mesmo se o feedback do usuário for terse ou frustrado, tente realmente entender a tarefa e por que o usuário está escrevendo o que escreveu, e o que eles realmente escreveram, e então transmita esse entendimento para as instruções. Se se encontrar escrevendo SEMPRE ou NUNCA em todas caps, ou usando estruturas super rígidas, isso é uma bandeira amarela — se possível, reframe e explique o raciocínio para que o modelo entenda por que a coisa que você está pedindo é importante. Essa é uma abordagem mais humana, poderosa e eficaz.

4. **Procure por trabalho repetido em casos de teste.** Leia as transcrições das execuções de teste e note se os subagentos todos independentemente escreveram scripts helper similares ou tomaram a mesma abordagem multi-etapa para algo. Se todos os 3 casos de teste resultaram no subagentos escrevendo um `create_docx.py` ou um `build_chart.py`, isso é um forte sinal de que a skill deveria agrupar esse script. Escreva uma vez, coloque em `scripts/`, e conte para a skill usá-lo. Isso economiza toda futura invocação de reinventar a roda.

Esta tarefa é bem importante (estamos tentando criar bilhões por ano em valor econômico aqui!) e seu tempo de pensamento não é o blocker; reserve seu tempo e realmente pense sobre isso. Sugiro escrever um rascunho de revisão e depois olhar para ele de novo e fazer melhorias. Realmente faça seu melhor para entrar na cabeça do usuário e entender o que eles querem e precisam.

### O loop de iteração

Após melhorar a skill:

1. Aplique suas melhorias à skill
2. Re-execute todos os casos de teste em um novo diretório `iteration-<N+1>/`, incluindo execuções baseline. Se você está criando uma skill nova, o baseline é sempre `without_skill` (sem skill) — isso permanece igual em iterações. Se você está melhorando uma skill existente, use seu julgamento sobre o que faz sentido como baseline: a versão original com a qual o usuário entrou, ou a iteração anterior.
3. Inicialize o reviewer com `--previous-workspace` apontando para a iteração anterior
4. Espere o usuário revisar e dizer que está feito
5. Leia o novo feedback, melhore novamente, repita

Continue até:
- O usuário dizer que está feliz
- O feedback estar tudo vazio (tudo parece bom)
- Você não estar fazendo progresso significativo

---

## Avançado: Comparação cega

Para situações onde você quer uma comparação mais rigorosa entre duas versões de uma skill (ex: o usuário pergunta "a nova versão é realmente melhor?"), há um sistema de comparação cega. Leia `agents/comparator.md` e `agents/analyzer.md` para os detalhes. A ideia básica é: dê duas saídas para um agente independente sem dizer qual é qual, e deixe-o julgar qualidade. Depois analise por que o vencedor venceu.

Isso é opcional, requer subagentos, e a maioria dos usuários não vai precisar. O loop de revisão humana geralmente é suficiente.

---

## Otimização de Descrição

O campo description no frontmatter SKILL.md é o mecanismo primário que determina se Claude invoca uma skill. Após criar ou melhorar uma skill, ofereça-se para otimizar a descrição para melhor precisão de disparo.

### Etapa 1: Gerar queries de avaliação de disparo

Crie 20 queries de avaliação — uma mistura de deve-disparar e não-deve-disparar. Salve como JSON:

```json
[
  {"query": "o prompt do usuário", "should_trigger": true},
  {"query": "outro prompt", "should_trigger": false}
]
```

As queries devem ser realistas e algo que um usuário de Claude Code ou Claude.ai realmente digitaria. Não pedidos abstratos, mas pedidos concretos e específicos e que têm uma boa quantidade de detalhe. Por exemplo, caminhos de arquivo, contexto pessoal sobre o trabalho do usuário ou situação, nomes de coluna e valores, nomes de empresas, URLs. Um pouco de backstory. Alguns podem estar em minúsculas ou conter abreviações ou typos ou fala casual. Use uma mistura de tamanhos diferentes, e foque em casos extremos em vez de torná-los claros (o usuário terá uma chance de aprovar).

Ruim: `"Formatar estes dados"`, `"Extrair texto de PDF"`, `"Criar um gráfico"`

Bom: `"ok então meu chefe me mandou esse arquivo xlsx (está no meu downloads, chamado algo como 'Q4 sales final FINAL v2.xlsx') e ela quer que eu adicione uma coluna que mostre a margem de lucro como percentual. A receita está na coluna C e custos estão na coluna D acho"`

Para as queries **deve-disparar** (8-10), pense sobre cobertura. Você quer fraseados diferentes da mesma intenção — alguns formais, alguns casuais. Inclua casos onde o usuário não nomeia explicitamente a skill ou tipo de arquivo mas claramente precisa dela. Jogue alguns casos de uso incomuns e casos onde essa skill compete com outra mas deveria ganhar.

Para as queries **não-deve-disparar** (8-10), as mais valiosas são os quase-erros — queries que compartilham palavras-chave ou conceitos com a skill mas realmente precisam de algo diferente. Pense em domínios adjacentes, fraseado ambíguo onde um match por palavra-chave ingênuo dispararia mas não deveria, e casos onde a query toca em algo que a skill faz mas em um contexto onde outra ferramenta é mais apropriada.

A coisa-chave a evitar: não faça queries não-deve-disparar obviamente irrelevantes. "Escrever uma função fibonacci" como teste negativo para uma skill de PDF é muito fácil — não testa nada. Os casos negativos devem ser genuinamente tricky.

### Etapa 2: Revisar com usuário

Apresente o conjunto de avaliação ao usuário para revisão usando o template HTML:

1. Leia o template de `assets/eval_review.html`
2. Substitua os placeholders:
   - `__EVAL_DATA_PLACEHOLDER__` → o array JSON de itens de avaliação (sem aspas ao redor — é uma atribuição de variável JS)
   - `__SKILL_NAME_PLACEHOLDER__` → o nome da skill
   - `__SKILL_DESCRIPTION_PLACEHOLDER__` → a descrição atual da skill
3. Escreva para um arquivo temporário (ex: `/tmp/eval_review_<nome-skill>.html`) e abra-o: `open /tmp/eval_review_<nome-skill>.html`
4. O usuário pode editar queries, alternar deve-disparar, adicionar/remover entradas, depois clicar "Export Eval Set"
5. O arquivo baixa para `~/Downloads/eval_set.json` — verifique a pasta Downloads pela versão mais recente em caso de múltiplas (ex: `eval_set (1).json`)

Este passo importa — queries de avaliação ruins levam a descrições ruins.

### Etapa 3: Execute o loop de otimização

Conte ao usuário: "Isto vai levar um tempo — vou executar o loop de otimização em background e checar periodicamente."

Salve o conjunto de avaliação no workspace, depois execute em background:

```bash
python -m scripts.run_loop \
  --eval-set <caminho-para-trigger-eval.json> \
  --skill-path <caminho-para-skill> \
  --model <id-do-modelo-nesta-sessão> \
  --max-iterations 5 \
  --verbose
```

Use o ID do modelo de seu system prompt (o que está alimentando a sessão atual) para que o teste de disparo corresponda ao que o usuário realmente experimenta.

Enquanto roda, periodicamente tail a saída para dar ao usuário atu