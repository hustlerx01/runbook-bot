# Postmortem (auto-generated): HostDiskFull

- **Generated:** 2026-10-11 10:11 UTC
- **Alert started:** 2026-10-11T09:55:00Z
- **Severity:** critical
- **Instance:** web-01:9100
- **Runbook:** RB-001 Disk usage high

## Summary
Disk usage on / above 85%

## Automated findings
- No threshold breached by automated checks.

## Timeline
| Time (UTC) | Event |
|---|---|
| 2026-10-11T09:55:00Z | Alert fired |
| 2026-10-11 10:11 UTC | Bot ran 3 diagnostic steps |
| _fill in_ | Mitigation applied |
| _fill in_ | Resolved |

## Diagnostics
### Filesystem usage (rc=0, 0.002s)
`df -h /`
```
Filesystem      Size  Used Avail Use% Mounted on
overlay         126G   22G   98G  19% /
```
### Inodes (rc=0, 0.001s)
`df -i /`
```
Filesystem      Inodes  IUsed   IFree IUse% Mounted on
overlay        8388608 169610 8218998    3% /
```
### Largest dirs under /var/log (rc=0, 0.004s)
`du -sh /var/log`
```
796K	/var/log
```

## Suggested remediation
1. Rotate/compress logs: logrotate -f /etc/logrotate.conf
1. Clear package cache: apt-get clean
1. If a single file grows, find the writer with lsof +L1 (deleted-but-open files)

## Root cause
_Human to fill in. 5-whys:_

## Action items
| Action | Owner | Due |
|---|---|---|
| _fill in_ | | |
