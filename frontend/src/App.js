import axios from "axios";
import { Bar } from "react-chartjs-2";
import { useEffect, useState } from "react";

// ✅ IMPORT CHART.JS CORE + COMPONENTS
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
  Tooltip,
  Legend
} from "chart.js";

// ✅ REGISTER (THIS IS CRITICAL)
ChartJS.register(
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
  Tooltip,
  Legend
);

function App() {
  const [data, setData] = useState(null);

  useEffect(() => {
    axios.get("http://127.0.0.1:8000/analytics")
      .then(res => {
        setData({
          labels: ["Total Expense", "Taxi", "Hotel"],
          datasets: [
            {
              label: "Expenses",
              data: [
                res.data.total_expense,
                res.data.taxi_expense,
                res.data.hotel_expense
              ]
            }
          ]
        });
      })
      .catch(err => console.error(err));
  }, []);

  return (
    <div style={{ width: "600px", margin: "auto" }}>
      <h2>Expense Dashboard</h2>

      {!data ? <p>Loading chart...</p> : <Bar data={data} />}
    </div>
  );
}

export default App;