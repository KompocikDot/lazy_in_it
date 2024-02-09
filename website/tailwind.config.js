 /** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["./**/*.{html,js,j2}"],
  theme: {
    extend: {
      colors: {
        'dark-gray': '#202020',
        'light-green': '#9BE49B',
        'dark-green': '#2BE82A',
      }
    },
  },
  plugins: [
      require('@tailwindcss/forms'),
  ],
}
