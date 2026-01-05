from rich.progress import Progress
import time as t
with Progress() as progress:
    bar_1 = progress.add_task('[red]Loading[yellow]...', total=None)
    def bar_update():
        while not progress.finished:
            progress.update(bar_1, advance=50)
            t.sleep(0.5)
            progress.update(bar_1, advance=-20)
            t.sleep(0.5) 
