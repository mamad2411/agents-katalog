---
name: fbf_list_fixed
description: Feedback bug listesini goster — fixed dahil. Arguman verilirse son N kaydi goster. Triggers: /fbf_list_fixed
argument-hint: "[N — son kaç kayıt]"
---

## Feedback Full List

1. `~/Projects/flutter_feedback_kit/docs/dev_feedback_log.md` oku
2. **Arguman yoksa:** Fixed + Open tablolarin tamamini goster
3. **Arguman varsa (ornegin `10`):** Fixed tablosunun son N satirini goster (en yeniden eskiye)
4. Kullaniciya sor: hangileri yeniden incelensin veya fix edilsin?
5. Sectiklerini sirayla isle:
   - Kodu analiz et, kok nedeni bul
   - Comment belirsizse capture/screenshot'lara bak
   - Duzelt
   - `flutter analyze && flutter test` gecsin
   - Log'u guncelle
