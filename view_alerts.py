from database import Session, Alert

session = Session()

alerts = session.query(Alert).all()

print("Total Alerts:", len(alerts))

for alert in alerts:

    print(
        alert.id,
        alert.time,
        alert.alert_type,
        alert.source_ip,
        alert.severity,
        alert.details
    )

session.close()