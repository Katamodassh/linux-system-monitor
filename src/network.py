import time

def read_network_stats():
    interfaces = {}

    with open("/proc/net/dev", "r") as file:
        lines = file.readlines()[2:]

    for line in lines:
        interface, data = line.split(":", 1)

        interface = interface.strip()

        values = data.split()

        received_bytes = int(values[0])
        transmitted_bytes = int(values[8])

        interfaces[interface] = {
            "received_bytes": received_bytes,
            "transmitted_bytes": transmitted_bytes,
        }

    return interfaces

def get_network_rates(interval=1.0):
    first = read_network_stats()

    time.sleep(interval)

    second = read_network_stats()

    return calculate_network_rates(
        first,
        second,
        interval,
    )

def bytes_to_mib(value):
    return value / (1024 ** 2)

def calculate_network_rates(first, second, interval):
    rates = {}

    if interval <= 0:
        return rates

    for interface, second_stats in second.items():

        if interface not in first:
            continue

        received_delta = (
            second_stats["received_bytes"]
            - first[interface]["received_bytes"]
        )

        transmitted_delta = (
            second_stats["transmitted_bytes"]
            - first[interface]["transmitted_bytes"]
        )

        rates[interface] = {
            "received_per_second":
                received_delta / interval,

            "transmitted_per_second":
                transmitted_delta / interval,
        }

    return rates