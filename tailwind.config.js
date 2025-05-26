/** @type {import('tailwindcss').Config} */
module.exports = {
  darkMode: 'class', // <-- Habilitar modo oscuro por clase
  content: [
    "./html_ui/**/*.html", // <-- Ruta a tus HTML
    "./html_ui/js/**/*.js",   // <-- Ruta a tus JS (para detectar clases usadas)
  ],
  theme: {
    extend: {},
  },
  plugins: [],
}