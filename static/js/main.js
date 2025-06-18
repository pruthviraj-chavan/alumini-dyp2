// Main JavaScript for DYP Salokhenagar Alumni Portal

document.addEventListener('DOMContentLoaded', function() {
    // Auto-dismiss alerts after 5 seconds
    setTimeout(function() {
        const alerts = document.querySelectorAll('.alert');
        alerts.forEach(function(alert) {
            const bsAlert = new bootstrap.Alert(alert);
            bsAlert.close();
        });
    }, 5000);

    // Enable tooltips
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });

    // Chat functionality
    const chatContainer = document.getElementById('chatContainer');
    if (chatContainer) {
        // Scroll to bottom of chat on load
        chatContainer.scrollTop = chatContainer.scrollHeight;
        
        // Form submission handling for chat
        const chatForm = document.querySelector('.chat-form');
        if (chatForm) {
            chatForm.addEventListener('submit', function() {
                const messageInput = document.getElementById('id_message_text');
                if (messageInput.value.trim() === '') {
                    event.preventDefault();
                    return false;
                }
            });
        }
    }

    // Filter form in directory
    const filterForm = document.querySelector('.filter-form');
    if (filterForm) {
        const clearButton = document.querySelector('.clear-filters');
        if (clearButton) {
            clearButton.addEventListener('click', function(e) {
                e.preventDefault();
                const inputs = filterForm.querySelectorAll('input, select');
                inputs.forEach(function(input) {
                    input.value = '';
                });
                filterForm.submit();
            });
        }
    }
});
