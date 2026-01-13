# 🖥️ Anti Desk Time

A lightweight Python utility that detects user inactivity (mouse + keyboard)
and simulates natural mouse movement to prevent system idle time.

Designed with clean architecture, human-like behavior, and developer-friendly controls.

---

## ✨ Features

- 🖱️ Mouse and keyboard activity detection
- 🧠 Human-like mouse movement (small jitter, not teleporting)
- ⏱️ Configurable inactivity threshold
- ⌨️ Global hotkey to pause/resume the script
- 🕘 Work-hours aware (auto disables outside office time)
- 📜 Structured logging with timestamps
- 🛑 PyAutoGUI failsafe enabled for safety

---

## 📦 Requirements

- Python **3.9+**
- Supported on **Windows, macOS, and Linux**

---

## 📥 Installation

```bash
pip install pyautogui pynput
```

---

## ▶️ Usage

### Default Settings

```bash
python index.py
```

### Custom Configuration

```bash
python index.py \
  --inactivity-threshold 120 \
  --check-interval 10 \
  --work-start 10 \
  --work-end 19
```

---

## ⚙️ Command Line Options

| Option | Description |
|--------|-------------|
| `--check-interval` | Seconds between inactivity checks |
| `--inactivity-threshold` | Idle time before action (seconds) |
| `--move-duration` | Mouse movement duration |
| `--work-start` | Work day start hour (24h format) |
| `--work-end` | Work day end hour (24h format) |
---

## ⌨️ Controls

- **CTRL + SHIFT + P** → Pause / Resume the script
- **Move mouse to top-left corner** → Emergency stop (PyAutoGUI failsafe)
- **CTRL + C** → Exit the script safely

---

## 🕘 Work Hours Behavior

Script runs continuously, but:
- Mouse movement is triggered **only during configured work hours**
- Outside work hours, the script stays idle and performs no action

---

## 🔒 Safety Notes

- No mouse clicks are performed
- No keystrokes are injected
- Mouse movement is minimal and human-like
- Runs entirely locally (no network access)

---

## 🚀 Roadmap / Future Enhancements

- System tray support
- Multiple activity profiles (jitter, random walk)
- Config file support
- Background service mode
- Cross-platform installer

---

## 📜 Disclaimer

This tool is intended for learning and productivity automation purposes.
Use responsibly and in accordance with your organization's policies.

---

## 👤 Author

**Rhythm Dubey**  
Python Developer | Automation & Productivity Enthusiast
