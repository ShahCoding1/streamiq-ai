# Architecture

React/Vite frontend → FastAPI REST and WebSocket → simulation engine → offline-trained gradient-boosting model → SQLAlchemy/SQLite. WebSocket streams deterministic per-segment results; REST persists sessions and exports results.
