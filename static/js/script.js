
// Mobile menu burger functionality
const burger = document.querySelector('.burger');
const nav = document.querySelector('.nav-links');

burger.addEventListener('click', () => {
    nav.classList.toggle('active');
    burger.classList.toggle('toggle');
});

// Page scroll animation
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function(e) {
        e.preventDefault();
        
        const targetId = this.getAttribute('href');
        const targetElement = document.querySelector(targetId);
        
        window.scrollTo({
            top: targetElement.offsetTop - 80,
            behavior: 'smooth'
        });
        
        // Close mobile menu
        if (nav.classList.contains('active')) {
            nav.classList.remove('active');
            burger.classList.remove('toggle');
        }
    });
});

// API URLs
const API_BASE_URL = '/api';
const CHAT_API = `${API_BASE_URL}/chat`;
const SERVICES_API = `${API_BASE_URL}/services`;
const CONTACT_API = `${API_BASE_URL}/contact`;

// AI Chat Demo
const chatMessages = document.getElementById('chat-messages');
const userInput = document.getElementById('user-input');
const sendBtn = document.getElementById('send-btn');

// Fallback responses (used when API connection fails)
const fallbackResponses = [
    "Artificial intelligence refers to computer systems designed to mimic human intelligence.",
    "I can help you with that. Could you provide more information?",
    "At AqAI, we offer custom AI solutions for your business.",
    "I need to do more research to answer this question.",
    "Artificial intelligence technologies are used in data analysis, natural language processing, and machine learning.",
    "Yes, AI systems can learn from large datasets and become smarter over time.",
    "We can offer a custom solution for this. Please fill out the contact form to get in touch with us."
];

// Send message function
async function sendMessage() {
    const message = userInput.value.trim();
    
    if (message !== '') {
        // Add user message
        addMessage(message, 'user');
        
        // Clear input field
        userInput.value = '';
        
        // Show loading animation
        const loadingElement = document.createElement('div');
        loadingElement.classList.add('message', 'bot', 'loading');
        loadingElement.innerHTML = 'Thinking<div class="loading-dots"><span></span><span></span><span></span></div>';
        chatMessages.appendChild(loadingElement);
        
        // Auto scroll
        chatMessages.scrollTop = chatMessages.scrollHeight;
        
        try {
            // Send request to API
            const response = await fetch(CHAT_API, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ message })
            });
            
            // Remove loading animation
            chatMessages.removeChild(loadingElement);
            
            if (response.ok) {
                const data = await response.json();
                addMessage(data.response, 'bot');
            } else {
                // Use fallback response in case of API error
                const randomResponse = fallbackResponses[Math.floor(Math.random() * fallbackResponses.length)];
                addMessage(randomResponse, 'bot');
                console.error('API response error:', response.status);
            }
        } catch (error) {
            // Remove loading animation
            chatMessages.removeChild(loadingElement);
            
            // Use fallback response in case of connection error
            const randomResponse = fallbackResponses[Math.floor(Math.random() * fallbackResponses.length)];
            addMessage(randomResponse, 'bot');
            console.error('API connection error:', error);
        }
    }
}

// Add message function
function addMessage(text, sender) {
    const messageElement = document.createElement('div');
    messageElement.classList.add('message', sender);
    messageElement.textContent = text;
    
    chatMessages.appendChild(messageElement);
    
    // Auto scroll
    chatMessages.scrollTop = chatMessages.scrollHeight;
}

// Send button click event
sendBtn.addEventListener('click', sendMessage);

// Enter key press event
userInput.addEventListener('keypress', (e) => {
    if (e.key === 'Enter') {
        sendMessage();
    }
});

// Load services from API
async function loadServices() {
    const servicesContainer = document.querySelector('.services-container');
    
    if (!servicesContainer) return;
    
    try {
        const response = await fetch(SERVICES_API);
        
        if (response.ok) {
            const services = await response.json();
            
            // Clear existing services
            servicesContainer.innerHTML = '';
            
            // Add services
            services.forEach(service => {
                const serviceCard = document.createElement('div');
                serviceCard.classList.add('service-card');
                
                serviceCard.innerHTML = `
                    <i class="fas ${service.icon}"></i>
                    <h3>${service.title}</h3>
                    <p>${service.description}</p>
                `;
                
                servicesContainer.appendChild(serviceCard);
            });
        }
    } catch (error) {
        console.error('Error loading services:', error);
    }
}

// Contact form submission
const contactForm = document.getElementById('contact-form');

contactForm.addEventListener('submit', async (e) => {
    e.preventDefault();
    
    // Get form data
    const name = document.getElementById('name').value;
    const email = document.getElementById('email').value;
    const message = document.getElementById('message').value;
    
    try {
        // Send request to API
        const response = await fetch(CONTACT_API, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ name, email, message })
        });
        
        if (response.ok) {
            const data = await response.json();
            alert(data.message);
            contactForm.reset();
        } else {
            const errorData = await response.json();
            alert(`Error: ${errorData.error || 'Something went wrong. Please try again later.'}`);
        }
    } catch (error) {
        console.error('Error sending contact form:', error);
        alert('Connection error. Please try again later.');
    }
});

// Page load animation
window.addEventListener('load', () => {
    document.body.classList.add('loaded');
    
    // Load services
    loadServices();
});

// Scroll event - Change navbar background
window.addEventListener('scroll', () => {
    const navbar = document.querySelector('.navbar');
    
    if (window.scrollY > 50) {
        navbar.style.backgroundColor = '#fff';
        navbar.style.boxShadow = '0 2px 10px rgba(0, 0, 0, 0.1)';
    } else {
        navbar.style.backgroundColor = 'var(--light-color)';
        navbar.style.boxShadow = 'none';
    }
}); 