---
name: email-indonesia
description: "Email Indonesia: kirim email otomatis, SMTP Gmail/Outlook, newsletter, blast email, autoresponder, template email HTML, email marketing UMKM, mailbox, SPF DKIM DMARC. | EN: send email smtp gmail outlook newsletter automation autoresponder marketing"
version: 1.0.0
category: productivity-automator
lang: id
---

# Email Indonesia

## Kirim email otomatis
- **SMTP langsung**: Gmail `smtp.gmail.com:587` (butuh App Password, bukan password biasa), Outlook `smtp.office365.com:587`.
- **API**: Gmail API, SendGrid, Mailgun, Resend — lebih andal untuk volume.
- **Library**: Python `smtplib`+`email.mime`, Node `nodemailer`, bash `curl` ke API.

## Email marketing/UMKM
- Newsletter: kumpulkan subscriber → segmentasi → kirim terjadwal (Mailchimp free, Brevo, MailerLite).
- Template HTML: header brand, CTA jelas, mobile-responsive, footer unsubscribe wajib (UU PDP & anti-spam).
- Timing: Selasa-Kamis pagi Indonesia terbuka lebih tinggi.

## Deliverability
- SPF, DKIM, DMARC wajib untuk domain sendiri — tanpa ini masuk spam.
- Jangan blast dari SMTP pribadi; pakai layanan transactional.

## Autoresponder
- Welcome email, invoice otomatis, reminder booking, notifikasi order marketplace.

## Tip
- Batch kirim max ~500/hari dari SMTP biasa; lebih dari itu pakai ESP.
- Personalisasi {nama} menaikkan open rate signifikan.
- ID keywords: kirim email, email otomatis, kirim pesan, blast, newsletter, smtp, gmail, outlook, autoresponder, template email.