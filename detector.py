from collections import defaultdict
from datetime import datetime

from alerts import generate_alert

port_tracker = defaultdict(list)
alerted_ips = set()

TIME_WINDOW = 30
PORT_THRESHOLD = 3

def detect_port_scan(source_ip, destination_port):

    current_time = datetime.now()

    port_tracker[source_ip].append(
        (destination_port, current_time)
    )

    recent_entries = []

    for port, timestamp in port_tracker[source_ip]:

        time_difference = (
            current_time - timestamp
        ).total_seconds()

        if time_difference <= TIME_WINDOW:

            recent_entries.append(
                (port, timestamp)
            )

    port_tracker[source_ip] = recent_entries

    unique_ports = {
        port
        for port, _
        in recent_entries
    }

    if (
        len(unique_ports) >= PORT_THRESHOLD
        and source_ip not in alerted_ips
    ):

        alerted_ips.add(source_ip)

        generate_alert(
            alert_type="PORT_SCAN",
            source_ip=source_ip,
            severity="HIGH",
            details=f"Ports scanned: {sorted(unique_ports)}"
        )
        