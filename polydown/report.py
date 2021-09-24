from rich import print as rprint

# themes
t_tick = "[on dark_khaki]📁✓[/on dark_khaki][green]"
t_tick_d = "[on cyan]📁✓[/on cyan][cyan]"
t_cross = "[on red]📁×[/on red][red]"
# /themes


class Report:
    def __init__(self):
        self.exist_files = 0
        self.downloaded_files = 0

    def add(self, type):
        if type == "exist":
            self.exist_files += 1
        elif type == "downloaded":
            self.downloaded_files += 1

    def show_report(self, overwrite, corrupted_files):
        print()
        if overwrite:
            rprint(
                f"{t_tick_d}> {self.exist_files} files already exist, downloaded and overwritten."
            )
        else:
            rprint(f"{t_tick}> {self.exist_files} files already exist, skipped.")
        rprint(f"{t_tick_d}> {self.downloaded_files} files downloaded.")
        if corrupted_files != []:
            rprint(
                f"{t_cross}> {len(corrupted_files)} files failed at the MD5 test:[/red]"
            )
            for i in corrupted_files:
                rprint(f"\t[red]{i}[/red]")
