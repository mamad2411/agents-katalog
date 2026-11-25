---
name: expo-deployment
description: "Deploy apps Expo para produção"
risk: safe
source: "https://github.com/expo/skills/tree/main/plugins/expo-deployment"
date_added: "2026-02-27"
---

# Expo Deployment

## Visão Geral

Implante aplicações Expo em ambientes de produção, incluindo app stores e atualizações over-the-air.

## Quando Usar Esta Skill

Use esta skill quando precisar implantar apps Expo em produção.

Use esta skill quando:
- Implantar apps Expo em produção
- Publicar em app stores (iOS App Store, Google Play)
- Configurar atualizações over-the-air (OTA)
- Configurar definições de build para produção
- Gerenciar canais de release e versões

## Instruções

Esta skill fornece orientação para implantar apps Expo:

1. **Configuração de Build**: Configure definições de build para produção
2. **Submissão em App Store**: Prepare e envie para app stores
3. **Atualizações OTA**: Configure canais de atualização over-the-air
4. **Gerenciamento de Releases**: Gerencie versões e canais de release
5. **Otimização para Produção**: Otimize apps para produção

## Fluxo de Implantação

### Pré-Implantação

1. Certifique-se de que todos os testes passam
2. Atualize números de versão
3. Configure variáveis de ambiente para produção
4. Revise e otimize o tamanho do bundle do app
5. Teste builds de produção localmente

### Implantação em App Store

1. Crie binários de produção (iOS/Android)
2. Configure metadados da app store
3. Envie para App Store Connect / Google Play Console
4. Gerencie listagens da app store e screenshots
5. Trate o processo de revisão da app store

### Atualizações OTA

1. Configure canais de atualização (produção, staging, etc.)
2. Crie e publique atualizações
3. Gerencie estratégias de rollout
4. Monitore adoção de atualizações
5. Trate reversões se necessário

## Melhores Práticas

- Use EAS Build para builds de produção confiáveis
- Teste builds de produção antes da submissão
- Implemente rastreamento de erros e analytics apropriados
- Use canais de release para rollouts em etapas
- Mantenha metadados da app store atualizados
- Monitore o desempenho do app em produção

## Recursos

Para mais informações, consulte o [repositório de origem](https://github.com/expo/skills/tree/main/plugins/expo-deployment).