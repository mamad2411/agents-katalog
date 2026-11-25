---
name: banco-inter-api
description: Use esta skill para implementar, revisar, depurar, testar, migrar ou explicar integrações com a plataforma de desenvolvedores do Banco Inter Empresas, incluindo OAuth 2.0 + mTLS, Banking, Pix, Pix Automático, Cobrança Boleto com Pix V3, Webhooks, Sandbox, SDKs, CNAB, Crédito Empresas e Crédito Imobiliário.
license: MIT
compatibility: Compatível com clientes que suportam Agent Skills, incluindo ChatGPT, Codex e Claude Code. Para mudanças sensíveis em produção, recomenda-se acesso à web para confirmar a documentação oficial atual.
metadata:
  author: whyrnld
  version: "1.2.0"
  language: pt-BR
---

# Banco Inter API

Use esta skill em trabalhos de engenharia envolvendo a plataforma de desenvolvedores do Banco Inter. O snapshot de conhecimento deste repositório foi auditado em **19/08/2026** a partir do portal oficial.

## Prioridade das fontes

Quando houver divergência, use esta ordem:

1. **API Reference atual** para contrato de endpoint, método, path, scope, rate limit, parâmetros e respostas.
2. **Guias atuais** para configuração e orientação operacional.
3. **Documentação atual específica do produto** para superfícies de Crédito Empresas e Crédito Imobiliário.
4. **Changelog** para histórico de migração e data em que um comportamento foi introduzido ou removido.
5. FAQ e páginas de suporte apenas como orientação complementar.

Nunca reative um contrato legado apenas porque ele aparece em um changelog antigo. Se a referência atual e o changelog divergirem, informe a divergência e prefira a referência operacional atual, salvo quando a tarefa for explicitamente histórica.

## Fluxo obrigatório

1. Identifique a superfície do produto antes de escrever código: Token/Auth, Banking, Pix, Pix Automático, Cobrança V3, Fórum, Crédito Empresas, Crédito Imobiliário, Webhook, Sandbox, SDK ou CNAB.
2. Leia o arquivo correspondente em `references/` antes de propor endpoint, scope, enum, rate limit ou payload.
3. Para trabalho sensível a mudanças, leia também `references/14-changelog-migrations.md`.
4. Se houver acesso à web, confirme a página oficial relevante antes de mudanças em produção, pois o snapshot pode ficar desatualizado.
5. Preserve identificadores técnicos exatamente. Não normalize grafia de enums, underscores, caixa, UUIDs, headers ou nomes de campos.
6. Se a documentação oficial for internamente inconsistente, informe a inconsistência em vez de adivinhar.

## Segurança

- Nunca publique, solicite para publicação, faça commit ou registre em logs um `client_secret`, chave privada, `.key`, `.pfx`, `.p12`, senha de certificado ou access token real.
- Use placeholders como `$CLIENT_ID`, `$CLIENT_SECRET`, `/caminho/cert.crt`, `/caminho/private.key`.
- Nas APIs padrão Inter Empresas, mantenha credenciais e certificado da **mesma integração**.
- Trate documentos de Crédito Imobiliário como confidenciais e não registre conteúdo ou URLs assinadas.
- Mantenha segredos fora do controle de versão.

## Autenticação padrão Inter Empresas

As APIs PJ padrão usam **mTLS + OAuth 2.0 client credentials**. No snapshot auditado:

- Produção: `https://cdpj.partners.bancointer.com.br/oauth/v2/token`
- Sandbox: `https://cdpj-sandbox.partners.uatinter.co/oauth/v2/token`

Envie `client_id`, `client_secret`, `grant_type=client_credentials` e `scope` separado por espaços como `application/x-www-form-urlencoded`, apresentando o certificado/chave da integração para mTLS. Reutilize o access token durante sua validade documentada de 60 minutos; não gere um token a cada chamada. O endpoint de token possui rate limit próprio.

Leia `references/01-getting-started-auth.md` antes de implementar autenticação.

## Regras transversais

- Chamadas e callbacks multi-conta podem usar `x-conta-corrente`; preserve o header quando documentado para a operação.
- A criação de Pix Pagamento usa `x-id-idempotente`; não substitua silenciosamente por outro header.
- Rate limits são **específicos por operação**. Nunca descreva “o rate limit do Pix” ou “do Banking” como um único número global.
- Trate HTTP `429` com backoff limitado e redução da frequência; nunca tente contornar limites.
- Receptores de webhook devem seguir os requisitos atuais de HTTPS/TLS/certificado/allowlist em `references/07-webhooks.md`.
- Sandbox possui comportamento simulado e ciclo próprio de disponibilidade/certificado. Leia `references/08-sandbox-postman.md`.

## Roteamento por produto

- **Banking** → `references/02-banking.md`
- **Pix** → `references/03-pix.md`
- **Pix Automático** → `references/04-pix-automatico.md`
- **Cobrança / Boleto com Pix** → `references/05-cobranca-boleto-pix.md`
- **Fórum** → `references/06-forum.md`
- **Webhooks** → `references/07-webhooks.md`
- **Sandbox/Postman** → `references/08-sandbox-postman.md`
- **SDKs** → `references/09-sdks.md`
- **CNAB/VAN** → `references/10-cnab.md`
- **Crédito Empresas** → `references/11-credito-empresas.md`
- **Crédito Imobiliário** → `references/12-credito-imobiliario.md`
- **Erros/troubleshooting** → `references/13-errors-status-codes.md`
- **Migrações/histórico** → `references/14-changelog-migrations.md`
- **Cobertura/fontes** → `references/00-source-index.md` e `sources.json`

## Guardrails de migração

- Não use `/references/cobranca`: é uma rota legada quebrada no snapshot auditado.
- Cobrança Boleto com Pix **V3** é a linha atual; trate V2 como descontinuada e migre UUID/processamento assíncrono/webhooks conforme a referência atual.
- Um aviso histórico de 24/12/2025 bloqueou temporariamente novas integrações Pix/Banking; o changelog de 12/03/2026 registra a reativação para novas solicitações sujeitas à análise. Não repita a restrição antiga como estado atual.
- A referência atual de Cobrança e o changelog de 18/05/2026 divergem sobre a data exata de descontinuação da V2. Trate V2 como descontinuada e exponha a divergência de data apenas quando a cronologia importar.

## Saída esperada

Ao gerar código de integração:

- inclua configuração de certificado, reutilização de token, timeouts e tratamento explícito de erros;
- use placeholders para segredos;
- respeite content types, headers obrigatórios, scopes e rate limits documentados;
- separe Produção e Sandbox;
- não converta silenciosamente valores monetários, enums, identificadores ou datas;
- em callbacks, projete para entregas duplicadas e retries, com processamento idempotente na aplicação quando apropriado;
- se uma operação exigir análise/aprovação posterior, não trate uma resposta aceita pela API como prova de liquidação final.
