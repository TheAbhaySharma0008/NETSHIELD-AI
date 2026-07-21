from collections import defaultdict
from datetime import datetime

from alerts import generate_alert

attempt_tracker = defaultdict(list)

TIME_WINDOW = 60
ATTEMPT_THRESHOLD = 20

alerted_ips = set()

def detect_bruteforce(
    source_ip,
    destination_port
):

    current_time = datetime.now()

    key = (
        source_ip,
        destination_port
    )

    attempt_tracker[key].append(
        current_time
    )

    recent_attempts = []

    for timestamp in attempt_tracker[key]:

        if (
            current_time - timestamp
        ).total_seconds() <= TIME_WINDOW:

            recent_attempts.append(
                timestamp
            )

    attempt_tracker[key] = recent_attempts

    if (
        len(recent_attempts)
        >= ATTEMPT_THRESHOLD
        and key not in alerted_ips
    ):

        alerted_ips.add(key)

        generate_alert(
            alert_type="BRUTE_FORCE",
            source_ip=source_ip,
            severity="CRITICAL",
            details=f"{len(recent_attempts)} attempts on port {destination_port}"
        )