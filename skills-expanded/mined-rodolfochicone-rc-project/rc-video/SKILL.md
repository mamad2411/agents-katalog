---
name: rc-video
description: "Guias para trabalhar com vídeo. Use ao manipular arquivos com ffmpeg (cortar, transcodificar, extrair frames/áudio, legendar, comprimir, HLS), planejar conteúdo (roteiro, storyboard, Reels/Shorts/YouTube) ou integrar o VideoDB. Não use para edição em GUI ou streaming ao vivo."
user-invocable: true
model: sonnet
effort: medium
---

# Vídeo — guias por tarefa

Leia o guia da tarefa em `references/` antes de agir. Para processamento local, o único
pré-requisito é o `ffmpeg` instalado (`ffmpeg -version`); nenhuma API paga é necessária.

## Roteamento

| Tarefa | Guia |
| ------ | ---- |
| Manipular arquivos de vídeo/áudio localmente (ffmpeg) | `references/ffmpeg.md` |
| Planejar/roteirizar conteúdo em vídeo (Reels/Shorts/YouTube) | `references/content.md` |
| Ingest/busca/edição via VideoDB (SaaS pago — opcional) | `references/videodb.md` |

## Escolha do caminho

- **Precisa cortar, converter, comprimir, legendar ou extrair algo de um arquivo?** → `ffmpeg.md`. É local, grátis e resolve a grande maioria dos casos. **Prefira sempre esta opção.**
- **Precisa planejar o que gravar/publicar (roteiro, gancho, estrutura, metadados)?** → `content.md`.
- **Precisa de busca semântica dentro do vídeo, indexação de fala/cena ou edição por timeline gerenciada?** → `videodb.md`, ciente do custo e do lock-in num SaaS pago.

## Error Handling

- `ffmpeg: command not found` → instrua a instalação (`brew install ffmpeg` no macOS) e pare; não tente workaround.
- VideoDB sem `VIDEO_DB_API_KEY` → não é erro de código: informe que a integração é opcional e exige a chave; ofereça o caminho ffmpeg local quando o objetivo for alcançável sem o SaaS.
