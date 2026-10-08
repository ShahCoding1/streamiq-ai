import pytest
from backend.simulator import BITRATES, network_trace, simulate, compare

def test_trace_is_reproducible():
    assert network_trace("mobile", 50, 3) == network_trace("mobile", 50, 3)

def test_profiles_have_positive_throughput():
    for profile in ("stable", "variable", "congested", "mobile"):
        assert all(x > 0 for x in network_trace(profile, 50))

def test_all_algorithms_produce_valid_results():
    trace = network_trace("variable", 40)
    for name in ("fixed", "buffer", "throughput", "predictive"):
        result = simulate(trace, name)
        assert len(result.timeline) == 40
        assert all(x["bitrate_kbps"] in BITRATES for x in result.timeline)
        assert result.summary["total_stall_seconds"] >= 0

def test_comparison_has_four_strategies():
    assert len(compare()["algorithms"]) == 4

def test_invalid_profile_rejected():
    with pytest.raises(ValueError):
        network_trace("invalid")

def test_invalid_algorithm_rejected():
    with pytest.raises(ValueError):
        simulate([1000.0], "invalid")
