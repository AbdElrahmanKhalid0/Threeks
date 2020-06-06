window.addEventListener('DOMContentLoaded', () => {
    const messages = document.querySelectorAll('.alert');
    for( let i = 0; i < messages.length; i++){
        setTimeout(() => {
            messages[i].style.animation = "fade-out 1s forwards";
            setTimeout(() => {
                messages[i].remove()
            }, 1000)
        }, 5000)
    }
})