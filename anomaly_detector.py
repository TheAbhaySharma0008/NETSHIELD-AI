from collections import deque
from datetime import datetime
from alerts import generate_alert

packet_times = deque()

TIME_WINDOW = 10
PACKET_THRESHOLD = 20



def detect_anomaly():

    current_time = datetime.now()

    packet_times.append(current_time)

    while (
        packet_times
        and
        (current_time - packet_times[0]).total_seconds()
        > TIME_WINDOW
    ):
        packet_times.popleft()

    if len(packet_times) >= PACKET_THRESHOLD:

        generate_alert(
            alert_type="ANOMALY",
            source_ip="NETWORK",
            severity="CRITICAL",
            details=f"Traffic spike detected ({len(packet_times)} packets)"
        )

        packet_times.clear()