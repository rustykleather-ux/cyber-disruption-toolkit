MITRE_ATTACK = {
    "T1059.001": {
        "technique_name": "PowerShell",
        "tactic": "Execution",
        "description": "Adversaries may abuse PowerShell commands and scripts."
    },
    "T1110": {
        "technique_name": "Brute Force",
        "tactic": "Credential Access",
        "description": "Adversaries may use repeated login attempts to gain access."
    }
}


def enrich_alert(alert: dict):
    technique_id = alert.get("mitre_technique")

    mitre_data = MITRE_ATTACK.get(
        technique_id,
        {
            "technique_name": "Unknown",
            "tactic": "Unknown",
            "description": "No MITRE ATT&CK enrichment available."
        }
    )

    return {
        **alert,
        **mitre_data
    }