---
name: openfec
description: "OpenFEC API skill. Use when working with OpenFEC for audit-case, audit-category, audit-primary-category. Covers 99 endpoints."
version: 1.0.0
generator: lapsh
---

# OpenFEC
API version: 1.0

## Auth
ApiKey X-Api-Key in header | ApiKey api_key in query | ApiKey api_key in query

## Base URL
Not specified.

## Setup
1. Set your API key in the appropriate header
2. GET /v1/audit-case/ -- verify access

## Endpoints

99 endpoints across 25 groups. See references/api-spec.lap for full details.

### audit-case
| Method | Path | Description |
|--------|------|-------------|
| GET | /v1/audit-case/ | This endpoint contains Final Audit Reports approved by the Commission since inception. |

### audit-category
| Method | Path | Description |
|--------|------|-------------|
| GET | /v1/audit-category/ | This lists the options for the categories and subcategories available in the /audit-search/ endpoint. |

### audit-primary-category
| Method | Path | Description |
|--------|------|-------------|
| GET | /v1/audit-primary-category/ | This lists the options for the primary categories available in the /audit-search/ endpoint. |

### calendar-dates
| Method | Path | Description |
|--------|------|-------------|
| GET | /v1/calendar-dates/ | Combines the election and reporting dates with Commission meetings, conferences, outreach, Advisory Opinions, rules, litigation dates and other |
| GET | /v1/calendar-dates/export/ | Returns CSV or ICS for downloading directly into calendar applications like Google, Outlook or other applications. |

### candidate
| Method | Path | Description |
|--------|------|-------------|
| GET | /v1/candidate/{candidate_id}/ | This endpoint is useful for finding detailed information about a particular candidate. Use the |
| GET | /v1/candidate/{candidate_id}/committees/ | This endpoint is useful for finding detailed information about a particular committee or |
| GET | /v1/candidate/{candidate_id}/committees/history/ | Explore a filer's characteristics over time. This can be particularly useful if the committees change treasurers, designation, or `committee_type`. |
| GET | /v1/candidate/{candidate_id}/committees/history/{cycle}/ | Explore a filer's characteristics over time. This can be particularly useful if the committees change treasurers, designation, or `committee_type`. |
| GET | /v1/candidate/{candidate_id}/filings/ | All official records and reports filed by or delivered to the FEC. |
| GET | /v1/candidate/{candidate_id}/history/ | Find out a candidate's characteristics over time. This is particularly useful if the |
| GET | /v1/candidate/{candidate_id}/history/{cycle}/ | Find out a candidate's characteristics over time. This is particularly useful if the |
| GET | /v1/candidate/{candidate_id}/totals/ | This endpoint provides information about a committee's Form 3, Form 3X, or Form 3P financial reports, |

### candidates
| Method | Path | Description |
|--------|------|-------------|
| GET | /v1/candidates/ | Fetch basic information about candidates, and use parameters to filter results to the |
| GET | /v1/candidates/search/ | Fetch basic information about candidates and their principal committees. |
| GET | /v1/candidates/totals/ | Aggregated candidate receipts and disbursements grouped by cycle. |
| GET | /v1/candidates/totals/aggregates/ | Candidate total receipts and disbursements aggregated by `aggregate_by`. |

### committee
| Method | Path | Description |
|--------|------|-------------|
| GET | /v1/committee/{committee_id}/ | This endpoint is useful for finding detailed information about a particular committee or |
| GET | /v1/committee/{committee_id}/candidates/ | This endpoint is useful for finding detailed information about a particular candidate. Use the |
| GET | /v1/committee/{committee_id}/candidates/history/ | Find out a candidate's characteristics over time. This is particularly useful if the |
| GET | /v1/committee/{committee_id}/candidates/history/{cycle}/ | Find out a candidate's characteristics over time. This is particularly useful if the |
| GET | /v1/committee/{committee_id}/filings/ | All official records and reports filed by or delivered to the FEC. |
| GET | /v1/committee/{committee_id}/history/ | Explore a filer's characteristics over time. This can be particularly useful if the committees change treasurers, designation, or `committee_type`. |
| GET | /v1/committee/{committee_id}/history/{cycle}/ | Explore a filer's characteristics over time. This can be particularly useful if the committees change treasurers, designation, or `committee_type`. |
| GET | /v1/committee/{committee_id}/reports/ | Each report represents the summary information from Form 3, Form 3X and Form 3P. |
| GET | /v1/committee/{committee_id}/totals/ | This endpoint provides information about a committee's Form 3, Form 3X, or Form 3P financial reports, |

### committees
| Method | Path | Description |
|--------|------|-------------|
| GET | /v1/committees/ | Fetch basic information about committees and filers. Use parameters to filter for |

### communication_costs
| Method | Path | Description |
|--------|------|-------------|
| GET | /v1/communication_costs/ | 52 U.S.C. 30118 allows "communications by a corporation to its stockholders and executive or administrative personnel and their families or by a labor organization to its members and their families on any subject," including the express advocacy of the election or defeat of any Federal candidate.  The costs of such communications must be reported to the Federal Election Commission under certain circumstances. |
| GET | /v1/communication_costs/aggregates/ | Communication cost aggregated by candidate ID and committee ID. |
| GET | /v1/communication_costs/by_candidate/ | Communication cost aggregated by candidate ID and committee ID. |
| GET | /v1/communication_costs/totals/by_candidate/ | Total communications costs aggregated across committees on supported or opposed candidates by cycle or candidate election year. |

### efile
| Method | Path | Description |
|--------|------|-------------|
| GET | /v1/efile/filings/ | Basic information about electronic files coming into the FEC, posted as they are received. |
| GET | /v1/efile/form1/ | Basic information about electronic files coming into the FEC, posted as they are received. |
| GET | /v1/efile/form2/ | Basic information about electronic files coming into the FEC, posted as they are received. |
| GET | /v1/efile/reports/house-senate/ | Key financial data reported periodically by committees as they are reported. This feed includes summary |
| GET | /v1/efile/reports/pac-party/ | Key financial data reported periodically by committees as they are reported. This feed includes summary |
| GET | /v1/efile/reports/presidential/ | Key financial data reported periodically by committees as they are reported. This feed includes summary |

### election-dates
| Method | Path | Description |
|--------|------|-------------|
| GET | /v1/election-dates/ | FEC election dates since 1995. |

### electioneering
| Method | Path | Description |
|--------|------|-------------|
| GET | /v1/electioneering/ | An electioneering communication is any broadcast, cable or satellite communication that fulfills each of the following conditions: |
| GET | /v1/electioneering/aggregates/ | Electioneering communications costs aggregates |
| GET | /v1/electioneering/by_candidate/ | Electioneering costs aggregated by candidate |
| GET | /v1/electioneering/totals/by_candidate/ | Total electioneering communications spent on candidates by cycle |

### elections
| Method | Path | Description |
|--------|------|-------------|
| GET | /v1/elections/ | Look at the top-level financial information for all candidates running for the same |
| GET | /v1/elections/search/ | List elections by cycle, office, state, and district. |
| GET | /v1/elections/summary/ | List elections by cycle, office, state, and district. |

### filings
| Method | Path | Description |
|--------|------|-------------|
| GET | /v1/filings/ | All official records and reports filed by or delivered to the FEC. |

### legal
| Method | Path | Description |
|--------|------|-------------|
| GET | /v1/legal/docs/{doc_type}/{no} | Search legal documents by type and number |
| GET | /v1/legal/search/ | Search legal documents by document type, or across all document types using keywords, parameter values and ranges. |

### names
| Method | Path | Description |
|--------|------|-------------|
| GET | /v1/names/audit_candidates/ | Search for candidates or committees by name. If you're looking for information on a |
| GET | /v1/names/audit_committees/ | Search for candidates or committees by name. If you're looking for information on a |
| GET | /v1/names/candidates/ | Search for candidates or committees by name. If you're looking for information on a |
| GET | /v1/names/committees/ | Search for candidates or committees by name. If you're looking for information on a |

### national_party
| Method | Path | Description |
|--------|------|-------------|
| GET | /v1/national_party/schedule_a/ | This endpoint includes national party committee account receipts for presidential nominating conventions, |
| GET | /v1/national_party/schedule_b/ | This endpoint includes national party committee account disbursements for presidential nominating conventions, |
| GET | /v1/national_party/totals/ | This endpoint includes national party committee account total receipts and total disbursements for |

### operations-log
| Method | Path | Description |
|--------|------|-------------|
| GET | /v1/operations-log/ | The Operations log contains details of each report loaded into the database. It is primarily |

### presidential
| Method | Path | Description |
|--------|------|-------------|
| GET | /v1/presidential/contributions/by_candidate/ | Net receipts per candidate. |
| GET | /v1/presidential/contributions/by_size/ | Contribution receipts by size per candidate. |
| GET | /v1/presidential/contributions/by_state/ | Contribution receipts by state per candidate. |
| GET | /v1/presidential/coverage_end_date/ | Coverage end date per candidate. |
| GET | /v1/presidential/financial_summary/ | Financial summary per candidate. |

### rad-analyst
| Method | Path | Description |
|--------|------|-------------|
| GET | /v1/rad-analyst/ | Use this endpoint to look up the RAD Analyst for a committee. |

### reporting-dates
| Method | Path | Description |
|--------|------|-------------|
| GET | /v1/reporting-dates/ | FEC election dates since 1995. |

### reports
| Method | Path | Description |
|--------|------|-------------|
| GET | /v1/reports/{entity_type}/ | Each report represents the summary information from Form 3, Form 3X and Form 3P. |

### schedules
| Method | Path | Description |
|--------|------|-------------|
| GET | /v1/schedules/schedule_a/ | This description is for both ​`/schedules​/schedule_a​/` and ​ `/schedules​/schedule_a​/{sub_id}​/`. |
| GET | /v1/schedules/schedule_a/by_employer/ | This endpoint provides itemized individual contributions received by a committee, aggregated by the contributor’s employer name. If you are interested in our “is_individual” methodology, review the [methodology page](https://www.fec.gov/campaign-finance-data/about-campaign-finance-data/methodology). Unitemized individual contributions are not included. |
| GET | /v1/schedules/schedule_a/by_occupation/ | This endpoint provides itemized individual contributions received by a committee, aggregated by the contributor’s occupation. If you are interested in our “is_individual” methodology, review the [methodology page](https://www.fec.gov/campaign-finance-data/about-campaign-finance-data/methodology). Unitemized individual contributions are not included. |
| GET | /v1/schedules/schedule_a/by_size/ | This endpoint provides individual contributions received by a committee, aggregated by size: |
| GET | /v1/schedules/schedule_a/by_size/by_candidate/ | This endpoint provides itemized individual contributions received by a committee, aggregated by size of contribution and candidate. If you are interested in our “is_individual” methodology, review the [methodology page](https://www.fec.gov/campaign-finance-data/about-campaign-finance-data/methodology). Unitemized individual contributions are not included. |
| GET | /v1/schedules/schedule_a/by_state/ | This endpoint provides itemized individual contributions received by a committee, aggregated by the contributor’s state. If you are interested in our “is_individual” methodology, review the [methodology page](https://www.fec.gov/campaign-finance-data/about-campaign-finance-data/methodology). Unitemized individual contributions are not included. |
| GET | /v1/schedules/schedule_a/by_state/by_candidate/ | This endpoint provides itemized individual contributions received by a committee, aggregated by contributor’s state and candidate. If you are interested in our “is_individual” methodology, review the [methodology page](https://www.fec.gov/campaign-finance-data/about-campaign-finance-data/methodology). Unitemized individual contributions are not included. |
| GET | /v1/schedules/schedule_a/by_state/by_candidate/totals/ | Itemized individual contributions aggregated by contributor’s state, candidate, committee type and cycle. If you are interested in our “is_individual” methodology, review the [methodology page](https://www.fec.gov/campaign-finance-data/about-campaign-finance-data/methodology). Unitemized individual contributions are not included. |
| GET | /v1/schedules/schedule_a/by_state/totals/ | This endpoint provides itemized individual contributions received by a committee, aggregated by contributor’s state, committee type and cycle. If you are interested in our “is_individual” methodology, review the [methodology page](https://www.fec.gov/campaign-finance-data/about-campaign-finance-data/methodology). Unitemized individual contributions are not included. |
| GET | /v1/schedules/schedule_a/by_zip/ | This endpoint provides itemized individual contributions received by a committee, aggregated by the contributor’s ZIP code. If you are interested in our “is_individual” methodology, review the [methodology page](https://www.fec.gov/campaign-finance-data/about-campaign-finance-data/methodology). Unitemized individual contributions are not included. |
| GET | /v1/schedules/schedule_a/efile/ | Efiling endpoints provide real-time campaign finance data received from electronic filers. Efiling endpoints only contain the most recent four months of data and don't contain the processed and coded data that you can find on other endpoints. |
| GET | /v1/schedules/schedule_a/{sub_id}/ | This description is for both ​`/schedules​/schedule_a​/` and ​ `/schedules​/schedule_a​/{sub_id}​/`. |
| GET | /v1/schedules/schedule_a_form5/ | FEC FORM 5 Receipts |
| GET | /v1/schedules/schedule_b/ | Schedule B filings describe itemized disbursements. This data |
| GET | /v1/schedules/schedule_b/by_purpose/ | Schedule B disbursements aggregated by disbursement purpose category. To avoid double counting, |
| GET | /v1/schedules/schedule_b/by_recipient/ | Schedule B disbursements aggregated by recipient name. To avoid double counting, |
| GET | /v1/schedules/schedule_b/by_recipient_id/ | Schedule B disbursements aggregated by recipient committee ID, if applicable. |
| GET | /v1/schedules/schedule_b/efile/ | Efiling endpoints provide real-time campaign finance data received from electronic filers. Efiling endpoints only contain the most recent four months of data and don't contain the processed and coded data that you can find on other endpoints. |
| GET | /v1/schedules/schedule_b/{sub_id}/ | Schedule B filings describe itemized disbursements. This data |
| GET | /v1/schedules/schedule_c/ | Schedule C shows all loans, endorsements and loan guarantees a committee |
| GET | /v1/schedules/schedule_c/{sub_id}/ | Schedule C shows all loans, endorsements and loan guarantees a committee |
| GET | /v1/schedules/schedule_d/ | Schedule D, it shows debts and obligations owed to or by the committee that are |
| GET | /v1/schedules/schedule_d/{sub_id}/ | Schedule D, it shows debts and obligations owed to or by the committee that are |
| GET | /v1/schedules/schedule_e/ | Schedule E covers the line item expenditures for independent expenditures. For example, if a super PAC |
| GET | /v1/schedules/schedule_e/by_candidate/ | Schedule E receipts aggregated by recipient candidate. To avoid double |
| GET | /v1/schedules/schedule_e/efile/ | Efiling endpoints provide real-time campaign finance data received from electronic filers. Efiling endpoints only contain the most recent four months of data and don't contain the processed and coded data that you can find on other endpoints. |
| GET | /v1/schedules/schedule_e/totals/by_candidate/ | Total independent expenditure on supported or opposed candidates by cycle or candidate election year. |
| GET | /v1/schedules/schedule_f/ | Schedule F, it shows all special expenditures a national or state party committee |
| GET | /v1/schedules/schedule_f/{sub_id}/ | Schedule F, it shows all special expenditures a national or state party committee |
| GET | /v1/schedules/schedule_h4/ | Schedule H4 filings describe disbursements for allocated federal/nonfederal activity. This data |
| GET | /v1/schedules/schedule_h4/efile/ | Efiling endpoints provide real-time campaign finance data received from electronic filers. Efiling endpoints only contain the most recent four months of data and don't contain the processed and coded data that you can find on other endpoints. |

### state-election-office
| Method | Path | Description |
|--------|------|-------------|
| GET | /v1/state-election-office/ | State laws and procedures govern elections for state or local offices as well as |

### totals
| Method | Path | Description |
|--------|------|-------------|
| GET | /v1/totals/by_entity/ | Provides cumulative receipt totals by entity type, over a two year cycle. Totals are adjusted to avoid double counting. |
| GET | /v1/totals/inaugural_committees/by_contributor/ | This endpoint provides information about an inaugural committee's Form 13 report of donations accepted. |
| GET | /v1/totals/{entity_type}/ | This endpoint provides information about a committee's Form 3, Form 3X, or Form 3P financial reports, |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "Search audit-case?" -> GET /v1/audit-case/
- "List all audit-category?" -> GET /v1/audit-category/
- "List all audit-primary-category?" -> GET /v1/audit-primary-category/
- "List all calendar-dates?" -> GET /v1/calendar-dates/
- "List all export?" -> GET /v1/calendar-dates/export/
- "Get candidate details?" -> GET /v1/candidate/{candidate_id}/
- "List all committees?" -> GET /v1/candidate/{candidate_id}/committees/
- "List all history?" -> GET /v1/candidate/{candidate_id}/committees/history/
- "Get history details?" -> GET /v1/candidate/{candidate_id}/committees/history/{cycle}/
- "List all filings?" -> GET /v1/candidate/{candidate_id}/filings/
- "List all history?" -> GET /v1/candidate/{candidate_id}/history/
- "Get history details?" -> GET /v1/candidate/{candidate_id}/history/{cycle}/
- "List all totals?" -> GET /v1/candidate/{candidate_id}/totals/
- "Search candidates?" -> GET /v1/candidates/
- "Search search?" -> GET /v1/candidates/search/
- "Search totals?" -> GET /v1/candidates/totals/
- "List all aggregates?" -> GET /v1/candidates/totals/aggregates/
- "Get committee details?" -> GET /v1/committee/{committee_id}/
- "List all candidates?" -> GET /v1/committee/{committee_id}/candidates/
- "List all history?" -> GET /v1/committee/{committee_id}/candidates/history/
- "Get history details?" -> GET /v1/committee/{committee_id}/candidates/history/{cycle}/
- "List all filings?" -> GET /v1/committee/{committee_id}/filings/
- "List all history?" -> GET /v1/committee/{committee_id}/history/
- "Get history details?" -> GET /v1/committee/{committee_id}/history/{cycle}/
- "List all reports?" -> GET /v1/committee/{committee_id}/reports/
- "List all totals?" -> GET /v1/committee/{committee_id}/totals/
- "Search committees?" -> GET /v1/committees/
- "List all communication_costs?" -> GET /v1/communication_costs/
- "List all aggregates?" -> GET /v1/communication_costs/aggregates/
- "List all by_candidate?" -> GET /v1/communication_costs/by_candidate/
- "List all by_candidate?" -> GET /v1/communication_costs/totals/by_candidate/
- "List all filings?" -> GET /v1/efile/filings/
- "List all form1?" -> GET /v1/efile/form1/
- "List all form2?" -> GET /v1/efile/form2/
- "List all house-senate?" -> GET /v1/efile/reports/house-senate/
- "List all pac-party?" -> GET /v1/efile/reports/pac-party/
- "List all presidential?" -> GET /v1/efile/reports/presidential/
- "List all election-dates?" -> GET /v1/election-dates/
- "List all electioneering?" -> GET /v1/electioneering/
- "List all aggregates?" -> GET /v1/electioneering/aggregates/
- "List all by_candidate?" -> GET /v1/electioneering/by_candidate/
- "List all by_candidate?" -> GET /v1/electioneering/totals/by_candidate/
- "List all elections?" -> GET /v1/elections/
- "List all search?" -> GET /v1/elections/search/
- "List all summary?" -> GET /v1/elections/summary/
- "List all filings?" -> GET /v1/filings/
- "Get doc details?" -> GET /v1/legal/docs/{doc_type}/{no}
- "Search search?" -> GET /v1/legal/search/
- "Search audit_candidates?" -> GET /v1/names/audit_candidates/
- "Search audit_committees?" -> GET /v1/names/audit_committees/
- "Search candidates?" -> GET /v1/names/candidates/
- "Search committees?" -> GET /v1/names/committees/
- "List all schedule_a?" -> GET /v1/national_party/schedule_a/
- "List all schedule_b?" -> GET /v1/national_party/schedule_b/
- "List all totals?" -> GET /v1/national_party/totals/
- "List all operations-log?" -> GET /v1/operations-log/
- "List all by_candidate?" -> GET /v1/presidential/contributions/by_candidate/
- "List all by_size?" -> GET /v1/presidential/contributions/by_size/
- "List all by_state?" -> GET /v1/presidential/contributions/by_state/
- "List all coverage_end_date?" -> GET /v1/presidential/coverage_end_date/
- "List all financial_summary?" -> GET /v1/presidential/financial_summary/
- "List all rad-analyst?" -> GET /v1/rad-analyst/
- "List all reporting-dates?" -> GET /v1/reporting-dates/
- "Get report details?" -> GET /v1/reports/{entity_type}/
- "List all schedule_a?" -> GET /v1/schedules/schedule_a/
- "List all by_employer?" -> GET /v1/schedules/schedule_a/by_employer/
- "List all by_occupation?" -> GET /v1/schedules/schedule_a/by_occupation/
- "List all by_size?" -> GET /v1/schedules/schedule_a/by_size/
- "List all by_candidate?" -> GET /v1/schedules/schedule_a/by_size/by_candidate/
- "List all by_state?" -> GET /v1/schedules/schedule_a/by_state/
- "List all by_candidate?" -> GET /v1/schedules/schedule_a/by_state/by_candidate/
- "List all totals?" -> GET /v1/schedules/schedule_a/by_state/by_candidate/totals/
- "List all totals?" -> GET /v1/schedules/schedule_a/by_state/totals/
- "List all by_zip?" -> GET /v1/schedules/schedule_a/by_zip/
- "List all efile?" -> GET /v1/schedules/schedule_a/efile/
- "Get schedule_a details?" -> GET /v1/schedules/schedule_a/{sub_id}/
- "List all schedule_a_form5?" -> GET /v1/schedules/schedule_a_form5/
- "List all schedule_b?" -> GET /v1/schedules/schedule_b/
- "List all by_purpose?" -> GET /v1/schedules/schedule_b/by_purpose/
- "List all by_recipient?" -> GET /v1/schedules/schedule_b/by_recipient/
- "List all by_recipient_id?" -> GET /v1/schedules/schedule_b/by_recipient_id/
- "List all efile?" -> GET /v1/schedules/schedule_b/efile/
- "Get schedule_b details?" -> GET /v1/schedules/schedule_b/{sub_id}/
- "List all schedule_c?" -> GET /v1/schedules/schedule_c/
- "Get schedule_c details?" -> GET /v1/schedules/schedule_c/{sub_id}/
- "List all schedule_d?" -> GET /v1/schedules/schedule_d/
- "Get schedule_d details?" -> GET /v1/schedules/schedule_d/{sub_id}/
- "List all schedule_e?" -> GET /v1/schedules/schedule_e/
- "List all by_candidate?" -> GET /v1/schedules/schedule_e/by_candidate/
- "List all efile?" -> GET /v1/schedules/schedule_e/efile/
- "List all by_candidate?" -> GET /v1/schedules/schedule_e/totals/by_candidate/
- "List all schedule_f?" -> GET /v1/schedules/schedule_f/
- "Get schedule_f details?" -> GET /v1/schedules/schedule_f/{sub_id}/
- "List all schedule_h4?" -> GET /v1/schedules/schedule_h4/
- "List all efile?" -> GET /v1/schedules/schedule_h4/efile/
- "List all state-election-office?" -> GET /v1/state-election-office/
- "List all by_entity?" -> GET /v1/totals/by_entity/
- "List all by_contributor?" -> GET /v1/totals/inaugural_committees/by_contributor/
- "Get total details?" -> GET /v1/totals/{entity_type}/
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- List endpoints may support pagination; check for limit, offset, or cursor params

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
