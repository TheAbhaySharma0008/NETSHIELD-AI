from datetime import datetime

from database import (
    Alert,
    Session
)

alerts = []

def generate_alert(
    alert_type,
    source_ip,
    severity,
    details
):

    alert = {
        "time": datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S"
        ),
        "type": alert_type,
        "source_ip": source_ip,
        "severity": severity,
        "details": details
    }

    alerts.append(alert)

    session = Session()

    db_alert = Alert(
        time=alert["time"],
        alert_type=alert["type"],
        source_ip=alert["source_ip"],
        severity=alert["severity"],
        details=alert["details"]
    )

    session.add(db_alert)
    session.commit()
    session.close()

    print("\n" + "=" * 60)
    print(f"[{severity}] {alert_type}")
    print(f"Source IP : {source_ip}")
    print(f"Details   : {details}")
    print("=" * 60)