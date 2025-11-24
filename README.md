# AI-Powered Quiz Generation System

An intelligent quiz generation system that creates authentic quizzes from latest news articles and research papers using NLP techniques.

## 🎯 Features

- 📰 **Latest News Integration** - Fetch trending news from multiple sources
- 📚 **Research Paper Access** - Pull papers from arXiv API
- 🧠 **AI-Powered Question Generation** - Generate multiple choice and true/false questions
- ✅ **Authentic Quizzes** - Questions aligned with source content
- 📊 **Quiz Results** - Detailed feedback and scoring
- 🎨 **Modern UI** - Beautiful, responsive web interface

## 🏗️ Project Structure

```
QUIZ_GENERATION_NLP/
├── backend/
│   ├── app.py              # Flask API server
│   ├── requirements.txt    # Python dependencies
│   └── .env.example       # Environment variables template
├── frontend/
│   ├── src/
│   │   ├── App.jsx        # Main React component
│   │   ├── App.css        # Styles
│   │   └── main.jsx       # Entry point
│   ├── package.json        # Node dependencies
│   └── vite.config.js     # Vite configuration
└── README.md              # This file
```

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- Node.js 16 or higher
- npm or yarn
- (Optional) NewsAPI key from https://newsapi.org/ (free tier available)

### Installation

#### 1. Backend Setup

```bash
cd QUIZ_GENERATION_NLP/backend
pip install -r requirements.txt
```

#### 2. Frontend Setup

```bash
cd QUIZ_GENERATION_NLP/frontend
npm install
```

#### 3. (Optional) Configure News API

1. Get a free API key from https://newsapi.org/
2. Copy `.env.example` to `.env`
3. Add your API key:
   ```
   NEWS_API_KEY=your_api_key_here
   ```

**Note:** The app works without NewsAPI key using RSS feeds as fallback.

### Running the Application

#### Start Backend (Terminal 1)

```bash
cd QUIZ_GENERATION_NLP/backend
python app.py
```

The API will be available at `http://localhost:5000`

#### Start Frontend (Terminal 2)

```bash
cd QUIZ_GENERATION_NLP/frontend
npm run dev
```

The frontend will be available at `http://localhost:3000`

## 📖 Usage

1. **Open the application** in your browser at `http://localhost:3000`

2. **Choose a source:**
   - **Latest News**: Browse trending news articles
   - **Research Papers**: Search arXiv for papers on any topic

3. **Generate Quiz:**
   - Click "Generate Quiz" on any article or paper
   - Questions are automatically generated using NLP

4. **Take the Quiz:**
   - Answer all questions
   - Click "Submit Quiz" to see your results

5. **View Results:**
   - See your score and detailed feedback
   - Review correct answers and explanations

## 🔧 API Endpoints

### `GET /api/health`
Health check endpoint.

### `GET /api/news`
Fetch latest news articles.
- Query params: `category` (default: 'technology'), `limit` (default: 5)

### `GET /api/papers`
Fetch research papers from arXiv.
- Query params: `query` (default: 'machine learning'), `limit` (default: 5)

### `POST /api/generate-from-news`
Generate quiz from a news article.
- Body: `{ "article_id": 0, "category": "technology", "num_questions": 5 }`

### `POST /api/generate-from-paper`
Generate quiz from a research paper.
- Body: `{ "query": "machine learning", "paper_index": 0, "num_questions": 5 }`

### `POST /api/submit-quiz`
Submit quiz answers and get results.
- Body: `{ "questions": [...], "answers": [...] }`

## 🧠 How It Works

1. **Content Extraction**: Fetches news articles or research papers
2. **Key Fact Extraction**: Uses NLP to identify important facts and information
3. **Question Generation**: Creates multiple choice and true/false questions
4. **Answer Validation**: Checks answers against source content
5. **Feedback**: Provides explanations based on original content

## 🛠️ Technologies Used

- **Backend**: Flask, Requests, Feedparser, NLTK
- **Frontend**: React, Vite, Axios
- **APIs**: NewsAPI, arXiv API
- **NLP**: Pattern matching, sentence extraction, fact identification

## 📝 Future Enhancements

- [ ] Integration with OpenAI/LLM for better question generation
- [ ] Support for more question types (fill-in-the-blank, short answer)
- [ ] Difficulty level selection
- [ ] Quiz history and statistics
- [ ] Export quizzes to PDF
- [ ] Multi-language support
- [ ] User authentication and saved quizzes

## 🐛 Troubleshooting

**Backend won't start:**
- Check if port 5000 is available
- Verify all Python packages are installed
- Check for any import errors

**Frontend won't start:**
- Check if port 3000 is available
- Run `npm install` again
- Clear node_modules and reinstall

**No news/articles:**
- Check internet connection
- Verify NewsAPI key if using (optional)
- App will fallback to RSS feeds

**Quiz generation fails:**
- Ensure content is available
- Check backend logs for errors
- Try with different article/paper

## 📄 License

This project is open source and available for educational purposes.

## 🤝 Contributing

Feel free to submit issues, fork the repository, and create pull requests!

