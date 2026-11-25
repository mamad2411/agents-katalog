---
name: fbf_list
description: Sadece acik (Open) buglari goster ve fix et. Triggers: /fbf_list
---

## Open Bug List

1. `~/Projects/flutter_feedback_kit/docs/dev_feedback_log.md` oku
2. Sadece **Open** tablosunu goster
3. Acik bug yoksa "Open issue yok" de
4. Kullanici sectiklerini fix et:
   - Kodu analiz et, kok nedeni bul
   - Comment belirsizse capture/screenshot'lara bak
   - Duzelt
   - `flutter analyze && flutter test` gecsin
   - Log'da Fixed'a tasi, commit hash ekle
