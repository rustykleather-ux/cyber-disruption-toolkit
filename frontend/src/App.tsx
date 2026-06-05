import { useEffect, useState } from "react";
import "./App.css";

type Alert = {
  id: number;
  title: string;
  severity: string;
  risk_score: number;
  host: string;
  user: string;
  source_ip: string;
  mitre_technique: string;
  technique_name: string;
  tactic: string;
  description: string;
  recommended_action: string;
};

function App() {
  const [alerts, setAlerts] = useState<Alert[]>([]);

  useEffect(() => {
    fetch("http://127.0.0.1:8000/alerts/")
      .then((response) => response.json())
      .then((data) => setAlerts(data))
      .catch((error) => console.error("Error fetching alerts:", error));
  }, []);

  return (
    <main className="app">
      <h1>Cyber Disruption Toolkit</h1>
      <p>Defensive alert dashboard</p>

      <section className="summary">
        <div>
          <h2>{alerts.length}</h2>
          <p>Total Alerts</p>
        </div>

        <div>
          <h2>{alerts.filter((a) => a.severity === "high").length}</h2>
          <p>High Severity</p>
        </div>

        <div>
          <h2>{alerts.filter((a) => a.risk_score >= 90).length}</h2>
          <p>Critical Risk</p>
        </div>
      </section>

      <section>
        <h2>Alerts</h2>

        <table>
          <thead>
            <tr>
              <th>Risk</th>
              <th>Severity</th>
              <th>Title</th>
              <th>Host</th>
              <th>User</th>
              <th>Source IP</th>
              <th>MITRE</th>
              <th>Tactic</th>
            </tr>
          </thead>

          <tbody>
            {alerts.map((alert) => (
              <tr key={alert.id}>
                <td>{alert.risk_score}</td>
                <td>{alert.severity}</td>
                <td>{alert.title}</td>
                <td>{alert.host}</td>
                <td>{alert.user}</td>
                <td>{alert.source_ip}</td>
                <td>
                  {alert.mitre_technique} - {alert.technique_name}
                </td>
                <td>{alert.tactic}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </section>
    </main>
  );
}

export default App;
