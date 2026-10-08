"""Reproducible adaptive bitrate streaming simulator (synthetic network traces)."""
from dataclasses import dataclass
from math import sin, pi
from random import Random
from statistics import mean

BITRATES = [300, 750, 1200, 1850, 2850, 4300]  # kbps
SEGMENT_SECONDS = 4.0

@dataclass
class Result:
    algorithm: str
    summary: dict
    timeline: list


def network_trace(profile: str = "variable", segments: int = 90, seed: int = 42) -> list[float]:
    if not 10 <= segments <= 500:
        raise ValueError("segments must be between 10 and 500")
    if profile not in {"stable", "variable", "congested", "mobile"}:
        raise ValueError("unknown network profile")
    rng = Random(seed)
    trace = []
    for i in range(segments):
        if profile == "stable":
            bandwidth = 3300 + rng.gauss(0, 220)
        elif profile == "congested":
            bandwidth = 1200 + 700 * sin(2 * pi * i / 27) + rng.gauss(0, 250)
        elif profile == "mobile":
            bandwidth = 2300 + 1450 * sin(2 * pi * i / 33) + rng.gauss(0, 500)
            if i % 23 in (0, 1, 2):
                bandwidth *= 0.3
        else:
            bandwidth = 2500 + 1200 * sin(2 * pi * i / 35) + rng.gauss(0, 360)
            if i % 29 in (0, 1):
                bandwidth *= 0.45
        trace.append(round(max(180, bandwidth), 2))
    return trace


def choose_bitrate(algorithm: str, history: list[float], buffer: float, previous: int) -> int:
    if algorithm == "fixed":
        return 2850
    if algorithm == "buffer":
        if buffer < 5:
            return 300
        if buffer > 20:
            return 4300
        return BITRATES[min(len(BITRATES)-1, int((buffer - 5) / 3.2))]
    if algorithm == "throughput":
        estimate = mean(history[-5:]) if history else 1200
        safe = estimate * 0.8
    elif algorithm == "predictive":
        if not history:
            safe = 1000
        else:
            recent = history[-5:]
            trend = (recent[-1] - recent[0]) / max(1, len(recent) - 1)
            estimate = max(180, mean(recent[-3:]) + 1.5 * trend)
            safety = 0.65 if buffer < 8 else 0.82 if buffer < 16 else 0.92
            safe = estimate * safety
    else:
        raise ValueError("unknown algorithm")
    return max(b for b in BITRATES if b <= safe) if safe >= BITRATES[0] else BITRATES[0]


def simulate(trace: list[float], algorithm: str = "predictive") -> Result:
    if algorithm not in {"fixed", "buffer", "throughput", "predictive"}:
        raise ValueError("unknown algorithm")
    if not trace or any(t <= 0 for t in trace):
        raise ValueError("trace must contain positive bandwidth values")
    buffer = 8.0
    history = []
    previous = 750
    timeline = []
    stalls = 0.0
    switches = 0
    for index, throughput in enumerate(trace):
        selected = choose_bitrate(algorithm, history, buffer, previous)
        download_time = SEGMENT_SECONDS * selected / throughput
        stalled = max(0.0, download_time - buffer)
        stalls += stalled
        buffer = min(30.0, max(0.0, buffer - download_time) + SEGMENT_SECONDS)
        switches += int(selected != previous and index > 0)
        timeline.append({"segment": index + 1, "bandwidth_kbps": round(throughput, 1),
                         "bitrate_kbps": selected, "buffer_seconds": round(buffer, 2),
                         "stall_seconds": round(stalled, 3), "download_seconds": round(download_time, 2)})
        history.append(throughput)
        previous = selected
    avg_bitrate = mean(x["bitrate_kbps"] for x in timeline)
    # Illustrative QoE proxy, not a validated perceptual quality metric.
    qoe = avg_bitrate / 1000 - 4.3 * stalls / len(trace) - 0.08 * switches / len(trace)
    return Result(algorithm, {"avg_bitrate_kbps": round(avg_bitrate, 1),
                              "total_stall_seconds": round(stalls, 2),
                              "quality_switches": switches,
                              "qoe_proxy": round(qoe, 3),
                              "segments": len(trace)}, timeline)


def compare(profile="variable", segments=90, seed=42):
    trace = network_trace(profile, segments, seed)
    results = [simulate(trace, name) for name in ("fixed", "buffer", "throughput", "predictive")]
    return {"profile": profile, "segments": segments, "seed": seed,
            "algorithms": [{"name": r.algorithm, **r.summary} for r in results],
            "timelines": {r.algorithm: r.timeline for r in results},
            "note": "Predictive is a heuristic forecasting baseline, not a trained ML model. QoE is an illustrative proxy."}
