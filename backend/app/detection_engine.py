def detect_suspicious_powershell(event: dict):
    command = str(event.get("command_line") or "").lower()

    suspicious_terms = [
        "encodedcommand",
        "encoded command",
        "invoke-webrequest",
        "iex",
        "downloadstring",
        "bypass",
        "hidden"
    ]

    if "powershell" in command and any(term in command for term in suspicious_terms):
        return {
            "title": "Suspicious PowerShell Activity",
            "severity": "high",
            "mitre_technique": "T1059.001",
            "recommended_action": "Isolate the host, preserve evidence, and review PowerShell logs."
        }

    return None


def run_detections(events: list[dict]):
    alerts = []

    for event in events:
        detection = detect_suspicious_powershell(event)

        if detection:
            detection["event"] = event
            alerts.append(detection)

    return alerts