from flask import Flask, request, jsonify, render_template, send_from_directory
from flask_cors import CORS
import os
import json
from model import AIModel

# Doğru klasör yollarını belirle
root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
static_dir = os.path.join(root_dir, 'static')

app = Flask(__name__, 
            static_folder=None,  # Statik dosyaları özel olarak işleyeceğiz
            template_folder=root_dir)
CORS(app)  # Cross Origin Resource Sharing etkinleştirme

# AI modelini yükle
ai_model = AIModel()

# Statik dosyaları sunmak için özel route
@app.route('/static/<path:path>')
def serve_static(path):
    return send_from_directory(static_dir, path)

@app.route('/')
def index():
    """Ana sayfa için yönlendirme"""
    return render_template('index.html')

@app.route('/api/chat', methods=['POST'])
def chat():
    """Kullanıcı mesajlarını işleyip AI yanıtı döndüren endpoint"""
    try:
        data = request.get_json()
        user_message = data.get('message', '')
        
        if not user_message:
            return jsonify({'error': 'Mesaj boş olamaz'}), 400
        
        # AI modelinden yanıt al
        response = ai_model.generate_response(user_message)
        
        return jsonify({
            'response': response,
            'status': 'success'
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/services', methods=['GET'])
def get_services():
    """Sunulan hizmetleri döndüren endpoint"""
    services = [
        {
            'id': 1,
            'title': 'Yapay Zeka Çözümleri',
            'description': 'İşletmenize özel yapay zeka modelleri ve çözümleri geliştiriyoruz.',
            'icon': 'fa-robot'
        },
        {
            'id': 2,
            'title': 'Makine Öğrenmesi',
            'description': 'Verilerinizden değer üreten makine öğrenmesi algoritmaları.',
            'icon': 'fa-brain'
        },
        {
            'id': 3,
            'title': 'Veri Analizi',
            'description': 'Büyük veri setlerinden anlamlı içgörüler çıkarın.',
            'icon': 'fa-chart-line'
        },
        {
            'id': 4,
            'title': 'Doğal Dil İşleme',
            'description': 'Metinleri anlayan ve yanıtlayan akıllı sistemler.',
            'icon': 'fa-comments'
        }
    ]
    
    return jsonify(services)

@app.route('/api/contact', methods=['POST'])
def contact():
    """İletişim formunu işleyen endpoint"""
    try:
        data = request.get_json()
        name = data.get('name', '')
        email = data.get('email', '')
        message = data.get('message', '')
        
        if not all([name, email, message]):
            return jsonify({'error': 'Tüm alanlar doldurulmalıdır'}), 400
        
        # Gerçek uygulamada burada e-posta gönderme veya veritabanına kaydetme işlemi yapılır
        # Şimdilik sadece bir dosyaya kaydedelim
        contact_data = {
            'name': name,
            'email': email,
            'message': message,
            'timestamp': import_time()
        }
        
        save_contact(contact_data)
        
        return jsonify({
            'message': 'Mesajınız başarıyla alındı. En kısa sürede size dönüş yapacağız.',
            'status': 'success'
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

def import_time():
    """Şu anki zamanı döndüren yardımcı fonksiyon"""
    from datetime import datetime
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def save_contact(contact_data):
    """İletişim verilerini dosyaya kaydeden yardımcı fonksiyon"""
    data_dir = os.path.join(os.path.dirname(__file__), 'data')
    
    # data klasörü yoksa oluştur
    if not os.path.exists(data_dir):
        os.makedirs(data_dir)
    
    contact_file = os.path.join(data_dir, 'contacts.json')
    
    # Dosya varsa mevcut verileri oku
    if os.path.exists(contact_file):
        with open(contact_file, 'r', encoding='utf-8') as f:
            try:
                contacts = json.load(f)
            except json.JSONDecodeError:
                contacts = []
    else:
        contacts = []
    
    # Yeni iletişim verisini ekle
    contacts.append(contact_data)
    
    # Dosyaya kaydet
    with open(contact_file, 'w', encoding='utf-8') as f:
        json.dump(contacts, f, ensure_ascii=False, indent=4)

if __name__ == '__main__':
    print("AqAI Web Uygulaması Başlatılıyor...")
    print("Web tarayıcınızda http://localhost:5000 adresini açın")
    app.run(debug=True, host='0.0.0.0', port=5000) 