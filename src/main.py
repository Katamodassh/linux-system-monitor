from system_info import get_system_info  
from cpu import get_cpu_usage

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

if __name__ == "__main__":
    main()