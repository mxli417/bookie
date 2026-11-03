from rich.console import Console

from bookie.sim.runner import simple_sim

console = Console()


def main() -> None:
    r_seed = 15
    bookie_margin = 0.10
    console.print("[bold blue]Running a simple simulation with a fixed seed[/]")
    console.rule("[bold yellow] Simulation Run >>>>>>>")
    console.print(
        f"[italic yellow]random seed: {r_seed}, "
        f"bookie margin: {bookie_margin:.0%}[/]"
    )
    simple_sim(random_seed=r_seed, bookie_margin=bookie_margin, worst_case_pnl=-200.0)
    console.print("[bold italic green] Done! [/bold italic green]")


if __name__ == "__main__":
    main()
