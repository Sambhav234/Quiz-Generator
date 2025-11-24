# Quick Start Guide - Quiz Generation System

## 🚀 Get Started in 3 Steps

### Step 1: Install Backend Dependencies
```bash
cd QUIZ_GENERATION_NLP/backend
pip install -r requirements.txt
```

### Step 2: Install Frontend Dependencies
```bash
cd ../frontend
npm install
```

### Step 3: Run Both Servers

**Terminal 1 - Backend:**
```bash
cd QUIZ_GENERATION_NLP/backend
python app.py
```

**Terminal 2 - Frontend:**
```bash
cd QUIZ_GENERATION_NLP/frontend
npm run dev
```

### Step 4: Open Browser
Navigate to: **http://localhost:3000**

## ✅ That's It!

The app works without any API keys - it uses RSS feeds as fallback for news.

For better news quality, get a free NewsAPI key from https://newsapi.org/ and add it to `backend/.env`:
```
NEWS_API_KEY=your_key_here
```

## 🎯 How to Use

1. Click on "Latest News" or "Research Papers" tab
2. Browse articles/papers
3. Click "Generate Quiz" on any item
4. Answer the questions
5. Submit to see your score!

Enjoy! 🎉

