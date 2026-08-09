#!/usr/bin/env python3

"""Safely create daily and seven-day review files without overwriting."""

from __future__ import annotations

import os
import re
import stat
import sys
from datetime import date, timedelta
from pathlib import Path


class ReviewSaveError(Exception):
    """A user-facing validation or save failure."""


def fail(message: str) -> None:
    raise ReviewSaveError(message)


def validate_date(value: str) -> date:
    if not re.fullmatch(r"[0-9]{4}-[0-9]{2}-[0-9]{2}", value):
        fail("Date must use YYYY-MM-DD.")
    try:
        parsed = date.fromisoformat(value)
    except ValueError:
        fail("Date is not a valid calendar date.")
    if parsed.isoformat() != value:
        fail("Date is not a valid calendar date.")
    return parsed


def prepare_output_dir(output_dir: Path) -> None:
    if output_dir.is_symlink():
        fail("Output directory must not be a symlink.")
    if output_dir.exists():
        if not output_dir.is_dir():
            fail("Output path is not a directory.")
        return
    try:
        output_dir.mkdir(parents=True, exist_ok=True)
    except OSError as error:
        fail(f"Unable to create output directory: {error.strerror or error}.")
    if output_dir.is_symlink():
        fail("Output directory must not be a symlink.")
    if not output_dir.is_dir():
        fail("Output path is not a directory.")


def open_source(source: Path) -> int:
    if source.is_symlink():
        fail("Source must be a regular, non-symlink file.")

    flags = os.O_RDONLY | getattr(os, "O_BINARY", 0)
    if hasattr(os, "O_NOFOLLOW"):
        flags |= os.O_NOFOLLOW

    try:
        source_fd = os.open(source, flags)
    except OSError:
        fail("Source must be a regular, non-symlink file.")

    try:
        source_stat = os.fstat(source_fd)
        if not stat.S_ISREG(source_stat.st_mode):
            fail("Source must be a regular, non-symlink file.")
        if source_stat.st_size == 0:
            fail("Source review is empty.")
    except Exception:
        os.close(source_fd)
        raise
    return source_fd


def copy_create_only(source: Path, destination: Path) -> None:
    source_fd = open_source(source)
    destination_fd: int | None = None
    created = False

    try:
        flags = os.O_WRONLY | os.O_CREAT | os.O_EXCL | getattr(os, "O_BINARY", 0)
        try:
            destination_fd = os.open(destination, flags, 0o644)
            created = True
        except FileExistsError:
            fail("Destination already exists; refusing to overwrite it.")
        except OSError as error:
            fail(f"Unable to create destination: {error.strerror or error}.")

        if hasattr(os, "fchmod"):
            os.fchmod(destination_fd, 0o644)

        while True:
            chunk = os.read(source_fd, 1024 * 1024)
            if not chunk:
                break
            view = memoryview(chunk)
            while view:
                written = os.write(destination_fd, view)
                if written == 0:
                    fail("Unable to write the complete review.")
                view = view[written:]
        os.fsync(destination_fd)
    except Exception:
        if destination_fd is not None:
            os.close(destination_fd)
            destination_fd = None
        if created:
            try:
                destination.unlink()
            except OSError:
                pass
        raise
    finally:
        os.close(source_fd)
        if destination_fd is not None:
            os.close(destination_fd)


def save_daily(output_dir: str, review_date: str, source_file: str) -> Path:
    parsed_date = validate_date(review_date)
    destination_dir = Path(output_dir)
    prepare_output_dir(destination_dir)
    destination = destination_dir / f"{parsed_date.isoformat()}-SUM.md"
    copy_create_only(Path(source_file), destination)
    return destination


def save_weekly(
    output_dir: str,
    start_date: str,
    end_date: str,
    source_file: str,
) -> Path:
    parsed_start = validate_date(start_date)
    parsed_end = validate_date(end_date)
    if parsed_end - timedelta(days=6) != parsed_start:
        fail("START_DATE must be six calendar days before END_DATE.")

    destination_dir = Path(output_dir)
    prepare_output_dir(destination_dir)
    destination = destination_dir / (
        f"{parsed_start.isoformat()}～{parsed_end.strftime('%m-%d')}-7dSUM.md"
    )
    copy_create_only(Path(source_file), destination)
    return destination


def main(arguments: list[str]) -> int:
    if sys.version_info < (3, 11):
        print("Python 3.11 or newer is required.", file=sys.stderr)
        return 2

    try:
        if not arguments:
            fail("Expected daily or weekly operation.")

        operation = arguments[0]
        if operation == "daily":
            if len(arguments) != 4:
                fail(
                    "Usage: save_review.py daily OUTPUT_DIR YYYY-MM-DD SOURCE_FILE"
                )
            destination = save_daily(*arguments[1:])
        elif operation == "weekly":
            if len(arguments) != 5:
                fail(
                    "Usage: save_review.py weekly OUTPUT_DIR START_DATE END_DATE "
                    "SOURCE_FILE"
                )
            destination = save_weekly(*arguments[1:])
        else:
            fail(f"Unknown operation: {operation}")
    except ReviewSaveError as error:
        print(error, file=sys.stderr)
        return 2

    print(destination)
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
