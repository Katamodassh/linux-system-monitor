from system_info import get_system_info  
from cpu import get_cpu_usage
from memory import get_memory_stats, kb_to_gib, read_meminfo

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

if __name__ == "__main__":
    main()