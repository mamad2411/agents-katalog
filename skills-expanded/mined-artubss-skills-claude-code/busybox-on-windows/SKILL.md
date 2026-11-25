---
name: busybox-on-windows
description: Como usar um build Win32 do BusyBox para executar muitas das ferramentas de linha de comando UNIX padrão no Windows.
license: MIT
---

BusyBox é um único binário que implementa muitas ferramentas UNIX comuns.

Use esta skill apenas no Windows. Se você estiver em UNIX, pare aqui.

Execute as seguintes etapas apenas se não conseguir encontrar um arquivo `busybox.exe` no mesmo diretório deste documento.
Estes são comandos PowerShell. Se você tiver um terminal clássico `cmd.exe`, deve usar `powershell -Command "..."` para executá-los.
1. Imprima o tipo de CPU: `Get-CimInstance -ClassName Win32_Processor | Select-Object Name, NumberOfCores, MaxClockSpeed`
2. Imprima as versões do SO: `Get-ItemProperty "HKLM:\SOFTWARE\Microsoft\Windows NT\CurrentVersion" | Select-Object ProductName, DisplayVersion, CurrentBuild`
3. Baixe um build adequado do BusyBox executando um destes comandos PowerShell:
   - 32-bit x86 (ANSI): `$ProgressPreference = 'SilentlyContinue'; Invoke-WebRequest -Uri https://frippery.org/files/busybox/busybox.exe -OutFile busybox.exe`
   - 64-bit x86 (ANSI): `$ProgressPreference = 'SilentlyContinue'; Invoke-WebRequest -Uri https://frippery.org/files/busybox/busybox64.exe -OutFile busybox.exe`
   - 64-bit x86 (Unicode): `$ProgressPreference = 'SilentlyContinue'; Invoke-WebRequest -Uri https://frippery.org/files/busybox/busybox64u.exe -OutFile busybox.exe`
   - 64-bit ARM (Unicode): `$ProgressPreference = 'SilentlyContinue'; Invoke-WebRequest -Uri https://frippery.org/files/busybox/busybox64a.exe -OutFile busybox.exe`

Comandos úteis:
- Ajuda: `busybox.exe --list`
- Comandos UNIX disponíveis: `busybox.exe --list`

Uso: Prefixe o comando UNIX com `busybox.exe`, por exemplo: `busybox.exe ls -1`

Se você precisar executar um comando UNIX em outro CWD, use o caminho absoluto para `busybox.exe`.

Documentação: https://frippery.org/busybox/
BusyBox original: https://busybox.net/