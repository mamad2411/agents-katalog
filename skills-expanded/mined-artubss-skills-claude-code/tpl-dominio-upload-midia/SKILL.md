---
name: tpl-dominio-upload-midia
description: Template do pack (dominio/09-upload-midia.md). Orienta o agente em regras de negocio e requisitos de produto alinhado a esse contexto.
metadata:
  version: 1.0.0
  source_template: dominio/09-upload-midia.md
  generated_by: install_pack_templates_as_claude_skills
---

# DOMAIN: Upload e Processamento de Mídia

Skill gerado a partir do pack `templates-claude-code`. Arquivo de origem: `dominio/09-upload-midia.md`. Use como baseline e adapte ao projeto antes de mudancas grandes.

## Conteudo do template

## CONTEXT
Upload de arquivo parece trivial até o primeiro vídeo de 4GB enviado para sua memória RAM,
ou o primeiro arquivo malicioso que bypassa validação de extensão. O fluxo correto é
upload direto para storage (sem passar pelo servidor), validação de conteúdo real,
processamento assíncrono e entrega via CDN — não via aplicação.

## STACK ASSUMPTIONS
- Storage: AWS S3 / GCS / Cloudflare R2
- CDN: CloudFront / Cloudflare para entrega de assets
- Processing: Sharp (imagens Node.js) / FFmpeg (vídeo) / ImageMagick
- Virus Scan: ClamAV / AWS Macie / VirusTotal API
- Queue: BullMQ / SQS para processamento assíncrono
- DB: PostgreSQL para metadados de mídia

## CORE CONCEPTS
- **Signed URL**: URL pré-assinada com TTL que permite upload direto para S3 sem passar pelo servidor
- **Multipart Upload**: S3 upload em partes para arquivos > 5MB (suporta pause/resume)
- **MIME Type Sniffing**: verificar bytes mágicos do arquivo, não apenas extensão
- **Image Pipeline**: thumbnails em múltiplos tamanhos gerados assincronamente
- **Transcoding**: converter vídeo para HLS ou MP4 padronizado via FFmpeg
- **Soft Delete**: marcar como deletado mas manter no S3 por período configurável
- **Lifecycle Policy**: S3 lifecycle para deletar objetos expirados automaticamente
- **CDN Key Signing**: URLs CDN assinadas para conteúdo privado (com TTL)

## ARCHITECTURE RULES

### Upload Flow (Direto para S3)
```
1. Client → POST /media/presign     → Servidor retorna {uploadUrl, mediaId, fields}
2. Client → PUT <uploadUrl>          → Upload direto ao S3 (sem passar pelo servidor)
3. Client → POST /media/:id/confirm  → Dispara job de processamento + validação
4. [Job Worker] valida MIME, escaneia vírus, processa imagem/vídeo
5. [Job Worker] atualiza media record: status → ready | failed
6. Client → GET /media/:id/status   → Polling até status = ready
```

### Validação de Arquivo
- Nunca aceitar arquivo apenas por extensão — verificar magic bytes
- Whitelist de tipos permitidos por contexto (avatar: apenas imagem; video: mp4/mov/webm)
- Tamanho máximo por tipo: imagens (20MB), vídeos (2GB), docs (50MB)
- Virus scan obrigatório antes de disponibilizar publicamente
- Quarantine bucket: arquivos aguardam scan em bucket privado, movidos após aprovação

### Magic Bytes por Tipo
```
JPEG: FF D8 FF
PNG:  89 50 4E 47 0D 0A 1A 0A
GIF:  47 49 46 38
PDF:  25 50 44 46
ZIP:  50 4B 03 04
MP4:  (ftyp box em offset 4)
```

### Image Processing Pipeline
- Gerar sincronamente: thumbnail (150x150 crop center)
- Gerar assincronamente: medium (800px), large (1200px), original compressed
- Formato output: WebP com fallback JPEG (60% menor que JPEG)
- Metadados EXIF: strip (privacidade — remove GPS, device info)
- Watermark: aplicar após resize, não antes (qualidade)

### Video Processing
- Validar codec antes de transcodar (FFprobe para metadata)
- Output: MP4 H.264 + AAC (máximo compatibilidade) + HLS para streaming
- Thumbnail: frame em 10% da duração
- Progress: reportar via WebSocket ou job status polling
- Streaming HLS: segmentos de 6s, manifest .m3u8

## ROUTING TABLE
| Trigger | Action |
|---------|--------|
| POST /media/presign | Criar media record (status: pending) → gerar signed URL S3 → retornar |
| POST /media/:id/confirm | Verificar que arquivo existe no S3 → enfileirar jobs validation + processing |
| GET /media/:id/status | Retornar status atual do media e jobs de processamento |
| GET /media/:id | Retornar metadata + URLs CDN por tamanho (apenas se status: ready) |
| DELETE /media/:id | Soft delete → schedule cleanup job → remover de conteúdos associados? |
| POST /media/batch-confirm | Confirmar múltiplos uploads de uma vez (galeria) |
| GET /admin/media?status=quarantine | Listar arquivos em quarentena para revisão |
| POST /admin/media/:id/approve | Aprovar arquivo em quarentena → mover para bucket público |
| POST /admin/media/:id/reject | Rejeitar arquivo → notificar usuário → deletar do S3 |
| PUT /media/:id/replace | Versionar mídia existente (manter versão anterior) |
| GET /media/:id/versions | Histórico de versões de um asset |
| POST /webhooks/s3/event | Receber S3 event notifications (ex: scan completado) |

## CRITICAL RULES
1. Upload direto para S3 — nunca receber arquivo pelo servidor de aplicação
2. MIME type verificado por magic bytes no servidor, não por extensão ou Content-Type header
3. Virus scan antes de disponibilizar qualquer arquivo publicamente
4. S3 key não deve ser adivinável — usar UUID no path, não filename do usuário
5. EXIF metadata stripped de todas as imagens antes de servir (privacidade)
6. Signed URLs de CDN para conteúdo privado com TTL (não S3 URLs diretas)
7. FFmpeg sandbox: executar em processo isolado com limits de CPU/memória
8. Soft delete: marcar no DB + S3 lifecycle policy para deletar após 30 dias
9. Multipart upload para arquivos > 5MB (S3 limite para single PUT)
10. Arquivos processados: nunca servir o objeto S3 original — sempre servir CDN URL

## COMMON PITFALLS

### ❌ Upload pelo servidor — OOM em produção
```javascript
// ERRADO: arquivo inteiro em memória do servidor
app.post('/upload', upload.single('file'), async (req) => {
  const buffer = req.file.buffer; // 2GB vídeo → OOM
  await s3.putObject({ Body: buffer, ... });
});

// CORRETO: signed URL para upload direto
app.post('/media/presign', async (req) => {
  const key = `uploads/${uuid()}`;
  const url = await s3.getSignedUrlPromise('putObject', { Key: key, Expires: 300 });
  return { uploadUrl: url, key };
});
// Cliente faz PUT diretamente para S3
```

### ❌ Confiar no Content-Type do cliente
```javascript
// ERRADO: cliente pode enviar image/jpeg para arquivo .exe
if (req.headers['content-type'] === 'image/jpeg') { processAsImage(); }

// CORRETO: ler magic bytes do arquivo
import { fileTypeFromBuffer } from 'file-type';
const buffer = await readFirstBytes(s3Key, 16);
const type = await fileTypeFromBuffer(buffer);
if (type?.mime !== 'image/jpeg' && type?.mime !== 'image/png') {
  throw new Error('Invalid file type');
}
```

### ❌ S3 URL direta para conteúdo privado
```javascript
// ERRADO: URL pública e permanente, não pode revogar
const url = `https://bucket.s3.amazonaws.com/${key}`;

// CORRETO: signed URL com TTL
const url = await s3.getSignedUrlPromise('getObject', {
  Key: key,
  Expires: 3600 // 1 hora
});
```

## QUALITY GATES
- [ ] Zero arquivos recebidos como buffer pelo servidor de aplicação
- [ ] MIME type verificado por magic bytes (não por extensão)
- [ ] Virus scan realizado antes de status = ready/public
- [ ] EXIF stripped de todas as imagens
- [ ] CDN signed URLs para conteúdo privado
- [ ] S3 keys não adivinháveis (UUID no path)
- [ ] Multipart upload implementado para arquivos > 5MB
- [ ] Pipeline de processamento assíncrono com status tracking
- [ ] Soft delete com lifecycle policy configurado no S3
- [ ] FFmpeg rodando em processo sandboxado com resource limits

## FORBIDDEN
- Receber arquivo como multipart/form-data no servidor de aplicação
- Confiar no `Content-Type` header enviado pelo cliente
- Servir arquivos diretamente do S3 sem CDN
- URLs permanentes para conteúdo privado (sem TTL)
- Processar vídeo ou imagem de alta resolução na thread principal
- Disponibilizar arquivo sem virus scan
- Incluir filename do usuário no S3 key (path traversal / predictability)
