import sys

def print_progress(current: int, total: int, label: str = "", bar_length: int = 40) -> None:
    '''Prints a simple in-place progress bar to the terminal'''
    fraction = current / total if total else 0
    filled = int(bar_length * fraction)
    bar = "#" * filled + "-" * (bar_length - filled)
    percent = fraction * 100
    sys.stdout.write(f"\r{label} [{bar}] {percent:5.1f}% ({current}/{total})")
    sys.stdout.flush()
    if current == total:
        print()
