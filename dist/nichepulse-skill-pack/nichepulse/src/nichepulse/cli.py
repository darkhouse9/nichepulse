"""NichePulse CLI — Command-line niche scoring tool."""

import click
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.columns import Columns
from rich import box

from .scoring import get_niche, list_niches, compare_niches, NicheScore, score_niche

console = Console()


def _grade_style(grade: str) -> str:
    """Return (open_tag, close_tag, border_color) for a grade."""
    styles = {
        "S": ("[bold green]", "[/bold green]", "green"),
        "A": ("[green]", "[/green]", "green"),
        "B": ("[yellow]", "[/yellow]", "yellow"),
        "C": ("[orange3]", "[/orange3]", "orange3"),
        "D": ("[red]", "[/red]", "red"),
    }
    return styles.get(grade, ("[white]", "[/white]", "white"))


def _render_niche(n: NicheScore, detailed: bool = False) -> Panel:
    """Render a single niche score as a rich panel."""
    open_tag, close_tag, border_color = _grade_style(n.grade)

    content = []
    content.append(f"[bold]{n.name}[/bold]")
    content.append("")
    dims = [
        ("Passion", n.passion),
        ("Buy Freq", n.buy_frequency),
        ("Gift", n.gift_potential),
        ("Competition", n.competition),
        ("Trend", n.trend),
    ]
    for label, val in dims:
        bar = "█" * val + "░" * (5 - val)
        content.append(f"  {label:12} {bar} {val}/5")

    content.append("")
    content.append(f"  {open_tag}TOTAL: {n.total}/25 (Grade: {n.grade}){close_tag}")
    content.append(f"  [italic]{n.verdict}[/italic]")
    content.append(f"  Est. Margin: {n.margin_estimate}")

    if detailed and n.notes:
        content.append("")
        for note in n.notes:
            content.append(f"  • {note}")

    return Panel(
        "\n".join(content),
        title=f"[bold]{n.name}[/bold]",
        border_style=border_color,
        box=box.ROUNDED,
    )


@click.group(invoke_without_command=True)
@click.version_option(version=__import__("nichepulse", fromlist=["__version__"]).__version__)
@click.pass_context
def main(ctx):
    """🎯 NichePulse — AI-Powered Niche Scoring for Creators

    Score, compare, and validate niches using a data-driven framework.
    """
    if ctx.invoked_subcommand is None:
        ctx.invoke(list)


@main.command()
@click.argument("niche")
@click.option("--detailed", "-d", is_flag=True, help="Show detailed analysis")
def score(niche: str, detailed: bool):
    """Score a single niche keyword.

    Example: nichepulse score mushroom-foraging
    """
    n = get_niche(niche)
    if n is None:
        console.print(f"[red]Niche '{niche}' not found in database.[/red]")
        console.print("Run [bold]nichepulse list[/bold] to see available niches or use [bold]nichepulse custom[/bold] to score your own.")
        return

    # Override detailed if requested
    if detailed and n.notes:
        console.print(_render_niche(n, detailed=True))
    else:
        console.print(_render_niche(n, detailed=detailed))


@main.command()
@click.option("--top", "-n", default=15, help="Show top N niches")
@click.option("--min-score", default=0, help="Minimum total score filter")
def list(top: int, min_score: int):
    """List all pre-scored niches, ranked by total score."""
    niches = list_niches()
    if min_score:
        niches = [n for n in niches if n.total >= min_score]

    table = Table(
        title=f"🎯 NichePulse — Top {min(top, len(niches))} Niches (Ranked)",
        box=box.SIMPLE_HEAVY,
        show_lines=True,
    )
    table.add_column("#", style="bold", width=4)
    table.add_column("Niche", min_width=28)
    table.add_column("Passion", width=8, justify="center")
    table.add_column("Buy", width=6, justify="center")
    table.add_column("Gift", width=6, justify="center")
    table.add_column("Comp.", width=6, justify="center")
    table.add_column("Trend", width=7, justify="center")
    table.add_column("TOTAL", width=7, justify="center")
    table.add_column("Grade", width=7, justify="center")
    table.add_column("Margin", min_width=30)

    grade_styles = {"S": "bold green", "A": "green", "B": "yellow", "C": "orange3", "D": "red"}

    for i, n in enumerate(niches[:top]):
        style = grade_styles.get(n.grade, "white")
        table.add_row(
            str(i + 1),
            n.name,
            str(n.passion),
            str(n.buy_frequency),
            str(n.gift_potential),
            str(n.competition),
            str(n.trend),
            f"[bold]{n.total}[/bold]/25",
            f"[{style}]{n.grade}[/{style}]",
            n.margin_estimate,
        )

    console.print(table)
    console.print(f"\n[italic]💡 Run 'nichepulse score <niche>' for detailed analysis[/italic]")


@main.command()
@click.argument("keywords")
def compare(keywords: str):
    """Compare multiple niches side by side.

    Example: nichepulse compare "mushroom-foraging birding trail-running"
    """
    niche_list = keywords.split()
    results = compare_niches(niche_list)
    if not results:
        console.print("[red]No matching niches found.[/red]")
        return

    panels = [_render_niche(n, detailed=True) for n in results[:6]]
    console.print(Columns(panels))


@main.command()
@click.argument("name")
@click.option("--passion", "-p", type=int, prompt="Passion level (1-5)")
@click.option("--buy-freq", "-b", type=int, prompt="Buy frequency (1-5)")
@click.option("--gift", "-g", type=int, prompt="Gift potential (1-5)")
@click.option("--competition", "-c", type=int, prompt="Competition level (1=high, 5=low)")
@click.option("--trend", "-t", type=int, prompt="Trend direction (1=down, 5=up)")
@click.option("--note", "-n", multiple=True, help="Add notes (repeatable)")
def custom(name: str, passion: int, buy_freq: int, gift: int, competition: int, trend: int, note: tuple):
    """Score a custom niche interactively.

    Example: nichepulse custom "Urban Beekeeping"
    """
    n = score_niche(
        name=name,
        passion=passion,
        buy_frequency=buy_freq,
        gift_potential=gift,
        competition=competition,
        trend=trend,
        notes=list(note) if note else None,
    )
    console.print(_render_niche(n, detailed=True))


@main.command()
@click.argument("keywords")
def roadmap(keywords: str):
    """Generate a 90-day action roadmap for the top-scoring niche.

    Example: nichepulse roadmap "mushroom-foraging birding"
    """
    results = compare_niches(keywords.split())
    if not results:
        console.print("[red]No matching niches found.[/red]")
        return

    winner = results[0]

    table = Table(
        title=f"🗺️ 90-Day Roadmap: {winner.name}",
        box=box.ROUNDED,
    )
    table.add_column("Phase", style="bold cyan", width=18)
    table.add_column("Days", width=8)
    table.add_column("Actions", min_width=50)
    table.add_column("Deliverable", min_width=25)

    phases = [
        ("Foundation", "1-14",
         "Design 10-15 core designs. Set up Etsy shop. Keyword research.",
         "15 designs + shop live"),
        ("Validation", "15-35",
         "List all designs. Collect first 20 reviews. Test pricing.",
         "15 listings + 20 reviews"),
        ("Optimization", "36-60",
         "Kill bottom 30% designs. Double down on winners. Pinterest launch.",
         "Top 10 designs identified"),
        ("Scale", "61-90",
         "Add Amazon Merch. Launch Shopify. First paid ad test.",
         "3 platforms + ad data"),
    ]

    for phase_name, days, actions, deliverable in phases:
        table.add_row(phase_name, days, actions, deliverable)

    console.print(table)
    console.print(f"\n[bold]Target: $500-2,000/month by Day 90[/bold]")
    console.print(f"[italic]Based on niche score {winner.total}/25 ({winner.grade}-grade opportunity)[/italic]")


if __name__ == "__main__":
    main()
