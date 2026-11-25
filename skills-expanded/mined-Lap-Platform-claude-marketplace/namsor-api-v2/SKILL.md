---
name: namsor-api-v2
description: "NamSor API v2 API skill. Use when working with NamSor API v2 for api2. Covers 115 endpoints."
version: 1.0.0
generator: lapsh
---

# NamSor API v2
API version: 2.1.4

## Auth
ApiKey X-API-KEY in header

## Base URL
https://v2.namsor.com/NamSorAPIv2

## Setup
1. Set your API key in the appropriate header
2. GET /api2/json/regions -- verify access
3. POST /api2/json/nameTypeBatch -- create first nameTypeBatch

## Endpoints

115 endpoints across 1 groups. See references/api-spec.lap for full details.

### api2
| Method | Path | Description |
|--------|------|-------------|
| GET | /api2/json/disable/{source}/{disabled} | Activate/deactivate an API Key. |
| GET | /api2/json/country/{personalNameFull} | [USES 10 UNITS PER NAME] Infer the likely country of residence of a personal full name, or one surname. Assumes names as they are in the country of residence OR the country of origin. |
| GET | /api2/json/origin/{firstName}/{lastName} | [USES 10 UNITS PER NAME] Infer the likely country of origin of a personal name. Assumes names as they are in the country of origin. For US, CA, AU, NZ and other melting-pots : use 'diaspora' instead. |
| GET | /api2/json/nameType/{properNoun} | Infer the likely type of a proper noun (personal name, brand name, place name etc.) |
| GET | /api2/json/parseName/{nameFull} | Infer the likely first/last name structure of a name, ex. John Smith or SMITH, John or SMITH; John. |
| GET | /api2/json/regions | Print basic source statistics. |
| GET | /api2/json/genderstatv3/{enabled} | Activate/deactivate genderstatv3. |
| GET | /api2/json/softwareVersion | Get the current software version |
| GET | /api2/json/apiStatus | Prints the current status of the classifiers. A classifier name in apiStatus corresponds to a service name in apiServices. |
| GET | /api2/json/apiServices | List of classification services and usage cost in Units per classification (default is 1=ONE Unit). Some API endpoints (ex. Corridor) combine multiple classifiers. |
| GET | /api2/json/taxonomyClasses/{classifierName} | Print the taxonomy classes valid for the given classifier. |
| GET | /api2/json/apiUsage | Print current API usage. |
| GET | /api2/json/learnable/{source}/{learnable} | Activate/deactivate learning from a source. |
| GET | /api2/json/learnable/{source}/{learnable}/{token} | Activate/deactivate learning from a source. |
| GET | /api2/json/apiKeyInfo | Read API Key info. |
| GET | /api2/json/anonymize/{source}/{anonymized}/{token} | Activate/deactivate anonymization for a source. |
| GET | /api2/json/anonymize/{source}/{anonymized} | Activate/deactivate anonymization for a source. |
| GET | /api2/json/nameTypeGeo/{properNoun}/{countryIso2} | Infer the likely type of a proper noun (personal name, brand name, place name etc.) |
| POST | /api2/json/nameTypeBatch | Infer the likely common type of up to 100 proper nouns (personal name, brand name, place name etc.) |
| POST | /api2/json/nameTypeGeoBatch | Infer the likely common type of up to 100 proper nouns (personal name, brand name, place name etc.) |
| GET | /api2/json/corridor/{countryIso2From}/{firstNameFrom}/{lastNameFrom}/{countryIso2To}/{firstNameTo}/{lastNameTo} | [USES 50 UNITS PER NAME COUPLE] Infer several classifications for a cross border interaction between names (ex. remit, travel, intl com) |
| POST | /api2/json/corridorBatch | [USES 50 UNITS PER NAME PAIR] Infer several classifications for up to 100 cross border interaction between names (ex. remit, travel, intl com) |
| GET | /api2/json/gender/{firstName} | Infer the likely gender of a just a fiven name, assuming default 'US' local context. Please use preferably full names and local geographic context for better accuracy. |
| GET | /api2/json/gender/{firstName}/{lastName} | Infer the likely gender of a name. |
| GET | /api2/json/genderGeo/{firstName}/{lastName}/{countryIso2} | Infer the likely gender of a name, given a local context (ISO2 country code). |
| POST | /api2/json/genderGeoBatch | Infer the likely gender of up to 100 names, each given a local context (ISO2 country code). |
| POST | /api2/json/genderBatch | Infer the likely gender of up to 100 names, detecting automatically the cultural context. |
| GET | /api2/json/genderFullGeo/{fullName}/{countryIso2} | Infer the likely gender of a full name, given a local context (ISO2 country code). |
| GET | /api2/json/genderFull/{fullName} | Infer the likely gender of a full name, ex. John H. Smith |
| POST | /api2/json/genderFullBatch | Infer the likely gender of up to 100 full names, detecting automatically the cultural context. |
| POST | /api2/json/genderFullGeoBatch | Infer the likely gender of up to 100 full names, with a given cultural context (country ISO2 code). |
| POST | /api2/json/originBatch | [USES 10 UNITS PER NAME] Infer the likely country of origin of up to 100 names, detecting automatically the cultural context. |
| GET | /api2/json/originFull/{personalNameFull} | [USES 10 UNITS PER NAME] Infer the likely country of origin of a personal name. Assumes names as they are in the country of origin. For US, CA, AU, NZ and other melting-pots : use 'diaspora' instead. |
| POST | /api2/json/originFullBatch | [USES 10 UNITS PER NAME] Infer the likely country of origin of up to 100 names, detecting automatically the cultural context. |
| GET | /api2/json/subclassificationIndian/{firstName}/{lastName} | [USES 10 UNITS PER NAME] Infer the likely Indian state of Union territory according to ISO 3166-2:IN based on the name. |
| GET | /api2/json/subclassificationIndianFull/{fullName} | [USES 10 UNITS PER NAME] Infer the likely Indian state of Union territory according to ISO 3166-2:IN based on the name. |
| GET | /api2/json/subclassification/{countryIso2}/{firstName}/{lastName} | [USES 10 UNITS PER NAME] Infer the likely origin of a name at a country subclassification level (state or regeion). Initially, this is only supported for India (ISO2 code 'IN'). |
| GET | /api2/json/subclassificationFull/{countryIso2}/{fullName} | [USES 10 UNITS PER NAME] Infer the likely origin of a name at a country subclassification level (state or regeion). Initially, this is only supported for India (ISO2 code 'IN'). |
| POST | /api2/json/subclassificationBatch | [USES 10 UNITS PER NAME] Infer the likely origin of a list of up to 100 names at a country subclassification level (state or regeion). Initially, this is only supported for India (ISO2 code 'IN'). |
| POST | /api2/json/subclassificationFullBatch | [USES 10 UNITS PER NAME] Infer the likely origin of a list of up to 100 names at a country subclassification level (state or regeion). Initially, this is only supported for India (ISO2 code 'IN'). |
| POST | /api2/json/subclassificationIndianBatch | [USES 10 UNITS PER NAME] Infer the likely Indian state of Union territory according to ISO 3166-2:IN based on a list of up to 100 names. |
| POST | /api2/json/subclassificationIndianFullBatch | [USES 10 UNITS PER NAME] Infer the likely Indian state of Union territory according to ISO 3166-2:IN based on a list of up to 100 names. |
| GET | /api2/json/religionIndian/{subDivisionIso31662}/{firstName}/{lastName} | [USES 10 UNITS PER NAME] Infer the likely religion of a personal Indian first/last name, provided the Indian state or Union territory (NB/ this can be inferred using the subclassification endpoint). |
| GET | /api2/json/religion/{countryIso2}/{subDivisionIso31662}/{firstName}/{lastName} | [USES 10 UNITS PER NAME] Infer the likely religion of a personal first/last name. NB: only for INDIA (as of current version). |
| GET | /api2/json/religionIndianFull/{subDivisionIso31662}/{personalNameFull} | [USES 10 UNITS PER NAME] Infer the likely religion of a personal Indian full name, provided the Indian state or Union territory (NB/ this can be inferred using the subclassification endpoint). |
| GET | /api2/json/religionFull/{countryIso2}/{subDivisionIso31662}/{personalNameFull} | [USES 10 UNITS PER NAME] Infer the likely religion of a personal full name. NB: only for INDIA (as of current version). |
| POST | /api2/json/religionFullBatch | [USES 10 UNITS PER NAME] Infer the likely religion of up to 100 personal full names. NB: only for India as of currently. |
| POST | /api2/json/religionIndianFullBatch | [USES 10 UNITS PER NAME] Infer the likely religion of up to 100 personal full Indian names, provided the subclassification at State or Union territory level (NB/ can be inferred using the subclassification endpoint). |
| POST | /api2/json/religionBatch | [USES 10 UNITS PER NAME] Infer the likely religion of up to 100 personal first/last names. NB: only for India as of currently. |
| POST | /api2/json/religionIndianBatch | [USES 10 UNITS PER NAME] Infer the likely religion of up to 100 personal first/last Indian names, provided the subclassification at State or Union territory level (NB/ can be inferred using the subclassification endpoint). |
| GET | /api2/json/castegroupIndianFull/{subDivisionIso31662}/{personalNameFull} | [USES 10 UNITS PER NAME] Infer the likely Indian name castegroup of a personal full name. |
| POST | /api2/json/castegroupIndianFullBatch | [USES 10 UNITS PER NAME] Infer the likely Indian name castegroup of up to 100 personal full names. |
| GET | /api2/json/castegroupIndian/{subDivisionIso31662}/{firstName}/{lastName} | [USES 10 UNITS PER NAME] Infer the likely Indian name castegroup of a first / last name. |
| POST | /api2/json/castegroupIndianBatch | [USES 10 UNITS PER NAME] Infer the likely Indian name castegroup of up to 100 personal first / last names. |
| GET | /api2/json/casteIndian/{subDivisionIso31662}/{firstName}/{lastName} | [USES 10 UNITS PER NAME] Infer the likely Indian name caste of a personal Hindu name. |
| POST | /api2/json/casteIndianBatch | [USES 10 UNITS PER NAME] Infer the likely Indian name caste of up to 100 personal Indian Hindu names. |
| GET | /api2/json/corridorFull/{countryIso2From}/{personalNameFrom}/{countryIso2To}/{personalNameTo} | [USES 50 UNITS PER NAME COUPLE] Infer several classifications for a cross border interaction between names (ex. remit, travel, intl com) |
| POST | /api2/json/corridorFullBatch | [USES 50 UNITS PER NAME PAIR] Infer several classifications for up to 100 cross border interaction between names (ex. remit, travel, intl com) |
| POST | /api2/json/countryBatch | [USES 10 UNITS PER NAME] Infer the likely country of residence of up to 100 personal full names, or surnames. Assumes names as they are in the country of residence OR the country of origin. |
| GET | /api2/json/countryFnLn/{firstName}/{lastName} | [USES 10 UNITS PER NAME] Infer the likely country of residence of a personal first / last name, or one surname. Assumes names as they are in the country of residence OR the country of origin. |
| POST | /api2/json/countryFnLnBatch | [USES 10 UNITS PER NAME] Infer the likely country of residence of up to 100 personal first / last names, or surnames. Assumes names as they are in the country of residence OR the country of origin. |
| GET | /api2/json/usRaceEthnicity/{firstName}/{lastName} | [USES 10 UNITS PER NAME] Infer a US resident's likely race/ethnicity according to US Census taxonomy W_NL (white, non latino), HL (hispano latino),  A (asian, non latino), B_NL (black, non latino). Optionally add header X-OPTION-USRACEETHNICITY-TAXONOMY: USRACEETHNICITY-6CLASSES for two additional classes, AI_AN (American Indian or Alaskan Native) and PI (Pacific Islander). |
| GET | /api2/json/usRaceEthnicityZIP5/{firstName}/{lastName}/{zip5Code} | [USES 10 UNITS PER NAME] Infer a US resident's likely race/ethnicity according to US Census taxonomy, using (optional) ZIP5 code info. Output is W_NL (white, non latino), HL (hispano latino),  A (asian, non latino), B_NL (black, non latino). Optionally add header X-OPTION-USRACEETHNICITY-TAXONOMY: USRACEETHNICITY-6CLASSES for two additional classes, AI_AN (American Indian or Alaskan Native) and PI (Pacific Islander). |
| POST | /api2/json/usRaceEthnicityBatch | [USES 10 UNITS PER NAME] Infer up-to 100 US resident's likely race/ethnicity according to US Census taxonomy. Output is W_NL (white, non latino), HL (hispano latino),  A (asian, non latino), B_NL (black, non latino). Optionally add header X-OPTION-USRACEETHNICITY-TAXONOMY: USRACEETHNICITY-6CLASSES for two additional classes, AI_AN (American Indian or Alaskan Native) and PI (Pacific Islander). |
| POST | /api2/json/usZipRaceEthnicityBatch | [USES 10 UNITS PER NAME] Infer up-to 100 US resident's likely race/ethnicity according to US Census taxonomy, with (optional) ZIP code. Output is W_NL (white, non latino), HL (hispano latino),  A (asian, non latino), B_NL (black, non latino). Optionally add header X-OPTION-USRACEETHNICITY-TAXONOMY: USRACEETHNICITY-6CLASSES for two additional classes, AI_AN (American Indian or Alaskan Native) and PI (Pacific Islander). |
| GET | /api2/json/usRaceEthnicityFull/{personalNameFull} | [USES 10 UNITS PER NAME] Infer a US resident's likely race/ethnicity according to US Census taxonomy W_NL (white, non latino), HL (hispano latino),  A (asian, non latino), B_NL (black, non latino). Optionally add header X-OPTION-USRACEETHNICITY-TAXONOMY: USRACEETHNICITY-6CLASSES for two additional classes, AI_AN (American Indian or Alaskan Native) and PI (Pacific Islander). |
| POST | /api2/json/usRaceEthnicityFullBatch | [USES 10 UNITS PER NAME] Infer up-to 100 US resident's likely race/ethnicity according to US Census taxonomy. Output is W_NL (white, non latino), HL (hispano latino),  A (asian, non latino), B_NL (black, non latino). Optionally add header X-OPTION-USRACEETHNICITY-TAXONOMY: USRACEETHNICITY-6CLASSES for two additional classes, AI_AN (American Indian or Alaskan Native) and PI (Pacific Islander). |
| GET | /api2/json/diaspora/{countryIso2}/{firstName}/{lastName} | [USES 20 UNITS PER NAME] Infer the likely ethnicity/diaspora of a personal name, given a country of residence ISO2 code (ex. US, CA, AU, NZ etc.) |
| POST | /api2/json/diasporaBatch | [USES 20 UNITS PER NAME] Infer the likely ethnicity/diaspora of up to 100 personal names, given a country of residence ISO2 code (ex. US, CA, AU, NZ etc.) |
| GET | /api2/json/diasporaFull/{countryIso2}/{personalNameFull} | [USES 20 UNITS PER NAME] Infer the likely ethnicity/diaspora of a personal name, given a country of residence ISO2 code (ex. US, CA, AU, NZ etc.) |
| POST | /api2/json/diasporaFullBatch | [USES 20 UNITS PER NAME] Infer the likely ethnicity/diaspora of up to 100 personal names, given a country of residence ISO2 code (ex. US, CA, AU, NZ etc.) |
| GET | /api2/json/communityEngage/{countryIso2}/{firstName}/{lastName} | [USES 20 UNITS PER NAME] Infer the likely ethnicity/diaspora, country, gender of a personal name, given a country of residence ISO2 code (ex. US, CA, AU, NZ etc.) for community engagement (require special module/pricing) |
| POST | /api2/json/communityEngageBatch | Infer the likely ethnicity/diaspora, country, gender of up to 100 personal names, given a country of residence ISO2 code (ex. US, CA, AU, NZ etc.) for community engagement (require special module/pricing) |
| GET | /api2/json/communityEngageFull/{countryIso2}/{personalNameFull} | [USES 20 UNITS PER NAME] Infer the likely ethnicity/diaspora, country, gender of a personal name, given a country of residence ISO2 code (ex. US, CA, AU, NZ etc.) for community engagement (require special module/pricing) |
| POST | /api2/json/communityEngageFullBatch | Infer the likely ethnicity/diaspora, country, gender of up to 100 personal names, given a country of residence ISO2 code (ex. US, CA, AU, NZ etc.) for community engagement (require special module/pricing) |
| GET | /api2/json/parseName/{nameFull}/{countryIso2} | Infer the likely first/last name structure of a name, ex. John Smith or SMITH, John or SMITH; John. For better accuracy, provide a geographic context. |
| POST | /api2/json/parseNameBatch | Infer the likely first/last name structure of a name, ex. John Smith or SMITH, John or SMITH; John. |
| POST | /api2/json/parseNameGeoBatch | Infer the likely first/last name structure of a name, ex. John Smith or SMITH, John or SMITH; John. Giving a local context improves precision. |
| GET | /api2/json/parseChineseName/{chineseName} | Infer the likely first/last name structure of a name, ex. 王晓明 -> 王(surname) 晓明(given name) |
| POST | /api2/json/parseChineseNameBatch | Infer the likely first/last name structure of a name, ex. 王晓明 -> 王(surname) 晓明(given name). |
| GET | /api2/json/pinyinChineseName/{chineseName} | Romanize the Chinese name to Pinyin, ex. 王晓明 -> Wang (surname) Xiaoming (given name) |
| POST | /api2/json/pinyinChineseNameBatch | Romanize a list of Chinese name to Pinyin, ex. 王晓明 -> Wang (surname) Xiaoming (given name). |
| GET | /api2/json/chineseNameMatch/{chineseSurnameLatin}/{chineseGivenNameLatin}/{chineseName} | Return a score for matching Chinese name ex. 王晓明 with a romanized name ex. Wang Xiaoming |
| POST | /api2/json/chineseNameMatchBatch | Identify Chinese name candidates, based on the romanized name (firstName = chineseGivenName; lastName=chineseSurname), ex. Wang Xiaoming |
| GET | /api2/json/genderChineseNamePinyin/{chineseSurnameLatin}/{chineseGivenNameLatin} | Infer the likely gender of a Chinese name in LATIN (Pinyin). |
| POST | /api2/json/genderChineseNamePinyinBatch | Infer the likely gender of up to 100 Chinese names in LATIN (Pinyin). |
| GET | /api2/json/genderChineseName/{chineseName} | Infer the likely gender of a Chinese full name ex. 王晓明 |
| POST | /api2/json/genderChineseNameBatch | Infer the likely gender of up to 100 full names ex. 王晓明 |
| GET | /api2/json/chineseNameCandidates/{chineseSurnameLatin}/{chineseGivenNameLatin} | Identify Chinese name candidates, based on the romanized name ex. Wang Xiaoming |
| POST | /api2/json/chineseNameCandidatesBatch | Identify Chinese name candidates, based on the romanized name (firstName = chineseGivenName; lastName=chineseSurname), ex. Wang Xiaoming |
| GET | /api2/json/chineseNameGenderCandidates/{chineseSurnameLatin}/{chineseGivenNameLatin}/{knownGender} | Identify Chinese name candidates, based on the romanized name ex. Wang Xiaoming - having a known gender ('male' or 'female') |
| POST | /api2/json/chineseNameCandidatesGenderBatch | Identify Chinese name candidates, based on the romanized name (firstName = chineseGivenName; lastName=chineseSurname) ex. Wang Xiaoming. |
| GET | /api2/json/parseJapaneseName/{japaneseName} | Infer the likely first/last name structure of a name, ex. 山本 早苗 or Yamamoto Sanae |
| POST | /api2/json/parseJapaneseNameBatch | Infer the likely first/last name structure of a name, ex. 山本 早苗 or Yamamoto Sanae |
| GET | /api2/json/japaneseNameKanjiCandidates/{japaneseSurnameLatin}/{japaneseGivenNameLatin} | Identify japanese name candidates in KANJI, based on the romanized name ex. Yamamoto Sanae |
| GET | /api2/json/japaneseNameKanjiCandidates/{japaneseSurnameLatin}/{japaneseGivenNameLatin}/{knownGender} | Identify japanese name candidates in KANJI, based on the romanized name ex. Yamamoto Sanae - and a known gender. |
| GET | /api2/json/japaneseNameLatinCandidates/{japaneseSurnameKanji}/{japaneseGivenNameKanji} | Romanize japanese name, based on the name in Kanji. |
| POST | /api2/json/japaneseNameKanjiCandidatesBatch | Identify japanese name candidates in KANJI, based on the romanized name (firstName = japaneseGivenName; lastName=japaneseSurname), ex. Yamamoto Sanae |
| POST | /api2/json/japaneseNameGenderKanjiCandidatesBatch | Identify japanese name candidates in KANJI, based on the romanized name (firstName = japaneseGivenName; lastName=japaneseSurname) with KNOWN gender, ex. Yamamoto Sanae |
| POST | /api2/json/japaneseNameLatinCandidatesBatch | Romanize japanese names, based on the name in KANJI |
| GET | /api2/json/japaneseNameMatch/{japaneseSurnameLatin}/{japaneseGivenNameLatin}/{japaneseName} | Return a score for matching Japanese name in KANJI ex. 山本 早苗 with a romanized name ex. Yamamoto Sanae |
| GET | /api2/json/japaneseNameMatchFeedbackLoop/{japaneseSurnameLatin}/{japaneseGivenNameLatin}/{japaneseName} | [CREDITS 1 UNIT] Feedback loop to better perform matching Japanese name in KANJI ex. 山本 早苗 with a romanized name ex. Yamamoto Sanae |
| POST | /api2/json/japaneseNameMatchBatch | Return a score for matching a list of Japanese names in KANJI ex. 山本 早苗 with romanized names ex. Yamamoto Sanae |
| GET | /api2/json/genderJapaneseName/{japaneseSurname}/{japaneseGivenName} | Infer the likely gender of a Japanese name in LATIN (Pinyin). |
| POST | /api2/json/genderJapaneseNameBatch | Infer the likely gender of up to 100 Japanese names in LATIN (Pinyin). |
| GET | /api2/json/genderJapaneseNameFull/{japaneseName} | Infer the likely gender of a Japanese full name ex. 王晓明 |
| POST | /api2/json/genderJapaneseNameFullBatch | Infer the likely gender of up to 100 full names |
| GET | /api2/json/phoneCode/{firstName}/{lastName}/{phoneNumber} | [USES 11 UNITS PER NAME] Infer the likely country and phone prefix, given a personal name and formatted / unformatted phone number. |
| GET | /api2/json/phoneCodeGeo/{firstName}/{lastName}/{phoneNumber}/{countryIso2} | [USES 11 UNITS PER NAME] Infer the likely phone prefix, given a personal name and formatted / unformatted phone number, with a local context (ISO2 country of residence). |
| GET | /api2/json/phoneCodeGeoFeedbackLoop/{firstName}/{lastName}/{phoneNumber}/{phoneNumberE164}/{countryIso2} | [CREDITS 1 UNIT] Feedback loop to better infer the likely phone prefix, given a personal name and formatted / unformatted phone number, with a local context (ISO2 country of residence). |
| POST | /api2/json/phoneCodeBatch | [USES 11 UNITS PER NAME] Infer the likely country and phone prefix, of up to 100 personal names, detecting automatically the local context given a name and formatted / unformatted phone number. |
| POST | /api2/json/phoneCodeGeoBatch | [USES 11 UNITS PER NAME] Infer the likely country and phone prefix, of up to 100 personal names, with a local context (ISO2 country of residence). |
| POST | /api2/json/translateFullBatch | Translate up to 100 full names, from one source language to a target language. |
| POST | /api2/json/searchFullBatch | Search up to 100 full names, in an indexed dataset - using fuzzy name maching. |
| POST | /api2/json/compareFullBatch | Compare up to 100 full name pairs, using fuzzy name maching. |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "Get disable details?" -> GET /api2/json/disable/{source}/{disabled}
- "Get country details?" -> GET /api2/json/country/{personalNameFull}
- "Get origin details?" -> GET /api2/json/origin/{firstName}/{lastName}
- "Get nameType details?" -> GET /api2/json/nameType/{properNoun}
- "Get parseName details?" -> GET /api2/json/parseName/{nameFull}
- "List all regions?" -> GET /api2/json/regions
- "Get genderstatv3 details?" -> GET /api2/json/genderstatv3/{enabled}
- "List all softwareVersion?" -> GET /api2/json/softwareVersion
- "List all apiStatus?" -> GET /api2/json/apiStatus
- "List all apiServices?" -> GET /api2/json/apiServices
- "Get taxonomyClass details?" -> GET /api2/json/taxonomyClasses/{classifierName}
- "List all apiUsage?" -> GET /api2/json/apiUsage
- "Get learnable details?" -> GET /api2/json/learnable/{source}/{learnable}
- "Get learnable details?" -> GET /api2/json/learnable/{source}/{learnable}/{token}
- "List all apiKeyInfo?" -> GET /api2/json/apiKeyInfo
- "Get anonymize details?" -> GET /api2/json/anonymize/{source}/{anonymized}/{token}
- "Get anonymize details?" -> GET /api2/json/anonymize/{source}/{anonymized}
- "Get nameTypeGeo details?" -> GET /api2/json/nameTypeGeo/{properNoun}/{countryIso2}
- "Create a nameTypeBatch?" -> POST /api2/json/nameTypeBatch
- "Create a nameTypeGeoBatch?" -> POST /api2/json/nameTypeGeoBatch
- "Get corridor details?" -> GET /api2/json/corridor/{countryIso2From}/{firstNameFrom}/{lastNameFrom}/{countryIso2To}/{firstNameTo}/{lastNameTo}
- "Create a corridorBatch?" -> POST /api2/json/corridorBatch
- "Get gender details?" -> GET /api2/json/gender/{firstName}
- "Get gender details?" -> GET /api2/json/gender/{firstName}/{lastName}
- "Get genderGeo details?" -> GET /api2/json/genderGeo/{firstName}/{lastName}/{countryIso2}
- "Create a genderGeoBatch?" -> POST /api2/json/genderGeoBatch
- "Create a genderBatch?" -> POST /api2/json/genderBatch
- "Get genderFullGeo details?" -> GET /api2/json/genderFullGeo/{fullName}/{countryIso2}
- "Get genderFull details?" -> GET /api2/json/genderFull/{fullName}
- "Create a genderFullBatch?" -> POST /api2/json/genderFullBatch
- "Create a genderFullGeoBatch?" -> POST /api2/json/genderFullGeoBatch
- "Create a originBatch?" -> POST /api2/json/originBatch
- "Get originFull details?" -> GET /api2/json/originFull/{personalNameFull}
- "Create a originFullBatch?" -> POST /api2/json/originFullBatch
- "Get subclassificationIndian details?" -> GET /api2/json/subclassificationIndian/{firstName}/{lastName}
- "Get subclassificationIndianFull details?" -> GET /api2/json/subclassificationIndianFull/{fullName}
- "Get subclassification details?" -> GET /api2/json/subclassification/{countryIso2}/{firstName}/{lastName}
- "Get subclassificationFull details?" -> GET /api2/json/subclassificationFull/{countryIso2}/{fullName}
- "Create a subclassificationBatch?" -> POST /api2/json/subclassificationBatch
- "Create a subclassificationFullBatch?" -> POST /api2/json/subclassificationFullBatch
- "Create a subclassificationIndianBatch?" -> POST /api2/json/subclassificationIndianBatch
- "Create a subclassificationIndianFullBatch?" -> POST /api2/json/subclassificationIndianFullBatch
- "Get religionIndian details?" -> GET /api2/json/religionIndian/{subDivisionIso31662}/{firstName}/{lastName}
- "Get religion details?" -> GET /api2/json/religion/{countryIso2}/{subDivisionIso31662}/{firstName}/{lastName}
- "Get religionIndianFull details?" -> GET /api2/json/religionIndianFull/{subDivisionIso31662}/{personalNameFull}
- "Get religionFull details?" -> GET /api2/json/religionFull/{countryIso2}/{subDivisionIso31662}/{personalNameFull}
- "Create a religionFullBatch?" -> POST /api2/json/religionFullBatch
- "Create a religionIndianFullBatch?" -> POST /api2/json/religionIndianFullBatch
- "Create a religionBatch?" -> POST /api2/json/religionBatch
- "Create a religionIndianBatch?" -> POST /api2/json/religionIndianBatch
- "Get castegroupIndianFull details?" -> GET /api2/json/castegroupIndianFull/{subDivisionIso31662}/{personalNameFull}
- "Create a castegroupIndianFullBatch?" -> POST /api2/json/castegroupIndianFullBatch
- "Get castegroupIndian details?" -> GET /api2/json/castegroupIndian/{subDivisionIso31662}/{firstName}/{lastName}
- "Create a castegroupIndianBatch?" -> POST /api2/json/castegroupIndianBatch
- "Get casteIndian details?" -> GET /api2/json/casteIndian/{subDivisionIso31662}/{firstName}/{lastName}
- "Create a casteIndianBatch?" -> POST /api2/json/casteIndianBatch
- "Get corridorFull details?" -> GET /api2/json/corridorFull/{countryIso2From}/{personalNameFrom}/{countryIso2To}/{personalNameTo}
- "Create a corridorFullBatch?" -> POST /api2/json/corridorFullBatch
- "Create a countryBatch?" -> POST /api2/json/countryBatch
- "Get countryFnLn details?" -> GET /api2/json/countryFnLn/{firstName}/{lastName}
- "Create a countryFnLnBatch?" -> POST /api2/json/countryFnLnBatch
- "Get usRaceEthnicity details?" -> GET /api2/json/usRaceEthnicity/{firstName}/{lastName}
- "Get usRaceEthnicityZIP5 details?" -> GET /api2/json/usRaceEthnicityZIP5/{firstName}/{lastName}/{zip5Code}
- "Create a usRaceEthnicityBatch?" -> POST /api2/json/usRaceEthnicityBatch
- "Create a usZipRaceEthnicityBatch?" -> POST /api2/json/usZipRaceEthnicityBatch
- "Get usRaceEthnicityFull details?" -> GET /api2/json/usRaceEthnicityFull/{personalNameFull}
- "Create a usRaceEthnicityFullBatch?" -> POST /api2/json/usRaceEthnicityFullBatch
- "Get diaspora details?" -> GET /api2/json/diaspora/{countryIso2}/{firstName}/{lastName}
- "Create a diasporaBatch?" -> POST /api2/json/diasporaBatch
- "Get diasporaFull details?" -> GET /api2/json/diasporaFull/{countryIso2}/{personalNameFull}
- "Create a diasporaFullBatch?" -> POST /api2/json/diasporaFullBatch
- "Get communityEngage details?" -> GET /api2/json/communityEngage/{countryIso2}/{firstName}/{lastName}
- "Create a communityEngageBatch?" -> POST /api2/json/communityEngageBatch
- "Get communityEngageFull details?" -> GET /api2/json/communityEngageFull/{countryIso2}/{personalNameFull}
- "Create a communityEngageFullBatch?" -> POST /api2/json/communityEngageFullBatch
- "Get parseName details?" -> GET /api2/json/parseName/{nameFull}/{countryIso2}
- "Create a parseNameBatch?" -> POST /api2/json/parseNameBatch
- "Create a parseNameGeoBatch?" -> POST /api2/json/parseNameGeoBatch
- "Get parseChineseName details?" -> GET /api2/json/parseChineseName/{chineseName}
- "Create a parseChineseNameBatch?" -> POST /api2/json/parseChineseNameBatch
- "Get pinyinChineseName details?" -> GET /api2/json/pinyinChineseName/{chineseName}
- "Create a pinyinChineseNameBatch?" -> POST /api2/json/pinyinChineseNameBatch
- "Get chineseNameMatch details?" -> GET /api2/json/chineseNameMatch/{chineseSurnameLatin}/{chineseGivenNameLatin}/{chineseName}
- "Create a chineseNameMatchBatch?" -> POST /api2/json/chineseNameMatchBatch
- "Get genderChineseNamePinyin details?" -> GET /api2/json/genderChineseNamePinyin/{chineseSurnameLatin}/{chineseGivenNameLatin}
- "Create a genderChineseNamePinyinBatch?" -> POST /api2/json/genderChineseNamePinyinBatch
- "Get genderChineseName details?" -> GET /api2/json/genderChineseName/{chineseName}
- "Create a genderChineseNameBatch?" -> POST /api2/json/genderChineseNameBatch
- "Get chineseNameCandidate details?" -> GET /api2/json/chineseNameCandidates/{chineseSurnameLatin}/{chineseGivenNameLatin}
- "Create a chineseNameCandidatesBatch?" -> POST /api2/json/chineseNameCandidatesBatch
- "Get chineseNameGenderCandidate details?" -> GET /api2/json/chineseNameGenderCandidates/{chineseSurnameLatin}/{chineseGivenNameLatin}/{knownGender}
- "Create a chineseNameCandidatesGenderBatch?" -> POST /api2/json/chineseNameCandidatesGenderBatch
- "Get parseJapaneseName details?" -> GET /api2/json/parseJapaneseName/{japaneseName}
- "Create a parseJapaneseNameBatch?" -> POST /api2/json/parseJapaneseNameBatch
- "Get japaneseNameKanjiCandidate details?" -> GET /api2/json/japaneseNameKanjiCandidates/{japaneseSurnameLatin}/{japaneseGivenNameLatin}
- "Get japaneseNameKanjiCandidate details?" -> GET /api2/json/japaneseNameKanjiCandidates/{japaneseSurnameLatin}/{japaneseGivenNameLatin}/{knownGender}
- "Get japaneseNameLatinCandidate details?" -> GET /api2/json/japaneseNameLatinCandidates/{japaneseSurnameKanji}/{japaneseGivenNameKanji}
- "Create a japaneseNameKanjiCandidatesBatch?" -> POST /api2/json/japaneseNameKanjiCandidatesBatch
- "Create a japaneseNameGenderKanjiCandidatesBatch?" -> POST /api2/json/japaneseNameGenderKanjiCandidatesBatch
- "Create a japaneseNameLatinCandidatesBatch?" -> POST /api2/json/japaneseNameLatinCandidatesBatch
- "Get japaneseNameMatch details?" -> GET /api2/json/japaneseNameMatch/{japaneseSurnameLatin}/{japaneseGivenNameLatin}/{japaneseName}
- "Get japaneseNameMatchFeedbackLoop details?" -> GET /api2/json/japaneseNameMatchFeedbackLoop/{japaneseSurnameLatin}/{japaneseGivenNameLatin}/{japaneseName}
- "Create a japaneseNameMatchBatch?" -> POST /api2/json/japaneseNameMatchBatch
- "Get genderJapaneseName details?" -> GET /api2/json/genderJapaneseName/{japaneseSurname}/{japaneseGivenName}
- "Create a genderJapaneseNameBatch?" -> POST /api2/json/genderJapaneseNameBatch
- "Get genderJapaneseNameFull details?" -> GET /api2/json/genderJapaneseNameFull/{japaneseName}
- "Create a genderJapaneseNameFullBatch?" -> POST /api2/json/genderJapaneseNameFullBatch
- "Get phoneCode details?" -> GET /api2/json/phoneCode/{firstName}/{lastName}/{phoneNumber}
- "Get phoneCodeGeo details?" -> GET /api2/json/phoneCodeGeo/{firstName}/{lastName}/{phoneNumber}/{countryIso2}
- "Get phoneCodeGeoFeedbackLoop details?" -> GET /api2/json/phoneCodeGeoFeedbackLoop/{firstName}/{lastName}/{phoneNumber}/{phoneNumberE164}/{countryIso2}
- "Create a phoneCodeBatch?" -> POST /api2/json/phoneCodeBatch
- "Create a phoneCodeGeoBatch?" -> POST /api2/json/phoneCodeGeoBatch
- "Create a translateFullBatch?" -> POST /api2/json/translateFullBatch
- "Create a searchFullBatch?" -> POST /api2/json/searchFullBatch
- "Create a compareFullBatch?" -> POST /api2/json/compareFullBatch
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- Create/update endpoints typically return the created/updated object

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
