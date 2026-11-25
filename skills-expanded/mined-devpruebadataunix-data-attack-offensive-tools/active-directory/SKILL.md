---
name: active-directory
description: Ruta de ataque en Active Directory — enumeración, Kerberoasting/AS-REP roasting, abuso de ACL/ADCS, DCSync y movimiento lateral. Úsala tras obtener un punto de apoyo (credencial o sesión) en un dominio Windows en scope.
---

# Active Directory — del punto de apoyo al dominio

El core del pentest enterprise. La cadena típica es: **enumerar → cosechar credenciales →
escalar por mala configuración → DCSync → dominio**. Todo dentro de scope y con aprobación humana.

## Cuándo usarla
Con una credencial de dominio (aunque sea de bajo privilegio) o una sesión en un host unido al
dominio, ambos en `contracts/scope.json`. La VLAN del cliente es la zona E2 (kill-switch activo).

## Técnicas (con MITRE)
- **Enumeración** (T1087, T1069): usuarios, grupos, GPO, confianzas; mapa de rutas con BloodHound.
- **Kerberoasting** (T1558.003): pide TGS de cuentas con SPN y crackea offline.
- **AS-REP roasting** (T1558.004): cuentas sin preauth Kerberos → hash crackeable.
- **Abuso de ACL** (T1098): `GenericAll`/`WriteDACL`/`ForceChangePassword` sobre objetos.
- **ADCS** (ESC1-ESC8): plantillas de certificado mal configuradas → suplantación.
- **DCSync** (T1003.006): con privilegios de replicación, extrae hashes del dominio (krbtgt).
- **Movimiento lateral** (T1021): pass-the-hash/ticket, SMB/WinRM/WMI.

## Herramientas (suite del repo)
- `netexec` (nxc) — spray, enum, ejecución SMB/LDAP/WinRM — tier **destructive** (siempre pregunta).
- Impacket (`GetUserSPNs`, `GetNPUsers`, `secretsdump`, `psexec`/`wmiexec`) — **destructive**.
- `certipy` (ADCS) — tier **sensitive**.
- `bloodhound`/bloodhound-python (rutas de ataque) — tier **sensitive**.
- Cracking offline: `hashcat`/`john` (modos 13100 TGS, 18200 AS-REP) — tier **sensitive**.

## Evidencia y alcance
- Cada hallazgo necesita prueba: salida de la herramienta + objeto/identidad afectada como `evidence`.
- DCSync/secretsdump tocan un Domain Controller: acción **destructive** → el bot exige tu OK.
- Mapea a `contracts/finding.schema.json`; `status` real solo con impacto demostrado.
- **Sin fuente no se explota**: una ACL "explotable" en BloodHound es candidato hasta ejecutarla.
