// Auto dismiss flash messages after 5 seconds
window.addEventListener('DOMContentLoaded', function () {
    setTimeout(function () {
        var flashMsg = document.getElementById('flash-msg');
        if (flashMsg) {
            flashMsg.style.transition = 'opacity 0.5s';
            flashMsg.style.opacity = '0';
            setTimeout(function () { flashMsg.remove(); }, 500);
        }
    }, 5000);
});

// Show loading overlay on form submit
var uploadForm = document.getElementById('upload-form');
if (uploadForm) {
    uploadForm.addEventListener('submit', function () {
        var overlay = document.getElementById('loading-overlay');
        if (overlay) {
            overlay.style.display = 'flex';
        }
    });
}