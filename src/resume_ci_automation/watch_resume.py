from __future__ import annotations

import contextlib
import os
import select
import signal
import sys
import time
import termios
import tty
from pathlib import Path


PACKAGE_DIR = Path(__file__).resolve().parent
SRC_DIR = PACKAGE_DIR.parent
PROJECT_ROOT = SRC_DIR.parent

if __package__ in {None, ""}:
    if str(SRC_DIR) not in sys.path:
        sys.path.insert(0, str(SRC_DIR))
    from resume_ci_automation.pdf_generator import generate_pdf
else:
    from .pdf_generator import generate_pdf


WATCHED_FILES = (
    PROJECT_ROOT / "data" / "resume.yaml",
    PROJECT_ROOT / "templates" / "resume_template.tex.j2",
)

DEBOUNCE_SECONDS = 1.0
POLL_INTERVAL_SECONDS = 0.25
REDRAW_INTERVAL_SECONDS = 0.5


def clear_screen() -> None:
    print("\033[2J\033[H", end="")


def render_status(message: str, *, debounce_remaining: float | None = None) -> None:
    clear_screen()
    print("Resume watcher")
    print("- Watching data/resume.yaml")
    print("- Watching templates/resume_template.tex.j2")
    print(f"- {message}")
    if debounce_remaining is not None:
        print(f"- Debouncing rebuild for {max(0.0, debounce_remaining):.1f}s")
    print("Controls: q to quit, Ctrl-C to exit")
    sys.stdout.flush()


def snapshot(paths: tuple[Path, ...]) -> dict[Path, tuple[int, int] | None]:
    state: dict[Path, tuple[int, int] | None] = {}
    for path in paths:
        if path.exists():
            stat = path.stat()
            state[path] = (stat.st_mtime_ns, stat.st_size)
        else:
            state[path] = None
    return state


def read_keypress() -> str | None:
    if not sys.stdin.isatty():
        return None

    ready, _, _ = select.select([sys.stdin], [], [], 0)
    if not ready:
        return None

    return sys.stdin.read(1)


def build_pdf() -> None:
    os.chdir(PROJECT_ROOT)
    try:
        generate_pdf()
    except SystemExit as exc:
        print(f"PDF generation failed with exit code {exc.code}; watching will continue.")
    except Exception as exc:  # pragma: no cover - defensive guard for the watcher loop
        print(f"PDF generation failed: {exc}")


@contextlib.contextmanager
def raw_terminal_mode() -> None:
    if not sys.stdin.isatty():
        yield
        return

    fd = sys.stdin.fileno()
    original_settings = termios.tcgetattr(fd)
    tty.setcbreak(fd)
    try:
        yield
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, original_settings)


def should_exit(keypress: str | None) -> bool:
    return keypress in {"q", "Q", "\x03"}


def wait_for_activity(timeout: float) -> str | None:
    if sys.stdin.isatty():
        ready, _, _ = select.select([sys.stdin], [], [], timeout)
        if ready:
            return sys.stdin.read(1)
        return None

    time.sleep(timeout)
    return None


def main() -> None:
    stop_requested = False
    previous_state = snapshot(WATCHED_FILES)
    pending_change_at: float | None = None
    last_render_at = 0.0

    def request_stop(signum: int, frame: object) -> None:  # noqa: ARG001
        nonlocal stop_requested
        stop_requested = True

    signal.signal(signal.SIGINT, request_stop)

    with raw_terminal_mode():
        render_status("Generating resume once before starting the watcher...")
        build_pdf()
        previous_state = snapshot(WATCHED_FILES)
        render_status("Watching for changes.")

        while not stop_requested:
            keypress = wait_for_activity(POLL_INTERVAL_SECONDS)
            if should_exit(keypress):
                stop_requested = True
                break

            current_state = snapshot(WATCHED_FILES)
            now = time.monotonic()

            if current_state != previous_state:
                previous_state = current_state
                pending_change_at = now
                render_status("Change detected; waiting for changes to settle before rebuilding.", debounce_remaining=DEBOUNCE_SECONDS)
                continue

            if pending_change_at is not None:
                debounce_remaining = DEBOUNCE_SECONDS - (now - pending_change_at)
                if debounce_remaining > 0:
                    if now - last_render_at >= REDRAW_INTERVAL_SECONDS:
                        render_status("Change detected; waiting for changes to settle before rebuilding.", debounce_remaining=debounce_remaining)
                        last_render_at = now
                    continue

                render_status("Changes settled; regenerating resume now.")
                build_pdf()
                previous_state = snapshot(WATCHED_FILES)
                pending_change_at = None
                render_status("Watching for changes.")

    print("Watcher exited cleanly.")


if __name__ == "__main__":
    main()