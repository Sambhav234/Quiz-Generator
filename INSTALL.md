# Installation Guide

## 📦 Step-by-Step Installation

### 1. Backend Setup

```bash
# Navigate to backend directory
cd QUIZ_GENERATION_NLP/backend

# Install Python dependencies
pip install -r requirements.txt

# NLTK will download required data automatically on first run
```

### 2. Frontend Setup

```bash
# Navigate to frontend directory
cd ../frontend

# Install Node.js dependencies
npm install
```

### 3. (Optional) News API Key

1. Visit https://newsapi.org/
2. Sign up for a free account
3. Get your API key
4. Create `.env` file in `backend/` directory:
   ```
   NEWS_API_KEY=your_api_key_here
   ```

**Note:** The app works without API key using RSS feeds as fallback.

## 🚀 Running the Application

### Terminal 1 - Backend
```bash
cd QUIZ_GENERATION_NLP/backend
python app.py
```

### Terminal 2 - Frontend
```bash
cd QUIZ_GENERATION_NLP/frontend
npm run dev
```

### Open Browser
Navigate to: **http://localhost:3000**

## ✅ Verification

Test if backend is running:
```bash
curl http://localhost:5000/api/health
```

Should return: `{"status":"ok","message":"Quiz Generation API is running"}`

## 🎉 You're Ready!

The application is now running and ready to generate quizzes from news and research papers!

