import argparse
import os
import time

from system_info import get_system_info

from cpu import (
    get_cpu_usage,
    read_cpu_times,
    get_total_cpu_time,
)

from memory import (
    get_memory_stats,
    kb_to_gib,
)

from disk import (
    get_disk_usage,
    bytes_to_gib,
)

from processes import (
    get_pids,
    get_processes,
    get_process_cpu_time,
)

from network import (
    get_network_rates,
    bytes_to_mib,
)


# ============================================================
# CLI ARGUMENTS
# ============================================================

def positive_float(value):
    value = float(value)

    if value <= 0:
        raise argparse.ArgumentTypeError(
            "Interval must be greater than 0."
        )

    return value


def parse_arguments():
    parser = argparse.ArgumentParser(
        description="Linux System Monitor"
    )

    parser.add_argument(
        "--system",
        action="store_true",
        help="Display system information",
    )

    parser.add_argument(
        "--cpu",
        action="store_true",
        help="Display CPU usage",
    )

    parser.add_argument(
        "--memory",
        action="store_true",
        help="Display memory and swap usage",
    )

    parser.add_argument(
        "--disk",
        action="store_true",
        help="Display filesystem usage",
    )

    parser.add_argument(
        "--processes",
        action="store_true",
        help="Display top processes",
    )

    parser.add_argument(
        "--network",
        action="store_true",
        help="Display network traffic",
    )

    parser.add_argument(
        "--all",
        action="store_true",
        help="Display all metrics",
    )

    parser.add_argument(
        "--interval",
        type=positive_float,
        default=1.0,
        help="Measurement interval in seconds",
    )

    return parser.parse_args()


# ============================================================
# SYSTEM INFORMATION
# ============================================================

def display_system_info():
    info = get_system_info()

    print("=== SYSTEM INFORMATION ===")

    print(
        f"Operating system : "
        f"{info['os']}"
    )

    print(
        f"Kernel           : "
        f"{info['kernel']}"
    )

    print(
        f"Architecture     : "
        f"{info['architecture']}"
    )

    print(
        f"Hostname         : "
        f"{info['hostname']}"
    )

    print(
        f"Logical CPUs     : "
        f"{info['logical_cpus']}"
    )


# ============================================================
# GLOBAL CPU
# ============================================================

def display_cpu(interval):
    usage = get_cpu_usage(interval)

    print("=== CPU ===")
    print(f"Usage            : {usage:.2f} %")


# ============================================================
# MEMORY + SWAP
# ============================================================

def display_memory():
    memory = get_memory_stats()

    print("=== MEMORY ===")

    print(
        f"Total            : "
        f"{kb_to_gib(memory['total']):.2f} GiB"
    )

    print(
        f"Used             : "
        f"{kb_to_gib(memory['used']):.2f} GiB"
    )

    print(
        f"Available        : "
        f"{kb_to_gib(memory['available']):.2f} GiB"
    )

    print(
        f"Usage            : "
        f"{memory['usage_percent']:.2f} %"
    )

    print()

    print("=== SWAP ===")

    print(
        f"Total            : "
        f"{kb_to_gib(memory['swap_total']):.2f} GiB"
    )

    print(
        f"Used             : "
        f"{kb_to_gib(memory['swap_used']):.2f} GiB"
    )

    print(
        f"Free             : "
        f"{kb_to_gib(memory['swap_free']):.2f} GiB"
    )


# ============================================================
# DISK / FILESYSTEM
# ============================================================

def display_disk():
    disk = get_disk_usage("/")

    print("=== DISK / FILESYSTEM ===")

    print(
        f"Mount point      : "
        f"{disk['path']}"
    )

    print(
        f"Total            : "
        f"{bytes_to_gib(disk['total']):.2f} GiB"
    )

    print(
        f"Used             : "
        f"{bytes_to_gib(disk['used']):.2f} GiB"
    )

    print(
        f"Available        : "
        f"{bytes_to_gib(disk['available']):.2f} GiB"
    )

    print(
        f"Usage            : "
        f"{disk['usage_percent']:.2f} %"
    )


# ============================================================
# PROCESS CPU
# ============================================================

def get_process_cpu_snapshot():
    """
    Return:
        {
            pid: cumulative_cpu_time,
            ...
        }
    """

    snapshot = {}

    for pid in get_pids():

        try:
            snapshot[pid] = get_process_cpu_time(pid)

        except (
            FileNotFoundError,
            PermissionError,
            ProcessLookupError,
            ValueError,
        ):
            # The process may disappear while we read /proc.
            continue

    return snapshot


def calculate_process_cpu_usage(interval):
    """
    Measure CPU usage of all processes during an interval.

    Return:
        {
            pid: cpu_percentage,
            ...
        }
    """

    # -----------------------------
    # Snapshot t1
    # -----------------------------

    system_first = get_total_cpu_time(
        read_cpu_times()
    )

    processes_first = get_process_cpu_snapshot()

    # -----------------------------
    # Wait
    # -----------------------------

    time.sleep(interval)

    # -----------------------------
    # Snapshot t2
    # -----------------------------

    system_second = get_total_cpu_time(
        read_cpu_times()
    )

    processes_second = get_process_cpu_snapshot()

    # -----------------------------
    # Global CPU delta
    # -----------------------------

    system_delta = (
        system_second
        - system_first
    )

    if system_delta <= 0:
        return {}

    cpu_count = os.cpu_count() or 1

    usage_by_pid = {}

    # -----------------------------
    # Process deltas
    # -----------------------------

    for pid, second_time in processes_second.items():

        first_time = processes_first.get(pid)

        # Process appeared after first snapshot
        if first_time is None:
            continue

        process_delta = (
            second_time
            - first_time
        )

        # Defensive check
        if process_delta < 0:
            continue

        cpu_percent = (
            process_delta
            / system_delta
            * 100
            * cpu_count
        )

        usage_by_pid[pid] = cpu_percent

    return usage_by_pid


# ============================================================
# PROCESSES
# ============================================================

def display_processes(interval):
    # First measure process CPU usage.
    cpu_usage_by_pid = calculate_process_cpu_usage(
        interval
    )

    # Then retrieve process information:
    # name, state, memory, threads, ...
    processes = get_processes()

    for process in processes:

        process["cpu_percent"] = (
            cpu_usage_by_pid.get(
                process["pid"],
                0.0,
            )
        )

    # Sort by CPU usage
    top_processes = sorted(
        processes,
        key=lambda process: process["cpu_percent"],
        reverse=True,
    )[:10]

    print("=== TOP PROCESSES BY CPU ===")

    print(
        f"{'PID':<8}"
        f"{'NAME':<25}"
        f"{'CPU %':>10}"
        f"{'MEMORY':>14}"
        f"{'THREADS':>10}"
    )

    print("-" * 67)

    for process in top_processes:

        memory_mib = (
            process["memory_kb"]
            / 1024
        )

        print(
            f"{process['pid']:<8}"
            f"{process['name']:<25}"
            f"{process['cpu_percent']:>9.2f}%"
            f"{memory_mib:>11.2f} MiB"
            f"{process['threads']:>10}"
        )


# ============================================================
# NETWORK
# ============================================================

def display_network(interval):
    network_rates = get_network_rates(
        interval
    )

    print("=== NETWORK ===")

    print(
        f"{'INTERFACE':<12}"
        f"{'RX':>15}"
        f"{'TX':>15}"
    )

    print("-" * 42)

    for interface, stats in network_rates.items():

        rx = bytes_to_mib(
            stats["received_per_second"]
        )

        tx = bytes_to_mib(
            stats["transmitted_per_second"]
        )

        print(
            f"{interface:<12}"
            f"{rx:>10.2f} MiB/s"
            f"{tx:>10.2f} MiB/s"
        )


# ============================================================
# MAIN
# ============================================================

def main():
    args = parse_arguments()

    # If no monitoring option is selected,
    # behave like --all.
    no_option_selected = not any(
        [
            args.system,
            args.cpu,
            args.memory,
            args.disk,
            args.processes,
            args.network,
            args.all,
        ]
    )

    if no_option_selected:
        args.all = True

    # ----------------------------
    # System
    # ----------------------------

    if args.system or args.all:
        display_system_info()
        print()

    # ----------------------------
    # CPU
    # ----------------------------

    if args.cpu or args.all:
        display_cpu(
            args.interval
        )
        print()

    # ----------------------------
    # Memory
    # ----------------------------

    if args.memory or args.all:
        display_memory()
        print()

    # ----------------------------
    # Disk
    # ----------------------------

    if args.disk or args.all:
        display_disk()
        print()

    # ----------------------------
    # Processes
    # ----------------------------

    if args.processes or args.all:
        display_processes(
            args.interval
        )
        print()

    # ----------------------------
    # Network
    # ----------------------------

    if args.network or args.all:
        display_network(
            args.interval
        )


# ============================================================
# ENTRY POINT
# ============================================================

if __name__ == "__main__":
    main()