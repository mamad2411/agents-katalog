# Tarım Pazaryeri Projesi - AI Geliştirici Kuralları

Ben bir Frontend geliştiriciyim, React biliyorum. Bu proje; üreticilerin sebze, meyve, fide, fidan, çiçek, süt ve yumurta ilanları verebileceği, modern tasarımlı ve yapay zeka destekli bir pazaryeri platformudur.

## 1. Temel Teknoloji Yığını (Tech Stack)
- **Frontend:** Next.js (App Router), TypeScript, Tailwind CSS, Shadcn UI
- **Backend / Veritabanı:** Supabase (veya Prisma + PostgreSQL), Next.js API Routes
- **Yapay Zeka (AI):** Google Gemini API (Google AI SDK / @google/genai)

## 2. Yapay Zeka (Gemini) Entegrasyon Öncelikleri
- Projede yapay zeka çözümleri için **SADECE Google Gemini API** ve Google servisleri kullanılacaktır. OpenAI, Anthropic vb. alternatifleri önerme.
- Kullanıcıların mevsimsel tarım soruları (Örn: "Biber ne zaman ekilir?") ve 12 aylık dinamik ekim/dikim takvimi için Gemini API entegrasyonuna uygun mimariler tasarla.
- Yapay zeka aramaları ve chatbot özellikleri için Next.js API route'ları üzerinden güvenli ve optimize edilmiş Gemini API çağrıları kurgula. API anahtarlarını (`process.env.GEMINI_API_KEY`) güvenli yönet.

## 3. Kodlama Standartları ve UI/UX
- Tüm bileşenleri **Next.js App Router** yapısına (`app/` klasörü) uygun ve TypeScript kullanarak yaz.
- Tasarımlarda modern, temiz, scannable (taranabilir) ve mobil uyumlu (responsive) **Tailwind CSS** kullan. Bileşen kütüphanesi olarak **Shadcn UI** pratiklerini benimse.
- Veritabanı işlemlerinde ilişkisel modeli (Üretici -> İlan -> Mesajlaşma) gözeterek sürdürülebilir SQL veya Prisma şemaları öner.
- Kodları parça parça ve eksiksiz ver. Büyük kod bloklarında `// ... eski kodlar buraya` diyerek geçiştirme, entegrasyon noktalarını net göster.

## 4. İletişim ve Dil
- Tüm kod açıklamalarını, yorum satırlarını ve sohbet yanıtlarını **Türkçe** olarak yap.
- Bana sadece kod verme; o kodu Next.js yapısında hangi klasöre koymam gerektiğini ve neden bu yöntemi seçtiğimizi kısa ve net bir şekilde açıkla.©