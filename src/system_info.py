import os
import platform


def get_system_info():
    return {
        "os": platform.system(),
        "kernel": platform.release(),
        "architecture": platform.machine(),
        "hostname": platform.node(),
        "logical_cpus": os.cpu_count(),
    }