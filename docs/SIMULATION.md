# Simulation

Segments are 2–6 seconds; size = bitrate × segment duration. Download time = segment duration × selected bitrate / effective throughput + latency. Effective throughput = bandwidth × (1−packet_loss). Buffer consumed during download, capped at buffer capacity. Startup downloads first segment. Rebuffer occurs if subsequent download exceeds buffer. QoE is an illustrative proxy documented in README.
