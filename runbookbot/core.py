"""Alert -> runbook -> diagnostics -> Markdown postmortem."""
from __future__ import annotations
import datetime as dt, re, shlex, subprocess, time
from dataclasses import dataclass, field
from pathlib import Path
import yaml

# Only these binaries may run; the runbook YAML cannot widen this.
ALLOWED_BINARIES = {"df", "uptime", "free", "ps", "ss", "cat", "uname", "hostname", "du", "ls", "echo", "nproc", "head"}
SAFE_LABEL = re.compile(r"^[A-Za-z0-9_.:/-]{1,64}$")


@dataclass
class StepResult:
    name: str
    command: str
    rc: int
    stdout: str
    duration_s: float
    finding: str | None = None


@dataclass
class Incident:
    alertname: str
    labels: dict
    annotations: dict
    starts_at: str
    runbook: str | None
    steps: list[StepResult] = field(default_factory=list)


def load_runbooks(directory: Path) -> dict:
    books = {}
    for p in sorted(Path(directory).glob("*.yml")):
        rb = yaml.safe_load(p.read_text())
        books[rb["alertname"]] = rb
    return books


def render_command(template: str, labels: dict) -> list[str]:
    """Substitute {label} placeholders; labels are attacker-influenced so they are validated."""
    def sub(m):
        v = str(labels.get(m.group(1), ""))
        if not SAFE_LABEL.match(v):
            raise ValueError(f"unsafe label value for {m.group(1)!r}: {v!r}")
        return v
    argv = shlex.split(re.sub(r"\{(\w+)\}", sub, template))
    if not argv or argv[0] not in ALLOWED_BINARIES:
        raise PermissionError(f"binary not allow-listed: {argv[:1]}")
    return argv


def evaluate_finding(step: dict, out: str) -> str | None:
    rule = step.get("detect")
    if not rule:
        return None
    m = re.search(rule["regex"], out, re.M)
    if not m:
        return None
    if "threshold" in rule:
        val = float(m.group(1))
        return rule["message"].format(value=val) if val >= rule["threshold"] else None
    return rule["message"].format(value=m.group(0))


def run_steps(rb: dict, labels: dict, timeout: float = 10.0) -> list[StepResult]:
    results = []
    for step in rb.get("diagnostics", []):
        t0 = time.monotonic()
        try:
            argv = render_command(step["run"], labels)
            p = subprocess.run(argv, capture_output=True, text=True, timeout=timeout)
            out, rc = (p.stdout + p.stderr)[-4000:], p.returncode
        except (ValueError, PermissionError) as e:
            out, rc, argv = f"BLOCKED: {e}", 126, [step["run"]]
        except subprocess.TimeoutExpired:
            out, rc = "TIMEOUT", 124
        results.append(StepResult(step["name"], " ".join(argv), rc, out,
                                  round(time.monotonic() - t0, 3), evaluate_finding(step, out)))
    return results


def handle_alert(alert: dict, books: dict) -> Incident:
    labels = alert.get("labels", {})
    name = labels.get("alertname", "unknown")
    rb = books.get(name)
    inc = Incident(name, labels, alert.get("annotations", {}), alert.get("startsAt", ""),
                   rb["title"] if rb else None)
    if rb:
        inc.steps = run_steps(rb, labels)
    return inc


def postmortem_md(inc: Incident, books: dict) -> str:
    rb = books.get(inc.alertname, {})
    now = dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    findings = [s.finding for s in inc.steps if s.finding]
    sev = inc.labels.get("severity", "unknown")
    lines = [f"# Postmortem (auto-generated): {inc.alertname}", "",
             f"- **Generated:** {now}", f"- **Alert started:** {inc.starts_at or 'n/a'}",
             f"- **Severity:** {sev}", f"- **Instance:** {inc.labels.get('instance', 'n/a')}",
             f"- **Runbook:** {inc.runbook or 'NONE: no runbook matched, escalate to on-call'}", "",
             "## Summary", inc.annotations.get("summary", "_fill in_"), "",
             "## Automated findings"]
    lines += [f"- {f}" for f in findings] or ["- No threshold breached by automated checks."]
    lines += ["", "## Timeline", "| Time (UTC) | Event |", "|---|---|",
              f"| {inc.starts_at or 'n/a'} | Alert fired |", f"| {now} | Bot ran {len(inc.steps)} diagnostic steps |",
              "| _fill in_ | Mitigation applied |", "| _fill in_ | Resolved |", "",
              "## Diagnostics"]
    for s in inc.steps:
        lines += [f"### {s.name} (rc={s.rc}, {s.duration_s}s)", f"`{s.command}`", "```", s.stdout.strip()[:1500], "```"]
    lines += ["", "## Suggested remediation"] + [f"1. {r}" for r in rb.get("remediation", ["Escalate"])]
    lines += ["", "## Root cause", "_Human to fill in. 5-whys:_", "",
              "## Action items", "| Action | Owner | Due |", "|---|---|---|", "| _fill in_ | | |", ""]
    return "\n".join(lines)
