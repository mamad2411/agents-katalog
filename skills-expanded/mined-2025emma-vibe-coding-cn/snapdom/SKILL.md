---
नाम: स्नैपडोम
विवरण: स्नैपडॉम एक तेज़, सटीक डोम-टू-इमेज कैप्चर टूल है जो HTML तत्वों को स्केलेबल एसवीजी छवियों में परिवर्तित करता है। HTML तत्वों को कैप्चर करने, DOM को छवियों (SVG, PNG, JPG, WebP) में परिवर्तित करने, शैलियों, फ़ॉन्ट और छद्म तत्वों को संरक्षित करने के लिए उपयोग करें।
---

#SnapDOMSkill

HTML तत्वों को स्केलेबल एसवीजी या रैस्टर छवि प्रारूपों में परिवर्तित करने के लिए तेज़, निर्भरता-मुक्त DOM-टू-इमेज कैप्चर लाइब्रेरी।

## इस कौशल का उपयोग कब करना है

जब आपको आवश्यकता हो तब SnapDOM का उपयोग करें:
- HTML तत्वों को छवियों में बदलें (एसवीजी, पीएनजी, जेपीजी, वेबपी)
- छद्म तत्वों और छायाओं के साथ स्टाइल वाले DOM को कैप्चर करें
- एम्बेडेड फ़ॉन्ट और आइकन के साथ तत्वों को निर्यात करें
- कस्टम आयाम या स्केलिंग के साथ स्क्रीनशॉट बनाएं
- प्रॉक्सी फ़ॉलबैक का उपयोग करके CORS-अवरुद्ध संसाधनों को संभालें
- प्लगइन्स के साथ कस्टम रेंडरिंग पाइपलाइन लागू करें
- बड़े या जटिल तत्वों पर प्रदर्शन का अनुकूलन करें

## प्रमुख विशेषताऐं

### सार्वभौमिक निर्यात विकल्प
- **एसवीजी** - स्केलेबल वेक्टर प्रारूप, सभी शैलियों को एम्बेड करता है
- **पीएनजी, जेपीजी, वेबपी** - विन्यास योग्य गुणवत्ता के साथ रेखापुंज प्रारूप
- **कैनवास** - आगे की प्रक्रिया के लिए कच्चा कैनवास तत्व प्राप्त करें
- **ब्लॉब** - कस्टम हैंडलिंग के लिए कच्चा बाइनरी डेटा

###प्रदर्शन
- अल्ट्रा-फास्ट कैप्चर (छोटे तत्वों के लिए 1.6 एमएस, 4000×2000 के लिए ~171 एमएस)
- **कोई निर्भरता नहीं** - केवल मानक वेब एपीआई का उपयोग करता है
- जटिल तत्वों पर html2canvas से 10-40 गुना बेहतर प्रदर्शन करता है

### शैली समर्थन
- एंबेडेड फ़ॉन्ट (आइकन फ़ॉन्ट सहित)
- सीएसएस छद्म तत्व (::पहले, ::बाद)
- सीएसएस काउंटर
- सीएसएस लाइन-क्लैंप
- परिवर्तन और छाया प्रभाव
- छाया डोम सामग्री

### उन्नत क्षमताएँ
-समान मूल आईफ्रेम समर्थन
- अवरुद्ध परिसंपत्तियों के लिए CORS प्रॉक्सी फ़ॉलबैक
- कस्टम परिवर्तनों के लिए प्लगइन प्रणाली
- परिवर्तनों को सीधा करें (घुमाएँ/अनुवाद हटाएँ)
-चयनात्मक तत्व बहिष्करण
- चुस्त बाउंडिंग बॉक्स गणना

## स्थापना

### एनपीएम/यार्न
```bash
npm install @zumer/snapdom
# or
yarn add @zumer/snapdom
```

### सीडीएन (ईएस मॉड्यूल)
```html
<script type="module">
  import { snapdom } from "https://unpkg.com/@zumer/snapdom/dist/snapdom.mjs";
</script>
```

### सीडीएन (यूएमडी)
```html
<script src="https://unpkg.com/@zumer/snapdom/dist/snapdom.umd.js"></script>
```

## त्वरित प्रारंभ उदाहरण

### बुनियादी पुन: प्रयोज्य कैप्चर
```javascript
// Create reusable capture object
const result = await snapdom(document.querySelector('#target'));

// Export to different formats
const png = await result.toPng();
const jpg = await result.toJpg();
const svg = await result.toSvg();
const canvas = await result.toCanvas();
const blob = await result.toBlob();

// Use the result
document.body.appendChild(png);
```

### एक-चरणीय निर्यात
```javascript
// Direct export without intermediate object
const png = await snapdom.toPng(document.querySelector('#target'));
const svg = await snapdom.toSvg(element);
```

### तत्व डाउनलोड करें
```javascript
// Automatically download as file
await snapdom.download(element, 'screenshot.png');
await snapdom.download(element, 'image.svg');
```

### विकल्पों के साथ
```javascript
const result = await snapdom(element, {
  scale: 2,                    // 2x resolution
  width: 800,                  // Custom width
  height: 600,                 // Custom height
  embedFonts: true,            // Include @font-face
  exclude: '.no-capture',      // Hide elements
  useProxy: true,              // Enable CORS proxy
  straighten: true,            // Remove transforms
  noShadows: false             // Keep shadows
});

const png = await result.toPng({ quality: 0.95 });
```

## आवश्यक विकल्प संदर्भ

| विकल्प | प्रकार | उद्देश्य |
|------|------|------|
| 'स्केल' | संख्या | स्केल आउटपुट (जैसे, 2x रिज़ॉल्यूशन के लिए 2) |
| 'चौड़ाई' | संख्या | पिक्सेल में कस्टम आउटपुट चौड़ाई |
| 'ऊंचाई' | संख्या | पिक्सेल में कस्टम आउटपुट ऊंचाई |
| `एम्बेडफ़ॉन्ट्स` | बूलियन | गैर-आइकन @ फ़ॉन्ट-फेस नियम शामिल करें |
| `प्रॉक्सी का प्रयोग करें` | स्ट्रिंग\|बूलियन | CORS प्रॉक्सी सक्षम करें (डिफ़ॉल्ट के लिए URL या सत्य) |
| 'बहिष्कृत' | स्ट्रिंग | तत्वों को छिपाने के लिए सीएसएस चयनकर्ता |
| 'सीधा करो' | बूलियन | ट्रांसलेशन/रोटेट ट्रांसफॉर्म हटाएं |
| `नोशैडोज़` | बूलियन | पट्टी छाया प्रभाव |

## सामान्य पैटर्न

### प्रतिक्रियाशील स्क्रीनशॉट
```javascript
// Capture at different scales
const mobile = await snapdom.toPng(element, { scale: 1 });
const tablet = await snapdom.toPng(element, { scale: 1.5 });
const desktop = await snapdom.toPng(element, { scale: 2 });
```

### तत्वों को बाहर निकालें
```javascript
// Hide specific elements from capture
const png = await snapdom.toPng(element, {
  exclude: '.controls, .watermark, [data-no-capture]'
});
```

### निश्चित आयाम
```javascript
// Capture with specific size
const result = await snapdom(element, {
  width: 1200,
  height: 630  // Standard social media size
});
```

### सीओआरएस हैंडलिंग
```javascript
// Fallback for CORS-blocked resources
const png = await snapdom.toPng(element, {
  useProxy: 'https://cors.example.com/?' // Custom proxy
});
```

### प्लगइन सिस्टम (बीटा)
```javascript
// Extend with custom exporters
snapdom.plugins([pluginFactory, { colorOverlay: true }]);

// Hook into lifecycle
defineExports(context) {
  return {
    pdf: async (ctx, opts) => { /* generate PDF */ }
  };
}

// Lifecycle hooks available:
// beforeSnap → beforeClone → afterClone →
// beforeRender → beforeExport → afterExport
```

## प्रदर्शन तुलना

SnapDOM html2canvas से काफी बेहतर प्रदर्शन करता है:

| परिदृश्य | स्नैपडॉम | html2कैनवास | सुधार |
|---|---|---|---|
| छोटा (200×100) | 1.6ms | 68ms | 42x तेज |
| मध्यम (800×600) | 12 एमएस | 280 एमएस | 23 गुना तेज |
| बड़ा (4000×2000) | 171 एमएस | 1,800 एमएस | 10 गुना तेज |

## विकास

### स्थापित करना
```bash
git clone https://github.com/zumerlab/snapdom.git
cd snapdom
npm install
```

### निर्माण
```bash
npm run compile
```

### परीक्षण
```bash
npm test
```

## ब्राउज़र समर्थन

- क्रोम/एज 90+
- फ़ायरफ़ॉक्स 88+
-सफारी 14+
- मोबाइल ब्राउज़र (iOS Safari 14+, Chrome मोबाइल)

## संसाधन

### दस्तावेज़ीकरण
- **आधिकारिक वेबसाइट:** https://snapdom.dev/
- **गिटहब रिपॉजिटरी:** https://github.com/zumerlab/snapdom
- **एनपीएम पैकेज:** https://www.npmjs.com/package/@zumer/snapdom
- **लाइसेंस:** एमआईटी

### स्क्रिप्ट/
स्वचालन के लिए यहां सहायक स्क्रिप्ट जोड़ें, उदाहरण:
- `बैच-स्क्रीनशॉट.जेएस` - एकाधिक तत्वों को कैप्चर करें
- `pdf-export.js` - स्नैपशॉट को पीडीएफ में बदलें
- `तुलना-आउटपुट.जेएस` - एसवीजी बनाम पीएनजी गुणवत्ता की तुलना करें

### संपत्ति/
टेम्पलेट और उदाहरण जोड़ें:
- सामान्य कैप्चर परिदृश्यों के लिए HTML टेम्पलेट
- सीएसएस फ्रेमवर्क स्नैपडोम के साथ पूर्व-कॉन्फ़िगर किया गया
- स्नैपडोम को एकीकृत करने वाली बॉयलरप्लेट परियोजनाएं

## संबंधित उपकरण

- **html2canvas** - वैकल्पिक DOM कैप्चर (धीमा लेकिन अधिक संगत)
- **ऑर्बिट सीएसएस टूलकिट** - ज़ुमेरलैब द्वारा सहयोगी टूलकिट (https://github.com/zumerlab/orbit)

## युक्तियाँ एवं सर्वोत्तम प्रथाएँ

1. **प्रदर्शन**: बेहतर प्रदर्शन के लिए `चौड़ाई`/`ऊंचाई` के बजाय `स्केल` का उपयोग करें
2. **फ़ॉन्ट**: यह सुनिश्चित करने के लिए कि कस्टम फ़ॉन्ट सही ढंग से दिखाई दें, `एम्बेडफ़ॉन्ट: सत्य` सेट करें
3. **सीओआरएस मुद्दे**: यदि छवियां लोड होने में विफल रहती हैं तो `useProxy: true` का उपयोग करें
4. **बड़े तत्व**: जटिल पृष्ठों के लिए छोटे भागों में तोड़ें
5. **गुणवत्ता**: पीएनजी/जेपीजी के लिए, सर्वोत्तम गुणवत्ता के लिए `गुणवत्ता: 0.95` का उपयोग करें
6. **एसवीजी वेक्टर**: चार्ट और ग्राफिक्स के लिए एसवीजी निर्यात को प्राथमिकता दें

## समस्या निवारण

### तत्वों का प्रतिपादन नहीं हो रहा है
- जांचें कि क्या तत्व की ऊंचाई/चौड़ाई पर्याप्त है
- कैप्चर करने से पहले सत्यापित करें कि सीएसएस पूरी तरह से लोड है
- यदि परिवर्तन समस्याएँ पैदा कर रहा है तो `सीधा करें: गलत` आज़माएँ

### गुम फ़ॉन्ट्स
- `एम्बेडफ़ॉन्ट: सत्य` सेट करें
- स्नैपडॉम को कॉल करने से पहले सुनिश्चित करें कि फ़ॉन्ट लोड किए गए हैं
- फ़ॉन्ट लोडिंग त्रुटियों के लिए ब्राउज़र कंसोल की जाँच करें

### सीओआरएस मुद्दे
- `useProxy: true` सक्षम करें
- डिफ़ॉल्ट विफल होने पर कस्टम प्रॉक्सी यूआरएल का उपयोग करें
- जांचें कि क्या संसाधन एक ही मूल से हैं

### प्रदर्शन संबंधी मुद्दे
- `स्केल' मान कम करें
- छाया प्रतिपादन को छोड़ने के लिए `noShadows: true` का उपयोग करें
- बड़े कैप्चर को छोटे खंडों में विभाजित करने पर विचार करें
