def detect_suspicious_powershell(event: dict):
    command = str(event.get("command_line") or "").lower()

    suspicious_terms = [
        "encodedcommand",
        "encoded command",
        "invoke-webrequest",
        "iex",
        "downloadstring",
        "bypass",
        "hidden",
    ]

    if "powershell" in command and any(term in command for term in suspicious_terms):
        return {
            "title": "Suspicious PowerShell Activity",
            "severity": "high",
            "risk_score": 85,
            "host": event.get("host"),
            "user": event.get("user"),
            "mitre_technique": "T1059.001",
            "source_ip": event.get("source_ip"),
            "recommended_action": "Isolate the host, preserve evidence, and review PowerShell logs.",
        }

    return None


def detect_failed_login(event: dict):
    event_type = str(event.get("event_type") or "").lower()
    status = str(event.get("status") or "").lower()

    if event_type == "login" and status == "failed":
        return {
            "title": "Failed Login Attempt",
            "severity": "medium",
            "risk_score": 45,
            "host": event.get("host"),
            "user": event.get("user"),
            "mitre_technique": "T1110",
            "source_ip": event.get("source_ip"),
            "recommended_action": "Review authentication logs and check for repeated failures from the same source.",
        }

    return None


def detect_new_admin_user(event: dict):
    event_type = str(event.get("event_type") or "").lower()
    group_name = str(event.get("group_name") or "").lower()

    if event_type == "user_added_to_group" and "admin" in group_name:
        return {
            "title": "User Added to Admin Group",
            "severity": "high",
            "risk_score": 80,
            "host": event.get("host"),
            "user": event.get("user"),
            "mitre_technique": "T1098",
            "source_ip": event.get("source_ip"),
            "recommended_action": "Verify the account change, confirm authorization, and review recent account activity.",
        }

    return None


def detect_suspicious_service_creation(event: dict):
    event_type = str(event.get("event_type") or "").lower()
    command = str(event.get("command_line") or "").lower()

    suspicious_terms = [
        "sc create",
        "powershell",
        "cmd.exe",
        "temp",
        "users\\public",
        "appdata",
    ]

    if event_type == "service_created" and any(term in command for term in suspicious_terms):
        return {
            "title": "Suspicious Service Creation",
            "severity": "high",
            "risk_score": 90,
            "host": event.get("host"),
            "user": event.get("user"),
            "mitre_technique": "T1543.003",
            "source_ip": event.get("source_ip"),
            "recommended_action": "Inspect the service binary path, validate the service owner, and isolate the host if unauthorized.",
        }

    return None


def run_detections(events: list[dict]):
    alerts = []

    detection_rules = [
        detect_suspicious_powershell,
        detect_failed_login,
        detect_new_admin_user,
        detect_suspicious_service_creation,
    ]

    for event in events:
        for rule in detection_rules:
            detection = rule(event)

            if detection:
                detection["event"] = event
                alerts.append(detection)

    return alerts