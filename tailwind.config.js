/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./app/templates/**/*.html",
    "./app/static/js/**/*.js",
  ],
  theme: {
    extend: {
      colors: {
        // 제주 테마 컬러
        jeju: {
          orange: '#F97316',
          blue: '#0EA5E9',
          green: '#22C55E',
        }
      }
    },
  },
  plugins: [],
}
