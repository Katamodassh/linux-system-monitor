import os


def get_disk_usage(path="/"):
    stats = os.statvfs(path)

    total = stats.f_blocks * stats.f_frsize
    available = stats.f_bavail * stats.f_frsize
    used = total - available

    usage_percent = used / total * 100

    return {
        "path": path,
        "total": total,
        "used": used,
        "available": available,
        "usage_percent": usage_percent,
    }

def bytes_to_gib(value):
    return value / (1024 ** 3)