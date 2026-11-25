---
name: validacao-real-sem-mock
description: Como validar de verdade, sem mock, o que pode ser executado localmente — inclusive integrações com LLM e APIs pagas sem gastar chave, browser real, contrato de stream, e o que fazer quando ao vivo é genuinamente impossível. Carregar antes de escrever teste para integração externa, antes de qualquer tentação de mockar HTTP/LLM, e antes de declarar "validado" algo que só foi lido.
---

# Validação real, sem mock

Regra do método: **nunca mocke o que pode ser executado de verdade.** Mock de HTTP testa o mock. Cada técnica abaixo pegou bug real no projeto de origem.

## Técnicas

1. **Servidor local que fala o mesmo formato.** Um runtime local de modelos com endpoint compatível valida o cliente de ponta a ponta (streaming incluído) sem chave paga. Atenção: camada de compatibilidade pode ignorar campos em silêncio — teste de formato ≠ teste de obediência do modelo.
2. **Chave inválida de propósito.** Contra a API de produção, a resposta de erro prova URL, headers e parsing (`401 invalid_api_key`, `400 API_KEY_INVALID` — cada provedor responde diferente; um `403` pode ser conta sem crédito, não chave errada).
3. **Contador de ingestão como sinal.** Para saber se o modelo RECEBEU um dado (imagem, áudio, contexto), compare a contagem de tokens de entrada com um baseline só-texto. Campo aceito sem erro e contagem idêntica = ignorado. Capacidade declarada ≠ canal exposto.
4. **Capacidade pelo que o runtime declara, nunca pelo nome.** Dois modelos da mesma família, um com visão e outro sem. Heurística por nome oferece recurso que falha.
5. **Fixture propositalmente quebrada.** Rode a ferramenta real contra o defeito plantado e confira o achado esperado. Caso de origem: o formato de relatório de uma ferramenta era de versão diferente da documentada — só rodando de verdade.
6. **Browser real.** "Não dá para rodar Playwright aqui" costuma ser uma variável de ambiente (plataforma do browser) — meça antes de declarar limite. Componente visual, WebGL, loop assíncrono e exceção sem `catch` não aparecem em jsdom.
7. **Router/serviço real em processo.** Monte a aplicação de produção com estado mínimo real (banco em memória) e dispare requisições contra ela — nunca uma reconstrução do handler.
8. **App empacotado, não só o frontend.** O WebView do app pode divergir do browser de teste; valide o artefato que o usuário instala quando o comportamento depende dele, conferindo antes que o binário em execução é o da release.

## Stream "funciona mas não faz nada"

Status 2xx, sem erro, e o consumidor não recebe nada: suspeite de falta de buffer entre chunks (fronteira TCP ≠ fronteira de linha SSE/NDJSON). Só aparece com payload grande — "testei texto curto" não cobre tool-calling do mesmo provedor. Stream pode terminar limpo e vazio ao mesmo tempo.

## Modelo "ignora" sem erro

Modelo pequeno pode receber contexto/tools corretos e responder errado. Antes de declarar bug de retrieval ou de streaming, reproduza isolado (payload mínimo, sem tools extras) — só então investigue o encanamento.

## Quando ao vivo é genuinamente impossível

Cobertura de tradução pura (montagem de payload + parsing de eventos), com cada teste travando uma diferença real de formato que causaria erro — e registro honesto, no PR e no registro de pendências, do que não foi validado ao vivo, com o motivo exato.

## Anti-padrões

- Testar a obediência do MODELO num teste do PROVIDER (flaky por natureza).
- Conferir estado com uma ferramenta de banco enquanto o serviço está vivo (pode corromper).
- Declarar "validado" com base em código lido, não executado. Distinga sempre "verificado ao vivo" de "escrito a partir da documentação".
