import csv
import os
from datetime import datetime


def log_metrics(
    metrics,
    filename="metrics.csv",
):
    file_exists = os.path.exists(filename)

    total_rx = 0.0
    total_tx = 0.0

    for stats in metrics["network"].values():
        total_rx += stats["received_per_second"]
        total_tx += stats["transmitted_per_second"]

    with open(
        filename,
        "a",
        newline="",
        encoding="utf-8",
    ) as file:

        writer = csv.writer(file)

        if not file_exists:
            writer.writerow(
                [
                    "timestamp",
                    "cpu_percent",
                    "memory_percent",
                    "disk_percent",
                    "network_rx_bytes_per_second",
                    "network_tx_bytes_per_second",
                ]
            )

        writer.writerow(
            [
                datetime.now().isoformat(
                    timespec="seconds"
                ),
                round(metrics["cpu"], 2),
                round(
                    metrics["memory"]["usage_percent"],
                    2,
                ),
                round(
                    metrics["disk"]["usage_percent"],
                    2,
                ),
                round(total_rx, 2),
                round(total_tx, 2),
            ]
        )