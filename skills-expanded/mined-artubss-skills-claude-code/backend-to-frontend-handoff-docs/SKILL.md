# API Handoff Mode

Entendi. Sou um desenvolvedor backend completando trabalho de API. Minha tarefa é produzir um documento estruturado de handoff que fornece aos desenvolvedores frontend (ou sua IA) contexto completo de negócio e técnico para construir integração/UI sem precisar fazer perguntas.

## Quando usar
Após completar trabalho de API backend—endpoints, DTOs, validação, lógica de negócio—execute este modo para gerar documentação de handoff.

## Objetivo
Produzir um documento pronto para copiar e colar com todo o contexto que uma IA frontend precisa para construir UI/integração corretamente e com confiança.

## Entradas
- Código de API completo (endpoints, controllers, services, DTOs, validação).
- Contexto de negócio relacionado da task/user story.
- Qualquer constraint, caso extremo ou armadilha descoberta durante implementação.

## Fluxo de Trabalho

1. **Coletar contexto** — confirme nome da feature, endpoints relevantes, DTOs, regras de auth, e casos extremos.
2. **Criar/atualizar arquivo de handoff** — escreva o documento em `.claude/docs/ai/<feature-name>/api-handoff.md`. Incremente o sufixo de iteração (`-v2`, `-v3`, …) se re-executar após feedback.
3. **Colar template** — preencha cada seção abaixo com dados concretos. Omita subseções apenas quando realmente não aplicável (anote por quê).
4. **Double-check** — garanta que payloads correspondem ao comportamento real da API, escopos de auth são precisos, e enums/validação refletem lógica backend.

## Formato de Saída

Produza um único bloco markdown estruturado como segue. Mantenha denso—sem fluff, sem repetição.

```markdown
# API Handoff: [Nome da Feature]

## Contexto de Negócio
[2-4 frases: Que problema resolve? Quem usa? Por que importa? Inclua qualquer termo de domínio que frontend precisa entender.]

## Endpoints

### [METHOD] /path/to/endpoint
- **Propósito**: [1 linha: o que faz]
- **Auth**: [role/permission obrigatório, ou "public"]
- **Request**:
  ```json
  {
    "field": "type — descrição, constraints"
  }
  ```
- **Response** (sucesso):
  ```json
  {
    "field": "type — descrição"
  }
  ```
- **Response** (erro): [Códigos HTTP e formas, ex: 422 validação, 404 não encontrado]
- **Notas**: [casos extremos, rate limits, paginação, ordenação, qualquer coisa não óbvia]

[Repita para cada endpoint]

## Modelos de Dados / DTOs
[Liste key models/DTOs que frontend receberá ou enviará. Inclua tipos de campo, nullability, enums, e significado de negócio.]

```typescript
// Exemplo de shape para typing frontend
interface ExampleDto {
  id: number;
  status: 'pending' | 'approved' | 'rejected';
  createdAt: string; // ISO 8601
}
```

## Enums & Constantes
[Liste qualquer enum, códigos de status, ou magic values que frontend precisa saber. Inclua rótulos de exibição se relevante.]

| Valor | Significado | Rótulo de Exibição |
|-------|-------------|-------------------|
| `pending` | Aguardando revisão | Pendente |

## Regras de Validação
[Resuma key validation rules que frontend deve espelhar para UX—campos obrigatórios, min/max, formatos, regras condicionais.]

## Lógica de Negócio & Casos Extremos
- [Bullet cada comportamento não óbvio, constraint, ou armadilha]
- [ex: "Usuário pode submeter apenas uma vez por dia", "Itens soft-deleted excluídos por padrão"]

## Notas de Integração
- **Fluxo recomendado**: [ex: "Buscar lista → selecionar item → submeter form → fazer polling para status"]
- **UI Otimista**: [segura ou não, por quê]
- **Caching**: [qualquer header de cache, triggers de invalidação]
- **Real-time**: [eventos websocket, intervalos de polling se aplicável]

## Cenários de Teste
[Key scenarios que frontend deve tratar—happy path, erros, casos extremos. Use como acceptance criteria ou test cases.]

1. **Happy path**: [breve descrição]
2. **Erro de validação**: [o que dispara, resposta esperada]
3. **Não encontrado**: [quando 404 é retornado]
4. **Permissão negada**: [quando 403 é retornado]

## Perguntas Abertas / TODOs
[Qualquer coisa não resolvida, pendendo decisão PM, ou precisa input frontend. Se nenhuma, omita seção.]
```

## Regras
- **SEM OUTPUT DE CHAT**—produza apenas o bloco markdown de handoff, nada mais.
- Seja preciso: tipos, constraints, exemplos—não prosa vaga.
- Inclua payloads de exemplo reais onde útil.
- Destaque comportamentos não óbvios—não assuma que frontend "simplesmente saberá."
- Se backend fez trade-offs ou assumptions, documente-os.
- Mantenha escaneável: headers, tabelas, bullets, code blocks.
- Nenhum detalhe de implementação backend (nenhum path de arquivo, nome de classe, serviços internos) a menos que diretamente relevante para integração.
- Se algo está incompleto ou TBD, diga explicitamente.

## Após Gerar
Escreva o markdown final apenas no arquivo de handoff—não ecoar em chat. (Se a plataforma requer confirmação, referencie o path do arquivo em vez de colar conteúdo.)