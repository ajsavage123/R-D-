# Apple-Supported WhatsAuto - Milestone 1

Single-file Python server for WhatsApp auto-reply with IP-based kill switch and spreadsheet logging.

## Quick Start

```bash
pip install -r requirements.txt
cp .env.example .env
# Edit .env with your WhatsApp Cloud API credentials
python app.py
```

## Files

| File | Purpose |
|------|---------|
| `app.py` | Main server with webhook, IP kill switch, auto-reply, CSV logging |
| `.env.example` | Environment variables template |
| `requirements.txt` | Python dependencies |
| `clients.csv` | Client list with IP-based kill switch |

## Endpoints

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/webhook` | GET | WhatsApp webhook verification |
| `/webhook` | POST | Receive incoming WhatsApp messages |
| `/health` | GET | Health check |

## How It Works

1. Customer sends WhatsApp message - server receives via webhook
2. Server checks IP kill switch in clients.csv
3. If is_active=false - sends "Service suspended" and blocks
4. If active - sends auto-reply (with random 2-10s delay for anti-ban)
5. All messages logged to messages.csv

## Requirements

- Python 3.10+
- WhatsApp Business Cloud API account (Meta)
- Verified business phone number
