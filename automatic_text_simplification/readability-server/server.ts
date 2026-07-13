import express, { Application, Request, Response } from "express";
import { analyse, scores} from "./readability";

const app: Application = express();
const port = 3000; // The port your express server will be running on.

// Enable URL-encoded form data parsing
app.use(express.urlencoded({ extended: true }));

// Middleware to parse JSON bodies
app.use(express.json());

// Basic route
app.post("/", async (req, res) => {
  const analysis = await analyse(req.body.text);
  const scoreResult = scores(analysis);
  res.json({
    analysis,
    score: scoreResult,
  });
});
// Start the server
app.listen(port, () => {
  console.log(`Server is running on http://localhost:${port}`);
});
