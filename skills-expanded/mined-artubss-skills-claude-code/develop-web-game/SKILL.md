---
name: "develop-web-game"
description: "Use quando o Codex está construindo ou iterando em um jogo web (HTML/JS) e precisa de um loop confiável de desenvolvimento + teste: implementar pequenas mudanças, executar um script de teste baseado em Playwright com rajadas curtas de input e pausas intencionais, inspecionar screenshots/texto e revisar erros de console com render_game_to_text."
author: openai
---


# Desenvolver Jogo Web

Construa jogos em pequenos passos e valide cada mudança. Trate cada iteração como: implementar → agir → pausar → observar → ajustar.

## Caminhos de habilidade (configure uma vez)

```bash
export CODEX_HOME="${CODEX_HOME:-$HOME/.codex}"
export WEB_GAME_CLIENT="$CODEX_HOME/skills/develop-web-game/scripts/web_game_playwright_client.js"
export WEB_GAME_ACTIONS="$CODEX_HOME/skills/develop-web-game/references/action_payloads.json"
```

Habilidades no escopo do usuário são instaladas em `$CODEX_HOME/skills` (padrão: `~/.codex/skills`).

## Fluxo de trabalho

1. **Escolha um objetivo.** Defina uma única funcionalidade ou comportamento para implementar.
2. **Implemente pequeno.** Faça a menor mudança que leve o jogo adiante.
3. **Garanta pontos de integração.** Forneça um único canvas e `window.render_game_to_text` para que o loop de teste possa ler o estado.
4. **Adicione `window.advanceTime(ms)`.** Prefira fortemente um hook de step determinístico para que o script Playwright possa avançar frames de forma confiável; sem ele, testes automatizados podem ser instáveis.
5. **Inicialize progress.md.** Se `progress.md` existe, leia-o primeiro e confirme que o prompt original do usuário está registrado no topo (prefixo com `Original prompt:`). Também anote qualquer TODO e sugestão deixada pelo agente anterior. Se faltar, crie-o e escreva `Original prompt: <prompt>` no topo antes de anexar atualizações.
6. **Verifique disponibilidade do Playwright.** Garanta que `playwright` está disponível (dependência local ou instalação global). Se incerto, verifique `npx` primeiro.
7. **Execute o script de teste Playwright.** Você deve executar `$WEB_GAME_CLIENT` após cada mudança significativa; não invente um novo cliente a menos que necessário.
8. **Use a referência de payload.** Base ações em `$WEB_GAME_ACTIONS` para evitar adivinhar chaves.
9. **Inspecione o estado.** Capture screenshots e estado de texto após cada rajada.
10. **Inspecione screenshots.** Abra o screenshot mais recente, verifique visuais esperados, corrija quaisquer problemas e reexecute o script. Repita até acertar.
11. **Verifique controles e estado (foco multi-passo).** Exercite exaustivamente todas as interações importantes. Para cada uma, pense em toda a sequência multi-passo que implica (causa → estados intermediários → resultado) e verifique se toda a cadeia funciona ponta-a-ponta. Confirme que `render_game_to_text` reflete o mesmo estado mostrado na tela. Se algo estiver errado, corrija e reexecute.
    Exemplos de interações importantes: mover, pular, disparar/atacar, interagir/usar, selecionar/confirmar/cancelar em menus, pausar/retomar, reiniciar e qualquer habilidade especial ou ação de quebra-cabeça definida pelo request. Exemplos multi-passo: disparar em um inimigo deve reduzir sua saúde; quando a saúde chega a 0 deve desaparecer e atualizar a pontuação; coletar uma chave deve abrir uma porta e permitir progressão de nível.
12. **Verifique erros.** Revise erros de console e corrija o primeiro problema novo antes de continuar.
13. **Resete entre cenários.** Evite estado entre testes ao validar funcionalidades distintas.
14. **Itere com pequenos deltas.** Mude uma variável por vez (frames, inputs, timing, posições), depois repita as etapas 7–13 até estabilizar.

Exemplo de comando (ações obrigatórias):
```
node "$WEB_GAME_CLIENT" --url http://localhost:5173 --actions-file "$WEB_GAME_ACTIONS" --click-selector "#start-btn" --iterations 3 --pause-ms 250
```

Exemplo de ações (JSON inline):
```json
{
  "steps": [
    { "buttons": ["left_mouse_button"], "frames": 2, "mouse_x": 120, "mouse_y": 80 },
    { "buttons": [], "frames": 6 },
    { "buttons": ["right"], "frames": 8 },
    { "buttons": ["space"], "frames": 4 }
  ]
}
```

## Checklist de Teste

Teste qualquer funcionalidade nova adicionada para o request e quaisquer áreas que sua mudança de lógica possa afetar. Identifique problemas, corrija-os e reexecute os testes para confirmar que foram resolvidos.

Exemplos de coisas a testar:
- Inputs primários de movimento/interação (ex: mover, pular, disparar, confirmar/selecionar).
- Transições de vitória/derrota ou sucesso/falha.
- Mudanças de pontuação/saúde/recursos.
- Condições limites (colisões, paredes, bordas de tela).
- Fluxo de menu/pausa/início se presente.
- Qualquer ação especial vinculada ao request (powerups, combos, habilidades, quebra-cabeças, timers).

## Artefatos de Teste para Revisar

- Screenshots mais recentes da execução do Playwright.
- Saída JSON mais recente de `render_game_to_text`.
- Logs de erro de console (corrija o primeiro erro novo antes de continuar).
Você deve realmente abrir e inspecionar visualmente os screenshots mais recentes após executar o script Playwright, não apenas gerá-los. Garanta que tudo que deve estar visível na tela está realmente visível. Vá além da tela inicial e capture screenshots de gameplay que cobrem todas as funcionalidades recém-adicionadas. Trate os screenshots como fonte da verdade; se algo está faltando, está faltando na build. Se suspeitar de problema de captura headless/WebGL, reexecute o script Playwright em modo headed e revise novamente. Corrija e reexecute em loop apertado até que screenshots e estado de texto pareçam corretos. Uma vez que as correções forem verificadas, reteste todas as interações e controles importantes, confirme que funcionam e garanta que suas mudanças não introduziram regressões. Se introduziram, corrija e reexecute tudo em loop até que interações, estado de texto e controles funcionem como esperado. Seja exaustivo ao testar controles; jogos quebrados não são aceitáveis.

## Diretrizes Principais do Jogo

### Canvas + Layout
- Prefira um único canvas centralizado na janela.

### Visuais
- Mantenha texto na tela mínimo; mostre controles em uma tela inicial/menu em vez de sobrepor durante o gameplay.
- Evite cenas excessivamente escuras a menos que o design exija. Torne elementos-chave fáceis de ver.
- Desenhe o background no próprio canvas em vez de confiar em backgrounds CSS.

### Saída de Estado de Texto (render_game_to_text)
Exponha uma função `window.render_game_to_text` que retorna uma string JSON concisa representando o estado atual do jogo. O texto deve incluir informações suficientes para jogar sem visuais.

Padrão mínimo:
```js
function renderGameToText() {
  const payload = {
    mode: state.mode,
    player: { x: state.player.x, y: state.player.y, r: state.player.r },
    entities: state.entities.map((e) => ({ x: e.x, y: e.y, r: e.r })),
    score: state.score,
  };
  return JSON.stringify(payload);
}
window.render_game_to_text = renderGameToText;
```

Mantenha o payload sucinto e enviesado para elementos na tela/interativos. Prefira entidades atuais visíveis sobre histórico completo.
Inclua uma nota clara de sistema de coordenadas (origem e direções de eixo), e codifique todo o estado relevante do jogador: posição/velocidade do jogador, obstáculos/inimigos ativos, coletáveis, timers/cooldowns, pontuação e qualquer flag de modo/estado necessária para tomar decisões corretas. Evite históricos grandes; inclua apenas o que é atualmente relevante e visível.

### Hook de Stepping de Tempo
Forneça um hook de stepping de tempo determinístico para que o cliente Playwright possa avançar o jogo em incrementos controlados. Exponha `window.advanceTime(ms)` (ou um wrapper fino que encaminhe para seu loop de atualização do jogo) e tenha o loop do jogo usá-lo quando presente.
O script de teste Playwright usa este hook para step frames deterministicamente durante testes automatizados.

Padrão mínimo:
```js
window.advanceTime = (ms) => {
  const steps = Math.max(1, Math.round(ms / (1000 / 60)));
  for (let i = 0; i < steps; i++) update(1 / 60);
  render();
};
```

### Toggle de Tela Cheia
- Use uma única tecla (prefira `f`) para alternar tela cheia ligada/desligada.
- Permita `Esc` para sair da tela cheia.
- Quando tela cheia alterna, redimensione o canvas/rendering para que visuais e mapeamento de input permaneçam corretos.

## Rastreamento de Progresso

Crie um arquivo `progress.md` se não existir e anexe TODOs, notas, armadilhas e pontas soltas conforme você avança para que outro agente possa pegar de forma contínua.
Se um arquivo `progress.md` já existe, leia-o primeiro, incluindo o prompt original do usuário no topo (você pode estar continuando o trabalho de outro agente). Não sobrescreva o prompt original; preserve-o.
Atualize `progress.md` após cada chunk significativo de trabalho (funcionalidade adicionada, bug encontrado, teste executado ou decisão tomada).
Ao final do seu trabalho, deixe TODOs e sugestões para o próximo agente em `progress.md`.

## Pré-requisitos do Playwright

- Prefira uma dependência local `playwright` se o projeto já a tem.
- Se incerto se Playwright está disponível, verifique por `npx`:
  ```
  command -v npx >/dev/null 2>&1
  ```
- Se `npx` estiver faltando, instale Node/npm e depois instale Playwright globalmente:
  ```
  npm install -g @playwright/mcp@latest
  ```
- Não mude para `@playwright/test` a menos que explicitamente pedido; mantenha o script do cliente.

## Scripts

- `$WEB_GAME_CLIENT` (instalação padrão: `$CODEX_HOME/skills/develop-web-game/scripts/web_game_playwright_client.js`) — loop de ação baseado em Playwright com stepping de tempo virtual, captura de screenshot e buffering de erro de console. Você deve passar uma rajada de ação via `--actions-file`, `--actions-json` ou `--click`.

## Referências

- `$WEB_GAME_ACTIONS` (instalação padrão: `$CODEX_HOME/skills/develop-web-game/references/action_payloads.json`) — exemplo de payloads de ação (teclado + mouse, por-frame capture). Use estes para construir sua rajada.