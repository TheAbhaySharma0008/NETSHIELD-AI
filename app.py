from flask import Flask, render_template
from database import Session, Alert

app = Flask(__name__)


@app.route("/")
def dashboard():

    session = Session()

    alerts = session.query(Alert).all()

    total_alerts = len(alerts)

    high_alerts = len(
        [alert for alert in alerts
         if alert.severity == "HIGH"]
    )

    critical_alerts = len(
        [alert for alert in alerts
         if alert.severity == "CRITICAL"]
    )

    # Threat Level Logic
    if critical_alerts >= 5:
        threat_level = "HIGH"

    elif critical_alerts >= 2:
        threat_level = "MEDIUM"

    else:
        threat_level = "LOW"

    session.close()

    return render_template(
        "index.html",
        alerts=alerts,
        total_alerts=total_alerts,
        high_alerts=high_alerts,
        critical_alerts=critical_alerts,
        threat_level=threat_level
    )


if __name__ == "__main__":
    app.run(debug=True)