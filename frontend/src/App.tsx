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
   const [file, setFile] = useState<File | null>(null);
   const [uploadMessage, setUploadMessage] = useState("");

  const fetchAlerts = async () => {
  const response = await fetch("http://127.0.0.1:8000/alerts/");
  const data = await response.json();
  setAlerts(data);
};

const uploadFile = async () => {
  if (!file) {
    setUploadMessage("Please choose a CSV file first.");
    return;
  }

  const formData = new FormData();
  formData.append("file", file);

  const response = await fetch("http://127.0.0.1:8000/uploads/csv", {
    method: "POST",
    body: formData,
  });

  if (!response.ok) {
    setUploadMessage("Upload failed.");
    return;
  }

  setUploadMessage("CSV uploaded successfully.");
  setFile(null);
  await fetchAlerts();
};

  useEffect(() => {
    fetchAlerts()
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
      <section className="upload-box">
  <h2>Upload Security Log</h2>

  <input
    type="file"
    accept=".csv"
    onChange={(e) => {
      if (e.target.files?.[0]) {
        setFile(e.target.files[0]);
      }
    }}
  />

  <button onClick={uploadFile}>Upload CSV</button>

  {uploadMessage && <p>{uploadMessage}</p>}
</section>
      <section>
        <h2>Alerts</h2>
      <h3>Alerts Loaded: {alerts.length}</h3>
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
                <td
                  style={{
                    color:
                      alert.risk_score >= 90
                        ? "red"
                        : alert.risk_score >= 70
                        ? "orange"
                        : "goldenrod",
                  }}
                  >
                  {alert.risk_score}
                  </td>
              </tr>
            ))}
          </tbody>
        </table>
      </section>
    </main>
  );
}

export default App;
