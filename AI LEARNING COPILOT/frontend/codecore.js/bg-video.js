/**
 * Background Video Auto-play Handler
 * Ensures video plays on page load and navbar navigation
 */
(function() {
    const video = document.getElementById('bgVideo');
    
    if (!video) {
        console.warn('Background video element not found');
        return;
    }
    
    // Play video function
    function playVideo() {
        video.play().catch(err => {
            console.log('Video autoplay prevented (user interaction may be required):', err.message);
        });
    }
    
    // Attach click handlers to all navbar links and buttons
    function attachNavbarHandlers() {
        const navbarLinks = document.querySelectorAll('.navbar a, .mobile-menu-toggle, button, a');
        
        navbarLinks.forEach(link => {
            link.addEventListener('click', function() {
                playVideo();
            }, { passive: true });
        });
    }
    
    // Initialize on page load
    function init() {
        // Try to play immediately
        playVideo();
        
        // Attach navbar handlers
        attachNavbarHandlers();
        
        // Fallback: play on first user interaction
        const playOnInteraction = function() {
            playVideo();
            document.body.removeEventListener('click', playOnInteraction);
            document.body.removeEventListener('touchstart', playOnInteraction);
        };
        
        document.body.addEventListener('click', playOnInteraction, { once: true, passive: true });
        document.body.addEventListener('touchstart', playOnInteraction, { once: true, passive: true });
    }
    
    // Wait for DOM to be ready
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', init);
    } else {
        init();
    }
})();
