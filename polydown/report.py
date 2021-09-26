from rich import print
from . import theme


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
        if self.exist_files > 0:
            print(f"{theme.t_tick} {self.exist_files} files already exist, skipped.")
        # f"{theme.t_tick_d}> {self.exist_files} files already exist, downloaded and overwritten."
        print(f"{theme.t_tick_d} {self.downloaded_files} files downloaded.")

        if corrupted_files != []:
            print(
                f"{theme.t_cross} {len(corrupted_files)} files failed at the MD5 test:[/red]"
            )
            for i in corrupted_files:
                print(f"\t[red]{i}[/red]")
