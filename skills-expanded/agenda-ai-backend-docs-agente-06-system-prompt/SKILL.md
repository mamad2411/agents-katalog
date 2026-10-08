# 06 — System prompt

## Localização do template

O conteúdo completo do system prompt foi definido anteriormente e deve ser armazenado em:

```
app/modules/agent/prompts/system_prompt.md
```

Esse arquivo é o template base. A função `build_system_prompt` injeta variáveis do `AgentContext` antes de enviar ao LLM.

## Implementação

`app/modules/agent/prompts.py`:

```python
from pathlib import Path
from functools import lru_cache
from app.modules.agent.context import AgentContext

TEMPLATE_PATH = Path(__file__).parent / "prompts" / "system_prompt.md"

@lru_cache(maxsize=1)
def _load_template() -> str:
    return TEMPLATE_PATH.read_text(encoding="utf-8")

def build_system_prompt(context: AgentContext) -> str:
    template = _load_template()
    return template.format(
        establishment_name=context.establishment_name,
        establishment_type=context.establishment_type,
        establishment_city=context.establishment_city,
        client_first_name=context.client_first_name,
        agent_name="assistente",  # fixo por enquanto
    )
```

## Variáveis injetadas

Confirmar que o template usa exatamente estas variáveis:

| Placeholder | Origem |
|---|---|
| `{establishment_name}` | `context.establishment_name` |
| `{establishment_type}` | `context.establishment_type` |
| `{establishment_city}` | `context.establishment_city` |
| `{client_first_name}` | `context.client_first_name` |
| `{agent_name}` | constante (futuramente pode vir do estabelecimento) |

## Ajustes necessários no template gerado anteriormente

O template original mencionava `{client_id}` e `{establishment_id}` como variáveis a injetar. **Remover essas referências do template** — esses valores não devem estar no system prompt, já que o LLM não precisa saber esses IDs e eles vêm via token de sessão.

Outros ajustes:

- Remover referência a tools que não foram implementadas (ex: `confirmar_agendamento` foi descartada como tool por ser intent reativa)
- Adicionar regra explícita: "Você nunca precisa pedir ou informar IDs do sistema ao cliente"
- Adicionar regra de tooling: "Use as tools sem mencioná-las pelo nome ao cliente"

## Versionamento

O template é parte do código fonte. Mudanças no comportamento do agente passam por commit no repositório — auditável e reversível.

Se no futuro cada estabelecimento puder customizar o prompt (ex: personalidade personalizada), considerar mover para uma tabela `establishment_agent_settings` com colunas como `custom_tone`, `custom_greeting`, etc. — mas mantendo a estrutura base no template versionado.

## Custo de tokens

O system prompt completo (~2000 tokens) é enviado a cada chamada à OpenAI. Para GPT-5-nano isso é aceitável; se migrar para modelos maiores, considerar:

- Cache de prompt (recurso da OpenAI quando disponível)
- Versão enxuta do prompt para mensagens curtas
