const toggleBtn = document.querySelector('.navbar-toggler');
const navBar = document.querySelector('.navbar-collapse');

toggleBtn.addEventListener('click', () => {
    if (toggleBtn.getAttribute('aria-expanded') === 'true') {
        toggleBtn.setAttribute('aria-expanded', 'false');
        navBar.classList.add('collapse')
    } else {
        toggleBtn.setAttribute('aria-expanded', 'true');
        navBar.classList.remove('collapse')
    }
});