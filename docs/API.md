# Api

FastAPI OpenAPI specification available at /docs. POST /api/simulation/run and /api/comparison/run accept Config: profile, segments, seed, base_bandwidth_kbps, latency_ms, packet_loss, segment_seconds, buffer_capacity, strategy. WS /ws/simulation accepts the same JSON and streams tick/complete events.
