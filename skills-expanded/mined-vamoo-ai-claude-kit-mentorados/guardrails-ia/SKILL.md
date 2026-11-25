---
name: guardrails-ia
description: >-
  Guard-rails de agente de IA que fala com pessoa real (WhatsApp, chat, bot): o
  que pode afirmar, opt-out permanente, escalar pra humano, IA vs humano no
  canal. Para construir ou revisar bot de cliente e antes de ligar o disparo.
  Só dispara quando você chama: /kit-vamoo:guardrails-ia.
disable-model-invocation: true
---

# Guard-rails da IA que fala com cliente

Um agente que responde lead comete dois erros que teste de fluxo não pega:
afirma coisa que a empresa não sustenta, e continua falando com quem mandou
parar. Nenhum dos dois aparece como erro no log — aparecem como conversa
normal, e chegam até você pelo cliente ou pelo jurídico.

Prompt pedindo "não invente" não é controle. Controle é lista fechada,
verificada fora do modelo.

## Alegações: allowlist, não instrução

Duas listas na config do projeto (arquivo único, gitignored, com `.example`
espelhado — ver skill `baseline`, pilar 07), nunca soltas dentro do prompt:

```json
{
  "alegacoes_verificadas": [
    "Integração com WhatsApp e CRM na mesma conta",
    "Implantação típica em 2 semanas — média das últimas 6 entregas"
  ],
  "alegacoes_bloqueadas": [
    "Aumenta a conversão em 30%",
    "Aprovação garantida",
    "Somos parceiros oficiais da Meta"
  ]
}
```

- **Verificada** = tem prova hoje: página no site, contrato, número que você
  mostra. É a única coisa que a IA pode afirmar.
- **Bloqueada** = o que você quer dizer e ainda não comprovou. Fica bloqueada
  até virar prova — não até parecer razoável.
- A lista entra no system prompt **e** vale como filtro na saída. Prompt
  sozinho vaza: o modelo parafraseia ("costuma dobrar o resultado" não está na
  lista, mas passa por qualquer instrução).
- Número, prazo, preço, taxa, garantia, percentual e superlativo que não
  estejam textualmente na lista não saem. Teste fácil: a resposta tem dígito ou
  "%"? Então esse dígito precisa ter origem na lista ou no dado do próprio
  lead.
- Saída reprovada não vira resposta genérica em silêncio: vai pra revisão
  humana, junto com o texto que o modelo tentou mandar. É esse log que mostra
  qual alegação falta comprovar — a lista bloqueada é um backlog, não uma
  lixeira.

Nunca: prometer aprovação de cadastro, inventar parceria ou relação
societária, fingir ser cliente/terceiro pra arrancar resposta.

## Pedido de parar é estado, não interpretação

"Não quero", "para", "me tira daí", bloqueio, denúncia → o contato entra em
`nao_contatar` **permanente**:

- sem follow-up, sem reentrada por outra campanha, **por nenhum canal** — a
  lista é por pessoa (telefone/e-mail/perfil), não por campanha;
- a checagem roda na montagem da fila **e** imediatamente antes do envio (a
  fila de hoje foi montada ontem, e o opt-out chegou no meio);
- gravada com origem e timestamp. Quem só tira a linha da fila perde a prova de
  que respeitou o pedido.

## Escalar pra humano é um resultado, não uma falha

A classificação da resposta precisa de um rótulo `precisa_humano`, e ele tem
que ter destino de verdade: fila visível, notificação, dono. Casos que sempre
caem nele: reclamação, ameaça de jurídico, pedido de algo que a IA não pode
afirmar, preço fora da tabela, resposta que a IA classificou como ambígua duas
vezes seguidas.

Agente sem escalação não tem "não sei" — tem alucinação bem-educada.

## Propriedade de canal: quem responde não é quem grava

Três emissores acabam disputando o mesmo fio: a IA, o humano que assumiu e a
rotina automática (follow-up, aviso, cron). O jeito comum de arbitrar é um
interruptor de pausa no começo do fluxo — e ele abre um buraco silencioso:
**o guard corta antes do nó que grava o inbound**, então tudo que o cliente
escreve enquanto o humano conduz não existe no seu banco. Some justamente o
trecho que alguém vai querer auditar depois.

A causa é modelar pausa como interruptor do fluxo em vez de propriedade do
canal.

**A regra: propriedade de canal decide quem RESPONDE, nunca quem GRAVA.**

Dois campos independentes, nunca um só:

- **estágio do funil** — `novo`, `qualificado`, `proposta`, `ganho`… (onde o
  negócio está)
- **dono do canal** — `ia` · `humano` · `api_oficial` · `aguardando_inbound` ·
  `nao_contatar` (quem pode falar agora), com `dono_desde` e `dono_motivo`

- Ordem obrigatória: **gravar inbound → resolver dono → decidir envio.** Todo
  guard de pausa fica depois da gravação.
- Quem não é dono não envia. Humano assumiu → a IA não manda nem "posso ajudar
  em mais alguma coisa", e o follow-up agendado também respeita o dono; senão o
  cron atropela a conversa humana às 9h da manhã.
- Handoff é `UPDATE` explícito no dono, com motivo e timestamp — não um
  `pausado_ate` que expira sozinho e devolve o fio pra IA no meio de uma
  negociação.
- Estágio e dono mudam por razões diferentes: `ganho` com dono `humano` é
  normal. Espremer os dois num campo só obriga a escolher entre perder o funil
  e perder o controle de quem fala.
- Nunca dois emissores no mesmo fio. Se duas rotas podem enviar, a trava é o
  dono — não a esperança de que não coincidam.

**Prova (2 minutos, e é o teste que ninguém faz):** transfira uma conversa pra
humano e mande 3 mensagens como cliente. As 3 têm que aparecer na sua tabela de
mensagens, e nenhuma resposta automática pode sair. Log com 0 mensagens = o
guard está antes da gravação.

## O resto dos guard-rails mora em outra skill

- Teto de gasto de IA e custo por lead → skill `baseline`, pilares `04` e `06`.
- Config de negócio fora do código → skill `baseline`, pilar `07`.
- Antes de ligar o disparo de verdade → skill `verificacao`, § efeito colateral
  externo (simulado → dry-run → smoke autorizado).
