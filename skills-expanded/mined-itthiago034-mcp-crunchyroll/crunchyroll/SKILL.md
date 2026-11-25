---
name: crunchyroll
description: "Assistir anime na Crunchyroll do usuário pelo MCP crunchyroll: colocar/abrir/tocar um episódio (\"coloca X ep 12\", \"temporada 2\", dublado ou legendado), continuar de onde parou, próximo episódio, dar play, pausar, tela cheia, buscar títulos, temporadas e episódios, recomendações, lançamentos da temporada, histórico e lista (watchlist). Use SEMPRE que o pedido envolver anime, Crunchyroll, o player ou assistir algo."
version: 2.0.0
author: Thiago
license: MIT
platforms: [linux]
metadata:
  hermes:
    tags: [Anime, Crunchyroll, Streaming, MCP, Media]
---

# Crunchyroll (MCP `crunchyroll`)

Esta skill ensina a usar o servidor MCP `crunchyroll` para encontrar e **tocar** anime na conta
Crunchyroll do usuário. O vídeo abre numa aba nova do navegador dedicado, que já está logado.
Você não precisa de navegador próprio, de senha nem de cookies.

As ferramentas aparecem com o prefixo `mcp__crunchyroll__`, por exemplo
`mcp__crunchyroll__crunchyroll_play`. Neste texto elas são citadas pelo nome curto
(`crunchyroll_play`), mas **chame sempre o nome completo**. Se o seu ambiente usa
`tool_describe`/`tool_call`, descreva só as ferramentas de que precisa e chame pelo nome completo.

## Regras de ouro

1. **Nunca abra a Crunchyroll com outro navegador** (`browser_exec`, `browser_navigate`, curl, web
   fetch). Ele não tem a sessão do usuário e cai na verificação da Cloudflare ("Um momento…",
   "Verify you are human"). Para tocar, use **somente** `crunchyroll_play`.
2. **O player só é controlado por `crunchyroll_player_control`** (play, pause, tela cheia, sair da
   tela cheia, status). É **proibido** improvisar: nada de terminal, `ps`/`find` atrás do navegador,
   scripts JavaScript, WebSocket direto, porta de depuração (`9222`, `DevToolsActivePort`), CDP
   avulso, `xdotool` ou cliques simulados. Se a ferramenta oficial falhar, **diga ao usuário o que
   ela respondeu** (veja "Respostas do player") em vez de contornar a camada de segurança.
3. **Nunca peça e-mail, senha ou código** ao usuário. O login é feito pelo próprio usuário na janela
   do navegador dedicado.
4. **Não invente IDs.** Todo ID (série, temporada, episódio) sai de uma resposta de ferramenta.
   IDs são letras maiúsculas e números: `G8DHV78ZM`, `GS00377802ENUS`, `GE00377814ENUS`.
5. **Não repita a mesma chamada com os mesmos argumentos** depois de um erro. Leia o erro e siga a
   tabela de erros abaixo.
6. `crunchyroll_continue_watching` e `crunchyroll_get_subscription` **não funcionam** (sempre
   respondem `OPERATION_NOT_MIGRATED`). Não chame. Para "continuar", use o histórico (receita C).
7. Responda ao usuário em português, curto: o que você abriu (anime, temporada, episódio, título e
   idioma). Não despeje JSON.

## Os tipos de ID (não confunda)

| Tipo | Exemplo | De onde vem | Serve para |
|---|---|---|---|
| Série | `G8DHV78ZM` | `crunchyroll_search`, `crunchyroll_browse`, `parent_id` do histórico | `crunchyroll_get_seasons`, `crunchyroll_get_series`, `crunchyroll_get_similar` |
| Temporada | `GS00377802ENUS` | `crunchyroll_get_seasons` → `seasons[].id` ou um valor de `seasons[].audio_versions` | `crunchyroll_get_episodes` |
| Episódio | `GE00377814ENUS` | `crunchyroll_get_episodes` → `episodes[].id` ou um valor de `episodes[].audio_versions` | `crunchyroll_play`, `crunchyroll_get_episode`, `crunchyroll_get_playheads` |

`crunchyroll_play` só aceita **ID de episódio** (ou de filme). Nunca passe ID de série ou temporada.

## Antes de tudo: sessão

Você **não** precisa checar o login nem chamar `crunchyroll_login` antes de consultar. As ferramentas
de conteúdo restabelecem a sessão sozinhas, **uma única vez para todas as chamadas simultâneas**,
quando isso é só reaproveitar uma sessão que o próprio usuário já autorizou no navegador dedicado
(inclusive na primeira consulta de uma conversa nova). Por isso:

- **Não** faça consultas "de teste" nem repita a primeira consulta por precaução.
- **Não** dispare histórico e recomendações em paralelo "para ganhar tempo": decida antes qual das
  duas o pedido precisa (Receita F).

Quando não dá para restabelecer sozinho, a resposta traz `code` e `hint`. Siga o `code`:

| `code` | O que fazer |
|---|---|
| `LOGIN_REQUIRED`, `SILENT_REAUTH_FAILED`, `SILENT_REAUTH_COOLDOWN`, `REAUTH_REQUIRED` | Chame `crunchyroll_login` (sem argumentos) **uma vez**; depois refaça **uma vez** a chamada que falhou. |
| `LOGGED_OUT` | O usuário saiu da conta. Pergunte se ele quer entrar de novo antes de chamar `crunchyroll_login`. |
| `LOGGING_OUT` | Um logout está em andamento. Não tente de novo sozinho. |
| `TIMEOUT` / `CANCELLED` | Avise o usuário; tente de novo só se ele pedir. |

Se `crunchyroll_login` demorar e voltar `LOGIN_REQUIRED`, ou der timeout, a sessão do navegador
acabou. Diga ao usuário, sem tentar de novo por conta própria:
"A sessão da Crunchyroll expirou. Abra o login manual com `npm run onboard:browser` na pasta
`~/mcp-crunchyroll-validacao`, entre na conta, feche a janela pelo X e me peça de novo."
(Se aparecer a verificação da Cloudflare dentro da janela aberta pelo MCP, é o mesmo caso: só o
login manual resolve.)

`crunchyroll_status` só informa o estado. Ele nunca conserta nada.

## Receita A — "Coloca <anime> [temporada N] ep M"

Exemplo: "coloca Clevatess temporada 2 episódio 12".

1. `crunchyroll_search` com `{"query": "Clevatess"}`.
   - A resposta é `{"count", "results": [{"type", "id", "title", "description"}]}` (só séries e
     filmes).
   - Escolha o resultado `type: "series"` cujo `title` bate com o pedido. Se houver dois animes
     diferentes plausíveis, pergunte qual. Se o pedido for um filme, procure `type: "movie_listing"`.
   - Nenhum resultado: tente o nome em inglês ou japonês (ex.: "Frieren", "Sousou no Frieren") antes
     de dizer que não achou.
2. `crunchyroll_get_seasons` com `{"series_id": "<id da série>"}`.
   - Cada item de `seasons` tem `id`, `title` (ex.: "Clevatess II"), `season_number`,
     `number_of_episodes`, `subtitle_locales`, `original_audio` e `audio_versions`.
   - **Séries longas numeradas de forma contínua** (One Piece, Naruto Shippuden, Boruto…): o
     `episode_number` é o número absoluto do episódio e o `title` da temporada mostra o intervalo, ex.:
     "Land of Wano (892-1088)", "Egghead (1089-1155)". Para "One Piece ep 1100", escolha a temporada
     cujo intervalo contém 1100. `season_number` nessas séries não corresponde ao que o usuário chama de
     "temporada".
   - "Temporada 2" = o item com `season_number: 2`. Sem temporada no pedido, use a 1 se o episódio
     couber nela; se o usuário disse só "ep M" e a série tem várias temporadas, prefira a temporada
     mais recente que tenha o episódio M **apenas se** ele estiver claramente acompanhando a série
     (histórico); senão, pergunte.
   - Ignore itens que não sejam temporadas da série principal (ex.: especiais, recaps) a menos que o
     usuário peça.
3. `crunchyroll_get_episodes` com `{"season_id": "<id da temporada>", "episode_number": M}`.
   - Passar `episode_number` devolve **só** aquele episódio (`count: 1`) e o total da temporada em
     `season_episode_count`. Use sempre que souber o número: a resposta fica pequena.
   - Cada episódio tem `id`, `episode_number`, `title`, `is_premium_only`, `availability_status`,
     `next_episode_id`, `duration_ms`, `original_audio` e `audio_versions`.
   - `count: 0` → a temporada pode **continuar a numeração da anterior** (ex.: Kaiju No. 8 temporada 2
     começa no episódio 13). Se `M <= season_episode_count`, chame de novo **sem** `episode_number`,
     ordene por `episode_number` e pegue o M-ésimo da temporada (o "ep 5 da temporada 2" do Kaiju
     é o `episode_number` 16). Diga ao usuário os dois números ("5º da temporada, ep. 16"). Se
     `M > season_episode_count`, diga quantos episódios a temporada tem.
   - Sem número (ex.: "o que tem nessa temporada?"), chame sem `episode_number` para listar todos.
4. Escolha o idioma (veja "Idioma e versões") e chame `crunchyroll_play` com
   `{"episode_id": "<id do episódio escolhido>"}`.
   - Sucesso: `{"opened": true, "episode_id", "url"}`. O player abre numa aba do navegador dedicado;
     se já houver um episódio tocando, a mesma aba troca para o novo.
   - Se o usuário pediu para já começar a tocar e/ou em tela cheia ("coloca e dá play", "em tela
     cheia"), passe as opções na **mesma** chamada: `{"episode_id": "...", "autoplay": true}` e/ou
     `"fullscreen": true`. A resposta traz `autoplay`/`fullscreen` com o resultado de cada passo e
     `partial: true` se algum não foi confirmado. Sem as opções, nada muda.
5. Responda: "Abri **Clevatess II – ep. 12: The Millennium of a Dark Beast Lord** (dublado em PT-BR)
   no navegador da Crunchyroll."

## Receita B — Próximo episódio / episódio seguinte

1. Descubra o episódio atual: o que você acabou de abrir, ou o primeiro do histórico (Receita C).
2. `crunchyroll_get_episode` com esse ID → leia `next_episode_id` (vem num idioma qualquer, ex.:
   `...ENUS`).
3. Para tocar no mesmo idioma do atual, chame `crunchyroll_get_episode` com o `next_episode_id` e pegue
   em `versions` a `guid` cujo `audio_locale` é o desejado (em `crunchyroll_get_episode` as versões vêm
   no formato completo: lista de `{audio_locale, guid, original, ...}`). **Não monte o ID trocando o sufixo na mão**
   (`ENUS` → `PTBR`): nem todo episódio tem todas as dublagens, e o ID inventado pode não existir.
4. `crunchyroll_play` com essa `guid`. Sem `next_episode_id`, a temporada acabou: diga isso e ofereça a
   próxima temporada (`crunchyroll_get_seasons`).

## Receita C — "Continua de onde parei" / "o que eu estava vendo?"

1. `crunchyroll_get_history` com `{"n": 10}`.
   - `items[]` vem do mais recente para o mais antigo. Cada item tem `id` (episódio, ex.:
     `GE00377814PTBR`), `title` (título do episódio), `parent_id` (série), `playhead` (segundos já
     vistos), `fully_watched`, `date_played` e `episode_metadata` com `series_title`,
     `season_title`, `season_number`, `episode_number`, `duration_ms`, `original_audio` e
     `audio_versions`.
   - Pode haver vários itens do mesmo episódio ou da mesma série; o primeiro é o mais recente.
2. Pegue o primeiro item (ou o primeiro da série que o usuário citou, comparando `parent_id`).
   - `fully_watched: false` → abra **esse mesmo** `id` com `crunchyroll_play`; o player retoma do
     `playhead`. "Continua o anime" quer o vídeo tocando: use
     `{"episode_id": "<id>", "autoplay": true}` na mesma chamada (não chame o player depois).
   - `fully_watched: true` → abra o próximo (Receita B, a partir do passo 2).
   - "Continuar" = retomar o mesmo episódio se não terminou. "Próximo" = sempre o seguinte (Receita B),
     mesmo que o atual não tenha terminado.
3. O sufixo do `id` no histórico mostra o idioma que o usuário costuma assistir (`...PTBR` = dublado
   em português; `...JAJP` = original japonês). Use isso como preferência padrão.

## Receita F — "Coloca um anime para mim" (sem dizer qual)

Uma consulta só, escolhida pelo contexto — **não** chame histórico e recomendações juntos:

1. Se a conversa já mostrou o que o usuário está acompanhando, ou ele disse "de novo", "aquele",
   "o que eu tava vendo": `crunchyroll_get_history {"n": 5}` e siga a Receita C.
2. Se ele pediu algo novo ("me surpreende", "algo diferente", um gênero): Receita D, **uma** ferramenta.
3. Sem pista nenhuma: `crunchyroll_get_history {"n": 5}`. Se o primeiro item não terminou
   (`fully_watched: false`), ofereça continuar ("Quer continuar **X**, ep. N?"); se a lista vier vazia,
   aí sim use `crunchyroll_get_recommendations {"n": 5}`.
4. Só abra (`crunchyroll_play`) depois que o usuário escolher, a não ser que ele tenha mandado
   "pode escolher" — aí abra o primeiro candidato e diga qual foi.

## Receita G — Controlar o player ("dá play", "pausa", "tela cheia")

O episódio já precisa estar aberto pelo `crunchyroll_play`. Uma chamada por pedido:

| Pedido | Chamada |
|---|---|
| "dá play", "continua", "volta a tocar" | `crunchyroll_player_control {"action": "play"}` |
| "pausa", "para um pouco" | `crunchyroll_player_control {"action": "pause"}` |
| "tela cheia", "maximiza o vídeo" | `crunchyroll_player_control {"action": "fullscreen"}` |
| "sai da tela cheia" | `crunchyroll_player_control {"action": "exit_fullscreen"}` |
| "tá tocando?", "em que minuto está?" | `crunchyroll_player_control {"action": "status"}` |
| "tela cheia e dá play" | `fullscreen`, depois `play` (duas chamadas, nessa ordem) |

**Só diga que deu certo quando `success: true` e `verified: true`.** O campo `state` mostra o que foi
observado (`playing`, `paused`, `fullscreen`, `current_time`, `duration`).

### Respostas do player

| `outcome` | O que dizer / fazer |
|---|---|
| `CONFIRMED` | Confirme ("Pronto, tocando em tela cheia."). `reason: "ALREADY_IN_STATE"` = já estava assim. |
| `REFUSED_BY_BROWSER` | O navegador recusou (`reason` diz o motivo, ex.: `AUTOPLAY_BLOCKED_USER_ACTIVATION_REQUIRED`, `FULLSCREEN_NOT_ALLOWED_IN_FRAME`). Diga ao usuário e sugira clicar no player / apertar `F` na janela. **Não** tente outro jeito. |
| `NOT_CONFIRMED` | O comando foi enviado mas o estado não mudou. Diga isso; repita **uma** vez só se o usuário pedir. |
| `PLAYER_LOADING` | O vídeo ainda está carregando. Espere alguns segundos e tente **uma** vez. |
| `PLAYER_UNAVAILABLE` | Não há player controlável na aba (ex.: página de aviso, anúncio, outra página). Diga isso. |
| `TAB_NOT_FOUND` | Nenhum episódio aberto: abra com `crunchyroll_play` primeiro (ou pergunte qual). |
| `TAB_CLOSED`, `SESSION_DISCONNECTED` | A aba/navegador fechou. Abra de novo com `crunchyroll_play` se o usuário quiser. |
| `NOT_PERMITTED` | Durante/depois de um logout o player não é controlado. Diga isso. |
| `TIMEOUT`, `BUSY` | Avise e não insista em loop. |

## Idioma e versões (dublado × legendado)

Nas listas (`crunchyroll_get_seasons`, `crunchyroll_get_episodes`, `crunchyroll_get_history`) cada item
traz `original_audio` e `audio_versions`, um mapa **idioma do áudio → ID para tocar**. Exemplo real
(Clevatess II, ep. 12):

```json
"original_audio": "ja-JP",
"audio_versions": {"ja-JP": "GE00377814JAJP", "en-US": "GE00377814ENUS", "pt-BR": "GE00377814PTBR"}
```

- "Dublado" / "em português" → `audio_versions["pt-BR"]`.
- "Legendado" / "original" / "em japonês" → `audio_versions[original_audio]` (geralmente `ja-JP`).
  As legendas em português aparecem no player.
- O usuário **já disse** o idioma → use direto; **não** consulte o histórico.
- Sem preferência no pedido → use a do histórico (Receita C, passo 3) se você já o tiver; sem
  histórico, use o `id` do episódio como veio (a Crunchyroll aplica o idioma preferido da conta).
- Não existe `pt-BR` no mapa → avise ("não tem dublagem em português; abri legendado") e use a
  original.

## Receita D — Descobrir o que assistir

| Pedido | Ferramenta | Argumentos |
|---|---|---|
| "me recomenda algo" | `crunchyroll_get_recommendations` | `{"n": 5}` |
| "parecido com X" | `crunchyroll_search` → `crunchyroll_get_similar` | `{"series_id": "...", "n": 5}` |
| "populares", "novidades" | `crunchyroll_browse` | `{"sort_by": "popularity"}` ou `{"sort_by": "newly_added"}` |
| "anime de romance/ação…" | `crunchyroll_get_categories`, depois `crunchyroll_browse` | `{"categories": "romance", "sort_by": "popularity"}` (use o `id` da categoria) |
| "lançamentos da temporada" | `crunchyroll_get_simulcast_seasons`, depois `crunchyroll_browse` | `{"seasonal_tag": "fall-2026"}` (o primeiro item é a temporada atual) |
| "me fala sobre X" | `crunchyroll_search` → `crunchyroll_get_series` | `{"series_id": "..."}` |

Apresente 3 a 5 opções com título e uma frase de sinopse em português, e ofereça abrir uma.
Recomendações podem trazer itens que não são anime (ex.: "The Crunchyroll Anime Awards"): pule-os.

## Receita E — Lista (watchlist)

- Ver a lista: `crunchyroll_get_watchlist` com `{"n": 10}`. Cada item já traz `id`, `title`, `type`
  (`series` ou `movie_listing`), `is_favorite` e `date_added`, do mais recente para o mais antigo.
  Liste os títulos direto; **não** chame `crunchyroll_get_series` item por item. Se o usuário pedir
  "a lista toda", use `{"n": 50}` (máximo).
- Adicionar: busque a série e chame `crunchyroll_add_to_watchlist` com `{"content_id": "<id da série>"}`.
- Remover: `crunchyroll_remove_from_watchlist` com `{"content_id": "<id da série>"}`.
- Estas duas alteram a conta. Faça só quando o usuário pedir claramente. Se a resposta for
  `MUTATION_OUTCOME_UNKNOWN`, **não repita**: confira com `crunchyroll_get_watchlist`.

## Progresso

- Ler: `crunchyroll_get_playheads` com `{"content_ids": ["GE..."]}` → `playhead` em segundos e
  `fully_watched`.
- `crunchyroll_update_playhead` altera a conta: use só se o usuário pedir explicitamente para
  marcar progresso.

## Tabela de erros

| Resposta | O que fazer |
|---|---|
| `Not authenticated: log in before requesting content` (com `code`) | Siga a tabela de `code` da seção "Sessão". Sem `code`: `crunchyroll_login` uma vez e refaça a chamada uma vez. |
| `OPERATION_NOT_MIGRATED` | Ferramenta desativada. Use a alternativa (histórico em vez de continue_watching). Não repita. |
| `crunchyroll_play takes episode_id ...` | Você passou ID errado (série/temporada, minúsculas, URL) ou uma opção que não é booleana. Pegue o `id` de `crunchyroll_get_episodes`. |
| `crunchyroll_player_control takes exactly one argument, action...` | Use só `{"action": "play" \| "pause" \| "fullscreen" \| "exit_fullscreen" \| "status"}`. |
| `Upstream has no such resource` | ID não existe. Volte um passo (busca/temporadas) e pegue o ID da resposta. |
| `Upstream is rate limiting this client` | Espere um pouco antes de tentar; avise o usuário. |
| `The managed browser is unavailable` / `BROWSER_UNAVAILABLE` | O navegador dedicado fechou ou está ocupado. Chame `crunchyroll_login` uma vez (ele reabre); se continuar, diga ao usuário para fechar janelas do perfil da Crunchyroll e tentar de novo. |
| `MCP server 'crunchyroll' lost its stdio subprocess` / timeout | O servidor reiniciou. Chame `crunchyroll_status` uma vez; se ele responder, refaça o pedido. Se não, peça ao usuário para rodar `/reload-mcp`. |
| `MUTATION_OUTCOME_UNKNOWN` | Não repita a alteração. Confira o estado (watchlist/playheads) e informe. |

## Exemplo completo (real)

Pedido: "Coloca Clevatess 2ª temporada ep 12 dublado"

1. `crunchyroll_search {"query":"Clevatess"}` → série `G8DHV78ZM` "Clevatess".
2. `crunchyroll_get_seasons {"series_id":"G8DHV78ZM"}` → `season_number: 2` = `GS00377802ENUS`
   "Clevatess II", 13 episódios.
3. `crunchyroll_get_episodes {"season_id":"GS00377802ENUS","episode_number":12}` → "The Millennium
   of a Dark Beast Lord"; `audio_versions["pt-BR"]` = `GE00377814PTBR`.
4. `crunchyroll_play {"episode_id":"GE00377814PTBR"}` → `{"opened": true, ...}`.
5. Resposta: "Abri **Clevatess II – ep. 12: The Millennium of a Dark Beast Lord**, dublado em PT-BR,
   no navegador da Crunchyroll."

Quatro chamadas, sem login, sem navegador próprio.

Pedido seguinte: "Pode colocar em tela cheia e dar play?"

1. `crunchyroll_player_control {"action":"fullscreen"}` → `{"success": true, "verified": true, "state": {"fullscreen": true, ...}}`.
2. `crunchyroll_player_control {"action":"play"}` → `{"success": true, "verified": true, "state": {"playing": true, ...}}`.
3. Resposta: "Pronto: tela cheia e tocando."

Duas chamadas, nenhum terminal, nenhum script.
