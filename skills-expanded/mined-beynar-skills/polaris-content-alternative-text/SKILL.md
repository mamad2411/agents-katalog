---
name: polaris-content-alternative-text
description: Write alt text and accessibility labels that create inclusive experiences for screen reader users. Master concise, contextual, and meaningful descriptions for images, icons, and interactive elements.
---

# Alternative Text

Build inclusive experiences for merchants who use screen readers.

Alt text is a text replacement for an image. Generally represented by the `alt` HTML element attribute: `alt="alt text"`.

Often used by people who are blind or have low vision, screen readers announce alt text to explain images. Alt text will also display when images fail to download due to unstable or low-bandwidth connections.

## Alt Text Principles

Alt text should:
- Help visitors navigate the site
- Provide an inclusive experience
- Be as short and specific as possible
- Be contextual to the intended message

## Alt Text for Images

Use alt text when the image conveys valuable information, such as the ability to play a demo video. Even if an image isn't conveying meaningful information, don't leave an `<img>` tag without an alt text element. The screen reader may try to read the filename and create a negative experience.

**All `<img>` tags need an alt text attribute, even if it's empty.** Set an empty alt text attribute using `<img alt="" />`.

### Do
```
<VideoThumbnail accessibilityLabel="Watch how-to video on Shopify reports." />
<Thumbnail alt="Black choker necklace" />
<Icon accessibilityLabel="" />
```

### Don't
```
<VideoThumbnail accessibilityLabel="Screenshot 2022-11-07 at 3.05.55 PM" />
<Thumbnail alt="Sneaker.png" />
<Icon accessibilityLabel="IMG_1206.heic" />
```

## Writing Alt Text

Always write alt text in plain text. Screen reader users often listen at fast speeds (3x faster than visual reading) to make up time. Be as brief as possible.

### Be Concise
- Think about how to write for a small amount of space or a character limit
- Use simple words
- Remove needless words
- Remove articles like "a, an, one of" whenever possible
- Avoid "image of" or "photograph" unless the type of image is relevant

### Avoid Punctuation and Emojis
- Don't use !! or 🥰
- Screen readers announce these as "exclamation point, exclamation point" and "smiling face with three hearts"
- Use regular punctuation (commas, periods) as normal; screen readers will pause

### Acronyms
- Only use acronyms your audience will understand
- Write acronyms with spaces in-between: "Y M C A" (not "YMCA")
- Most screen readers will try to read the acronym as a word

### Voice
- Write in active voice when possible

## Alt Text in Context

Ask yourself:
- Is it interactive?
- Does this image convey information that isn't given elsewhere?
- Does the context of the image communicate anything?

The same image may have different alt text depending on what it conveys.

## Situations That Need Alt Text

### Icons
Icons that could be misinterpreted need an explanation. Use the Polaris `accessibilityLabel` prop or the `aria-label` HTML attribute. For interactive icons, describe the action ("search"), not the image ("magnifying glass").

### Do
```
<Button accessibilityLabel="search" onClick={() => search()}>
  <Icon source={SearchIcon} accessibilityLabel="" />
</Button>
```

### Actions
Write clear and predictable link text. If space constraints require unclear calls to action (like "Learn more"), give further indication of where merchants will be sent.

### Do
```
<Link url="https://www.shopify.com/protect" accessibilityLabel="Learn more about Fraud Protect">
  Learn more
</Link>
```

### Complex Images
Groups of image elements can be described by a single text rather than announcing each individual element.

For more guidance, visit the W3C page on [complex images](https://www.w3.org/WAI/tutorials/images/complex/).

## Situations That Don't Need Alt Text

Set `alt=""` to let screen readers know to skip the image.

### Decorative Elements
Elements purely for aesthetic reasons: empty state illustrations, dividers, hero images.

### Progress Bars
Progress bars often present visual information also found in text ("Loading 53%"). Continuously announcing changes is annoying.

### Images with Adequate Captions
Avoid adding repetitive alt text if an image has a caption that accurately reflects the information.

### Tracking Images
Images not visible to sighted users should not be announced to screen readers.

## Pronunciation and Translation

Always state the language of the page content with the HTML `lang` attribute. This ensures pronunciation and translation tools know what rules to use. If certain phrases are in a different language, use the `lang` attribute in a `<p>` tag or similar.

### Do
```
<html lang="en"></html>
<html lang="de"></html>
<html lang="pt-BR"></html>
```

### Don't
```
<html></html>
```

## SEO

Search engines also read alt text. Alt text helps increase image ranking results and site searchability outside of Shopify's admin.

When accounting for SEO:
- Use logical keywords (the words people search for)
- Include relevant listing details (limited edition, unique colorway)
- Describe the image, not what you want your audience to think
- Don't repeat your site name or brand name
- Avoid reducing clarity just to insert a keyword
- Never include unassociated lists of keywords in alt text

### Do
```
<Thumbnail alt="1460 Boot Limited Edition Oxblood Women's" />
```

### Don't
```
<Thumbnail alt="shoes sneakers womens footwear girls sizes soles heels boots" />
<Thumbnail alt="Cool shoes for a night out or hot date" />
```

## Related Components

Polaris components with alt text or aria label props:
- Avatar
- Button
- Icon
- Link
- Thumbnail
- Video Thumbnail
