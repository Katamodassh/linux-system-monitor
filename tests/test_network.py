from network import calculate_network_rates


def test_calculate_network_rates():
    first = {
        "eth0": {
            "received_bytes": 1000,
            "transmitted_bytes": 500,
        }
    }

    second = {
        "eth0": {
            "received_bytes": 1600,
            "transmitted_bytes": 800,
        }
    }

    result = calculate_network_rates(
        first,
        second,
        interval=2,
    )

    assert (
        result["eth0"]["received_per_second"]
        == 300.0
    )

    assert (
        result["eth0"]["transmitted_per_second"]
        == 150.0
    )


def test_new_network_interface_is_ignored():
    first = {
        "eth0": {
            "received_bytes": 1000,
            "transmitted_bytes": 500,
        }
    }

    second = {
        "eth0": {
            "received_bytes": 1200,
            "transmitted_bytes": 600,
        },
        "wlan0": {
            "received_bytes": 500,
            "transmitted_bytes": 200,
        },
    }

    result = calculate_network_rates(
        first,
        second,
        interval=1,
    )

    assert "eth0" in result
    assert "wlan0" not in result