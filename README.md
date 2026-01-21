# PING Log Analyzer

A lightweight Python-based log analyzer focused on **network ping logs**, providing **colorful terminal output** and an **explainable performance summary**.
Built for clarity, extensibility, and educational or research use.

## 🚀 Features

* Parses Linux `ping` output logs
* Color-coded latency display (green / yellow / red)
* Calculates:

  * Average latency
  * Minimum & maximum latency
  * Jitter (latency stability)
* Human-readable interpretation of network quality
* Modular and easy to extend for other log formats

## 📦 Requirements

* Python **3.8+**
* `colorama`

```bash
pip install colorama
```

## ▶️ Usage

```bash
python colorful_log_analyzer.py ping.log
```

## 📊 Output

* A clean, colored table showing:

  * ICMP sequence number
  * TTL
  * Latency (ms)
* An explainable summary interpreting network performance and stability

## 🧩 Extensibility

The analyzer is designed to be easily extended:

* Add new regex patterns for other log types
* Plug in additional metrics or visual indicators
* Expand the explanation engine for advanced analysis

## 🎓 Use Cases

* Network diagnostics
* Academic projects
* IoT / networking research
* Teaching log analysis concepts

## 📄 License

Open for educational, academic, and personal use.
