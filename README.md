# Linux System Monitor

A Linux system monitoring tool written in Python.

I built this project mainly to understand how Linux exposes information about CPU usage, memory, processes, disks and network activity. Instead of using a high-level library such as `psutil`, most of the metrics are collected directly from Linux interfaces such as `/proc`.

The project started as a simple CLI and was progressively extended with process monitoring, a live dashboard, CSV logging, alerts and automated tests.

## Features

- System information
- Global CPU usage
- Memory and swap usage
- Filesystem usage
- Process monitoring
- CPU and memory usage per process
- Network RX/TX rates
- Command-line interface
- Live monitoring dashboard
- CSV logging
- Resource usage alerts
- Automated tests with `pytest`

## How it works

Linux exposes a lot of system information through the `/proc` pseudo-filesystem.

For example:

```text
/proc/stat          -> CPU counters
/proc/meminfo       -> memory information
/proc/<PID>/status  -> process information
/proc/<PID>/stat    -> process CPU counters
/proc/net/dev       -> network counters
```

Some values, such as memory usage, can be read directly.

CPU and network usage are different because Linux mainly exposes cumulative counters. To calculate a rate, the monitor takes two snapshots separated by a sampling interval.

```text
snapshot 1
    |
    | wait
    |
snapshot 2
    |
    v
calculate the difference
```

For the live dashboard, CPU, network and process snapshots are collected during the same sampling interval so that the measurements stay consistent.

## Project structure

```text
linux-system-monitor/
├── src/
│   ├── main.py
│   ├── system_info.py
│   ├── cpu.py
│   ├── memory.py
│   ├── disk.py
│   ├── processes.py
│   ├── network.py
│   ├── dashboard.py
│   ├── logger.py
│   └── alerts.py
│
├── tests/
│   ├── test_cpu.py
│   ├── test_network.py
│   ├── test_dashboard.py
│   └── test_alerts.py
│
├── pytest.ini
├── .gitignore
└── README.md
```

## Usage

Display all metrics:

```bash
python3 src/main.py
```

Individual metrics can also be displayed:

```bash
python3 src/main.py --cpu
python3 src/main.py --memory
python3 src/main.py --disk
python3 src/main.py --processes
python3 src/main.py --network
```

The sampling interval can be changed with:

```bash
python3 src/main.py --cpu --interval 2
```

## Live dashboard

```bash
python3 src/main.py --watch
```

Example:

```text
============================================================
              LINUX SYSTEM MONITOR
============================================================

CPU
█░░░░░░░░░░░░░░░░░░░   6.30 %

MEMORY
███░░░░░░░░░░░░░░░░░  15.64 %
1.16 GiB / 7.43 GiB

DISK
█░░░░░░░░░░░░░░░░░░░   5.82 %

NETWORK
lo         ↓ 0.00 MiB/s ↑ 0.00 MiB/s
eth0       ↓ 0.00 MiB/s ↑ 0.00 MiB/s

TOP PROCESSES
PID     NAME                    CPU %        RAM
-------------------------------------------------
5343    yes                    100.81%      1.50 MiB
```

The dashboard can be stopped with `Ctrl+C`.

## Logging

Metrics can also be saved to a CSV file:

```bash
python3 src/main.py --watch --log
```

This creates `metrics.csv`, which can later be analyzed with Python, Pandas or another data analysis tool.

## Alerts

The monitor can display alerts when resource usage exceeds predefined thresholds.

Current default thresholds are:

```text
CPU     90 %
Memory  85 %
Disk    90 %
```

## Testing

Run the test suite with:

```bash
python3 -m pytest -v
```

The tests currently cover CPU calculations, network rates, dashboard utilities and alerts.

For CPU monitoring I also used the Linux command:

```bash
yes > /dev/null &
```

to create a CPU-intensive process and check that it appeared at around 100% CPU in the process monitor.

It can be stopped with:

```bash
pkill yes
```

## What I learned

This project helped me understand several concepts that were previously quite abstract to me, especially:

- how `/proc` works
- cumulative CPU counters
- how CPU percentages are actually calculated
- processes, PIDs and threads
- memory information exposed by Linux
- filesystem statistics
- network counters and transfer rates
- exception handling when processes disappear while being inspected
- CLI development with `argparse`
- Git branches and feature development
- automated testing with `pytest`

One of the most useful parts of the project was understanding that monitoring values such as CPU usage or network throughput are often not directly available as percentages or rates. They have to be calculated from measurements taken at different points in time.

## Environment

The project was developed with:

- Python 3
- Ubuntu on WSL2
- Git / GitHub

## Status

Version `v1.0.0` is the first complete version of the project.

There are still improvements I may add later, especially a cleaner terminal refresh system, configurable alert thresholds and possibly integration with monitoring tools such as Prometheus or Grafana.