---
name: usage-monitor-social-video
description: Generate social videos about any theme (text, facts or images) in the approved Usage Monitor look, with voice, soundtrack, captions and post copy for TikTok, YouTube Shorts, LinkedIn, X and YouTube long form. Use for "vídeo sobre", "vídeo para as redes", "vídeo para TikTok/Shorts/LinkedIn/X/YouTube" when the subject is not a release; releases use usage-monitor-release-video.
---

# Usage Monitor — vídeos para redes a partir de um tema

Entrada: um tema, com informações, imagens ou só texto, e uma chave temporária da OpenRouter. Saída: 6 vídeos, legendas e
descrições. O padrão foi aprovado pelo dono no #540 e **não muda por tema**:

| Item | Padrão |
|---|---|
| Visual | Modelo 01 Horizonte de eventos (`assets/scene.js`), design system do projeto |
| Voz | `elevenlabs/eleven-v4`: `matilda` (PT), `george` (EN), pela OpenRouter, via harness do opencode |
| Trilha | Pulso de sonda, sintetizada em `scripts/audio.py`, sem amostra de terceiros |
| Plataformas | TikTok e Shorts (PT, 9:16, 1 min), LinkedIn (PT, 16:9, 1 min), X (EN, 16:9, 1 min), YouTube (PT e EN, 16:9, 5 min) |

Vídeo novo é **dado, não código**: só muda o `video.json` (contrato em [`references/video-spec.md`](references/video-spec.md)).
Pedido de outro visual, voz ou trilha é mudança da skill, com protótipos antes; nunca ajuste no meio de um vídeo.

Todo o trabalho segue o fluxo do `CLAUDE.md`. Versionado: `docs/planos/video-<slug>/` (`video.json`, `roteiro.md`, `social.md`,
imagens). Mídia fica fora: `build/social-video/<slug>/` e `~/Videos/usage-monitor/<slug>/`. A skill **não publica** nada.

## Passo a passo

1. **Material.** Tema e fontes. Número, nome ou afirmação só entra com origem: o que o dono mandou ou o que você mediu com
   comando. Se faltar dado, pergunte; nunca complete. Olhe cada imagem: credencial, e-mail ou dado pessoal visível bloqueia o uso.
2. **Roteiro.** Escreva `video.json` e, a partir dele, `roteiro.md` com as duas versões. Um roteiro que só cita etapas foi recusado
   pelo dono: **cada etapa diz o que acontece e como**, com o artefato real em tela.
   - **Curto:** teto medido de 630 caracteres por idioma (12,2 caracteres/s); cada fala tem uma ação e um porquê.
   - **Longo:** até 3400 caracteres, no máximo 15 etapas, cada uma com 2 a 4 frases, abrindo com o contexto e fechando com um caso real.
   - Fala curta, sem jargão desnecessário; `facts` lista todo número usado.
3. **Conferência.** `node <skill>/scripts/make.mjs check <video.json>`. Erro de teto se resolve cortando texto, nunca acelerando voz.
4. **Prévia, sem gastar API.** `node <skill>/scripts/make.mjs preview <video.json>`: gera linha do tempo estimada e quadros em
   `build/social-video/<slug>/qa/`, com folha de contato `sheet.jpg`. **Olhe a folha você mesmo**: texto cortado, sobreposição, imagem
   ilegível ou faixa de legenda invadida voltam para o `video.json`.
5. **Parada obrigatória.** Mande `roteiro.md` e a folha ao dono e espere o ok. Nada de voz nem render antes: render longo custa
   cerca de 14 minutos por idioma, e o dono já recusou roteiro depois do visual aprovado.
6. **Chave.** Peça a chave só agora, se não veio. Grave em arquivo temporário fora do repositório e passe por variável de ambiente.
   Nunca em comando impresso, log, `video.json` ou commit. Ao terminar, apague o arquivo e diga ao dono para revogar.
7. **Voz.** Pelo harness do opencode, com a entrada fechada; sem `</dev/null` o processo fica parado sem saída:

   ```bash
   OPENROUTER_API_KEY="$(cat <arquivo>)" opencode run --format json -m openrouter/anthropic/claude-haiku-5.5 \
     "Rode node <skill>/scripts/make.mjs voice <video.json> e devolva a saída. Nunca imprima a chave." </dev/null > <scratch>/voice.jsonl
   ```

   Rode em segundo plano. Depois confirme que a saída não contém `sk-or-`. O relatório diz o custo aproximado e as falas medidas;
   se o `gap` ficar abaixo de 0,8 s, corte texto e refaça só os segmentos alterados.
8. **Render.** `node <skill>/scripts/make.mjs render <video.json>` em segundo plano (`--only <variante>` para refazer uma). Medido: 3 minutos
   por vídeo de 60 s e 14 minutos por vídeo longo, com dois em paralelo.
9. **Validação com evidência própria.** `ffprobe` (resolução, 30 fps, duração), `ebur128` (cerca de −14 LUFS, pico abaixo de −1 dBTP) e
   quadros extraídos **do MP4 final**, nos dois formatos e idiomas. Relatório de agente não conta.
10. **Descrições.** `docs/planos/video-<slug>/social.md`, uma seção por rede, no formato de `docs/planos/video-fluxo-540/social.md`:
    capítulos do YouTube pelos tempos reais de `build/social-video/<slug>/long-*.js`, X até 280 caracteres (link conta 23), TikTok com
    "Link na bio". Texto publicado sai na voz do dono: sem opinião ou resultado que ele não afirmou.
11. **Entrega,** em até 15 linhas: caminho dos arquivos, duração, custo real, o que não foi verificado. Sempre diga que **ninguém
    ouviu** o resultado: pronúncia e qualidade da voz dependem da escuta do dono.

## Regras aprendidas

| Regra | Por quê |
|---|---|
| Velocidade da voz nunca muda | Pedido do dono no #503 e no #540; o conserto é cortar texto |
| Sigla escrita ≠ falada | `say` e `toSpoken` cuidam da voz; a legenda usa o texto escrito |
| Sem nome de filme, compositor ou logotipo de terceiro | Direitos autorais; prompt de trilha é descritivo |
| Dado na cena vem de `facts` | Número inventado em vídeo público não tem conserto depois de postado |
| Imagem de terceiro só com licença clara | O vídeo é público |
| Teste curto antes de render longo | `make.mjs render <video.json> --silent --to 3` prova trilha, cena e encode sem voz nem API; grava em `smoke/` |
| `drawtext` do ffmpeg não é usado | Falhou com `Segmentation fault` nesta máquina (fontconfig) |

Testes: `node --test ".claude/skills/usage-monitor-social-video/scripts/test/*.test.mjs"`. O CI não os roda.
