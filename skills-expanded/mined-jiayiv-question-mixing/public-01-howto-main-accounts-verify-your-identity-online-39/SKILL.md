---
name: verify-your-identity-online
domain: accounts
locale: [generic]
interface: mixed
difficulty: intermediate
est_time: 30min
risk: high
prerequisites: []
status: draft
last_verified: 2026-07-21
---

## Goal

Complete an online identity verification request while limiting the chance of sending identity documents to the wrong party.

## Preconditions

- You know why verification is being requested and which account or application it belongs to.
- You have the requested identity document, such as passport, driver's license, national ID, or residence permit.
- Your device camera works and the browser or app has camera permission.
- You are on the official website or app, not a link from an unexpected message.

## Steps

1. **Confirm the request is legitimate.** Navigate to the service from a bookmark or typed address and look for the same verification notice after signing in. → *Expect:* the verification prompt appears inside the official account.
2. **Read what they need.** Check the document types, country rules, selfie or liveness requirement, and review time. → *Expect:* you know exactly which document and photos are required.
3. **Prepare the document.** Use an unexpired ID, remove it from sleeves, and place it on a plain surface with good light. → *Expect:* all edges and text are visible to your eye.
4. **Reduce unrelated exposure.** Cover nearby papers, close other tabs, and turn off screen sharing. → *Expect:* only the verification page and ID are visible.
5. **Start the upload inside the official flow.** Choose the correct issuing country and document type. → *Expect:* the form asks for front, back, passport page, or camera capture as appropriate.
6. **Capture the ID clearly.** Take the photo straight on, without glare, blur, cut-off corners, or fingers over text. → *Expect:* the preview is sharp enough to read the name, birth date, document number, and expiration date.
7. **Complete the liveness selfie.** Follow the prompt to look at the camera, turn your head, blink, or record a short video if required. → *Expect:* the app accepts the selfie capture without a retry warning.
8. **Review before submitting.** Confirm the service name, account email, document images, and privacy notice are still the expected ones. → *Expect:* the final submit button belongs to the same official flow.
9. **Submit the verification.** Send the documents only after confirming the destination. ⚠️ *Irreversible:* identity documents cannot be made secret again once uploaded, so stop if the site or request looks wrong. → *Expect:* the service shows a submitted, pending, or under review status.
10. **Save the receipt.** Record the case number, timestamp, and official sender address for follow-up. → *Expect:* you can find the submission record without reopening the upload page.
11. **Watch for the result.** Check the account status and inbox over the stated review window. → *Expect:* the service either approves, rejects with a reason, or asks for a specific retry.
12. **Delete local temporary copies.** Remove ID photos from downloads, desktop, camera roll, and trash if you created them outside the secure capture flow. → *Expect:* no loose identity-document images remain on the device.

## Decision points

- The request came from an email or text → verify by signing in independently before clicking anything.
- The service asks for more data than expected → pause and check the official help page or support channel.
- The ID is expired → use another accepted document or renew before submitting.
- You are uncomfortable with retention terms → decide whether the account or transaction is worth completing.

## Failure modes & recovery

- **F1 Blurry ID rejected:** detect a rejection for unreadable document, recover by retaking in brighter indirect light with all corners visible.
- **F2 Liveness fails:** detect repeated selfie failures, recover by cleaning the camera, removing hats or sunglasses, and using a different device.
- **F3 Wrong official flow:** detect a domain mismatch or unexpected payment request, recover by closing the page and reporting phishing to the service.
- **F4 Name mismatch:** detect rejection because account name differs from ID, recover by updating account profile or providing the requested supporting document.
- **F5 Review stalls:** detect no status change after the stated window, recover with the case number through official support.

## Verification

The official account status shows identity verified, or the service provides a dated pending case number tied to the correct account and document submission.

## Variations

- Financial service: additional tax ID, address, or source-of-funds questions may be required.
- Age-restricted service: the flow may verify age without storing a full ID image, depending on provider.
- Mobile app: camera capture may be mandatory and uploads from files may be blocked.
- Business account: beneficial-owner documents and company registration records may be needed.

## Safety & privacy

Identity verification exposes sensitive personal data. Use only official sites, avoid public Wi-Fi when possible, read retention notices, and delete temporary copies after submission.
