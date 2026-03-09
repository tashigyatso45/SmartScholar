import { useEffect, useState } from "react";
import API_BASE from "../api";
import Subjectcard from "./Subjectcard";
import ProblemView from "./ProblemView";
import {
  Grid,
  Typography,
  CircularProgress,
  Alert,
  Box,
  Button,
} from "@mui/material";

const DIFFICULTIES = [
  {
    value: "easy",
    label: "Easy",
    emoji: "⭐",
    color: "#4CAF50",
    bg: "#E8F5E9",
    desc: "Simple problems to warm up!",
  },
  {
    value: "medium",
    label: "Medium",
    emoji: "⭐⭐",
    color: "#FF9500",
    bg: "#FFF3E0",
    desc: "A little more challenging!",
  },
  {
    value: "hard",
    label: "Hard",
    emoji: "⭐⭐⭐",
    color: "#F44336",
    bg: "#FFEBEE",
    desc: "Push your limits!",
  },
];

export default function Home({ onAnswer }) {
  const [subjects, setSubjects] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  // Quiz flow: 'subjects' → 'difficulty' → 'quiz'
  const [view, setView] = useState("subjects");
  const [selectedSubject, setSelectedSubject] = useState(null);
  const [problems, setProblems] = useState([]);
  const [problemsLoading, setProblemsLoading] = useState(false);
  const [problemsError, setProblemsError] = useState(null);

  useEffect(() => {
    fetch(`${API_BASE}/home`).then((resp) => {
      if (resp.ok) {
        resp.json().then((data) => {
          setSubjects(data);
          setLoading(false);
        });
      } else {
        setError("Couldn't load subjects. Please try again.");
        setLoading(false);
      }
    });
  }, []);

  function handleSubjectSelect(subject) {
    setSelectedSubject(subject);
    setProblems([]);
    setProblemsError(null);
    setView("difficulty");
  }

  async function handleDifficultySelect(difficulty) {
    setProblemsLoading(true);
    setProblemsError(null);
    setView("quiz");

    try {
      // Try cached problems first
      const resp = await fetch(
        `${API_BASE}/problems?subject=${encodeURIComponent(selectedSubject.type_operation)}&difficulty=${difficulty}`
      );
      const cached = await resp.json();

      if (Array.isArray(cached) && cached.length > 0) {
        setProblems(cached);
        setProblemsLoading(false);
        return;
      }

      // No cache — generate with Claude
      const genResp = await fetch(`${API_BASE}/problems/generate`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          subject: selectedSubject.type_operation,
          difficulty,
          count: 5,
        }),
      });

      if (!genResp.ok) {
        const err = await genResp.json();
        throw new Error(err.error || "Failed to generate problems.");
      }

      const generated = await genResp.json();
      setProblems(generated);
      setProblemsLoading(false);
    } catch (err) {
      setProblemsError(err.message);
      setProblemsLoading(false);
    }
  }

  function handleBack() {
    setView("subjects");
    setSelectedSubject(null);
    setProblems([]);
    setProblemsError(null);
  }

  // ── Subject grid ────────────────────────────────────────────────────────────
  if (loading) {
    return (
      <Box display="flex" justifyContent="center" mt={8}>
        <CircularProgress size={56} color="primary" />
      </Box>
    );
  }

  if (view === "subjects") {
    return (
      <Box>
        <Typography variant="h4" fontWeight={800} gutterBottom>
          📚 Choose a Subject
        </Typography>
        <Typography color="text.secondary" mb={4} fontSize="1.1rem">
          Pick a topic and let's practice together!
        </Typography>

        {error && (
          <Alert severity="error" sx={{ mb: 3 }}>
            {error}
          </Alert>
        )}

        {subjects.length ? (
          <Grid container spacing={3}>
            {subjects.map((subObject) => (
              <Grid item xs={12} sm={6} md={4} key={subObject.id}>
                <Subjectcard subject={subObject} onSelect={handleSubjectSelect} />
              </Grid>
            ))}
          </Grid>
        ) : (
          <Box textAlign="center" mt={8}>
            <Typography fontSize="5rem">🌟</Typography>
            <Typography variant="h5" fontWeight={800} mt={2}>
              Let's get started!
            </Typography>
            <Typography color="text.secondary" mt={1} fontSize="1.1rem">
              No subjects are available yet. Check back soon!
            </Typography>
          </Box>
        )}
      </Box>
    );
  }

  // ── Difficulty picker ───────────────────────────────────────────────────────
  if (view === "difficulty") {
    return (
      <Box>
        <Button
          onClick={handleBack}
          sx={{ mb: 3, fontWeight: 700 }}
          startIcon={<span>←</span>}
        >
          Back to Subjects
        </Button>

        <Typography variant="h4" fontWeight={800} gutterBottom>
          How tough do you want it? 💪
        </Typography>
        <Typography color="text.secondary" mb={4} fontSize="1.1rem">
          Subject:{" "}
          <strong style={{ color: "#FF8C00" }}>
            {selectedSubject.type_operation}
          </strong>
        </Typography>

        <Grid container spacing={3} justifyContent="center">
          {DIFFICULTIES.map((d) => (
            <Grid item xs={12} sm={4} key={d.value}>
              <Box
                onClick={() => handleDifficultySelect(d.value)}
                sx={{
                  bgcolor: d.bg,
                  border: `3px solid ${d.color}`,
                  borderRadius: 4,
                  p: 4,
                  textAlign: "center",
                  cursor: "pointer",
                  transition: "all 0.18s",
                  "&:hover": {
                    transform: "translateY(-6px)",
                    boxShadow: `0 12px 32px ${d.color}55`,
                  },
                }}
              >
                <Typography fontSize="3rem">{d.emoji}</Typography>
                <Typography
                  variant="h5"
                  fontWeight={900}
                  mt={1}
                  color={d.color}
                >
                  {d.label}
                </Typography>
                <Typography color="text.secondary" mt={1} fontSize="0.9rem">
                  {d.desc}
                </Typography>
              </Box>
            </Grid>
          ))}
        </Grid>
      </Box>
    );
  }

  // ── Quiz (loading or active) ────────────────────────────────────────────────
  if (view === "quiz") {
    if (problemsLoading) {
      return (
        <Box textAlign="center" mt={8}>
          <Typography fontSize="4rem" className="bounce-in">
            🤖
          </Typography>
          <CircularProgress color="primary" size={56} sx={{ mt: 3 }} />
          <Typography variant="h5" fontWeight={800} mt={3}>
            Generating your problems…
          </Typography>
          <Typography color="text.secondary" mt={1}>
            Hang tight, this takes just a moment!
          </Typography>
        </Box>
      );
    }

    if (problemsError) {
      return (
        <Box textAlign="center" mt={8}>
          <Typography fontSize="4rem">😕</Typography>
          <Typography variant="h5" fontWeight={800} mt={2}>
            Oops! Something went wrong.
          </Typography>
          <Alert severity="error" sx={{ mt: 2, mb: 3, textAlign: "left" }}>
            {problemsError}
          </Alert>
          <Button variant="contained" onClick={handleBack}>
            ← Go Back
          </Button>
        </Box>
      );
    }

    return (
      <ProblemView
        problems={problems}
        subject={selectedSubject}
        onBack={handleBack}
        onAnswer={onAnswer}
      />
    );
  }

  return null;
}
