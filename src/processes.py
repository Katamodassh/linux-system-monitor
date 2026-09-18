import os



def parse_memory(value):
    parts = value.split()

    if not parts:
        return 0

    return int(parts[0])

def get_pids():
    pids = []

    for entry in os.listdir("/proc"):
        if entry.isdigit():
            pids.append(int(entry))

    return pids

def read_process_status(pid):
    path = f"/proc/{pid}/status"

    data = {}

    with open(path, "r") as file:
        for line in file:
            key, value = line.split(":", 1)
            data[key] = value.strip()

    return data

def get_process_info(pid):
    try:
        status = read_process_status(pid)

        return {
            "pid": pid,
            "name": status.get("Name", "unknown"),
            "state": status.get("State", "unknown"),
            "ppid": int(status.get("PPid", 0)),
            "threads": int(status.get("Threads", 0)),
            "memory_kb":parse_memory( 
                status.get("VmRSS", "0 kB")
            ),
        }

    except (FileNotFoundError, PermissionError):
        return None    

def get_processes():
    processes = []

    for pid in get_pids():
        process = get_process_info(pid)

        if process is not None:
            processes.append(process)

    return processes 