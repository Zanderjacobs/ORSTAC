# Deriv Synthetics Portfolio Bot — ORSTAC Edition

## Objective
Build a robust, 24/7 **multi-asset, multi-strategy** trading system for **Deriv Synthetics** using the Deriv WebSocket API. Safety, configurability, tests, and paper-by-default.

## Deliverables
- Codebase per the structure below, plus `requirements.txt`, `.env.example`, `config.example.yaml`, `Dockerfile`, `README.md`, and tests (pytest ≥80% for utils/alpha/alloc/risk/backtest).
- CLI with commands: `discover`, `backtest`, `paper`, `live --confirm`, `validate-config`, `orstac-seed`.

## Architecture
/bot
  /api          # Deriv WS: authorize, website_status, active_symbols, contracts_for, ticks/ohlc, proposal/buy/sell, balance/portfolio
  /data         # stream fanout, bar builders (1s/5s/1m), feature pipelines
  /alpha        # BaseStrategy + ema_trend, mean_revert, breakout, vol_squeeze, impulse_fade
  /alloc        # online bandit (thompson/ucb1) over symbol×strategy arms
  /risk         # vol-targeted sizing, kelly_fraction_cap, daily caps, cooldowns
  /exec         # multipliers executor (paper & live), TP/SL handling, order lifecycle
  /orstac       # XML idea miner: parse DBot XML for parameter **ideas** → seed_params.yaml
  /backtest     # vectorised, walk-forward; reuse alpha/risk/exec
  /storage      # sqlite/parquet, reports/
  /utils        # config, logging, retry, time, schema validation
/tests
cli.py
config.example.yaml
.env.example
Dockerfile
README.md

## Key requirements
- Universe discovery via `active_symbols` (Synthetic/Derived submarkets) refreshed hourly; verify Multipliers via `contracts_for`.
- Bandit allocator over symbol×strategy arms; reward = EWMA expectancy with drawdown penalty.
- Risk: ATR-based sizing, daily/global caps, cooldowns; **no martingale**.
- Execution: **Multipliers** with TP/SL. Paper/live modes.
- Backtest: walk-forward, metrics (Sharpe/Sortino, DD, MAR, CAGR, win rate, expectancy), equity + underwater plots.

## Tasks (in order)
1. Bootstrap project + config loader + CLI skeleton; pass `validate-config`.
2. Implement WS client: authorize, website_status, active_symbols, contracts_for, ticks/ohlc (subs), robust reconnect.
3. Data: 1s/5s/1m bar builders; features (EMA/RSI/ATR/Bollinger/Donchian, NR7).
4. Strategies: BaseStrategy + 5 models; param schemas + warmup handling.
5. Allocator: Thompson sampling (default) + UCB1 option; time-decay; per-symbol concurrency caps.
6. Risk engine: ATR sizing, kelly cap, daily/per-symbol loss caps, cooldowns, hard kill on drawdown.
7. Execution: paper executor; live multipliers executor with proposal/buy/monitor/close; safe shutdown.
8. ORSTAC idea miner: parse XML in `./ORSTAC_XML/`, write `seed_params.yaml` for defaults.
9. Backtest module: reuse alpha/risk/exec; outputs reports to `./reports/{timestamp}/`.
10. README + tests + pre-commit (black, isort, flake8, mypy).

## Acceptance tests
- `python cli.py validate-config --config config.example.yaml` exits 0.
- `python cli.py discover --config config.example.yaml` prints ≥20 synthetic symbols with verified multipliers constraints.
- `python cli.py backtest --config config.example.yaml` produces metrics + equity curve PNG.
- `python cli.py paper --config config.example.yaml` streams live ticks ≥30 min with auto-reconnect.
- `python cli.py live --config config.example.yaml --confirm` places a tiny trade and exits cleanly.

> NOTE: Study ideas in `https://github.com/Zanderjacobs/ORSTAC` (DBot XML). **Do not copy code.** Only mine parameter themes for seeding.
