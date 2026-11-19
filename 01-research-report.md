# Apple-Supported WhatsAuto — Research Report

**Topic:** WhatsApp auto-reply with remote IP control, spreadsheet data logging, Apple + Android support, no-WhatsApp-ban approach  
**Prepared by:** @deep-researcher (Kilo R&D pipeline)  
**Research date:** 2026-11-19  
**Budget:** ₹0 (free / open-source only)  
**Market:** Global  
**Client requirement:** IP-based kill switch (stop app if client does not pay)

---

## Executive Verdict

**RECOMMENDED — Proceed with blueprint, with critical caveats.**

A zero-₹ WhatsApp auto-reply with IP-based remote control is technically feasible, but **no open-source solution gives zero WhatsApp-ban risk**. The trade-off is binary:

| Approach | Ban Risk | Cost | iOS Support | Best For |
|----------|----------|------|-------------|----------|
| Official WhatsApp Cloud API (pywa wrapper) | LOW — Meta-sanctioned | ₹0 only within 1,000 free service msgs/month; outbound templates cost ₹0.115–₹0.8631 each | Yes (cloud server-side, iOS device is just a client) | Production, client work, no ban tolerance |
| Baileys (MIT, unofficial) | HIGH — reverse-engineered protocol | ₹0 (self-hosted) | No automation on iOS (server-side only; iPhone can be primary device) | Experimental, disposable numbers only |
| whatsapp-web.js (Apache-2.0, unofficial) | HIGH — Chromium driving WhatsApp Web | ₹0 (self-hosted) | No automation on iOS | Experimental, disposable numbers only |

**Critical iOS finding:** An iOS app **cannot** read WhatsApp notifications (Apple sandbox siloes notifications per app) and **cannot** auto-send WhatsApp messages (URL scheme pre-fills composer but user must tap send). iOS automation must run server-side (WhatsApp Cloud API) or use the WhatsApp Business app's built-in auto-reply features (Away message, Greeting message, Quick replies) — none of which give you IP-based remote kill-switch control.

**Critical ban finding:** Using unofficial libraries (Baileys, whatsapp-web.js) violates WhatsApp ToS and carries a non-zero ban risk. The only zero-ban-risk path is the official WhatsApp Cloud API, which requires a verified business phone number and message templates for outbound messages outside the 24-hour customer service window.

**Fact-checker corrections applied (2026-11-19):**
- pywa is a third-party wrapper (david-lev/pywa, MIT, 600★), not Meta-endorsed — 'official Cloud API wrapper' is marketing, not fact.
- Evolution API license = NOASSERTION via GitHub API (Apache-2.0 claim is README-only).
- WAHA stars = 7,855 (not 7,817).
- python-whatsapp-bot = 33★, last push 2026-10-15 (not 2025-07-16).
- WPPConnect license = NOASSERTION (LGPL-3.0 not confirmed).

---

## Options Comparison Table

| # | Option | Type | License | Stars | Last Active | Ban Risk | iOS Notification Read | Auto-Send on iOS | IP Kill Switch | Cost (₹0?) |
|---|--------|------|---------|-------|-------------|----------|----------------------|------------------|----------------|------------|
| 1 | WhatsApp Cloud API + pywa | Official API wrapper | MIT (pywa) | 600 | 2026-11-12 | LOW | No (server-side) | No (server-side) | Yes | ₹0 only if ≤1,000 free service msgs/month + no outbound templates |
| 2 | Baileys | Unofficial library | MIT | 11,668 | 2026-11-17 | HIGH | No (server-side) | No | Yes | ₹0 (self-hosted) |
| 3 | whatsapp-web.js | Unofficial library | Apache-2.0 | 22,932 | 2026-11-15 | HIGH | No (server-side) | No | Yes | ₹0 (self-hosted) |
| 4 | WAHA | Unofficial server | Apache-2.0 | 7,855 | 2026-11-11 | HIGH | No (server-side) | No | Yes | ₹0 (self-hosted) |
| 5 | Evolution API | Unofficial + official hybrid | NOASSERTION (Apache-2.0 README-only) | 10,153 | 2026-11-12 | HIGH (Baileys) / LOW (Cloud API) | No | No | Yes | ₹0 (self-hosted) / ₹+ (Cloud API) |
| 6 | WhatsApp Business App (built-in) | Native app | Proprietary | — | — | N/A (official feature) | N/A | Limited (away/greeting only) | No — no IP control | Free |
| 7 | WhatsApp native scheduler (iOS 17+) | Native feature | Proprietary | — | — | N/A | N/A | Scheduled send only | No | Free |

**Top recommendation:** WhatsApp Cloud API + pywa (MIT) — lowest ban risk, works on iOS (server-side), gives you full server-side control for IP kill switch and spreadsheet logging. Trade-off: ₹0 only within free tier limits. pywa is a third-party community wrapper, not Meta-endorsed.

---

## Deep-Dive Findings

### 1. WhatsApp Cloud API (Meta official)
- **Pricing:** Per-message, effective 2025-07-01. Only delivered business→user messages charged; user→business free. India rates (2026-10-01): Marketing ₹0.8631, Utility ₹0.115, Authentication ₹0.115, Service ₹0.115 after free tier. Note: Meta may update rates quarterly (Jan 1 / Apr 1 / Jul 1 / Oct 1); re-verify before quoting.
- **Free tier:** First 1,000 service messages/month per business phone number free (since 2026-10-01). Unused do not roll over.
- **Rate limits:** New portfolio = 250 unique users/24-hour outside customer service window. Scalable to 2,000 then auto-scale (10,000 → 100,000 → Unlimited).
- **Templates:** Outbound messages outside the 24-hour customer service window require pre-approved templates (Authentication/Marketing/Utility). Max 100 templates/hour created per WABA.
- **Customer service window:** 24 hours; opens/resets on each user message. Free-form replies only within open window.
- **Ban risk:** Using official API carries no ban risk from usage itself. Policy violations (spam, low quality, template misuse) can pause templates, reduce limits, or restrict the number.
- **iOS:** Works as cloud server-side API; iPhone/iOS device is just a WhatsApp client. Coexistence with WhatsApp Business app supported on iPhone (v2.24.17+).
- **Sources:** Meta for Developers WhatsApp Business Platform docs (pricing, get-started, templates, messaging limits, webhooks), verified 2026-11-19.

### 2. Open-Source Unofficial Libraries
- **Baileys (WhiskeySockets/Baileys):** MIT, 11,668 stars, last push 2026-11-17. WebSocket multi-device, no browser. HIGH ban risk — reverse-engineered protocol, maintainers discourage bulk/automated messaging.
- **whatsapp-web.js (wwebjs):** Apache-2.0, 22,932 stars, last push 2026-11-15. Puppeteer + Chromium driving real WhatsApp Web. HIGH ban risk — project states 'not guaranteed you will not be blocked.'
- **WAHA (devlikeapro/waha):** Apache-2.0, 7,855 stars, last push 2026-11-11. Self-hosted REST server. HIGH ban risk with browser engines (WEBJS/WPP run real WhatsApp Web).
- **Evolution API (evolution-foundation/evolution-api):** License = NOASSERTION via GitHub API (Apache-2.0 claim is README-only, not confirmed). 10,153 stars, last push 2026-11-12. HIGH ban risk in Baileys-connector mode; LOW only with official Cloud API integration.
- **Python Cloud API wrappers (LOW ban risk):** pywa (MIT, david-lev/pywa, 600★, pushed 2026-11-12 — third-party wrapper, NOT Meta-endorsed), python-whatsapp-bot (MIT, radi-dev, 33★, pushed 2026-10-15 — third-party wrapper, NOT Meta-endorsed), heyoo (MIT), whatsapp-sdk (MIT). Use official Cloud API — no 'unofficial client' ban vector.
- **Excluded by license:** whatsmeow (MPL-2.0 copyleft), WPPConnect (NOASSERTION via GitHub API — LGPL-3.0 not confirmed), Venom-bot (404/stale).

### 3. iOS WhatsApp Automation Limitations
- **iOS app reading WhatsApp notifications: NO.** Apple App Sandbox siloes notifications per app. UNUserNotificationCenter only manages your own app's notifications. The com.apple.developer.usernotifications.filtering entitlement (iOS 13.3+) allows a Notification Service Extension to suppress your own app's notifications only, requires Apple's explicit per-app approval, and does NOT let you read WhatsApp notifications.
- **iOS app auto-sending WhatsApp messages: NO fully automatic.** URL scheme (whatsapp://send?phone=<number>&text=<text> / https://wa.me/<number>?text=<text>) opens WhatsApp with pre-filled composer; user must tap Send. iOS Shortcuts same limitation — can open WhatsApp with pre-filled message but cannot tap the send button. 'Ask Before Running' can be disabled but the final send step still requires manual confirmation.
- **PWA reading WhatsApp notifications on iOS: NO.** iOS Web Push (16.4+) only delivers the PWA's own notifications via Push API/Service Worker; cannot read WhatsApp or any other app's notifications.
- **WhatsApp Business API on iOS: Yes** as cloud service; server-side automation works regardless of end-user device. Coexistence with WhatsApp Business app supported on iPhone (v2.24.17+), capped at 20 msgs/sec for coexistence numbers.
- **Alternatives:** WhatsApp Business app built-in auto-replies (Away/Greeting/Quick replies — reactive only), WhatsApp native scheduler (v25.10+, iOS 17+ — one-shot only, max 30 days ahead), iOS Shortcuts + Personal Automations (manual tap required).
- **Sources:** Apple developer docs (App Sandbox, UNUserNotificationCenter), WhatsApp FAQ URL scheme, Meta Cloud API docs, WebKit Web Push blog, verified 2026-11-19.

### 4. Anti-Ban / Account Safety
- **Ban triggers:** Bulk/automated messaging is explicit ToS violation. WhatsApp bans accounts sending unwanted automated messages (ML + user reports). Unofficial/modified clients and scraping prohibited.
- **Minimize ban risk:** Use dedicated disposable number (never primary personal/business). Warm up new numbers (profile photo, saved contacts, real 2-way conversations) before automating. Only message opted-in recipients. Honor opt-out/block immediately. Prefer replies/inbound-initiated traffic over cold outbound. Randomize message content and timing.
- **Delay/randomization:** Random gaps between messages. bailey-antiban implements Gaussian jitter, typing simulation (~30ms/char), warm-up ramp. OpenWA pacing: warmup 20→100 msgs/day by session age.
- **Daily limits:** Official Cloud API = 250 unique users/24h (new portfolio) → 2,000 → auto-scale. Unofficial clients: NO published stable cap; community guardrails suggest ~20→100 msgs/day warmup for new numbers.
- **Sources:** WhatsApp Messaging Guidelines, WhatsApp Help Center (automated/bulk messaging, use responsibly, account bans), Meta for Developers messaging limits, OpenWA safe-sending, verified 2026-11-19.

---

## Risks & Constraints

| Risk | Impact | Mitigation |
|------|--------|------------|
| No iOS notification reading | High | Accept server-side model; automation runs on your server, iPhone is just a WhatsApp client |
| WhatsApp ban risk with unofficial libs | High | Use official Cloud API + pywa (LOW ban risk). If using Baileys/whatsapp-web.js, use disposable numbers only |
| ₹0 budget limitation | Medium | Cloud API free tier = 1,000 service msgs/month. Outbound templates cost money. Self-hosted unofficial libs are ₹0 but HIGH ban risk |
| No IP kill switch on native WhatsApp Business app | High | Build your own server-side control (your server decides whether to forward messages to WhatsApp API) |
| Template approval required for outbound | Medium | Use free-form replies within 24h CSW; pre-approve templates for outbound notifications |
| Business phone number required | Low | Must own a number able to receive SMS/voice; cannot use WhatsApp personal app number without removing it first |
| pywa is third-party (not Meta-endorsed) | Low | Verify pywa repo (david-lev/pywa) is actively maintained before production use |

---

## Verified Sources

| # | Area | Source URL | Date Verified |
|---|------|------------|---------------|
| 1 | WhatsApp Cloud API pricing (India INR card, free tier) | https://developers.facebook.com/documentation/business-messaging/whatsapp/pricing | 2026-11-19 |
| 2 | WhatsApp Cloud API get-started (access, phone numbers) | https://developers.facebook.com/documentation/business-messaging/whatsapp/get-started | 2026-11-19 |
| 3 | WhatsApp Cloud API templates overview | https://developers.facebook.com/docs/whatsapp/message-templates/guidelines/ | 2026-11-19 |
| 4 | WhatsApp Cloud API messaging limits | https://developers.facebook.com/documentation/business-messaging/whatsapp/messaging-limits | 2026-11-19 |
| 5 | WhatsApp Cloud API webhooks | https://developers.facebook.com/documentation/business-messaging/whatsapp/webhooks/overview | 2026-11-19 |
| 6 | WhatsApp Cloud API throughput | https://developers.facebook.com/documentation/business-messaging/whatsapp/throughput | 2026-11-19 |
| 7 | WhatsApp Business FAQ | https://whatsappbusiness.com/resources/faq/ | 2026-11-19 |
| 8 | Baileys GitHub repo | https://github.com/WhiskeySockets/Baileys | 2026-11-19 |
| 9 | whatsapp-web.js GitHub repo | https://github.com/wwebjs/whatsapp-web.js | 2026-11-19 |
| 10 | WAHA GitHub repo | https://github.com/devlikeapro/waha | 2026-11-19 |
| 11 | Evolution API GitHub repo | https://github.com/evolution-foundation/evolution-api | 2026-11-19 |
| 12 | pywa (PyPI/GitHub) | https://github.com/david-lev/pywa | 2026-11-19 |
| 13 | WhatsApp Messaging Guidelines | https://www.whatsapp.com/legal/messaging-guidelines | 2026-11-19 |
| 14 | WhatsApp Help Center: automated/bulk messaging | https://faq.whatsapp.com/5957850900902049 | 2026-11-19 |
| 15 | WhatsApp Help Center: account bans | https://faq.whatsapp.com/723378546580115 | 2026-11-19 |
| 16 | OpenWA safe sending | https://docs.open-wa.org/guides/safe-sending | 2026-11-19 |
| 17 | Apple developer docs (notification sandboxing) | https://developer.apple.com/documentation/usernotifications | 2026-11-19 |

**Fact-checker audit:** Completed 2026-11-19. All 25 claims audited; corrections applied above. Key corrections: pywa is third-party (not Meta-endorsed), Evolution API license unverified, WAHA star count corrected, WhatsApp Business API URL scheme confirmed via WhatsApp FAQ.

