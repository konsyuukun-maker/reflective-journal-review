#!/usr/bin/env python3

from __future__ import annotations

import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = (
    ROOT
    / "skills"
    / "reflective-journal-review"
    / "scripts"
    / "save_review.py"
)


class SaveReviewTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary_directory = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary_directory.cleanup)
        self.test_dir = Path(self.temporary_directory.name)
        self.source = self.test_dir / "review.md"
        self.source_content = "# Review\n\nSynthetic content.\n"
        self.source.write_text(self.source_content, encoding="utf-8")
        self.output = self.test_dir / "output"

    def run_script(
        self,
        *arguments: object,
        environment: dict[str, str] | None = None,
    ) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [sys.executable, str(SCRIPT), *(str(argument) for argument in arguments)],
            capture_output=True,
            check=False,
            text=True,
            encoding="utf-8",
            env=environment,
        )

    def assert_rejected(self, *arguments: object) -> subprocess.CompletedProcess[str]:
        result = self.run_script(*arguments)
        self.assertEqual(result.returncode, 2, result)
        self.assertEqual(result.stdout, "")
        self.assertNotEqual(result.stderr.strip(), "")
        return result

    def test_daily_save_preserves_content_and_reports_path(self) -> None:
        result = self.run_script("daily", self.output, "2026-03-14", self.source)
        destination = self.output / "2026-03-14-SUM.md"

        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(result.stdout.strip(), str(destination))
        self.assertEqual(destination.read_text(encoding="utf-8"), self.source_content)
        if os.name != "nt":
            self.assertEqual(destination.stat().st_mode & 0o777, 0o644)

    def test_weekly_save_uses_expected_unicode_filename(self) -> None:
        result = self.run_script(
            "weekly",
            self.output,
            "2026-03-09",
            "2026-03-15",
            self.source,
        )
        destination = self.output / "2026-03-09～03-15-7dSUM.md"

        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(result.stdout.strip(), str(destination))
        self.assertEqual(destination.read_bytes(), self.source.read_bytes())

    def test_weekly_path_is_utf8_when_parent_encoding_is_cp1252(self) -> None:
        environment = os.environ.copy()
        environment["PYTHONIOENCODING"] = "cp1252"

        result = self.run_script(
            "weekly",
            self.output,
            "2026-03-09",
            "2026-03-15",
            self.source,
            environment=environment,
        )

        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("～", result.stdout)

    def test_existing_destination_is_not_overwritten(self) -> None:
        self.output.mkdir()
        destination = self.output / "2026-03-14-SUM.md"
        destination.write_text("keep me", encoding="utf-8")

        result = self.assert_rejected(
            "daily", self.output, "2026-03-14", self.source
        )

        self.assertIn("refusing to overwrite", result.stderr)
        self.assertEqual(destination.read_text(encoding="utf-8"), "keep me")

    def test_invalid_dates_and_weekly_range_are_rejected(self) -> None:
        self.assert_rejected("daily", self.output, "2026-02-30", self.source)
        self.assert_rejected("daily", self.output, "03-14-2026", self.source)
        self.assert_rejected(
            "weekly",
            self.output,
            "2026-03-08",
            "2026-03-15",
            self.source,
        )

    def test_empty_source_is_rejected(self) -> None:
        empty_source = self.test_dir / "empty.md"
        empty_source.touch()

        self.assert_rejected("daily", self.output, "2026-03-14", empty_source)

    def test_missing_source_and_output_file_are_rejected(self) -> None:
        missing_source = self.test_dir / "missing.md"
        self.assert_rejected("daily", self.output, "2026-03-14", missing_source)

        output_file = self.test_dir / "not-a-directory"
        output_file.write_text("keep me", encoding="utf-8")
        self.assert_rejected("daily", output_file, "2026-03-14", self.source)
        self.assertEqual(output_file.read_text(encoding="utf-8"), "keep me")

    def test_invalid_operation_and_argument_counts_are_rejected(self) -> None:
        self.assert_rejected()
        self.assert_rejected("monthly")
        self.assert_rejected("daily", self.output, "2026-03-14")
        self.assert_rejected(
            "weekly", self.output, "2026-03-09", "2026-03-15"
        )

    def test_source_symlink_is_rejected_when_supported(self) -> None:
        linked_source = self.test_dir / "linked-source.md"
        try:
            linked_source.symlink_to(self.source)
        except (NotImplementedError, OSError) as error:
            self.skipTest(f"symlink creation is unavailable: {error}")

        self.assert_rejected("daily", self.output, "2026-03-14", linked_source)

    def test_output_directory_symlink_is_rejected_when_supported(self) -> None:
        real_output = self.test_dir / "real-output"
        real_output.mkdir()
        linked_output = self.test_dir / "linked-output"
        try:
            linked_output.symlink_to(real_output, target_is_directory=True)
        except (NotImplementedError, OSError) as error:
            self.skipTest(f"symlink creation is unavailable: {error}")

        self.assert_rejected("daily", linked_output, "2026-03-14", self.source)
        self.assertEqual(list(real_output.iterdir()), [])

    def test_destination_symlink_is_rejected_when_supported(self) -> None:
        self.output.mkdir()
        protected_file = self.test_dir / "protected.md"
        protected_file.write_text("keep me", encoding="utf-8")
        destination = self.output / "2026-03-14-SUM.md"
        try:
            destination.symlink_to(protected_file)
        except (NotImplementedError, OSError) as error:
            self.skipTest(f"symlink creation is unavailable: {error}")

        self.assert_rejected("daily", self.output, "2026-03-14", self.source)
        self.assertEqual(protected_file.read_text(encoding="utf-8"), "keep me")

    def test_concurrent_creation_allows_exactly_one_writer(self) -> None:
        command = [
            sys.executable,
            str(SCRIPT),
            "daily",
            str(self.output),
            "2026-03-14",
            str(self.source),
        ]
        processes = [
            subprocess.Popen(
                command,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                encoding="utf-8",
            )
            for _ in range(2)
        ]
        results = [process.communicate() for process in processes]
        return_codes = sorted(process.returncode for process in processes)

        self.assertEqual(return_codes, [0, 2], results)
        destination = self.output / "2026-03-14-SUM.md"
        self.assertEqual(destination.read_text(encoding="utf-8"), self.source_content)


if __name__ == "__main__":
    unittest.main()
