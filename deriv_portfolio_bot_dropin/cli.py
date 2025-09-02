#!/usr/bin/env python3
import asyncio
import typer
from rich import print
from pathlib import Path

app = typer.Typer(add_completion=False)

# --- tiny config loader (swap to pydantic later) ---
import os, yaml
def load_yaml(path: str):
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f) or {}

@app.command()
def validate_config(config: str = "config.example.yaml") -> None:
    cfg = load_yaml(config)
    required = ["mode", "account", "universe", "alpha", "risk", "execution"]
    missing = [k for k in required if k not in cfg]
    if missing:
        print(f"[red]Missing keys: {missing}[/red]")
        raise typer.Exit(code=1)
    print("[green]Config looks OK.[/green]")

@app.command()
def discover(config: str = "config.example.yaml") -> None:
    # TODO: implement with Deriv WS (`active_symbols` + `contracts_for`)
    print("[yellow]discover() stub — implement active_symbols + contracts_for and print multipliers-capable symbols[/yellow]")

@app.command()
def backtest(config: str = "config.example.yaml") -> None:
    print("[yellow]backtest() stub — implement vectorised walk-forward backtester[/yellow]")

@app.command()
def paper(config: str = "config.example.yaml") -> None:
    print("[yellow]paper() stub — connect WS, stream ticks, run strategies, simulate fills[/yellow]")

@app.command()
def live(config: str = "config.example.yaml", confirm: bool = typer.Option(False, "--confirm")) -> None:
    if not confirm:
        print("[red]Refusing to run live without --confirm[/red]")
        raise typer.Exit(code=1)
    print("[yellow]live() stub — execute multipliers trades with TP/SL[/yellow]")

@app.command()
def orstac_seed(folder: str = "./ORSTAC_XML", out: str = "./seed_params.yaml") -> None:
    # Minimal XML param miner (stub). Expand with real tag extraction.
    import xml.etree.ElementTree as ET, yaml, re
    params = {"ema_fast": [], "ema_slow": [], "boll_len": [], "boll_dev": [], "rsi_len": []}
    for p in Path(folder).glob("*.xml"):
        try:
            ET.parse(p)  # in real version, walk tags and extract numeric params
        except Exception:
            continue
    with open(out, "w", encoding="utf-8") as f:
        yaml.safe_dump({"seeded_params": params}, f)
    print(f"[green]Wrote seed params to {out} (stub).[/green]")

if __name__ == "__main__":
    app()
