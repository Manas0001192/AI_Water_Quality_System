
import yagmail

def send_email_alert(df):

    sender_email = "vicharemanas8406@gmail.com"
    app_password = "acenstdagwyiuufd"
    receiver_email = "receiver_email@gmail.com"

    critical_cases = df[df["Risk_Level"] == "CRITICAL"]

    if not critical_cases.empty:

        yag = yagmail.SMTP(sender_email, app_password)

        subject = "🚨 CRITICAL Water Quality Alert"
        body = f"{len(critical_cases)} critical samples detected. Immediate action required."

        yag.send(
            to=receiver_email,
            subject=subject,
            contents=body,
            attachments="risk_report.csv"
        )
