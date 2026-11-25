---
name: privacy-lgpd
description: LGPD aplicada a produto e sistemas Spring Boot — conceitos, princípios, bases legais, privacy by design, mapa de dados e RIPD, direitos do titular e como implementá-los, retenção e eliminação ponta a ponta, dados em logs/eventos/analytics, fornecedores, incidentes e checklist para o PRD (não é aconselhamento jurídico). Use quando uma funcionalidade tocar dado pessoal.
---

Antes de aplicar este pattern, leia também [`../prd-writing/SKILL.md`](../prd-writing/SKILL.md) (a seção de privacidade do PRD), [`../product-metrics/SKILL.md`](../product-metrics/SKILL.md) (analytics sem PII), [`../product-discovery/SKILL.md`](../product-discovery/SKILL.md) (pesquisa com pessoas) e, no lado técnico, [`../cqrs-event-sourcing/SKILL.md`](../cqrs-event-sourcing/SKILL.md) (eliminação e crypto-shredding), [`../aws-observability/SKILL.md`](../aws-observability/SKILL.md) (logs e retenção), [`../aws-s3-sqs/SKILL.md`](../aws-s3-sqs/SKILL.md), [`../aws-dynamodb/SKILL.md`](../aws-dynamodb/SKILL.md) (TTL) e [`../authentication/SKILL.md`](../authentication/SKILL.md).

> ### ⚠️ Esta skill **não é aconselhamento jurídico**
> Ela traduz os **princípios da LGPD** em **requisitos de produto e de engenharia**. **Decisões jurídicas** (qual base legal usar, o que é "legítimo interesse", prazos de retenção legais, conteúdo de termos, resposta a incidente, transferência internacional, contratos com fornecedores) **devem ser validadas com o jurídico e o encarregado/DPO**. Artigos, resoluções e prazos citados aqui podem ter sido **atualizados** — **confirme na lei, nos regulamentos da ANPD e com o jurídico** antes de agir.

# Privacidade e LGPD

A **LGPD** (Lei Geral de Proteção de Dados Pessoais — **Lei nº 13.709/2018**) regula o **tratamento de dados pessoais** no Brasil: qualquer operação com dado de **pessoa natural identificada ou identificável** (coletar, armazenar, consultar, compartilhar, analisar, eliminar). **Não** é só "um assunto do jurídico": **a arquitetura e as decisões de produto determinam se a empresa consegue cumprir a lei** (eliminar um dado "espalhado" por 6 serviços, backups e logs é um problema de **engenharia**). Por isso privacidade é **requisito de produto desde o início** (*privacy by design*), não um remendo no fim.

## 1. Conceitos essenciais

| Termo | Significado |
|---|---|
| **Dado pessoal** | Informação relacionada a pessoa natural **identificada ou identificável**: nome, CPF, e-mail, telefone, endereço, IP, ID de dispositivo, localização, **e-mail em log**, `userId` que leva à pessoa |
| **Dado pessoal sensível** | Origem racial/étnica, convicção religiosa, opinião política, filiação sindical/religiosa/filosófica/política, **saúde ou vida sexual**, **dado genético ou biométrico** vinculado a uma pessoa — **regime mais rigoroso** (hipóteses legais restritas) |
| **Dado anonimizado** | Não permite identificar a pessoa por **meios técnicos razoáveis** — **fora** da LGPD. **Pseudonimizado** (trocar nome por um código, mas a chave existe) **continua** sendo dado pessoal |
| **Titular** | A pessoa a quem os dados se referem |
| **Controlador** | Quem **decide** as finalidades e os meios do tratamento (geralmente a empresa dona do produto) |
| **Operador** | Quem trata dados **em nome** do controlador (fornecedor de nuvem, e-mail, analytics) |
| **Encarregado (DPO)** | Canal de comunicação entre controlador, titulares e a **ANPD**; orienta a empresa |
| **ANPD** | Autoridade Nacional de Proteção de Dados — regulamenta e **fiscaliza**; pode aplicar sanções |
| **Tratamento** | **Qualquer** operação com o dado, do coletar ao eliminar |

**Pegadinhas comuns:** **IP, cookie ID, device ID, e-mail e `userId`** **são** dado pessoal quando levam a uma pessoa; **dado "público" ou de login** também é protegido; **um dado inofensivo isolado** pode **identificar** quando cruzado com outros.

## 2. Princípios (Art. 6º) — o que guia as decisões

**Finalidade** (propósitos legítimos, específicos, informados) · **Adequação** (compatível com a finalidade) · **Necessidade** (**só o mínimo** necessário — *minimização*) · **Livre acesso** (o titular consulta seus dados) · **Qualidade dos dados** (exatos e atualizados) · **Transparência** (informação clara ao titular) · **Segurança** (medidas técnicas e administrativas) · **Prevenção** (evitar danos) · **Não discriminação** · **Responsabilização e prestação de contas** (**demonstrar** a conformidade).
Os três que mais impactam o produto: **finalidade** ("para que coletamos?" — sem finalidade, não colete), **necessidade/minimização** ("precisamos mesmo do CPF para isto?") e **segurança**.

## 3. Bases legais (Art. 7º) — todo tratamento precisa de **uma**

Não se trata dado pessoal "porque é útil"; é preciso uma **base legal** para **cada finalidade**:
| Base | Quando faz sentido | Observação |
|---|---|---|
| **Consentimento** | O titular escolhe livremente (marketing, cookies não essenciais, compartilhamento opcional) | Deve ser **livre, informado, inequívoco, para finalidade específica**, e **revogável** a qualquer momento, **tão fácil quanto dar**. Não vale "aceito tudo" genérico nem caixa pré-marcada |
| **Execução de contrato** | O dado é **necessário** para prestar o serviço contratado (endereço para entregar) | Só o necessário ao contrato |
| **Obrigação legal/regulatória** | A lei exige guardar/informar (notas fiscais, registros) | Define a **retenção** mínima |
| **Legítimo interesse** | Interesse legítimo do controlador **que não prevalece** sobre os direitos do titular (segurança, prevenção a fraude) | Exige **teste de balanceamento** documentado; **não** serve para tudo; **jurídico** valida |
| **Exercício regular de direitos**, **proteção da vida**, **tutela da saúde**, **proteção do crédito**, **estudos por órgão de pesquisa**, **políticas públicas** | Hipóteses específicas | Aplicáveis a casos particulares; **dados sensíveis** têm lista **própria e mais restrita** (Art. 11) |

**Para o PM:** a cada coleta, escreva **qual dado, para qual finalidade, com qual base legal** (isso vira o **mapa de dados**, seção 5). **Consentimento é a base mais frágil** (pode ser revogada) — use quando é a **escolha real** do usuário, **não** como "chave genérica". **Dados de crianças e adolescentes** (Art. 14) exigem **cuidado adicional** (melhor interesse, consentimento de responsável).

## 4. Privacy by design — o que o PM pede desde o PRD

Incorpore na **definição** do produto (`prd-writing`, seção 6 de NFRs), **não** no fim:
1. **Colete o mínimo.** Cada campo coletado precisa de **justificativa**. Se não há finalidade clara, **não colete** (o dado que não existe não vaza nem precisa ser protegido/eliminado).
2. **Finalidade e base legal por tratamento**, **registradas**.
3. **Retenção definida** (por quanto tempo e **o que acontece depois**: eliminar ou anonimizar), **desde o desenho** — não "guardamos para sempre".
4. **Segurança proporcional**: criptografia em trânsito (TLS) e em repouso (`aws-rds-secrets-manager`, KMS), **controle de acesso por menor privilégio** (`authentication`), **segregação** de dados sensíveis, **segredos fora do código**.
5. **Transparência**: aviso de privacidade **claro e acessível**, no momento da coleta (**o que, por quê, por quanto tempo, com quem compartilha, como exercer direitos**), sem juridiquês.
6. **Direitos do titular implementáveis** (seção 6) — o produto **precisa ter** como atender.
7. **Avalie o risco** (RIPD — seção 5) quando o tratamento for de **alto risco** (dados sensíveis, grande escala, perfilamento, decisões automatizadas, crianças).
8. **Fornecedores/operadores** avaliados e **contratados** com cláusulas de proteção de dados (seção 8).
9. **Anonimize/pseudonimize** sempre que a finalidade permitir (analytics, testes — **nunca use dados reais de produção em dev/teste** sem proteção).

## 5. Mapa de dados (ROPA) e RIPD

- **Mapa/inventário de tratamento** (Registro das Operações): para **cada** tratamento, **dado, titulares, finalidade, base legal, onde fica (sistemas, backups, logs, terceiros), quem acessa, retenção, compartilhamentos**. **Sem esse mapa não há como** atender um pedido de acesso/eliminação nem responder a um incidente. Mantenha-o **vivo** (atualize quando o produto muda); a LGPD exige que o controlador **mantenha registro** das operações.
```markdown
| Dado | Titulares | Finalidade | Base legal | Onde está | Acesso | Retenção | Compartilha com |
|---|---|---|---|---|---|---|---|
| E-mail do sócio | Sócios | Avisos de vencimento | Execução de contrato | RDS `members`; logs (mascarado); SES (operador) | Suporte, sistema | Enquanto sócio ativo + 5 anos (legal) | SES (AWS) |
```
- **RIPD** — **Relatório de Impacto à Proteção de Dados Pessoais** (Art. 38): documento que **descreve o tratamento de risco, os riscos aos titulares e as medidas de mitigação**. A **ANPD pode exigi-lo**; **boa prática**: faça-o para tratamentos de **alto risco** (sensíveis, larga escala, perfilamento, tecnologias novas). O **encarregado/jurídico** lidera; o **PM e a engenharia** fornecem os fatos.

## 6. Direitos do titular (Art. 18) — e como implementá-los

O titular pode **requerer** ao controlador (que deve responder **em prazo regulamentado** — confirme o prazo vigente com o jurídico/ANPD):
| Direito | O que o titular pede | O que o sistema precisa suportar |
|---|---|---|
| **Confirmação e acesso** | Saber **se** e **quais** dados tratamos | **Exportar todos os dados** da pessoa, de **todos os sistemas** (mapa de dados!) |
| **Correção** | Corrigir dado incompleto/errado/desatualizado | Atualização que **propaga** para cópias/projeções (`cqrs-event-sourcing`) |
| **Anonimização, bloqueio ou eliminação** de dados desnecessários/excessivos/tratados em desconformidade | Parar/limpar | **Fluxo de eliminação ponta a ponta** (abaixo) |
| **Portabilidade** | Receber os dados em **formato estruturado** para outro fornecedor | Export em **JSON/CSV** documentado |
| **Eliminação** dos dados tratados com **consentimento** | "Apague meus dados" | Idem, **ressalvadas** as hipóteses legais de **guarda obrigatória** |
| **Informação sobre compartilhamento** | Com quem compartilhamos | Mapa de dados atualizado |
| **Informação sobre a possibilidade de não consentir** e consequências | | Texto claro na coleta |
| **Revogação do consentimento** | Retirar a permissão | **Botão/fluxo fácil**; efeito **imediato** nos novos tratamentos |
| **Revisão de decisões automatizadas** | Pedir revisão de decisão tomada **só por algoritmo** que afete seus interesses | Possibilidade de **intervenção humana** e **explicação** |

**Implementar como produto, não como "ticket manual":** com volume, atendimento manual **não escala** e **erra**. Construa **um canal** (formulário/e-mail do encarregado), um **fluxo de verificação de identidade** (para **não entregar dados à pessoa errada** — um vazamento por engano), um **registro** dos pedidos e **prazos**, e **automação** da exportação/eliminação.

### Eliminação ponta a ponta — o problema de engenharia

Um dado pessoal raramente está em **um** lugar: **banco transacional, cópias/projeções (read models), cache, índices de busca, data lake/analytics, backups, logs, filas/mensagens retidas, arquivos no S3, e-mails já enviados, fornecedores**. A eliminação precisa cobrir (veja o mapa de dados):
- **Banco principal e réplicas**: apagar ou **anonimizar** (ex.: substituir identificadores, manter agregados). **Obrigações legais** (fiscal, contábil) podem exigir **reter** parte do dado — **bloqueie** o uso e elimine ao fim do prazo legal.
- **Propagação por eventos**: publique um **evento de eliminação** (`member_erased`) que **cada serviço** consome (**idempotente** — `idempotency`, `messaging`) para apagar **sua** cópia/projeção (`cqrs-event-sourcing`).
- **Event sourcing**: eventos são **imutáveis** — **não coloque PII nos eventos** (guarde por referência, apagável) **ou** use **crypto-shredding** (PII cifrada com chave **por titular**; "esquecer" = **destruir a chave**) — **decisão de projeto antes do primeiro evento**.
- **Logs e analytics**: **não registre PII** (mascare e-mail/CPF — `aws-observability`); **retenção curta**; analytics com **ID pseudonimizado** (`product-metrics`).
- **Backups**: não dá para "editar" um backup — defina **retenção de backup limitada** e registre que o dado **expira** com o ciclo de backup; o processo de **restauração** deve **reaplicar as eliminações** feitas depois do backup (lista de eliminação).
- **Mensageria**: mensagens têm **retenção**; evite PII no payload (envie **IDs**); Kafka com retenção/compaction conforme o caso (`kafka`).
- **S3/armazenamento**: **lifecycle** para expirar; objetos por titular **localizáveis** (prefixo por usuário) para eliminar (`aws-s3-sqs`). **DynamoDB**: **TTL** (`aws-dynamodb`).
- **Fornecedores (operadores)**: **solicite a eliminação** a eles e **tenha a rota contratual** para isso (seção 8).
- **Prove**: **registre** que a eliminação ocorreu (sem guardar o dado eliminado).

## 7. Dados em logs, analytics, eventos, testes e IA

| Onde | Risco | Prática |
|---|---|---|
| **Logs** (`observability`) | E-mail/CPF/token em log vira cópia espalhada e **retida** por meses | **Nunca logar** PII/credenciais; **mascarar** (`j***@x.com`); retenção **curta**; *data protection policies* do CloudWatch (`aws-observability`) |
| **Analytics / eventos de produto** (`product-metrics`) | Rastreamento excessivo/sem consentimento | **ID pseudonimizado**, **sem PII** nas propriedades, **consentimento** para cookies/rastreamento não essencial, **retenção** definida |
| **Mensagens/eventos** (`messaging`) | PII em payload retido e replicado | **IDs** no evento, PII só buscada onde precisa; criptografia em repouso |
| **Ambientes de teste/dev** | Dados reais de produção copiados | **Dados sintéticos/anonimizados**; **nunca** dump de produção sem mascaramento |
| **Pesquisa com usuários** (`product-discovery`) | Gravações/notas identificáveis | **Consentimento**, anonimizar, apagar conforme prometido |
| **IA/ML e terceiros de análise** | Enviar dados pessoais a provedor externo | Base legal, contrato com **operador**, **minimização** (não enviar o que não precisa), verificar **retenção/treinamento** do provedor |
| **Cookies e SDKs** (web/mobile) | Rastreadores de terceiros sem consentimento | Banner de consentimento com **categorias**, **recusar tão fácil quanto aceitar**; só **essenciais** sem consentimento |

## 8. Fornecedores, nuvem e transferência internacional

- **Operadores**: todo fornecedor que trata dados em seu nome (AWS, provedor de e-mail, analytics, suporte) é **operador**: exija **contrato** com **cláusulas de proteção de dados** (finalidade, segurança, subcontratados, eliminação, notificação de incidente), e **avalie** a segurança deles. O controlador **continua responsável** perante o titular.
- **Transferência internacional** (Art. 33): enviar dados para **fora do Brasil** (inclusive **região de nuvem no exterior**, SaaS estrangeiro) **só** em **hipóteses previstas** (país com nível adequado, **cláusulas contratuais**, consentimento específico, etc.). **Antes de escolher a região da nuvem** (`aws-terraform`, `aws-eks`) ou um SaaS, **valide com o jurídico** — a escolha de **região** é decisão de privacidade, não só de latência/custo. **Mantenha dados de brasileiros na região adequada** quando a análise jurídica exigir.
- **Subprocessadores**: peça a **lista** e **notificação de mudança**.
- **Segurança da cadeia**: o incidente no fornecedor é **seu** incidente perante o titular.

## 9. Incidentes de segurança com dados pessoais

Um **incidente** (vazamento, acesso indevido, perda, ransomware) que possa gerar **risco ou dano relevante** aos titulares **obriga o controlador a comunicar a ANPD e os titulares** (Art. 48), **em prazo razoável** — **a ANPD regulamentou prazos específicos** (a regulamentação de comunicação de incidente prevê prazo curto, na ordem de **poucos dias úteis**; **confirme o regulamento vigente e o prazo exato com o jurídico/DPO** — não confie em memória).
**Prepare-se antes (plano de resposta):**
1. **Detecção** (`observability`, alertas de acesso anômalo) e **canal de reporte** interno claro.
2. **Quem aciona quem**: **segurança, engenharia, jurídico/DPO, comunicação** — contatos e **papéis** definidos (**não** descobrir no meio do incidente).
3. **Contenção, avaliação do que/quem foi afetado** (**o mapa de dados e os logs de auditoria** respondem a isso — por isso existem).
4. **Decisão de comunicação** (ANPD/titulares) **pelo jurídico/DPO**, com conteúdo exigido (natureza dos dados, titulares, medidas, riscos, o que fazer).
5. **Registro do incidente** e **post-mortem** com ações (`stakeholder-communication`, `technical-product-management`).
**Para o PM:** em incidente com dado pessoal, **acione o jurídico/DPO imediatamente**, **não** improvise o comunicado, **não minimize**, e **comunique ao suporte** o que dizer.

## 10. Checklist de privacidade para o PRD (cole no `prd-writing`)

```markdown
## Privacidade e proteção de dados (LGPD)
- [ ] Dados pessoais envolvidos (lista) e **se há dado sensível/de crianças**: ______
- [ ] **Finalidade** de cada dado: ______   **Base legal** (validada com jurídico/DPO): ______
- [ ] **Minimização**: cada campo é necessário? O que cortamos? ______
- [ ] **Retenção** e o que acontece ao fim (eliminar/anonimizar): ______
- [ ] **Aviso/transparência** ao titular na coleta (texto e local): ______
- [ ] **Consentimento** (se for a base): como coletar, **revogar** e registrar: ______
- [ ] **Direitos do titular**: como acessar/corrigir/eliminar/exportar (fluxo e prazo): ______
- [ ] **Segurança**: criptografia, controle de acesso, auditoria; **sem PII em logs/eventos/analytics**: ______
- [ ] **Compartilhamento e fornecedores** (operadores, contrato), **transferência internacional**/região: ______
- [ ] **Mapa de dados atualizado**; **RIPD** necessário? (alto risco): ______
- [ ] **Eliminação ponta a ponta** (todos os sistemas, eventos, backups, fornecedores) desenhada: ______
- [ ] Revisão **jurídico/DPO** concluída em: ______ (antes de congelar o escopo)
```

## 11. O que o PM entrega à engenharia (requisitos concretos)

Traduza princípios em **requisitos testáveis** (`prd-writing`, `user-stories`):
- **"O cadastro não coleta CPF"** (minimização) · **"O e-mail é mascarado em todo log"** · **"Os eventos publicados contêm `memberId`, não e-mail/nome"** · **"Existe um endpoint/rotina para exportar e eliminar os dados de um titular em todos os serviços, concluindo em ≤ X dias"** · **"Logs expiram em 30 dias; backups em 35"** · **"O consentimento de marketing é registrado (quando, versão do texto, finalidade) e revogável com um clique"** · **"O ambiente de teste usa dados sintéticos"** · **"A região de armazenamento é `sa-east-1`"** (se a análise jurídica exigir).
O `qa` verifica (`testing`): **nenhum PII em log/evento**, **fluxo de eliminação realmente apaga em todos os destinos**, **consentimento revogado para de tratar**, **exportação completa**. O `code-reviewer` procura **PII em log/evento/URL** e **dado pessoal sem finalidade**.

## 12. Anti-patterns

- **Coletar "por via das dúvidas"** (sem finalidade) e **guardar para sempre**.
- **Consentimento genérico/pré-marcado** ou como base para tudo; **revogação difícil**.
- **PII em logs, URLs, eventos, analytics e mensagens**; **dados reais de produção em dev/teste**.
- **Sem mapa de dados** (não se sabe onde o dado está → não se elimina nem se responde incidente).
- **Atender direitos do titular "no braço"**, sem verificar identidade (vazar para a pessoa errada) ou sem prazo.
- **Eliminar só do banco principal** (esquecer cache, índices, analytics, backups, logs, fornecedores).
- **Event sourcing com PII nos eventos** sem estratégia de esquecimento.
- **Escolher região/fornecedor** sem considerar transferência internacional.
- **Tratar LGPD como "tarefa do jurídico no fim do projeto"**; **improvisar a resposta a incidente**.
- **Tratar pseudonimização como anonimização.**
- **Dar aconselhamento jurídico próprio** em vez de validar com jurídico/DPO.

---

## Regras principais

- **Não é aconselhamento jurídico**: decisões de base legal, retenção, termos, incidente e transferência internacional **vão ao jurídico/DPO**; **confirme** artigos, regulamentos da ANPD e prazos vigentes.
- **Privacy by design desde o PRD**: **coletar o mínimo**, **finalidade + base legal registradas por tratamento**, **retenção definida**, segurança proporcional, transparência, **direitos do titular implementáveis**.
- **Dado pessoal é amplo** (IP, e-mail, `userId`, device ID); **pseudonimizado ainda é pessoal**; **dado sensível** e **de crianças** têm regime reforçado.
- **Consentimento** só quando é escolha real (livre, informado, específico, **revogável com facilidade**); preferir **outras bases** quando cabem; **legítimo interesse** exige teste e validação jurídica.
- **Mapa de dados (ROPA) vivo** e **RIPD** para alto risco; sem mapa, não há como eliminar nem responder a incidentes.
- **Direitos do titular como funcionalidade**: acesso/exportação, correção, eliminação, portabilidade, revogação — com **verificação de identidade**, registro e prazos.
- **Eliminação ponta a ponta**: banco, projeções, cache, índices, analytics, **backups** (retenção limitada + reaplicar eliminações), logs, mensageria, S3/DynamoDB TTL, **fornecedores**; **event sourcing sem PII ou com crypto-shredding**.
- **Sem PII em logs, eventos, URLs e analytics** (IDs pseudonimizados, máscara); **dados sintéticos em dev/teste**; **IA/terceiros** só com base legal, contrato e minimização.
- **Operadores com contrato**; **região da nuvem/SaaS é decisão de privacidade** (transferência internacional) — valide **antes**.
- **Incidente com dado pessoal**: plano **pré-definido**, **jurídico/DPO imediatamente**, comunicação a ANPD/titulares conforme a regulamentação vigente; **não improvise nem minimize**.
- **Cole o checklist de privacidade no PRD**; transforme em **requisitos testáveis** (QA verifica).
- **Sem Lombok** — deliberado (skill de produto, sem código).
