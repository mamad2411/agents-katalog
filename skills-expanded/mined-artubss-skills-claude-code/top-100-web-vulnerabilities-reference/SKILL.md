---
name: Top 100 Web Vulnerabilities Reference
description: Esta habilidade deve ser usada quando o usuário pedir para "identificar vulnerabilidades de aplicações web", "explicar falhas de segurança comuns", "entender categorias de vulnerabilidades", "aprender sobre ataques de injeção", "revisar fraquezas de controle de acesso", "analisar problemas de segurança de API", "avaliar configurações incorretas de segurança", "entender vulnerabilidades do lado do cliente", "examinar falhas de segurança de mobile e IoT", ou "referenciar a taxonomia de vulnerabilidades alinhada ao OWASP". Use esta habilidade para fornecer definições abrangentes de vulnerabilidades, causas raiz, impactos e estratégias de mitigação em todas as principais categorias de segurança web.
metadata:
  author: zebbern
  version: "1.1"
---

# Top 100 Web Vulnerabilities Reference

## Objetivo

Fornecer uma referência abrangente e estruturada para as 100 vulnerabilidades mais críticas de aplicações web organizadas por categoria. Esta habilidade permite identificação sistemática de vulnerabilidades, avaliação de impacto e orientação de remediação em todo o espectro de ameaças de segurança web. Conteúdo organizado em 15 categorias principais de vulnerabilidades alinhadas aos padrões da indústria e padrões de ataque do mundo real.

## Pré-requisitos

- Compreensão básica de arquitetura de aplicações web (modelo cliente-servidor, protocolo HTTP)
- Familiaridade com tecnologias web comuns (HTML, JavaScript, SQL, XML, APIs)
- Entendimento de conceitos de autenticação e autorização
- Acesso a ferramentas de teste de segurança de aplicações web (Burp Suite, OWASP ZAP)
- Conhecimento de princípios de codificação segura recomendado

## Saídas e Entregáveis

- Catálogo completo de vulnerabilidades com definições, causas raiz, impactos e mitigações
- Agrupamentos de vulnerabilidades por categoria para avaliação sistemática
- Referência rápida para testes de segurança e remediação
- Base para checklists de avaliação de vulnerabilidades e políticas de segurança

---

## Fluxo de Trabalho Principal

### Fase 1: Avaliação de Vulnerabilidades de Injeção

Avalie vetores de ataque de injeção direcionados a componentes de processamento de dados:

**SQL Injection (1)**
- Definição: Código SQL malicioso inserido em campos de entrada para manipular consultas de banco de dados
- Causa Raiz: Falta de validação de entrada, uso inadequado de consultas parametrizadas
- Impacto: Acesso não autorizado a dados, manipulação de dados, comprometimento do banco de dados
- Mitigação: Usar consultas parametrizadas/prepared statements, validação de entrada, contas de banco de dados com privilégio mínimo

**Cross-Site Scripting - XSS (2)**
- Definição: Injeção de scripts maliciosos em páginas web visualizadas por outros usuários
- Causa Raiz: Codificação de saída insuficiente, falta de sanitização de entrada
- Impacto: Sequestro de sessão, roubo de credenciais, desfiguração de site
- Mitigação: Codificação de saída, Content Security Policy (CSP), sanitização de entrada

**Command Injection (5, 11)**
- Definição: Execução de comandos arbitrários do sistema através de aplicações vulneráveis
- Causa Raiz: Entrada do usuário não sanitizada passada para shells do sistema
- Impacto: Comprometimento total do sistema, exfiltração de dados, movimento lateral
- Mitigação: Evitar execução de shell, whitelist de comandos válidos, validação rigorosa de entrada

**XML Injection (6), LDAP Injection (7), XPath Injection (8)**
- Definição: Manipulação de consultas XML/LDAP/XPath através de entrada maliciosa
- Causa Raiz: Tratamento inadequado de entrada na construção de consultas
- Impacto: Exposição de dados, bypass de autenticação, divulgação de informações
- Mitigação: Validação de entrada, consultas parametrizadas, escape de caracteres especiais

**Server-Side Template Injection - SSTI (13)**
- Definição: Injeção de código malicioso em engines de template
- Causa Raiz: Entrada do usuário incorporada diretamente em expressões de template
- Impacto: Execução remota de código, comprometimento do servidor
- Mitigação: Sandbox de engines de template, evitar entrada do usuário em templates, validação rigorosa de entrada

### Fase 2: Segurança de Autenticação e Sessão

Avalie fraquezas de mecanismo de autenticação:

**Session Fixation (14)**
- Definição: Atacante define o ID de sessão da vítima antes da autenticação
- Causa Raiz: ID de sessão não regenerado após login
- Impacto: Sequestro de sessão, acesso não autorizado a conta
- Mitigação: Regenerar ID de sessão na autenticação, usar gerenciamento seguro de sessão

**Brute Force Attack (15)**
- Definição: Adivinhação sistemática de senha usando ferramentas automatizadas
- Causa Raiz: Falta de bloqueio de conta, rate limiting ou CAPTCHA
- Impacto: Acesso não autorizado, comprometimento de credenciais
- Mitigação: Políticas de bloqueio de conta, rate limiting, MFA, CAPTCHA

**Session Hijacking (16)**
- Definição: Atacante rouba ou prevê tokens de sessão válidos
- Causa Raiz: Geração fraca de token de sessão, transmissão insegura
- Impacto: Takeover de conta, acesso não autorizado
- Mitigação: Geração de token aleatória segura, HTTPS, sinalizadores HttpOnly/Secure em cookies

**Credential Stuffing and Reuse (22)**
- Definição: Uso de credenciais vazadas para acessar contas em vários serviços
- Causa Raiz: Usuários reutilizando senhas, sem detecção de violação
- Impacto: Comprometimento em massa de contas, violações de dados
- Mitigação: MFA, verificação de senhas violadas, requisitos de credenciais únicas

**Insecure "Remember Me" Functionality (85)**
- Definição: Implementação fraca de token de autenticação persistente
- Causa Raiz: Tokens previsíveis, controles de expiração inadequados
- Impacto: Acesso persistente não autorizado, comprometimento de sessão
- Mitigação: Geração forte de token, expiração apropriada, armazenamento seguro

**CAPTCHA Bypass (86)**
- Definição: Circunvenção de mecanismos de detecção de bot
- Causa Raiz: Algoritmos CAPTCHA fracos, validação inadequada
- Impacto: Ataques automatizados, credential stuffing, spam
- Mitigação: reCAPTCHA v3, detecção de bot em camadas, rate limiting

### Fase 3: Exposição de Dados Sensíveis

Identifique falhas de proteção de dados:

**IDOR - Insecure Direct Object References (23, 42)**
- Definição: Acesso direto a objetos internos através de referências fornecidas pelo usuário
- Causa Raiz: Verificações de autorização faltando no acesso a objetos
- Impacto: Acesso não autorizado a dados, violações de privacidade
- Mitigação: Validação de controle de acesso, mapas de referência indireta, verificações de autorização

**Data Leakage (24)**
- Definição: Divulgação inadvertida de informações sensíveis
- Causa Raiz: Proteção de dados inadequada, controles de acesso fracos
- Impacto: Violações de privacidade, penalidades regulatórias, danos à reputação
- Mitigação: Soluções DLP, criptografia, controles de acesso, treinamento de segurança

**Unencrypted Data Storage (25)**
- Definição: Armazenamento de dados sensíveis sem criptografia
- Causa Raiz: Falha em implementar criptografia em repouso
- Impacto: Violação de dados se armazenamento for comprometido
- Mitigação: Criptografia de disco completo, criptografia de banco de dados, gerenciamento seguro de chaves

**Information Disclosure (33)**
- Definição: Exposição de detalhes do sistema através de mensagens de erro ou respostas
- Causa Raiz: Tratamento de erro verboso, informações de debug em produção
- Impacto: Reconhecimento para ataques posteriores, exposição de credenciais
- Mitigação: Mensagens de erro genéricas, desabilitar modo debug, logging seguro

### Fase 4: Configuração Incorreta de Segurança

Avalie fraquezas de configuração:

**Missing Security Headers (26)**
- Definição: Ausência de headers HTTP protetores (CSP, X-Frame-Options, HSTS)
- Causa Raiz: Configuração inadequada de servidor
- Impacto: Ataques XSS, clickjacking, downgrade de protocolo
- Mitigação: Implementar CSP, X-Content-Type-Options, X-Frame-Options, HSTS

**Default Passwords (28)**
- Definição: Credenciais padrão não alteradas em sistemas/aplicações
- Causa Raiz: Falha em alterar padrões do fornecedor
- Impacto: Acesso não autorizado, comprometimento do sistema
- Mitigação: Mudanças de senha obrigatórias, políticas de senha forte

**Directory Listing (29)**
- Definição: Servidor web expõe conteúdo de diretórios
- Causa Raiz: Configuração inadequada de servidor
- Impacto: Divulgação de informações, exposição de arquivo sensível
- Mitigação: Desabilitar indexação de diretório, usar arquivos de índice padrão

**Unprotected API Endpoints (30)**
- Definição: APIs sem autenticação ou autorização
- Causa Raiz: Controles de segurança faltando em rotas de API
- Impacto: Acesso não autorizado a dados, abuso de API
- Mitigação: OAuth/chaves de API, controles de acesso, rate limiting

**Open Ports and Services (31)**
- Definição: Serviços de rede desnecessários expostos
- Causa Raiz: Falha em minimizar superfície de ataque
- Impacto: Exploração de serviços vulneráveis
- Mitigação: Auditorias de varredura de porta, regras de firewall, minimização de serviços

**Misconfigured CORS (35)**
- Definição: Políticas Cross-Origin Resource Sharing excessivamente permissivas
- Causa Raiz: Origens curinga, configuração inadequada de CORS
- Impacto: Ataques entre sites, roubo de dados
- Mitigação: Whitelistagem de origens confiáveis, validação de headers CORS

**Unpatched Software (34)**
- Definição: Sistemas executando software desatualizado vulnerável
- Causa Raiz: Gerenciamento de patch negligenciado
- Impacto: Exploração de vulnerabilidades conhecidas
- Mitigação: Programa de gerenciamento de patches, varredura de vulnerabilidades, atualizações automatizadas

### Fase 5: Vulnerabilidades Relacionadas a XML

Avalie segurança de processamento de XML:

**XXE - XML External Entity Injection (37)**
- Definição: Exploração de parsers XML para acessar arquivos ou sistemas internos
- Causa Raiz: Processamento de entidade externa habilitado
- Impacto: Divulgação de arquivo, SSRF, negação de serviço
- Mitigação: Desabilitar entidades externas, usar parsers XML seguros

**XEE - XML Entity Expansion (38)**
- Definição: Expansão de entidade excessiva causando esgotamento de recursos
- Causa Raiz: Expansão de entidade ilimitada permitida
- Impacto: Negação de serviço, falhas de parser
- Mitigação: Limitar expansão de entidade, configurar restrições de parser

**XML Bomb (Billion Laughs) (39)**
- Definição: XML criado com entidades aninhadas consumindo recursos
- Causa Raiz: Definições de entidade recursivas
- Impacto: Esgotamento de memória, negação de serviço
- Mitigação: Limites de expansão de entidade, restrições de tamanho de entrada

**XML Denial of Service (65)**
- Definição: XML especialmente criado causando processamento excessivo
- Causa Raiz: Estruturas de documento complexas sem limites
- Impacto: Esgotamento de CPU/memória, indisponibilidade de serviço
- Mitigação: Validação de schema, limites de tamanho, timeouts de processamento

### Fase 6: Controle de Acesso Quebrado

Avalie aplicação de autorização:

**Inadequate Authorization (40)**
- Definição: Falha em aplicar corretamente controles de acesso
- Causa Raiz: Políticas de autorização fracas, verificações faltando
- Impacto: Acesso não autorizado a recursos sensíveis
- Mitigação: RBAC, IAM centralizado, revisões de acesso regulares

**Privilege Escalation (41)**
- Definição: Obtenção de acesso elevado além das permissões pretendidas
- Causa Raiz: Permissões configuradas incorretamente, vulnerabilidades do sistema
- Impacto: Comprometimento total do sistema, manipulação de dados
- Mitigação: Privilégio mínimo, patching regular, monitoramento de privilégio

**Forceful Browsing (43)**
- Definição: Manipulação direta de URL para acessar recursos restritos
- Causa Raiz: Controles de acesso fracos, URLs previsíveis
- Impacto: Acesso não autorizado a arquivo/diretório
- Mitigação: Controles de acesso do lado do servidor, caminhos de recurso imprevisíveis

**Missing Function-Level Access Control (44)**
- Definição: Funções administrativas ou privilegiadas desprotegidas
- Causa Raiz: Autorização apenas em nível de UI
- Impacto: Execução de função não autorizada
- Mitigação: Autorização do lado do servidor para todas as funções, RBAC

### Fase 7: Desserialização Insegura

Avalie segurança de serialização de objeto:

**Remote Code Execution via Deserialization (45)**
- Definição: Execução de código arbitrário através de objetos serializados maliciosos
- Causa Raiz: Desserialização de dados não confiáveis sem validação
- Impacto: Comprometimento total do sistema, execução de código
- Mitigação: Evitar desserialização de dados não confiáveis, verificações de integridade, validação de tipo

**Data Tampering (46)**
- Definição: Modificação não autorizada de dados serializados
- Causa Raiz: Verificação de integridade faltando
- Impacto: Corrupção de dados, manipulação de privilégio
- Mitigação: Assinaturas digitais, validação HMAC, criptografia

**Object Injection (47)**
- Definição: Instanciação maliciosa de objeto durante desserialização
- Causa Raiz: Práticas de desserialização insegura
- Impacto: Execução de código, acesso não autorizado
- Mitigação: Restrições de tipo, whitelisting de classe, bibliotecas seguras

### Fase 8: Avaliação de Segurança de API

Avalie vulnerabilidades específicas de API:

**Insecure API Endpoints (48)**
- Definição: APIs sem controles de segurança apropriados
- Causa Raiz: Design de API ruim, autenticação faltando
- Impacto: Violação de dados, acesso não autorizado
- Mitigação: OAuth/JWT, HTTPS, validação de entrada, rate limiting

**API Key Exposure (49)**
- Definição: Credenciais de API vazadas ou expostas
- Causa Raiz: Chaves hardcoded, armazenamento inseguro
- Impacto: Acesso não autorizado a API, abuso
- Mitigação: Armazenamento seguro de chave, rotação, variáveis de ambiente

**Lack of Rate Limiting (50)**
- Definição: Sem controles na frequência de requisição de API
- Causa Raiz: Mecanismos de throttling faltando
- Impacto: DoS, abuso de API, esgotamento de recurso
- Mitigação: Limites de taxa por usuário/IP, throttling, proteção DDoS

**Inadequate Input Validation (51)**
- Definição: APIs aceitando entrada do usuário não validada
- Causa Raiz: Validação do lado do servidor faltando
- Impacto: Ataques de injeção, corrupção de dados
- Mitigação: Validação rigorosa, consultas parametrizadas, WAF

**API Abuse (75)**
- Definição: Exploração de funcionalidade de API para fins maliciosos
- Causa Raiz: Confiança excessiva em entrada do cliente
- Impacto: Roubo de dados, takeover de conta, abuso de serviço
- Mitigação: Autenticação forte, análise de comportamento, detecção de anomalia

### Fase 9: Segurança de Comunicação

Avalie proteções da camada de transporte:

**Man-in-the-Middle Attack (52)**
- Definição: Interceptação de comunicação entre partes
- Causa Raiz: Canais não criptografados, redes comprometidas
- Impacto: Roubo de dados, sequestro de sessão, falsificação
- Mitigação: TLS/SSL, certificate pinning, autenticação mútua

**Insufficient Transport Layer Security (53)**
- Definição: Criptografia fraca ou desatualizada para dados em trânsito
- Causa Raiz: Protocolos desatualizado (SSLv2/3), cifras fracas
- Impacto: Interceptação de tráfego, roubo de credencial
- Mitigação: TLS 1.2+, suites de cifra forte, HSTS

**Insecure SSL/TLS Configuration (54)**
- Definição: Configuração incorreta de criptografia
- Causa Raiz: Cifras fracas, sigilo perfeito para frente faltando
- Impacto: Descriptografia de tráfego, ataques MITM
- Mitigação: Suites de cifra modernas, PFS, validação de certificado

**Insecure Communication Protocols (55)**
- Definição: Uso de protocolos não criptografados (HTTP, Telnet, FTP)
- Causa Raiz: Sistemas legados, falta de conhecimento de segurança
- Impacto: Sniffing de tráfego, exposição de credencial
- Mitigação: HTTPS, SSH, SFTP, túneis VPN

### Fase 10: Vulnerabilidades do Lado do Cliente

Avalie segurança do navegador:

**DOM-based XSS (56)**
- Definição: XSS através de manipulação de JavaScript do lado do cliente
- Causa Raiz: Manipulação insegura de DOM com entrada do usuário
- Impacto: Roubo de sessão, colheita de credencial
- Mitigação: APIs DOM seguras, CSP, sanitização de entrada

**Insecure Cross-Origin Communication (57)**
- Definição: Tratamento inadequado de requisições entre origens
- Causa Raiz: Políticas relaxadas de CORS/SOP
- Impacto: Vazamento de dados, ataques CSRF
- Mitigação: CORS rigoroso, tokens CSRF, validação de origem

**Browser Cache Poisoning (58)**
- Definição: Manipulação de conteúdo cacheado
- Causa Raiz: Validação de cache fraca
- Impacto: Entrega de conteúdo malicioso
- Mitigação: Headers Cache-Control, HTTPS, verificações de integridade

**Clickjacking (59, 71)**
- Definição: Ataque de redress de UI enganando usuários para clicar em elementos ocultos
- Causa Raiz: Proteção de frame faltando
- Impacto: Ações não pretendidas, roubo de credencial
- Mitigação: X-Frame-Options, CSP frame-ancestors, frame-busting

**HTML5 Security Issues (60)**
- Definição: Vulnerabilidades em APIs HTML5 (WebSockets, Storage, Geolocation)
- Causa Raiz: Uso inadequado de API, validação insuficiente
- Impacto: Vazamento de dados, XSS, violações de privacidade
- Mitigação: Uso seguro de API, validação de entrada, sandboxing

### Fase 11: Avaliação de Negação de Serviço

Avalie ameaças de disponibilidade:

**DDoS - Distributed Denial of Service (61)**
- Definição: Sobrecarga de sistemas com tráfego de múltiplas fontes
- Causa Raiz: Botnets, ataques de amplificação
- Impacto: Indisponibilidade de serviço, perda de receita
- Mitigação: Serviços de proteção DDoS, rate limiting, CDN

**Application Layer DoS (62)**
- Definição: Direcionamento de lógica de aplicação para esgotar recursos
- Causa Raiz: Código ineficiente, operações que consomem muitos recursos
- Impacto: Indisponibilidade de aplicação, desempenho degradado
- Mitigação: Rate limiting, caching, WAF, otimização de código

**Resource Exhaustion (63)**
- Definição: Depleção de recursos CPU, memória, disco ou rede
- Causa Raiz: Gerenciamento ineficiente de recurso
- Impacto: Falhas do sistema, degradação de serviço
- Mitigação: Quotas de recurso, monitoramento, balanceamento de carga

**Slowloris Attack (64)**
- Definição: Manutenção de conexões abertas com requisições HTTP parciais
- Causa Raiz: Sem timeouts de conexão
- Impacto: Esgotamento de recurso de servidor web
- Mitigação: Timeouts de conexão, limites de requisição, proxy reverso

### Fase 12: Server-Side Request Forgery

Avalie vulnerabilidades de SSRF:

**SSRF - Server-Side Request Forgery (66)**
- Definição: Manipulação de servidor para fazer requisições a recursos internos
- Causa Raiz: URLs controladas pelo usuário não validadas
- Impacto: Acesso à rede interna, roubo de dados, acesso a metadados de nuvem
- Mitigação: Whitelisting de URL, segmentação de rede, filtragem de egress

**Blind SSRF (87)**
- Definição: SSRF sem visibilidade de resposta direta
- Causa Raiz: Similar a SSRF, mais difícil de detectar
- Impacto: Exfiltração de dados, reconhecimento interno
- Mitigação: Allowlists, WAF, restrições de rede

**Time-Based Blind SSRF (88)**
- Definição: Inferência de sucesso de SSRF através de timing de resposta
- Causa Raiz: Atrasos de processamento indicando resultados de requisição
- Impacto: Exploração prolongada, evasão de detecção
- Mitigação: Timeouts de requisição, detecção de anomalia, monitoramento de timing

### Fase 13: Vulnerabilidades Web Adicionais

| # | Vulnerabilidade | Causa Raiz | Impacto | Mitigação |
|---|--------------|-----------|--------|------------|
| 67 | HTTP Parameter Pollution | Parsing inconsistente | Injeção, bypass de ACL | Parsing rigoroso, validação |
| 68 | Insecure Redirects | Destinos não validados | Phishing, malware | Whitelistagem de destinos |
| 69 | File Inclusion (LFI/RFI) | Caminhos não validados | Exec de código, divulgação | Whitelistagem de arquivo, desabilitar RFI |
| 70 | Security Header Bypass | Headers configurados incorretamente | XSS, clickjacking | Headers apropriados, auditorias |
| 72 | Inadequate Session Timeout | Timeouts excessivos | Sequestro de sessão | Terminação por inatividade, timeouts |
| 73 | Insufficient Logging | Infraestrutura faltando | Lacunas de detecção | SIEM, alerting |
| 74 | Business Logic Flaws | Design inseguro | Fraude, operações não autorizadas | Threat modeling, testes |

### Fase 14: Segurança de Mobile e IoT

| # | Vulnerabilidade | Causa Raiz | Impacto | Mitigação |
|---|--------------|-----------|--------|------------|
| 76 | Insecure Mobile Storage | Texto plano, crypto fraca | Roubo de dados | Keychain/Keystore, criptografia |
| 77 | Insecure Mobile Transmission | HTTP, falhas de cert | Interceptação de tráfego | TLS, certificate pinning |
| 78 | Insecure Mobile APIs | Auth/validação faltando | Exposição de dados | OAuth/JWT, validação |
| 79 | App Reverse Engineering | Credenciais hardcoded | Roubo de credencial | Obfuscação, RASP |
| 80 | IoT Management Issues | Auth fraca, sem TLS | Takeover de dispositivo | Auth forte, TLS |
| 81 | Weak IoT Authentication | Senhas padrão | Acesso não autorizado | Credenciais únicas, MFA |
| 82 | IoT Vulnerabilities | Falhas de design, firmware antigo | Recrutamento de botnet | Atualizações, segmentação |
| 83 | Smart Home Access | Padrões inseguros | Invasão de privacidade | MFA, segmentação |
| 84 | IoT Privacy Issues | Coleta excessiva | Vigilância | Minimização de dados |

### Fase 15: Ameaças Avançadas e Zero-Day

| # | Vulnerabilidade | Causa Raiz | Impacto | Mitigação |
|---|--------------|-----------|--------|------------|
| 89 | MIME Sniffing | Headers faltando | XSS, spoofing | X-Content-Type-Options |
| 91 | CSP Bypass | Config fraca | XSS apesar de CSP | CSP rigoroso, nonces |
| 92 | Inconsistent Validation | Lógica descentralizada | Bypass de controle | Validação centralizada |
| 93 | Race Conditions | Sincronismo faltando | Escalação de privilégio | Locking apropriado |
| 94-95 | Business Logic Flaws | Validação faltando | Fraude financeira | Validação do lado do servidor |
| 96 | Account Enumeration | Respostas diferentes | Ataques direcionados | Respostas uniformes |
| 98-99 | Unpatched Vulnerabilities | Atrasos de patch | Exploração zero-day | Gerenciamento de patches |
| 100 | Zero-Day Exploits | Vulns desconhecidas | Ataques não mitigados | Defesa em profundidade |

---

## Referência Rápida

### Resumo de Categorias de Vulnerabilidade

| Categoria | Números de Vulnerabilidade | Controles-Chave |
|----------|----------------------|--------------|
| Injeção | 1-13 | Consultas parametrizadas, validação de entrada, codificação de saída |
| Autenticação | 14-23, 85-86 | MFA, gerenciamento de sessão, bloqueio de conta |
| Exposição de Dados | 24-27 | Criptografia em repouso/trânsito, controles de acesso, DLP |
| Configuração Incorreta | 28-36 | Padrões seguros, hardening, patching |
| XML | 37-39, 65 | Desabilitar entidades externas, limitar expansão |
| Controle de Acesso | 40-44 | RBAC, privilégio mínimo, verificações de autorização |
| Desserialização | 45-47 | Evitar dados não confiáveis, validação de integridade |
| Segurança de API | 48-51, 75 | OAuth, rate limiting, validação de entrada |
| Comunicação | 52-55 | TLS 1.2+, validação de certificado, HTTPS |
| Lado do Cliente | 56-60 | CSP, X-Frame-Options, DOM seguro |
| DoS | 61-65 | Rate limiting, proteção DDoS, limites de recurso |
| SSRF | 66, 87-88 | Whitelisting de URL, filtragem de egress |
| Mobile/IoT | 76-84 | Criptografia, autenticação, armazenamento seguro |
| Lógica de Negócio | 74, 92-97 | Threat modeling, testes de lógica |
| Zero-Day | 98-100 | Defesa em profundidade, inteligência de ameaça |

### Headers de Segurança Críticos

```
Content-Security-Policy: default-src 'self'; script-src 'self'
X-Content-Type-Options: nosniff
X-Frame-Options: DENY
X-XSS-Protection: 1; mode=block
Strict-Transport-Security: max-age=31