---
name: detection-response
description: "Detección y respuesta a incidentes generalista. Cubre SIEM, SOAR, threat hunting, IR lifecycle, forensics, logging, monitoring, y purple teaming. Actívala al configurar SOC, responder a incidentes o diseñar capacidades de detección."
disable-model-invocation: true
---

# Detección y Respuesta a Incidentes

Guía de operaciones de seguridad: desde logging hasta recuperación post-incidente.

---

## Logging y Monitorización

### Principios
- **Log everything, trust nothing**: Toda acción sensible debe dejar rastro
- **Inmutabilidad**: Logs no deben ser modificables por atacantes
- **Centralización**: Agregar en SIEM, no dispersar
- **Retención**: Definir por compliance y necesidad forense (típico 1-7 años)
- **Redacción**: No loggear PII, passwords, tokens, tarjetas

### Qué loggear

| Evento | Datos | Prioridad |
|--------|-------|-----------|
| AuthN success/fail | User, IP, user-agent, MFA result | Crítico |
| AuthZ decisions | Resource, action, decision, reason | Crítico |
| Admin actions | Config changes, privilege escalation | Crítico |
| Data access | Who, what, when, classification | Crítico |
| Network flow | Src IP, dst IP, port, bytes, duration | Alto |
| File integrity | Path, hash, user, action | Alto |
| Process execution | Command line, user, parent process | Alto |
| API requests | Endpoint, method, status, latency, client | Medio |

### Formatos
- Preferir structured logging (JSON) sobre texto libre
- Campos estándar: timestamp (ISO 8601), severity, service, trace_id, user_id, action, result, source_ip
- Correlación por trace_id/correlation_id entre servicios

### Retención y protección
- Hot storage (7-30 días): SIEM, búsqueda rápida
- Warm storage (1-12 meses): Data lake, búsqueda batch
- Cold storage (1-7 años): WORM / Glacier / Archive, compliance
- Hash/chain de integridad para logs críticos (blockchain-like o HMAC)

---

## SIEM (Security Information and Event Management)

### Funciones
- **Collection**: Agregar logs de toda la infraestructura
- **Correlation**: Detectar patrones entre múltiples fuentes
- **Alerting**: Generar alertas basadas en reglas o ML
- **Investigation**: Búsqueda forense, pivoting
- **Reporting**: Dashboards, compliance, métricas
- **Retention**: Storage escalable

### Plataformas
- Enterprise: Splunk, IBM QRadar, Microsoft Sentinel, Chronicle
- Open source: Wazuh, Elastic Security, Graylog, Apache Metron
- Cloud-native: AWS Security Lake, Azure Sentinel, Google Chronicle

### Reglas de detección (use cases)
```
1. Brute force: 5+ failed logins en 5 min desde misma IP
2. Impossible travel: Login desde 2 países en < 2 horas
3. Privilege escalation: User asignado a admin role
4. Lateral movement: RDP/SSH entre workstations
5. Data exfiltration: > 1GB upload a dominio raro
6. Malware: Process execution desde temp con conexión outbound
7. Insider threat: Acceso a datos fuera de patrón normal
```

---

## SOAR (Security Orchestration, Automation and Response)

### Casos de automatización
```
Alerta: Phishing reportado
  → Extraer IOCs (URLs, hashes)
  → Buscar en endpoints (EDR)
  → Bloquear en firewall/proxy
  → Crear ticket Jira
  → Notificar al usuario
  → Enriquecer con Threat Intel
```

### Playbooks comunes
- **Triage automático**: Enriquecer alerta con contexto, priorizar, asignar
- **Containment**: Isolar host, bloquear IP, revocar sesión
- **Eradication**: Kill process, eliminar malware, patch
- **Notification**: Slack/Teams a SOC, email a stakeholders

### Plataformas
- Palo Alto XSOAR, Splunk SOAR, Tines, Shuffle, Phantom

---

## Threat Hunting

### Diferencia con detección reactiva
- **Detección**: Esperar alerta, investigar
- **Hunting**: Hipótesis activa, búsqueda proactiva

### Hipótesis de hunting
```
1. "Un atacante con credenciales válidas está moviéndose lateralmente"
   → Buscar: RDP/SSH/SMB entre hosts que nunca se comunicaron

2. "Hay un web shell en nuestros servidores web"
   → Buscar: archivos PHP/ASP/JSP recientes en directorios web

3. "Un insider está exfiltrando datos"
   → Buscar: usuarios con downloads/upload anómalos fuera de horario

4. "Hay persistencia en endpoints"
   → Buscar: nuevas tareas programadas, run keys, servicios
```

### Técnicas
- **IOC-based**: Buscar indicadores conocidos (IPs, hashes, domains)
- **Behavioral**: Desviaciones de baseline (ML, UEBA)
- **Hypothesis-driven**: Basado en TTPs de MITRE ATT&CK

---

## Incident Response Lifecycle (NIST SP 800-61)

### 1. Preparation
- Plan de IR documentado y aprobado
- Equipo designado con roles claros
- Herramientas listas (forensics kits, imágenes limpias)
- Contactos legales, PR, forense, law enforcement
- Simulacros (tabletop exercises) trimestrales

### 2. Detection & Analysis
- Identificar: ¿Es un incidente real? ¿Qué tipo?
- Clasificar: Malware, breach, DDoS, insider, APT
- Priorizar: Impacto × Urgencia
- Documentar: Timeline inicial, evidencia preservada

### 3. Containment
- **Short-term**: Isolar host, bloquear IP, revocar cuenta
- **Long-term**: Segmentar red, reforzar monitoreo, preservar evidencia
- Evidencia: Memory dump, disk image, logs, network captures

### 4. Eradication
- Eliminar malware, backdoors, cuentas comprometidas
- Patching de vulnerabilidades explotadas
- Rotación de credenciales expuestas
- Verificación: scan forense, re-image si es necesario

### 5. Recovery
- Restaurar desde backups limpios
- Monitoreo intensivo del sistema recuperado
- Validar integridad antes de reconexión
- Comunicación a usuarios/clientes afectados

### 6. Post-Incident Activity
- Lessons learned meeting (dentro de 72h)
- Actualizar playbooks, reglas de detección
- Métricas: MTTD (Mean Time to Detect), MTTR (Mean Time to Respond)
- Reporte ejecutivo

---

## Forensics Básico

### Orden de volatilidad
```
1. CPU registers, cache
2. RAM (memory dump)
3. Network state, connections
4. Disk (running processes, open files)
5. External storage, logs remotos
6. Archival media (backups)
```

### Cadena de custodia
- Documentar quién tocó qué, cuándo, por qué
- Hashes criptográficos (SHA-256) de toda evidencia
- Almacenamiento write-protected
- Acceso limitado y auditado

### Herramientas
- **Memory**: Volatility, Rekall, Magnet RAM Capture
- **Disk**: Autopsy, Sleuth Kit, FTK Imager
- **Network**: Wireshark, Zeek, NetworkMiner
- **Logs**: Splunk, ELK, custom parsers
- **Mobile**: Cellebrite, Oxygen, open source alternatives

---

## Purple Teaming

### Concepto
Colaboración entre Red Team (ataque) y Blue Team (defensa) para mejorar:
- Red Team ejecuta TTPs específicos
- Blue Team observa y ajusta detección
- Knowledge transfer en tiempo real

### Ejercicio típico
```
1. Plan: Red Team propone 3 técnicas MITRE ATT&CK
2. Execute: Red Team ejecuta con Blue Team observando
3. Detect: Blue Team identifica qué detectó, qué no, y por qué
4. Improve: Blue Team ajusta reglas; Red Team ajusta evasión
5. Repeat: Ciclo continuo
```

---

## Métricas de SOC / IR

| Métrica | Meta | Definición |
|---------|------|------------|
| MTTD | < 24h | Tiempo desde inicio del incidente hasta detección |
| MTTR | < 4h | Tiempo desde detección hasta contención |
| MTTC | < 1h | Tiempo desde alerta hasta triage inicial |
| Alert quality | > 80% | True positives / total alerts |
| Escalation rate | < 10% | Alertas que requieren nivel 2+ |
| Coverage | 100% | Técnicas MITRE ATT&CK con detección |

---

## Checklist de detección y respuesta

- [ ] Logging centralizado e inmutable para todos los sistemas críticos
- [ ] SIEM operativo con reglas de detección basadas en MITRE ATT&CK
- [ ] Retención de logs definida por compliance (1-7 años)
- [ ] SOAR con playbooks para incidentes comunes
- [ ] Threat hunting program: hipótesis semanales
- [ ] Plan de IR documentado, aprobado y testeado (tabletop)
- [ ] Equipo de IR con roles definidos y contactos 24/7
- [ ] Forensics toolkit listo y actualizado
- [ ] Purple teaming trimestral
- [ ] MTTD y MTTR medidos y mejorando
- [ ] Post-incident reviews dentro de 72h con acciones
- [ ] Comunicación de incidentes a stakeholders definida
