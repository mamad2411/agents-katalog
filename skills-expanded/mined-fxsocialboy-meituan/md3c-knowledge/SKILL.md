---
name: md3c-knowledge
description: TikTok 3V architecture (VGeo/VRegion/VDC) datacenter hierarchy. Use when needing 3V mapping, VGeo/VRegion/VDC relationships, or environment functions like env.IDC(), env.GetCurrentVRegion(), region_lib.VGeo().
user-invocable: false
---

# TikTok 3V Architecture

## 3V Architecture Overview

TikTok infrastructure uses a hierarchical "3V" structure:
- **VGeo** (Compliance Zones): Major geographic regions
- **VRegion** (Logical Regions): Subdivisions within VGeos
- **VDC** (Data Centers): Physical facilities

### 3V Mapping
```yaml
VGeo-EU: # Previous as Clover. VGeo Name is VGeo-EU, including VGeo- prefix.
  EU-TTP: # VRegion Name is EU-TTP, excluding VRegion- prefix.
    - ie
  EU-TTP2:
    - no1a
  US-EastRed: # Previously referred to as `i18n` in the context of Region; also known as `gcp`
    - useast2a
    - useast2b

VGeo-ROW:
  Singapore-Central: # Previously referred to as `alisg` in the context of Region
    - my
    - my2
    - my3 # Planned new datacenter
    - sg1
  US-East: # Also known as `va`
    - maliva

VGeo-US: # Previously as Texas
  US-TTP: # Also known as `ttp`
    - useast5
  US-TTP2: # Also known as `ttp2`
    - useast8

NO-VGeo-For-These-VRegions: # Not core TikTok data center, but it may appear
  Asia-SouthEastBD:
    - mya
    - myb
    - myc
  US-EastBD:
    - useast9a
    - useast12a
    - useast13a
    - useast14a
  Asia-CIS:
    - mycisa
    - mycisb
  China-North:
    - hl
    - lf
    - lq
    - yg
    - gl
  China-East:
    - pd
    - hj
    - yz
    - zjg
```

### Testing Environments
```yaml
NO-VGeo-For-Testing-Environments:
  US-BOE:
    - boei18n
    - boettp
  China-BOE:
    - boe
```

### 3V Relevant Functions
```go
package main

import (
    "code.byted.org/gopkg/env" // Both gopkg/env and gdp/env are ok. Follow original codes.
    "code.byted.org/tiktok/region_lib"
)

func Example() {
  env.IDC() // return current VDC
  env.DC_${VDC.upper()} // constants for each VDC

  env.GetCurrentVRegion() // return current VRegion
  env.VRegion_${VRegion.replace('-', '').upper() } // constants for each VRegion

  region_lib.VGeo() // return current VGeo
  region_lib.VGEO_ROW, region_lib.VGEO_US,  region_lib.VGEO_EU // constant for VGeos

  // Deprecated: Use env.GetCurrentVRegion() instead
  env.Region() // return current Region
  env.R_MALIVA (env.VREGION_USEAST), env.R_ALISG (env.VREGION_SINGAPORECENTRAL), env.R_USTTP, env.R_USTTP2, env.I18N (env.VREGION_USEASTRED), env.R_EUTTP, env.R_EUTTP2 // constants for each Region

  env.IsBoe() // return true if in "US-BOE" or "China-BOE".
  env.IsBoeI18N()  // return true if in "US-BOE"
  env.IsBoeCN() // return true if in "China-BOE"
  env.IsProduct()  // equivalent to !env.IsBoe()
}
```

For environment functions not listed above, search its definition to understand its behavior as needed.
