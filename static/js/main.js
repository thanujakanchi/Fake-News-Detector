/**
 * VeriFact - Fake News Detection System
 * Main JavaScript file for interactive features
 */

// ========================================
// DOM READY
// ========================================
document.addEventListener('DOMContentLoaded', function() {
    
    // ========================================
    // 1. CHARACTER COUNTER FOR DETECTOR
    // ========================================
    const textarea = document.getElementById('news-input');
    const charCount = document.getElementById('char-count');
    
    if (textarea && charCount) {
        // Update counter on input
        textarea.addEventListener('input', function() {
            const length = this.value.length;
            charCount.textContent = length;
            
            // Change color when approaching limit
            if (length > 2000) {
                charCount.style.color = '#FF6B6B';
            } else if (length > 1500) {
                charCount.style.color = '#FBBF24';
            } else {
                charCount.style.color = '#A0A0B8';
            }
        });
        
        // Initial count
        if (textarea.value) {
            charCount.textContent = textarea.value.length;
        }
    }
    
    // ========================================
    // 2. FORM SUBMISSION LOADER
    // ========================================
    const detectForm = document.getElementById('detect-form');
    const detectBtn = document.getElementById('detect-btn');
    
    if (detectForm && detectBtn) {
        detectForm.addEventListener('submit', function() {
            const btnText = detectBtn.querySelector('.btn-text');
            const btnLoader = detectBtn.querySelector('.btn-loader');
            
            if (btnText && btnLoader) {
                detectBtn.disabled = true;
                btnText.textContent = 'Analyzing...';
                btnLoader.style.display = 'inline';
            }
        });
    }
    
    // ========================================
    // 3. CLICK EXAMPLE TO COPY TO DETECTOR
    // ========================================
    const exampleItems = document.querySelectorAll('.example-item');
    
    exampleItems.forEach(function(item) {
        item.addEventListener('click', function() {
            const text = this.querySelector('.text')?.textContent || '';
            if (text) {
                // Store in sessionStorage
                sessionStorage.setItem('example_text', text);
                // Navigate to detector
                window.location.href = '/detector';
            }
        });
        
        // Add cursor pointer style
        item.style.cursor = 'pointer';
    });
    
    // ========================================
    // 4. AUTO-FILL DETECTOR FROM EXAMPLES
    // ========================================
    const exampleText = sessionStorage.getItem('example_text');
    const newsInput = document.getElementById('news-input');
    
    if (exampleText && newsInput && window.location.pathname === '/detector') {
        newsInput.value = exampleText;
        // Trigger input event for character counter
        const event = new Event('input');
        newsInput.dispatchEvent(event);
        // Clear storage after use
        sessionStorage.removeItem('example_text');
    }
    
    // ========================================
    // 5. AUTO-DISMISS FLASH MESSAGES
    // ========================================
    const flashMessages = document.querySelectorAll('.flash-message');
    
    flashMessages.forEach(function(msg) {
        // Auto dismiss after 5 seconds
        setTimeout(function() {
            msg.style.transition = 'opacity 0.5s';
            msg.style.opacity = '0';
            setTimeout(function() {
                if (msg.parentNode) {
                    msg.remove();
                }
            }, 500);
        }, 5000);
        
        // Dismiss on click
        msg.addEventListener('click', function() {
            this.style.transition = 'opacity 0.3s';
            this.style.opacity = '0';
            setTimeout(function() {
                if (msg.parentNode) {
                    msg.remove();
                }
            }, 300);
        });
        
        // Add close button
        const closeBtn = document.createElement('span');
        closeBtn.textContent = '×';
        closeBtn.style.cssText = `
            float: right;
            cursor: pointer;
            font-size: 20px;
            font-weight: 300;
            margin-left: 12px;
            opacity: 0.6;
            transition: opacity 0.3s;
        `;
        closeBtn.addEventListener('mouseenter', function() {
            this.style.opacity = '1';
        });
        closeBtn.addEventListener('mouseleave', function() {
            this.style.opacity = '0.6';
        });
        closeBtn.addEventListener('click', function(e) {
            e.stopPropagation();
            const parent = this.parentElement;
            parent.style.transition = 'opacity 0.3s';
            parent.style.opacity = '0';
            setTimeout(function() {
                if (parent.parentNode) {
                    parent.remove();
                }
            }, 300);
        });
        msg.prepend(closeBtn);
    });
    
    // ========================================
    // 6. RESPONSIVE NAVBAR TOGGLE (Mobile)
    // ========================================
    // Add hamburger menu for mobile
    const navbar = document.querySelector('.navbar');
    const navLinks = document.querySelector('.nav-links');
    
    if (navbar && navLinks && window.innerWidth <= 768) {
        // Create hamburger button
        const hamburger = document.createElement('button');
        hamburger.innerHTML = '☰';
        hamburger.style.cssText = `
            background: none;
            border: none;
            color: #fff;
            font-size: 28px;
            cursor: pointer;
            display: block;
            padding: 4px 8px;
        `;
        
        // Insert after logo
        const logo = navbar.querySelector('.logo');
        if (logo) {
            logo.after(hamburger);
        }
        
        // Toggle menu
        hamburger.addEventListener('click', function() {
            if (navLinks.style.display === 'flex') {
                navLinks.style.display = 'none';
                this.innerHTML = '☰';
            } else {
                navLinks.style.display = 'flex';
                this.innerHTML = '✕';
            }
        });
        
        // Hide by default on mobile
        navLinks.style.display = 'none';
        
        // Reset on resize
        window.addEventListener('resize', function() {
            if (window.innerWidth > 768) {
                navLinks.style.display = 'flex';
                hamburger.style.display = 'none';
            } else {
                navLinks.style.display = 'none';
                hamburger.style.display = 'block';
            }
        });
    }
    
    // ========================================
    // 7. SMOOTH SCROLL FOR ANCHOR LINKS
    // ========================================
    document.querySelectorAll('a[href^="#"]').forEach(function(anchor) {
        anchor.addEventListener('click', function(e) {
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                e.preventDefault();
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });
    
    // ========================================
    // 8. KEYBOARD SHORTCUTS
    // ========================================
    document.addEventListener('keydown', function(e) {
        // Ctrl+Enter to submit form on detector page
        if ((e.ctrlKey || e.metaKey) && e.key === 'Enter') {
            const form = document.getElementById('detect-form');
            if (form && window.location.pathname === '/detector') {
                e.preventDefault();
                form.submit();
            }
        }
        
        // Escape key to clear flash messages
        if (e.key === 'Escape') {
            document.querySelectorAll('.flash-message').forEach(function(msg) {
                msg.style.transition = 'opacity 0.3s';
                msg.style.opacity = '0';
                setTimeout(function() {
                    if (msg.parentNode) {
                        msg.remove();
                    }
                }, 300);
            });
        }
    });
    
    // ========================================
    // 9. DASHBOARD ANIMATIONS
    // ========================================
    const statCards = document.querySelectorAll('.stat-card');
    
    if (statCards.length > 0) {
        const observer = new IntersectionObserver(function(entries) {
            entries.forEach(function(entry, index) {
                if (entry.isIntersecting) {
                    setTimeout(function() {
                        entry.target.style.opacity = '1';
                        entry.target.style.transform = 'translateY(0)';
                    }, index * 100);
                }
            });
        }, { threshold: 0.1 });
        
        statCards.forEach(function(card) {
            card.style.opacity = '0';
            card.style.transform = 'translateY(20px)';
            card.style.transition = 'all 0.6s ease';
            observer.observe(card);
        });
    }
    
    // ========================================
    // 10. FEATURE CARD ANIMATIONS
    // ========================================
    const featureCards = document.querySelectorAll('.feature-card');
    
    if (featureCards.length > 0) {
        const observer = new IntersectionObserver(function(entries) {
            entries.forEach(function(entry, index) {
                if (entry.isIntersecting) {
                    setTimeout(function() {
                        entry.target.style.opacity = '1';
                        entry.target.style.transform = 'translateY(0)';
                    }, index * 150);
                }
            });
        }, { threshold: 0.1 });
        
        featureCards.forEach(function(card) {
            card.style.opacity = '0';
            card.style.transform = 'translateY(30px)';
            card.style.transition = 'all 0.6s ease';
            observer.observe(card);
        });
    }
    
    // ========================================
    // 11. COPY TO CLIPBOARD HELPER
    // ========================================
    window.copyToClipboard = function(text) {
        if (navigator.clipboard) {
            navigator.clipboard.writeText(text).then(function() {
                showToast('Copied to clipboard! ✅');
            }).catch(function() {
                fallbackCopy(text);
            });
        } else {
            fallbackCopy(text);
        }
    };
    
    function fallbackCopy(text) {
        const textarea = document.createElement('textarea');
        textarea.value = text;
        textarea.style.position = 'fixed';
        textarea.style.opacity = '0';
        document.body.appendChild(textarea);
        textarea.select();
        try {
            document.execCommand('copy');
            showToast('Copied to clipboard! ✅');
        } catch (err) {
            showToast('Failed to copy ❌');
        }
        document.body.removeChild(textarea);
    }
    
    function showToast(message) {
        const toast = document.createElement('div');
        toast.textContent = message;
        toast.style.cssText = `
            position: fixed;
            bottom: 30px;
            left: 50%;
            transform: translateX(-50%);
            background: rgba(30, 41, 59, 0.95);
            color: #fff;
            padding: 12px 24px;
            border-radius: 12px;
            font-size: 14px;
            z-index: 9999;
            border: 1px solid rgba(56, 189, 248, 0.2);
            backdrop-filter: blur(12px);
            animation: fadeInUp 0.4s ease;
            max-width: 90%;
            text-align: center;
        `;
        document.body.appendChild(toast);
        
        setTimeout(function() {
            toast.style.transition = 'opacity 0.4s';
            toast.style.opacity = '0';
            setTimeout(function() {
                if (toast.parentNode) {
                    toast.remove();
                }
            }, 400);
        }, 3000);
    }
    
    // ========================================
    // 12. DARK MODE TOGGLE (Optional)
    // ========================================
    // Check if user prefers dark mode
    const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
    
    // Add toggle button to navbar if needed
    // (Currently using dark mode by default)
    
    // ========================================
    // 13. ANALYTICS TRACKING (Optional)
    // ========================================
    // Track page views
    function trackPageView(page) {
        if (window.gtag) {
            window.gtag('event', 'page_view', {
                page_title: page,
                page_location: window.location.href
            });
        }
    }
    
    // Track detection events
    window.trackDetection = function(result, category, confidence) {
        if (window.gtag) {
            window.gtag('event', 'detection', {
                'result': result,
                'category': category,
                'confidence': confidence
            });
        }
    };
    
    // ========================================
    // 14. PERFORMANCE MONITORING
    // ========================================
    // Log page load time
    window.addEventListener('load', function() {
        const loadTime = performance.now();
        console.log(`Page loaded in ${loadTime.toFixed(2)}ms`);
    });
    
    // ========================================
    // 15. KEYBOARD NAVIGATION (Accessibility)
    // ========================================
    document.addEventListener('keydown', function(e) {
        // Alt+1 → Home
        if (e.altKey && e.key === '1') {
            window.location.href = '/';
        }
        // Alt+2 → Detector
        if (e.altKey && e.key === '2') {
            window.location.href = '/detector';
        }
        // Alt+3 → Dashboard
        if (e.altKey && e.key === '3') {
            window.location.href = '/dashboard';
        }
        // Alt+4 → Features
        if (e.altKey && e.key === '4') {
            window.location.href = '/features';
        }
        // Alt+5 → About
        if (e.altKey && e.key === '5') {
            window.location.href = '/about';
        }
    });
    
    console.log('🚀 VeriFact JS loaded successfully!');
    console.log('📖 Keyboard shortcuts: Alt+1 (Home), Alt+2 (Detector), Alt+3 (Dashboard)');
});

// ========================================
// GLOBAL FUNCTIONS
// ========================================

/**
 * Copy text to detector page
 */
window.copyToDetector = function(text) {
    sessionStorage.setItem('example_text', text);
    window.location.href = '/detector';
};

/**
 * Share result (opens share dialog)
 */
window.shareResult = function(text) {
    if (navigator.share) {
        navigator.share({
            title: 'VeriFact Result',
            text: text,
            url: window.location.href
        }).catch(function() {
            // User cancelled
        });
    } else {
        // Fallback: copy to clipboard
        copyToClipboard(text);
    }
};

/**
 * Print current page
 */
window.printPage = function() {
    window.print();
};

/**
 * Reload detector with new text
 */
window.reloadWithText = function(text) {
    sessionStorage.setItem('example_text', text);
    window.location.reload();
};