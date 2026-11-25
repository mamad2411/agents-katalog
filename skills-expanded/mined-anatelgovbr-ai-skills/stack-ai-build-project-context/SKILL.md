---
name: stack-ai-build-project-context
description: >
  Enriquece uma stack de IA instalada com evidência do repositório. Use para registrar ou revisar
  contexto no AGENTS.md, skills de fluxo, referências e guardrails. Investiga a arquitetura e as
  convenções de implementação, incluindo unidades do sistema, acesso a dados, autenticação,
  autorização, validação e integrações. Na rodada de enriquecimento, identifica a pasta da
  aplicação e complementa em ops/ as lacunas de execução e testes. Acione também para escolher
  onde registrar uma convenção, conferir a stack contra o código atual ou preparar agentes para
  uma codebase desconhecida. Implementação de funcionalidades, revisão de código, dicionário de
  dados e documentação para usuários ficam fora do escopo.
---

# stack-ai-build-project-context

Descubra como este sistema e construido e como se desenvolve nele, e deixe isso escrito de
forma que outro agente consiga implementar sem redescobrir. O produto da rodada nao e
documentacao descritiva: e base operacional, distribuida entre `AGENTS.md`, skills,
`.agents/references/`, guardrails e instruções operacionais em `ops/`.

## O alvo real

Um agente generico ja sabe programar. O que ele nao sabe e **como se faz uma coisa nova
neste sistema**: quais arquivos participam, em que ordem, quais dependencias sao
obrigatorias, qual mecanismo de acesso a dados e o convencionado, o que precisa ser
verificado antes de uma pagina executar, o que o resto do codigo faz de um jeito proprio.

A rodada termina quando o repositorio consegue responder, com artefato escrito, perguntas
como estas:

- Como uma pagina, tela, endpoint ou unidade equivalente e construida aqui?
- Como se cria uma unidade autenticada, e como a permissao e verificada?
- Onde ficam as regras de negocio, e como sao acionadas?
- Como o sistema acessa dados? Procedure, query direta, ORM ou abstracao propria?
- Isso e obrigatorio ou apenas comum?
- Como transacoes, erros e sessao sao tratados?
- Como as integracoes externas sao usadas deste lado?
- Quais arquivos costumam participar de uma funcionalidade?
- Quais padroes devem ser preservados ao criar codigo novo, e qual desvio merece alerta?
- Onde fica o código da aplicação e como preparar e executar o ambiente local, a validação em QA e as suítes de testes que o projeto oferece?

Cada uma dessas perguntas sem resposta escrita e uma lacuna a declarar no relatorio, nao um
silencio.

## Principio fundamental

**A codebase e a unica autoridade.** Nunca assuma padrao de mercado, boa pratica, arquitetura
conhecida ou convencao que nao tenha evidencia no codigo investigado. Nome de pasta,
framework declarado, documentacao interna e experiencia com tecnologia parecida sao
hipoteses a confirmar.

**Padrao legado recorrente e convencao, nao defeito a corrigir.** O objetivo nao e avaliar se
a arquitetura segue boas praticas modernas nem propor a arquitetura ideal. Quando um padrao
parecer tecnicamente inadequado mas for claramente o que o sistema usa, ele e registrado
como o padrao existente, sustentado por contagem e sem juizo de qualidade. Coerencia
com o sistema e o criterio; boa pratica externa nao e.

Conhecimento de convencao externa pode ser usado para **formular hipotese** ("num sistema
assim, a conexao costuma vir de X: aqui vem de onde?") e para nomear o que se encontrou.
Nunca para decidir o que deveria existir, nem para entrar num artefato como regra.

**Documente a separacao que o codigo tiver.** Se persistencia, validacao, regra de negocio e
renderizacao vivem no mesmo arquivo, isso e a descoberta arquitetural, e e ela que se
documenta.

## Regra de importacao zero

Esta skill pode estar instalada em um repositorio com convencoes fortes e opinativas.
Nenhuma delas acompanha a skill. Nao leve para a codebase de destino regra, nome de camada,
gate, prefixo, padrao de commit ou estrutura de pastas observados no repositorio onde a
skill vive.

Quando existir uma stack de IA de referencia acessivel, use a **apenas como referencia
estrutural**: que tipos de artefato costumam ser uteis (skill de fluxo, skill de
verificacao, reference de padrao, guardrail, checklist), como uma skill de verificacao se
organiza, que forma uma tabela de guardrails costuma ter. Conteudo, regra, nome de
mecanismo e convencao nao atravessam: o que entra no destino sai da evidencia do destino.

A rodada preserva o código e a estrutura da aplicação. Escreva nos destinos definidos em `references/contrato-da-stack.md`, incluindo documentação operacional em `ops/`. Para criar script ou configuração executável em `ops/`, siga o ramo de autorização específica de `references/operacao-do-projeto.md`. Encontrar código que viola um padrão é um achado a relatar.

## Fontes de regra

Carregue sob demanda, conforme a fase:

| Arquivo | Autoridade sobre | Quando ler |
|---|---|---|
| `references/contrato-da-stack.md` | O que e a stack minima, o que cada destino aceita, secoes do esqueleto, indices e idempotencia | Fases 0, 1 e 8 |
| `references/protocolo-investigacao.md` | Eixos obrigatorios, unidades do sistema, amostra representativa, classificacao de padrao e barra de evidencia | Fases 1 a 4 |
| `references/operacao-do-projeto.md` | Diagnóstico de execução e testes, localização da aplicação, admissão, autorização e verificação dos itens de `ops/` | Fase 2 e retomada nas Fases 5 a 9 |
| `references/protocolo-subagentes.md` | Quando dividir, retorno do ROI, registro no runtime e resolucao de divergencia | Fases 2 e 3 |
| `references/criterios-de-classificacao.md` | Testes de admissao de `AGENTS.md`, skill, reference, guardrail e automacao | Fase 5 |
| `references/gauntlet-loop.md` | Papeis, verificacao proporcional, vereditos e rodadas | Fase 6 |
| `references/formato-artefatos.md` | Forma de cada artefato escrito e uso obrigatorio da `skill-creator` | Fase 8 |
| `references/armadilhas-de-medicao.md` | Testes que separam numero que reproduz de numero que mede certo, e amostra minima por territorio | Fases 3, 6 e 8 |

Os papeis executados em contexto separado tem prompt proprio em `agents/`, prontos para
enviar a um subagente: `revisor-do-que-investigar.md`, `investigador.md`, `auditor-do-rascunho.md`
e `medidor-de-conformidade.md`.

Modelos de artefato ficam em `assets/`: registro da rodada, esqueleto de reference e
proposta de skill.

## Fluxo

### Fase 0. Enquadramento

Confirme a raiz do repositorio de destino e rode o inventario:

```bash
python3 <caminho-desta-skill>/scripts/inventario_stack.py stack --raiz <raiz-do-repo>
```

Use o caminho absoluto da propria skill: o diretorio de trabalho e o repositorio de destino,
que pode ter um `scripts/` proprio sem relacao com este. `--json` devolve a saida estruturada
quando for mais util que o relatorio legivel.

Se a instalação do Python 3 responder por `python` em vez de `python3`, use esse comando em toda a rodada.

O script reporta quais pecas da stack existem, o que ja esta escrito nelas e o **orcamento de
contexto permanente**. Leia `references/contrato-da-stack.md` para interpretar o resultado e
decidir entre prosseguir, pedir autorizacao para criar o esqueleto faltante ou parar.

Antes de qualquer coisa, **leia o que a stack de destino ja contem**. Enriquecer e operacao
incremental: conhecimento ja registrado nao volta a entrar, e artefato existente e atualizado
em vez de duplicado.

**Preflight de ferramentas.** Verifique o que o runtime oferece antes de prometer qualquer
coisa. Ausencia descoberta no fim custa a rodada inteira:

| Ferramenta | Como confirmar | O que se perde sem ela |
|---|---|---|
| raiz do repositorio | `git rev-parse --show-toplevel` | tudo: caminho relativo errado invalida qualquer evidencia |
| Python 3 | `python3 --version` ou `python --version` | censo, perfil de codificacao e verificador. Pare e resolva |
| `rg`, com `grep` como reserva | `rg --version` | contagem confiavel fora de ASCII |
| `file` e `iconv` | `which file iconv` | desempate byte a byte quando o perfil de codificacao nao decidir |
| subagentes | mecanismo do proprio runtime | paralelismo e independencia do Auditor |
| `skill-creator` | localize o `SKILL.md` dela; nao presuma | a fase de skill inteira |
| `configuracao-de-testes-unitarios` | localize o `SKILL.md` dela | apoio ao diagnóstico de testes unitários e ao plano do relatório |

Procure a `skill-creator` antes de declara la ausente: ela costuma estar em `.claude/skills/`,
em `.agents/skills/`, no diretorio de skills do usuario ou instalada como plugin. Diretorio
vazio com o nome dela e ausencia, nao instalacao. Skill e destino esperado desta rodada:
quando a `skill-creator` faltar, diga ao desenvolvedor **antes de comecar** o que fica
bloqueado e o que a instala. Um minuto ali evita uma rodada que descobre fluxos e nao
consegue empacotar nenhum.

Feche tambem, no mesmo momento, os pontos abaixo. **Todos tem default**: quem pede a
rodada pode nao conhecer a arquitetura do sistema, e frequentemente e esse o caso, porque e
justamente o que a rodada vai descobrir. Pergunte apenas o que o codigo nao responde, e nunca
pergunte para comecar.

1. **Escopo de escrita.** Por padrão, `AGENTS.md`, `.agents/references/`, `.agents/skills/`, as quatro seções de projeto da ponte `.agents/security/mapa-cwe-guia.md` quando ela existir e a documentação operacional em `ops/`, dentro dos limites do destino. Script ou configuração executável em `ops/` depende de autorização específica na Fase 7. Registre outros pedidos de escrita fora do escopo para decisão do desenvolvedor.
2. **Nao objetivos.** Fluxo de branches, promoção, deploy, agendamento e operação de sistemas externos ficam fora da rodada. Os arquivos versionados que comprovam como o projeto executa e testa são evidência do diagnóstico, inclusive os de integração contínua.
3. **Sistemas externos no alcance.** Default: derive do censo, sem perguntar. Componente
   instanciado por nome, include que aponta para fora da arvore versionada e driver de dados
   sao a lista, e o censo ja os devolve. Declare a lista no registro da rodada e siga: o que
   se investiga e o uso local, conforme a Fase 3.
4. **Escopo de investigacao.** Default: derive do censo. Em repositorio grande ou plural,
   escolha o recorte de maior massa com vocabulario proprio, declare o recorte, o motivo e o
   que ficou de fora para a proxima rodada. Nao peca ao desenvolvedor que escolha por
   arquitetura: ele pode nao ter como, e a escolha esta no censo.
5. **Independencia limitada.** Sem subagentes, a investigacao vira passagens inline separadas
   por frente e a independencia do Auditor fica limitada. E aceitavel, desde que declarado no
   relatorio.

Toda decisao tomada por default **e declarada** no registro da rodada e repetida no relatorio,
como premissa e nao como fato. Premissa declarada o desenvolvedor corrige na rodada seguinte;
premissa silenciosa vira regra errada sem dono.

A stack ausente exige decisão de instalar antes de começar. Decisões sobre escrita fora do escopo padrão ficam pendentes enquanto a rodada avança na leitura e nos itens independentes.

**Abra o registro da rodada.** Copie `assets/template-registro-da-rodada.md` para a area de
trabalho da sessao, fora do repositorio de destino, e preencha o enquadramento agora. O
arquivo e preenchido fase a fase e, na Fase 7, ja e o plano.

**Declare os tetos da rodada no enquadramento**, antes de qualquer investigacao: subagentes
simultaneos, subagentes na rodada inteira e ciclos de auditoria na rodada inteira. Sao numeros
finitos e valem para a rodada toda. Teto e limite de seguranca, nao meta: a rodada termina antes
sempre que a evidencia permitir. Os valores tipicos e o que cada um impede estao em
`references/protocolo-subagentes.md`, secao Teto da rodada.

**Antes de abrir um registro novo, pergunte se ja existe um.** Rodada interrompida por contexto,
por sessao encerrada ou por decisao do desenvolvedor deixa trabalho pago no chao. Quando o
desenvolvedor informar o caminho de um registro anterior, ou quando voce mesmo tiver aberto um
nesta maquina, retome dali em vez de recomecar.

Ao acionar um papel em contexto separado, envie **o trecho** que aquele papel precisa, nunca o
arquivo inteiro: o registro acumula os achados de todas as frentes, e mandar tudo para um
investigador produz confirmacao encomendada.

Se a stack ja estiver povoada, a rodada inclui **medicao de conformidade**: cada regra de
`AGENTS.md`, cada guardrail e cada afirmacao das secoes de evidencias e reverificada contra o
codigo atual, com veredito `conforme`, `alcance-reduzido`, `contradiz` ou `comando-nao-reproduz`.
Rode o comando registrado ao lado da afirmacao, exatamente como esta escrito. Comando que nao
reproduz o proprio numero e defeito do artefato, nao mudanca do sistema: corrija o comando na
mesma rodada e diga isso no relatorio.

**Monte a fila pelo historico, nao pela lista inteira.** Antes de medir, leia a secao
`## Historico de conformidade` de cada reference. Afirmacao com tres vereditos `conforme`
consecutivos esta estavel e sai da fila, desde que os arquivos do alcance dela nao tenham mudado
desde a ultima medicao, o que se confirma com um `git log` no escopo, conforme
`references/formato-artefatos.md`. Commit no escopo devolve a afirmacao para a fila por mais
estavel que ela fosse.

E isso que faz a medicao ficar mais barata a cada rodada. Sem o historico, a decima rodada paga o
mesmo que a primeira para reconfirmar o que ninguem tocou, e o orcamento que sobraria para
investigar coisa nova se gasta reconfirmando o conhecido. Os vereditos desta rodada entram como
bloco novo no topo do historico, e bloco anterior nunca e reescrito.

Escopo amplo demais produz achados rasos. Em repositorio grande ou plural, recorte: sistema
inteiro, um subsistema ou um conjunto de diretorios. Quando o desenvolvedor nomear o recorte,
use o dele; quando nao, escolha pelo censo e declare a escolha com o motivo.

### Fase 1. Censo e dependencias

Levantamento barato e deterministico antes de qualquer leitura profunda:

```bash
python3 <caminho-desta-skill>/scripts/inventario_stack.py censo --raiz <raiz-do-repo> --top 25
```

`--top` limita cada lista e corta em silencio o que exceder, entao aumente o valor em
repositorio grande antes de concluir que algo nao existe. O censo devolve distribuicao de
linguagens, diretorios de topo por volume, manifestos, configuracao de lint e CI, diretorios
de teste e migracao, documentacao existente, o **perfil de codificacao por extensao** e os
**sinais de dependencia**: componentes instanciados, includes e imports mais frequentes,
strings de conexao e driver, bibliotecas cliente com versao no nome, extensoes proprietarias.

Os sinais de dependencia existem porque manifesto nao e a unica forma de declarar
dependencia, e em sistema legado quase nunca e a forma usada. Eles alimentam diretamente as
secoes de contexto e de dependencias tecnicas do `AGENTS.md`, que sao **inventario em
topicos** e nao regra: conforme `references/contrato-da-stack.md`, essas secoes nao passam
pelos criterios de admissao de regra, e ficar vaga ali e falha da rodada.

**O censo e insumo, nao conteudo.** A saida dele, quantidade de arquivos, distribuicao por
extensao, perfil de codificacao, existe para voce descobrir qual e a tecnologia, qual e a
unidade e de que o sistema depende. Descoberto isso, ela e consumida e descartada. O que entra
no `AGENTS.md` e o fato que ela revelou, "a unidade e a pagina `.x` em `X/`, escrita em
<tecnologia>", nunca a medicao que levou ate ele, "o censo encontrou N arquivos em `X/`". Numero
medido sobrevive so na secao de evidencias de uma reference, onde existe para ser reexecutado;
no contexto global ele nao tem leitor e nao muda o que ninguem escreve.

O perfil de codificacao e requisito das fases seguintes. Em repositorio de codificacao mista,
ferramenta de busca discorda de ferramenta de busca, e dois papeis que buscam de formas
diferentes chegam a numeros diferentes. Feche o **protocolo de busca** antes da Fase 2, na
secao correspondente do registro da rodada, e envie o mesmo texto a todos os papeis: um
comando canonico por grupo de codificacao, com o escopo onde vale.

Todo comando canonico e **executado como esta escrito** antes de ser adotado, e o numero que
ele devolve e o numero que vale. Comando publicado que nao reproduz o proprio numero derruba
a proxima medicao de conformidade inteira.

Aproveite a documentacao que o repositorio ja tem, incluindo README, ADRs, comentarios de
configuracao e mensagens de commit recorrentes. Documento interno e evidencia declarativa
forte, desde que confirmado contra o codigo.

### Fase 2. Unidades do sistema e frentes

O censo diz do que o repositorio e feito. Esta fase decide **o que investigar**, e ela e a
que determina se a rodada produz base operacional ou uma lista de curiosidades.

**Diagnostique a operação e localize a aplicação.** Siga `references/operacao-do-projeto.md` em leitura. Preencha no registro as cinco linhas de execução e testes e a avaliação da pasta da aplicação. Faça esse diagnóstico além das frentes de código abaixo, que continuam sujeitas ao gate de amostra.

**Identifique as unidades que o sistema produz repetidamente.** Pagina, tela, endpoint,
formulario, relatorio, procedure, job, componente, modulo: o que quer que seja a coisa que
alguem cria quando implementa uma funcionalidade nova. O sinal e volume com vocabulario
proprio: centenas de arquivos com a mesma extensao e o mesmo formato de nome quase sempre
sao a unidade principal.

**Escolha exemplares representativos de cada unidade**, e nao um so. Pegue os mais recentes
pelo historico do versionamento, os mais antigos, e ao menos um de cada modulo ou subsistema
relevante. Exemplar recente mostra a convencao viva; exemplar antigo mostra o que mudou;
exemplares de modulos diferentes revelam se existe um padrao ou varios.

**Gate de amostra, e ele trava a fase.** Antes de descrever qualquer familia, liste os
diretorios onde a unidade existe e leia por inteiro pelo menos um exemplar de cada um dos tres
maiores. Dois arquivos do mesmo diretorio contam como um.

```bash
find <escopo> -name '<padrao da unidade>' -printf '%h\n' | sort | uniq -c | sort -rn | head
```

Descrever uma familia a partir de um territorio so foi o defeito mais caro medido em rodada
real: uma familia de 22 arquivos descrita a partir de 1, e a descricao valia para 7. Se voce
so consegue nomear um diretorio, o alcance da afirmacao **e aquele diretorio**.

**Leia os exemplares por inteiro antes de qualquer busca.** A ordem importa e e facil de
inverter: quem busca primeiro so encontra o que ja imaginava procurar, e devolve padroes
isolados em vez da sequencia que constroi a unidade. A leitura integral de dez arquivos revela
como o sistema e construido; a busca entra depois, para medir a extensao do que a leitura
mostrou e para procurar o que a contradiz.

**Derive as frentes por eixo, cruzado com subsistema.** Os eixos obrigatorios estao em
`references/protocolo-investigacao.md` e cobrem estrutura, ciclo da requisicao, autenticacao
e permissao, construcao da unidade, validacao, persistencia, regra de negocio, integracoes,
erro e log, configuracao e a comparacao entre implementacoes equivalentes. Cada frente recebe
um recorte de caminhos, um conjunto de eixos e uma lista de exemplares por onde comecar.

Prefira de tres a seis frentes. Nomeie pelo recorte observado, nunca por camada teorica: uma
frente chamada "camada de servico" pressupoe que existe uma.

Registre as frentes e a cobertura de eixos no registro da rodada. Eixo que nenhuma frente
cobre e decisao explicita, nao esquecimento.

**Gate do que investigar, antes de lancar qualquer investigador.** Envie a proposta fechada, unidade,
cobertura de territorio da amostra, frentes e eixos sem frente, ao Revisor do que investigar, com o
prompt de `agents/revisor-do-que-investigar.md`. Ele tenta derrubar a hipotese com orcamento
apertado, dez comandos e tres arquivos, e devolve a premissa que mata o recorte com o comando
que a testa.

Uma janela aqui e o seguro mais barato da rodada: o recorte errado so se revela na Fase 7, e ali
ja custou de tres a seis janelas medindo a coisa certa sobre o territorio errado. Veredito
`refazer o recorte` volta para esta fase; `ajustar` corrige a frente apontada e segue; `sem
bloqueios` autoriza o lancamento.

Quando o repositorio for pequeno e homogeneo e a investigacao correr direto na sessao principal,
os seis testes mecanicos do prompt sao rodados assim mesmo, inline. O que nao se dispensa e a
passagem: o que a torna util e ser feita contra o codigo antes do gasto, nao o subagente.

### Fase 3. Investigacao

Cada frente vira um subagente investigador com escopo de caminhos limitado, os eixos que lhe
cabem, os exemplares iniciais e proibicao explicita de escrever arquivos. Envie o prompt de
`agents/investigador.md`, preenchido, e lance todas as frentes independentes na mesma rodada.

Subagente custa uma janela de contexto inteira e so compensa por contexto protegido,
paralelismo ou independencia de julgamento. Repositorio pequeno e homogeneo se investiga
direto. O criterio completo esta em `references/protocolo-subagentes.md`.

O investigador devolve tres coisas, e as tres importam:

1. **Padroes com finalidade.** Nao "existe uma chamada X", e sim para que ela serve e em que
   momento do fluxo aparece: "paginas autenticadas inicializam X e executam a validacao Y
   antes de processar a requisicao". Padrao sem finalidade nao orienta implementacao.
2. **Processos observados.** A sequencia reconstruida a partir dos exemplares: que arquivos
   participam de uma funcionalidade, em que ordem, o que e obrigatorio, o que varia entre um
   exemplar e outro, e onde os exemplares divergem. E daqui que sai skill; sem esta secao, a
   fase de skill nao tem entrada e a rodada termina sem nenhuma.
3. **Candidatos a guardrail.** Convencao que uma implementacao nova pode violar sem perceber,
   com a contagem dos dois lados.

Toda afirmacao carrega evidencia rastreavel: caminhos completos a partir da raiz, contagem de
ocorrencias e de arquivos, o comando literal que produziu a contagem e a busca que tentaria
derruba la.

**Reproduzir nao e medir certo.** Antes de registrar qualquer contagem, passe a afirmacao pelas
nove perguntas de `references/armadilhas-de-medicao.md`. Um comando pode reproduzir o proprio
numero para sempre e estar medindo outra coisa desde o inicio. As tres que mais derrubam
artefato, e que nao custam nada:

```bash
python3 <caminho-desta-skill>/scripts/inventario_stack.py auditar-comando --raiz <raiz> --cmd '<comando>'
```

- **ancora**: o padrao casa sufixo de outra palavra? (`id` casa `uuid` e `valid`)
- **ativo contra comentado**: quantas das ocorrencias estao em linha comentada?
- **incluido contra chamado**: o simbolo e usado, ou so declarado e carregado? A barra completa, e o que muda entre padrao dominante, padroes concorrentes,
excecao e caso isolado, estao em `references/protocolo-investigacao.md`.

**Fronteira de sistema externo.** Codigo que o repositorio consome e nao versiona nao e
auditavel por dentro, e tentar isso produz linhas de "nao confirmavel". A pergunta muda de
lado: nao e como aquele sistema funciona, e **como o nosso codigo o usa**. Onde a integracao
aparece, para que serve, qual o padrao local de uso, quais arquivos participam, que
pre condicoes existem e o que o objeto externo entrega ao nosso codigo. Esse contrato esta
inteiro deste lado e e material de primeira linha: quando um objeto externo e a origem da
conexao de banco, da identidade do usuario ou da verificacao de permissao, isso e arquitetura
local, nao detalhe do outro sistema.

### Fase 4. Consolidacao

Passe cada dossie pelo verificador antes de ler:

```bash
python3 <caminho-desta-skill>/scripts/inventario_stack.py validar-achado --arquivo <dossie>
```

Ele confere campos ausentes ou devolvidos como molde, contagem que nao fecha, contraexemplo
sem quantidade, comando de contraexemplo igual ao de confirmacao, e classifica o padrao a
partir dos numeros. Classificacao declarada acima da calculada volta ao investigador.

Reuna os dossies e organize os achados **por eixo**, nao por frente. Remova sobreposicao.
Trate divergencia entre frentes com verificacao dirigida no codigo, nunca por maioria.

Divergencia que sobrevive a verificacao costuma ser um achado melhor que qualquer um dos
dois originais: dois subsistemas fazem a mesma coisa de formas diferentes, e essa diferenca e
legitima. Preserve os dois com alcance separado, com a contagem de cada um. **Dois padroes
concorrentes nao paralisam a rodada**: registre os dois, diga onde cada um vive, e o guardrail
que sai dali pede confirmacao de qual vale no modulo em vez de proibir. A pergunta ao
desenvolvedor entra no plano em paralelo, nunca no lugar do artefato.

**Hipotese derrubada volta como afirmacao.** Uma hipotese que o codigo contradisse costuma ser
o que um agente generico assume sozinho. Reformule na forma negativa ou condicional e submeta
ao mesmo teste. Ela e conhecimento util, mas nao substitui o padrao positivo: uma stack feita
so de negacoes diz o que nao assumir e nao ensina a fazer nada.

Leia a secao `## Descartado` das references de evidencias antes de reabrir qualquer fila: achado
reprovado em rodada anterior so volta quando o campo "o que mudaria a decisao" tiver acontecido.

Compare tudo contra a stack existente. Achado ja registrado sai da fila em silencio. Achado
que **contradiz** o que esta registrado segue para a Fase 6 com as duas evidencias lado a
lado. O resultado da medicao de conformidade entra aqui pelo mesmo caminho.

### Fase 5. Classificacao

Para cada padrão consolidado de implementação, decida o destino pelos testes de `references/criterios-de-classificacao.md`. Para o diagnóstico da Fase 2, use o critério de `references/operacao-do-projeto.md`: o item resolve uma lacuna comprovada de execução ou de teste?

| Destino | Recebe |
|---|---|
| `AGENTS.md` | contexto e dependencias em topicos, regra transversal curta, guardrail de alcance amplo, roteamento para os demais artefatos |
| Skill | fluxo de implementacao ou de verificacao recorrente: quando usar, como reconhecer, como aplicar |
| `.agents/references/` | detalhe consultivo: arquitetura, estrutura das unidades, persistencia, autenticacao, integracoes, convencoes de modulo, exemplares representativos |
| Guardrail | convencao violavel por implementacao nova, escrito como alerta com o padrao e a contagem |
| `ops/` | instruções que faltam para preparar, executar ou verificar o ambiente ou os testes. Script ou configuração executável segue o ramo de autorização específica |
| Automacao | recomendacao de hook, subagente ou comando ao desenvolvedor, sem instalar nada |
| Descarte | o que nao muda decisao nenhuma: motivo no relatorio e linha na secao `## Descartado` da reference de evidencias, para a proxima rodada nao reinvestigar |

Dois vieses opostos vivem aqui, e os dois custam caro.

**Inflacao** e promover achado interessante para o contexto global. Cada linha de `AGENTS.md`
e paga em toda tarefa do repositorio, inclusive nas que nada tem a ver com o assunto.

**Esterilizacao** e o oposto, e foi o que produziu rodadas sem nenhum artefato: aplicar a
barra de regra global a todo achado, reprovar o que nao passa e terminar com uma stack que so
diz o que nao assumir. Fluxo de implementacao recorrente nao disputa espaco com regra global,
porque skill nao mora no contexto global: ela e o destino natural desse conhecimento, e
rebaixa la para "reference que ninguem abre" e perder a rodada.

### Fase 6. Verificacao proporcional

O rigor acompanha o custo do erro. Nem todo artefato merece o mesmo ciclo, e aplicar o ciclo
completo a tudo foi o que fez rodadas inteiras terminarem sem entrega.

| Artefato | Verificacao |
|---|---|
| Regra em `AGENTS.md`, guardrail | ciclo completo: Auditor em contexto novo, contra o codigo |
| Proposta de skill | Auditor avalia a proposta consolidada: o processo descrito reproduz o que os exemplares mostram? |
| Reference descritiva, secoes de contexto e dependencias | conferencia dirigida: os numeros reproduzem com o comando canonico e os exemplares citados existem |
| Documentação e proposta executável em `ops/` | confira fonte, referências, comando, diretório, alvo, pré-requisitos e verificação prevista, conforme `references/operacao-do-projeto.md` |

O ciclo acontece sobre **rascunho fora do repositorio de destino**. O repositorio so e tocado
na Fase 8, depois da aprovacao.

O Auditor recebe a barra, o artefato e acesso ao repositorio, **sem a narrativa do
investigador**. Prompt em `agents/auditor-do-rascunho.md`. Ele procura afirmacao sem
evidencia, padrao declarado sem amostra que o sustente, excecao promovida a convencao,
alcance maior que o comprovado, duplicacao, destino errado, contagem que nao reproduz,
guardrail que proibe em vez de alertar, e skill que descreve sem ensinar a aplicar.

Cada veredito cita evidencia propria: reprovacao sem busca e opiniao. Duas rodadas validas no
maximo por item. Bloqueio causado por divergencia de comando de busca, e nao por divergencia
sobre o codigo, e `rodada-invalida` e nao consome tentativa. O que nao se resolve na segunda
rodada valida vira pergunta ao desenvolvedor **junto com o artefato reduzido ao que a
evidencia sustenta**, nao no lugar dele. Detalhes em `references/gauntlet-loop.md`.

### Fase 7. Plano e aprovacao

O plano ja existe: e o registro da rodada. Feche a secao de itens propostos, uma linha por
item com destino, acao, resumo, evidencia, comando, alcance, classificacao e veredito.

Feche tambem a **tabela de cobertura por eixo**: para cada eixo obrigatorio, o que foi
encontrado, onde vai ser escrito, ou por que ficou vazio. Eixo vazio tem uma de tres causas,
e cada uma leva a uma acao diferente: nao existe no sistema, nao foi investigado por decisao,
ou foi investigado e a evidencia nao fechou. Silencio nao e nenhuma das tres.

Antes de apresentar, confira o plano contra os criterios de conclusao da rodada. Nenhum deles
e opcional, e cada um tem uma saida legitima quando nao ha material:

| Criterio | Saida quando nao ha material |
|---|---|
| Secoes de contexto e dependencias preenchidas em topicos, uma linha por fato do censo | nao existe: o censo nao devolveu nada, e isso e dito |
| Ao menos uma skill de fluxo ou de verificacao proposta | declarar por que: o sistema nao tem fluxo repetido, com a evidencia, ou a investigacao nao reconstruiu processo, com o que falta |
| Ao menos uma reference sobre a construcao da unidade, com exemplares por caminho completo | declarar que nenhuma unidade repetida foi identificada, e o que foi buscado |
| Guardrails escritos como alerta, com padrao e contagem | nenhuma convencao violavel encontrada, e o que foi medido |
| Tabela de cobertura sem linha em branco | cada eixo vazio com um dos tres motivos |
| Todo comando de evidência executado como está escrito e reproduzindo o resultado | comando de evidência que falha volta para correção. Registre a conferência estática dos comandos operacionais e a validação prevista |
| Diagnóstico de operação e localização da aplicação completo | cada área tem evidência ou lacuna com responsável e o isolamento tem confirmação ou pergunta pendente |

Detalhe os itens de `ops/` conforme `references/operacao-do-projeto.md`. Para cada proposta executável, inclua no plano o impacto arquitetural conforme as regras do destino e obtenha autorização específica para o item antes de aplicar.

Um plano que nao atende um criterio e nao declara a saida esta incompleto, nao pronto.

### O gate tem duas posicoes

**Padrao: aprovacao antes de escrever.** Apresente o plano e aguarde. Escrever em `AGENTS.md`
sem revisao humana e a operacao de maior alcance e menor reversibilidade da stack. O
desenvolvedor aprova, rejeita ou reduz item a item.

**Modo autonomo: aprovacao depois de escrever.** Quando o desenvolvedor autorizar
explicitamente a rodada a aplicar sem apresentar o plano antes, o gate nao desaparece: ele se
move para depois da escrita, e o que muda e so o momento da revisao.

O que continua igual no modo autonomo, e nao e negociavel:

- O plano e escrito assim mesmo, no registro da rodada, antes de qualquer escrita. Ele e o que
  torna o resultado revisavel: sem ele o desenvolvedor recebe um diff sem saber o que foi
  decidido nem o que foi descartado.
- Os criterios de conclusao acima valem por inteiro.
- O escopo de escrita autorizado continua sendo o limite. Autorizar aplicar nao autoriza tocar
  em arquivo fora dele.
- A passagem final de Auditor sobre o diff real passa a ser **obrigatoria**, com contexto novo.
  Ela e a unica revisao antes do desenvolvedor, e nao ha segunda chance de pegar regra que
  mudou de sentido ao ser encaixada numa secao existente.

O que continua exigindo pergunta, mesmo autorizada a rodada a aplicar:

| Operacao | Por que continua no gate |
|---|---|
| Remover linha de `AGENTS.md`, guardrail ou reference existente | E perda, nao ganho. O desenvolvedor precisa aprovar o que sai, e a evidencia de hoje pode estar medindo errado |
| Reduzir o alcance de regra ja escrita | Mesma coisa: parte do que valia deixa de valer |
| Escolher entre dois padroes concorrentes | A escolha e do dono do repositorio, nao da evidencia. Registre os dois e pergunte |
| Escrever fora do escopo autorizado | Nao e decisao da rodada |
| Criar script ou configuração executável em `ops/` | Requer aprovação específica do item, mesmo em modo autônomo |

Nesses casos, escreva o que foi comprovado, deixe o item pendente no relatorio com as duas
evidencias, e siga. Nao pare a rodada inteira por causa deles.

O relatorio da rodada autonoma abre pelo que foi escrito, arquivo por arquivo, e pelas
perguntas pendentes. O desenvolvedor revisa o diff no versionamento, que e onde a reversao
existe: a skill nao faz commit e nao apaga historico.

### Fase 8. Aplicacao

Escreva somente os itens aprovados, na forma de `references/formato-artefatos.md`. Para `ops/`, siga `references/operacao-do-projeto.md` na escrita e na conferência estática. Execute a validação operacional quando houver autorização e condições seguras. Registre separadamente o que foi conferido por leitura e o que foi executado.

- Skill nova ou evoluida passa **obrigatoriamente** pela `skill-creator`, inclusive na
  descricao de disparo. Entregue a ela a proposta consolidada de
  `assets/template-proposta-de-skill.md`, para nao reabrir a investigacao dentro dela.
- Toda skill sai com o **eixo de invocacao** decidido: ponto de entrada de fluxo fica
  model-invocada; skill de etapa recebe `disable-model-invocation: true` e um artefato que mande
  ler o `SKILL.md` dela pelo caminho. Sem isso a descricao passa a ser paga em toda tarefa do
  repositorio, e uma skill de etapa nao tem por que custar isso.
- Toda reference termina com secao de evidencias, com caminhos, comando, alcance e a coluna de
  confianca. Todo comando de evidência é executado como está antes de ser publicado e passa por
  `auditar-comando`. Publicar comando que reproduz o numero mas mede outra coisa entrega a
  proxima rodada um artefato que parece verificado e nao esta.
- **Marque o que nao foi medido.** Afirmacao medida nao recebe marca; o que a leitura integral
  mostrou e a busca nao decide recebe `inferido:` com o que a confirmaria; o eixo investigado que
  nao fechou recebe `lacuna:` com a busca ja feita, e so em reference. Silencio no lugar de
  `lacuna:` faz o agente assumir ausencia e a proxima rodada repetir a busca. Formas e regras de
  reclassificacao em `references/formato-artefatos.md`.
- **Declare o sistema, nao a rodada.** O corpo do artefato diz qual e a tecnologia, onde a
  unidade vive e o que o codigo faz, no presente do indicativo. "O censo encontrou N arquivos
  `.x` em `X/Y`" e relatorio de investigacao; "a unidade e a pagina `.x` em `X/Y`, escrita em
  <tecnologia>" e o fato que muda a proxima implementacao. Metodo, contagem e comando ficam na
  secao de evidencias.
- Prefira **nomear o territorio** a cravar a contagem no corpo do texto. "Os arquivos de `X/Y`
  fazem assim" e mais acionavel que "8 de 22 fazem assim", nao envelhece quando alguem
  acrescenta um arquivo, e nao vira defeito quando a proxima medicao usa outra
  ferramenta. A contagem vive na secao de evidencias, na forma do comando que a produz.
- **Extraia o padrao; nao aponte para um arquivo.** Skill e reference descrevem os elementos, a
  ordem, o que e obrigatorio, o que varia e o criterio de cada decisao, de modo que o agente
  implemente sem abrir exemplar nenhum. Exemplar e conferencia da forma local, e vem sempre com
  a regra que localiza o equivalente de hoje: caminho citado sem essa regra vira ponteiro
  quebrado no primeiro rename, e "siga o padrao de `<arquivo>`" nao sobrevive a exclusao dele.
- Guardrail e escrito como alerta, com o padrao identificado e a contagem, nunca como
  proibicao e nunca afirmando que o padrao e tecnicamente ideal.
- Convencoes de formato, idioma, encoding e indice sao as **do repositorio de destino**,
  descobertas na Fase 1, nunca as do repositorio de origem.
- **Um artefato por vez, marcado no registro assim que sai.** Escrever a stack inteira numa
  passagem so gasta contexto no pior momento da rodada, quando ele ja esta curto, e produz um
  bloco que ninguem consegue revisar por partes. Cada artefato escrito fecha sua linha na secao de
  execucao do registro, e e ela que permite retomar a Fase 8 pela metade em sessao nova.
- **Ponte de seguranca.** Quando `.agents/security/mapa-cwe-guia.md` existir no destino, preencha as quatro secoes de projeto com o que a investigacao mediu, e so elas: `Traducao` e `Saidas opcionais` chegam da stack e nao sao alteradas. Cada entrada se apoia em evidencia do codigo, arquivo e linha ou saida do comando. Sem sinal ou auditor real, a secao mantem o texto padrao que veio da stack. Forma de cada secao em `references/formato-artefatos.md`.
  - `Sinais do projeto`: tabela com as colunas `Sinal no escopo`, `Play` e `Onde esta hoje`, um sinal por tipo de artefato que a investigacao encontrou (pagina ou unidade equivalente, API ou endpoint, dependencia versionada, infraestrutura como codigo, codigo que chama modelo de IA, configuracao de agente de IA), com o play correspondente da tabela Plays disponiveis do `SKILL.md` da `owasp-playbook`. Nao invente sinal para artefato que o projeto nao tem.
  - `Auditores do projeto`: bloco `bash` com comandos que existem no repositório ou buscas derivadas dos guardrails do `AGENTS.md`. Registre o que cada comando procura e execute-o uma vez antes de incluir. Comando operacional, como rodar testes ou iniciar um ambiente, só entra se a execução autorizada já tiver sido verificada.
  - `Excecoes`: lista do que nao e achado neste repositorio, com o motivo e a evidencia: area congelada pelo escopo de escrita, biblioteca de terceiros versionada, mecanismo que vem do core ou do framework.
  - `Correcao`: a skill ou o procedimento do projeto que recebe a correcao, por tipo de artefato, apontando o que ja existe na stack do destino.

Escrito o que foi aprovado, rode a passagem final de Auditor sobre o diff real, com contexto
novo, e corrija somente o que ela bloquear. Em modo autonomo essa passagem e obrigatoria, pelo
motivo da Fase 7: ela e a unica revisao antes do desenvolvedor. Feche verificando o resultado:

```bash
python3 <caminho-desta-skill>/scripts/inventario_stack.py verificar --raiz <raiz-do-repo>
```

### Fase 9. Relatorio

Reporte o que entrou em cada destino, a cobertura por eixo, o que foi rejeitado e por que, o
que ficou como pergunta aberta e o que tinha evidencia insuficiente. Mantenha o resumo curto:
o detalhe vive nos artefatos escritos.

A secao de automacao sai com no maximo dois itens por tipo. Ela e recomendacao pura, com
tipo, gatilho e o achado que a motiva; a configuracao fica com o desenvolvedor.

Reporte o diagnóstico de operação, o que foi complementado em `ops/`, o que já estava coberto e o que ficou pendente, com responsável. Informe o caminho e o estado do isolamento da aplicação. Quando a `configuracao-de-testes-unitarios` tiver apoiado a Fase 2, inclua o plano sustentado pelo projeto como recomendação. A validação de itens operacionais aprovados segue a Fase 8.

```text
Artefatos alterados:
- <caminho>: <o que entrou, mudou ou saiu>

Cobertura por eixo:
- <eixo>: <padrao registrado e onde> | <vazio: nao existe no sistema | nao objetivo | evidencia insuficiente>

Conhecimento consolidado:
- <destino>: <padrao ou regra> | evidencia: <caminho:linha, N de M> | alcance: <alcance>

Skills criadas ou evoluidas:
- <nome> | via skill-creator | eixo: <model-invocada | user-invocada, alcancada por <artefato>> | recorrencia: <numeros> | gatilho: <quando dispara>
- nenhuma | por que: <o sistema nao tem fluxo repetido, e a evidencia disso | a investigacao nao reconstruiu processo, e o que falta para reconstruir>

Guardrails escritos:
- <padrao identificado> | alerta quando: <desvio> | evidencia: <N de M> | onde vive: <artefato>

Nao consolidado:
- <afirmacao> | bloqueio: <ferramenta | evidencia-insuficiente | dois-padroes-concorrentes | fora-do-repositorio> | busca executada: <comando e universo> | resolveria: <artefato, acesso ou decisao> | dono: <quem resolve>

Nao investigado por decisao:
- <assunto> | nao objetivo declarado no preflight

Automacao sugerida ao desenvolvedor:
- <tipo: hook | subagente | comando> | <o que faz> | gatilho: <evento ou pedido> | evidencia: <achado desta rodada> | nao instalada por esta skill

Operação e testes:
- <local, QA, unitários, integração ou ponta a ponta> | <já coberto, complementado ou lacuna> | <fonte ou caminho em ops/> | <conferência estática, resultado executado ou pendência com responsável>
- aplicação: <caminho e evidência> | <isolamento confirmado ou decisão pendente>
- plano de testes unitários, quando houver: <item recomendado, onde roda e como conferir>

Premissas assumidas por default:
- <ponto do enquadramento> | assumido: <o que foi assumido> | derivado de: <censo ou contrato da stack>

Perguntas ao desenvolvedor:
- <pergunta objetiva>

Validacao:
- comandos de evidência reexecutados como estão: <N de N reproduzem o resultado>
- exemplares citados conferidos: <N de N existem>
- <check>: <resultado>

Limitacoes desta rodada:
- <subagentes indisponiveis, skill-creator ausente, escopo reduzido, ou "nenhuma">
```

## Rodada longa: pausa, limpeza e retomada

Em repositorio grande a rodada nao cabe numa sessao, e tratar isso como acidente e o que faz
perder frente inteira ja investigada.

**O estado se reconstroi por inspecao, nao por confianca no registro.** O registro da rodada diz o
que voce decidiu; o repositorio diz o que existe. Ao retomar, rode `inventario_stack.py stack` e
leia o que ja esta escrito na stack de destino, depois cruze com a tabela de cobertura por eixo do
registro. Onde os dois divergirem, vale o repositorio: artefato escrito e fato, linha de plano e
intencao.

**Feche o estado a cada fronteira, nao no fim.** Fronteira e frente de investigacao concluida,
dossie validado, item classificado e artefato escrito. Cada uma dessas fecha uma linha do
registro, com o que ficou pronto e o que falta. Fase que termina sem deixar linha escrita nao
aconteceu, do ponto de vista da proxima sessao.

**Ofereca a pausa antes de precisar dela.** Depois de uma frente pesada, ou de tres frentes
seguidas na mesma sessao, ofereca ao desenvolvedor parar, limpar o contexto e voltar com a rodada
retomada. A pergunta e curta e a decisao e dele:

```text
Frente <nome> concluida e registrada em <caminho do registro>. A proxima e <nome>, que le
<quantos> exemplares por inteiro. Continuar agora, ou pausar aqui, limpar o contexto e retomar
apontando o registro?
```

Tres regras fecham o protocolo, e as tres saem de erro observado:

- **Confirme que o registro esta salvo antes de oferecer a pausa.** Oferecer pausa sem estado
  gravado transforma limpeza de contexto em perda de trabalho.
- **Nao ofereca pausa logo apos uma retomada.** A sessao acabou de nascer limpa; sugerir limpeza
  ali so confunde.
- **Nao tente estimar tokens restantes.** A conta varia por runtime e erra. O sinal utilizavel e
  observavel: quantos arquivos voce leu por inteiro, quantas frentes fechou, ha quantas trocas a
  sessao comecou.

Investigacao em subagente ja protege o contexto principal, e por isso a pausa costuma cair entre
frentes, nao dentro de uma. Sem subagentes, a pausa e o unico mecanismo que resta: use a.

## Quando o pedido ja nomeia o artefato

As vezes o desenvolvedor nao pede uma investigacao: ele pede o resultado, ja decidido. "Cria
uma skill para gerar os relatorios, todo mundo erra isso." O fluxo continua o mesmo, com a
ordem invertida: o candidato vem primeiro e a investigacao existe para julga lo.

Quando a evidencia sustentar o pedido, siga. Quando nao sustentar, diga isso com os numeros e
proponha o destino que a evidencia sustenta, sem produzir o artefato pedido assim mesmo:
entregar uma skill sem processo observavel cria uma instrucao que sera obedecida como se
fosse verdade.

## Quando parar e perguntar

Pergunte, em vez de inferir, quando: o codigo mostrar dois padroes concorrentes e a escolha
entre eles mudar o que o agente deve fazer; a regra depender de contexto externo que o codigo
nao revela; a evidencia apontar para pratica que pode ser defeito recente e nao convencao
estabelecida. Agrupe as perguntas em um bloco so, no momento do plano.

Perguntar nao suspende a escrita do que ja esta comprovado. Registre o padrao com a contagem
dos dois lados e deixe a pergunta ao lado; parar tudo por uma decisao pendente e o caminho
mais curto para uma rodada sem entrega.

## Antipadroes

| Antipadrao | Por que falha |
|---|---|
| Terminar a rodada sem nenhuma skill porque nenhum achado "virou processo" | Processo nao aparece sozinho: ele so existe se alguem reconstruir a sequencia a partir dos exemplares |
| Em modo autonomo, escrever sem registrar o plano | O desenvolvedor recebe um diff sem saber o que foi decidido, o que foi descartado e por que |
| Em modo autonomo, remover ou reduzir regra existente sem perguntar | Autorizar aplicar autoriza acrescentar, nao autoriza tirar o que ja valia |
| Investigar so hipoteses a derrubar | Produz uma stack que diz o que nao assumir e nao ensina a implementar nada |
| Avaliar a arquitetura em vez de descreve la | O objetivo e coerencia com o sistema, nao adequacao a boa pratica externa |
| Descartar padrao recorrente por parecer antipadrao tecnico | Se e o que o sistema usa, e a convencao, e o agente precisa sabe la para nao destoar |
| Importar convencao de mercado como regra do repo | A stack passa a descrever um sistema imaginario e o agente entrega fora do padrao real |
| Descrever a arvore de diretorios em `AGENTS.md` | O agente enxerga a arvore sozinho; gasta contexto global sem informar nada |
| Promover pratica de tres arquivos a convencao do repositorio | Alcance sem lastro vira instrucao errada em todo o resto do codigo |
| Transformar dois padroes concorrentes em pergunta e nao escrever nada | Os dois padroes existem e sao conhecimento; a pergunta e sobre qual preferir daqui para frente |
| Guardrail escrito como proibicao | O sistema tem excecoes legitimas; alerta preserva coerencia, proibicao gera conflito com o codigo real |
| Deixar as secoes de contexto e dependencias vagas | Sao inventario do censo, nao regra: vago ali e falha da rodada, nao economia de contexto |
| Publicar comando que nao reproduz o proprio numero | A proxima medicao de conformidade le contradicao onde ha erro de comando e derruba artefato bom |
| Tentar descrever o interior de um sistema externo | Nao versionado, nao auditavel; o que se comprova e o uso local deste lado |
| Descrever a familia inteira a partir de exemplares de um diretorio so | O territorio mais organizado vira "o sistema", e a instrucao destoa em todos os outros |
| Aceitar um comando porque ele reproduz o proprio numero | Reproduzir e repetir o mesmo erro; um regex sem ancora reproduz para sempre e mede outra coisa |
| Contar inclusao como uso, definicao como chamada, ou linha comentada como ativa | Em codigo legado o morto convive com o vivo sem marca, e so as duas contagens separam |
| Afirmar consequencia de execucao sem ter executado nada | "Falha silenciosamente" e suposicao; o codigo costuma tratar o caso, e de um jeito que muda a instrucao |
| Escrever afirmacao negativa ampla a partir de uma busca so | Alguem vai confiar nela para nao procurar, e e ali que estava o que se procurava |
| Restringir a busca a uma extensao e concluir alcance | O instrumento deixa de enxergar metade do sistema, e a conclusao herda a cegueira |
| Contar biblioteca de terceiros versionada como convencao do time | O padrao medido passa a ser o da dependencia, e o agente imita o que veio de fora |
| Escrever no artefato como o achado foi medido, em vez do que o sistema e | O agente recebe o relatorio da rodada onde precisava do fato tecnico, e a frase envelhece a cada commit |
| Mandar seguir o padrao de um arquivo nomeado | O arquivo e apagado ou renomeado e a instrucao fica sem conteudo; o padrao precisa estar escrito, o exemplar so confirma |
