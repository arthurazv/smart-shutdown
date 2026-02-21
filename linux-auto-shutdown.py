import subprocess
import datetime
import logging
from typing import List

# -----------------------------
# Configuration (Policy Layer)
# -----------------------------

CRITICAL_PORTS = [":22", ":47984", ":47989"]

SHUTDOWN_START_HOUR = 2
SHUTDOWN_START_MIN = 15
SHUTDOWN_END_HOUR = 4
SHUTDOWN_END_MIN = 0

LOG_FILE = "/var/log/auto_shutdown.log"

logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# -----------------------------
# Policy Logic
# -----------------------------

def is_in_time_window(current_time: datetime.datetime) -> bool:
    """Return True if current time is inside the shutdown window."""
    start_time = current_time.replace(
        hour=SHUTDOWN_START_HOUR,
        minute=SHUTDOWN_START_MIN,
        second=0,
        microsecond=0
    )
    end_time = current_time.replace(
        hour=SHUTDOWN_END_HOUR,
        minute=SHUTDOWN_END_MIN,
        second=0,
        microsecond=0
    )

    return start_time <= current_time <= end_time


def check_network_activity(ports: List[str]) -> bool:
    """
    Return True if any active connection is found on critical ports.
    Fail-safe: returns True if network check fails.
    """
    try:
        output = subprocess.check_output(
            ["/usr/sbin/ss", "-tn", "state", "established"],
            timeout=5,
            text=True
        )

        for line in output.splitlines():
            if any(port in line for port in ports):
                logging.info("Active network connection detected on critical port.")
                return True

        logging.info("No active connections on critical ports.")
        return False

    except subprocess.TimeoutExpired:
        logging.error("The 'ss' command exceeded timeout.")
        return True  # Fail-closed

    except Exception as e:
        logging.error(f"Network activity check failed: {e}")
        return True  # Fail-closed


# -----------------------------
# Mechanism Layer
# -----------------------------

def shutdown_system() -> None:
    """Execute system shutdown."""
    try:
        logging.info("Conditions met. Initiating system shutdown.")
        subprocess.run(["/bin/systemctl", "poweroff"], check=True)
    except subprocess.CalledProcessError as e:
        logging.error(f"Shutdown failed: {e}")


# -----------------------------
# Entry Point
# -----------------------------

def main():
    now = datetime.datetime.now()

    if not is_in_time_window(now):
        logging.info("Outside shutdown window. Skipping execution.")
        return

    if check_network_activity(CRITICAL_PORTS):
        logging.info("Shutdown aborted due to active network usage.")
        return

    shutdown_system()


if __name__ == "__main__":
    main()
