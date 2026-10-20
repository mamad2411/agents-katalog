<!--
LICENSE UPL
Author: Mauro Risonho de Paula Assumpção
Data Create: 2026-03-16
Data Update: 2026-03-16
-->

---
name: writeup-djotahub
description: CTF writeups and security challenges by djotahub.
---

# Writeups by djotahub

Source repository: `/repos/djotahub`

## Repository Index

- ecommerce-audit-pentest/README.md
- ecommerce-audit-pentest/01_Executive_Report/report_source.md

## Writeup Content


### File: ecommerce-audit-pentest/README.md

# Auditoría Web: Compromiso y Remediación

## 1. Descripción General del Proyecto

Este repositorio contiene los artefactos técnicos, documentación ejecutiva y código de ingeniería de remediación resultantes de una **Prueba de Penetración de Caja Negra (Black-Box)** exhaustiva, realizada sobre una arquitectura moderna de comercio electrónico (Stack MEAN).

El objetivo principal de este compromiso fue evaluar la postura de seguridad de la aplicación frente a las categorías de riesgo del **OWASP Top 10**, identificando vulnerabilidades que pudieran comprometer la confidencialidad, integridad y disponibilidad de los datos (Tríada CID).

### 1.1 Alcance del Trabajo

- **Objetivo:** OWASP Juice Shop (v14.x)
    
- **Tipo de Evaluación:** Evaluación de Seguridad Ofensiva (Caja Negra)
    
- **Áreas de Enfoque:** Mecanismos de autenticación, Gestión de Sesiones, Control de Acceso (BOLA/IDOR) y fallas de Inyección.
    

## 2. Metodología

La evaluación siguió el estándar **PTES (Penetration Testing Execution Standard)**:

1. **Recolección de Inteligencia:** Reconocimiento pasivo y activo de los endpoints de la API y la lógica de la aplicación.
    
2. **Modelado de Amenazas:** Identificación de activos de alto valor (Base de Datos de Usuarios, Paneles Administrativos).
    
3. **Análisis de Vulnerabilidades:** Verificación manual de fallas en la validación de entradas.
    
4. **Explotación:** Ejecución controlada de payloads para demostrar el impacto (Prueba de Concepto).
    
5. **Post-Explotación:** Evaluación de posible movimiento lateral y escalada de privilegios.
    
6. **Reporte y Remediación:** Desarrollo de informes técnicos y parches de código seguro.
    

## 3. Estructura del Repositorio

Este repositorio está organizado para reflejar un paquete de entregables de consultoría estándar:

- **`/01_Executive_Report`**: Contiene el informe final de auditoría (`.pdf` / `.md`). Este documento incluye resúmenes ejecutivos, matrices de riesgo y hallazgos técnicos detallados mapeados a puntajes CVSS v3.1.
    
- **`/02_Technical_Evidence`**: Evidencia forense cruda recolectada durante el compromiso (Logs de Burp Suite, capturas de pantalla y volcados de peticiones/respuestas HTTP).
    
- **`/03_Remediation_Code`**: Contramedidas de ingeniería. Incluye comparaciones de código "Vulnerable" vs. "Seguro" para demostrar la implementación de prácticas de codificación segura (ej. Sentencias Preparadas, Codificación de Salida, Middlewares ABAC).
    

## 4. Stack Técnico y Herramientas

- **Análisis Dinámico (DAST):** Burp Suite, OWASP ZAP.
    
- **Frameworks de Explotación:** SQLMap (Inyección SQL Automatizada), Scripts de Python personalizados (C2/Exfiltración).
    
- **Entorno de Desarrollo:** Node.js, SQLite, Express.js.
    

## 5. Aviso Legal (Disclaimer)

Este proyecto está destinado únicamente a fines educativos y de demostración de portafolio. Todas las pruebas se realizaron en un entorno de laboratorio controlado y aislado.

**Autor:** Qb1t | **Rol:** Offensive Security Engineer



### File: ecommerce-audit-pentest/01_Executive_Report/report_source.md

# Informe de Auditoría de Seguridad Ecommerce Platform

|Meta-Información|Detalle|
|---|---|
|**Cliente:**|Simulación Interna (OWASP Juice Shop)|
|**Fecha:**|02 de Noviembre, 2025|
|**Clasificación:**|🔴 Confidencial / Solo uso interno|
|**Consultor:**|[Qb1t]|

## 1. Resumen Ejecutivo

### 1.1 Alcance y Objetivo

Se ha realizado una **Prueba de Penetración de Caja Negra (Black-Box Penetration Test)** sobre la infraestructura de comercio electrónico de la organización. El objetivo principal fue evaluar la resiliencia de la aplicación frente a ataques dirigidos que pudieran comprometer la confidencialidad de los datos de clientes, la integridad de las transacciones y la disponibilidad del servicio.

La evaluación se centró en los riesgos definidos en el estándar **OWASP Top 10**, simulando el comportamiento de un actor de amenaza externo con intenciones maliciosas.

### 1.2 Panorama de Riesgos Detectados

Durante la ventana de auditoría, se identificaron **tres (3) vulnerabilidades críticas y de alto impacto** que permiten el compromiso total de la plataforma.

| ID Hallazgo | Vulnerabilidad                   | Severidad     | Impacto de Negocio                                                                                                                                            |
| ----------- | -------------------------------- | ------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **VULN-01** | **SQL Injection (SQLi)**         | 🔴**CRÍTICA** | **Pérdida Total de Confidencialidad.** Un atacante puede extraer la base de datos completa de clientes (PII) y acceder como Administrador sin credenciales.   |
| **VULN-02** | **Cross-Site Scripting (XSS)**   | 🟠 **ALTA**   | **Fraude y Suplantación.** Permite el secuestro de sesiones activas (Account Takeover), facilitando fraudes a nombre de usuarios legítimos o administradores. |
| **VULN-03** | **IDOR (Broken Access Control)** | 🟡 **MEDIA**  | **Fuga de Información Privada.** Exposición no autorizada de historiales de compra y datos de carritos de terceros.                                           |
|             |                                  |               |                                                                                                                                                               |

### 1.3 Conclusión Estratégica

La postura de seguridad actual de la aplicación es **insuficiente** para operar en un entorno productivo. La existencia de una inyección SQL trivial en el mecanismo de autenticación representa un riesgo inaceptable para la continuidad del negocio.

**Recomendación Inmediata:** Se aconseja suspender cualquier paso a producción o nuevas funcionalidades hasta que se apliquen los parches de seguridad detallados en la Sección 3 (Remediación), priorizando la implementación de consultas parametrizadas y validación de sesiones.

## 2. Hallazgos Técnicos Detallados

### 2.1 [CRÍTICA] SQL Injection en Mecanismos de Autenticación

**CVSS v3.1 Base Score:** 9.8 (Critical) **Vector:** `/rest/user/login`

#### Descripción Técnica

La aplicación no sanitiza correctamente la entrada del usuario antes de construir las consultas SQL. Esto permite la inyección de comandos arbitrarios en la base de datos backend (SQLite), resultando en una evasión total de la autenticación.

#### Prueba de Concepto (PoC)

**Fase 1: Evasión de Autenticación** Se interceptó la petición de login inyectando el payload `' OR 1=1 --`. Esto forzó a la base de datos a evaluar la condición lógica como "VERDADERA", otorgando acceso inmediato a la cuenta administrativa.

_Evidencia 1: Petición Maliciosa interceptada en Burp Suite:_
![SQLi Request](../02_Technical_Evidence/01_SQL_Injection/SQLi_01_Burp_Request.png)

**Análisis Forense (JWT):** Mediante el análisis del Token de Sesión en el Decoder de Burp Suite, se confirmó que el servidor asignó el rol de `admin` al atacante.

_Evidencia 2: Decodificación del Token Admin:_
![JWT Decoder](../02_Technical_Evidence/01_SQL_Injection/SQLi_02_Burp_DecoderRole.png)

_Evidencia 3: Acceso Administrativo confirmado en navegador:_
![Admin Proof](../02_Technical_Evidence/01_SQL_Injection/SQLi_02_Admin_Access_Proof.png)

**Fase 2: Exfiltración de Datos (Data Breach)** Se escaló el ataque para realizar un volcado completo de la tabla `Users`, obteniendo correos y hashes de contraseñas de todos los clientes.

_Evidencia 4: Volcado de Base de Datos (Emails y Hashes):_
![DB Dump Browser](../02_Technical_Evidence/01_SQL_Injection/sqlidump4.png)

_Evidencia 4.1: Volcado de Base de Datos (tabla Users):_
![DB Dump Terminal](../02_Technical_Evidence/01_SQL_Injection/SQLi_03_Database_Dump.png)

#### Recomendación Técnica

Reemplazar la concatenación de cadenas por **Prepared Statements (Consultas Parametrizadas)**. Esto asegura que el motor de base de datos trate la entrada del usuario estrictamente como datos literales.

### 2.2 [ALTA] Account Takeover vía Cross-Site Scripting (XSS)

**CVSS v3.1 Base Score:** 8.1 (High) **Vector:** Barra de Búsqueda (Reflected XSS)

#### Descripción Técnica

La aplicación refleja la entrada del usuario en el navegador sin la debida codificación de salida (Output Encoding). Esto permite la inyección y ejecución de código JavaScript malicioso en el contexto de la sesión de la víctima.

#### Prueba de Concepto (PoC)

**Fase 1: Ejecución de Código Arbitrario** Se inyectó un payload `<iframe src="javascript:alert('XSS')">` confirmando la falta de sanitización.

_Evidencia 5: Ejecución de alerta en navegador:_
![XSS Alert](../02_Technical_Evidence/02_Cross_Site_Scripting/XSS_02_Alert_Execution.png)

**Fase 2: Secuestro de Sesión (Session Hijacking)** Se escaló el ataque inyectando un script capaz de exfiltrar el **JSON Web Token (JWT)** de la víctima hacia un servidor C2 controlado por el atacante.

_Evidencia 6: Token de sesión capturado en la terminal del atacante:_
![Token Steal](../02_Technical_Evidence/02_Cross_Site_Scripting/XSS_03_Cookie_Steal_Terminal.png)

**Fase 3: Suplantación de Identidad** Utilizando el token exfiltrado, se inyectó la sesión en un navegador en modo incógnito (simulando un equipo externo), logrando acceso total a la cuenta de Administrador sin credenciales.

_Evidencia 7: Inyección del Token Robado:_
![Account Takeover](../02_Technical_Evidence/02_Cross_Site_Scripting/XSS_04_Account_Takeover_Proof.png)

_Evidencia 7.1:Validación de persistencia en Local Storage::_
![LocalStorage Injection](../02_Technical_Evidence/02_Cross_Site_Scripting/XSS_05_Local_Storage_Account_Takeover_Proof.png)
#### Recomendación Técnica

1. **Codificación de Salida:** Implementar librerías de `escape-html` para convertir caracteres especiales en entidades seguras.
    
2. **Seguridad de Cookies:** Configurar las cookies de sesión con el flag `HttpOnly` para impedir su lectura mediante JavaScript.
    

### 2.3 [MEDIA] Insecure Direct Object Reference (IDOR) en Carrito

**CVSS v3.1 Base Score:** 5.3 (Medium) **Vector:** `/rest/basket/{id}`

#### Descripción Técnica

El endpoint de consulta de carritos (`GET`) utiliza identificadores numéricos secuenciales sin validar correctamente la propiedad del objeto. Esto permite a un usuario autenticado acceder a recursos privados de terceros mediante la iteración del parámetro `BasketId`.

#### Prueba de Concepto (PoC)

**Escenario de Ataque:**

1. **Línea Base:** El atacante identifica su propio carrito (`BasketId: 1`).
    
2. **Manipulación:** Se intercepta la petición y se modifica el identificador hacia el carrito de la víctima (`BasketId: 2`).
    
3. **Resultado:** El servidor entrega los datos de la víctima sin validar permisos.
    

_Evidencia 8: Comparativa - Acceso Legítimo vs. Acceso No Autorizado:_

**1. Acceso Legítimo (Control - ID 1):**
Se realiza una petición al carrito propio para establecer la línea base.
![IDOR Normal](../02_Technical_Evidence/03_IDOR/IDOR_01_Victim_Basket_Revealed.png)

**2. Acceso No Autorizado (Ataque - ID 2):**
Al modificar el ID en la URL, el servidor entrega los datos del carrito de otro usuario (Víctima) sin validar permisos.
![IDOR Victim](../02_Technical_Evidence/03_IDOR/IDOR_02_Victim_Basket_Revealed.png)

#### Recomendación Técnica

Implementar una capa de control de acceso (Middleware) que verifique la propiedad del recurso antes de devolver la respuesta: `if (User.id == Basket.owner_id)`.

## 3. Anexo: Plan de Remediación

Se adjunta evidencia de código seguro en el repositorio, demostrando la corrección de las vulnerabilidades halladas mediante dos enfoques: parches tácticos inmediatos y fortalecimiento estratégico de la arquitectura.

### 3.1 Parches Tácticos (Tactical Patches)
Soluciones puntuales aplicadas a los controladores vulnerables identificados.

* **SQL Injection:** [secure_login_fixed.js](../03_Remediation_Code/Tactical_Patches/secure_login_fixed.js)
* **XSS:** [fix_xss.js](../03_Remediation_Code/Tactical_Patches/fix_xss.js)
* **IDOR:** [fix_idor.js](../03_Remediation_Code/Tactical_Patches/fix_idor.js)

### 3.2 Defensa Estratégica (Strategic Defense)
Propuesta de arquitectura de seguridad para prevenir clases enteras de vulnerabilidades.

* **Defensa en Profundidad:** [security_architecture.js](../03_Remediation_Code/Strategic_Defense/security_architecture.js)

### 3.3 Referencia de Código Vulnerable
Se incluyen los snippets originales para facilitar la reproducción de los hallazgos en laboratorio.

* [vulnerable_login.js](../03_Remediation_Code/Vulnerable_Examples/vulnerable_login.js)
* [vulnerable_search.js](../03_Remediation_Code/Vulnerable_Examples/vulnerable_search.js)


