import random
import json
import os
import re
import math
import time

class AIModel:
    """A simple artificial intelligence model class"""
    
    def __init__(self):
        """Initialize the model and load necessary data"""
        self.responses = self._load_responses()
        self.conversation_history = []
        self.max_history = 10  # Maximum conversation history to keep
        self.teaching_mode = False  # Teaching mode flag
        self.learned_data = self._load_learned_data()
    
    def _load_responses(self):
        """Load response data"""
        # Default responses
        default_responses = {
            "greetings": [
                "Hello! How can I help you?",
                "Hi! I'm the AqAI assistant at your service.",
                "Hello! Would you like to learn more about our AI solutions?"
            ],
            "farewells": [
                "Goodbye! Feel free to ask if you have more questions.",
                "Have a great day! I'm here if you need help.",
                "Farewell! Hope to see you again soon."
            ],
            "ai_info": [
                "Artificial intelligence refers to computer systems designed to mimic human intelligence.",
                "AI is systems that learn from data and become smarter over time.",
                "Artificial intelligence technologies are used in data analysis, natural language processing, and machine learning."
            ],
            "services": [
                "At AqAI, we offer custom AI solutions for your business.",
                "Our services include machine learning, data analysis, and natural language processing.",
                "You can contact us to develop custom AI solutions for your needs."
            ],
            "contact": [
                "You can fill out the contact form to get in touch with us.",
                "For more information, you can send an email to info@aqai.com.",
                "You can reach us through the contact section."
            ],
            "unknown": [
                "I'm sorry, my knowledge on this topic is limited. How else can I help you?",
                "I need to do more research to answer this question.",
                "I can't help you with this topic. Is there something else I can assist you with?"
            ],
            "mathematics": [
                "I can help with basic mathematical calculations. What would you like to calculate?",
                "Our mathematical modeling services can solve complex optimization problems for your business.",
                "Mathematics is at the core of our AI algorithms. We use advanced statistical methods to analyze data and make predictions."
            ],
            "math_answers": {
                "addition": "The sum of {a} and {b} is {result}.",
                "subtraction": "The difference between {a} and {b} is {result}.",
                "multiplication": "The product of {a} and {b} is {result}.",
                "division": "The result of dividing {a} by {b} is {result}.",
                "square_root": "The square root of {a} is {result}.",
                "power": "{a} raised to the power of {b} is {result}."
            },
            "tr_math_answers": {
                "addition": "{a} ile {b} toplamı {result} eder.",
                "subtraction": "{a} eksi {b} işleminin sonucu {result} eder.",
                "multiplication": "{a} çarpı {b} işleminin sonucu {result} eder.",
                "division": "{a} bölü {b} işleminin sonucu {result} eder.",
                "square_root": "{a} sayısının karekökü {result} eder.",
                "power": "{a} üssü {b} işleminin sonucu {result} eder.",
                "general": "{expression} işleminin sonucu {result} eder."
            },
            "teaching_mode": {
                "activated": "Teaching mode activated. You can now teach me new information. Please enter the information in the format: 'Question: [question] Answer: [answer]'",
                "deactivated": "Teaching mode deactivated. Thank you for teaching me new information.",
                "saved": "Thank you! I've saved this information. Would you like to teach me something else?",
                "format_error": "Please enter the information in the format: 'Question: [question] Answer: [answer]'",
                "already_exists": "This question already exists in my database. Would you like to update it?",
                "updated": "Information successfully updated.",
                "help": "In teaching mode, you can teach me new information. Enter the information in the format: 'Question: [question] Answer: [answer]'. To exit teaching mode, type 'exit teaching mode'."
            },
            "tr_teaching_mode": {
                "activated": "Öğretme modu aktif edildi. Şimdi bana yeni bilgiler öğretebilirsiniz. Bilgiyi şu formatta girin: 'Soru: [soru] Cevap: [cevap]'",
                "deactivated": "Öğretme modu devre dışı bırakıldı. Teşekkür ederim, öğrettiğiniz bilgileri kaydettim.",
                "saved": "Teşekkürler! Bu bilgiyi kaydettim. Başka bir şey öğretmek ister misiniz?",
                "format_error": "Lütfen bilgiyi şu formatta girin: 'Soru: [soru] Cevap: [cevap]'",
                "already_exists": "Bu soru zaten veritabanımda mevcut. Güncellemek ister misiniz?",
                "updated": "Bilgi başarıyla güncellendi.",
                "help": "Öğretme modunda bana yeni bilgiler öğretebilirsiniz. Bilgiyi 'Soru: [soru] Cevap: [cevap]' formatında girin. Öğretme modundan çıkmak için 'öğretme modunu kapat' yazabilirsiniz."
            }
        }
        
        # Load custom response file if it exists
        responses_file = os.path.join(os.path.dirname(__file__), 'data', 'responses.json')
        if os.path.exists(responses_file):
            try:
                with open(responses_file, 'r', encoding='utf-8') as f:
                    custom_responses = json.load(f)
                    # Merge default responses with custom responses
                    for category, responses in custom_responses.items():
                        if category in default_responses:
                            if isinstance(responses, dict) and isinstance(default_responses[category], dict):
                                default_responses[category].update(responses)
                            elif isinstance(responses, list) and isinstance(default_responses[category], list):
                                default_responses[category].extend(responses)
                            else:
                                default_responses[category] = responses
                        else:
                            default_responses[category] = responses
            except Exception as e:
                print(f"Error loading response file: {e}")
        
        return default_responses
    
    def _load_learned_data(self):
        """Load learned data from file"""
        learned_data_file = os.path.join(os.path.dirname(__file__), 'data', 'learned_data.json')
        if os.path.exists(learned_data_file):
            try:
                with open(learned_data_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception as e:
                print(f"Error loading learned data: {e}")
                return {}
        else:
            return {}
    
    def _save_learned_data(self):
        """Save learned data to file"""
        learned_data_file = os.path.join(os.path.dirname(__file__), 'data', 'learned_data.json')
        data_dir = os.path.dirname(learned_data_file)
        
        # Create data directory if it doesn't exist
        if not os.path.exists(data_dir):
            os.makedirs(data_dir)
        
        try:
            with open(learned_data_file, 'w', encoding='utf-8') as f:
                json.dump(self.learned_data, f, ensure_ascii=False, indent=4)
        except Exception as e:
            print(f"Error saving learned data: {e}")
    
    def generate_response(self, user_message):
        """Generate a response to the user message"""
        # Add to conversation history
        self.conversation_history.append({"user": user_message})
        
        # Simulate thinking time (0.5 to 1.5 seconds)
        thinking_time = random.uniform(0.5, 1.5)
        time.sleep(thinking_time)
        
        # Process the message
        processed_message = self._preprocess_message(user_message)
        
        # Detect language (simple check for Turkish keywords)
        is_turkish = any(word in processed_message for word in ['merhaba', 'selam', 'nasılsın', 'nedir', 'öğret', 'kapat'])
        
        # Check if it's a teaching mode command
        teaching_response = self._process_teaching_mode(user_message, is_turkish)
        if teaching_response:
            self.conversation_history.append({"ai": teaching_response})
            return teaching_response
        
        # If in teaching mode, don't process other commands
        if self.teaching_mode:
            # Check for simple stop command
            if user_message.lower().strip() == "stop" or user_message.lower().strip() == "dur":
                self.teaching_mode = False
                response_dict = self.responses["tr_teaching_mode"] if is_turkish else self.responses["teaching_mode"]
                deactivation_response = response_dict["deactivated"]
                self.conversation_history.append({"ai": deactivation_response})
                return deactivation_response
            
            # Process teaching input
            teaching_input_response = self._process_teaching_input(user_message, is_turkish)
            self.conversation_history.append({"ai": teaching_input_response})
            return teaching_input_response
        
        # Check if the question exists in learned data
        for question, answer in self.learned_data.items():
            # Simple fuzzy matching
            if self._is_similar(processed_message, question.lower()):
                self.conversation_history.append({"ai": answer})
                return answer
        
        # Check if it's a math question
        math_result = self._process_math_question(user_message)
        if math_result:
            response = math_result
        else:
            # Categorize the message
            category = self._categorize_message(processed_message)
            
            # Select a response based on category
            if category in self.responses:
                response = random.choice(self.responses[category])
            else:
                response = random.choice(self.responses["unknown"])
        
        # Add response to conversation history
        self.conversation_history.append({"ai": response})
        
        # Limit history
        if len(self.conversation_history) > self.max_history * 2:
            self.conversation_history = self.conversation_history[-self.max_history*2:]
        
        return response
    
    def _is_similar(self, text1, text2, threshold=0.7):
        """Check if two texts are similar using a simple similarity measure"""
        # Convert to sets of words
        words1 = set(text1.split())
        words2 = set(text2.split())
        
        # Calculate Jaccard similarity
        intersection = len(words1.intersection(words2))
        union = len(words1.union(words2))
        
        if union == 0:
            return False
        
        similarity = intersection / union
        return similarity >= threshold
    
    def _process_teaching_mode(self, message, is_turkish):
        """Process teaching mode commands"""
        response_dict = self.responses["tr_teaching_mode"] if is_turkish else self.responses["teaching_mode"]
        
        # Check for teaching mode activation
        if re.search(r'(activate|enable|start|turn on)\s+teaching\s+mode', message, re.IGNORECASE) or \
           re.search(r'(öğretme|öğrenme)\s+mod(u|unu)\s+(aç|aktif|başlat|etkinleştir)', message, re.IGNORECASE):
            self.teaching_mode = True
            return response_dict["activated"]
        
        # Check for teaching mode deactivation
        elif re.search(r'(deactivate|disable|stop|turn off|exit)\s+teaching\s+mode', message, re.IGNORECASE) or \
             re.search(r'(öğretme|öğrenme)\s+mod(u|unu)\s+(kapat|devre dışı|durdur)', message, re.IGNORECASE) or \
             message.lower().strip() == "stop" or message.lower().strip() == "dur":
            self.teaching_mode = False
            return response_dict["deactivated"]
        
        # Check for teaching mode help
        elif re.search(r'(how\s+to|help)\s+(use|with)\s+teaching\s+mode', message, re.IGNORECASE) or \
             re.search(r'öğretme\s+mod(u|unu)\s+(nasıl|yardım)', message, re.IGNORECASE):
            return response_dict["help"]
        
        return None
    
    def _process_teaching_input(self, message, is_turkish):
        """Process input in teaching mode"""
        response_dict = self.responses["tr_teaching_mode"] if is_turkish else self.responses["teaching_mode"]
        
        # Check for question-answer format
        if is_turkish:
            pattern = re.compile(r'soru:\s*(.+?)\s*cevap:\s*(.+)', re.IGNORECASE | re.DOTALL)
        else:
            pattern = re.compile(r'question:\s*(.+?)\s*answer:\s*(.+)', re.IGNORECASE | re.DOTALL)
        
        match = pattern.search(message)
        if match:
            question = match.group(1).strip()
            answer = match.group(2).strip()
            
            # Check if question already exists
            if question.lower() in [q.lower() for q in self.learned_data.keys()]:
                # For simplicity, we'll just update it
                self.learned_data[question] = answer
                self._save_learned_data()
                return response_dict["updated"]
            else:
                # Add new question-answer pair
                self.learned_data[question] = answer
                self._save_learned_data()
                return response_dict["saved"]
        else:
            return response_dict["format_error"]
    
    def _preprocess_message(self, message):
        """Process the message"""
        # Convert to lowercase
        message = message.lower()
        # Remove punctuation
        message = re.sub(r'[^\w\s]', '', message)
        return message
    
    def _categorize_message(self, message):
        """Categorize the message"""
        # Simple keyword-based categorization
        if any(word in message for word in ["hello", "hi", "hey", "how are you"]):
            return "greetings"
        elif any(word in message for word in ["goodbye", "bye", "see you", "farewell"]):
            return "farewells"
        elif any(word in message for word in ["artificial intelligence", "ai", "machine learning", "ml"]):
            return "ai_info"
        elif any(word in message for word in ["service", "what do you do", "solution", "product"]):
            return "services"
        elif any(word in message for word in ["contact", "phone", "email", "message", "reach"]):
            return "contact"
        elif any(word in message for word in ["math", "mathematics", "calculation", "compute", "calculate"]):
            return "mathematics"
        else:
            return "unknown"
    
    def _process_math_question(self, message):
        """Process mathematical questions and return the answer"""
        # Detect language (simple check for Turkish keywords)
        is_turkish = any(word in message.lower() for word in ['topla', 'çıkar', 'çarp', 'böl', 'karekök', 'üssü', 'hesapla', 'nedir'])
        
        # Try to evaluate direct mathematical expressions
        try:
            # Check if the message contains only mathematical expression
            # Remove all spaces
            clean_message = message.strip().replace(" ", "")
            
            # Check if it's a simple mathematical expression with basic operators
            if re.match(r'^[\d\+\-\*\/\^\(\)\.]+$', clean_message):
                # Replace ^ with ** for Python's power operator
                clean_message = clean_message.replace('^', '**')
                
                # Safely evaluate the expression
                result = eval(clean_message)
                
                # Use Turkish or English responses based on detected language
                response_dict = self.responses["tr_math_answers"] if is_turkish else self.responses["math_answers"]
                
                # Determine the operation type
                if '+' in message:
                    return response_dict["addition"].format(a=clean_message, b="", result=result)
                elif '-' in message:
                    return response_dict["subtraction"].format(a=clean_message, b="", result=result)
                elif '*' in message or 'x' in message.lower():
                    return response_dict["multiplication"].format(a=clean_message, b="", result=result)
                elif '/' in message:
                    return response_dict["division"].format(a=clean_message, b="", result=result)
                elif '**' in clean_message or '^' in message:
                    return response_dict["power"].format(a=clean_message, b="", result=result)
                else:
                    if is_turkish:
                        return f"{clean_message} işleminin sonucu {result} eder."
                    else:
                        return f"The result of {clean_message} is {result}."
        except:
            # If evaluation fails, continue with pattern matching
            pass
        
        # Choose response dictionary based on language
        response_dict = self.responses["tr_math_answers"] if is_turkish else self.responses["math_answers"]
        
        # Direct mathematical expression pattern: "1+3", "5-2", "4*6", "10/2"
        direct_math_pattern = re.compile(r'^(\d+(?:\.\d+)?)\s*([\+\-\*\/\^])\s*(\d+(?:\.\d+)?)$')
        direct_math_match = direct_math_pattern.search(message)
        if direct_math_match:
            a = float(direct_math_match.group(1))
            operator = direct_math_match.group(2)
            b = float(direct_math_match.group(3))
            
            if operator == '+':
                result = a + b
                return response_dict["addition"].format(a=a, b=b, result=result)
            elif operator == '-':
                result = a - b
                return response_dict["subtraction"].format(a=a, b=b, result=result)
            elif operator == '*':
                result = a * b
                return response_dict["multiplication"].format(a=a, b=b, result=result)
            elif operator == '/':
                if b == 0:
                    return "Sıfıra bölme yapılamaz." if is_turkish else "I cannot divide by zero. Please provide a non-zero divisor."
                result = a / b
                return response_dict["division"].format(a=a, b=b, result=result)
            elif operator == '^':
                result = math.pow(a, b)
                return response_dict["power"].format(a=a, b=b, result=result)
        
        # Turkish patterns
        if is_turkish:
            # Turkish addition pattern
            tr_addition_pattern = re.compile(r'(?:(?:kaç|ne|nedir|hesapla|bul|topla))\s+(\d+(?:\.\d+)?)\s+(?:(?:artı|ve|ile|\+))\s+(\d+(?:\.\d+)?)', re.IGNORECASE)
            tr_addition_match = tr_addition_pattern.search(message)
            if tr_addition_match:
                a = float(tr_addition_match.group(1))
                b = float(tr_addition_match.group(2))
                result = a + b
                return response_dict["addition"].format(a=a, b=b, result=result)
            
            # Turkish subtraction pattern
            tr_subtraction_pattern = re.compile(r'(?:(?:kaç|ne|nedir|hesapla|bul))\s+(\d+(?:\.\d+)?)\s+(?:(?:eksi|çıkar))\s+(\d+(?:\.\d+)?)', re.IGNORECASE)
            tr_subtraction_match = tr_subtraction_pattern.search(message)
            if tr_subtraction_match:
                a = float(tr_subtraction_match.group(1))
                b = float(tr_subtraction_match.group(2))
                result = a - b
                return response_dict["subtraction"].format(a=a, b=b, result=result)
            
            # Turkish multiplication pattern
            tr_multiplication_pattern = re.compile(r'(?:(?:kaç|ne|nedir|hesapla|bul))\s+(\d+(?:\.\d+)?)\s+(?:(?:çarpı|kere|kez|\*))\s+(\d+(?:\.\d+)?)', re.IGNORECASE)
            tr_multiplication_match = tr_multiplication_pattern.search(message)
            if tr_multiplication_match:
                a = float(tr_multiplication_match.group(1))
                b = float(tr_multiplication_match.group(2))
                result = a * b
                return response_dict["multiplication"].format(a=a, b=b, result=result)
            
            # Turkish division pattern
            tr_division_pattern = re.compile(r'(?:(?:kaç|ne|nedir|hesapla|bul))\s+(\d+(?:\.\d+)?)\s+(?:(?:bölü|\/|÷))\s+(\d+(?:\.\d+)?)', re.IGNORECASE)
            tr_division_match = tr_division_pattern.search(message)
            if tr_division_match:
                a = float(tr_division_match.group(1))
                b = float(tr_division_match.group(2))
                if b == 0:
                    return "Sıfıra bölme yapılamaz."
                result = a / b
                return response_dict["division"].format(a=a, b=b, result=result)
            
            # Turkish square root pattern
            tr_sqrt_pattern = re.compile(r'(?:(?:kaç|ne|nedir|hesapla|bul))\s+(?:(?:karekök|kök))\s+(\d+(?:\.\d+)?)', re.IGNORECASE)
            tr_sqrt_match = tr_sqrt_pattern.search(message)
            if tr_sqrt_match:
                a = float(tr_sqrt_match.group(1))
                if a < 0:
                    return "Negatif sayıların karekökü reel sayı sisteminde hesaplanamaz."
                result = math.sqrt(a)
                return response_dict["square_root"].format(a=a, result=result)
            
            # Turkish power pattern
            tr_power_pattern = re.compile(r'(?:(?:kaç|ne|nedir|hesapla|bul))\s+(\d+(?:\.\d+)?)\s+(?:(?:üssü|üzeri|kuvveti))\s+(\d+(?:\.\d+)?)', re.IGNORECASE)
            tr_power_match = tr_power_pattern.search(message)
            if tr_power_match:
                a = float(tr_power_match.group(1))
                b = float(tr_power_match.group(2))
                result = math.pow(a, b)
                return response_dict["power"].format(a=a, b=b, result=result)
        
        # English patterns
        # Addition pattern: "what is X plus Y" or "add X and Y"
        addition_pattern = re.compile(r'(?:what\s+is|calculate|compute|add)\s+(\d+(?:\.\d+)?)\s+(?:plus|and|\+)\s+(\d+(?:\.\d+)?)', re.IGNORECASE)
        addition_match = addition_pattern.search(message)
        if addition_match:
            a = float(addition_match.group(1))
            b = float(addition_match.group(2))
            result = a + b
            return response_dict["addition"].format(a=a, b=b, result=result)
        
        # Subtraction pattern: "what is X minus Y" or "subtract Y from X"
        subtraction_pattern = re.compile(r'(?:what\s+is|calculate|compute)\s+(\d+(?:\.\d+)?)\s+(?:minus|subtract|subtracted by|-)\s+(\d+(?:\.\d+)?)', re.IGNORECASE)
        subtraction_match = subtraction_pattern.search(message)
        if subtraction_match:
            a = float(subtraction_match.group(1))
            b = float(subtraction_match.group(2))
            result = a - b
            return response_dict["subtraction"].format(a=a, b=b, result=result)
        
        # Multiplication pattern: "what is X times Y" or "multiply X by Y"
        multiplication_pattern = re.compile(r'(?:what\s+is|calculate|compute|multiply)\s+(\d+(?:\.\d+)?)\s+(?:times|multiplied by|\*)\s+(\d+(?:\.\d+)?)', re.IGNORECASE)
        multiplication_match = multiplication_pattern.search(message)
        if multiplication_match:
            a = float(multiplication_match.group(1))
            b = float(multiplication_match.group(2))
            result = a * b
            return response_dict["multiplication"].format(a=a, b=b, result=result)
        
        # Division pattern: "what is X divided by Y" or "divide X by Y"
        division_pattern = re.compile(r'(?:what\s+is|calculate|compute|divide)\s+(\d+(?:\.\d+)?)\s+(?:divided by|\/)\s+(\d+(?:\.\d+)?)', re.IGNORECASE)
        division_match = division_pattern.search(message)
        if division_match:
            a = float(division_match.group(1))
            b = float(division_match.group(2))
            if b == 0:
                return "I cannot divide by zero. Please provide a non-zero divisor."
            result = a / b
            return response_dict["division"].format(a=a, b=b, result=result)
        
        # Square root pattern: "what is the square root of X"
        sqrt_pattern = re.compile(r'(?:what\s+is|calculate|compute)\s+(?:the\s+)?(?:square\s+root|sqrt)\s+(?:of\s+)?(\d+(?:\.\d+)?)', re.IGNORECASE)
        sqrt_match = sqrt_pattern.search(message)
        if sqrt_match:
            a = float(sqrt_match.group(1))
            if a < 0:
                return "I cannot calculate the square root of a negative number in the real number system."
            result = math.sqrt(a)
            return response_dict["square_root"].format(a=a, result=result)
        
        # Power pattern: "what is X to the power of Y" or "X raised to Y"
        power_pattern = re.compile(r'(?:what\s+is|calculate|compute)\s+(\d+(?:\.\d+)?)\s+(?:to the power of|raised to|power|\^)\s+(\d+(?:\.\d+)?)', re.IGNORECASE)
        power_match = power_pattern.search(message)
        if power_match:
            a = float(power_match.group(1))
            b = float(power_match.group(2))
            result = math.pow(a, b)
            return response_dict["power"].format(a=a, b=b, result=result)
        
        return None
    
    def get_conversation_history(self):
        """Return the conversation history"""
        return self.conversation_history 