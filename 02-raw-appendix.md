# Apple-Supported WhatsAuto — Raw Appendix

**Topic:** WhatsApp auto-reply with remote IP control, spreadsheet data logging, Apple + Android support, no-WhatsApp-ban approach  
**Prepared by:** @web-scout + @fact-checker (Kilo R&D pipeline)  
**Research date:** 2026-11-19  
**Budget:** ₹0 (free / open-source only)

---

## Table 1 — WhatsApp Business Cloud API Pricing (India INR, effective 2026-10-01, pre-tax)

| Category | Rate per message (India) | Notes |
|----------|--------------------------|-------|
| Marketing | ₹0.8631 | Increased 2026-01-01 |
| Utility | ₹0.115 | |
| Authentication | ₹0.115 | |
| Service (after free tier) | ₹0.115 | Within 24h CSW is free |
| Authentication-International (to Indian number from abroad) | ₹2.4971 | |
| Meta Business Agent (AI) | .00 USD / 1M tokens | ~4–5¢/message |

**Free tier:** First 1,000 service messages/month per business phone number free (since 2026-10-01). Unused do not roll over.

**Source:** https://developers.facebook.com/documentation/business-messaging/whatsapp/pricing

---

## Table 2 — Official Cloud API Rate Limits & Limits

| Parameter | Value | Source |
|-----------|-------|--------|
| New portfolio messaging limit | 250 unique users/24-hour outside CSW | https://developers.facebook.com/documentation/business-messaging/whatsapp/messaging-limits |
| Scalable limit | 2,000 (via scaling path) | Same |
| Auto-scale tiers | 10,000 → 100,000 → Unlimited | Same |
| Auto-scale condition | ≥50% limit utilization in 7 days + high quality rating | Same |
| Template creation limit | Max 100 templates/hour per WABA | https://developers.facebook.com/docs/whatsapp/message-templates/guidelines/ |
| Unverified portfolio template cap | 250 templates | Same |
| Verified portfolio + approved display name | 6,000 templates | Same |
| Template auto-archive | After 12 months inactive | Same |
| Customer service window | 24 hours; resets on each user message | https://developers.facebook.com/documentation/business-messaging/whatsapp/webhooks/overview |
| Free-form message limit | 4,096 characters | Meta docs |
| Template body limit | 1,024 characters | Meta docs |
| Pair rate limit | ~1 msg per 6s to same user (~45 burst) | Meta docs |
| Default throughput | 80 msgs/sec per number | https://developers.facebook.com/documentation/business-messaging/whatsapp/throughput |
| Auto-upgrade throughput | Up to 1,000 msgs/sec (Unlimited tier + 100K unique users/24h + quality YELLOW+) | Same |
| Coexistence number throughput | 20 msgs/sec fixed | Meta docs |

---

## Table 3 — Open-Source WhatsApp Automation Libraries (verified via GitHub API, 2026-11-19)

| # | Library | License | Stars | Last Push | Architecture | Ban Risk | Notes |
|---|---------|---------|-------|-----------|--------------|----------|-------|
| 1 | Baileys (WhiskeySockets/Baileys) | MIT | 11,668 | 2026-11-17 | WebSocket multi-device, no browser | HIGH | Unofficial, reverse-engineered protocol |
| 2 | whatsapp-web.js (wwebjs) | Apache-2.0 | 22,932 | 2026-11-15 | Puppeteer + Chromium driving WhatsApp Web | HIGH | Project: 'not guaranteed you will not be blocked' |
| 3 | WAHA (devlikeapro/waha) | Apache-2.0 | 7,855 | 2026-11-11 | Self-hosted REST server; WEBJS/WPP/NOWEB/GOWS engines | HIGH (browser engines) | |
| 4 | Evolution API (evolution-foundation/evolution-api) | NOASSERTION (Apache-2.0 README-only) | 10,153 | 2026-11-12 | REST server; Baileys connector OR official Cloud API | HIGH (Baileys mode) / LOW (Cloud API mode) | License NOT confirmed by primary source |
| 5 | pywa (david-lev/pywa) | MIT | 600 | 2026-11-12 | Python wrapper for official Cloud API | LOW | Third-party wrapper, NOT Meta-endorsed |
| 6 | python-whatsapp-bot (radi-dev) | MIT | 33 | 2026-10-15 | Official Cloud API wrapper | LOW | Third-party wrapper |
| 7 | heyoo (Neurotech-HQ) | MIT | — | created 2022-05-20, 179 commits | Official Cloud API wrapper | LOW | |
| 8 | whatsapp-sdk (alejandrovelez243) | MIT | — | created 2025-09-07, 26 commits | Official Cloud API SDK | LOW | |

**Excluded by license:** whatsmeow (MPL-2.0 copyleft), WPPConnect (NOASSERTION via GitHub API — LGPL-3.0 not confirmed), Venom-bot (404/stale).

**Repo URLs:**
- Baileys: https://github.com/WhiskeySockets/Baileys
- whatsapp-web.js: https://github.com/wwebjs/whatsapp-web.js
- WAHA: https://github.com/devlikeapro/waha
- Evolution API: https://github.com/evolution-foundation/evolution-api
- pywa: https://github.com/david-lev/pywa
- python-whatsapp-bot: https://github.com/radi-dev/python-whatsapp-bot
- heyoo: https://github.com/Neurotech-HQ/heyoo
- whatsapp-sdk: https://github.com/alejandrovelez243/whatsapp-sdk

---

## Table 4 — iOS WhatsApp Automation Limitations (verified 2026-11-19)

| # | Question | Short Answer | Source |
|---|----------|--------------|--------|
| 1 | Can an iOS app read WhatsApp notifications? | NO — Apple App Sandbox siloes notifications per app | https://developer.apple.com/documentation/security/protecting-user-data-with-app-sandbox |
| 2 | Can an iOS app auto-send WhatsApp messages? | NO fully automatic — URL scheme pre-fills composer, user must tap Send | https://faq.whatsapp.com/en/iphone/23559013/ |
| 3 | Can a PWA read WhatsApp notifications on iOS? | NO — iOS Web Push only delivers the PWA's own notifications | https://webkit.org/blog/13878/web-push-for-web-apps-on-ios-and-ipados/ |
| 4 | Does WhatsApp Business API work on iOS? | Yes as cloud service; server-side, not iOS-native | https://developers.facebook.com/documentation/business-messaging/whatsapp/overview |
| 5 | WhatsApp Business app coexistence on iPhone? | Yes (app v2.24.17+), capped at 20 msgs/sec | https://developers.facebook.com/documentation/business-messaging/whatsapp/embedded-signup/onboarding-business-app-users |

**iOS Alternatives for auto-reply:**
| Alternative | Auto-reply? | Scheduled send? | Cost | Risk |
|-------------|-------------|-----------------|------|------|
| WhatsApp Business app (Away/Greeting/Quick replies) | Yes (reactive only) | No | Free | None (official) |
| WhatsApp native scheduler (v25.10+, iOS 17+) | No | Yes (one-shot, max 30 days) | Free | None (official) |
| iOS Shortcuts + Personal Automations | No | Manual tap required | Free | None (official) |
| WhatsApp Cloud API | Yes | Yes | Per-message fees | None (official) |
| Third-party cloud WhatsApp API | Yes | Yes | Varies | Account ban risk (unofficial) |

---

## Table 5 — Anti-Ban / Account Safety (verified 2026-11-19)

| Area | Finding | Source |
|------|---------|--------|
| Ban triggers | Bulk/automated messaging is explicit ToS violation; ML + user reports detect it | https://www.whatsapp.com/legal/messaging-guidelines |
| Unofficial clients | Prohibited; can lead to temporary then permanent ban | https://faq.whatsapp.com/5957850900902049 |
| Spam reports/blocks | Count against account; repeated → restriction/ban | https://faq.whatsapp.com/723378546580115 |
| Accounts banned/month | Over 2M for bulk/automated behavior; >75% without recent user report | WhatsApp anti-abuse white paper |
| Ban minimization | Use dedicated disposable number; warm up new numbers; only opt-in recipients; honor opt-out; randomize delays | https://docs.open-wa.org/guides/safe-sending |
| Delay/randomization | Random gaps between messages; bailey-antiban implements Gaussian jitter, typing sim (~30ms/char), warm-up ramp | https://www.npmjs.com/package/baileys-antiban |
| OpenWA pacing | Warmup 20→100 msgs/day by session age; breaker threshold 5 consecutive failures | https://openwa.dev/docs/guides/rate-limits/ |
| Cloud API daily limit | 250 unique users/24h (new) → 2,000 → auto-scale | Meta for Developers messaging limits |
| Cloud API throughput | 80 msgs/sec default; up to 1,000 msgs/sec auto-upgrade | Meta for Developers throughput |
| Pair rate limit | ~1 msg per 6s to same user (~45 burst) | Meta for Developers |

---

## Table 6 — Excluded Libraries (with reasons)

| Library | License | Reason Excluded |
|---------|---------|-----------------|
| whatsmeow (tulir/whatsmeow) | MPL-2.0 | Copyleft license — fails MIT/Apache-2.0 filter |
| WPPConnect (@wppconnect-team/wppconnect) | NOASSERTION | License not confirmed by GitHub API — inspect LICENSE file before adoption |
| Venom-bot (oushun/venom-bot) | Apache-2.0 claimed | Repo returns 404; last stable release Nov 2024 (~2 years stale) — unverifiable/inactive |

---

## @fact-checker Audit Table

**Status:** Completed 2026-11-19. All 25 claims audited.

| Claim | Verdict | Corrected Value | Source URL |
|-------|---------|-----------------|------------|
| Per-message pricing eff. 2025-07-01; only delivered business→user charged | CONFIRMED | — | https://developers.facebook.com/documentation/business-messaging/whatsapp/pricing |
| India: Marketing ₹0.8631, Utility ₹0.115, Authentication ₹0.115, Service ₹0.115/msg after free tier | CONFIRMED | Meta INR rate card eff. 2026-10-01 | https://developers.facebook.com/documentation/business-messaging/whatsapp/pricing |
| Free tier: first 1,000 service messages/month per business phone number free since 2026-10-01 | CONFIRMED | — | https://developers.facebook.com/documentation/business-messaging/whatsapp/pricing |
| Portfolio limit: 250 unique users/24h outside CSW; scales to 2,000 then auto-scales | CONFIRMED | Tiers continue 10,000 / 100,000 / Unlimited | https://developers.facebook.com/documentation/business-messaging/whatsapp/messaging-limits |
| Templates must be APPROVED before sending; max 100 created/hour per WABA | CONFIRMED | — | https://developers.facebook.com/docs/whatsapp/message-templates/guidelines/ |
| CSW: 24-hour; opens/resets on each user message | CONFIRMED | — | https://developers.facebook.com/documentation/business-messaging/whatsapp/pricing |
| Official API: no ban risk from usage itself; violations can pause/reduce limits/restrict number | CONFIRMED (nuanced) | — | https://www.whatsapp.com/legal/terms-of-service |
| Cloud API works on iOS as cloud service; coexistence supported on iPhone | CONFIRMED | — | https://developers.facebook.com/documentation/business-messaging/whatsapp/embedded-signup/onboarding-business-app-users |
| Baileys: MIT, 11,668★, pushed 2026-11-17, HIGH ban risk | CONFIRMED (repo data) | Ban risk is assessment, not primary fact | https://api.github.com/repos/WhiskeySockets/Baileys |
| whatsapp-web.js: Apache-2.0, 22,932★, pushed 2026-11-15, HIGH ban risk | CONFIRMED (repo data) | — | https://api.github.com/repos/wwebjs/whatsapp-web.js |
| WAHA: Apache-2.0, 7,855★, pushed 2026-11-11 | CORRECTED | Stars = 7,855 (not 7,817) | https://api.github.com/repos/devlikeapro/waha |
| Evolution API: Apache-2.0 + brand conditions, 10,153★ | FLAGGED | license.spdx_id = NOASSERTION; Apache-2.0 is README-only | https://api.github.com/repos/evolution-foundation/evolution-api |
| pywa: MIT, official Cloud API wrapper, LOW ban risk | FLAGGED / PARTIAL | Repo = david-lev/pywa, 600★, pushed 2026-11-12; third-party wrapper, not Meta-endorsed | https://api.github.com/repos/david-lev/pywa |
| python-whatsapp-bot (radi-dev): MIT, official Cloud API wrapper, LOW ban risk | FLAGGED / PARTIAL | MIT ✓, 33★, pushed 2026-10-15; third-party wrapper | https://api.github.com/repos/radi-dev/python-whatsapp-bot |
| whatsmeow: MPL-2.0 copyleft, excluded | CONFIRMED | — | https://api.github.com/repos/tulir/whatsmeow |
| WPPConnect: LGPL-3.0-or-later, excluded | FLAGGED | license.spdx_id = NOASSERTION; LGPL not confirmed by primary source | https://api.github.com/repos/wppconnect-team/wppconnect |
| iOS app cannot read WhatsApp notifications | CONFIRMED | — | https://developer.apple.com/documentation/usernotifications/unusernotificationcenter |
| iOS app cannot auto-send; URL scheme pre-fills composer, user taps send | CONFIRMED | — | https://faq.whatsapp.com/5913398998672934 |
| WhatsApp Business API works on iOS as cloud service | CONFIRMED | — | https://developers.facebook.com/documentation/business-messaging/whatsapp/throughput |
| PWA cannot read WhatsApp notifications on iOS | CONFIRMED | — | https://developer.apple.com/documentation/usernotifications/unusernotificationcenter |
| Bulk/automated messaging is explicit ToS violation | CONFIRMED | — | https://www.whatsapp.com/legal/terms-of-service |
| Dedicated disposable number; warm up new numbers | NOT VERIFIABLE | Operational best practice; no primary source | — |
| Random delays/jitter; bailey-antiban implements Gaussian jitter | NOT VERIFIABLE | README-only third-party claim | — |
| Opt-in required; honor opt-out/block immediately | CONFIRMED | — | https://whatsappbusiness.com/policy/ |
| Cloud API: 80 msgs/sec default per number; ~1 msg/6s to same user | CONFIRMED | — | https://developers.facebook.com/documentation/business-messaging/whatsapp/throughput |

**Hidden risks:**
1. India INR figures may change quarterly (Jan 1 / Apr 1 / Jul 1 / Oct 1); re-verify before quoting.
2. Evolution API and WPPConnect licenses are NOASSERTION via GitHub API — inspect LICENSE files directly before adoption.
3. WAHA star count may drift; re-verify at decision time.
4. pywa and python-whatsapp-bot are third-party community wrappers, not Meta-endorsed.
5. Unofficial libraries automate personal WhatsApp accounts, contravening ToS ban on bulk/auto-messaging → account ban risk.
6. Messaging limits are portfolio-level and shared across all numbers — adding numbers does not multiply capacity.
7. Service messages charged after 1,000-message free tier from 2026-10-01; utility templates inside open CSW also charged from that date.
8. India billing localization: INR migration required by 2026-12-31 or message delivery stops 2027-01-01.

