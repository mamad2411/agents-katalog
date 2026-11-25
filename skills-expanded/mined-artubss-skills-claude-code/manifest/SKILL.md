---
name: Manifest
description: Instale e configure o plugin de observabilidade Manifest para seus agentes. Use ao configurar telemetria, definir chaves de API ou endpoints, resolver problemas de conexão do plugin ou verificar se o pipeline de observabilidade está em execução.
---

# Configuração do Manifest

Configure observabilidade em tempo real para seus agentes de IA com o plugin Manifest. Monitora custos, tokens, mensagens e desempenho via telemetria OTLP.

## Quando Usar Esta Habilidade

Use esta habilidade quando:
- Configurar observabilidade ou telemetria para um agente de IA
- Conectar um agente ao Manifest para monitoramento de custos e desempenho
- Configurar uma chave de API do Manifest ou um endpoint customizado
- Resolver problemas de conexão do plugin Manifest
- Verificar se o pipeline de observabilidade do Manifest está em execução

## Instruções de Configuração

Siga estas etapas **na ordem apresentada**. Não pule nenhuma.

### Etapa 1 — Parar o Gateway

Pare o gateway primeiro para evitar problemas de hot-reload durante a configuração.

```bash
claude gateway stop
```

### Etapa 2 — Instalar o Plugin

```bash
claude plugins install manifest
```

Se falhar, verifique se a CLI está instalada e disponível no PATH.

### Etapa 3 — Obter uma Chave de API

Peça ao usuário:

> Para conectar seu agente, você precisa de uma chave de API do Manifest:
>
> 1. Acesse **https://app.manifest.build** e crie uma conta (ou faça login)
> 2. Clique em **"Connect Agent"** para criar um novo agente
> 3. Copie a chave de API que começa com `mnfst_`
> 4. Cole-a aqui

Aguarde uma chave que comece com `mnfst_`. Se a chave não corresponder, diga ao usuário que o formato parece incorreto e peça para tentar novamente.

### Etapa 4 — Configurar o Plugin

```bash
claude config set plugins.entries.manifest.config.apiKey "USER_API_KEY"
```

Substitua `USER_API_KEY` pela chave real que o usuário forneceu.

Se o usuário tiver um endpoint customizado (self-hosted):

```bash
claude config set plugins.entries.manifest.config.endpoint "USER_ENDPOINT"
```

O endpoint padrão (`https://app.manifest.build/api/v1/otlp`) é usado automaticamente se nenhum for especificado.

### Etapa 5 — Iniciar o Gateway

```bash
claude gateway install
```

### Etapa 6 — Verificar

Aguarde 3 segundos para o gateway iniciar completamente e, em seguida, verifique os logs:

```bash
grep "manifest" ~/.claude/logs/gateway.log | tail -5
```

Procure por:

```
[manifest] Observability pipeline active
```

Se aparecer, diga ao usuário que a configuração está completa. Se não, verifique as mensagens de erro e resolva os problemas.

## Resolução de Problemas

| Erro | Solução |
|------|---------|
| Missing apiKey | Re-execute a Etapa 4 com a chave correta |
| Invalid apiKey format | A chave deve começar com `mnfst_` |
| Connection refused | Endpoint está inacessível — verifique a URL ou pergunte se está usando self-hosting |
| Duplicate OTel registration | Desabilite o plugin built-in conflitante: `claude plugins disable diagnostics-otel` |

## Melhores Práticas

- Sempre pare o gateway antes de fazer alterações de configuração
- O endpoint padrão funciona para a maioria dos usuários — altere-o apenas se estiver usando self-hosting
- Chaves de API sempre começam com `mnfst_` — qualquer outro formato é inválido
- Nunca registre ou exiba a chave de API em texto simples após a configuração
- Verifique os logs do gateway primeiro ao depurar qualquer problema de plugin