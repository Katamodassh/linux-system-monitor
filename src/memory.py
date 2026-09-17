def read_meminfo():
    memory_info = {}

    with open("/proc/meminfo", "r") as file:
        for line in file:
            key, value = line.split(":", 1)

            parts = value.strip().split()

            memory_info[key] = int(parts[0])
    
    return memory_info

def get_memory_stats():
    meminfo = read_meminfo()

    total = meminfo["MemTotal"]
    free = meminfo["MemFree"]
    available = meminfo["MemAvailable"]
    swap_total = meminfo["SwapTotal"]
    swap_free = meminfo["SwapFree"]
    swap_used = swap_total - swap_free

    used = total - available

    usage_percent = used / total * 100

    return {
        "total": total,
        "free": free,
        "available": available,
        "used": used,
        "usage_percent": usage_percent,
        "swap_total": swap_total,
        "swap_free": swap_free,
        "swap_used": swap_used,
    }    

def kb_to_gib(value_kb):
    return value_kb / (1024 ** 2)