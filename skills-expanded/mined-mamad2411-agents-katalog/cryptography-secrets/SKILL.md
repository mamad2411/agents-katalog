---
name: cryptography-secrets
description: "Criptografía y gestión de secretos generalista. Cubre algoritmos simétricos/asimétricos, hashing, PKI, TLS/SSL, key management, HSM, y gestión de secretos (Vault, rotation, injection). Actívala al diseñar cifrado, gestionar credenciales o auditar implementaciones criptográficas."
disable-model-invocation: true
---

# Criptografía y Gestión de Secretos

Guía de criptografía práctica y gestión de credenciales. No implementar algoritmos propios; usar bibliotecas auditadas.

---

## Principios fundamentales

1. **No inventar criptografía propia**: Usar bibliotecas estándar (OpenSSL, libsodium, BouncyCastle, .NET System.Security.Cryptography, Java JCA)
2. **No obfuscar como seguridad**: La seguridad reside en la clave, no en el algoritmo secreto
3. **Defense in depth**: Cifrado + control de acceso + audit logging
4. **Fail secure**: Si el cifrado falla, los datos deben permanecer inaccesibles

---

## Algoritmos recomendados (2026)

### Simétricos

| Uso | Algoritmo | Modo | Tamaño de clave | Notas |
|-----|-----------|------|-----------------|-------|
| Cifrado de datos | AES | GCM o ChaCha20-Poly1305 | 256 bits | GCM: no reusar nonce con misma clave |
| Cifrado de archivos grandes | AES | GCM con streaming | 256 bits | Chunked encryption con nonces incrementales |
| Alternativa moderna | ChaCha20-Poly1305 | AEAD | 256 bits | Preferir en mobile/ARM sin AES-NI |

### Asimétricos

| Uso | Algoritmo | Tamaño de clave | Notas |
|-----|-----------|-----------------|-------|
| Key exchange | ECDH (Curve25519, P-256) | 256 bits | Forward secrecy |
| Firmas digitales | ECDSA (P-256, P-384) o Ed25519 | 256-384 bits | Ed25519: determinista, más rápido |
| RSA legacy | RSA-OAEP / RSA-PSS | 3072+ bits | Solo para compatibilidad |

### Hashing

| Uso | Algoritmo | Notas |
|-----|-----------|-------|
| Passwords | Argon2id (winner PHC) | Memory-hard, configurable |
| Passwords legacy | scrypt, bcrypt, PBKDF2 | Migrar a Argon2id |
| **NUNCA** | MD5, SHA1 | Rotos, solo para checksums no seguros |
| Integridad de datos | SHA-256, SHA-3 | HMAC-SHA-256 para autenticación |

### Evitar
- DES, 3DES, RC4, Blowfish
- ECB mode (Electronic Codebook)
- CBC sin HMAC (padding oracle attacks)
- MD5, SHA1 para seguridad
- RSA sin OAEP/PSS padding
- Curvas no estándar (brainpool raro, curvas custom)

---

## Cifrado de datos

### At rest
```
1. Clasificar datos: público, interno, confidencial, restringido
2. Cifrar restringido/confidencial obligatoriamente
3. Usar AES-256-GCM con clave gestionada por KMS/HSM
4. Separar DEK (Data Encryption Key) de KEK (Key Encryption Key)
   - DEK cifra los datos
   - KEK cifra la DEK (envelope encryption)
   - KEK nunca sale del HSM/KMS
5. Rotación de DEK periódica (re-cifrar datos)
6. Rotación de KEK: re-cifrar DEKs, no datos completos
```

### In transit
```
1. TLS 1.3 obligatorio para tráfico externo
2. mTLS para servicio-a-servicio
3. Certificate pinning para mobile (con fallback)
4. No aceptar certificados autofirmados en producción
5. OCSP stapling para revocación
```

### En uso (confidential computing)
- TEE (Trusted Execution Environment): Intel SGX, AMD SEV, ARM TrustZone
- Homomorphic encryption (cuando el rendimiento lo permita)
- Memory encryption

---

## PKI (Public Key Infrastructure)

### Componentes
- **CA (Certificate Authority)**: Emite y firma certificados
- **RA (Registration Authority)**: Valida identidades antes de emitir
- **VA (Validation Authority)**: Verifica validez (OCSP, CRL)
- **End-entity**: El certificado del servidor/usuario

### Mejores prácticas
- Usar certificados de 2048+ bits (RSA) o 256+ bits (ECC)
- Vida útil corta: 90 días (Let's Encrypt) o 1 año máximo
- Automatizar emisión y renovación (ACME protocol)
- Private CA para interno (HashiCorp Vault, AWS PCA, AD CS)
- Certificate Transparency (CT) logs para monitoreo
- Revocación: OCSP preferido sobre CRL

### Certificado perfecto
```
Subject: CN=api.example.com
SAN: DNS:api.example.com, DNS:api-east.example.com
Key Usage: Digital Signature, Key Encipherment
Extended Key Usage: Server Authentication
Signature Algorithm: ecdsa-with-SHA256
Valid: 90 days
CA: False
```

---

## Gestión de Secretos

### Ciclo de vida
```
1. Creación: CSPRNG, nunca hardcodeado
2. Distribución: Inyectado por secret manager, no en repos
3. Uso: En memoria, no en logs, no en variables de entorno si es posible
4. Rotación: Automática periódica o bajo demanda
5. Revocación: Inmediata en caso de compromiso
6. Auditoría: Quién accedió, cuándo, desde dónde
```

### Secret Managers

| Solución | Tipo | Ideal para |
|----------|------|------------|
| HashiCorp Vault | Enterprise / Cloud-agnostic | Multi-cloud, PKI, dynamic secrets |
| AWS Secrets Manager | Cloud-native | AWS workloads, rotación automática RDS |
| Azure Key Vault | Cloud-native | Azure, HSM, certificates |
| Google Secret Manager | Cloud-native | GCP workloads |
| Doppler / 1Password Secrets | SaaS | Equipos pequeños, multi-cloud |
| Kubernetes External Secrets | K8s | Inyectar secrets de cloud a pods |

### Anti-patrones
```
❌ Secretos en código fuente (nunca, ni en repos privados)
❌ .env files en producción sin cifrado
❌ Pasar secrets por CLI args (visibles en ps/process list)
❌ Secrets en logs o error messages
❌ Compartir credenciales entre equipos/servicios
❌ Sin rotación: misma clave por años
```

### Patrón de inyección
```
1. App arranca sin secrets
2. Se autentica con el secret manager (managed identity, IAM role, K8s SA)
3. Lee secrets en runtime
4. Cachea en memoria con TTL corto
5. Refresca antes de expiración
6. Nunca persiste en disco
```

---

## Key Management

### Jerarquía de claves
```
Root Key (HSM, offline, split knowledge)
    └── KEK (Key Encryption Key, en HSM)
            └── DEK (Data Encryption Key, por dataset)
                    └── Datos cifrados
```

### Rotación
| Tipo | Frecuencia | Método |
|------|------------|--------|
| KEK | Anual o bajo sospecha | Re-cifrar DEKs |
| DEK | Trimestral o por volumen | Re-cifrar datos |
| JWT signing key | Cada rotación de deployment | JWKs endpoint con múltiples keys |
| API Keys | Cada 90 días o evento de seguridad | Grace period con dual-key |
| Passwords salting | N/A (único por usuario) | Argon2id por login |

### HSM (Hardware Security Module)
- FIPS 140-2 Level 3+ para compliance estricto
- Cloud HSM: AWS CloudHSM, Azure Dedicated HSM, Google Cloud HSM
- Usar para: KEK storage, firma de certificados, signing keys críticas

---

## TLS/SSL Configuration

### TLS 1.3 (obligatorio)
- Suites: TLS_AES_256_GCM_SHA384, TLS_CHACHA20_POLY1305_SHA256
- No TLS 1.0, 1.1 (deprecated)
- TLS 1.2 solo para compatibilidad legacy con suites seguras

### Certificate validation
- Verify hostname matches SAN
- Verify chain to trusted root
- Verify not expired
- Verify not revoked (OCSP)
- Pinning para mobile (con backup pin)

---

## Checklist de criptografía

- [ ] Algoritmos auditados y modernos (AES-256-GCM, ChaCha20, Argon2id, ECDSA)
- [ ] No algoritmos legacy (MD5, SHA1, DES, RC4, RSA sin padding)
- [ ] Cifrado at rest para datos confidenciales/restringidos
- [ ] TLS 1.3 para todo tráfico externo
- [ ] mTLS para comunicación interna
- [ ] Secret manager en uso; sin secrets en código
- [ ] Rotación automática de credenciales
- [ ] DEK/KEK separation (envelope encryption)
- [ ] HSM o Cloud KMS para KEK críticas
- [ ] Password hashing con Argon2id (o scrypt/bcrypt)
- [ ] Nonces únicos por operación en AEAD
- [ ] Certificate lifecycle automatizado (emisión, renovación, revocación)
- [ ] Auditoría de acceso a claves y secretos
