import { Box, Typography } from "@mui/material";

const SUBJECT_CONFIG = {
  Addition: {
    emoji: "➕",
    color: "#4285F4",
    bg: "#EEF4FF",
    border: "#4285F433",
    hoverShadow: "#4285F455",
  },
  Subtraction: {
    emoji: "➖",
    color: "#9C27B0",
    bg: "#F5EEF9",
    border: "#9C27B033",
    hoverShadow: "#9C27B055",
  },
  Multiplication: {
    emoji: "✖️",
    color: "#FF9500",
    bg: "#FFF4E5",
    border: "#FF950033",
    hoverShadow: "#FF950055",
  },
  Division: {
    emoji: "➗",
    color: "#4CAF50",
    bg: "#EEF8EE",
    border: "#4CAF5033",
    hoverShadow: "#4CAF5055",
  },
};

const DEFAULT_CONFIG = {
  emoji: "📐",
  color: "#607D8B",
  bg: "#ECEFF1",
  border: "#607D8B33",
  hoverShadow: "#607D8B55",
};

export default function Subjectcard({ subject, onSelect }) {
  const { type_operation } = subject;
  const config = SUBJECT_CONFIG[type_operation] || DEFAULT_CONFIG;

  return (
    <Box
      role="button"
      tabIndex={0}
      onClick={() => onSelect(subject)}
      onKeyDown={(e) => e.key === "Enter" && onSelect(subject)}
      aria-label={`Practice ${type_operation}`}
      sx={{
        bgcolor: config.bg,
        border: `2px solid ${config.border}`,
        borderRadius: 4,
        p: 4,
        cursor: "pointer",
        textAlign: "center",
        transition: "all 0.2s cubic-bezier(0.34, 1.56, 0.64, 1)",
        userSelect: "none",
        "&:hover, &:focus-visible": {
          transform: "translateY(-8px) scale(1.02)",
          boxShadow: `0 16px 40px ${config.hoverShadow}`,
          border: `2px solid ${config.color}`,
          outline: "none",
        },
      }}
    >
      <Typography fontSize="4rem" lineHeight={1}>
        {config.emoji}
      </Typography>
      <Typography
        variant="h5"
        fontWeight={900}
        mt={1.5}
        color={config.color}
      >
        {type_operation}
      </Typography>
      <Typography color="text.secondary" mt={1} fontSize="0.9rem" fontWeight={600}>
        Tap to practice! →
      </Typography>
    </Box>
  );
}
