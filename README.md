# AqAI - Artificial Intelligence Solutions Website

This project is a modern and responsive website design for a company offering artificial intelligence services. It was created using HTML, CSS, and JavaScript for the frontend, and Python Flask for the backend.

## Features

- Fully responsive design
- Modern and clean user interface
- Real artificial intelligence chat API
- Contact form
- Animated SVG illustrations
- Mobile-friendly navigation
- Flask-based backend API

## File Structure

```
AqAI/
├── index.html          # Main HTML file
├── static/             # Static files
│   ├── css/            # CSS styles
│   ├── js/             # JavaScript files
│   └── img/            # Images and illustrations
├── ai/                 # Backend folder
│   ├── app.py          # Flask API application
│   ├── model.py        # AI model
│   ├── requirements.txt # Python dependencies
│   ├── data/           # Data folder
│   └── README.md       # Backend README file
└── README.md           # This file
```

## Installation

### Frontend

1. Clone this repository or download it as a ZIP
2. Upload the files to a web server or open `index.html` directly in a browser

### Backend

1. Make sure Python 3.8 or higher is installed
2. Go to the `ai` folder
3. Install the required dependencies:
```bash
pip install -r requirements.txt
```
4. Start the backend server:
```bash
python app.py
```
5. The backend API will run at http://localhost:5000

## Usage

The website consists of the following sections:

- **Home**: Company introduction and call-to-action button
- **Services**: List of AI services offered (dynamically loaded from the API)
- **About Us**: Information about the company
- **Demo**: Interactive AI chat demo (works with the Backend API)
- **Contact**: Contact form and contact information (works with the Backend API)

## Customization

### Frontend

- Change the color variables in the `static/css/style.css` file
- Update the texts and images in the `index.html` file

### Backend

- Customize the AI model in the `ai/model.py` file
- Create a `ai/data/responses.json` file to add custom responses

## API Endpoints

The backend API provides the following endpoints:

- **POST /api/chat**: AI chat API
- **GET /api/services**: Services list API
- **POST /api/contact**: Contact form API

For more information, see the `ai/README.md` file.

## Technologies

### Frontend
- HTML5
- CSS3 (Flexbox and Grid)
- JavaScript (ES6+)
- SVG Animations
- Font Awesome icons

### Backend
- Python 3.8+
- Flask
- Flask-CORS

## License

This project is licensed under the MIT License.

## Contact

For questions or feedback: Discord: aqwoz
