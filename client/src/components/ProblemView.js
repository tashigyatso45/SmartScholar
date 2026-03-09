import { useState } from "react";
import {
  Box,
  Typography,
  Button,
  LinearProgress,
  Chip,
} from "@mui/material";

export default function ProblemView({ problems, subject, onBack, onAnswer }) {
  const [currentIndex, setCurrentIndex] = useState(0);
  const [selectedAnswer, setSelectedAnswer] = useState(null);
  const [showFeedback, setShowFeedback] = useState(false);
  const [sessionScore, setSessionScore] = useState(0);
  const [streak, setStreak] = useState(0);
  const [correctCount, setCorrectCount] = useState(0);
  const [done, setDone] = useState(false);

  const problem = problems[currentIndex];
  const progress = (currentIndex / problems.length) * 100;
  const isCorrect = selectedAnswer === problem?.correct_answer;

  function handleSelectAnswer(option) {
    if (showFeedback) return;
    setSelectedAnswer(option);
    setShowFeedback(true);
    const correct = option === problem.correct_answer;
    if (correct) {
      setSessionScore((s) => s + 10);
      setStreak((s) => s + 1);
      setCorrectCount((c) => c + 1);
    } else {
      setStreak(0);
    }
    onAnswer(correct);
  }

  function handleNext() {
    if (currentIndex < problems.length - 1) {
      setCurrentIndex((i) => i + 1);
      setSelectedAnswer(null);
      setShowFeedback(false);
    } else {
      setDone(true);
    }
  }

  // ── Results screen ────────────────────────────────────────────────────────
  if (done) {
    const pct = Math.round((correctCount / problems.length) * 100);
    const stars = pct >= 90 ? "⭐⭐⭐" : pct >= 60 ? "⭐⭐" : "⭐";
    const message =
      pct >= 90
        ? "You're a Math Star! 🌟"
        : pct >= 60
        ? "Great Job! Keep it up! 🎉"
        : "Nice try! Practice makes perfect! 💪";

    return (
      <Box textAlign="center" sx={{ py: 6 }}>
        <Typography fontSize="5rem" className="pop-in">
          {stars}
        </Typography>
        <Typography variant="h3" fontWeight={900} mt={2} color="primary.main">
          {message}
        </Typography>
        <Typography variant="h6" color="text.secondary" mt={2}>
          You got{" "}
          <strong>
            {correctCount} out of {problems.length}
          </strong>{" "}
          correct!
        </Typography>
        <Typography
          variant="h5"
          fontWeight={800}
          mt={1}
          color="success.main"
        >
          +{sessionScore} ⭐ points earned
        </Typography>

        <Box
          mt={5}
          display="flex"
          gap={2}
          justifyContent="center"
          flexWrap="wrap"
        >
          <Button variant="outlined" size="large" onClick={onBack}>
            Choose Another Subject
          </Button>
          <Button
            variant="contained"
            size="large"
            onClick={() => {
              setCurrentIndex(0);
              setSelectedAnswer(null);
              setShowFeedback(false);
              setSessionScore(0);
              setStreak(0);
              setCorrectCount(0);
              setDone(false);
            }}
          >
            Try Again 🔄
          </Button>
        </Box>
      </Box>
    );
  }

  // ── Option button styling ─────────────────────────────────────────────────
  function getOptionSx(option) {
    const base = {
      p: 2.5,
      borderRadius: 3,
      cursor: showFeedback ? "default" : "pointer",
      transition: "all 0.15s",
      display: "flex",
      alignItems: "center",
      gap: 1.5,
      border: "2px solid",
    };

    if (!showFeedback) {
      return {
        ...base,
        bgcolor: "white",
        borderColor: "grey.200",
        "&:hover": {
          borderColor: "primary.main",
          bgcolor: "#FFF4E5",
          transform: "scale(1.02)",
          boxShadow: "0 4px 16px rgba(255,140,0,0.2)",
        },
      };
    }
    if (option === problem.correct_answer) {
      return {
        ...base,
        bgcolor: "#E8F5E9",
        borderColor: "#4CAF50",
        transform: "none",
      };
    }
    if (option === selectedAnswer) {
      return {
        ...base,
        bgcolor: "#FFEBEE",
        borderColor: "#F44336",
        transform: "none",
      };
    }
    return {
      ...base,
      bgcolor: "grey.100",
      borderColor: "grey.200",
      opacity: 0.6,
    };
  }

  // ── Problem screen ─────────────────────────────────────────────────────────
  return (
    <Box>
      {/* Top bar */}
      <Box
        display="flex"
        alignItems="center"
        justifyContent="space-between"
        mb={3}
        flexWrap="wrap"
        gap={1}
      >
        <Button onClick={onBack} size="small" sx={{ fontWeight: 700 }}>
          ← Exit
        </Button>
        <Box display="flex" gap={1} flexWrap="wrap">
          {sessionScore > 0 && (
            <Chip
              label={`⭐ ${sessionScore} pts`}
              color="primary"
              sx={{ fontWeight: 800 }}
            />
          )}
          {streak >= 2 && (
            <Chip
              label={`🔥 ${streak} streak!`}
              color="warning"
              sx={{ fontWeight: 800 }}
            />
          )}
        </Box>
      </Box>

      {/* Progress bar */}
      <Box mb={3}>
        <Box display="flex" justifyContent="space-between" mb={1}>
          <Typography variant="body2" color="text.secondary" fontWeight={700}>
            Question {currentIndex + 1} of {problems.length}
          </Typography>
          <Typography variant="body2" color="text.secondary" fontWeight={700}>
            {subject.type_operation}
          </Typography>
        </Box>
        <LinearProgress
          variant="determinate"
          value={progress}
          sx={{ height: 12, borderRadius: 6, bgcolor: "grey.200" }}
        />
      </Box>

      {/* Question card */}
      <Box
        sx={{
          bgcolor: "white",
          borderRadius: 4,
          p: { xs: 3, sm: 5 },
          mb: 3,
          boxShadow: "0 4px 24px rgba(0,0,0,0.08)",
          textAlign: "center",
          border: "2px solid",
          borderColor: "grey.100",
        }}
      >
        <Typography variant="h4" fontWeight={900}>
          {problem.question}
        </Typography>
        {problem.topic && (
          <Typography
            color="text.secondary"
            mt={1}
            fontSize="0.85rem"
            fontWeight={600}
          >
            📌 {problem.topic}
          </Typography>
        )}
      </Box>

      {/* Answer options */}
      <Box
        display="grid"
        gridTemplateColumns={{ xs: "1fr", sm: "1fr 1fr" }}
        gap={2}
        mb={3}
      >
        {problem.options.map((option) => (
          <Box
            key={option}
            onClick={() => handleSelectAnswer(option)}
            sx={getOptionSx(option)}
          >
            <Typography
              fontWeight={800}
              fontSize="1.2rem"
              flexGrow={1}
              color={
                showFeedback && option === problem.correct_answer
                  ? "#2E7D32"
                  : showFeedback &&
                    option === selectedAnswer &&
                    option !== problem.correct_answer
                  ? "#C62828"
                  : "text.primary"
              }
            >
              {option}
            </Typography>
            {showFeedback && option === problem.correct_answer && (
              <Typography fontSize="1.4rem">✅</Typography>
            )}
            {showFeedback &&
              option === selectedAnswer &&
              option !== problem.correct_answer && (
                <Typography fontSize="1.4rem">❌</Typography>
              )}
          </Box>
        ))}
      </Box>

      {/* Feedback panel */}
      {showFeedback && (
        <Box
          className="pop-in"
          sx={{
            bgcolor: isCorrect ? "#E8F5E9" : "#FFF8E1",
            border: "2px solid",
            borderColor: isCorrect ? "#4CAF50" : "#FF9500",
            borderRadius: 4,
            p: 3,
            mb: 3,
          }}
        >
          <Typography
            variant="h5"
            fontWeight={900}
            color={isCorrect ? "#2E7D32" : "#E65100"}
            gutterBottom
          >
            {isCorrect ? "🎉 Correct! +10 ⭐" : "💡 Almost! Here's how:"}
          </Typography>
          <Typography color="text.secondary" fontWeight={600} lineHeight={1.7}>
            {problem.explanation}
          </Typography>
        </Box>
      )}

      {/* Next button */}
      {showFeedback && (
        <Button
          variant="contained"
          size="large"
          fullWidth
          onClick={handleNext}
          sx={{ py: 1.8, fontSize: "1.1rem" }}
        >
          {currentIndex < problems.length - 1
            ? "Next Problem →"
            : "See My Results! 🏆"}
        </Button>
      )}
    </Box>
  );
}
