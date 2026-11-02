document.addEventListener('DOMContentLoaded', function () {

    const toggles = document.querySelectorAll('.nk-toggle-password');

    toggles.forEach(function (toggle) {

        toggle.addEventListener('click', function () {

            const targetId = toggle.getAttribute('data-target');
            const input = document.getElementById(targetId);

            if (!input) {
                return;
            }

            const icon = toggle.querySelector('i');

            if (input.type === 'password') {

                input.type = 'text';

                if (icon) {
                    icon.classList.remove('fa-eye');
                    icon.classList.add('fa-eye-slash');
                }

            } else {

                input.type = 'password';

                if (icon) {
                    icon.classList.remove('fa-eye-slash');
                    icon.classList.add('fa-eye');
                }

            }

        });

    });

});