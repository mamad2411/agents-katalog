---
name: usage-monitor-release-video
description: Release video (vertical, PT/EN, voice, captions) and post text for X/Instagram/TikTok, plus the 16:9 tour of the whole app. Use for "vídeo da release", "vídeo de lançamento", "vídeo para o insta/tiktok", "descrição para X/Instagram/TikTok", "tour em vídeo".
---

# Usage Monitor — vídeo de lançamento

Gera, para uma versão estável, **dois vídeos verticais** (PT e EN), as **legendas `.srt`** e as **descrições para X,
Instagram e TikTok**. O vídeo **mostra o app de verdade**: as telas reais, gravadas offscreen com dados sintéticos,
narradas passo a passo. O padrão foi aprovado pelo dono na v42.3.0 (#633; referência `docs/planos/video-v42-3/`).
É regra, não sugestão:

| Regra | Como é garantida |
|---|---|
| Vertical 1080×1920, **60 fps**, H.264 `slow`/CRF 16 + AAC | `render.mjs` (`RELEASE_ENCODE`; o tour segue `DEFAULT_ENCODE` 30 fps) |
| **Telas reais**, nunca mockup nem captura imitada | demos de vídeo do gerador (`gradlew.bat generateVideoMedia`), registro `VideoDemos.kt` |
| Voz pela API do OpenRouter, mesma voz nos dois idiomas | `elevenlabs/eleven-v4`, voz `george` (`openrouter.mjs`, `speak.mjs`); escolhida pelo dono em audição de 27 amostras |
| **Sem pressa** | ≤ 15 caracteres/s por fala (a voz fala ~13,5/s e o OpenRouter recusa `speed`), 1,8 s de respiro, ≤ 150 s; a cena dura no mínimo a demo + 1,5 s (`RELEASE_PACING`). Conserto é cortar texto ou pontuar pausas, **nunca** acelerar a voz |
| **Uma fala por passo** | `lines[lang]` como lista de beats `{ at, text, say? }`: cada fala toca quando o passo acontece na demo |
| Demo no ritmo de quem assiste | `VideoDemoPace`: 2,5 s antes da 1ª ação, cursor anda 1,4 s (nunca teleporta), 0,9 s parado antes do clique, 2,5 s por resultado, animações ≥ 1,6 s, margem de 48 dp |
| **Sem moldura de janela** | nenhuma barra "● ● ● usage-monitor". HUD: `"surface": "hud"`, quadros com fundo transparente direto sobre as estrelas, sem caixa, clip nem câmera. Janela do app (Codex, análise): cartão raio 10, sem barra |
| Zoom contido | câmera só em telas de janela; `maxZoom` padrão 1,35 (tela densa pode declarar mais); chaves a ≥ 1,5 s (`scene-check.mjs` recusa) |
| Transição | 1,8 s no respiro: a cena é puxada em espiral pelo **Gargantua da abertura** (disco girando, anel de fótons, rastros de estrelas) e a próxima nasce do centro |
| Legenda | queimada (2 linhas × 26 caracteres) e `.srt`; por beat; entra 150 ms antes da fala, sai 300 ms depois |
| Todas as mudanças da versão | cada issue de `collect-changes.mjs` tem cena ou item; nada além do que está nos commits (commit só de teste não é novidade) |
| Tema do app | tokens de `docs/design-system/tokens/`, Plex Mono/Sans do app |
| Descrições | `social.mjs` recusa X acima de 280 (link = 23, emoji = 2) ou sem o link da release, link em Instagram/TikTok e mais de 5 hashtags |

A skill **não publica** nada nas redes. O dono aprova pela **prévia** (`--preview`), que é o próprio renderizador do
vídeo, nunca uma página paralela.

## Chave do OpenRouter

A chave vem **só** da variável `OPENROUTER_API_KEY` na chamada (o dono a passa ao pedir a skill). Nunca gravada em
arquivo versionado, log, `scenes.json` ou memória; sem ela a skill falha com mensagem, sem cair para o Piper. Voz:
`POST /api/v1/audio/speech`; `google/*-tts` só aceita `pcm`. Imagem (opcional, só capa ou ilustração, **nunca** tela
do app): `google/gemini-3.1-flash-image` por `generateImage`. A fala é cacheada por assinatura (modelo, voz, texto):
regerar a prévia não cobra de novo.

## Passo a passo

Todo o trabalho segue o fluxo do `CLAUDE.md` (issue, worktree, PR): roteiro e descrições ficam em
`docs/planos/video-v<maior>-<menor>/`.

1. **Versão.** A pedida, ou a última estável (`git tag --list 'v*'` sem `-beta`).
2. **O que mudou.** `node .claude/skills/usage-monitor-release-video/scripts/collect-changes.mjs vX.Y.Z`. Leia o
   corpo da release e o plano de cada issue em `docs/planos/` para entender **o que a pessoa vê**.
3. **Demos reais.** Cada novidade visível vira uma demo de vídeo em `src/desktopTest/.../screenshots/` (registro
   `VideoDemos.kt`, ritmo `VideoDemoPace`, ids `video-*`; `HelpTopic` é enum e **não** ganha valor). Composable de
   produção com estado sintético, motion `AppMotionPolicy.Live`, escala 4×, HUD com `transparent = true`. Grave PT e
   EN: `gradlew.bat generateVideoMedia -PvideoMediaLanguage=pt -PhelpMediaTopic=<ids>` (e `en`). Confira início,
   meio e fim de cada demo; a soma de `frames.json` dá a duração, e os quadros longos (≥ 0,8 s) marcam os passos.
   Novidade sem tela (memória, correção interna) vai na cena `list` "E mais" com os **rótulos reais** do app.
4. **Roteiro.** `scenes.json` (formato abaixo): abertura, uma cena `screen` por demo, `list` "E mais", fechamento.
   Um beat por passo, com `at` no instante do passo (os quadros longos do `frames.json`). Recorte (`crop`) na caixa
   do conteúdo: `ffmpeg -i <demo>/%03d.png -vf "alphaextract,bbox=min_val=8" -f null -` dá a caixa da HUD; tela de
   janela densa recorta a região de interesse até o texto de 13 dp ficar ≥ 18 px no vídeo. Número escrito na legenda
   (`42.3`) e por extenso no `say`.
5. **Prévia.** `OPENROUTER_API_KEY=… node .claude/skills/usage-monitor-release-video/scripts/make-video.mjs vX.Y.Z
   --preview --out prototipos/video-v<M>-<m>/final`. Se o ritmo recusar, corte ou pontue a fala apontada. **Olhe**
   antes de mostrar: capture `preview.html?t=<s>` no Chrome via puppeteer esperando 4 s (o `--virtual-time-budget`
   do Edge fotografa antes das imagens carregarem e dá quadro vazio). Confira foco no alvo, legenda, nada cortado.
   Abra a prévia para o dono e só siga com a aprovação dele.
6. **Descrições.** `social.json` (PT e EN para `x`, `instagram`, `tiktok`): o X leva o link da release; Instagram e
   TikTok dizem "link na bio" / "link in bio"; até 5 hashtags.
7. **Vídeos.** `make-video.mjs vX.Y.Z` (render a 60 fps; ~5 s de parede por segundo de vídeo por idioma). Saída em
   `~/Videos/usage-monitor/vX.Y.Z/`: `usage-monitor-<label>-{en,pt}.mp4`, `.srt` e `social.md`. Confira o `ffprobe`
   (1080×1920, 60 fps, h264 + aac) e extraia quadros do MP4 final.
8. **Roteiro escrito.** `roteiro.md` na mesma pasta: fonte (tags e issues), parâmetros medidos e a tabela de cenas.
9. **Entrega ao dono** (≤ 15 linhas): caminho dos arquivos, duração, e o texto de cada rede está no `social.md`.

Na primeira vez numa máquina, `setup-tools.mjs` instala puppeteer-core e o Chrome sem tela em
`%LOCALAPPDATA%\usage-monitor-video` (o vídeo de release não baixa mais Piper).

## Tour em vídeo 16:9 (#505)

O tour de todas as funcionalidades é outro alvo da mesma skill, com regras próprias: roteiro em
`docs/planos/video-tour/scenes.json`, saída em `~/Videos/usage-monitor/tour/usage-monitor-tour-{en,pt}.mp4` + `.srt`.

| Regra | Como é garantida |
|---|---|
| 1920×1080, 30 fps, **5 a 10 min** | `TOUR_PACING` (`timeline.mjs`) falha abaixo de 300 s ou acima de 600 s |
| Sem pressa | ≤ 14 caracteres/s, 1,4 s de respiro; conserto é cortar texto ou baixar `voice.speed`, nunca acelerar |
| Voz | Kokoro `pf_dora` (PT) e `am_michael` (EN), escolhidas pelo dono ouvindo amostras; `voice` no roteiro |
| Capturas reais nos dois idiomas | as demos da ajuda a 2× em PNG: `gradlew.bat generateVideoMedia -PvideoMediaLanguage=en` (o `make-tour.mjs` roda sozinho se faltar `build/video-media/<idioma>`) |
| Trilha e efeitos | `soundtrack.py`, sintetizados (sem amostra de terceiros), semente fixa; efeitos nos instantes de `soundEvents`; trilha abaixa sob a fala (sidechain) |
| Transições do tema | lente gravitacional + cartão do capítulo, deslize de captura, foco com contorno azul, digitação; anel Gargantua só na abertura e no fechamento |

```bash
node .claude/skills/usage-monitor-release-video/scripts/make-tour.mjs --stills   # conferência (~2 min)
node .claude/skills/usage-monitor-release-video/scripts/make-tour.mjs --only en  # um idioma (~20 min)
node .claude/skills/usage-monitor-release-video/scripts/make-tour.mjs --remix     # só o áudio, sobre o vídeo mudo
```

Mixagem com ganhos fixos e `loudnorm` **linear** em duas passadas: o de uma passada é dinâmico e levantou a trilha nos
respiros até o nível da fala (medido no #505). Roteiro e medições: `docs/planos/video-tour/roteiro.md`.

Cena `screen` do tour: `media: [{ "media": "<mediaId da ajuda>", "bar", "focus": [x, y, l, a], "crop": [x, y, l, a] }]`, em dp da cena
de 1000×420 da ajuda; várias capturas dividem o capítulo. `steps` e `commands` como no vídeo de release.

## Formato do `scenes.json` (vídeo de release)

```json
{
  "version": "v42.3.0",
  "label": "42.3",
  "voice": { "model": "elevenlabs/eleven-v4", "voice": { "en": "george", "pt": "george" } },
  "sources": { "minimize": { "frames": "build/video-media/{lang}/video-hud-minimize" } },
  "scenes": [
    { "id": "title", "kind": "title", "headline": { "en": "…", "pt": "…" },
      "lines": { "en": { "text": "Usage Monitor 42.3. …", "say": "Usage Monitor forty-two point three. …" }, "pt": { … } } },
    { "id": "minimize", "kind": "screen", "frames": "minimize", "surface": "hud", "tag": "#576",
      "kicker": { "en": "hud", "pt": "hud" }, "headline": { … }, "crop": [x, y, largura, altura],
      "focus": [x, y, largura, altura], "focusAt": 4.3,
      "lines": { "en": [ { "at": 0, "text": "…" }, { "at": 6, "text": "…" } ], "pt": [ … ] } },
    { "id": "codex", "kind": "screen", "frames": "codex", "crop": […], "maxZoom": 1.8,
      "camera": [ { "at": 0, "rect": [x, y, l, a] }, { "at": 3.0, "rect": […] } ], … },
    { "id": "more", "kind": "list", "items": [ { "en": "…", "pt": "…" } ], "stagger": 1.2, … },
    { "id": "closing", "kind": "closing", "headline": { … }, "link": "github.com/edilsonvilarinho/usage-monitor", … }
  ]
}
```

- `voice` é opcional (padrão `eleven-v4`/`george`). `lines[lang]` aceita um objeto (uma fala em `at` 0) ou a lista de
  beats; o validador recusa beat fora de ordem ou que passe do próximo `at` em mais de 1,5 s.
- Coordenadas (`crop`, `focus`, `camera`) em pixels da captura (4×). `focus` some depois de `focusFor` (padrão 2,5 s).
- `surface: "hud"` não aceita `camera`; cena de janela sem `camera` faz um Ken Burns leve.
- Cenas `steps` e `commands` continuam existindo, mas o padrão é demo real; use-as só para o que não tem tela.

## Onde mexer

| Arquivo | Papel |
|---|---|
| `scripts/collect-changes.mjs` | commits entre tags estáveis, por issue (testado) |
| `scripts/openrouter.mjs` | cliente de fala e imagem do OpenRouter (testado) |
| `scripts/speak.mjs` | fala por cena/beat, cache por assinatura, `durations.json` (testado) |
| `scripts/timeline.mjs` | ritmo, beats, tempos das cenas, legendas, SRT (testado) |
| `scripts/frames.mjs` | sequências de quadros das demos no palco (testado) |
| `scripts/scene-check.mjs` | validador do roteiro: câmera, `surface`, beats (testado) |
| `scripts/preview.mjs` | `preview.html` que dirige o `video.html` com a trilha (testado) |
| `scripts/social.mjs` | limites das redes e `social.md` (testado) |
| `assets/video.html` | renderizador: `renderFrame(t)` puro — câmera, foco, superfície, transição Gargantua |
| `scripts/render.mjs` | Chrome sem tela → ffmpeg; `RELEASE_ENCODE`/`DEFAULT_ENCODE`; `--stills` |
| `scripts/make-video.mjs` | orquestra: palco, fala, linha do tempo, prévia, render e áudio (`loudnorm` −16 LUFS) |
| `src/desktopTest/.../screenshots/VideoDemos.kt`, `Video*Demo*.kt` | demos de vídeo gravadas com as telas reais |
| `scripts/make-tour.mjs`, `assets/tour.html`, `scripts/soundtrack.py`, `scripts/synthesize.py` | tour 16:9 |
| `scripts/setup-tools.mjs` | instala as ferramentas fora de `build/` |

Testes: `node --test .claude/skills/usage-monitor-release-video/scripts/test/*.test.mjs` e
`gradlew.bat desktopTest --tests "*VideoDemos*" --tests "*VideoDemoPaceTest*" --tests "*SceneRecorderDragTest*"`.

Ao rodar com saída filtrada (`| tail`, `| grep`), use `set -o pipefail`: sem ele a recusa da linha do tempo sai com 0.
