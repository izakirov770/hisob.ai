# Hisob AI — Bazaviy Skeleton (Aiogram v3, SQLite)

## Tez start
```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
# .env ichida BOT_TOKEN ni to'ldiring
python bot.py
```

### Funksiyalar
- 3 til: uz / ru / en
- Kirim/chiqim: matn (`+12000 kofe`), ovoz (stub), chek OCR (stub)
- Avto-kategoriya: oddiy qoidalar
- Kunlik 20:00 eslatma
- Qarzlar va muddat eslatmasi
- Hisobot: kun/hafta/oy

### Keyingi qadamlar
- Webhook + Railway
- Click/Payme obuna
- Mini App

### Testlar
```bash
pytest -q
```
