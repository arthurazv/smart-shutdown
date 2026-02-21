# Smart Shutdown

**Smart Shutdown** is a lightweight Linux automation tool designed to reduce unnecessary energy consumption by safely powering off a system during low-demand hours.

The system only shuts down if:

- It is inside a **configured shutdown time window**.
- No **active connections** are detected on critical ports.
- Network checks **complete successfully**.

The script follows a **fail-safe design**: if there is any uncertainty (timeout or error), the shutdown is aborted.

---

## Features

- **Time-window-based** shutdown policy.
- **Network activity detection** using `ss`.
- **Fail-closed safety behavior** (prevents accidental shutdowns).
- **Structured logging** for easy observability.
- **Cron-optimized**: Designed for automated execution.
- **Secure execution**: Uses absolute system paths and avoids shell usage.

---

## How It Works

1.  **Time Check:** Determines whether the current system time falls within the predefined shutdown window.
2.  **Network Audit:** Scans for active `ESTABLISHED` connections on critical ports.
3.  **Execution:** If both conditions are met, the script triggers a system shutdown via `systemctl poweroff`.

---

## Configuration

Configuration values are defined at the top of the script for easy modification:

| Variable              | Description                                      |
| :-------------------- | :----------------------------------------------- |
| `CRITICAL_PORTS`      | List of ports to monitor (e.g., SSH, Plex, Web). |
| `SHUTDOWN_START_HOUR` | The hour the window begins (24-hour format).     |
| `SHUTDOWN_END_HOUR`   | The hour the window ends.                        |
| `LOG_FILE`            | Path to the execution logs.                      |

---

## Example Cron Setup

To run the script every 5 minutes, add the following to your root crontab:

```bash
*/5 * * * * /usr/bin/python3 /path/to/smart_shutdown.py
```

---

## Security Considerations

- **Path Integrity:** Uses absolute binary paths to prevent path-injection attacks.
- **No shell=True:** Subprocesses are called directly to avoid shell injection vulnerabilities.
- **Fail-Closed Design:** Any script error or timeout defaults to "Abort," keeping the server online.
- **Privilege Management:** Intended to run via root cron to manage system power states safely.

---
