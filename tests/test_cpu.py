from cpu import calculate_cpu_usage


def test_calculate_cpu_usage():
    first = {
        "user": 100,
        "nice": 0,
        "system": 50,
        "idle": 850,
        "iowait": 0,
        "irq": 0,
        "softirq": 0,
        "steal": 0,
    }

    second = {
        "user": 150,
        "nice": 0,
        "system": 70,
        "idle": 880,
        "iowait": 0,
        "irq": 0,
        "softirq": 0,
        "steal": 0,
    }

    result = calculate_cpu_usage(
        first,
        second,
    )

    assert result == 70.0


def test_calculate_cpu_usage_zero_delta():
    first = {
        "user": 100,
        "nice": 0,
        "system": 50,
        "idle": 850,
        "iowait": 0,
        "irq": 0,
        "softirq": 0,
        "steal": 0,
    }

    second = first.copy()

    result = calculate_cpu_usage(
        first,
        second,
    )

    assert result == 0.0