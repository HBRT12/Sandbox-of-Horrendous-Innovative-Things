import time
from rich.progress import Progress

with Progress() as progress:
    task = progress.add_task("loading...", total=None)  # total=None = indeterminate

    # Keep it alive for a bit
    for _ in range(50):  
        time.sleep(0.1)  # let Rich update
        progress.advance(task)  # triggers a refresh
