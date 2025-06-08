/**
 * FLL Team Name Generator
 * Main JavaScript file for common functionality
 */

document.addEventListener('DOMContentLoaded', function() {
    // Add any global functionality here
    console.log('FLL Team Name Generator loaded');
    
    // Helper function to show notifications
    window.showNotification = function(message, type = 'info') {
        // Create notification element if it doesn't exist
        let notification = document.getElementById('notification');
        
        if (!notification) {
            notification = document.createElement('div');
            notification.id = 'notification';
            document.body.appendChild(notification);
        }
        
        // Set message and type
        notification.textContent = message;
        notification.className = 'notification ' + type;
        
        // Show notification
        notification.classList.add('show');
        
        // Hide after 3 seconds
        setTimeout(function() {
            notification.classList.remove('show');
        }, 3000);
    };
    
    // Add notification styles if not already in CSS
    if (!document.querySelector('style#notification-styles')) {
        const style = document.createElement('style');
        style.id = 'notification-styles';
        style.textContent = `
            .notification {
                position: fixed;
                top: 20px;
                right: 20px;
                padding: 12px 20px;
                border-radius: 8px;
                color: white;
                font-weight: 600;
                z-index: 1000;
                opacity: 0;
                transform: translateY(-20px);
                transition: opacity 0.3s, transform 0.3s;
                max-width: 300px;
            }
            
            .notification.show {
                opacity: 1;
                transform: translateY(0);
            }
            
            .notification.info {
                background-color: #0055BF;
            }
            
            .notification.success {
                background-color: #00852B;
            }
            
            .notification.error {
                background-color: #D01012;
            }
        `;
        document.head.appendChild(style);
    }
    
    // Add sanitization helper to prevent XSS
    window.sanitizeInput = function(input) {
        const temp = document.createElement('div');
        temp.textContent = input;
        return temp.innerHTML;
    };
});
