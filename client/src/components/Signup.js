import {
  Button,
  TextField,
  MenuItem,
  InputLabel,
  Select,
  Box,
  FormControl,
  Typography,
  Paper,
  Stack,
  CircularProgress,
  Alert,
  Collapse,
} from "@mui/material";
import { useFormik } from "formik";
import { useState } from "react";
import * as yup from "yup";
import { ThemeProvider } from "@mui/material/styles";
import CssBaseline from "@mui/material/CssBaseline";
import theme from "../theme";

const GRADE_OPTIONS = [
  { value: 1, label: "Grade 1 — Beginner ⭐" },
  { value: 2, label: "Grade 2 — Explorer ⭐⭐" },
  { value: 3, label: "Grade 3 — Champion ⭐⭐⭐" },
];

function SignupForm({ setUser }) {
  const [isLogin, setIsLogin] = useState(false);
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [serverError, setServerError] = useState(null);

  const signupSchema = yup.object().shape({
    username: yup
      .string()
      .min(5, "Username must be at least 5 characters")
      .max(15, "Username must be 15 characters or fewer")
      .required("Username is required"),
    email: yup.string().email("That doesn't look like a valid email"),
    password: yup
      .string()
      .min(5, "Password must be at least 5 characters")
      .max(15, "Password must be 15 characters or fewer")
      .required("Password is required"),
    grade_level: yup
      .number()
      .min(1, "Please pick a grade")
      .max(3, "Please pick a grade"),
  });

  const loginSchema = yup.object().shape({
    username: yup.string().required("Username is required"),
    password: yup.string().required("Password is required"),
  });

  const formik = useFormik({
    initialValues: { username: "", email: "", password: "", grade_level: "" },
    validationSchema: isLogin ? loginSchema : signupSchema,
    onSubmit: (values) => {
      setIsSubmitting(true);
      setServerError(null);
      const endpoint = isLogin ? "/login" : "/register";
      fetch(endpoint, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(values),
      })
        .then((resp) => {
          if (resp.ok) {
            resp.json().then(({ user }) => setUser(user));
          } else {
            resp
              .json()
              .then((data) =>
                setServerError(
                  data.error || data.message || "Something went wrong. Please try again!"
                )
              )
              .catch(() =>
                setServerError("Something went wrong. Please try again!")
              );
          }
        })
        .finally(() => setIsSubmitting(false));
    },
  });

  function toggle() {
    setIsLogin((v) => !v);
    setServerError(null);
    formik.resetForm();
  }

  return (
    <Box
      display="flex"
      flexDirection="column"
      justifyContent="center"
      alignItems="center"
      minHeight="100vh"
      sx={{ background: "linear-gradient(160deg, #FFF8F0 0%, #FFE8CC 100%)" }}
    >
      <Paper
        elevation={4}
        sx={{
          maxWidth: 440,
          width: "100%",
          p: { xs: 3, sm: 5 },
          m: 2,
          borderRadius: 5,
          boxShadow: "0 8px 40px rgba(255,140,0,0.18)",
        }}
      >
        {/* Logo */}
        <Box textAlign="center" mb={3}>
          <Typography fontSize="3.5rem" lineHeight={1}>
            🎓
          </Typography>
          <Typography variant="h4" fontWeight={900} mt={1} color="primary.main">
            SmartScholars
          </Typography>
          <Typography color="text.secondary" mt={0.5} fontWeight={600}>
            {isLogin
              ? "Welcome back, scholar! 👋"
              : "Join thousands of young learners! 🚀"}
          </Typography>
        </Box>

        {serverError && (
          <Alert severity="error" aria-live="polite" sx={{ mb: 2 }}>
            {serverError}
          </Alert>
        )}

        <form onSubmit={formik.handleSubmit}>
          <Stack spacing={2}>
            <TextField
              name="username"
              id="username"
              label="Username"
              variant="outlined"
              fullWidth
              required
              value={formik.values.username}
              onChange={formik.handleChange}
              onBlur={formik.handleBlur}
              error={formik.touched.username && Boolean(formik.errors.username)}
              helperText={formik.touched.username && formik.errors.username}
            />

            <Collapse in={!isLogin} unmountOnExit>
              <Stack spacing={2}>
                <TextField
                  name="email"
                  id="email"
                  label="Email (optional)"
                  variant="outlined"
                  fullWidth
                  value={formik.values.email}
                  onChange={formik.handleChange}
                  onBlur={formik.handleBlur}
                  error={formik.touched.email && Boolean(formik.errors.email)}
                  helperText={formik.touched.email && formik.errors.email}
                />

                <FormControl fullWidth>
                  <InputLabel id="grade-level-label">
                    What grade are you in?
                  </InputLabel>
                  <Select
                    name="grade_level"
                    id="grade_level"
                    labelId="grade-level-label"
                    value={formik.values.grade_level}
                    label="What grade are you in?"
                    onChange={formik.handleChange}
                    onBlur={formik.handleBlur}
                  >
                    {GRADE_OPTIONS.map((g) => (
                      <MenuItem key={g.value} value={g.value}>
                        {g.label}
                      </MenuItem>
                    ))}
                  </Select>
                </FormControl>
              </Stack>
            </Collapse>

            <TextField
              name="password"
              id="password"
              label="Password"
              type="password"
              variant="outlined"
              fullWidth
              required
              value={formik.values.password}
              onChange={formik.handleChange}
              onBlur={formik.handleBlur}
              error={formik.touched.password && Boolean(formik.errors.password)}
              helperText={formik.touched.password && formik.errors.password}
            />

            <Button
              variant="contained"
              type="submit"
              fullWidth
              size="large"
              disabled={isSubmitting}
              startIcon={
                isSubmitting ? (
                  <CircularProgress size={18} color="inherit" />
                ) : null
              }
              sx={{ mt: 1 }}
            >
              {isSubmitting
                ? "Loading…"
                : isLogin
                ? "Let's Go! 🚀"
                : "Create My Account! 🎉"}
            </Button>

            <Button
              onClick={toggle}
              fullWidth
              aria-label={isLogin ? "Switch to sign up" : "Switch to login"}
              sx={{ color: "text.secondary", fontWeight: 700 }}
            >
              {isLogin
                ? "New here? Create an account →"
                : "Already have an account? Log in →"}
            </Button>
          </Stack>
        </form>
      </Paper>
    </Box>
  );
}

export default function Signup({ setUser }) {
  return (
    <ThemeProvider theme={theme}>
      <CssBaseline />
      <SignupForm setUser={setUser} />
    </ThemeProvider>
  );
}
