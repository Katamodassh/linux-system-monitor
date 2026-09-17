import os
import platform


def main():
    print("=== SYSTEM INFORMATION ===")

    print(f"OS: {platform.system()}")
    print(f"Kernel: {platform.release()}")
    print(f"Architecture: {platform.machine()}")
    print(f"Hostname: {platform.node()}")
    print(f"Logical CPUs: {os.cpu_count()}")


if __name__ == "__main__":
    main()