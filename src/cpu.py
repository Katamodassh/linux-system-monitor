import time

def read_cpu_times():
    with open("/proc/stat", "r") as file:
        first_line = file.readline()
    values = first_line.split()
    times = [int(value) for value in values[1:]]
    return {
        "user": times[0],
        "nice": times[1],
        "system": times[2],
        "idle": times[3],
        "iowait": times[4],
        "irq": times[5],
        "softirq": times[6],
        "steal": times[7],
    } 

def get_total_cpu_time(cpu_times):
    return sum(cpu_times.values())

def get_idle_cpu_time(cpu_times):
    return cpu_times["idle"] + cpu_times["iowait"]

def get_cpu_usage(interval=1.0):
    first = read_cpu_times()

    time.sleep(interval)

    second = read_cpu_times()

    first_total = get_total_cpu_time(first)
    second_total = get_total_cpu_time(second)

    first_idle = get_idle_cpu_time(first)
    second_idle = get_idle_cpu_time(second)

    total_delta = second_total - first_total
    idle_delta = second_idle - first_idle

    active_delta = total_delta - idle_delta

    usage = active_delta / total_delta * 100

    return usage