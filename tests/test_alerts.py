from alerts import check_alerts


def test_no_alerts():
    metrics = {
        "cpu": 30.0,

        "memory": {
            "usage_percent": 50.0,
        },

        "disk": {
            "usage_percent": 40.0,
        },
    }

    alerts = check_alerts(metrics)

    assert alerts == []


def test_cpu_alert():
    metrics = {
        "cpu": 95.0,

        "memory": {
            "usage_percent": 50.0,
        },

        "disk": {
            "usage_percent": 40.0,
        },
    }

    alerts = check_alerts(metrics)

    assert "HIGH CPU: 95.00%" in alerts


def test_multiple_alerts():
    metrics = {
        "cpu": 95.0,

        "memory": {
            "usage_percent": 90.0,
        },

        "disk": {
            "usage_percent": 95.0,
        },
    }

    alerts = check_alerts(metrics)

    assert len(alerts) == 3