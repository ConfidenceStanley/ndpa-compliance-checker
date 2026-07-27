document.addEventListener('DOMContentLoaded', function () {

    // Auto dismiss flash messages
    setTimeout(function () {
        var msgs = document.querySelectorAll('#flash-msg');
        msgs.forEach(function (msg) {
            msg.style.transition = 'opacity 0.4s ease, transform 0.4s ease';
            msg.style.opacity = '0';
            msg.style.transform = 'translateY(-10px)';
            setTimeout(function () { msg.remove(); }, 400);
        });
    }, 8000);

    // Loading overlay
    var uploadForm = document.getElementById('upload-form');
    if (uploadForm) {
        uploadForm.addEventListener('submit', function () {
            var overlay = document.getElementById('loading-overlay');
            if (overlay) overlay.style.display = 'flex';
        });
    }

    // Navbar scroll
    window.addEventListener('scroll', function () {
        var navbar = document.getElementById('main-navbar');
        if (navbar) {
            if (window.scrollY > 30) {
                navbar.classList.add('scrolled');
            } else {
                navbar.classList.remove('scrolled');
            }
        }
    });

    // Count up animation
    var statValues = document.querySelectorAll('.stat-value');
    statValues.forEach(function (el) {
        var text = el.textContent.trim();
        var num = parseFloat(text);
        if (!isNaN(num) && num > 0 && text.match(/^[\d.]+%?$/)) {
            var suffix = text.includes('%') ? '%' : '';
            var duration = 1200;
            var startTime = null;

            function animate(ts) {
                if (!startTime) startTime = ts;
                var progress = Math.min((ts - startTime) / duration, 1);
                var eased = 1 - Math.pow(1 - progress, 3);
                var current = Math.floor(eased * num);
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

// Password toggle
function togglePassword(inputId, btn) {
    var input = document.getElementById(inputId);
    var icon = btn.querySelector('i');
    if (input.type === 'password') {
        input.type = 'text';
        icon.classList.remove('bi-eye');
        icon.classList.add('bi-eye-slash');
    } else {
        input.type = 'password';
        icon.classList.remove('bi-eye-slash');
        icon.classList.add('bi-eye');
    }
}








// File drag and drop + name display
var dropArea = document.getElementById('drop-area');
var fileInput = document.getElementById('document');
var fileNameDisplay = document.getElementById('file-name-display');

if (dropArea && fileInput) {

    dropArea.addEventListener('click', function (e) {
        if (e.target !== fileInput && !e.target.closest('label')) {
            fileInput.click();
        }
    });

    fileInput.addEventListener('change', function () {
        if (fileInput.files[0]) {
            fileNameDisplay.textContent = fileInput.files[0].name;
        }
    });

    dropArea.addEventListener('dragover', function (e) {
        e.preventDefault();
        dropArea.classList.add('dragover');
    });

    dropArea.addEventListener('dragleave', function () {
        dropArea.classList.remove('dragover');
    });

    dropArea.addEventListener('drop', function (e) {
        e.preventDefault();
        dropArea.classList.remove('dragover');
        var files = e.dataTransfer.files;
        if (files.length > 0) {
            fileInput.files = files;
            fileNameDisplay.textContent = files[0].name;
        }
    });
}