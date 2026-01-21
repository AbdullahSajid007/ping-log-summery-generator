#!/usr/bin/env python3
"""
Colorful & Explainable Log Analyzer (Ping-focused, extensible)
-------------------------------------------------------------
This script reads a log file (e.g., Linux ping output), parses results,
prints COLORFUL terminal output, and generates an EXPLAINABLE summary.

Designed to be easily extended for other log types.

Usage:
  python colorful_log_analyzer.py ping.log

Requirements:
  - Python 3.8+
  - colorama (pip install colorama)
"""

import re
import sys
import statistics
from typing import List

try:
    from colorama import Fore, Style, init
    init(autoreset=True)
except ImportError:
    print("colorama not installed. Run: pip install colorama")
    sys.exit(1)

# -----------------------------
# Regex patterns (extensible)
# -----------------------------
PING_REPLY_PATTERN = re.compile(
    r"bytes from (?P<ip>[\d\.]+): icmp_seq=(?P<seq>\d+) ttl=(?P<ttl>\d+) time=(?P<time>[\d\.]+) ms"
)

# -----------------------------
# Data structure
# -----------------------------
class PingResult:
    def __init__(self, seq: int, ttl: int, time_ms: float):
        self.seq = seq
        self.ttl = ttl
        self.time_ms = time_ms

# -----------------------------
# Parser
# -----------------------------
def parse_ping_log(lines: List[str]) -> List[PingResult]:
    results = []
    for line in lines:
        match = PING_REPLY_PATTERN.search(line)
        if match:
            results.append(
                PingResult(
                    seq=int(match.group("seq")),
                    ttl=int(match.group("ttl")),
                    time_ms=float(match.group("time"))
                )
            )
    return results

# -----------------------------
# Color logic
# -----------------------------
def latency_color(latency: float) -> str:
    if latency < 0.3:
        return Fore.GREEN
    elif latency < 0.5:
        return Fore.YELLOW
    else:
        return Fore.RED

# -----------------------------
# Explanation engine
# -----------------------------
def explain_results(results: List[PingResult]):
    times = [r.time_ms for r in results]

    avg = statistics.mean(times)
    minimum = min(times)
    maximum = max(times)
    jitter = statistics.pstdev(times)

    print("\n" + Fore.CYAN + "=== EXPLAINABLE SUMMARY ===")

    print(f"{Fore.WHITE}Packets received      : {Fore.GREEN}{len(results)}")
    print(f"{Fore.WHITE}Average latency       : {Fore.YELLOW}{avg:.3f} ms")
    print(f"{Fore.WHITE}Minimum latency       : {Fore.GREEN}{minimum:.3f} ms")
    print(f"{Fore.WHITE}Maximum latency       : {Fore.RED}{maximum:.3f} ms")
    print(f"{Fore.WHITE}Jitter (stability)    : {Fore.MAGENTA}{jitter:.3f} ms")

    print("\n" + Fore.CYAN + "Interpretation:")

    if avg < 1:
        print(Fore.GREEN + "• Network latency is excellent (sub-millisecond).")
    elif avg < 10:
        print(Fore.YELLOW + "• Network latency is good and suitable for real-time apps.")
    else:
        print(Fore.RED + "• High latency detected; may affect real-time services.")

    if jitter < 0.1:
        print(Fore.GREEN + "• Very stable connection (low jitter).")
    else:
        print(Fore.YELLOW + "• Some variability in latency observed.")

# -----------------------------
# Pretty printer
# -----------------------------
def print_colorful_table(results: List[PingResult]):
    print(Fore.CYAN + "\nSeq   TTL   Latency (ms)")
    print(Fore.CYAN + "------------------------")

    for r in results:
        color = latency_color(r.time_ms)
        print(f"{r.seq:<5} {r.ttl:<5} {color}{r.time_ms:>8.3f}{Style.RESET_ALL}")

# -----------------------------
# Main
# -----------------------------
def main():
    if len(sys.argv) != 2:
        print("Usage: python colorful_log_analyzer.py <logfile>")
        sys.exit(1)

    logfile = sys.argv[1]

    try:
        with open(logfile, 'r') as f:
            lines = f.readlines()
    except FileNotFoundError:
        print(Fore.RED + "Log file not found.")
        sys.exit(1)

    results = parse_ping_log(lines)

    if not results:
        print(Fore.RED + "No ping data detected in log file.")
        sys.exit(1)

    print_colorful_table(results)
    explain_results(results)


if __name__ == "__main__":
    main()
