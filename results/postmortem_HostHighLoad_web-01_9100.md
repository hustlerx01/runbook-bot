# Postmortem (auto-generated): HostHighLoad

- **Generated:** 2026-10-11 10:11 UTC
- **Alert started:** 2026-10-11T09:57:00Z
- **Severity:** warning
- **Instance:** web-01:9100
- **Runbook:** RB-002 High CPU load

## Summary
Load average high

## Automated findings
- No threshold breached by automated checks.

## Timeline
| Time (UTC) | Event |
|---|---|
| 2026-10-11T09:57:00Z | Alert fired |
| 2026-10-11 10:11 UTC | Bot ran 3 diagnostic steps |
| _fill in_ | Mitigation applied |
| _fill in_ | Resolved |

## Diagnostics
### Load average (rc=0, 0.002s)
`cat /proc/loadavg`
```
2.22 2.07 2.45 2/1102 75382
```
### CPU count (rc=0, 0.002s)
`nproc`
```
8
```
### Top processes by CPU (rc=0, 0.012s)
`ps -eo pid,comm,%cpu,%mem --sort=-%cpu`
```
0.0  0.0
    199 bash             0.0  0.0
    200 flock            0.0  0.0
    244 bash             0.0  0.0
    245 flock            0.0  0.0
    274 bash             0.0  0.0
    275 flock            0.0  0.0
    359 bash             0.0  0.0
    759 bash             0.0  0.0
    761 flock            0.0  0.0
    802 dbus-daemon      0.0  0.0
   1404 dconf-service    0.0  0.0
   4274 bash             0.0  0.0
   4275 flock            0.0  0.0
   4338 bash             0.0  0.0
   4339 flock            0.0  0.0
   4346 bash             0.0  0.0
   4437 sand-daemon-sup  0.0  0.0
   4438 bash             0.0  0.0
   4439 flock            0.0  0.0
   4454 bash             0.0  0.0
   4455 flock            0.0  0.0
   4500 bash             0.0  0.0
   4501 flock            0.0  0.0
   4531 bash             0.0  0.0
   4532 flock            0.0  0.0
   4606 bash             0.0  0.0
   4607 flock            0.0  0.0
   4675 dconf-service    0.0  0.0
   5009 bash             0.0  0.0
   5011 flock            0.0  0.0
   5116 bamfdaemon-dbus  0.0  0.0
   5401 bash             0.0  0.0
   5403 flock            0.0  0.0
   5443 dbus-daemon      0.0  0.0
   5453 bash             0.0  0.0
   5454 flock            0.0  0.0
   6433 bash             0.0  0.0
   6532 bash             0.0  0.0
   6533 flock            0.0  0.0
   6566 bash             0.0  0.0
   6568 flock            0.0  0.0
   6598 bash             0.0  0.0
   6610 flock            0.0  0.0
   6659 dconf-service    0.0 
```

## Suggested remediation
1. Compare load to nproc; load/nproc > 1 means saturation
1. Identify runaway PID above; restart owning service, don't kill -9 blindly

## Root cause
_Human to fill in. 5-whys:_

## Action items
| Action | Owner | Due |
|---|---|---|
| _fill in_ | | |
