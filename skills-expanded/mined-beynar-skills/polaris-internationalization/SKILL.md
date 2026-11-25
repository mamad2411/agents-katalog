---
name: polaris-internationalization
description: Build global interfaces that work everywhere. Use this when designing for text expansion, word order changes, multiple languages, locales, cultural differences, right-to-left text, date formats, RTL layouts, translation, localization, character-based languages, cultural sensitivity, international commerce.
---

# Internationalization

Make commerce better for everyone by building interfaces that work everywhere. These guidelines help you design, write, and build products that can be used in every part of the world.

We aim to build one experience that works for all merchants in all markets. However, when a certain experience doesn't fit a specific market, tailor it.

## Key Definitions

### Internationalization (i18n)

Building your product and interface so they can be used in different locales. This includes creating flexible interfaces that allow for text expansion and changes to word order.

### Localization (l10n)

Adapting your product and interface for different locales to make them a good cultural fit. This includes adapting features, changing visuals, and translating text.

### Translation

Converting text from one language to another. Not to be confused with localization—translation is just one part of localizing a product.

### Locale

A linguistic region defined by both its language and country.

Examples: French-France (fr-FR); French-Canada (fr-CA); Portuguese-Brazil (pt-BR). Languages and countries won't always have a 1:1 mapping.

## Planning for Text Expansion

When interfaces are localized, the content will often expand in length. In most languages, text is up to 50% longer on average than English. Some non-Latin languages, such as Japanese, take up more vertical space. For character-based languages, text wrapping and line breaking can't always rely on spaces to separate words. Your interface needs to be flexible enough to accommodate language-specific formatting and text expansion without changing its context of use.

### Do's:
- Lay out elements so text expansion doesn't hinder information hierarchy
- Use single columns to stack elements flexibly to accommodate text expansion
- Ensure the right amount of padding for a clean interface

### Don'ts:
- Don't rely on responsive stacking alone. It can change the hierarchy of information and break at wrong spots.
- Don't use narrow columns in smaller components. Ensure flexibility for all text lengths.

### Tips for Text Expansion:
- Always assume the worst-case scenario for text length, especially on mobile and in layouts such as tables and columns. Avoid narrow columns.
- Pay particular attention to content elements with only a few words. In English, labels and buttons exclude words like "a" or "the," but many other languages need to include them. Small pieces of text may expand up to 300%.
- Polaris components are designed to be expandable, but test them in your designs and builds. Check the CSS layout to ensure text doesn't overflow when screen size is reduced.
- Work with linguistic experts to review line breaks and word wrapping for character-based languages like Chinese or Japanese to ensure they don't break sentences.

## Planning for Changes in Word Order

Word order can change dramatically in translation. If the layout and functionality of your interface depends on a certain word order, it's likely to break when localized.

### Do's:
- If content elements need to stay in a certain position, implement them as separate labels, outside of sentences
- When including links in body text, use only a single descriptive term or small part of a phrase as the link

### Don'ts:
- Don't place elements with fixed position inside a sentence. The sentence order often needs to change in translation.
- Don't use full phrases as links. Word order changes might break the link into several parts when translated.

### Tips for Word Order:
- Assume the word order of every sentence in your interface will change when translated
- Avoid using UI components to build sentences
- Avoid splitting one sentence into several strings (concatenated strings). Translators won't be able to change word order and translations won't make sense.
- Avoid using variables in your strings as they will translate differently

## Planning for Cultural Differences

Merchants in each locale have different cultural sensibilities. Use visuals, content, and interface formats that are useful and meaningful to merchants in all parts of the world.

### Visual and Symbolic Considerations:
- When possible, use universally known icons. Be mindful of country-specific icons and where they are surfaced.
- Be mindful of using colors to represent meaning. Colors hold discrete connotations in different cultures. For example, in North America, green indicates success and red indicates failure, but in China, red symbolizes prosperity and good fortune.

### Tips for Cultural Sensitivity:
- When using photos, illustrations, icons, or emojis, ensure visuals are not offensive or culturally insensitive. If unsure, research or ask someone with local knowledge.
- When naming features, be mindful of connotations in other cultures, especially for evocative names and acronyms.
- Avoid colloquial words, idioms, and references to popular culture. They're difficult to translate meaningfully.
- In some cultures, a person's given name comes first; in others, the family name comes first. Let merchants choose how they want to enter, read, and sort names, especially in text fields and lists.
- Many types of information (addresses, dates, numbers, currencies) are shown in different formats in different locales. Ensure these can be translated appropriately.
- Some cultures expect more guidelines and instructions when filling in long or critical forms. Consider using asterisks to mark mandatory fields in forms to match that expectation.
- Work with people that have local knowledge if possible.

## Internationalizing Polaris Components

When designing with a Polaris component, test the localized versions to ensure it still works with the rest of your interface.

If you need a certain component to adapt but it hasn't yet been internationalized in Polaris, you can open a feature request on GitHub: https://github.com/Shopify/polaris-react/issues/
