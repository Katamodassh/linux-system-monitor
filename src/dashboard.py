import os
import time
from logger import log_metrics
from alerts import check_alerts

from cpu import (
    read_cpu_times,
    get_total_cpu_time,
    calculate_cpu_usage,
)

from memory import (
    get_memory_stats,
    kb_to_gib,
)

from disk import (
    get_disk_usage,
    bytes_to_gib,
)

from network import (
    read_network_stats,
    calculate_network_rates,
    bytes_to_mib,
)

from processes import (
    get_processes,
    get_process_cpu_snapshot,
    calculate_process_cpu_usage,
)


def clear_screen():
    print(
        "\033[2J\033[H",
        end="",
        flush=True,
    )

def display_dashboard(metrics):
    cpu = metrics["cpu"]
    memory = metrics["memory"]
    disk = metrics["disk"]
    network = metrics["network"]
    processes = metrics["processes"]

    # ==========================================
    # HEADER
    # ==========================================

    print("=" * 60)
    print("              LINUX SYSTEM MONITOR")
    print("=" * 60)

    print()

    # ==========================================
    # CPU
    # ==========================================

    print("CPU")

    print(
        f"{progress_bar(cpu)} "
        f"{cpu:6.2f} %"
    )

    print()

    # ==========================================
    # MEMORY
    # ==========================================

    memory_percent = memory["usage_percent"]

    print("MEMORY")

    print(
        f"{progress_bar(memory_percent)} "
        f"{memory_percent:6.2f} %"
    )

    print(
        f"{kb_to_gib(memory['used']):.2f} GiB"
        f" / "
        f"{kb_to_gib(memory['total']):.2f} GiB"
    )

    print()

    # ==========================================
    # DISK
    # ==========================================

    disk_percent = disk["usage_percent"]

    print("DISK")

    print(
        f"{progress_bar(disk_percent)} "
        f"{disk_percent:6.2f} %"
    )

    print(
        f"{bytes_to_gib(disk['used']):.2f} GiB"
        f" / "
        f"{bytes_to_gib(disk['total']):.2f} GiB"
    )

    print()

    # ==========================================
    # NETWORK
    # ==========================================

    print("NETWORK")

    for interface, stats in network.items():
        rx = bytes_to_mib(
            stats["received_per_second"]
        )

        tx = bytes_to_mib(
            stats["transmitted_per_second"]
        )

        print(
            f"{interface:<10}"
            f" ↓ {rx:>7.2f} MiB/s"
            f" ↑ {tx:>7.2f} MiB/s"
        )

    print()


    # ==========================================
    # DISPLAY OF ALERTS
    # ==========================================

    alerts = check_alerts(metrics)

    if alerts:
        print()
        print("ALERTS")

        for alert in alerts:
            print(
                f"⚠ {alert}"
            )

    # ==========================================
    # TOP PROCESSES
    # ==========================================

    print("TOP PROCESSES")

    top_processes = sorted(
        processes,
        key=lambda process: process["cpu_percent"],
        reverse=True,
    )[:8]

    print(
        f"{'PID':<8}"
        f"{'NAME':<25}"
        f"{'CPU %':>10}"
        f"{'RAM':>12}"
    )

    print("-" * 55)

    for process in top_processes:
        memory_mib = (
            process["memory_kb"]
            / 1024
        )

        print(
            f"{process['pid']:<8}"
            f"{process['name']:<25}"
            f"{process['cpu_percent']:>9.2f}%"
            f"{memory_mib:>9.2f} MiB"
        )

def run_dashboard(
    interval=1.0,
    log=False,
):
    try:
        while True:
            metrics = collect_metrics(interval)

            if log:
                log_metrics(metrics)

            clear_screen()

            display_dashboard(metrics)

    except KeyboardInterrupt:
        print()
        print("System monitor stopped.")


def progress_bar(percent, width=20):
    percent = max(0.0, min(percent, 100.0))

    filled = int(
        percent / 100 * width
    )

    empty = width - filled

    return (
        "█" * filled
        + "░" * empty
    )

def collect_metrics(interval):
    # =========================
    # SNAPSHOT T1
    # =========================

    cpu_first = read_cpu_times()
    network_first = read_network_stats()
    processes_first = get_process_cpu_snapshot()

    # Start measuring the real elapsed time
    start_time = time.monotonic()

    # =========================
    # WAIT
    # =========================

    time.sleep(interval)

    # =========================
    # SNAPSHOT T2
    # =========================

    cpu_second = read_cpu_times()
    network_second = read_network_stats()
    processes_second = get_process_cpu_snapshot()

    # End of the real elapsed-time measurement
    end_time = time.monotonic()

    real_interval = end_time - start_time

    # =========================
    # GLOBAL CPU
    # =========================

    cpu_usage = calculate_cpu_usage(
        cpu_first,
        cpu_second,
    )

    # =========================
    # NETWORK
    # =========================

    network_rates = calculate_network_rates(
        network_first,
        network_second,
        real_interval,
    )

    # =========================
    # SYSTEM CPU DELTA
    # =========================

    system_delta = (
        get_total_cpu_time(cpu_second)
        - get_total_cpu_time(cpu_first)
    )

    # Number of logical CPUs
    cpu_count = os.cpu_count() or 1

    # =========================
    # PROCESS CPU
    # =========================

    process_cpu = calculate_process_cpu_usage(
        processes_first,
        processes_second,
        system_delta,
        cpu_count,
    )

    # =========================
    # PROCESS INFORMATION
    # =========================

    processes = get_processes()

    for process in processes:
        process["cpu_percent"] = process_cpu.get(
            process["pid"],
            0.0,
        )

    # =========================
    # MEMORY
    # =========================

    memory = get_memory_stats()

    # =========================
    # DISK
    # =========================

    disk = get_disk_usage("/")

    # =========================
    # FINAL METRICS STRUCTURE
    # =========================

    return {
        "cpu": cpu_usage,
        "memory": memory,
        "disk": disk,
        "network": network_rates,
        "processes": processes,
    }