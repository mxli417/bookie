from bookie.sim.runner import simple_sim
from rich.console import Console

console = Console()

def main() -> None:
    r_seed = 15
    bookie_margin = 0.10
    console.print("[bold blue]Running a simple bookie simulation \
        with fixed random seed[/bold blue]")
    console.rule("[bold yellow] Simulation Run >>>>>>>")
    console.print("[italic yellow] random seed: {r_seed}, \
        bookie margin: {bookie_margin} [/italic yellow]")
    simple_sim(random_seed=r_seed, bookie_margin=bookie_margin, worst_case_pnl=-200.0)
    console.print("[bold italic green] Done! [/bold italic green]")

if __name__ == "__main__":
    main()
