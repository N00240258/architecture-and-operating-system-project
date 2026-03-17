#! /usr/bin/env -S uv run
# /// script
# requires-python = ">=3.14"
# dependencies = [
#     "psutil>=7.2.2",
# ]
# ///

import time
from datetime import datetime

import psutil

LOG_FILE = "system.log"
INTERVAL_SECONDS = 5
SAMPLES = 12  # 12 samples * 5 seconds = 1 minute


def test_get_metrics(row):
    assert "timestamp" in row
    assert "cpu_percent" in row
    assert "memory_percent" in row
    assert "disk_percent" in row


def get_metrics():
    """Return one metrics row:
    {
        "timestamp": timestamp,
        "cpu_percent": cpu_percent,
        "memory_percent": memory_percent,
        "disk_percent": disk_percent,
    }
    """
    # TODO: create a timestamp string with datetime.now().isoformat(timespec="seconds")

    # TODO: read CPU percent (hint: psutil.cpu_percent(interval=1))

    # TODO: read memory percent from psutil.virtual_memory()

    # TODO: read disk percent from psutil.disk_usage("/")

    # TODO: return a dictionary in the required order
    return {}


def init_log_file(path):
    """Create/overwrite the log file and write the header row."""
    # TODO: open with mode "w" and newline=""
    # TODO: use f.write("") to clear the file


def append_log_row(path, row):
    """
    Append one row to the log file with the format:

    timestamp=...,cpu_percent=...,memory_percent=...,disk_percent=...

    Each row should be on a new line.
    """
    # TODO: open with mode "a"
    # TODO: append the row with f.write(...)


def main():
    init_log_file(LOG_FILE)
    print(
        f"Logging {SAMPLES} samples to {LOG_FILE} every {INTERVAL_SECONDS} seconds..."
    )

    for i in range(SAMPLES):
        row = get_metrics()

        test_get_metrics(row)

        append_log_row(LOG_FILE, row)
        print(f"[{i + 1}/{SAMPLES}] {row}")
        if i < SAMPLES - 1:
            time.sleep(INTERVAL_SECONDS)

    print("Done.")


if __name__ == "__main__":
    main()
