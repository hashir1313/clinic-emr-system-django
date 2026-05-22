document.addEventListener('DOMContentLoaded', function() {
    var messages = document.querySelectorAll('[data-auto-dismiss]');
    messages.forEach(function(msg) {
        setTimeout(function() {
            msg.style.transition = 'opacity 0.3s';
            msg.style.opacity = '0';
            setTimeout(function() { msg.remove(); }, 300);
        }, 4000);
    });
});
