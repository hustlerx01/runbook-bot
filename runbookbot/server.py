"""Alertmanager-compatible webhook receiver."""
import os
from pathlib import Path
from fastapi import FastAPI, Request
from .core import load_runbooks, handle_alert, postmortem_md

app = FastAPI(title="runbook-bot")
BOOKS = load_runbooks(Path(os.getenv("RUNBOOK_DIR", "runbooks")))
OUT = Path(os.getenv("OUT_DIR", "results")); OUT.mkdir(exist_ok=True)

@app.get("/healthz")
def healthz():
    return {"ok": True, "runbooks": len(BOOKS)}

@app.post("/webhook")
async def webhook(req: Request):
    payload = await req.json()
    out = []
    for alert in payload.get("alerts", []):
        if alert.get("status", "firing") != "firing":
            continue
        inc = handle_alert(alert, BOOKS)
        f = OUT / f"postmortem_{inc.alertname}.md"
        f.write_text(postmortem_md(inc, BOOKS))
        out.append({"alert": inc.alertname, "file": str(f), "findings": [s.finding for s in inc.steps if s.finding]})
    return {"processed": out}
