---
name: red-team-tactics
description: Princípios de táticas de red team baseados no framework MITRE ATT&CK. Fases de ataque, evasão de detecção, relatórios.
allowed-tools: Read, Glob, Grep
---

# Red Team Tactics

> Princípios de simulação de adversário baseados no framework MITRE ATT&CK.

---

## 1. Fases MITRE ATT&CK

### Ciclo de Ataque

```
RECONNAISSANCE → INITIAL ACCESS → EXECUTION → PERSISTENCE
       ↓              ↓              ↓            ↓
   PRIVILEGE ESC → DEFENSE EVASION → CRED ACCESS → DISCOVERY
       ↓              ↓              ↓            ↓
LATERAL MOVEMENT → COLLECTION → C2 → EXFILTRATION → IMPACT
```

### Objetivos por Fase

| Fase | Objetivo |
|-------|-----------|
| **Recon** | Mapear superfície de ataque |
| **Initial Access** | Obter primeiro acesso |
| **Execution** | Executar código no alvo |
| **Persistence** | Persistir após reboots |
| **Privilege Escalation** | Obter privilégios de admin/root |
| **Defense Evasion** | Evitar detecção |
| **Credential Access** | Coletar credenciais |
| **Discovery** | Mapear rede interna |
| **Lateral Movement** | Espalhar para outros sistemas |
| **Collection** | Coletar dados do alvo |
| **C2** | Manter canal de comando |
| **Exfiltration** | Extrair dados |

---

## 2. Princípios de Reconhecimento

### Passivo vs Ativo

| Tipo | Trade-off |
|------|-----------|
| **Passivo** | Sem contato com alvo, informações limitadas |
| **Ativo** | Contato direto, maior risco de detecção |

### Alvo de Informações

| Categoria | Valor |
|----------|-------|
| Stack de tecnologia | Seleção de vetor de ataque |
| Informações de funcionários | Engenharia social |
| Ranges de rede | Escopo de varredura |
| Terceiros | Ataque de cadeia de suprimentos |

---

## 3. Vetores de Acesso Inicial

### Critérios de Seleção

| Vetor | Quando Usar |
|--------|-------------|
| **Phishing** | Alvo humano, acesso a email |
| **Exploits públicos** | Serviços vulneráveis expostos |
| **Credenciais válidas** | Vazadas ou quebradas |
| **Cadeia de suprimentos** | Acesso de terceiros |

---

## 4. Princípios de Escalação de Privilégios

### Alvo Windows

| Verificação | Oportunidade |
|-------|-------------|
| Caminhos de serviço sem aspas | Escrever no path |
| Permissões fracas de serviço | Modificar serviço |
| Privilégios de token | Abusar SeDebug, etc. |
| Credenciais armazenadas | Coletar |

### Alvo Linux

| Verificação | Oportunidade |
|-------|-------------|
| Binários SUID | Executar como proprietário |
| Misconfigurações de sudo | Execução de comando |
| Vulnerabilidades de kernel | Exploits de kernel |
| Cron jobs | Scripts graváveis |

---

## 5. Princípios de Evasão de Defesa

### Técnicas Principais

| Técnica | Propósito |
|-----------|---------|
| LOLBins | Usar ferramentas legítimas |
| Ofuscação | Ocultar código malicioso |
| Timestomping | Ocultar modificações de arquivo |
| Limpeza de logs | Remover evidências |

### Segurança Operacional

- Trabalhar durante horário comercial
- Imitar padrões de tráfego legítimo
- Usar canais criptografados
- Mesclar com comportamento normal

---

## 6. Princípios de Movimento Lateral

### Tipos de Credenciais

| Tipo | Uso |
|------|-----|
| Senha | Autenticação padrão |
| Hash | Pass-the-hash |
| Ticket | Pass-the-ticket |
| Certificado | Autenticação por certificado |

### Caminhos de Movimento

- Shares de admin
- Serviços remotos (RDP, SSH, WinRM)
- Exploração de serviços internos

---

## 7. Ataques em Active Directory

### Categorias de Ataque

| Ataque | Alvo |
|--------|--------|
| Kerberoasting | Senhas de contas de serviço |
| AS-REP Roasting | Contas sem pré-autenticação |
| DCSync | Credenciais de domínio |
| Golden Ticket | Acesso persistente ao domínio |

---

## 8. Princípios de Relatório

### Narrativa de Ataque

Documente a cadeia de ataque completa:
1. Como o acesso inicial foi obtido
2. Quais técnicas foram usadas
3. Quais objetivos foram alcançados
4. Onde a detecção falhou

### Lacunas de Detecção

Para cada técnica bem-sucedida:
- O que deveria ter detectado?
- Por que a detecção não funcionou?
- Como melhorar a detecção

---

## 9. Limites Éticos

### Sempre

- Ficar dentro do escopo
- Minimizar impacto
- Reportar imediatamente se ameaça real for encontrada
- Documentar todas as ações

### Nunca

- Destruir dados de produção
- Causar negação de serviço (a menos que no escopo)
- Acessar além de prova de conceito
- Reter dados sensíveis

---

## 10. Anti-Padrões

| ❌ Não faça | ✅ Faça |
|----------|-------|
| Apressar exploração | Seguir metodologia |
| Causar dano | Minimizar impacto |
| Pular relatórios | Documentar tudo |
| Ignorar escopo | Ficar dentro dos limites |

---

> **Lembre-se:** Red team simula atacantes para melhorar as defesas, não para causar dano.