---
name: instagram-content-calendar-gr
description: A ready-to-paste Greek-language meta-prompt that makes ChatGPT or Claude interview the user about their business, then generate a 30-day Instagram content calendar (one table row per post, with caption structure and AI-image instructions). Use when the user asks for a μηνιαίο πλάνο περιεχομένου / content calendar for Instagram in Greek, or wants a reusable prompt to regenerate that calendar every month.
---

# Instagram 30-Day Content Calendar (Greek meta-prompt)

Source: "30 μέρες content με ένα prompt" carousel (@wedohype / Andreas).
Original terms and the prompt itself are kept in Greek, as written — this
is a prompt meant to be pasted verbatim into ChatGPT or Claude, not a
skill to translate.

## How it works

The meta-prompt has six parts. Part 6 tells the model to ask its own
clarifying questions *before* writing anything, so the calendar comes out
built from the user's real business details instead of placeholders. Give
the model the whole block below in one message; it will ask the questions
in Part 2, then produce the table from Part 4 once answered.

## The prompt (copy-paste as-is)

```
Είσαι ένας ειδικός στη στρατηγική social media και στη δημιουργία
περιεχομένου. Στόχος σου είναι να δημιουργήσεις ένα ημερολόγιο
περιεχομένου 30 ημερών για το Instagram για την επιχείρησή μου, με
ισορροπία ανάμεσα στο branding και τις πωλήσεις. Ακολούθησε τα παρακάτω
βήματα:

ΣΧΕΤΙΚΑ ΜΕ ΤΗΝ ΕΠΙΧΕΙΡΗΣΗ ΜΟΥ
Η επιχείρησή μου λέγεται Χ και πουλάω την υπηρεσία/προϊόν Υ. Το κοινό μου
είναι Ζ αλλά θέλω τη βοήθειά σου σε αυτό για να απευθυνθώ και σε άλλα
κοινά. Τα ενδιαφέροντα του κοινού μου είναι [αυτά].
Το πρόβλημα που τους λύνω είναι [αυτό] αλλά βοήθησέ με να βρω κι άλλα
προβλήματα που λύνω και δεν το γνωρίζω ακόμα.
Ο τόνος φωνής που θέλω να έχω είναι [στυλ] (π.χ. παιχνιδιάρικο,
πολυτελές, μινιμαλιστικό)
Οι ανταγωνιστές μου είναι οι [ανταγωνιστές]

ΣΤΡΑΤΗΓΙΚΗ
Για τη στρατηγική και το περιεχόμενο θέλω:
Χ συχνότητα (π.χ. 5 φορές την εβδομάδα).
Δημοσίευση με βάση αυτούς τους πυλώνες περιεχομένου (παραδείγματα):
Ψυχαγωγία & Αλληλεπίδραση (αστεία videos, quiz, backstage)
Εκπαίδευση & Έμπνευση (tips, ιστορίες πελατών, facts)
Προώθηση & Πωλήσεις (παρουσίαση προϊόντων, προσφορές, testimonials)
Θέλω την εξής ισορροπία (π.χ. 40% engagement, 30% εκπαίδευση, 30%
πώληση).

ΜΟΡΦΗ
Τα θέλω στην εξής μορφή:
Παρουσίασε έναν πίνακα με μία γραμμή για κάθε δημοσίευση, με τρεις
στήλες:
Ημερομηνία & Ημέρα (π.χ. «5 Μαΐου, Δευτέρα»)
Κείμενο Caption (hook, κύριο μέρος, call-to-action, σχετικά hashtags)
Οδηγίες Εικόνας
Προτεινόμενο Οπτικό (σύντομη περιγραφή φωτογραφίας ή γραφικού)
Prompt για AI-Εικόνα (αν χρειάζεται):
Περιγραφή Σκηνής (τι θέλουμε να δείχνει)
3 Λέξεις Στυλ (π.χ. «οργανικό», «φωτεινό», «φυσικό φως»)

ΠΡΟΣΘΕΤΕΣ ΟΔΗΓΙΕΣ
Θέλω ποικιλία από: στατικές εικόνες, carousel, Reels, Stories ή σύντομα
βίντεο. Τουλάχιστον ένα interactive στοιχείο την εβδομάδα (poll, quiz,
sticker ερωτήσεων). Πρόσθεσε μια εβδομαδιαία bonus ιδέα για Story
highlight ή συνεργασία.

ΕΚΤΕΛΕΣΗ
Πρώτα κάνε μου τις απαραίτητες ερωτήσεις για την επιχείρησή μου.
Μόλις συγκεντρωθούν οι πληροφορίες, παρέθεσε το ημερολόγιο 30 ημερών
όπως περιγράφεται.
```

## Where this fits vs. this repo's other content-planning skills

- **content-strategy**: the English-language, deeper strategic skill
  (pillars, topic clusters, keyword-by-buyer-stage). This meta-prompt is a
  lighter, single-shot, Greek-language tool for a monthly Instagram
  calendar specifically — reach for `content-strategy` when the request
  is broader than one platform or one month.
- **caption-writer** / **carousel-writer** / **hook-writer**: once this
  calendar names a post's pillar and format, hand the actual caption or
  carousel copy to those skills instead of writing it inline here.
- Keep the prompt's placeholders (`Χ`, `Υ`, `Ζ`, `[αυτά]`, etc.) — they are
  what makes Part 6's clarifying-questions step work. Filling them in
  before handing the prompt to the model defeats that step.

## Notes

Rerun this prompt at the start of each month (Part 6's own instruction:
"Κράτα το για την αρχή κάθε μήνα"). The business-specific answers from a
previous run can be pasted back in to skip the interview on repeat runs.
