/** @type {import('tailwindcss').Config} */
import { heroui } from "@heroui/react";
import typography from "@tailwindcss/typography";
export default {
  darkMode: false,
  theme: {
    extend: {
      colors: {
        background: "#ffffff",
        foreground: "#000000",
        primary: "#007bff",
        secondary: "#6c757d",
      }
    }
  },
  plugins: [typography],
};
