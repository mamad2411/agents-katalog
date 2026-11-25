---
name: corno-limpa
description: Libera espaço em disco com segurança no macOS, Windows ou Linux, como uma limpeza completa de sistema - varre tudo sem apagar nada, mostra a prévia por categoria com quanto dá para liberar (caches, logs, dependências, builds, simuladores, emuladores, modelos de IA, sobras de apps desinstalados, instaladores esquecidos, arquivos grandes parados), limpa o que volta sozinho com uma confirmação só e pede decisão para o que é pessoal ou insubstituível. Identifica o que se baixa de novo sozinho e desliga antes de apagar, confere o git antes de tocar em código, respeita uma lista de protegidos e guarda o histórico do que apagou. Use quando disserem "disco cheio", "pouco espaço", "o que posso apagar", "limpa meu computador", "libera espaço", "System Data enorme", "o C: está cheio", "disk full", "free up space", mesmo que citem uma pasta só.
---

# Corno limpa

Liberar espaço sem perder nada que a pessoa sentiria falta. Quase tudo que enche o disco de quem programa volta sozinho (dependências, builds, caches, simuladores mortos, modelos baixados). O difícil é a fração que não volta: código sem commit, chaves, fotos, documentos únicos. O fluxo existe para separar uma coisa da outra antes de apagar.

## Regras

- **Mede antes de propor.** Rode o scan primeiro. Com tamanhos na frente a pessoa decide melhor, e o maior item quase nunca é o que ela chutou.
  - macOS e Linux: `bash scripts/scan.sh`
  - Windows: `powershell -ExecutionPolicy Bypass -File scripts/scan.ps1`
  - Pastas de código (qualquer sistema; no Windows via Git Bash): `bash scripts/find-build-dirs.sh <raiz-do-código>`
- **Dois baldes.** *Volta sozinho* (reinstalar, recompilar ou baixar de novo traz de volta): uma confirmação para o balde inteiro, com a opção de tirar categorias. *Seu* (documentos, fotos, chaves, trabalho sem commit, dumps, instaladores, arquivos grandes parados): decisão da pessoa, grupo a grupo.
- **Olha o alvo antes de apagar.** Espie arquivos desconhecidos (`head`, `pdftotext -l 1`, `unzip -l`, `file`) em vez de julgar pelo nome. Um `asdsad.pdf` era nota fiscal duplicada; uma pasta com cara de clone velho era a única cópia de um protótipo.
- **Lixeira para arquivo pessoal, apagar direto para cache.** Arquivo pessoal vai para a lixeira, para poder voltar:
  - macOS 14+: `trash <arquivos>`
  - Linux: `gio trash <arquivos>`
  - Windows: `Add-Type -AssemblyName Microsoft.VisualBasic; [Microsoft.VisualBasic.FileIO.FileSystem]::DeleteFile('<arquivo>','OnlyErrorDialogs','SendToRecycleBin')`

  Mandar 80 GB de `node_modules` para a lixeira não libera nada até esvaziar, então regenerável se apaga direto (`rm -rf`, `Remove-Item -Recurse -Force`).
- **Git antes de código.** Nunca apague repo, worktree ou branch sem rodar `scripts/git-audit.sh` nele. Veja `references/codigo.md`.
- **Fecha o app antes de apagar os dados dele.** Confira se está rodando (`pgrep -f '<App>'`, `Get-Process <nome>`). Se estiver, pule e entregue o comando de uma linha para rodar depois de fechar.
- **Bloqueia o que se baixa de novo.** Alguns itens voltam sozinhos se você só apagar: modelos de IA que navegadores e apps baixam por conta própria, atualizações baixadas e não instaladas. O scan identifica esses itens; desligue o recurso primeiro, depois apague. Veja `references/navegadores-e-ia.md`.
- **Relata com números.** Anote o espaço livre antes e depois de cada rodada e diga quanto liberou.
- **Protegidos e histórico.** Antes de propor, leia `~/.config/corno-limpa/protegidos.txt` (Windows: `%APPDATA%\corno-limpa\protegidos.txt`), um caminho por linha, e nunca proponha nada dentro deles. Quando a pessoa disser "nunca mexe nisso", acrescente a linha. Cada remoção vai para `historico.tsv` na mesma pasta: data, tamanho, caminho e se foi apagado ou para a lixeira.
- **Admin só com aviso.** Limpezas que pedem `sudo` ou prompt elevado (journal, cache do apt, Windows Update, `DISM`) são opcionais. Explique o que fazem e entregue o comando, ou rode só se a pessoa autorizar.

## Pedindo decisões

Use a ferramenta de pergunta estruturada se o ambiente tiver uma (no Claude Code: `AskUserQuestion`); senão pergunte direto e espere. Junte 3 ou 4 decisões por vez. A opção recomendada vem primeiro, com "(Recomendado)" no rótulo, e a descrição de cada opção diz o que acontece de verdade: quanto libera, o que se perde, o que precisa reinstalar.

Para grupos de arquivos que a pessoa precisa ver (prints, fotos, vídeos), **separe em pastas**: mova cada grupo para `~/Downloads/_revisar/<n>-<categoria>/`, abra as pastas (`open`, `xdg-open`, `explorer`) e pergunte por grupo: *Apagar tudo* / *Vou arrastar o que fica* / *Manter tudo*. Mover é reversível e a pessoa vê miniaturas em vez de nomes. No fim, remova `_revisar`.

## Fluxo

1. **Varredura completa, sem apagar nada.** Espaço livre, o scan geral, `find-build-dirs.sh` nas pastas de código e `docker system df` se houver Docker. Não pergunte antes qual área limpar: varra tudo, como uma prévia.
2. **Prévia por categoria.** Uma tabela só, com tamanho, balde e o que acontece se apagar, nesta ordem quando houver:
   - Sistema e logs
   - Caches de apps
   - Navegadores e modelos de IA baixados por apps
   - Nuvem e Office
   - Ferramentas de dev: dependências, builds, simuladores, emuladores, SDKs, caches de pacote
   - Virtualização e containers
   - Sobras de apps desinstalados
   - Backups de aparelho e firmware
   - Instaladores esquecidos
   - Arquivos grandes parados
   - Lixeira

   No topo, o resumo: "Dá para liberar X GB sem perder nada. Mais Y GB dependem de você." Marque o que se baixa de novo sozinho se não for desligado.
3. **Uma confirmação para o que volta sozinho**: *Limpar tudo que volta sozinho (Recomendado)* / *Escolher categorias* / *Só me mostra os comandos*.
4. **Limpa** cada categoria com o arquivo de referência dela, pulando app aberto e protegido:
   - Downloads e pastas pessoais: `references/pastas-pessoais.md`
   - Pastas de código, repos, worktrees, dumps: `references/codigo.md`
   - Simuladores, emuladores, SDKs, caches de pacote, VMs e containers: `references/ferramentas-dev.md`
   - Navegadores, modelos de IA, apps Electron, modelos locais, CLIs e apps de agente: `references/navegadores-e-ia.md`
   - Sistema operacional, sobras de apps, firmware e backups: `references/sistema-mac.md`, `references/sistema-windows.md` ou `references/sistema-linux.md`
5. **Decide o que é seu**, grupo a grupo, como em "Pedindo decisões".
6. **Confere** que cada remoção liberou espaço mesmo (vários comandos fazem menos do que o nome promete) e mede de novo.
7. **Fecha.** Antes e depois em números, o que foi apagado, o que ficou e por quê, e o que a pessoa precisa fazer a seguir (instalar dependências antes do próximo build, baixar um runtime de simulador, esvaziar a lixeira). Aponte problemas de segurança achados no caminho (chaves soltas, credenciais em README, dump de produção com dados pessoais) sem imprimir o conteúdo.

## Nunca mexa

- Bibliotecas de fotos por dentro (`Photos Library.photoslibrary`, bancos do Lightroom). Apagar lá dentro corrompe a biblioteca. Se for grande, a saída é mover inteira para um disco externo.
- Chaveiros e cofres de senha (`~/Library/Keychains`, `~/.local/share/keyrings`, Credential Manager), Mail, Messages e pastas sincronizadas por nuvem (iCloud Drive, OneDrive, Dropbox, Google Drive). Apague pelos próprios apps, se for o caso.
- Pastas do sistema fora da home, exceto os caminhos documentados nas referências de sistema. No Windows, nunca `C:\Windows\WinSxS`, `C:\Windows\Installer` ou `C:\ProgramData\Package Cache` na mão: quebra atualização e desinstalação.
- `pagefile.sys` e `swapfile`. O sistema gerencia.
- Qualquer coisa com trabalho sem commit ou sem push, a menos que a pessoa confirme depois de ver o audit.

## Segredos achados durante a limpeza

Chaves e credenciais (`.env*`, `*.pem`, `*.p8`, `*.p12`, JSON de service account, client secrets OAuth, `google-services.json`, códigos de backup, kits de recuperação de gerenciador de senha) não são lixo, mas não devem ficar soltos em Downloads. Ofereça mover para uma pasta privada que a pessoa já usa (por exemplo `~/.private_keys/<data>/`, com `chmod 700` na pasta e `600` em cada arquivo; no Windows, uma pasta só do usuário). Nunca imprima o conteúdo. Para classificar, procure só a estrutura (por exemplo `"type": "service_account"`). Sugira levar códigos de recuperação para um gerenciador de senha.
