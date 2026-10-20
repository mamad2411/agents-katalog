## 1. Codebase İnceleme ve Arama Kuralı (ZORUNLU)

Kod tabanında herhangi bir arama veya inceleme yaparken **ÖNCE codebase-memory MCP araçlarını** kullanacaksın.

### Çalışma Sırası (İstisnasız):
1. **Geniş Arama:** Kod tabanında ilgili sembol, fonksiyon veya dosyayı taramak için ilk adım olarak `search_graph` çalıştır.
2. **Kod Okuma:** İlgili yeri tespit ettikten sonra `get_code_snippet` ile kodu oku.
3. **Bağlam Anlama:** Gerekirse `trace_path` veya `get_architecture` ile bağlantıları analiz et.
4. **Değişiklik:** Kod değişikliğini ancak bu adımları tamamladıktan sonra yap.

### YASAKLAR:
- Klasik `grep`, `find` veya dosya dosya manuel gezerek kod aramak YASAKTIR.
- Dosya yollarını tahmin ederek iş yapamazsın.

### Manuel Aramaya Geçiş (Fallback):
Sadece aşağıdaki durumlar gerçekleşirse standart arama araçlarını (`grep`, `bash` vb.) kullanabilirsin:
- MCP aracı hata verirse veya 0 sonuç döndürürse (Bu durumda manuel aramaya geçip işine devam et, kullanıcıya sormakla zaman tasarruf et).
- `.env`, `Dockerfile`, build çıktıları veya log dosyalarını incelerken.

---

## 2. İş Bitimi Kapanış Protokolü (Session End)

Verilen görevi tamamladığında ajanı kapatmadan veya yeni göreve geçmeden önce ZORUNLU olarak:

1. **Hafızayı Güncelle:** `memory-bank/` klasöründeki takip dosyalarını (`activeContext.md`, `progress.md`) son durumla güncelle.
2. **Yerel Kayıt (Commit):** Yaptığın değişiklikleri özetleyen kısa ve net bir commit mesajı at:
   ```bash
   git add -A
   git commit -m "feat: [yapılan işin kısa özeti]"
   ```
3. **Push:** Commit'i uzak depoya gönder:
   ```bash
   git push
   ```

Bu adımlar agent kapatılmadan veya yeni task'a geçilmeden ÖNCE yapılmalıdır.
