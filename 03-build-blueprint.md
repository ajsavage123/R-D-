## Scorecard (Stamped by @blueprint-critic)

**Verdict:**  
**Feasibility:**  
**Rules & Constraints:**  
**Main Risk:**  

---

# Apple-Supported WhatsAuto — Build Blueprint

## PART 1: PRODUCT BRIEF (Plain English for Founder — Zero Code)

### 1. Goal & How It Works

**One-Sentence Goal:** A WhatsApp auto-reply system that reads incoming messages, sends automatic replies, logs queries/orders to a spreadsheet, and lets you remotely kill the app via IP control if a client doesn't pay — working on both Apple (iOS) and Android devices without getting the WhatsApp account banned.

**Step-by-Step Flow:**
1. Customer sends a WhatsApp message to your business number.
2. WhatsApp delivers the message to your server (via WhatsApp Cloud API webhook).
3. Your server checks the IP-based kill switch: if the client's access is revoked (non-payment), the server stops processing and sends a service suspended message instead.
4. If active, your server sends an auto-reply (free-form within 24-hour customer service window, or pre-approved template outside it).
5. Your server logs the query/order details (customer phone, message, timestamp, response) to a spreadsheet (Google Sheets or local CSV).
6. On iPhone/iPad, the customer sees the auto-reply in WhatsApp normally — no special iOS app needed. The automation runs entirely on your server.

**Day-1 Scope (Milestone 1):**
- WhatsApp Cloud API webhook receiving messages
- Auto-reply to incoming messages (within 24h window)
- IP-based kill switch (server-side control)
- Spreadsheet logging (queries/orders count)
- iOS + Android compatible (server-side, works on any WhatsApp client)
- No WhatsApp ban risk (official Cloud API only)

**Saved for Later (Milestones 2–3):**
- Outbound message templates (Marketing/Utility/Authentication) for proactive messaging
- Multi-client management (separate phone numbers per client)
- Advanced analytics dashboard
- Mobile app for you to manage kill switches remotely

---

## 2. Chosen Tools & Requirements

| Component | Chosen Tool | Why This One | License | Limits / Cost |
|-----------|-------------|--------------|---------|----------------|
| Messaging API | WhatsApp Cloud API (Meta) | Only zero-ban-risk option; works on iOS + Android; server-side | Meta Terms (free to use) | 250 unique users/24h (new portfolio); 1,000 free service msgs/month; outbound templates ₹0.115–₹0.8631 each (India) |
| API Wrapper | pywa (Python) | MIT-licensed, actively maintained (david-lev/pywa, 600★), third-party wrapper for official Cloud API | MIT | Third-party wrapper, NOT Meta-endorsed |
| Server Runtime | Python | pywa requires Python; widely available | — | — |
| Spreadsheet Logging | Google Sheets API or local CSV | Free tier available; easy to query | Google Sheets API (free tier) / CSV format | — |
| IP Kill Switch | Custom server middleware | Full control — your server decides whether to process | Custom | — |
| Hosting | Any Python-capable VPS (or local) | Full control over IP and kill switch | Varies | VPS cost not specified |

**Rejected Alternatives:**
- Baileys (MIT, unofficial): HIGH ban risk — reverse-engineered protocol; violates WhatsApp ToS. Rejected for production client work.
- whatsapp-web.js (Apache-2.0, unofficial): HIGH ban risk — Chromium driving WhatsApp Web; project itself warns of blocking. Rejected.
- WAHA / Evolution API (unofficial modes): HIGH ban risk in unofficial connector modes. Rejected.
- WhatsApp Business App built-in auto-reply: No IP kill switch possible; reactive only. Rejected as primary solution.

---

## 3. Safety & Guardrails

- Ban prevention: Use ONLY official WhatsApp Cloud API via pywa. Never use Baileys, whatsapp-web.js, or any unofficial client for client work.
- Opt-in only: Only message customers who have contacted you first (inbound-initiated). Honor opt-out/block immediately.
- 24-hour window: Free-form replies only within 24 hours of customer's last message. Outside window, use pre-approved templates only.
- Rate limiting: Stay within 250 unique users/24-hour limit for new portfolios. Implement message queue with random delays to avoid burst sending.
- Disposable number: Use a dedicated business phone number, never your primary personal WhatsApp number.
- IP kill switch: Your server maintains an allow/deny list keyed by client IP address. If payment is overdue, the server rejects all processing for that IP.
- Data privacy: Log only what's needed (phone, message text, timestamp, response). Do not store sensitive customer data unnecessarily.
- pywa third-party: Verify pywa repo (david-lev/pywa) is actively maintained before production use; it is a community wrapper, not Meta-endorsed.

---

## 4. Build Phases (Milestones 1 → 3)

**Milestone 1 (Working Prototype):**
- Deliverables: Python server with pywa + WhatsApp Cloud API webhook; auto-reply to inbound messages; IP kill switch middleware; CSV/Google Sheets logging; basic README with setup instructions.
- Test: Send a WhatsApp message to your business number → receive auto-reply → verify entry appears in spreadsheet → toggle kill switch → verify message is blocked.
- Pass criteria: Auto-reply works, kill switch blocks messages, spreadsheet logs entries, no WhatsApp ban warnings.

**Milestone 2 (Core System):**
- Deliverables: Multi-client support (separate phone numbers per client); outbound message templates (pre-approved); web dashboard to manage clients and kill switches; payment integration trigger for kill switch.
- Test: Add a client → assign phone number → send outbound template → toggle kill switch from dashboard → verify blocking.
- Pass criteria: Multi-client isolation works, outbound templates send, dashboard kill switch functions.

**Milestone 3 (Production Ready):**
- Deliverables: Rate limiting with warm-up ramp; message queue with jitter; analytics dashboard (queries/orders per client); billing integration; production VPS deployment with monitoring.
- Test: Handle messages within 250 unique users/24h limit; analytics accurately track queries/orders; billing triggers kill switch automatically.
- Pass criteria: Stable at production volume, billing integration triggers kill switch, monitoring alerts on issues.

---

## PART 2: ENGINEERING SPECS (For AI Code Mode Only)

### 5. System Architecture

`
Customer (iOS/Android) ── WhatsApp Cloud API ── Your Server (Python + pywa) ── Spreadsheet Log
                                ▲                                              │
                                │                                              ▼
                                └────────── Webhook (JSON POST) ◄── IP Kill Switch Middleware ◄── Clients CSV
`

Data flow: Customer → WhatsApp Cloud API → Your Server webhook → IP Kill Switch check → Auto-reply → Spreadsheet log → WhatsApp Cloud API → Customer

### 6. Data Structure & Hard Rules

**Client Table (clients.csv or Google Sheets):**
| Field | Type | Required | Description |
|-------|------|----------|-------------|
| client_id | string | Yes | Unique client identifier |
| phone_number | string | Yes | WhatsApp business number (E.164 format) |
| ip_address | string | Yes | Client IP address for kill switch |
| is_active | boolean | Yes | Kill switch: true = active, false = suspended |
| last_payment_date | date | No | Last payment received |
| created_at | timestamp | Yes | Client onboarding date |

**Message Log Table (messages.csv or Google Sheets):**
| Field | Type | Required | Description |
|-------|------|----------|-------------|
| message_id | string | Yes | WhatsApp message ID |
| client_phone | string | Yes | Customer's WhatsApp number |
| inbound_text | string | Yes | Customer's message |
| outbound_text | string | Yes | Auto-reply sent |
| timestamp | timestamp | Yes | Message received time |
| is_killed | boolean | Yes | Was kill switch active at time? |

**Hard Rules:**
1. IP kill switch checked BEFORE any message processing — if is_active=false for the client's IP, send service suspended and do not log as normal query.
2. Outbound messages only within 24-hour customer service window unless using pre-approved template.
3. No bulk/broadcast messaging — only reply to inbound messages.
4. Implement random delay before sending any reply (anti-ban).
5. Dedicated phone number per client (no sharing between personal and business).

### 7. Interfaces & Connections

| Interface | Direction | Protocol | Endpoint | Auth |
|-----------|-----------|----------|----------|------|
| WhatsApp Cloud API Webhook | Inbound (to your server) | HTTPS POST | /webhook | Verify token (challenge-response) |
| WhatsApp Cloud API Send Message | Outbound (from your server) | HTTPS POST | https://graph.facebook.com/v22.0/{phone_number_id}/messages | Bearer token (system user access token) |
| Google Sheets API | Outbound (logging) | HTTPS POST/GET | https://sheets.googleapis.com/v4/spreadsheets/{spreadsheetId}/values/{range}:append | OAuth2 / API key |
| Kill Switch Admin | Inbound (your dashboard) | HTTPS GET/POST | /admin/kill-switch/{client_id} | Session-based auth |

### 8. Kickoff Prompt for Code Mode

Build Milestone 1 of the Apple-Supported WhatsAuto system strictly from this blueprint file.

Deliverables:
1. A Python server using pywa (MIT) and WhatsApp Cloud API.
2. Webhook endpoint at /webhook that receives incoming WhatsApp messages.
3. IP-based kill switch middleware: read clients.csv, check is_active for the client's IP address; if false, send Service suspended. Please contact support. and stop processing.
4. Auto-reply: send a configurable free-form reply to inbound messages (within 24-hour CSW).
5. Spreadsheet logging: append each inbound/outbound message to messages.csv (or Google Sheets if credentials provided).
6. clients.csv with sample client data including client_id, phone_number, ip_address, is_active flag.
7. .env.example with required env vars: WHATSAPP_ACCESS_TOKEN, WHATSAPP_PHONE_NUMBER_ID, WHATSAPP_VERIFY_TOKEN.
8. requirements.txt with pywa and dependencies.
9. README.md with setup instructions: create Meta app, configure webhook, get access token, run server.

Testing:
- Send a WhatsApp message to your business number → verify auto-reply received.
- Set is_active=false for a client in clients.csv → send message → verify Service suspended received instead.
- Verify messages.csv has new rows for each message.

Constraints:
- Use ONLY official WhatsApp Cloud API (no Baileys, whatsapp-web.js, or other unofficial clients).
- Add random delay before sending replies (anti-ban).
- Do not write any outbound template logic (Milestone 2).
- Do not write any dashboard UI (Milestone 2).

Return the file list and a one-line confirmation when Milestone 1 is complete and tested.

