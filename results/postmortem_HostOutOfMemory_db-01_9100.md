# Postmortem (auto-generated): HostOutOfMemory

- **Generated:** 2026-10-11 10:11 UTC
- **Alert started:** 2026-10-11T09:58:00Z
- **Severity:** warning
- **Instance:** db-01:9100
- **Runbook:** RB-003 Memory pressure

## Summary
Memory pressure

## Automated findings
- No threshold breached by automated checks.

## Timeline
| Time (UTC) | Event |
|---|---|
| 2026-10-11T09:58:00Z | Alert fired |
| 2026-10-11 10:11 UTC | Bot ran 3 diagnostic steps |
| _fill in_ | Mitigation applied |
| _fill in_ | Resolved |

## Diagnostics
### Memory (rc=0, 0.002s)
`free -m`
```
total        used        free      shared  buff/cache   available
Mem:           16013        9214        2878          61        4312        6798
Swap:              0           0           0
```
### Pressure stall info (rc=0, 0.002s)
`cat /proc/pressure/memory`
```
some avg10=0.77 avg60=0.40 avg300=0.13 total=2060741
full avg10=0.77 avg60=0.40 avg300=0.13 total=1997090
```
### Top processes by RSS (rc=0, 0.009s)
`ps -eo pid,comm,rss --sort=-rss`
```
3800
  75269 bash             3796
   9036 picom            3764
  46957 picom            3704
   6593 picom            3696
  14029 picom            3688
   4250 bash             3656
  17233 bamfdaemon-dbus  3512
    359 bash             3496
   7141 bamfdaemon-dbus  3448
  14648 bamfdaemon-dbus  3448
  47727 bamfdaemon-dbus  3428
   9582 bamfdaemon-dbus  3400
   4266 bash             3392
   5116 bamfdaemon-dbus  3364
   9112 dconf-service    3056
   4675 dconf-service    3016
  16712 dconf-service    2988
   1404 dconf-service    2980
  47019 dconf-service    2928
  14091 dconf-service    2828
   6659 dconf-service    2820
    355 sand-egress-tun  2596
   4437 sand-daemon-sup  2088
   4274 bash             2068
   6566 bash             2064
  12536 bash             2060
   4531 bash             2052
   6598 bash             2048
   4338 bash             2036
    759 bash             2028
   9043 bash             2024
  14036 bash             2024
  44940 bash             2024
   4606 bash             2020
   7713 bash             2020
  13962 bash             2020
  13987 bash             2016
  47315 bash             2012
  14349 bash             2008
  46913 bash             2008
    244 bash             2004
  44992 bash             2004
  14910 bash             2000
   5009 bash             1996
   4438 bash             1992
  75332 sleep            1988
   5401 bash             1976
   6532 bash             1972
   8998 bash             1972
  14859 bash             
```

## Suggested remediation
1. Check for leak: RSS growth over time of the top process
1. Check dmesg for OOM-killer events

## Root cause
_Human to fill in. 5-whys:_

## Action items
| Action | Owner | Due |
|---|---|---|
| _fill in_ | | |
