MITRE_ATTACK = {
    "T1059.001": {
        "technique_name": "PowerShell",
        "tactic": "Execution",
        "description": "Adversaries may abuse PowerShell commands and scripts.",
    },
    "T1110": {
        "technique_name": "Brute Force",
        "tactic": "Credential Access",
        "description": "Adversaries may use repeated login attempts to gain access.",
    },
    "T1098": {
        "technique_name": "Account Manipulation",
        "tactic": "Persistence",
        "description": "Adversaries may manipulate accounts to maintain access.",
    },
    "T1543.003": {
        "technique_name": "Windows Service",
        "tactic": "Persistence",
        "description": "Adversaries may create or modify Windows services to execute malicious payloads.",
    },
}


def enrich_alert(alert: dict):
    technique_id = alert.get("mitre_technique")

    mitre_data = MITRE_ATTACK.get(
        technique_id,
        {
            "technique_name": "Unknown",
            "tactic": "Unknown",
            "description": "No MITRE ATT&CK enrichment available.",
        },
    )

    return {
        **alert,
        **mitre_data,
    }