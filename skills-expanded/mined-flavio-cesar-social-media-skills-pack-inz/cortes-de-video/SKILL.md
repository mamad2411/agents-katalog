---
name: cortes-de-video
description: "Transforma vídeos longos em cortes estratégicos para reels e shorts — recebe o arquivo de vídeo, transcreve, identifica os melhores trechos, CORTA o vídeo em arquivos separados prontos para postar e sugere hooks magnéticos para cada corte. Use esta skill sempre que alguém pedir para cortar vídeo para reels, identificar melhores momentos de um vídeo, criar cortes para Instagram/TikTok/YouTube Shorts, transformar live/podcast/vídeo longo em conteúdo curto, encontrar trechos virais, ou extrair clips de vídeo. Também aciona quando mencionarem 'cortar vídeo', 'melhores trechos', 'transformar em reels', 'clips do vídeo', 'cortes pra shorts', 'reaproveitar vídeo longo', ou quando enviarem um arquivo de vídeo pedindo para identificar momentos de impacto."
---

# Cortes de Vídeo — Reels & Shorts Estratégicos

Skill para transformar vídeos longos em cortes curtos e estratégicos. Recebe o arquivo de vídeo, transcreve, identifica os melhores momentos, **corta o vídeo em arquivos separados** e entrega tudo pronto para publicar.

## O que esta skill entrega

1. Arquivos de vídeo cortados (.mp4), um por trecho, prontos para postar
2. Uma lista dos cortes ranqueados por potencial de engajamento
3. Um hook magnético sugerido para cada corte
4. Tipo de conteúdo de cada corte (educativo, polêmico, emocional, prático)
5. Sugestão de copy para tela inicial de cada corte
6. Dicas de edição para maximizar o engajamento

## Fluxo de Trabalho

### Passo 1 — Receber e transcrever o vídeo

O usuário envia um arquivo de vídeo (.mp4, .mov, .webm, .avi, .mkv, etc.).

**Primeiro, extrair informações do vídeo:**
```bash
# Verificar duração e formato do vídeo
ffprobe -v quiet -print_format json -show_format -show_streams video.mp4
```

**Depois, transcrever com timestamps usando Whisper:**
```bash
# Instalar whisper se necessário
pip install openai-whisper --break-system-packages 2>/dev/null

# Transcrever com timestamps detalhados (formato SRT para ter timestamps por frase)
whisper video.mp4 --language pt --output_format srt --output_dir ./
```

Se Whisper falhar por falta de memória ou outro erro, tentar com o modelo menor:
```bash
whisper video.mp4 --language pt --output_format srt --output_dir ./ --model tiny
```

Se Whisper não estiver disponível de forma alguma, pedir ao usuário para colar a transcrição manualmente — mas sempre tentar instalar e rodar primeiro, porque o objetivo é automatizar o máximo possível.

**Alternativa — transcrição pronta:**
Se o usuário enviar a transcrição (texto ou .srt) em vez do vídeo, usar diretamente. Mas nesse caso, avisar que sem o arquivo de vídeo não é possível gerar os cortes automáticos — apenas a análise e recomendações de timestamps.

### Passo 2 — Analisar a transcrição e selecionar trechos

Ler a transcrição completa com timestamps e identificar trechos com alto potencial de engajamento.

**Gatilhos de viralização (o que procurar):**
- Frases de impacto ou provocativas que geram reação ("isso mudou meu jogo", "para de fazer isso agora")
- Momentos de revelação ou surpresa ("e foi aí que eu descobri que...")
- Dados ou números impressionantes ("isso me economiza 4 horas por semana")
- Contradições ao senso comum ("todo mundo faz X, mas o certo é Y")
- Histórias pessoais com virada emocional
- Demonstrações práticas com resultado visível ("olha o que acontece quando eu faço isso")
- Reações espontâneas e genuínas (risadas, espanto, emoção)

**Critérios técnicos de um bom corte:**
- Duração ideal: 15-60 segundos (priorizar 20-40s que é o sweet spot para reels)
- O trecho precisa fazer sentido sozinho, sem contexto adicional
- Deve ter início claro (frase de abertura forte) e fim natural
- Evitar trechos que começam ou terminam no meio de um raciocínio
- Dar preferência a trechos onde a pessoa está olhando para a câmera (se aplicável)

### Passo 3 — Cortar o vídeo com ffmpeg

Esta é a etapa mais importante: usar ffmpeg para cortar o vídeo em arquivos separados.

**Para cada corte identificado, executar:**
```bash
# Corte sem re-encoding (rápido, mantém qualidade original)
ffmpeg -y -ss [INICIO] -to [FIM] -i video_original.mp4 -c copy -avoid_negative_ts make_zero "corte-[N]-[slug-do-tema].mp4"

# Se o corte sem re-encoding ficar com problemas de sync ou início cortado,
# usar re-encoding (mais lento, mas mais preciso):
ffmpeg -y -i video_original.mp4 -ss [INICIO] -to [FIM] -c:v libx264 -preset fast -crf 23 -c:a aac -b:a 128k "corte-[N]-[slug-do-tema].mp4"
```

**Regras para os cortes:**
- Usar `-ss` ANTES de `-i` para seek rápido no modo copy, ou DEPOIS de `-i` para seek preciso no modo re-encode
- Adicionar 0.5s de margem no início (o espectador leva um instante para processar)
- O nome do arquivo deve ser descritivo: `corte-1-dica-produtividade.mp4`, `corte-2-historia-cliente.mp4`
- Sempre usar `-y` para sobrescrever sem perguntar
- Verificar que cada arquivo cortado foi gerado corretamente (checar se tem tamanho > 0)

**Verificação pós-corte:**
```bash
# Verificar duração de cada corte
for f in corte-*.mp4; do
  echo "$f: $(ffprobe -v quiet -show_entries format=duration -of csv=p=0 "$f")s"
done
```

**Salvar os cortes na pasta de outputs:**
```bash
# Criar pasta para os cortes
mkdir -p /sessions/determined-serene-johnson/mnt/outputs/cortes/

# Mover todos os cortes para lá
mv corte-*.mp4 /sessions/determined-serene-johnson/mnt/outputs/cortes/
```

### Passo 4 — Montar o relatório dos cortes

Para cada corte, entregar as informações estratégicas:

```
═══════════════════════════════════════
corte #[número] — [tipo: educativo/polêmico/emocional/prático/inspiracional]
📁 arquivo: corte-[N]-[slug].mp4
potencial de engajamento: [alto/muito alto/viral]
═══════════════════════════════════════

⏱️ timestamps originais: [início] → [fim] (duração: Xs)

📱 hook sugerido para tela inicial:
[copy curta e impactante, máximo 2 linhas, lowercase]

🎤 o que é falado nesse trecho:
"[transcrição exata do trecho]"

💡 por que esse trecho funciona:
[explicação breve — qual gatilho de viralização ele ativa]

✂️ dica de edição:
[sugestão prática — ex: "adicionar texto animado na frase X", "começar com zoom", "usar legendas auto"]
```

### Passo 5 — Ranking final e recomendações

```
🏆 ranking dos cortes (do maior para menor potencial):

1. corte #X — [razão em uma frase] → arquivo: corte-X-[slug].mp4
2. corte #Y — [razão em uma frase] → arquivo: corte-Y-[slug].mp4
3. corte #Z — [razão em uma frase] → arquivo: corte-Z-[slug].mp4

💎 recomendação:
- se for publicar apenas 1, vá com o corte #X porque [razão estratégica]
- se puder publicar 3 ao longo da semana: #X (segunda), #Y (quarta), #Z (sexta)
- melhor horário para postar reels: entre 11h-13h ou 18h-20h

📁 todos os cortes estão na pasta "cortes/"
```

### Passo 6 — Entregar os arquivos

Compartilhar links para cada arquivo cortado usando o formato:
```
[Ver corte #1 — nome-do-corte](computer:///sessions/determined-serene-johnson/mnt/outputs/cortes/corte-1-slug.mp4)
```

## Regras Importantes

### Quantidade de cortes
- Vídeo curto (até 5min): identificar 2-4 cortes
- Vídeo médio (5-20min): identificar 4-8 cortes
- Vídeo longo (20min+): identificar 6-12 cortes
- Nunca forçar cortes fracos só para completar número. Qualidade > quantidade.

### Tom dos hooks
Os hooks sugeridos devem ser:
- Curtos (máximo 2 linhas na tela)
- Em português brasileiro natural
- Gerar curiosidade ou espanto imediato
- Prometer um resultado ou revelação
- Em letras minúsculas (padrão Instagram atual)

Bons exemplos:
- "ninguém te conta isso sobre [tema]"
- "eu fazia errado por 3 anos até descobrir que..."
- "para tudo e assiste isso"
- "o que acontece quando você [ação] é insano"

### Qualidade do vídeo
- Manter a qualidade original sempre que possível (usar `-c copy` primeiro)
- Se o corte com `-c copy` tiver problemas (áudio dessincronizado, frame congelado no início), refazer com re-encoding
- Formato de saída sempre .mp4 (compatível com todas as plataformas)
- Não redimensionar ou alterar aspect ratio — o criador faz isso no app de edição se quiser

### Sobre o idioma
- O vídeo pode estar em qualquer idioma
- Os hooks e recomendações devem ser sempre em português brasileiro
- Se o vídeo for em outro idioma, transcrever no idioma original e traduzir os trechos relevantes

## Troubleshooting

### Whisper demora muito ou trava
Usar modelo menor: `--model tiny` ou `--model base`. Qualidade menor mas muito mais rápido.

### Corte tem frame preto no início
Adicionar `0.1s` ao timestamp de início, ou usar re-encoding em vez de copy mode.

### Áudio dessincronizado no corte
Usar re-encoding: trocar `-c copy` por `-c:v libx264 -preset fast -crf 23 -c:a aac -b:a 128k`

### Vídeo muito grande (>500MB)
Avisar o usuário que a transcrição pode demorar alguns minutos. Considerar extrair apenas o áudio primeiro para acelerar a transcrição:
```bash
ffmpeg -i video_grande.mp4 -vn -acodec pcm_s16le -ar 16000 -ac 1 audio.wav
whisper audio.wav --language pt --output_format srt --output_dir ./
```

## Checklist de qualidade

Antes de entregar os cortes, verificar:
- [ ] Cada arquivo .mp4 foi gerado e tem tamanho > 0?
- [ ] Cada corte faz sentido sozinho, sem precisar de contexto?
- [ ] Os hooks geram curiosidade real?
- [ ] As durações estão no range ideal (15-60s)?
- [ ] O ranking final está coerente com os critérios?
- [ ] Os nomes dos arquivos são descritivos?
- [ ] Tem variedade de tipos de conteúdo entre os cortes?
- [ ] As dicas de edição são práticas e acionáveis?
- [ ] Os arquivos estão salvos na pasta de outputs e com links compartilhados?

