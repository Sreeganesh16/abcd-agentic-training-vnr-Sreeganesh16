import { useState, useEffect, useRef } from "react";
import axios from "axios";

function App() {
  const [count, setCount] = useState(0);
  const [time, setTime] = useState(10);
  const [running, setRunning] = useState(false);
  const [scores, setScores] = useState([]);
  const [highScore, setHighScore] = useState(0);
  const [clicked, setClicked] = useState(false);

  const savedRef = useRef(false);

  // Timer logic
  useEffect(() => {
    let timer;

    if (running && time > 0) {
      timer = setTimeout(() => setTime(time - 1), 1000);
    }

    if (time === 0 && running && !savedRef.current) {
      savedRef.current = true;
      setRunning(false);
      saveScore();
    }

    return () => clearTimeout(timer);
  }, [running, time]);

  // Fetch leaderboard
  const fetchScores = async () => {
    const res = await axios.get("http://localhost:5000/scores");
    setScores(res.data);
    if (res.data.length > 0) {
      setHighScore(res.data[0].score);
    }
  };

  useEffect(() => {
    fetchScores();
  }, []);

  // Click handler with animation
  const handleClick = () => {
    if (!running) return;

    setCount((prev) => prev + 1);

    // click animation trigger
    setClicked(true);
    setTimeout(() => setClicked(false), 100);
  };

  // Start game
  const startGame = () => {
    setCount(0);
    setTime(10);
    setRunning(true);
    savedRef.current = false;
  };

  // Save score
  const saveScore = async () => {
    await axios.post("http://localhost:5000/save-score", {
      score: count,
      time: 10,
    });
    fetchScores();
  };

  return (
    <div style={styles.container}>
      <h1 style={styles.title}>⚡ CLICK SPEED TEST ⚡</h1>

      <div style={styles.card}>
        <div style={styles.stats}>
          <div>⏳ {time}s</div>
          <div>🖱 {count}</div>
          <div style={styles.highScore}>🏆 {highScore}</div>
        </div>

        <button
          style={{
            ...styles.clickBtn,
            transform: clicked ? "scale(0.9)" : "scale(1)",
            boxShadow: clicked
              ? "0 0 10px #ff4757"
              : "0 0 25px #ff4757",
          }}
          onClick={handleClick}
          disabled={!running}
        >
          CLICK
        </button>

        <button style={styles.startBtn} onClick={startGame}>
          START GAME
        </button>
      </div>

      <div style={styles.leaderboard}>
        <h2 style={{ marginBottom: "10px" }}>🏆 LEADERBOARD</h2>
        {scores.slice(0, 5).map((s, i) => (
          <div key={i} style={styles.scoreItem}>
            #{i + 1} — {s.score}
          </div>
        ))}
      </div>
    </div>
  );
}

// 🎨 STYLES (Dark Neon Theme)
const styles = {
  container: {
    minHeight: "100vh",
    background: "#0f0f0f",
    color: "#fff",
    textAlign: "center",
    fontFamily: "Arial, sans-serif",
    paddingTop: "40px",
  },
  title: {
    fontSize: "42px",
    marginBottom: "30px",
    textShadow: "0 0 20px #00f2ff",
  },
  card: {
    background: "#1a1a1a",
    padding: "30px",
    borderRadius: "20px",
    width: "320px",
    margin: "auto",
    boxShadow: "0 0 30px rgba(0,255,255,0.2)",
  },
  stats: {
    display: "flex",
    justifyContent: "space-between",
    fontSize: "20px",
    marginBottom: "20px",
  },
  highScore: {
    color: "#FFD700",
    textShadow: "0 0 10px gold",
  },
  clickBtn: {
    padding: "20px 60px",
    fontSize: "22px",
    borderRadius: "12px",
    border: "none",
    background: "#ff4757",
    color: "white",
    cursor: "pointer",
    marginBottom: "15px",
    transition: "all 0.1s ease",
  },
  startBtn: {
    padding: "12px 30px",
    fontSize: "16px",
    borderRadius: "10px",
    border: "none",
    background: "#00f2ff",
    color: "#000",
    cursor: "pointer",
    boxShadow: "0 0 15px #00f2ff",
  },
  leaderboard: {
    marginTop: "30px",
  },
  scoreItem: {
    background: "#1f1f1f",
    margin: "6px auto",
    padding: "10px",
    width: "200px",
    borderRadius: "10px",
    boxShadow: "0 0 10px rgba(255,255,255,0.1)",
  },
};

export default App;