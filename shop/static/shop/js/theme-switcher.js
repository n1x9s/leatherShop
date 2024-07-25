document.addEventListener('DOMContentLoaded', (event) => {
    const themeSwitcher = document.getElementById('theme-switcher');
    const htmlElement = document.documentElement;

    // Check the saved theme in localStorage
    let isDarkTheme = localStorage.getItem('isDarkTheme') === 'true';

    // Apply the saved theme
    htmlElement.setAttribute('data-bs-theme', isDarkTheme ? 'dark' : 'light');
    themeSwitcher.textContent = isDarkTheme ? 'Switch to Light Theme' : 'Switch to Dark Theme';

    themeSwitcher.addEventListener('click', () => {
        isDarkTheme = !isDarkTheme;
        htmlElement.setAttribute('data-bs-theme', isDarkTheme ? 'dark' : 'light');
        themeSwitcher.textContent = isDarkTheme ? 'Switch to Light Theme' : 'Switch to Dark Theme';

        // Save the theme choice in localStorage
        localStorage.setItem('isDarkTheme', isDarkTheme);
    });
});
