import React, { useEffect, useState } from "react";
import { Switch, Route } from "react-router-dom";
import Signup from "./Signup";
import Home from "./Home";
import {
  AppBar,
  Toolbar,
  Typography,
  Button,
  Container,
  Box,
  CircularProgress,
  Chip,
} from "@mui/material";
import { ThemeProvider } from "@mui/material/styles";
import CssBaseline from "@mui/material/CssBaseline";
import theme from "../theme";

function App() {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);
  const [score, setScore] = useState(0);
  const [streak, setStreak] = useState(0);

  useEffect(() => {
    fetch("/authorized").then((resp) => {
      if (resp.ok) {
        resp.json().then((user) => {
          setUser(user);
          setLoading(false);
        });
      } else {
        setLoading(false);
      }
    });
  }, []);

  function handleLogOut() {
    fetch("/logout", { method: "DELETE" }).then((resp) => {
      if (resp.ok) {
        setUser(null);
        setScore(0);
        setStreak(0);
      }
    });
  }

  function handleAnswer(isCorrect) {
    if (isCorrect) {
      setScore((s) => s + 10);
      setStreak((s) => s + 1);
    } else {
      setStreak(0);
    }
  }

  if (loading) {
    return (
      <ThemeProvider theme={theme}>
        <CssBaseline />
        <Box
          display="flex"
          flexDirection="column"
          justifyContent="center"
          alignItems="center"
          minHeight="100vh"
          gap={2}
        >
          <Typography fontSize="4rem">🎓</Typography>
          <CircularProgress color="primary" size={48} />
          <Typography variant="h6" color="text.secondary">
            Loading SmartScholars…
          </Typography>
        </Box>
      </ThemeProvider>
    );
  }

  if (!user) {
    return (
      <ThemeProvider theme={theme}>
        <CssBaseline />
        <Signup setUser={setUser} />
      </ThemeProvider>
    );
  }

  return (
    <ThemeProvider theme={theme}>
      <CssBaseline />
      <AppBar
        position="static"
        sx={{
          background: "linear-gradient(135deg, #FF8C00 0%, #FFB347 100%)",
          boxShadow: "0 4px 20px rgba(255,140,0,0.35)",
        }}
      >
        <Toolbar sx={{ gap: 1 }}>
          <Typography
            variant="h5"
            fontWeight={900}
            sx={{ flexGrow: 1, letterSpacing: "-0.5px" }}
          >
            🎓 SmartScholars
          </Typography>

          {score > 0 && (
            <Chip
              label={`⭐ ${score} pts`}
              sx={{
                bgcolor: "rgba(255,255,255,0.25)",
                color: "white",
                fontWeight: 800,
                fontSize: "0.9rem",
              }}
            />
          )}
          {streak >= 2 && (
            <Chip
              label={`🔥 ${streak} streak`}
              sx={{
                bgcolor: "rgba(255,255,255,0.25)",
                color: "white",
                fontWeight: 800,
                fontSize: "0.9rem",
              }}
            />
          )}

          <Typography
            variant="body2"
            sx={{ color: "rgba(255,255,255,0.85)", ml: 1 }}
          >
            Hi, {user.username}! 👋
          </Typography>

          <Button
            color="inherit"
            onClick={handleLogOut}
            aria-label="Sign out"
            sx={{
              bgcolor: "rgba(255,255,255,0.15)",
              "&:hover": { bgcolor: "rgba(255,255,255,0.3)" },
              ml: 1,
            }}
          >
            Sign Out
          </Button>
        </Toolbar>
      </AppBar>

      <Container maxWidth="lg" sx={{ mt: 4, mb: 6 }}>
        <Home onAnswer={handleAnswer} />
      </Container>
    </ThemeProvider>
  );
}

export default App;
