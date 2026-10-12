import json
from pathlib import Path
import pytest
from runbookbot.core import load_runbooks, render_command, handle_alert, postmortem_md, evaluate_finding

ROOT = Path(__file__).resolve().parents[1]
BOOKS = load_runbooks(ROOT / "runbooks")

def test_runbooks_load():
    assert set(BOOKS) == {"HostDiskFull", "HostHighLoad", "HostOutOfMemory", "ServiceDown"}

def test_label_injection_blocked():
    with pytest.raises(ValueError):
        render_command("df -h {mountpoint}", {"mountpoint": "/; rm -rf /"})

def test_non_allowlisted_binary_blocked():
    with pytest.raises(PermissionError):
        render_command("curl http://evil", {})

def test_threshold_detection():
    step = {"detect": {"regex": r"(\d+)%", "threshold": 85, "message": "at {value:.0f}%"}}
    assert evaluate_finding(step, "/dev/sda1 50G 45G 5G 91% /") == "at 91%"
    assert evaluate_finding(step, "/dev/sda1 50G 10G 40G 20% /") is None

def test_injected_alert_gets_blocked_step_not_executed():
    alert = {"labels": {"alertname": "HostDiskFull", "mountpoint": "$(id)"}}
    inc = handle_alert(alert, BOOKS)
    assert inc.steps[0].rc == 126 and "BLOCKED" in inc.steps[0].stdout

def test_unknown_alert_escalates():
    inc = handle_alert({"labels": {"alertname": "CertExpiry"}}, BOOKS)
    md = postmortem_md(inc, BOOKS)
    assert "no runbook matched" in md and inc.steps == []

def test_full_payload_produces_markdown(tmp_path):
    from runbookbot.cli import main
    assert main([str(ROOT / "samples/alertmanager_payload.json"), "--runbooks", str(ROOT / "runbooks"), "-o", str(tmp_path)]) == 0
    files = list(tmp_path.glob("*.md"))
    assert len(files) == 5
    assert all("## Timeline" in f.read_text() for f in files)

def test_webhook(monkeypatch, tmp_path):
    monkeypatch.setenv("RUNBOOK_DIR", str(ROOT / "runbooks")); monkeypatch.setenv("OUT_DIR", str(tmp_path))
    import importlib, runbookbot.server as s; importlib.reload(s)
    from fastapi.testclient import TestClient
    c = TestClient(s.app)
    assert c.get("/healthz").json()["runbooks"] == 4
    r = c.post("/webhook", json=json.loads((ROOT / "samples/alertmanager_payload.json").read_text()))
    assert len(r.json()["processed"]) == 5
