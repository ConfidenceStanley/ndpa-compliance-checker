document.addEventListener('DOMContentLoaded', function () {

    // Auto dismiss flash messages
    setTimeout(function () {
        var flashMsgs = document.querySelectorAll('#flash-msg');
        flashMsgs.forEach(function (msg) {
            msg.style.transition = 'opacity 0.5s ease, transform 0.5s ease';
            msg.style.opacity = '0';
            msg.style.transform = 'translateY(-10px)';
            setTimeout(function () { msg.remove(); }, 500);
        });
    }, 5000);

    // Loading overlay on form submit
    var uploadForm = document.getElementById('upload-form');
    if (uploadForm) {
        uploadForm.addEventListener('submit', function () {
            var overlay = document.getElementById('loading-overlay');
            if (overlay) {
                overlay.style.display = 'flex';
            }
        });
    }

    // Navbar scroll effect
    window.addEventListener('scroll', function () {
        var navbar = document.getElementById('main-navbar');
        if (window.scrollY > 50) {
            navbar.classList.add('scrolled');
        } else {
            navbar.classList.remove('scrolled');
        }
    });

    // Animate stat values counting up
    var statValues = document.querySelectorAll('.stat-value');
    statValues.forEach(function (el) {
        var text = el.textContent.trim();
        var num = parseFloat(text);
        if (!isNaN(num) && num > 0) {
            var suffix = text.replace(num.toString(), '');
            var duration = 1500;
            var startTime = null;
            var startVal = 0;

            function animate(currentTime) {
                if (!startTime) startTime = currentTime;
                var progress = Math.min((currentTime - startTime) / duration, 1);
                var current = Math.floor(progress * num);
                el.textContent = current + suffix;
                if (progress < 1) {
                    requestAnimationFrame(animate);
                } else {
                    el.textContent = text;
                }
            }
            requestAnimationFrame(animate);
        }
    });
});