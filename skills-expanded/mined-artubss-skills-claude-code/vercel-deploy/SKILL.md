---
name: vercel-deploy
description: Fazer deploy de aplicações e websites para a Vercel. Use quando o usuário solicitar ações de deploy como "deploy meu app", "deploy e me dá o link", "coloca isso no ar" ou "cria um deploy de preview".
author: openai
---

# Vercel Deploy

Faça deploy de qualquer projeto para a Vercel instantaneamente. **Sempre faça deploy como preview** (não produção) a menos que o usuário peça explicitamente por produção.

## Pré-requisitos

- Quando o sandbox bloqueia as chamadas de rede do deploy, execute novamente com `sandbox_permissions=require_escalated`.
- O deploy pode levar alguns minutos. Use valores de timeout apropriados.

## Início Rápido

**Apenas execute isto (com timeout de 10 minutos):**
```bash
vercel deploy [path] -y
```

**Importante:** Use timeout de 10 minutos (600000ms) para o comando de deploy, pois builds podem levar um tempo.

Se isso falhar com "No existing credentials found", use o método alternativo abaixo.

## Alternativo (Sem Autenticação)

Se a CLI falhar com erro de autenticação, use o script de deploy:

```bash
# Fazer deploy do diretório atual
bash scripts/deploy.sh

# Fazer deploy de um projeto específico
bash scripts/deploy.sh /path/to/project

# Fazer deploy de tarball existente
bash scripts/deploy.sh /path/to/project.tgz
```

O script cuida da detecção de framework, empacotamento e deploy. Aguarda a conclusão do build e retorna JSON com `previewUrl` e `claimUrl`.

**Diga ao usuário:** "Seu deployment está pronto em [previewUrl]. Reclame-o em [claimUrl] para gerenciar seu deployment."

## Deploy em Produção

Apenas se o usuário pedir explicitamente:
```bash
vercel deploy [path] --prod -y
```

## Saída

Mostre ao usuário a URL do deployment. Para deployments com fallback, também mostre a URL de claim.

**Não** faça curl ou fetch da URL do deployment para verificar se funciona. Apenas retorne o link.

## Solução de Problemas

### Acesso de Rede Escalado

Se o deployment falhar devido a problemas de rede (timeouts, erros DNS, conexões resetadas), execute novamente o deploy com permissões escaladas (use `sandbox_permissions=require_escalated`). O deploy requer acesso de rede escalado quando o sandbox bloqueia requisições outbound.

Exemplo de orientação ao usuário:

```
O deploy precisa de acesso de rede escalado para fazer deploy na Vercel. Posso executar novamente o comando com permissões escaladas—quer que eu prossiga?
```