require("dotenv").config(); // MUST be at top

const express = require("express");
const mongoose = require("mongoose");
const cors = require("cors");

const app = express();
app.use(cors());
app.use(express.json());

// ✅ Build connection string from .env
const mongoURI = `mongodb+srv://${process.env.MONGO_USER}:${process.env.MONGO_PASS}@${process.env.MONGO_CLUSTER}/clickgame?retryWrites=true&w=majority`;

mongoose.connect(process.env.MONGO_URI)
  .then(() => console.log("DB Connected"))
  .catch(err => console.log(err));

// schema
const ScoreSchema = new mongoose.Schema({
  score: Number,
  time: Number,
});

const Score = mongoose.model("Score", ScoreSchema);

// routes
app.post("/save-score", async (req, res) => {
  try {
    const { score, time } = req.body;

    if (score == null) {
      return res.status(400).send("Invalid score");
    }

    const newScore = new Score({ score, time });
    await newScore.save();

    res.send("Saved");
  } catch (err) {
    res.status(500).send("Error saving score");
  }
});

app.get("/scores", async (req, res) => {
  try {
    const scores = await Score.find().sort({ score: -1 });
    res.json(scores);
  } catch (err) {
    res.status(500).send("Error fetching scores");
  }
});

// use env port
const PORT = process.env.PORT || 5000;

app.listen(PORT, () => {
  console.log(`Server running on http://localhost:${PORT}`);
});