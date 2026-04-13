"""Application entry point."""

import uvicorn
from rich.console import Console
from rich.panel import Panel
from rich.text import Text

from jrebel import __version__
from jrebel.config import get_settings


def print_banner(host: str, port: int) -> None:
    """Print startup banner with server information."""
    console = Console()

    banner = Text()
    banner.append("JRebel License Server\n", style="bold cyan")
    banner.append(f"Version {__version__}\n\n", style="dim")
    banner.append("Server running at:\n", style="green")
    banner.append(f"  http://{host}:{port}\n\n", style="bold white")
    banner.append("Activation URLs:\n", style="yellow")
    banner.append("  JRebel 7.1 and earlier: ", style="white")
    banner.append(f"http://localhost:{port}/{{tokenname}}\n", style="bold magenta")
    banner.append("  JRebel 2018.1+:         ", style="white")
    banner.append(f"http://localhost:{port}/{{guid}}\n\n", style="bold magenta")
    banner.append("Use any email address for activation.", style="dim")

    console.print(Panel(banner, border_style="cyan", padding=(1, 2)))


def main() -> None:
    """Run the application server."""
    settings = get_settings()

    print_banner(settings.host, settings.port)

    uvicorn.run(
        "jrebel.app:app",
        host=settings.host,
        port=settings.port,
        reload=settings.debug,
        log_level=settings.log_level.lower(),
        access_log=settings.debug,
    )


if __name__ == "__main__":
    main()
