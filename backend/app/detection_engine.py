def detect_suspicious_powershell(event: dict):
    command_line = event.get("command_line", "").lower()

    suspicious_terms = [
        "encodedcommand",
        "invoke-webrequest"
        "iex",
        "downloadstring",
        "bypass",
        "hidden",
    ]
    
    if "powershell" in command and any(term in command for term in suspicious_terms):
        return {
            "title": "Suspicious PowerShell Command Detected",
            "severity": "High",
            "mitre_technique": "T1059.001 - PowerShell",
            "recomendation": "Isolate the host, preserve evidence, and review Powershell commands."
        }
    
    return None

def run_detections(event: list[dict]):
    alerts = []
    
    for event in events:
        detections = [detect_suspicious_powershell(event)
        ]

        for detection in detections:
            if detection:
                detection["event"] = event
                alerts.append(detection)

    return alerts         