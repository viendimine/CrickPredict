# 🏏 CrickPredict — Live Cricket Match Tracking & Predictions

CrickPredict is a **Django-based cricket match tracking web application** that provides **real-time match updates, scorecards, and series details**.  
Inspired by platforms like **Cricbuzz** and **ESPNcricinfo**, it offers a **clean, modern UI** and **powerful API integrations** to deliver accurate, live cricket data.

---

## 🚀 Features
- **Live Match Updates** — Real-time scores, overs, wickets, and commentary  
- **Series-Wise Match Listing** — Browse completed, live, and upcoming matches  
- **Dynamic API Integration** — Fetches live data from CricketData API  
- **Responsive UI** — Tailwind CSS design for mobile & desktop  
- **Search & Filter** — Quickly find matches by team, series, or date  
- **Optimized Performance** — API rate-limit handling & caching  

---

## 🛠️ Tech Stack
- **Backend:** Django 5  
- **Frontend:** Tailwind CSS, HTML, JavaScript  
- **API:** CricketData API  
- **Database:** SQLite / PostgreSQL  
- **Hosting:** Render / Vercel (Optional)  

---

## 📂 Project Structure
```
CrickPredict/
│── crickpredict/        # Main Django project folder
│── matches/             # App for match listings & scorecards
│── templates/           # HTML templates
│── static/              # CSS, JS, Images
│── manage.py
│── requirements.txt
│── README.md
```

---

## ⚡ Installation & Setup

### 1️⃣ Clone the Repository
```bash
git clone https://github.com/yourusername/CrickPredict.git
cd CrickPredict
```

### 2️⃣ Create Virtual Environment
```bash
python -m venv venv
source venv/bin/activate   # For Mac/Linux
venv\Scripts\activate      # For Windows
```

### 3️⃣ Install Dependencies
```bash
pip install -r requirements.txt
```

### 4️⃣ Set API Key
Create a `.env` file and add:
```env
CRICKETDATA_API_KEY=your_api_key_here
```

### 5️⃣ Run Server
```bash
python manage.py runserver
```

---

## 📸 Screenshots
- **Live Matches View**  
- **Scorecard View**
