# Postmortem (auto-generated): ServiceDown

- **Generated:** 2026-10-11 10:11 UTC
- **Alert started:** 2026-10-11T10:00:00Z
- **Severity:** critical
- **Instance:** api-01:8080
- **Runbook:** RB-004 Service port not listening

## Summary
api port 8080 down

## Automated findings
- No threshold breached by automated checks.

## Timeline
| Time (UTC) | Event |
|---|---|
| 2026-10-11T10:00:00Z | Alert fired |
| 2026-10-11 10:11 UTC | Bot ran 2 diagnostic steps |
| _fill in_ | Mitigation applied |
| _fill in_ | Resolved |

## Diagnostics
### Listening sockets (rc=0, 0.002s)
`ss -ltn`
```
State  Recv-Q Send-Q Local Address:Port  Peer Address:Port
LISTEN 0      100          0.0.0.0:6081       0.0.0.0:*   
LISTEN 0      100          0.0.0.0:6080       0.0.0.0:*   
LISTEN 0      128        127.0.0.1:8791       0.0.0.0:*   
LISTEN 0      128          0.0.0.0:26500      0.0.0.0:*   
LISTEN 0      511          0.0.0.0:1340       0.0.0.0:*   
LISTEN 0      511          0.0.0.0:1339       0.0.0.0:*   
LISTEN 0      128          0.0.0.0:50052      0.0.0.0:*   
LISTEN 0      128          0.0.0.0:8790       0.0.0.0:*   
LISTEN 0      5            0.0.0.0:2375       0.0.0.0:*   
LISTEN 0      32         127.0.0.1:5902       0.0.0.0:*   
LISTEN 0      32         127.0.0.1:5900       0.0.0.0:*   
LISTEN 0      32         127.0.0.1:5910       0.0.0.0:*   
LISTEN 0      32         127.0.0.1:5909       0.0.0.0:*   
LISTEN 0      32         127.0.0.1:5906       0.0.0.0:*   
LISTEN 0      32         127.0.0.1:5904       0.0.0.0:*   
LISTEN 0      32             [::1]:5906          [::]:*   
LISTEN 0      32             [::1]:5904          [::]:*   
LISTEN 0      32             [::1]:5910          [::]:*   
LISTEN 0      32             [::1]:5909          [::]:*   
LISTEN 0      32             [::1]:5902          [::]:*   
LISTEN 0      32             [::1]:5900          [::]:*   
LISTEN 0      511                *:14004            *:*   
LISTEN 0      511                *:14006            *:*   
LISTEN 0      511                *:14002            *:*   
LISTEN 0      511        
```
### Kernel (rc=0, 0.001s)
`uname -a`
```
Linux lab-host 6.12.94+ #1 SMP PREEMPT_DYNAMIC Tue Oct  6 06:02:30 UTC 2026 x86_64 GNU/Linux
```

## Suggested remediation
1. systemctl status <svc>; journalctl -u <svc> -n 100

## Root cause
_Human to fill in. 5-whys:_

## Action items
| Action | Owner | Due |
|---|---|---|
| _fill in_ | | |
