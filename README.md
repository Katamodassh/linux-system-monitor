# Linux System Monitor

A lightweight Linux system monitoring tool written in Python.

The project collects system metrics directly from Linux interfaces such as `/proc` and displays them through a command-line interface and a live terminal dashboard.

It was developed to better understand how Linux exposes CPU, memory, process, filesystem, and network information without relying on high-level monitoring libraries such as `psutil`.

---

## Features

The monitor currently supports:

- General system information
- Global CPU usage
- Memory and swap monitoring
- Filesystem usage
- Process discovery
- CPU usage per process
- Memory usage per process
- Network receive/transmit rates
- Command-line interface
- Live monitoring dashboard
- Synchronized metric collection
- CSV metric logging
- CPU, memory, and disk alerts
- Automated tests with `pytest`

---

## Architecture

The application is organized into several specialized Python modules.

```text
User
 │
 ▼
main.py
 │
 ├── system_info.py
 ├── cpu.py
 ├── memory.py
 ├── disk.py
 ├── processes.py
 ├── network.py
 │
 └── dashboard.py
       │
       ├── logger.py
       └── alerts.py
```

The monitoring modules retrieve information from Linux system interfaces.

```text
Linux Kernel
    │
    ├── /proc/stat
    │      └── CPU counters
    │
    ├── /proc/meminfo
    │      └── Memory and swap
    │
    ├── /proc/<PID>/status
    │      └── Process information
    │
    ├── /proc/<PID>/stat
    │      └── Process CPU counters
    │
    ├── /proc/net/dev
    │      └── Network counters
    │
    └── statvfs()
           └── Filesystem information
```

The kernel maintains the system state and cumulative counters. The Python modules read and parse these interfaces, calculate useful metrics, and send the results to the CLI or dashboard.

---

## Metric Collection

Some metrics can be read directly.

For example:

```text
Memory
Disk
System information
```

Other metrics are based on cumulative counters and require two snapshots.

```text
snapshot t1
    │
    ▼
wait for sampling interval
    │
    ▼
snapshot t2
    │
    ▼
calculate delta
```

This approach is used for:

- Global CPU usage
- CPU usage per process
- Network throughput

For example, network throughput is calculated using:

```text
rate = (counter_t2 - counter_t1) / elapsed_time
```

The live dashboard uses synchronized snapshots so CPU, network, and process measurements are collected over approximately the same time interval.

---

## Project Structure

```text
linux-system-monitor/
│
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

---

## Requirements

The project is designed for Linux environments.

It has also been developed and tested under Ubuntu running through WSL2.

Recommended:

```text
Python 3.10+
Linux / WSL2
pytest
```

---

## Installation

Clone the repository:

```bash
git clone <repository-url>
cd linux-system-monitor
```

Check Python:

```bash
python3 --version
```

Install `pytest` if necessary:

```bash
sudo apt install python3-pytest
```

---

## Usage

### Display all metrics

```bash
python3 src/main.py
```

or:

```bash
python3 src/main.py --all
```

### System information

```bash
python3 src/main.py --system
```

### CPU

```bash
python3 src/main.py --cpu
```

### Memory

```bash
python3 src/main.py --memory
```

### Disk

```bash
python3 src/main.py --disk
```

### Processes

```bash
python3 src/main.py --processes
```

### Network

```bash
python3 src/main.py --network
```

---

## Sampling Interval

The sampling interval can be changed using:

```bash
python3 src/main.py --cpu --interval 2
```

For example:

```text
--interval 2
```

means that two seconds are used between metric snapshots.

The interval must be greater than zero.

---

## Live Dashboard

Launch continuous monitoring with:

```bash
python3 src/main.py --watch
```

The dashboard displays:

```text
CPU
Memory
Disk
Network
Alerts
Top processes
```

Example:

```text
============================================================
              LINUX SYSTEM MONITOR
============================================================

CPU
██░░░░░░░░░░░░░░░░░░  8.42 %

MEMORY
███░░░░░░░░░░░░░░░░░ 15.61 %
1.16 GiB / 7.43 GiB

DISK
█░░░░░░░░░░░░░░░░░░░  5.82 %

NETWORK
eth0       ↓ 0.02 MiB/s ↑ 0.01 MiB/s

TOP PROCESSES
PID     NAME                  CPU %        RAM
------------------------------------------------
5343    yes                  100.21%      1.50 MiB
```

Stop the dashboard with:

```text
Ctrl+C
```

---

## CSV Logging

Metrics can be saved while the dashboard is running:

```bash
python3 src/main.py --watch --log
```

This creates:

```text
metrics.csv
```

with data similar to:

```csv
timestamp,cpu_percent,memory_percent,disk_percent,network_rx_bytes_per_second,network_tx_bytes_per_second
2026-11-16T15:00:01,7.42,15.63,5.82,1024.0,520.0
2026-11-16T15:00:02,6.91,15.64,5.82,2420.0,830.0
```

This allows system activity to be analyzed later with tools such as Python or Pandas.

---

## Alerts

The dashboard can detect high resource utilization.

Default thresholds include:

```text
CPU    : 90 %
Memory : 85 %
Disk   : 90 %
```

Possible output:

```text
ALERTS
⚠ HIGH CPU: 94.22%
⚠ HIGH MEMORY: 88.13%
```

The CPU alert currently monitors global system CPU usage rather than the CPU usage of an individual process.

---

## Process CPU Monitoring

Linux exposes cumulative CPU counters for each process through:

```text
/proc/<PID>/stat
```

The monitor takes two snapshots and calculates the CPU consumed between them.

The displayed percentage follows a convention similar to tools such as `top`, where approximately:

```text
one fully utilized logical CPU ≈ 100 %
```

Therefore a multithreaded process may legitimately exceed 100%.

---

## Testing

Run the complete automated test suite with:

```bash
python3 -m pytest -v
```

The tests cover important components including:

- CPU percentage calculations
- Network rate calculations
- Dashboard progress bars
- Alert generation
- Edge cases

The tests use deterministic artificial snapshots rather than depending on the current activity of the computer.

This makes them faster and reproducible.

---

## Example CPU Validation

A CPU-intensive process can be generated with:

```bash
yes > /dev/null &
```

The process should appear near the top of the process list with approximately:

```text
100 % CPU
```

Stop it with:

```bash
pkill yes
```

This can be used to validate CPU monitoring behavior.

---

## Design Decisions

### Direct use of `/proc`

The project intentionally reads Linux interfaces directly instead of hiding the implementation behind a high-level monitoring library.

This makes it possible to understand:

- Linux pseudo-filesystems
- Kernel counters
- CPU accounting
- Process management
- Memory information
- Network statistics
- Filesystem statistics

### Modular architecture

Different monitoring responsibilities are separated into modules.

This makes the project easier to:

- understand
- test
- maintain
- extend

### Synchronized snapshots

CPU, process CPU, and network statistics are collected around a common sampling interval to avoid unnecessary sequential delays.

---

## Current Limitations

The current version is intentionally lightweight.

Some possible future improvements include:

- Improved terminal screen refresh behavior
- Configurable alert thresholds from the CLI
- Per-process CPU alerts
- JSON logging
- Historical charts
- Process filtering
- Signal handling improvements
- Packaging as an installable Python application
- Integration with Prometheus or Grafana

---

## What I Learned

This project was developed as a systems programming exercise and helped reinforce concepts including:

- Linux filesystem hierarchy
- `/proc` pseudo-filesystem
- CPU accounting
- Processes and PIDs
- Parent processes
- Threads
- Memory and swap
- Filesystems and mount points
- Network interfaces
- Cumulative counters
- Sampling and rates
- Python modules
- Exception handling
- CLI design with `argparse`
- Logging
- Automated testing
- Git workflow

---

## Project Status

Version 1 is functionally complete.

The project currently provides Linux system monitoring through both a CLI and a live terminal dashboard, with metric logging, alerts, and automated tests.