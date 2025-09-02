# Deriv Synthetics Portfolio Bot — ORSTAC Edition

This is a scaffold. Use `AGENTS.md` as the build brief for Codex to implement the full system.

## Quickstart
```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt

cp .env.example .env   # add your DERIV_APP_ID and DERIV_API_TOKEN
python cli.py validate-config --config config.example.yaml
python cli.py discover --config config.example.yaml  # after Codex implements it
```

## Notes
- Paper by default; require `--confirm` to run live.
- See `AGENTS.md` for acceptance tests and module structure.
