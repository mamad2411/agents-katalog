---
name: video-watch
description: Assistir/analisar um vídeo local ou de link compartilhado (CleanShot, Loom, mp4 direto) — extrai frames-chave como imagens e transcreve o áudio offline com whisper.cpp. Use quando mandarem uma gravação de tela para assistir, resumir ou transcrever, ou quando um bug for demonstrado em vídeo. YouTube público vai pelo conector Watch Any Video. Gatilhos - "cleanshot.com/share", "loom.com/share", ".mp4".
disable-model-invocation: true
allowed-tools:
  - 'Bash(bash "${CLAUDE_PLUGIN_ROOT}/skills/video-watch/scripts/watch.sh" *)'
  - 'Bash(bash ${CLAUDE_PLUGIN_ROOT}/skills/video-watch/scripts/watch.sh *)'
---

# video-watch

Você não processa vídeo nem áudio nativamente. Esta skill converte o vídeo em duas
coisas que você **consegue** ler: frames JPEG (via `Read`, que exibe imagens) e um
transcript de texto.

## Esta skill ou o conector Watch Any Video?

O conector da comunidade [Watch Any Video](https://claude.ai/directory/watch-any-video)
(`watchanyvideo.com/api/mcp`, da Wikivec) cobre o que esta skill não cobre. Ele manda o vídeo
para o Gemini do Google, que analisa e devolve a resposta com timestamps.

| Situação | Use |
|---|---|
| YouTube público (aula, palestra, Shorts, live passada) | conector |
| Fora do Claude Code (claude.ai na web, celular) ou máquina sem ffmpeg/whisper | conector |
| Precisa de timestamp por fala ou de várias perguntas sobre o mesmo vídeo | conector (`ask_video` não gasta minutos) |
| Gravação de tela de bug, CleanShot, Loom | **esta skill** (o conector não resolve página de share) |
| Reunião de cliente, dado sensível, vídeo privado ou não listado | **esta skill**: o vídeo não sai da máquina |
| Instagram, TikTok, Facebook, X | nenhum dos dois: baixe o arquivo e passe local para esta skill |

Antes de mandar um vídeo para o conector, confira se ele pode sair da máquina: ele não é
verificado pela Anthropic e guarda perguntas e respostas por 7 dias. Na dúvida, esta skill.
O plano grátis dá 60 min de vídeo por mês (`my_usage` mostra o saldo).

## Uso

```bash
bash "${CLAUDE_PLUGIN_ROOT}/skills/video-watch/scripts/watch.sh" <url-ou-arquivo> [opções]
```

| Opção | Default | Para quê |
|---|---|---|
| `--out DIR` | `$TMPDIR/video-watch/<ts>` | onde gravar frames/transcript |
| `--frames N` | `16` | teto de frames extraídos |
| `--lang pt` | `pt` | idioma do áudio (`en`, `auto`, …) |
| `--interval S` | auto | força 1 frame a cada S segundos em vez de corte de cena |
| `--no-audio` | — | pula a transcrição (screencast mudo) |

O script imprime um índice com duração, resolução, os caminhos dos frames e o
caminho do transcript. Depois: **`Read` no transcript e `Read` nos frames que
importam** — é aí que você de fato "assiste".

## Fluxo obrigatório

1. Rode `watch.sh` com a URL.
2. `Read` o `transcript.txt` inteiro (é texto, barato).
3. `Read` os frames — **seletivamente**. Cada imagem custa ~1,5k tokens; 16 frames
   ≈ 24k. Leia 4–6 primeiro; puxe o resto só se o transcript apontar um trecho
   visual que você precisa ver.
4. Vídeo mudo (`áudio: não` no índice) → o sinal está todo nos frames; aí vale ler
   todos e pedir `--frames 24` se o fluxo for longo.

## Como os frames são escolhidos

Corte de cena (`scene > 0.25`) por padrão — em screencast isso pega troca de tela,
abertura de modal, navegação. Se render menos de 4 frames (vídeo estático, ex.:
alguém falando sobre uma tela parada), cai automaticamente para intervalo fixo.
Timestamps não vêm no nome do arquivo; ancore o "quando" pelo transcript.

## Pré-requisito — confira antes do primeiro uso

```bash
command -v ffmpeg ffprobe whisper-cli python3 curl | wc -l   # tem que dar 5
ls -l "${WHISPER_MODEL:-$HOME/.cache/whisper-cpp/models/ggml-large-v3-turbo.bin}"
```

(Leia a contagem, não o exit code: com um nome faltando, o `command -v` sai 0 no bash e
1 no zsh. Deu menos de 5 → rode sem o `| wc -l` e veja qual não apareceu.)

- **Binários:** no macOS, `brew install ffmpeg whisper-cpp` — dá `ffmpeg`, `ffprobe` e
  `whisper-cli`. A skill foi feita e testada no macOS. No Linux, o `ffmpeg` vem do gerenciador
  de pacotes e o `whisper-cli` sai do build do whisper.cpp; no Windows ela não foi testada.
  **ffmpeg >= 5.1** (`ffmpeg -version | head -1`): o script usa `-fps_mode`,
  que não existe antes disso. `python3` e `curl` já vêm no macOS; o `resolve-url.py` usa só a
  stdlib, não há `pip install`.
- **Modelo whisper** (~1,5 GB, uma vez por máquina):

```bash
mkdir -p ~/.cache/whisper-cpp/models
curl -L -o ~/.cache/whisper-cpp/models/ggml-large-v3-turbo.bin \
  https://huggingface.co/ggerganov/whisper.cpp/resolve/main/ggml-large-v3-turbo.bin
```

  Guardou em outro lugar → `WHISPER_MODEL=/caminho/outro.bin`.

**Modelo ausente não aborta o script.** O `watch.sh` escreve
`!! modelo whisper ausente` no stderr, segue extraindo os frames e fecha o índice com
`transcript: — (falhou)`. Transcript que some sem explicação é isto — confira o `ls`
acima antes de culpar o vídeo.

Tudo roda offline; o vídeo não sai da máquina exceto para baixar do host original.

## Limites conhecidos

- O `transcript.txt` não traz tempo, com ou sem `-nt`. Para sincronizar fala↔tela, rode o
  whisper de novo sobre o `audio.wav` que ficou no `--out`, sem `-nt` (com ele o `.srt` sai em
  janelas de 30 s) e com `-osrt`:
  `whisper-cli -m "${WHISPER_MODEL:-$HOME/.cache/whisper-cpp/models/ggml-large-v3-turbo.bin}" -f <out>/audio.wav -l pt -np -mc 0 -osrt -of <out>/transcript`
  → `<out>/transcript.srt`, com `00:00:00,000 --> …` por frase.
- CleanShot/Loom/og:video cobertos pelo `resolve-url.py`. Host novo que falhar:
  abra a página e pegue o `.mp4` do painel Network, ou passe o arquivo local.
- URL assinada do CleanShot expira — resolva e baixe na mesma execução (o script
  já faz), não guarde a URL direta para depois.
- ffmpeg < 5.1 falha com `Unrecognized option 'fps_mode'` — atualize (`brew upgrade ffmpeg`).
  O inverso (`-vsync` no ffmpeg 9) e o `Non full-range YUV is non-standard` do mjpeg já
  estão tratados no `watch.sh`.
- Vídeo grande (>10 min) → `--frames 24` e espere ~1 min de transcrição.
