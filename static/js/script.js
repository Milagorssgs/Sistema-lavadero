// Archivo JS principal para interacciones adicionales
document.addEventListener('DOMContentLoaded', function() {
    // 1. Cerrar alertas automáticamente con animación
    const alerts = document.querySelectorAll('.alert');
    if (alerts.length > 0) {
        setTimeout(() => {
            alerts.forEach(alert => {
                alert.style.transition = 'opacity 0.4s ease, transform 0.4s ease';
                alert.style.opacity = '0';
                alert.style.transform = 'translateY(-10px)';
                setTimeout(() => alert.remove(), 400);
            });
        }, 4000);
    }
    
    // 2. Toggle Menu Móvil
    const mobileToggle = document.getElementById('mobile-toggle');
    const sidebar = document.getElementById('sidebar');
    if(mobileToggle && sidebar) {
        mobileToggle.addEventListener('click', () => {
            sidebar.classList.toggle('open');
        });
    }

    // 3. Manejo de Modo Oscuro (Dark Theme)
    const themeToggleBtn = document.getElementById('theme-toggle');
    const body = document.documentElement; // Guardaremos el data-theme en html o body. Lo haremos en body o documentElement
    const iconTheme = document.getElementById('theme-icon');

    // Cargar preferencia
    const savedTheme = localStorage.getItem('lavadero_theme');
    if (savedTheme === 'dark') {
        document.body.setAttribute('data-theme', 'dark');
        if(iconTheme) { iconTheme.classList.replace('fa-moon', 'fa-sun'); }
    }

    if (themeToggleBtn) {
        themeToggleBtn.addEventListener('click', () => {
            const currentTheme = document.body.getAttribute('data-theme');
            if (currentTheme === 'dark') {
                document.body.removeAttribute('data-theme');
                localStorage.setItem('lavadero_theme', 'light');
                if(iconTheme) iconTheme.classList.replace('fa-sun', 'fa-moon');
            } else {
                document.body.setAttribute('data-theme', 'dark');
                localStorage.setItem('lavadero_theme', 'dark');
                if(iconTheme) iconTheme.classList.replace('fa-moon', 'fa-sun');
            }
            
            // Disparar evento para que Chart.js se actualice si existe
            window.dispatchEvent(new Event('themeChanged'));
        });
    }

    // 4. Prevenir doble envío de formularios y mostrar "Guardando..."
    const forms = document.querySelectorAll('form');
    forms.forEach(form => {
        form.addEventListener('submit', function(e) {
            // Evitar si es un formulario de búsqueda (método GET)
            if (this.method.toUpperCase() === 'GET') return;

            const submitBtn = this.querySelector('button[type="submit"]');
            if (submitBtn) {
                // Prevenir doble click
                if (submitBtn.disabled) {
                    e.preventDefault();
                    return;
                }
                submitBtn.disabled = true;
                const originalText = submitBtn.innerHTML;
                submitBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Guardando...';
                
                // Habilitar nuevamente si por alguna razón falla silenciosamente después de 10s (por ej. descarga de archivo)
                setTimeout(() => {
                    submitBtn.disabled = false;
                    submitBtn.innerHTML = originalText;
                }, 10000);
            }
        });
    });
});
