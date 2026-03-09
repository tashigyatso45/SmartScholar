import { createTheme } from "@mui/material/styles";

const theme = createTheme({
  palette: {
    primary: {
      main: "#FF8C00",
      light: "#FFB347",
      dark: "#E67E00",
      contrastText: "#FFFFFF",
    },
    secondary: {
      main: "#4285F4",
      contrastText: "#FFFFFF",
    },
    success: {
      main: "#4CAF50",
      light: "#E8F5E9",
    },
    error: {
      main: "#F44336",
      light: "#FFEBEE",
    },
    warning: {
      main: "#FF9500",
      light: "#FFF3E0",
    },
    background: {
      default: "#FFF8F0",
      paper: "#FFFFFF",
    },
    text: {
      primary: "#2D3436",
      secondary: "#636E72",
    },
  },
  typography: {
    fontFamily: '"Nunito", "Helvetica Neue", "Arial", sans-serif',
    h3: { fontWeight: 900 },
    h4: { fontWeight: 800 },
    h5: { fontWeight: 700 },
    h6: { fontWeight: 700 },
    button: { fontWeight: 700, textTransform: "none" },
  },
  shape: {
    borderRadius: 16,
  },
  components: {
    MuiButton: {
      styleOverrides: {
        root: {
          borderRadius: 50,
          padding: "10px 28px",
          fontSize: "1rem",
          boxShadow: "none",
          "&:hover": { boxShadow: "0 4px 16px rgba(0,0,0,0.15)" },
        },
        sizeLarge: { padding: "14px 36px", fontSize: "1.1rem" },
      },
    },
    MuiCard: {
      styleOverrides: {
        root: {
          borderRadius: 20,
          boxShadow: "0 4px 20px rgba(0,0,0,0.08)",
        },
      },
    },
    MuiPaper: {
      styleOverrides: {
        root: { borderRadius: 20 },
      },
    },
    MuiTextField: {
      styleOverrides: {
        root: {
          "& .MuiOutlinedInput-root": { borderRadius: 12 },
        },
      },
    },
    MuiSelect: {
      styleOverrides: {
        outlined: { borderRadius: 12 },
      },
    },
    MuiChip: {
      styleOverrides: {
        root: { fontWeight: 700, borderRadius: 50 },
      },
    },
    MuiLinearProgress: {
      styleOverrides: {
        root: { borderRadius: 8 },
        bar: { borderRadius: 8 },
      },
    },
    MuiAlert: {
      styleOverrides: {
        root: { borderRadius: 12 },
      },
    },
  },
});

export default theme;
