# Development roadmap

1. **V1 — Simulation:** synthetic throughput profiles, four ABR baselines, buffer/rebuffer simulator, QoE proxy, dashboard, tests. COMPLETE.
2. **V2 — Real traces:** CSV import, data validation, train/test splits by trace/session, evaluation over seeds, CSV/JSON report export.
3. **V3 — Trained ML:** forecast next-segment throughput using lag features; compare to moving-average and trend baselines with MAE/RMSE and ABR QoE.
4. **V4 — Reinforcement learning:** formalize state/action/reward; train PPO/DQN agent on training traces, evaluate on unseen traces against baselines; track training seeds.
5. **V5 — Media systems:** local HLS/DASH segment playback, player telemetry, measured startup delay, throughput and buffer metrics.

**Scientific integrity:** Never claim an ML/RL model or live video player is implemented until it is built and evaluated.
