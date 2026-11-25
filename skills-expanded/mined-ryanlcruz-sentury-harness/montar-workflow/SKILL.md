---
name: montar-workflow
# Como a skill aparece na lista do "o que sei fazer".
vitrine:
  grupo: 'Trabalho'
  rotulo: 'conduzir trabalho de várias fases até fechar'
description: "Conduzir trabalho que atravessa dias: dividir em fases, parar nos pontos certos, marcar o que fechou e retomar de onde parou. Pode receber automação separada quando a pessoa pedir."
version: 1.1.0
author: Sentury
license: MIT
metadata:
  # `gatilhos` sao regex e o MAIS ESPECIFICO ganha, entao aqui entra so frase
  # que nao pertence a mais ninguem. As `tags` ficaram de fora de proposito:
  # a descoberta difusa soma ponto por palavra solta, e "plano" ou "tarefa"
  # roubavam a skill de plano de acao do setor e a do terminal.
  gatilhos:
    - 'acompanh\w* at[eé] (fechar|terminar|resolver)'
    - 'conduz\w* esse trabalho'
    - 'retoma\w* de onde (paramos|parou)'
    - 'divid\w* em fases'
    - 'isso vai levar (dias|semanas)'
    - 'toda (semana|segunda|ter[çc]a|quarta|quinta|sexta|manh[ãa]|noite).{0,40}(analis|atualiz|process|envi|rod)'
    - 'todo dia.{0,40}(analis|atualiz|process|envi|rod)'
  category: cognitive
---

# Montar e conduzir um workflow

## O plano é o SEU roteiro, não a lista de afazeres do usuário

Antes de qualquer coisa: cada tarefa é um passo que **você** vai executar, com
uma ferramenta sua. Não é dever de casa para a pessoa.

Um caso real, e o erro é fácil de cometer. Pediram "quero um workflow de buscar
vagas de TI" e saiu isto:

```
- [ ] 1.1 Escolher 3-5 plataformas principais
- [ ] 1.3 Preparar portfólio e CV
```

Nenhum dos dois é executável por você: são instruções para o usuário. O plano
virou um documento de conselhos com caixinhas, e ele nunca vai ser marcado,
porque quem marca é você e você não fez nada.

O mesmo pedido, como roteiro de agente:

```
- [ ] 1. Levantar as vagas
  - [ ] 1.1 Buscar na web as vagas de TI dos últimos 7 dias  (buscar_web)
  - [ ] 1.2 Extrair de cada anúncio: empresa, stack, link, data
  _Requisito: ter a lista antes de filtrar_
- [ ]! 2. Você confirma o recorte? (nível, stack, remoto)
  - opção: júnior, Python, remoto
  - opção: pleno, qualquer stack, híbrido
- [ ] 3. Entregar
  - [ ] 3.1 Montar a planilha com o que passou no filtro  (export_xlsx)
```

Se uma tarefa não tem ferramenta que a execute, ela não é tarefa: ou vira
**portão** (você pergunta e a pessoa decide), ou vira frase na resposta, ou não
entra. Teste rápido para cada linha: *qual ferramenta minha fecha isto?* Sem
resposta, a linha está errada.

O plano já existe em disco, com `criar_plano`, `ver_plano` e `status_da_tarefa`.
O que decide se ele ajuda ou atrapalha não é a ferramenta — é o julgamento de
**quando criar**, **como dividir** e **quando marcar**. É disso que esta skill
trata.

Um plano que ninguém marca vira documento desatualizado, e documento
desatualizado atrapalha mais do que a ausência dele.

## Plano, workflow e agendamento são três coisas

A diferença não é o tamanho do checklist nem a presença de cron:

- `criar_plano`: caminho de uma execução única, que começa uma vez e fecha;
- `criar_workflow`: trabalho persistente de várias etapas, com retomada,
  portões e histórico; por padrão começa manualmente depois da aprovação;
- agendamento: automação opcional e separada. Só existe quando a pessoa pede
  explicitamente horário ou recorrência.

Workflow **não precisa de gatilho**. Não procure cron para justificar um
workflow e não transforme prazo, dependência ou próxima fase em agendamento.
Se a pessoa disser "toda segunda às 8", aí sim envie o `gatilho` opcional a
`criar_workflow`; fora disso, omita o campo.

Nunca use `executar_python`, `escrever_arquivo` nem outro script para fabricar
o `.md` do plano ou workflow. O Markdown é armazenamento interno com estado e
histórico; escrever o arquivo por fora pula validação, card, aprovação e
retomada.

Criar é **propor**, não autorizar. Depois de apresentar os passos, espere a
pessoa escolher **Aprovar e começar** ou **Ajustar** no card. Se houver um
agendamento pedido explicitamente, ele nasce pausado e só arma o relógio após
a aprovação.

## Primeiro: isto merece um plano?

Crie um plano quando **pelo menos uma** destas for verdade:

- o trabalho tem **mais de uma fase** — existe algo que precisa fechar antes de
  outra coisa começar;
- tem passo que **altera alguma coisa** e vai precisar de autorização;
- **não termina hoje**: tem medição futura, prazo, ou você prometeu voltar.

Se nenhuma for verdade, responda direto. "Quanto vendemos em setembro" não tem
fase, não altera nada e termina na resposta — um checklist de três itens ali só
adia o que o usuário pediu.

Em dúvida entre plano e resposta direta, escolha a resposta direta. O custo de
não criar um plano é escrever um depois; o custo de criar um desnecessário é
ensinar a pessoa a ignorar todos os próximos.

## Dividir em fases

**Fase é o que precisa fechar antes da próxima começar.** Se duas "fases" podem
rodar ao mesmo tempo, elas são uma só.

O `id` é escrito no arquivo (`2.1`) e é ele que o histórico segue, então a
numeração hierárquica é o que separa fase de tarefa:

```
- [ ] 1. Entender a queda
  - [ ] 1.1 Separar por loja e por semana
  - [ ] 1.2 Cruzar com as devoluções do período
  _Requisito: R1 — saber onde a queda se concentra_
- [ ] 2. Provar que a causa é essa
  - [ ] 2.1 Testar se a queda some sem a loja suspeita
  - [ ]* 2.2 Ouvir cinco comentários abertos
  _Requisito: R2 — não agir sobre causa não confirmada_
```

Seis marcas do formato que valem usar, porque o arquivo já as entende:

- **`!` depois do colchete** marca o item como **portão**: nada depois dele
  acontece enquanto ele não for resolvido. `- [ ]! 4. Você aprova subir?`. Sem a
  marca o plano é uma lista, e lista não tem fase — o passo 5 roda com a decisão
  do 4 ainda pendente. Quem lê o plano vê `travado` e vê por quem.
- **Linha `- opção:` sob um portão** dá as respostas possíveis. Portão sem
  opção é pergunta aberta no meio da execução, e quem responde precisa adivinhar
  o que vale. Duas ou três, nas palavras de quem decide.
- **Agendamento não mora numa tarefa.** Não escreva `_Agenda:` no checklist.
  Se a pessoa pediu recorrência explicitamente, o `gatilho` opcional vai em
  `criar_workflow`; sem esse pedido, não há cron.
- **`*` depois do colchete** marca o item como **opcional**. Use para o que
  melhora a confiança mas não bloqueia. Sem essa marca, o agente corta o que não
  devia quando o tempo aperta — ou faz o supérfluo achando que era obrigatório.
- **Linha começando com `_`** guarda o **requisito**: por que este item existe, e
  contra o que ele responde. Quem executar o item 2.1 depois de dois dias precisa
  saber o que estava tentando provar.
- **Indentação** cria o nível. Duas fases com quatro tarefas cada leem melhor que
  oito itens soltos.

Tamanho: entre 5 e 15 tarefas. Menos que isso normalmente não precisava de plano;
mais que isso é sinal de que a primeira fase deveria ser "descobrir o que é
preciso fazer".

## Onde colocar portão

Portão é um ponto onde você **para e pergunta**, com `perguntar_usuario` — e que
fica marcado com `!` no checklist, para que parar não dependa de você lembrar.
Coloque portão em dois lugares, e só:

1. **Onde a resposta muda o caminho.** "Encontrei duas causas possíveis, uma leva
   a mexer no processo e outra no treinamento" — seguir sem perguntar é escolher
   pelo dono.
2. **Onde a ação altera o mundo dele.** Abrir ação com responsável nomeado,
   escrever em pasta do usuário, disparar mensagem.

Proporção que funciona: **cerca de três portões em dez tarefas**. Se cada passo
pede confirmação, a pessoa aprova no automático e o portão perde o sentido — que
é justamente proteger os dois ou três momentos que importam.

Descobrir a estrutura de um banco, contar linhas, montar um rascunho: nada disso
é portão.

## Quando marcar, e com que prova

Chame `status_da_tarefa` **assim que a etapa termina**, não no fim do turno.

Só marque `feito` com **prova positiva**:

| a tarefa era | a prova é |
|---|---|
| gerar um arquivo | o arquivo existe e tem conteúdo |
| consultar dado | a consulta voltou linhas (ou zero, e isso é o achado) |
| criar ação | a ação tem id |
| rodar script | o código de saída foi zero |

"Não deu erro" não é prova. Se você não consegue dizer o que prova que terminou,
a tarefa ainda não terminou — ou ela estava mal escrita.

Os outros estados também são informação:

- **`fazendo`** antes de começar uma etapa longa: quem abre o painel vê onde
  você está.
- **`falhou`** com uma `nota` dizendo **o que** falhou. O histórico é
  append-only: a tentativa que deu errado é evidência, não lixo.
- **`pulado`** quando um opcional foi dispensado — deixe registrado por quê.

## Quando a hipótese cai

Trabalho de investigação erra, e o plano precisa aguentar isso.

- Hipótese não se sustentou: **volte à fase anterior** e anote a hipótese
  descartada como tarefa marcada (`falhou`, com a nota). Continuar montando o
  entregável sobre uma causa não confirmada é o erro caro: causa errada com
  responsável nomeado custa mais do que demorar mais um dia.
- **Duas hipóteses seguidas caíram: pare e pergunte.** Nesse ponto o que falta
  provavelmente é contexto que só o dono tem, e uma terceira tentativa às cegas
  gasta o tempo dele.

## Retomar depois

O plano fica em disco justamente para o trabalho sobreviver à conversa. Numa
sessão nova, antes de refazer qualquer coisa:

```
ver_plano()                      # que planos existem e quanto falta
ver_plano(plano="queda-de-vendas")  # em que item parou, e o que já falhou antes
```

Recomeçar do zero um trabalho que já tinha três fases fechadas é o desperdício
que o plano existe para evitar. Leia antes de propor.

## Quando o trabalho é um workflow

Workflow é um trabalho que atravessa etapas ou turnos e precisa ser retomado
sem perder decisões, portões e evidências. Ele não precisa se repetir nem
disparar sozinho.

Exemplo de chamada conceitual:

```
criar_workflow(
  nome="migracao-do-banco",
  porque="conduzir a migração com validação e possibilidade de retomada",
  passos=["Inventariar dependências", "Preparar a migração", "Validar", "Encerrar"]
)
```

Não chame `agenda` junto. Agendamento não é parte obrigatória do
workflow. Se, além do workflow, a pessoa pedir recorrência, use o `gatilho`
opcional da ferramenta; isso deixa a automação visível e editável em
Agendamentos sem duplicar chamadas.

Antes de propor:

- se a fonte ou o formato são incertos, inclua um passo verificável para
  validá-los; não invente acesso que ainda não existe;
- escreva passos que o agente consegue executar com ferramentas reais;
- só mencione gatilho quando a pessoa realmente tiver pedido recorrência;
- pare após criar a proposta. A pessoa aprova ou ajusta; não ative em silêncio.

Para conferir um workflow já criado, use `ver_workflow`. Quando existir um
agendamento separado, dias, horário, prompt, pausa e exclusão são editados na
página de Agendamentos — não reescreva o arquivo à mão.

## O que não escrever no plano

O plano diz **o que precisa ficar pronto**. Ele não diz **em que ordem pensar**.

Item bom: "Provar que a queda some sem a loja Curitiba".
Item ruim: "Analisar cuidadosamente os dados passo a passo antes de concluir".

O segundo não é verificável — não dá para marcar `feito` com prova — e roteiro de
raciocínio dentro do plano engessa o trabalho em vez de organizá-lo. Escreva
entregas, não instruções de pensamento.
