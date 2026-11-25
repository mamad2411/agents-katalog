<!--
LICENSE UPL
Author: Mauro Risonho de Paula Assumpção
Data Create: 2026-03-16
Data Update: 2026-03-16
-->

---
name: writeup-hczdmr
description: CTF writeups and security challenges by hczdmr.
---

# Writeups by hczdmr

Source repository: `/repos/hczdmr`

## Repository Index

- AI-based-automated-verification-for-pentest-reports/README.md

## Writeup Content


### File: AI-based-automated-verification-for-pentest-reports/README.md

<body>
<div class="container">

<h1>Doc-to-LLM Uyumlu Pentest Raporlama Standardı</h1>

<p>
Sızma testi (Pentest) raporları uzun yıllardır insan uzmanlar tarafından okunmak üzere tasarlanmaktadır.
Bu raporlar; teknik detay, anlatı, bağlam ve önerileri içeren serbest metin bloklarından oluşur.
Ancak büyük dil modellerinin (LLM) güvenlik doğrulama süreçlerinde kullanılmaya başlanmasıyla birlikte,
raporların yalnızca <span class="highlight">okunabilir</span> değil, aynı zamanda <span class="highlight">makine tarafından işlenebilir</span> olması kritik hale gelmiştir.
</p>

<p>
Bu doküman, pentest bulgularının LLM destekli otomatik doğrulama sistemlerine aktarılabilmesi için
standartlaştırılmış bir raporlama yapısı önermektedir.
Amaç, pentest çıktısını tek seferlik PDF belgesi olmaktan çıkararak,
sürekli çalıştırılabilir doğrulama kontrollerine dönüştürmektir.
</p>

<div class="section">
<h2>Mevcut Sorun</h2>

<p>
Geleneksel raporlama yaklaşımında bulgular genellikle paragraf formatında sunulur.
Aynı metin içinde:
</p>

<ul>
  <li>Zafiyetin mevcut durumu</li>
  <li>Teknik kanıt</li>
  <li>Düzeltme önerisi</li>
  <li>Örnek konfigürasyon</li>
</ul>

<p>
bir arada bulunur. Bu yapı, LLM tarafından kod üretimi sırasında bağlam karışıklığına yol açabilir.
Örneğin model, “eklenmelidir” ifadesini “mevcuttur” şeklinde yorumlayabilir veya
örnek konfigürasyonu canlı sistem çıktısı sanabilir.
</p>

<p>
Sonuç olarak:
</p>

<ul>
  <li>Yanlış doğrulama betikleri üretilebilir.</li>
  <li>Halüsinasyon riski artar.</li>
  <li>Yanlış pozitif sonuçlar oluşabilir.</li>
  <li>Pentest çıktıları süreklilik kazanamaz.</li>
</ul>
</div>

<div class="section">
<h2>Önerilen Çözüm: Yapılandırılmış Bulgu Kaydı</h2>

<p>
Her güvenlik bulgusu, doğrulama kodu üretimini doğrudan destekleyecek alanlara ayrıştırılmalıdır.
Bu yaklaşım, bulgunun yalnızca açıklanmasını değil, <span class="highlight">otomatik olarak yeniden test edilebilmesini</span> hedefler.
</p>

<p>Önerilen temel alanlar:</p>

<ul>
  <li><span class="highlight">Target:</span> URL veya IP adresi</li>
  <li><span class="highlight">Protocol ve Port:</span> Test edilecek servis bilgisi</li>
  <li><span class="highlight">Type & Category:</span> Zafiyet sınıflandırması</li>
  <li><span class="highlight">Severity:</span> Öncelik seviyesi</li>
  <li><span class="highlight">Request detayları:</span> HTTP method, headers, parametreler</li>
  <li><span class="highlight">Payload:</span> Zafiyeti tetikleyen veri</li>
  <li><span class="highlight">Expected Response:</span> Başarılı istismarı gösteren çıktı</li>
  <li><span class="highlight">Success Indicator:</span> Doğrulama kanıtı</li>
  <li><span class="highlight">False Positive Indicator:</span> Yanlış pozitifleri engelleyen kriter</li>
</ul>

<p>
Bu yapı sayesinde model, yorum yapmak yerine tanımlı parametreleri kullanarak doğrulama betiği üretir.
</p>
</div>

<div class="section">
<h2>Örnek Yapılandırılmış Bulgu</h2>

<pre>{
  "finding_id": "PT-2026-001",
  "title": "Eksik HTTP Security Header",
  "target": "https://example.com/",
  "protocol": "https",
  "port": 443,
  "type": "Security Misconfiguration",
  "severity": "Medium",

  "request": {
    "method": "GET",
    "path": "/"
  },

  "expected_response": {
    "status_code": 200,
    "must_contain_headers": ["Content-Security-Policy"]
  },

  "validation_success_indicator":
    "Header 'Content-Security-Policy' canlı yanıtta mevcut.",

  "validation_false_positive_indicator":
    "Header yalnızca dokümantasyon metninde geçiyor, canlı yanıtta yok."
}</pre>

<p class="small">
Bu yapı doğrudan doğrulama betiği üretimini destekler. LLM, hangi URL’ye hangi yöntemle
istek atacağını ve hangi çıktıyı kontrol edeceğini açık biçimde bilir.
</p>
</div>

<div class="section">
<h2>ROI ve Stratejik Etki</h2>

<p>
Bu yaklaşım yalnızca teknik doğruluk sağlamaz; aynı zamanda operasyonel verimlilik yaratır.
</p>

<ul>
  <li>Pentest çıktısı sürekli doğrulama mekanizmasına dönüşür.</li>
  <li>Düzeltildi sanılan zafiyetlerin geri dönmesi erkenden yakalanır.</li>
  <li>CI/CD ve CTEM süreçlerine doğal entegrasyon sağlanır.</li>
  <li>Daha düşük token tüketimi ile daha yüksek doğruluk elde edilir.</li>
</ul>

<p>
Pentest artık tek seferlik bir rapor değil,
sürekli çalışan bir güvenlik kontrol katmanı haline gelir.
</p>
</div>

<div class="section">
<h2>Sonuç</h2>

<p>
LLM çağında asıl dönüşüm modelde değil, veri yapısındadır.
Doc-to-LLM uyumlu raporlama yaklaşımı,
sızma testi raporlarını statik belgeler olmaktan çıkararak
otomatik ve sürekli güvenlik doğrulama sistemlerinin temel bileşeni haline getirir.
</p>

<p>
Pentest sona ermiyor; rapor formatı evriliyor.
</p>

</div>

</div>
</body>
</html>

