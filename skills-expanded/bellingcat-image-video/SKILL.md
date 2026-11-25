---
name: bellingcat-image-video
description: >
  Verify and analyze photos, videos, and images. Reverse image search, extract
  EXIF metadata, detect deepfakes/GAN images, perform facial recognition, and
  analyze video content. Use when the user shares an image, photo, screenshot,
  or video and needs to verify authenticity, find the source, or identify
  people/objects, even if they don't mention "OSINT."
compatibility: Requires internet access to fetch tool detail pages from bellingcat.gitbook.io
---

# Bellingcat Image & Video Investigation Tools

Tools for verifying, analyzing, and extracting information from photos and videos. Covers reverse image search, metadata extraction, facial recognition, and video forensics.

## Choosing Tools

- Use reverse search to investigate provenance, metadata tools for origin clues, and forensic tools to assess possible manipulation.
- Treat facial-recognition results as leads, not identification; corroborate with independent evidence and consider privacy impacts.

## Tools

### Reverse Image Search

| Tool | Best for | Cost | Description | Guide |
|------|----------|------|-------------|-------|
| [Google Lens](https://lens.google/) | An image recognition tool that can be used to identify locations or objects in photographs. | Free | Google Lens is an image recognition tool that can be used to identify locations or objects in photographs. | [Details](https://bellingcat.gitbook.io/toolkit/more/all-tools/google-lens) |
| [InVID](https://weverify.eu/verification-plugin/) | A toolkit that supports the verification of videos and images. | Free | A toolkit that supports the verification of videos and images. | [Details](https://bellingcat.gitbook.io/toolkit/more/all-tools/invid) |
| [RootAbout](http://rootabout.com/) | Reverse search images on the Internet Archive | Free | Reverse search images on the Internet Archive | [Details](https://bellingcat.gitbook.io/toolkit/more/all-tools/rootabout) |
| [Search by Image](https://addons.opera.com/extensions/details/search-by-image/) | A browser extension to reverse search an image on multiple search engines. | Free | A browser extension to reverse search an image on multiple search engines. | [Details](https://bellingcat.gitbook.io/toolkit/more/all-tools/search-by-image) |
| [TinEye](https://tineye.com/) | A search engine that allows the user to search using images (reverse image search). | Free | TinEye is a search engine that allows the user to search using images (reverse image search). | [Details](https://bellingcat.gitbook.io/toolkit/more/all-tools/tineye) |

### Facial Recognition

| Tool | Best for | Cost | Description | Guide |
|------|----------|------|-------------|-------|
| [Amazon Rekognition](https://aws.amazon.com/rekognition/) | Check how similar two faces are | Free | Check how similar two faces are |  |
| [Azure AI Video Indexer](https://vi.microsoft.com/en-us) | AI video tool for facial detection and other types of insights. | Paid | AI video tool for facial detection and other types of insights. | [Details](https://bellingcat.gitbook.io/toolkit/more/all-tools/azure-ai-video-indexer) |
| [Face Comparison by ToolPie](https://facecomparison.toolpie.com/) | Compares two human face photos to determine similarity. | Free | Compares two human face photos to determine similarity. | [Details](https://bellingcat.gitbook.io/toolkit/more/all-tools/face-comparison-toolpie) |
| [FaceCheck.ID](https://facecheck.id/) | A facial recognition search engine that tries to find photos of people that look similar… | Paid | A facial recognition search engine that tries to find photos of people that look similar to a person of interest. | [Details](https://bellingcat.gitbook.io/toolkit/more/all-tools/facecheck.id) |
| [PimEyes](https://pimeyes.com/en) | An AI-powered facial recognition reverse image search tool. | Paid | An AI-powered facial recognition reverse image search tool. | [Details](https://bellingcat.gitbook.io/toolkit/more/all-tools/pimeyes) |
| [Search4Faces](https://search4faces.com) | Upload the picture of a face and find pictures of similar looking people on VKontakte,… | Free | Upload the picture of a face and find pictures of similar looking people on VKontakte, Odnoklassniki, TikTok and Club... | [Details](https://bellingcat.gitbook.io/toolkit/more/all-tools/search4faces) |

### Metadata & EXIF

| Tool | Best for | Cost | Description | Guide |
|------|----------|------|-------------|-------|
| [ExifPurge](http://www.exifpurge.com/) | EXIF Purge is a small portable application to remove EXIF metadata from multiple images at… | Free | EXIF Purge is a small portable application to remove EXIF metadata from multiple images at once. With the click of a ... |  |
| [Forensically](https://29a.ch/photo-forensics/#forensic-magnifier) | A collection of web-based image forensics tools. | Free | A collection of web-based image forensics tools. Can identify fake or doctored images. | [Details](https://bellingcat.gitbook.io/toolkit/more/all-tools/forensically) |
| [FotoForensics](http://fotoforensics.com/) | Image forensics tool. | Free | Image forensics tool. |  |
| [InVID](https://weverify.eu/verification-plugin/) | A toolkit that supports the verification of videos and images. | Free | A toolkit that supports the verification of videos and images. | [Details](https://bellingcat.gitbook.io/toolkit/more/all-tools/invid) |
| [Irfanview](http://irfanview.com/) | Windows-based software to extract metadata. | Free | Windows-based software to extract metadata. |  |
| [Jimpl](https://jimpl.com/) | Online EXIF data viewer | Free | Online EXIF data viewer |  |
| [metadata2go](https://www.metadata2go.com/) | Check metadata for both photos and videos online. | Free | Check metadata for both photos and videos online. |  |
| [Reveal Image Verification Assistant](https://www.rand.org/research/projects/truth-decay/fighting-disinformation/search/items/reveal-image-verification-assistant.html) | Forensic providing eight filters to detect still images alterations. | Free | Forensic providing eight filters to detect still images alterations. Web-based image tool. Also available within InVI... |  |
| [xIFr](https://github.com/StigNygaard/xIFr) | A Firefox add-on for extracting EXIF metadata by right-clicking an image. | Free | A Firefox add-on for extracting EXIF metadata by right-clicking an image. | [Details](https://bellingcat.gitbook.io/toolkit/more/all-tools/xifr) |

### Image Misc

| Tool | Best for | Cost | Description | Guide |
|------|----------|------|-------------|-------|
| [AmIReal](https://seintpl.github.io/AmIReal/) | Github - GAN detector detects if faces were generated by ThisPersonDoesNotExist | Free | Github - GAN detector detects if faces were generated by ThisPersonDoesNotExist |  |
| [AutoStitch](https://mattabrown.github.io/autostitch.html) | Autostitch is a free tool for seamlessly combining multiple photos into a single panoramic… | Free | Autostitch is a free tool for seamlessly combining multiple photos into a single panoramic image, making it ideal for... | [Details](https://bellingcat.gitbook.io/toolkit/more/all-tools/autostitch) |
| [Cleanup.Pictures](https://cleanup.pictures/) | Web tool for quickly removing objects from an image. | Free | Web tool for quickly removing objects from an image. |  |
| [fdupes](https://github.com/adrianlopezroche/fdupes) | Github - Locating exact matches of duplicate files. | Free | Github - Locating exact matches of duplicate files. |  |
| [Forensically](https://29a.ch/photo-forensics/#forensic-magnifier) | A collection of web-based image forensics tools. | Free | A collection of web-based image forensics tools. Can identify fake or doctored images. | [Details](https://bellingcat.gitbook.io/toolkit/more/all-tools/forensically) |
| [Hugin](https://hugin.sourceforge.io/) | A free and open-source panorama photo stitching and HDR (High Dynamic Range imaging)… | Free | Hugin is a free and open-source panorama photo stitching and HDR (High Dynamic Range imaging) merging software that h... | [Details](https://bellingcat.gitbook.io/toolkit/more/all-tools/hugin) |
| [InVID](https://weverify.eu/verification-plugin/) | A toolkit that supports the verification of videos and images. | Free | A toolkit that supports the verification of videos and images. | [Details](https://bellingcat.gitbook.io/toolkit/more/all-tools/invid) |
| [IPVM Calculator](https://calculator.ipvm.com/) | Tool for simulating camera views (for geolocations). | Free | Tool for simulating camera views (for geolocations). |  |
| [PureRef](https://www.pureref.com/index.php) | Image workspace; lets you arrange images in groups, organize them, etc. | Free | Image workspace; lets you arrange images in groups, organize them, etc. |  |

## Investigation Tips

- Start with reverse image search (Google Lens, TinEye) to find the earliest known appearance of an image
- Extract EXIF metadata (Jimpl, metadata2go, xIFr) to find camera model, date, and GPS coordinates
- Use Forensically for a suite of forensic filters to detect manipulation (clone detection, error level analysis)
- For videos, use InVID to extract key frames for reverse image search and verify authenticity
- PimEyes or FaceCheck.ID for facial recognition — be aware of ethical and privacy considerations
- AmIReal detects GAN-generated faces; use before trusting facial recognition results
