from system_info import get_system_info  
from cpu import get_cpu_usage
from memory import get_memory_stats, kb_to_gib, read_meminfo
from disk import get_disk_usage, bytes_to_gib

def main():
    info = get_system_info()

    print("=== SYSTEM INFORMATION ===")
    print(f"Operating system : {info['os']}")
    print(f"Kernel           : {info['kernel']}")
    print(f"Architecture     : {info['architecture']}")
    print(f"Hostname         : {info['hostname']}")
    print(f"Logical CPUs     : {info['logical_cpus']}")

    print()
    print("=== CPU ===")

    cpu_usage = get_cpu_usage()

    print(f"Usage            : {cpu_usage:.2f} %")

    memory = get_memory_stats()

    print()
    print("=== MEMORY ===")

    print(
        f"Total       : "
        f"{kb_to_gib(memory['total']):.2f} GiB"
    )

    print(
        f"Used        : "
        f"{kb_to_gib(memory['used']):.2f} GiB"
    )

    print(
        f"Available   : "
        f"{kb_to_gib(memory['available']):.2f} GiB"
    )

    print(
        f"Usage       : "
        f"{memory['usage_percent']:.2f} %"
    )

    print()
    print("=== SWAP ===")

    print(
        f"Total       : "
        f"{kb_to_gib(memory['swap_total']):.2f} GiB"
    )

    print(
        f"Used        : "
        f"{kb_to_gib(memory['swap_used']):.2f} GiB"
    )

    disk = get_disk_usage("/")

    print()
    print("=== DISK ===")

    print(f"Mount point : {disk['path']}")
    print(f"Total       : {bytes_to_gib(disk['total']):.2f} GiB")
    print(f"Used        : {bytes_to_gib(disk['used']):.2f} GiB")
    print(f"Available   : {bytes_to_gib(disk['available']):.2f} GiB")
    print(f"Usage       : {disk['usage_percent']:.2f} %")

    windows_disk = get_disk_usage("/mnt/c")

    print()
    print("=== WINDOWS C: via WSL ===")

    print(f"Mount point : {windows_disk['path']}")
    print(f"Total       : {bytes_to_gib(windows_disk['total']):.2f} GiB")
    print(f"Used        : {bytes_to_gib(windows_disk['used']):.2f} GiB")
    print(f"Available   : {bytes_to_gib(windows_disk['available']):.2f} GiB")
    print(f"Usage       : {windows_disk['usage_percent']:.2f} %")

if __name__ == "__main__":
    main()