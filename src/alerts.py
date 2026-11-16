def check_alerts(
    metrics,
    cpu_threshold=90.0,
    memory_threshold=85.0,
    disk_threshold=90.0,
):
    alerts = []

    cpu = metrics["cpu"]
    memory = metrics["memory"]["usage_percent"]
    disk = metrics["disk"]["usage_percent"]

    if cpu >= cpu_threshold:
        alerts.append(
            f"HIGH CPU: {cpu:.2f}%"
        )

    if memory >= memory_threshold:
        alerts.append(
            f"HIGH MEMORY: {memory:.2f}%"
        )

    if disk >= disk_threshold:
        alerts.append(
            f"DISK ALMOST FULL: {disk:.2f}%"
        )

    return alerts