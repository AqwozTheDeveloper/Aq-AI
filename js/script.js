// Mobil menü için burger menü işlevselliği
const burger = document.querySelector('.burger');
const nav = document.querySelector('.nav-links');

burger.addEventListener('click', () => {
    nav.classList.toggle('active');
    burger.classList.toggle('toggle');
});

// Sayfa kaydırma animasyonu
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function(e) {
        e.preventDefault();
        
        const targetId = this.getAttribute('href');
        const targetElement = document.querySelector(targetId);
        
        window.scrollTo({
            top: targetElement.offsetTop - 80,
            behavior: 'smooth'
        });
        
        // Mobil menüyü kapat
        if (nav.classList.contains('active')) {
            nav.classList.remove('active');
            burger.classList.remove('toggle');
        }
    });
});

// API URL'leri
const API_BASE_URL = '/api';
const CHAT_API = `${API_BASE_URL}/chat`;
const SERVICES_API = `${API_BASE_URL}/services`;
const CONTACT_API = `${API_BASE_URL}/contact`;

// Yapay Zeka Chat Demo
const chatMessages = document.getElementById('chat-messages');
const userInput = document.getElementById('user-input');
const sendBtn = document.getElementById('send-btn');

// Yedek yanıtlar (API bağlantısı olmadığında kullanılır)
const fallbackResponses = [
    "Yapay zeka, insan zekasını taklit etmek için tasarlanmış bilgisayar sistemleridir.",
    "Size bu konuda yardımcı olabilirim. Daha fazla bilgi verebilir misiniz?",
    "AqAI olarak, işletmenize özel yapay zeka çözümleri sunuyoruz.",
    "Bu sorunun cevabı için biraz daha araştırma yapmam gerekiyor.",
    "Yapay zeka teknolojileri, veri analizi, doğal dil işleme ve makine öğrenmesi gibi alanlarda kullanılır.",
    "Evet, yapay zeka sistemleri büyük veri setlerinden öğrenebilir ve zamanla daha akıllı hale gelebilir.",
    "Bu konuda size özel bir çözüm sunabiliriz. İletişim formunu doldurarak bizimle iletişime geçebilirsiniz."
];

// Mesaj gönderme işlevi
async function sendMessage() {
    const message = userInput.value.trim();
    
    if (message !== '') {
        // Kullanıcı mesajını ekle
        addMessage(message, 'user');
        
        // Giriş alanını temizle
        userInput.value = '';
        
        try {
            // API'ye istek gönder
            const response = await fetch(CHAT_API, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ message })
            });
            
            if (response.ok) {
                const data = await response.json();
                addMessage(data.response, 'bot');
            } else {
                // API hatası durumunda yedek yanıt kullan
                const randomResponse = fallbackResponses[Math.floor(Math.random() * fallbackResponses.length)];
                addMessage(randomResponse, 'bot');
                console.error('API yanıt hatası:', response.status);
            }
        } catch (error) {
            // Bağlantı hatası durumunda yedek yanıt kullan
            const randomResponse = fallbackResponses[Math.floor(Math.random() * fallbackResponses.length)];
            addMessage(randomResponse, 'bot');
            console.error('API bağlantı hatası:', error);
        }
    }
}

// Mesaj ekleme işlevi
function addMessage(text, sender) {
    const messageElement = document.createElement('div');
    messageElement.classList.add('message', sender);
    messageElement.textContent = text;
    
    chatMessages.appendChild(messageElement);
    
    // Otomatik kaydırma
    chatMessages.scrollTop = chatMessages.scrollHeight;
}

// Gönder düğmesi tıklama olayı
sendBtn.addEventListener('click', sendMessage);

// Enter tuşu basma olayı
userInput.addEventListener('keypress', (e) => {
    if (e.key === 'Enter') {
        sendMessage();
    }
});

// Hizmetleri API'den yükle
async function loadServices() {
    const servicesContainer = document.querySelector('.services-container');
    
    if (!servicesContainer) return;
    
    try {
        const response = await fetch(SERVICES_API);
        
        if (response.ok) {
            const services = await response.json();
            
            // Mevcut hizmetleri temizle
            servicesContainer.innerHTML = '';
            
            // Hizmetleri ekle
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
        console.error('Hizmetler yüklenirken hata oluştu:', error);
    }
}

// İletişim formu gönderimi
const contactForm = document.getElementById('contact-form');

contactForm.addEventListener('submit', async (e) => {
    e.preventDefault();
    
    // Form verilerini al
    const name = document.getElementById('name').value;
    const email = document.getElementById('email').value;
    const message = document.getElementById('message').value;
    
    try {
        // API'ye istek gönder
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
            alert(`Hata: ${errorData.error || 'Bir sorun oluştu. Lütfen daha sonra tekrar deneyin.'}`);
        }
    } catch (error) {
        console.error('İletişim formu gönderilirken hata oluştu:', error);
        alert('Bağlantı hatası. Lütfen daha sonra tekrar deneyin.');
    }
});

// Sayfa yüklendiğinde animasyon
window.addEventListener('load', () => {
    document.body.classList.add('loaded');
    
    // Hizmetleri yükle
    loadServices();
});

// Scroll olayı - Navbar arka planını değiştir
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