---
name: usage-monitor-visual-options
description: Generate N animated HTML visual options side by side for a Usage Monitor visual or animation change, so the user picks a direction before any Kotlin. Use for "opções", "modelos", "exemplos em HTML", "me dá N versões", or /usage-monitor-visual-options.
---

# Usage Monitor — opções visuais em HTML

O usuário escolhe mudança visual **vendo**, nunca no escuro: duas rodadas de visual feito direto no
Kotlin foram recusadas ("muito 2D", "disco chamativo"), e todas as rodadas com opções lado a lado
saíram escolhidas de primeira. O objetivo dele é a HUD "mais bonita, tema espacial", sem perder a
leitura do dado. Esta skill recebe **o que mudar** e
**quantas opções** (ex.: `/usage-monitor-visual-options animação do balão 5`) e entrega N protótipos
animados lado a lado, no tema vigente, para ele escolher — e só depois disso vem o Compose.

Sem número no pedido, faça **5**. Com menos de 3, faça 3.

## 1. Antes de desenhar

1. Ler o tema vigente e o histórico do que já foi escolhido e recusado — a tabela no fim desta skill
   é a fonte. **Não reproponha uma opção já recusada com o mesmo nome ou o mesmo gesto.**
2. Ler a seção da tela em [`docs/hud-notch.md`](../../../docs/hud-notch.md) (HUD) ou em
   [`docs/presentation.md`](../../../docs/presentation.md) (demais telas), e o contrato da primitiva em
   `docs/design-system/components/**/*.prompt.md`. A skill `usage-monitor-design` tem a precedência.
3. Olhar o que existe hoje no código (tempo, curva, o que anima) — vira o card **"Hoje
   (referência)"**, tracejado, quando a mudança substitui algo.
4. Se o usuário mandou print, reproduzir o conteúdo real dele (textos, contas, valores) no mockup.

## 2. Regras de criação (valem para toda opção)

- **Vocabulário Gargantua**: luz quente (`--gargantua-gold #E8AE63`, `--gargantua-hot #FFF0CB`,
  `--gargantua-ember #B4501E`), núcleo escuro (`#030508`), plasma com núcleo claro, clarão, ondas
  finas, lente, disco com Doppler (quente de um lado, brasa do outro). Cada opção nomeada por um
  fenômeno ("B3 · Jato relativístico", "D5 · Horizonte de eventos") com prefixo de letra da rodada.
- **Dado nunca anima errado**: comprimento de barra/arco não cresce por efeito, número não passa do
  valor (sem overshoot/rebote), cor nunca informa sozinha. Efeito é por cima do dado, não no lugar dele.
- **Cenário discreto**: o usuário recusou efeito "chamativo" (disco forte, 6 faixas). Efeito não
  compete com o dado nem com o cometa azul de sessão.
- **Finito por padrão**: transição tem duração em ms (tipicamente 180–800). Animação infinita só se o
  pedido for de estado contínuo, e ela mora atrás de `AppMotionPolicy.continuous` no app.
- **"Reduzir animações" = corte seco** em todas; diga isso no texto.
- **Geometria não muda por quadro**: nada de janela ou notch redimensionando; revelar é recorte ou
  desenho por cima.
- Opções **distintas entre si** no gesto (não cinco variações de fade). Se duas ficarem parecidas,
  troque uma.
- Mesma animação aplicada a todas as superfícies pedidas (ex.: balão da conta **e** da engrenagem).
- **Opções só quando competem pelo mesmo lugar.** Quando o pedido é um produto com várias peças
  complementares (rodada AG, modo terminal), a galeria de opções soltas confunde: mostre a proposta
  fechada, tela por tela, e deixe a escolha para o que de fato disputa a mesma tela.

## 3. Como montar o HTML

- Um arquivo em `build/gargantua-preview/<tema>-options.html` (pasta ignorada pelo git), fundo
  escuro, IBM Plex Mono/Consolas, um card por opção com: nome curto, 1–3 frases do que acontece em
  cada fase, tempos em ms. Card "Hoje (referência)" tracejado primeiro.
- **Anel real**: colar [`assets/gargantua-ring.js`](assets/gargantua-ring.js) inline (é o mesmo
  desenho do `AppGargantuaRing`; `drawRing(ctx, acc, phase, overrides)`), anel de 64 px (1× o app) —
  ou 1,5× quando o foco é o próprio anel.
- **Loop sozinho**: cada palco roda fechado → animando → parado → saindo, com a fase escrita no canto
  ("abrindo · 520 ms"). Botão/checkbox **"câmera lenta ×3"** e, quando fizer sentido, "Atualizar agora".
- Um hook de depuração `window.FREEZE = t` que congela todos os palcos no quadro `t` ajuda a conferir.
- Exemplo completo que funcionou: [`assets/example-balloon-options.html`](assets/example-balloon-options.html)
  (5 aberturas de balão + referência, dois palcos por opção).

## 4. Conferir e mostrar

1. Abrir o arquivo no painel do navegador (`mcp__Claude_Browser__*`), ler o console (sem erro) e
   tirar 2–3 screenshots no meio das animações (`FREEZE`) para ver que cada efeito aparece de fato.
2. **Mostrar no chat**: o usuário prefere ver ali. Publicar como widget (`show_widget`, largura
   680 px — reorganizar em grade ou um palco com seletor de opção) e também mandar o arquivo com
   `SendUserFile` (display render).
3. Na resposta: uma linha por opção com o gesto e o tempo, e perguntar a direção (pode combinar
   opções). Não comece o Kotlin antes da escolha.

## 5. Depois da escolha

- Registrar a escolhida e as não escolhidas na tabela abaixo, **no mesmo commit** da implementação
  (nada disso vai para a memória: a skill é a fonte).
- Implementar como **função pura de quadro** em `commonMain` (padrão `GargantuaTransition.kt`,
  `GargantuaBalloonJet.kt`, `GargantuaRoll.kt`) com teste em `commonTest`; durações em
  `AppGargantuaTokens` com espelho em `docs/design-system/tokens/motion.css`; tween via
  `appTweenSpec` (vira `snap()` com animação reduzida).
- Teste de pixel da tela no arquivo de teste dela; GIF em `GargantuaPreviewGenerator`
  (`gradlew.bat generateGargantuaPreview`), conferido quadro a quadro.
- Docs no mesmo commit: `docs/hud-notch.md` (ou `presentation.md`), o `*.prompt.md` da primitiva,
  o protótipo `docs/planos/prototipo-visual-opencode.html` e o kit `.jsx` quando houver.
- `gradlew.bat allTests`, e **perguntar antes de commit/push** (skill `usage-monitor-commit-push`).

## Histórico das rodadas (escolhidas e recusadas)

| Rodada | Escolhida | Não escolhidas / recusadas |
|---|---|---|
| Arcos de cota | C · vidro com plasma | tubo iluminado, órbitas 3D inclinadas |
| Cenário | disco discreto (1 faixa, Doppler) | disco forte de 6 faixas ("chamativo") |
| Ativar API / abrir HUD | S1 · onda de choque (1100 ms) | S2 supernova, S3 acreção |
| Desativar API | C2 · colapso com clarão (480 ms) | C1 espaguetificação, C3 evaporação de Hawking, C4 horizonte engole |
| Coleta | R1 · ondas gravitacionais (1300/800 ms) | varredura de sonda, recarga de plasma, tique-taque |
| Abrir balão (conta e engrenagem, e troca de anel) | B3 · jato relativístico (520/240 ms) | B1 onda de choque, B2 lente gravitacional, B4 luz de acreção no contorno, B5 ondas gravitacionais |
| Dado novo (percentuais e pílula) | D5 · horizonte de eventos (480 ms, cascata 50 ms) | D1 desvio para o vermelho, D2 lente, D3 plasma que conta, D4 onda gravitacional |
| Modais: abrir, fechar e apresentar dados (todas as janelas e o `AppDialog`) | E9 · filamentos de plasma (680/220 ms) | E1 jato relativístico, E2 horizonte de eventos, E3 varredura do disco, E4 condensação da nebulosa, E5 captura orbital, E6 farol do pulsar, E7 buraco de minhoca, E8 malha do espaço-tempo, E10 estrela de nêutrons |
| Balão da conta, indicador de execução e balão da engrenagem | F10 · cometa com cauda de íons (restante em destaque, cauda de íons, versão e contagem em linha própria; o botão dentro do aviso não coube e ficou abaixo) | F1 telemetria de sonda, F2 jatos polares, F3 companheira binária, F4 anel de fótons, F5 acreção de partículas, F6 anel de detritos, F7 sinal de rádio, F8 espiral de lente, F9 coroa de plasma |
| Banner do README (`img/banner.svg`, SVG+CSS que toca uma vez; o GitHub não roda JS) | G5 · cometa com cauda de íons (1500 ms; a linha parada virou `img/divider.svg`) | G1 horizonte de eventos, G2 jato relativístico, G3 varredura do disco, G4 anel de Einstein |
| Ícone do app, só tema (estático; 128/48/32/16 px e barras de tarefas clara e escura) | nenhuma — o usuário pediu uma rodada com o nome | H1 horizonte de eventos, H2 anel de cota, H3 monograma no disco, H4 anel de Einstein, H5 jato relativístico, H6 cometa de íons, H7 o notch, H8 medidor do espaço-tempo, H9 eclipse, H10 órbitas em U |
| Ícone do app com o nome (`tools/brand/render_icons.py`) | I10 · nome por tamanho (≥ 96 px USAGE MONITOR, 32–64 px U·M, ≤ 24 px só o núcleo) | I1 U de acreção, I2 M de horizonte, I3 UM entrelaçado, I4 U medidor, I5 "um" no horizonte, I6 U·M (virou a faixa do meio da I10), I7 U de cometa, I8 notch em U, I9 M de sinal |
| Trilha de cota sem projeção (era o tracejado cinza; laço contínuo atrás da política) | J7 · anel de detritos (órbitas de 16 s na linha central, laço de 128 s com voltas inteiras) | J1 poeira de acreção, J2 contas de plasma, J3 tracejado Doppler, J4 tubo oco, J5 graduação com radar, J6 onda gravitacional, J8 rastro que se perde, J9 névoa de nebulosa, J10 sonda em órbita; a primeira rodada, estática, foi recusada ("queria com animação") |
| Desligar uma API: o anel sai e o notch acompanha (antes: C2 480 ms e o notch saltando no fim) | K1 · colapso lento, depois assenta (850 + 450 ms; notch desenhado recolhendo, janela só no fim) | K2 maré (tudo junto, 950 ms), K3 onda gravitacional que fecha, K4 as vizinhas ocupam a vaga |
| Muitas contas: quando a faixa completa não cabe na borda | L1 · borda lateral pode mais (80%; em cima e embaixo continua 45%) | L2 compacta só quem está em dia, L3 degrau sem pílula, L4 duas colunas na lateral |
| Corpo do notch mais alinhado ao Gargantua (era a laje plana `#1B1818`) | M1 · horizonte de eventos (núcleo escuro no tema escuro, anel de fótons de 1dp com Doppler, respira em 6 s) | M2 disco na borda da tela, M3 lente gravitacional, M4 poço do espaço-tempo, M5 luz de acreção, M6 fóton no contorno, M7 jatos entre as contas, M8 silhueta de maré, M9 vidro fumê, M10 órbita que liga as contas |
| Histórico — faixa ativa das janelas 5h/7d/30d (#382; telas estáticas, galeria única `docs/planos/issues-381-388-visual/`) | N6 · degraus de consumo (fundo claro + chave sobre o trecho em que o uso subiu, legenda em frase) | N1 faixa na linha do tempo, N2 colunas na tabela (a coluna "Ativa" entrou junto), N3 cartão por janela, N4 Gantt de janelas, N5 relógio da janela, N7 resumo em frase, N8 calendário de atividade, N9 três trilhos alinhados ao agora, N10 marcos da janela |
| Modais de sessões CLI Anthropic e Codex no mesmo padrão (#384; estática, galeria única) | O1 · evolução mínima (coluna e bloco Vazão, Codex com Resumo e PDF, sem botão de atualizar) | O2 mestre e detalhe, O3 cartões de sessão, O4 uma janela com duas fontes, O5 trilhas no tempo, O6 agora em destaque, O7 agrupado por projeto, O8 relatório contínuo, O9 filtros laterais, O10 painel de métricas |
| Comparação entre modelos e APIs (#386; tela nova, estática, galeria única) | P7 · mapa de calor (valor sobre o máximo da coluna, número sempre escrito, cor da fonte) | P1 tabela com barras, P2 versus em cartões, P3 custo × velocidade, P4 ranking por métrica, P5 perfis paralelos, P6 linhas no tempo, P8 duelo A × B, P9 eficiência de custo, P10 leitura automática |
| HUD no navegador da rede local (#388; página web + seção em Configurações › Rede, estática, galeria única) | R3 · grade de anéis (anel Gargantua a 2×, linhas de cota, grade responsiva) | R1 réplica da HUD, R2 lista de contas, R4 tabela compacta, R5 uma conta por tela, R6 abas por API, R7 pior risco primeiro, R8 linha do tempo de reinícios, R9 barras leves, R10 modo parede |
| Bot do Telegram nas Configurações (#387; seção na aba Alertas, estática, galeria única) | Q10 · configuração e conversa (campos à esquerda, conversa com o /status real à direita) | Q1 canal dentro de Alertas, Q2 integrações em Rede, Q3 assistente em 3 passos, Q4 status e registro, Q5 matriz evento × canal, Q6 pareamento por QR, Q7 comandos com permissão, Q8 prévia da mensagem, Q9 linha compacta por canal |
| Histórico — janelas e horas (#392; estática, galeria única `docs/planos/issues-392-393-visual/`) | S9 · lista de janelas e detalhe (curva, faixa ativa e horas só da janela escolhida; menu abaixo de 600dp) | S1 abas da janela, S2 abas por assunto, S3 rótulos que desambiguam, S4 período dentro do gráfico, S5 tabela com trilhos, S6 barras com valor escrito, S7 legenda que acompanha o zoom, S8 mapa de calor dia × hora, S10 dicas e glossário em tudo |
| Detalhe de sessão CLI — paridade Codex × Claude (#393; estática, galeria única `docs/planos/issues-392-393-visual/`) | T3 · grade de gráficos 2×2 (Claude: contexto, cache, saída, custo; Codex: contexto, cache, saída, vazão) | T1 paridade mínima, T2 abas no detalhe, T4 um gráfico com métrica escolhida, T5 cabeçalho compacto e avisos agrupados, T6 linha do tempo combinada, T7 tabela de turnos rica, T8 duas colunas, T9 comparada com suas sessões, T10 seções recolhíveis |
| HUD no navegador — movimento (#394; galeria única `docs/planos/issues-394-396-visual/`) | U5 · paridade + próxima leitura (plasma e cometa contínuos, ondas R1 e horizonte D5 na coleta nova, ponto dourado e filete até a releitura) | U1 paridade com a HUD (virou a base da U5), U2 só eventos, U3 só contínuo, U4 paridade + entrada com onda de choque |
| Respostas do bot do Telegram (#396; galeria única `docs/planos/issues-394-396-visual/`) | W5 · W1 + botões na mensagem (cartão por conta com barra de 10 células, risco em emoji e palavra; teclado Atualizar, Silenciar 1h, Limiares; menu por `setMyCommands`) | W1 cartão por conta (virou a base da W5), W2 tabela monoespaçada, W3 bloco por conta com tempo até o reinício, W4 pior primeiro com o resto recolhido |
| Card "Bot do Telegram" nas Configurações (#396; estática, galeria única `docs/planos/issues-394-396-visual/`) | V2 · três passos numerados (token, pareamento com Copiar e Abrir no Telegram, teste; exemplo recolhido) | V1 comando com Copiar e prévia real, V3 pareamento em foco, V4 guia de comandos no lugar da conversa, V5 faixa de status e prévia larga |

| Configurações — organizar a aba Geral (#399; estática, galeria única `docs/planos/issues-398-399-visual/`) | X1 · Aparência e Sistema viram abas (exceção à regra do enum, aprovada) + X10 · prévia ao vivo do notch na Aparência | X2 sub-abas na Geral, X3 painéis recolhíveis com resumo, X4 árvore com âncoras, X5 tema numa janela própria, X6 duas colunas, X7 busca nas Configurações, X8 aba "Sobre", X9 navegação por assunto em grupos |
| Bot do Telegram — funções novas (#398; estática, galeria única `docs/planos/issues-398-399-visual/`) | Y1 resumo diário, Y2 aviso de reinício de cota, Y4 uma conta por vez, Y5 painel fixado ao vivo, Y6 gráfico das últimas 24 h, Y8 controle remoto | Y3 `/custo` e orçamento do mês, Y7 sessões CLI ativas e travadas, Y9 alerta com ação na mensagem, Y10 relatório semanal em PDF |
| HUD — recolher e expandir a barra (#400; modo opcional pelo alfinete, parada vira faixa de 10dp com um ponto de risco por conta) | Z2 · íris do eclipse (disco do meio da faixa revela o notch, fio dourado na borda; 420/240 ms, intenção de 200 ms) | Z1 ejeção coronal, Z3 aglomerado que acende, Z4 terminador, Z5 foco do telescópio, Z6 precessão do eixo, Z7 migração planetária, Z8 aurora, Z9 nebulosa bipolar, Z10 clarão de raio gama, Z11 mosaico do interferômetro, Z12 camadas da atmosfera, Z13 rolamento na órbita, Z14 vela solar, Z15 telescópio que estende |
| Bot do Telegram — 30 funções novas (#408; estática, galeria única `docs/planos/issue-408-visual/`; Y3, Y7, Y9 e Y10 ficaram fora por decisão do usuário) | **todas**, AA1 a AA30 (o usuário aprovou a rodada inteira) | nenhuma |
| Análise da sessão no bot e no app (`/analise` e ação "Análise" no card/balão; estática, galeria única `docs/planos/analise-sessao-visual/`) | **todas**, AB1 a AB15, mais área de análises no menu, menu por categoria e idioma do app em tudo | nenhuma |
| Guia de introdução e dica do dia (#411; galeria animada `docs/planos/issue-411-visual/`) | AC4 · carrossel ilustrado (ressalva do usuário: o mockup saiu diferente do app — no Kotlin a ilustração é a demo real da Ajuda e a moldura são as primitivas; sem emoji) | AC1 holofote orbital, AC2 constelação de funções, AC3 lista de primeiros passos, AC5 um dia com o app, AC6 guia dentro do notch, AC7 piloto automático, AC8 trilhas por perfil, AC9 anatomia do anel, AC10 central de descobertas |
| Janela "Análise" remodelada, com atualização ao vivo (estática, galeria única `docs/planos/analise-modal-visual/`) | AD1 · painel único (as duas janelas lado a lado, 24 h com tok/s, intervalos e antes × agora em tabela; o usuário pediu tempo real: relê a cada coleta e a cada 30 s) | AD2 curva da janela, AD3 espelho 5h \| semanal, AD4 régua de ritmo, AD5 abas por pergunta, AD6 mestre e detalhe, AD7 grade de indicadores, AD8 relatório contínuo, AD9 mapa de calor em destaque, AD10 antes × agora sobreposto, AD11 escada de intervalos, AD12 leitura com prova, AD13 veredito no topo, AD14 instrumentos Gargantua, AD15 faixas sincronizadas 24 h, AD16 seletor de intervalo |
| Bot do Telegram — menu de comandos e respostas (estática, galeria única `docs/planos/telegram-bot-ae-visual/`; defeitos medidos no print: emoji de categoria repetido, sparkline virando retângulo, cota em 0% com três linhas) | AE4 · teclado fixo como controle (menu do Telegram só com `/status`, `/teclado` e `/ajuda`; teclado em duas páginas, ligado desde o pareamento) + AE7 · barra de quadrados por zona (dez emoji coloridos pelos limiares da conta, número em negrito, legenda no fim; a sparkline saiu) | AE1 central de comandos, AE2 ícone próprio por comando, AE3 áreas como títulos no menu, AE5 cartão em citação, AE6 uma linha por cota, AE8 painel em imagem, AE9 abas na mensagem, AE10 resumo no topo com conta parada numa linha |
| Vídeo de lançamento da 41.11 (EN e PT, legenda e voz Piper; galeria animada `build/gargantua-preview/video-v41-11-options.html`, roteiro `docs/planos/video-v41-11/roteiro.md`) | AF5 · mergulho no tesseract (assunto chega numa célula vindo do ponto de fuga em 900 ms e sai pela câmera em 700 ms; o usuário pediu 1 min e destaque ao processo do COSMIC) | AF1 órbita de apresentação, AF2 lente gravitacional, AF3 fita de acreção, AF4 jatos relativísticos |
| Modo terminal (pedido de usuário, #439–#441; estática; virou o design system `docs/design-system/cli/` e o protótipo `docs/planos/prototipo-modo-cli.html`) | Proposta fechada em vez de escolha: AG1 status, AG2 scripts, AG4 statusline do Claude Code, AG5 tmux, AG7 painel com abas (+ AG10 sessões, AG11 histórico, AG14 time), AG15 regra de cor, mais configuração completa e serviço sem tela (o usuário pediu "o modo CLI tem que suprir tudo"). A galeria de 15 opções soltas foi recusada por confusa: rodada com escolha só quando as opções competem | AG3 frases sem argumento (abriria o app), AG6 prompt do shell (precisa leitor sem JVM), AG8 mosaico btop, AG9 conversa por comandos, AG12 watch em linha, AG13 HUD de bolso |
| Análise e Histórico mais claros, no app (#463; estática, galeria única `docs/planos/issue-463-visual/`; o pedido foi "não tá claro o suficiente para mostrar os dados de forma clara e objetiva usando gráfico") | AH1 · diagonal do ritmo (eixo X = tempo da janela que passou, Y = cota usada, linha dourada que chega a 100% no reinício; anteriores atrás em cinza; frase embaixo) | AH2 colunas por janela, AH3 faixa do seu habitual, AH4 uma janela só "Usage" (Análise + Histórico), AH5 corrida esgotar × reiniciar. A curva com projeção (AD2) não foi reproposta, por ter ficado de fora na rodada AD |
| Análise e Histórico no modo terminal (#463; estática, mesma galeria) | **todas**, AI1 a AI5: tabela de janelas na aba Histórico (AI4) com o gráfico alto no `enter` (AI1), aba Análise (AI2) com a corrida (AI3), comando `analysis` (AI3) e a linha "tempo" no `status` e na linha de status (AI5) | nenhuma |
| Falha do servidor de time (#494; estática, galeria `build/gargantua-preview/team-error-options.html`; caso real: certificado TLS vencido) | AJ4 · caminho da conexão (etapa onde parou + trilha Endereço › Conexão › Certificado › Servidor › Chave/Token, aplicada às janelas de time, ações, Configurações, bot e terminal — o usuário lembrou das outras telas de time e a rodada virou proposta fechada) | AJ1 diagnóstico em frase (a classificação e o conselho entraram na AJ4), AJ2 última leitura mantida, AJ3 saúde do servidor com dono único, AJ5 texto por papel |

| Ícones das APIs "mais 3D" — só o preenchimento da marca (#517; galeria `build/gargantua-preview/api-marks-3d-options.html`) | nenhuma como cena — o pedido era a cena inteira; o relevo **AK1** entrou depois, na marca do anel, do card, do balão e da HUD web ("relevo no anel e nos cards") | AK2 extrusão de maré, AK3 cromo do horizonte, AK4 ouro de acreção, AK5 vidro com plasma, AK6 esfera do núcleo, AK7 luz do disco, AK8 plano do disco, AK9 rotação de pulsar, AK10 levitação, AK11 entalhe, AK12 paralaxe em camadas, AK13 cristal facetado, AK14 esmalte vítreo, AK15 fotosfera |
| Cena 3D de cada API: buraco negro e órbitas em volta da marca (#517; galeria `build/gargantua-preview/api-orbits-3d-options.html`) | AL1 · Gargantua de Interstellar (disco de trás dobrado por cima do horizonte, trás mais fraca, frente mais larga e por cima da marca) | AL2 giroscópio de órbitas, AL3 disco espesso, AL4 esfera e cometa, AL5 anéis planetários, AL6 precessão, AL7 jatos polares, AL8 espiral de acreção, AL9 estrela companheira, AL10 câmera em órbita, AL11 toro de poeira, AL12 casca de partículas, AL13 reflexo no horizonte, AL14 disco empenado, AL15 Gargantua completo |
| Ordenar colunas das sessões CLI (#537; galeria `prototipos/issue-537/index.html`) | AM1 · estrela-guia (seta só na coluna ativa, seta fraca no hover) | AM2 linha do horizonte, AM3 constelação fixa, AM4 coluna de luz, AM5 painel de bordo |
| Configurações › Time mais simples, chave por e-mail (#551; estática, galeria `prototipos/issue-551/`) | AN2 · etapas (1 Conexão, 2 Contas com e-mail e chave por linha, 3 Administração; um bloco aberto) | AN1 resumo e editar, AN3 tabela de contas, AN4 abas dentro do time, AN5 mínimo + avançado |
| Janela de sessões do Codex no padrão da Anthropic (#560; estática, galeria `prototipos/issue-560/`, cópia em `docs/planos/issue-560-visual/ao5.html`) | AO5 · espelho + eixo Agente (Respostas no lugar do Custo, Resumo pelo mesmo painel da Anthropic com o eixo sessão principal × subagentes) | AO1 espelho estrito (Custo em "—"), AO2 Respostas (virou a base da AO5), AO3 raciocínio, AO4 cota da janela (exigiria indexar `rate_limits`) |
| Minimizar uma conta na HUD sem desabilitar (#576; galeria `prototipos/issue-576/`) | AP1 · anã branca (botão Minimizar no balão, anel 28 dp com a cota em foco ao lado, 520 ms) | AP2 estrela distante, AP3 cinturão de asteroides, AP4 eclipse parcial, AP5 pílula de horizonte, AP6 lua na borda, AP7 pulsar, AP8 hibernação com despertar, AP9 arco nu, AP10 doca por arrasto |
| Emoji da conta maior (#585; galeria `prototipos/issue-585/`) | AR3 · lua em órbita (18 dp, não os 22 do protótipo: o respiro do notch aceita 6 dp de excesso) | AR1 selo ampliado no canto, AR2 emoji no rótulo, AR4 emoji na pílula, AR5 selo grande com auréola |
| Trocar a posição das contas na HUD (#584; galeria `prototipos/issue-584/`) | AQ1 · captura orbital por arrasto (pressão longa 300 ms, vizinhas por mola sem rebote, halo dourado) | AQ2 subir e descer no balão, AQ3 modo reorganizar, AQ4 lista em Configurações com prévia, AQ5 troca binária |
| HUD com vida — ícones que interagem quando em execução (#586; galeria `prototipos/issue-586/`) | nenhuma — o usuário recusou a rodada e refez o pedido: só o fundo, sem mexer no indicador de execução | AS1 paralaxe estelar, AS2 bolha de choque, AS3 vento estelar, AS4 cortina de aurora, AS5 constelação de atividade, AS6 cometa que migra, AS7 chuva de meteoros, AS8 atração de maré, AS9 alimentação pela borda, AS10 trânsito planetário, AS11 luz zodiacal, AS12 eco de luz, AS13 magnetosfera, AS14 correio de fótons, AS15 braços de galáxia |
| Fundo da HUD: estrelas em paralaxe, cada anel é buraco negro (#586; galeria `prototipos/issue-586-r2/`) | AT1 · paralaxe em três camadas, com o claro L1 · tinta densa | rodada `at1-claro/`: L2 brasa e ouro, L3 brilho em cruz, L4 poço tênue não escolhidas; AT2 arco de Einstein, AT3 espaguetificação rara, AT4 sombra e acúmulo de luz, AT5 arrasto do referencial, AT6 desvio para o vermelho, AT7 rio galáctico, AT8 poeira e filamentos, AT9 céu em rotação, AT10 viagem lenta |
| Fundo de espaço profundo na HUD (#590; galeria `prototipos/issue-590/`, 15 opções) | AU2 · Catálogo Messier com ressalvas (muito rápido; manter o reforço da fonte no claro) | 14 não escolhidas |
| Fundo da HUD: supernovas e galáxias nascendo (#590; galeria `prototipos/issue-590-r2/`, 10 opções) | nenhuma: pedido refeito para "só estrelas" | 10 opções |
| Fundo da HUD: só estrelas, não passando muito rápido, algumas capturadas pelas APIs (#590; galeria `prototipos/issue-590-r3/`, 2 opções) | AW1 · céu noturno claro (o claro ficou branco na rodada AX) | AW2 · calhas de espaço profundo |
| Cor do céu no claro (#590; galeria `prototipos/issue-590-r4/ax-cores-ceu/`, 6 cores) | nenhuma: recusada, "deixa branco mesmo como tá no original" | 6 cores, claro fica branco |

Próxima rodada usa a próxima letra livre (letras duplas: AA, AB, AC…; U a Z e AA a AT já usadas). Trilha, fundo ou estado contínuo: as opções
já nascem animadas (laço atrás da política), nunca só o quadro parado. Ícone de sistema não anima: nessa rodada o
card mostra os tamanhos reais (lupa ×4 no 16 px) sobre barra clara e escura, e não um laço.
