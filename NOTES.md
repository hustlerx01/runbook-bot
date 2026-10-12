# Interview talking points: runbook-bot
1. **Toil reduction.** The first 5 minutes of most incidents are the same commands every time. Automating evidence collection cuts MTTR and gives a postmortem with real output, not memory.
2. **Security of automation.** Alert labels come from scraped targets, so they're attacker-influenced. Commands are `shlex`-split with no shell, binaries are allow-listed in code (the YAML can't widen the list), and label values must match `^[A-Za-z0-9_.:/-]+$`. Tests prove `$(id)` and `; rm -rf /` are blocked.
3. **Blameless postmortems.** The template follows the Google SRE structure: summary, timeline, evidence, root cause (left to a human), and action items with owners.
4. **Honest results.** 0 findings because the lab host was healthy. I don't fake a breach in the results; the threshold logic is covered by unit tests.
5. **Next steps.** Run the steps remotely via SSM or Ansible, post a link to Slack, open a Jira ticket, add a dedup window for flapping alerts.
6. **PSI over free -m.** `/proc/pressure/memory` shows real stall time, which is a better saturation signal than "free" memory (the page cache confuses people).
