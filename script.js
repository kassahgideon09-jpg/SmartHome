// DOM Content Loaded
document.addEventListener('DOMContentLoaded', function() {
    initializeNavigation();
    initializeAffiliateLinks();
    initializeNewsletterForm();
    initializeScrollEffects();
    initializeLazyLoading();
});

// Navigation functionality
function initializeNavigation() {
    const mobileMenu = document.getElementById('mobile-menu');
    const navMenu = document.querySelector('.nav-menu');
    const navLinks = document.querySelectorAll('.nav-link');

    // Mobile menu toggle
    if (mobileMenu) {
        mobileMenu.addEventListener('click', function() {
            mobileMenu.classList.toggle('active');
            navMenu.classList.toggle('active');
        });
    }

    // Close mobile menu when clicking on a link
    navLinks.forEach(link => {
        link.addEventListener('click', function() {
            if (navMenu.classList.contains('active')) {
                mobileMenu.classList.remove('active');
                navMenu.classList.remove('active');
            }
        });
    });

    // Close mobile menu when clicking outside
    document.addEventListener('click', function(event) {
        const isClickInsideNav = navMenu.contains(event.target) || mobileMenu.contains(event.target);
        
        if (!isClickInsideNav && navMenu.classList.contains('active')) {
            mobileMenu.classList.remove('active');
            navMenu.classList.remove('active');
        }
    });

    // Header scroll effect
    let lastScrollTop = 0;
    const header = document.querySelector('.header');
    
    window.addEventListener('scroll', function() {
        const scrollTop = window.pageYOffset || document.documentElement.scrollTop;
        
        if (scrollTop > lastScrollTop && scrollTop > 100) {
            // Scrolling down
            header.style.transform = 'translateY(-100%)';
        } else {
            // Scrolling up
            header.style.transform = 'translateY(0)';
        }
        
        lastScrollTop = scrollTop;
    });
}

// Affiliate link tracking and management
function initializeAffiliateLinks() {
    const affiliateLinks = document.querySelectorAll('.btn-affiliate');
    
    // Affiliate link URLs (replace with your actual affiliate links)
    const affiliateUrls = {
        'echo-dot': 'https://amzn.to/3example1',
        'nest-thermostat': 'https://amzn.to/3example2',
        'airpods-pro': 'https://amzn.to/3example3'
    };

    affiliateLinks.forEach(link => {
        const productId = link.getAttribute('data-product');
        
        if (productId && affiliateUrls[productId]) {
            link.href = affiliateUrls[productId];
            link.target = '_blank';
            link.rel = 'noopener noreferrer sponsored';
        }

        // Track affiliate link clicks
        link.addEventListener('click', function(e) {
            const productName = this.closest('.review-card').querySelector('h3').textContent;
            
            // Analytics tracking (replace with your analytics code)
            if (typeof gtag !== 'undefined') {
                gtag('event', 'affiliate_click', {
                    'product_name': productName,
                    'product_id': productId,
                    'link_url': this.href
                });
            }

            // Optional: Show confirmation modal
            if (confirm(`You're about to visit our affiliate partner to view "${productName}". We may earn a commission from qualifying purchases at no extra cost to you. Continue?`)) {
                return true;
            } else {
                e.preventDefault();
                return false;
            }
        });
    });
}

// Newsletter form handling
function initializeNewsletterForm() {
    const newsletterForm = document.getElementById('newsletter-form');
    
    if (newsletterForm) {
        newsletterForm.addEventListener('submit', function(e) {
            e.preventDefault();
            
            const emailInput = this.querySelector('input[type="email"]');
            const submitButton = this.querySelector('button[type="submit"]');
            const email = emailInput.value.trim();
            
            if (!isValidEmail(email)) {
                showNotification('Please enter a valid email address.', 'error');
                return;
            }

            // Show loading state
            const originalText = submitButton.textContent;
            submitButton.innerHTML = '<span class="loading"></span> Subscribing...';
            submitButton.disabled = true;

            // Simulate API call (replace with your actual newsletter service)
            setTimeout(() => {
                // Reset form
                emailInput.value = '';
                submitButton.textContent = originalText;
                submitButton.disabled = false;
                
                showNotification('Thank you for subscribing! Check your email for confirmation.', 'success');
                
                // Analytics tracking
                if (typeof gtag !== 'undefined') {
                    gtag('event', 'newsletter_signup', {
                        'email': email
                    });
                }
            }, 2000);
        });
    }
}

// Email validation
function isValidEmail(email) {
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return emailRegex.test(email);
}

// Notification system
function showNotification(message, type = 'info') {
    // Remove existing notifications
    const existingNotifications = document.querySelectorAll('.notification');
    existingNotifications.forEach(notification => notification.remove());

    // Create notification element
    const notification = document.createElement('div');
    notification.className = `notification notification-${type}`;
    notification.innerHTML = `
        <div class="notification-content">
            <span class="notification-message">${message}</span>
            <button class="notification-close">&times;</button>
        </div>
    `;

    // Add styles
    notification.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        background: ${type === 'success' ? '#4CAF50' : type === 'error' ? '#f44336' : '#2196F3'};
        color: white;
        padding: 1rem 1.5rem;
        border-radius: 8px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.15);
        z-index: 10000;
        max-width: 400px;
        animation: slideInRight 0.3s ease;
    `;

    // Add to page
    document.body.appendChild(notification);

    // Close button functionality
    const closeButton = notification.querySelector('.notification-close');
    closeButton.addEventListener('click', () => {
        notification.style.animation = 'slideOutRight 0.3s ease';
        setTimeout(() => notification.remove(), 300);
    });

    // Auto remove after 5 seconds
    setTimeout(() => {
        if (notification.parentNode) {
            notification.style.animation = 'slideOutRight 0.3s ease';
            setTimeout(() => notification.remove(), 300);
        }
    }, 5000);
}

// Scroll effects and animations
function initializeScrollEffects() {
    // Smooth scroll for anchor links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function(e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });

    // Intersection Observer for fade-in animations
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };

    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('fade-in');
                observer.unobserve(entry.target);
            }
        });
    }, observerOptions);

    // Observe elements for animation
    const animateElements = document.querySelectorAll('.review-card, .category-card, .blog-card');
    animateElements.forEach(el => {
        observer.observe(el);
    });
}

// Lazy loading for images
function initializeLazyLoading() {
    if ('IntersectionObserver' in window) {
        const imageObserver = new IntersectionObserver((entries, observer) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    const img = entry.target;
                    img.src = img.dataset.src || img.src;
                    img.classList.remove('lazy');
                    imageObserver.unobserve(img);
                }
            });
        });

        const lazyImages = document.querySelectorAll('img[loading="lazy"]');
        lazyImages.forEach(img => {
            imageObserver.observe(img);
        });
    }
}

// Search functionality (for future implementation)
function initializeSearch() {
    const searchInput = document.getElementById('search-input');
    const searchResults = document.getElementById('search-results');
    
    if (searchInput) {
        let searchTimeout;
        
        searchInput.addEventListener('input', function() {
            clearTimeout(searchTimeout);
            const query = this.value.trim();
            
            if (query.length < 2) {
                searchResults.innerHTML = '';
                searchResults.style.display = 'none';
                return;
            }
            
            searchTimeout = setTimeout(() => {
                performSearch(query);
            }, 300);
        });
    }
}

// Search function (placeholder for future implementation)
function performSearch(query) {
    // This would typically make an API call to search your content
    console.log('Searching for:', query);
    
    // Placeholder search results
    const mockResults = [
        { title: 'Amazon Echo Dot Review', url: 'review-echo-dot.html', type: 'review' },
        { title: 'Smart Home Setup Guide', url: 'blog-smart-home-setup.html', type: 'blog' }
    ];
    
    displaySearchResults(mockResults);
}

function displaySearchResults(results) {
    const searchResults = document.getElementById('search-results');
    
    if (!searchResults) return;
    
    if (results.length === 0) {
        searchResults.innerHTML = '<p>No results found.</p>';
    } else {
        const resultsHTML = results.map(result => `
            <div class="search-result">
                <h4><a href="${result.url}">${result.title}</a></h4>
                <span class="result-type">${result.type}</span>
            </div>
        `).join('');
        
        searchResults.innerHTML = resultsHTML;
    }
    
    searchResults.style.display = 'block';
}

// Rating system (for future implementation)
function initializeRatingSystem() {
    const ratingElements = document.querySelectorAll('.rating-interactive');
    
    ratingElements.forEach(rating => {
        const stars = rating.querySelectorAll('.star');
        
        stars.forEach((star, index) => {
            star.addEventListener('click', function() {
                const ratingValue = index + 1;
                updateRating(rating, ratingValue);
                
                // Send rating to server (implement as needed)
                submitRating(rating.dataset.productId, ratingValue);
            });
            
            star.addEventListener('mouseenter', function() {
                highlightStars(stars, index);
            });
        });
        
        rating.addEventListener('mouseleave', function() {
            resetStarHighlight(stars, rating.dataset.currentRating || 0);
        });
    });
}

function highlightStars(stars, upToIndex) {
    stars.forEach((star, index) => {
        if (index <= upToIndex) {
            star.classList.add('highlighted');
        } else {
            star.classList.remove('highlighted');
        }
    });
}

function resetStarHighlight(stars, currentRating) {
    stars.forEach((star, index) => {
        star.classList.remove('highlighted');
        if (index < currentRating) {
            star.classList.add('active');
        } else {
            star.classList.remove('active');
        }
    });
}

function updateRating(ratingElement, value) {
    ratingElement.dataset.currentRating = value;
    const stars = ratingElement.querySelectorAll('.star');
    resetStarHighlight(stars, value);
}

function submitRating(productId, rating) {
    // Implement rating submission to your backend
    console.log(`Rating submitted: Product ${productId}, Rating: ${rating}`);
    
    // Analytics tracking
    if (typeof gtag !== 'undefined') {
        gtag('event', 'product_rating', {
            'product_id': productId,
            'rating': rating
        });
    }
}

// Utility functions
function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

function throttle(func, limit) {
    let inThrottle;
    return function() {
        const args = arguments;
        const context = this;
        if (!inThrottle) {
            func.apply(context, args);
            inThrottle = true;
            setTimeout(() => inThrottle = false, limit);
        }
    };
}

// Performance monitoring
function trackPagePerformance() {
    window.addEventListener('load', function() {
        setTimeout(() => {
            const perfData = performance.getEntriesByType('navigation')[0];
            const loadTime = perfData.loadEventEnd - perfData.loadEventStart;
            
            // Track page load time
            if (typeof gtag !== 'undefined') {
                gtag('event', 'page_load_time', {
                    'load_time': loadTime,
                    'page_url': window.location.href
                });
            }
        }, 0);
    });
}

// Initialize performance tracking
trackPagePerformance();

// Add CSS animations
const style = document.createElement('style');
style.textContent = `
    @keyframes slideInRight {
        from {
            transform: translateX(100%);
            opacity: 0;
        }
        to {
            transform: translateX(0);
            opacity: 1;
        }
    }
    
    @keyframes slideOutRight {
        from {
            transform: translateX(0);
            opacity: 1;
        }
        to {
            transform: translateX(100%);
            opacity: 0;
        }
    }
    
    .notification-content {
        display: flex;
        justify-content: space-between;
        align-items: center;
        gap: 1rem;
    }
    
    .notification-close {
        background: none;
        border: none;
        color: white;
        font-size: 1.5rem;
        cursor: pointer;
        padding: 0;
        line-height: 1;
    }
    
    .notification-close:hover {
        opacity: 0.8;
    }
`;
document.head.appendChild(style);