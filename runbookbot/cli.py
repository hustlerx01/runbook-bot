import argparse, json, sys
from pathlib import Path
from .core import load_runbooks, handle_alert, postmortem_md

def main(argv=None):
    ap = argparse.ArgumentParser(description="Alertmanager webhook JSON -> postmortem reports")
    ap.add_argument("payload"); ap.add_argument("--runbooks", default="runbooks"); ap.add_argument("-o", "--out", default="results")
    a = ap.parse_args(argv)
    books = load_runbooks(Path(a.runbooks))
    payload = json.loads(Path(a.payload).read_text())
    Path(a.out).mkdir(exist_ok=True)
    for alert in payload.get("alerts", []):
        inc = handle_alert(alert, books)
        f = Path(a.out) / f"postmortem_{inc.alertname}_{inc.labels.get('instance','x').replace(':','_')}.md"
        f.write_text(postmortem_md(inc, books))
        print(f"{inc.alertname}: runbook={'yes' if inc.runbook else 'no'} steps={len(inc.steps)} findings={sum(1 for s in inc.steps if s.finding)} -> {f}")
    return 0

if __name__ == "__main__":
    sys.exit(main())
