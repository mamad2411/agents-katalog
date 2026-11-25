---
name: Burp Suite Web Application Testing
description: Esta habilidade deve ser usada quando o usuário pede para "interceptar tráfego HTTP", "modificar requisições web", "usar Burp Suite para testes", "realizar varredura de vulnerabilidades web", "testar com Burp Repeater", "analisar histórico HTTP" ou "configurar proxy para testes web". Fornece orientação abrangente para usar os principais recursos do Burp Suite em testes de segurança de aplicações web.
metadata:
  author: zebbern
  version: "1.1"
---

# Burp Suite Web Application Testing

## Propósito

Executar testes abrangentes de segurança de aplicações web usando o conjunto de ferramentas integrado do Burp Suite, incluindo interceptação e modificação de tráfego HTTP, análise e repetição de requisições, varredura automatizada de vulnerabilidades e fluxos de trabalho de testes manuais. Esta habilidade permite a descoberta e exploração sistemática de vulnerabilidades de aplicações web por meio de metodologia de testes baseada em proxy.

## Inputs / Pré-requisitos

### Ferramentas Necessárias
- Burp Suite Community ou Professional Edition instalado
- Navegador integrado do Burp ou navegador externo configurado
- URL da aplicação web alvo
- Credenciais válidas para testes autenticados (se aplicável)

### Configuração do Ambiente
- Burp Suite iniciado com projeto temporário ou nomeado
- Listener de proxy ativo em 127.0.0.1:8080 (padrão)
- Navegador configurado para usar proxy do Burp (ou use navegador do Burp)
- Certificado CA instalado para interceptação HTTPS

### Comparação de Edições
| Recurso | Community | Professional |
|---------|-----------|--------------|
| Proxy | ✓ | ✓ |
| Repeater | ✓ | ✓ |
| Intruder | Limitado | Completo |
| Scanner | ✗ | ✓ |
| Extensions | ✓ | ✓ |

## Outputs / Entregas

### Saídas Primárias
- Requisições/respostas HTTP interceptadas e modificadas
- Relatórios de varredura de vulnerabilidades com conselhos de remediação
- Documentação de histórico HTTP e mapa do site
- Provas de conceito de exploits para vulnerabilidades identificadas

## Fluxo de Trabalho Principal

### Fase 1: Interceptando Tráfego HTTP

#### Iniciar Navegador do Burp
Navegue para navegador integrado para integração perfeita com proxy:

1. Abra Burp Suite e crie/abra projeto
2. Vá para aba **Proxy > Intercept**
3. Clique em **Open Browser** para iniciar navegador pré-configurado
4. Posicione as janelas para visualizar Burp e navegador simultaneamente

#### Configurar Interceptação
Controle quais requisições são capturadas:

```
Proxy > Intercept > Toggle Intercept is on/off

When ON: Requisições pausam para revisão/modificação
When OFF: Requisições passam, registradas no histórico
```

#### Interceptar e Encaminhar Requisições
Processe tráfego interceptado:

1. Defina o toggle de interceptação para **Intercept on**
2. Navegue até a URL alvo no navegador
3. Observe a requisição mantida na aba Proxy > Intercept
4. Revise o conteúdo da requisição (headers, parâmetros, body)
5. Clique em **Forward** para enviar requisição ao servidor
6. Continue encaminhando requisições subsequentes até página carregar

#### Ver Histórico HTTP
Acesse log completo de tráfego:

1. Vá para aba **Proxy > HTTP history**
2. Clique em qualquer entrada para visualizar requisição/resposta completa
3. Ordene clicando nos cabeçalhos de colunas (# para ordem cronológica)
4. Use filtros para focar em tráfego relevante

### Fase 2: Modificando Requisições

#### Interceptar e Modificar
Altere parâmetros de requisição antes de encaminhar:

1. Ative interceptação: **Intercept on**
2. Dispare requisição alvo no navegador
3. Localize parâmetro a modificar na requisição interceptada
4. Edite valor diretamente no editor de requisição
5. Clique em **Forward** para enviar requisição modificada

#### Alvo Comum de Modificações
| Alvo | Exemplo | Propósito |
|-----|---------|----------|
| Parâmetros de preço | `price=1` | Testar lógica de negócio |
| IDs de usuário | `userId=admin` | Testar controle de acesso |
| Valores de quantidade | `qty=-1` | Testar validação de entrada |
| Campos ocultos | `isAdmin=true` | Testar escalação de privilégio |

#### Exemplo: Manipulação de Preço

```http
POST /cart HTTP/1.1
Host: target.com
Content-Type: application/x-www-form-urlencoded

productId=1&quantity=1&price=100

# Modificar para:
productId=1&quantity=1&price=1
```

Resultado: Item adicionado ao carrinho ao preço modificado.

### Fase 3: Definindo Escopo de Alvo

#### Definir Escopo
Focalize testes em alvo específico:

1. Vá para **Target > Site map**
2. Clique com botão direito no host alvo no painel esquerdo
3. Selecione **Add to scope**
4. Quando solicitado, clique em **Yes** para excluir tráfego fora de escopo

#### Filtrar por Escopo
Remova ruído do histórico HTTP:

1. Clique no filtro de exibição acima do histórico HTTP
2. Selecione **Show only in-scope items**
3. Histórico agora mostra apenas tráfego do site alvo

#### Benefícios do Escopo
- Reduz confusão de requisições de terceiros
- Previne testes acidentais de sites fora de escopo
- Melhora eficiência de varredura
- Cria relatórios mais limpos

### Fase 4: Usando Burp Repeater

#### Enviar Requisição para Repeater
Prepare requisição para testes manuais:

1. Identifique requisição interessante no histórico HTTP
2. Clique com botão direito em requisição e selecione **Send to Repeater**
3. Vá para aba **Repeater** para acessar requisição

#### Modificar e Reenviar
Teste diferentes entradas com eficiência:

```
1. Visualize requisição na aba Repeater
2. Modifique valores de parâmetros
3. Clique em Send para enviar requisição
4. Revise resposta no painel direito
5. Use setas de navegação para revisar histórico de requisições
```

#### Fluxo de Trabalho de Testes com Repeater

```
Requisição Original:
GET /product?productId=1 HTTP/1.1

Teste 1: productId=2    → Resposta de produto válido
Teste 2: productId=999  → Resposta Not Found  
Teste 3: productId='    → Resposta de erro/exceção
Teste 4: productId=1 OR 1=1 → Teste de SQL injection
```

#### Analisar Respostas
Procure por indicadores de vulnerabilidades:

- Mensagens de erro revelando stack traces
- Informações de versão/framework divulgadas
- Diferentes comprimentos de resposta indicando falhas lógicas
- Diferenças de tempo sugerindo injeção cega
- Dados inesperados em respostas

### Fase 5: Executando Varreduras Automatizadas

#### Iniciar Nova Varredura
Inicie varredura de vulnerabilidades (apenas Professional):

1. Vá para aba **Dashboard**
2. Clique em **New scan**
3. Digite URL alvo em **URLs to scan**
4. Configure opções de varredura

#### Opções de Configuração de Varredura

| Modo | Descrição | Duração |
|------|-----------|---------|
| Lightweight | Visão geral de alto nível | ~15 minutos |
| Fast | Verificação rápida de vulnerabilidades | ~30 minutos |
| Balanced | Varredura abrangente padrão | ~1-2 horas |
| Deep | Testes minuciosos | Várias horas |

#### Monitorar Progresso da Varredura
Acompanhe atividade de varredura:

1. Visualize status da tarefa em **Dashboard**
2. Observe **Target > Site map** atualizar em tempo real
3. Verifique aba **Issues** para vulnerabilidades descobertas

#### Revisar Problemas Identificados
Analise descobertas da varredura:

1. Selecione tarefa de varredura em Dashboard
2. Vá para aba **Issues**
3. Clique em problema para visualizar:
   - **Advisory**: Descrição e remediação
   - **Request**: Requisição HTTP disparadora
   - **Response**: Resposta do servidor mostrando vulnerabilidade

### Fase 6: Ataques Intruder

#### Configurar Intruder
Configure ataque automatizado:

1. Envie requisição para Intruder (clique direito > Send to Intruder)
2. Vá para aba **Intruder**
3. Defina posições de payload usando marcadores §
4. Selecione tipo de ataque

#### Tipos de Ataque

| Tipo | Descrição | Caso de Uso |
|------|-----------|------------|
| Sniper | Posição única, iterar payloads | Fuzzing de um parâmetro |
| Battering ram | Mesmo payload em todas posições | Testes de credenciais |
| Pitchfork | Iteração paralela de payloads | Pares usuário:senha |
| Cluster bomb | Todas combinações de payload | Força bruta completa |

#### Configurar Payloads

```
Positions Tab:
POST /login HTTP/1.1
...
username=§admin§&password=§password§

Payloads Tab:
Set 1: admin, user, test, guest
Set 2: password, 123456, admin, letmein
```

#### Analisar Resultados
Revise saída do ataque:

- Ordene por comprimento de resposta para encontrar anomalias
- Filtre por código de status para tentativas bem-sucedidas
- Use grep para buscar strings específicas
- Exporte resultados para documentação

## Referência Rápida

### Atalhos de Teclado
| Ação | Windows/Linux | macOS |
|------|---------------|-------|
| Encaminhar requisição | Ctrl+F | Cmd+F |
| Descartar requisição | Ctrl+D | Cmd+D |
| Enviar para Repeater | Ctrl+R | Cmd+R |
| Enviar para Intruder | Ctrl+I | Cmd+I |
| Toggle de interceptação | Ctrl+T | Cmd+T |

### Payloads Comuns de Teste

```
# SQL Injection
' OR '1'='1
' OR '1'='1'--
1 UNION SELECT NULL--

# XSS
<script>alert(1)</script>
"><img src=x onerror=alert(1)>
javascript:alert(1)

# Path Traversal
../../../etc/passwd
..\..\..\..\windows\win.ini

# Command Injection
; ls -la
| cat /etc/passwd
`whoami`
```

### Dicas de Modificação de Requisição
- Clique direito para opções de menu de contexto
- Use decoder para codificar/decodificar
- Compare requisições usando ferramenta Comparer
- Salve requisições interessantes no projeto

## Restrições e Salvaguardas

### Limites Operacionais
- Teste apenas aplicações autorizadas
- Configure escopo para prevenir testes acidentais fora de escopo
- Limite taxa de varreduras para evitar negação de serviço
- Documente todos os achados e ações

### Limitações Técnicas
- Community Edition não possui scanner automatizado
- Alguns sites podem bloquear tráfego de proxy
- HSTS/certificate pinning podem exigir configuração adicional
- Varreduras pesadas podem disparar blocos de WAF

### Melhores Práticas
- Sempre defina escopo de alvo antes de testes extensivos
- Use navegador do Burp para interceptação confiável
- Salve projeto regularmente para preservar trabalho
- Revise resultados de varredura manualmente para falsos positivos

## Exemplos

### Exemplo 1: Testes de Lógica de Negócio

**Cenário**: Manipulação de preço em e-commerce

1. Adicione item ao carrinho normalmente, intercepte requisição
2. Identifique parâmetro `price=9999` no corpo POST
3. Modifique para `price=1`
4. Encaminhe requisição
5. Complete checkout ao preço manipulado

**Achado**: Servidor confia em valores de preço fornecidos pelo cliente.

### Exemplo 2: Bypass de Autenticação

**Cenário**: Testando formulário de login

1. Envie credenciais válidas, capture requisição em Repeater
2. Envie para Repeater para testes
3. Tente: `username=admin' OR '1'='1'--`
4. Observe resposta de login bem-sucedida

**Achado**: SQL injection na autenticação.

### Exemplo 3: Divulgação de Informações

**Cenário**: Coleta de informações baseada em erros

1. Navegue para página de produto, observe parâmetro `productId`
2. Envie requisição para Repeater
3. Mude `productId=1` para `productId=test`
4. Observe erro detalhado revelando versão de framework

**Achado**: Apache Struts 2.5.12 divulgado em stack trace.

## Troubleshooting

### Navegador Não Conectando Através de Proxy
- Verifique se listener de proxy está ativo (Proxy > Options)
- Confira configurações de proxy do navegador apontam para 127.0.0.1:8080
- Garanta que nenhum firewall bloqueia conexões locais
- Use navegador integrado do Burp para configuração confiável

### Interceptação HTTPS Falhando
- Instale certificado CA do Burp em navegador/sistema
- Navegue para http://burp para baixar certificado
- Adicione certificado a raízes confiáveis
- Reinicie navegador após instalação

### Performance Lenta
- Limite escopo para reduzir processamento
- Desative extensões desnecessárias
- Aumente tamanho de heap Java em opções de inicialização
- Feche abas e recursos do Burp não utilizados

### Requisições Não Sendo Interceptadas
- Verifique se "Intercept on" está ativado
- Verifique se regras de interceptação não filtram alvo
- Garanta que navegador está usando proxy do Burp
- Verifique se alvo não está usando protocolo não suportado