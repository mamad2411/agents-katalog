---
name: jd-price-protection
description: Applies JD.com price protection for eligible recent orders through the JD price protection page. Use when the user asks to run JD/Jingdong/京东 price protection, 保价, 价保, 价格保护, or scheduled JD price-protection checks.
---

# JD Price Protection

## Scope

Use this skill to help the user apply for JD.com price protection on eligible orders. The default scope is the last 30 days from the current date unless the user gives a different date range. Never click orders older than the requested range.

Submitting price-protection applications is an external account action. If the user explicitly asks to apply for price protection or a scheduled automation invokes this skill, that is authorization to click eligible "申请价保" buttons. Do not make purchases, cancel orders, change account settings, save payment methods, or reveal private account data.

## Prerequisites

1. Use the in-app browser control skill if available, and follow its documentation before browser work.
2. Open or reuse the JD price protection page:
   `https://pcsitepp-fm.jd.com/`
3. The user must already be logged in to JD in the in-app browser. If the page redirects to `passport.jd.com` or shows a login/CAPTCHA/verification challenge:
   - Show the browser to the user.
   - Ask the user to complete login or verification themselves.
   - Do not request, type, store, or expose passwords, SMS codes, OTPs, or CAPTCHA solutions unless the browser safety policy explicitly allows the user-confirmed action.
4. If a scheduled run cannot access an authenticated JD browser session, report that login is required and stop without attempting account work.

## Workflow

1. Confirm the page title or visible text indicates "我的京东-价格保护" or "价格保护".
2. Gather current eligible buttons from `#dataList`:
   - Find rows whose button id starts with `applyBT_`.
   - Parse `applyBT_<orderId>_<skuId>_<sequence>`.
   - Read each order header time from the nearest preceding `.tr-th .time`.
   - Group buttons by `orderId`.
3. Filter groups:
   - Keep only orders within the requested date range, defaulting to last 30 days.
   - Skip older orders and mention the oldest skipped date/order in the summary if relevant.
   - If one order has multiple eligible SKUs, click only one "申请价保" button for that order. JD's page code submits all currently eligible SKUs in that order together.
4. Apply:
   - Scroll the target button into view.
   - Verify the exact target is still present and still says "申请价保".
   - Click once.
   - Wait about 3-5 seconds before the next order to avoid frequent-operation errors.
   - After each click, read the affected order rows and record button text/result text, such as "已申请", "当前无差价", "暂不支持价保", or a refund amount.
5. Continue through lazy-loaded content:
   - Re-scan after each batch because the page may load additional older orders while scrolling.
   - Continue while there are eligible "申请价保" buttons inside the date range.
   - Stop when no in-range eligible buttons remain, or when only older-than-range buttons remain.

## Page Behavior Notes

The current JD PC page builds requests in `priceskus-pcnew_v2_1.js`:

- List pull: `siteppPC_priceskusPull`
- Apply: `siteppPC_orderProtectApply`
- Result polling: `siteppPC_moreApplyResult`

The apply request body contains `orderId` and `skuIds`; `sequence` is for DOM lookup only. The page signs requests with `h5st` and an `x-api-eid-token`, so prefer real browser interaction over manually recreating API calls.

## Output

End with a concise summary:

- Number of orders and SKUs submitted.
- Any successful refund amount shown by JD.
- Common failure/status messages, grouped briefly.
- Any in-range orders not submitted and why.
- Any older orders intentionally skipped.
