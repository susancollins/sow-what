#!/usr/bin/env python3
"""Command-line module for sow-what."""

import typer

app = typer.Typer()


@app.command()
def main():
    """
    Run sow-what.
    """
    print("sow-what coming soon...")


if __name__ == "__main__":
    app()
