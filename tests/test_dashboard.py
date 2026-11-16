from dashboard import progress_bar


def test_progress_bar_half():
    result = progress_bar(
        50,
        width=10,
    )

    assert result == "█████░░░░░"


def test_progress_bar_zero():
    result = progress_bar(
        0,
        width=10,
    )

    assert result == "░░░░░░░░░░"


def test_progress_bar_full():
    result = progress_bar(
        100,
        width=10,
    )

    assert result == "██████████"


def test_progress_bar_clamps_values():
    below_zero = progress_bar(
        -20,
        width=10,
    )

    above_hundred = progress_bar(
        150,
        width=10,
    )

    assert below_zero == "░░░░░░░░░░"
    assert above_hundred == "██████████"