# Airtable SDK — Full Integration
## Triggers: airtable, airtable base, airtable records, write to airtable, sync airtable, airtable integration, meta ads to airtable

## CREDENTIALS (configured)
AIRTABLE_API_KEY=patjCeXyPkvsgyBYK... (PAT format) ✅
AIRTABLE_BASE_ID=appdWr8FVxiARc0Iy ✅ (Meta Ads Spy base)

## SDK REPOS
~/installed-repos/airtable.js/       ← official JS SDK
~/installed-repos/pyairtable/         ← best Python SDK
~/installed-repos/airtable-py-pcorpet/ ← lightweight Python

## PYTHON (pyairtable)
```python
from pyairtable import Api
api = Api(os.environ["AIRTABLE_API_KEY"])
table = api.table(os.environ["AIRTABLE_BASE_ID"], "Ads")
table.batch_create([{"Ad ID": "123", "Advertiser": "Nike"}])
table.batch_upsert([{"Ad ID": "123", "Status": "Active"}], key_fields=["Ad ID"])
```

## META ADS SPY TABLE: appdWr8FVxiARc0Iy → "Ads"
Fields: Ad ID · Advertiser · Ad Copy · Headline · Media Type · Status · Image URL · Ad Library URL · Start Date
