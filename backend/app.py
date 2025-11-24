from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import feedparser
from datetime import datetime, timedelta
import re
import random
from typing import List, Dict
import json
import os
from dotenv import load_dotenv
from quiz_generator import EnhancedQuizGenerator

# Load environment variables
load_dotenv()

app = Flask(__name__)
CORS(app)

# News API configuration (using free NewsAPI)
NEWS_API_KEY = os.getenv('NEWS_API_KEY', '')  # Get free key from https://newsapi.org/
NEWS_API_URL = "https://newsapi.org/v2/top-headlines"

# arXiv API
ARXIV_API_URL = "http://export.arxiv.org/api/query"

# Initialize enhanced quiz generator
quiz_generator = EnhancedQuizGenerator()

def fetch_latest_news(category: str = "technology", num_articles: int = 5) -> List[Dict]:
    """Fetch latest news articles"""
    try:
        # Using NewsAPI if key is available
        if NEWS_API_KEY and NEWS_API_KEY != 'YOUR_NEWS_API_KEY':
            params = {
                'apiKey': NEWS_API_KEY,
                'category': category,
                'pageSize': num_articles,
                'country': 'us'
            }
            
            response = requests.get(NEWS_API_URL, params=params, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                articles = []
                for article in data.get('articles', []):
                    articles.append({
                        'title': article.get('title', ''),
                        'description': article.get('description', ''),
                        'content': article.get('content', '') or article.get('description', ''),
                        'url': article.get('url', ''),
                        'publishedAt': article.get('publishedAt', ''),
                        'source': article.get('source', {}).get('name', 'Unknown')
                    })
                return articles
        
        # Fallback: Use RSS feeds
        return fetch_news_rss(category, num_articles)
    except Exception as e:
        print(f"Error fetching news: {e}")
        return fetch_news_rss(category, num_articles)

def fetch_news_rss(category: str = "technology", num_articles: int = 5) -> List[Dict]:
    """Fetch news from RSS feeds (fallback)"""
    rss_feeds = {
        'technology': 'https://feeds.feedburner.com/oreilly/radar',
        'science': 'https://rss.cnn.com/rss/edition.rss',
        'general': 'https://feeds.bbci.co.uk/news/rss.xml'
    }
    
    feed_url = rss_feeds.get(category, rss_feeds['general'])
    
    try:
        feed = feedparser.parse(feed_url)
        articles = []
        for entry in feed.entries[:num_articles]:
            articles.append({
                'title': entry.get('title', ''),
                'description': entry.get('summary', ''),
                'content': entry.get('summary', ''),
                'url': entry.get('link', ''),
                'publishedAt': entry.get('published', ''),
                'source': 'RSS Feed'
            })
        return articles
    except Exception as e:
        print(f"Error fetching RSS: {e}")
        return []

def fetch_research_papers(query: str = "machine learning", max_results: int = 5) -> List[Dict]:
    """Fetch research papers from arXiv"""
    try:
        params = {
            'search_query': f'all:{query}',
            'start': 0,
            'max_results': max_results,
            'sortBy': 'submittedDate',
            'sortOrder': 'descending'
        }
        
        response = requests.get(ARXIV_API_URL, params=params, timeout=15)
        
        if response.status_code == 200:
            feed = feedparser.parse(response.text)
            papers = []
            
            for entry in feed.entries:
                # Extract abstract
                summary = entry.get('summary', '')
                # Clean HTML tags
                summary = re.sub(r'<[^>]+>', '', summary)
                
                papers.append({
                    'id': entry.get('id', '').split('/')[-1],
                    'title': entry.get('title', ''),
                    'abstract': summary,
                    'authors': [author.get('name', '') for author in entry.get('authors', [])],
                    'published': entry.get('published', ''),
                    'url': entry.get('link', ''),
                    'categories': [tag.get('term', '') for tag in entry.get('tags', [])]
                })
            
            return papers
        else:
            return []
    except Exception as e:
        print(f"Error fetching papers: {e}")
        return []

@app.route('/api/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({'status': 'ok', 'message': 'Quiz Generation API is running'})

@app.route('/api/news', methods=['GET'])
def get_news():
    """Fetch latest news articles"""
    category = request.args.get('category', 'technology')
    num_articles = int(request.args.get('limit', 5))
    
    articles = fetch_latest_news(category, num_articles)
    return jsonify({
        'success': True,
        'articles': articles,
        'count': len(articles)
    })

@app.route('/api/papers', methods=['GET'])
def get_papers():
    """Fetch research papers from arXiv"""
    query = request.args.get('query', 'machine learning')
    max_results = int(request.args.get('limit', 5))
    
    papers = fetch_research_papers(query, max_results)
    return jsonify({
        'success': True,
        'papers': papers,
        'count': len(papers)
    })

@app.route('/api/generate-quiz', methods=['POST'])
def generate_quiz():
    """Generate quiz questions from provided content"""
    try:
        data = request.get_json()
        content_type = data.get('type', 'news')  # 'news' or 'paper'
        source_id = data.get('source_id')
        num_questions = int(data.get('num_questions', 5))
        content_text = data.get('content', '')
        
        if not content_text:
            return jsonify({'error': 'No content provided'}), 400
        
        # Generate questions
        questions = quiz_generator.generate_questions(content_text, num_questions)
        
        return jsonify({
            'success': True,
            'questions': questions,
            'count': len(questions),
            'source_type': content_type,
            'source_id': source_id
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/generate-from-news', methods=['POST'])
def generate_from_news():
    """Generate quiz from a news article"""
    try:
        data = request.get_json()
        article_id = data.get('article_id')
        category = data.get('category', 'technology')
        num_questions = int(data.get('num_questions', 5))
        
        # Fetch news
        articles = fetch_latest_news(category, 10)
        
        if not articles:
            return jsonify({'error': 'No news articles found'}), 404
        
        # Use specific article or first one
        article = articles[0] if not article_id else next(
            (a for i, a in enumerate(articles) if i == article_id), articles[0]
        )
        
        # Combine title and content
        content = f"{article['title']}. {article['content']}"
        
        # Generate questions
        questions = quiz_generator.generate_questions(content, num_questions)
        
        return jsonify({
            'success': True,
            'article': article,
            'questions': questions,
            'count': len(questions)
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/generate-from-paper', methods=['POST'])
def generate_from_paper():
    """Generate quiz from a research paper"""
    try:
        data = request.get_json()
        query = data.get('query', 'machine learning')
        paper_index = data.get('paper_index', 0)
        num_questions = int(data.get('num_questions', 5))
        
        # Fetch papers
        papers = fetch_research_papers(query, 10)
        
        if not papers:
            return jsonify({'error': 'No research papers found'}), 404
        
        # Use specific paper
        paper = papers[paper_index] if paper_index < len(papers) else papers[0]
        
        # Use title and abstract
        content = f"{paper['title']}. {paper['abstract']}"
        
        # Generate questions
        questions = quiz_generator.generate_questions(content, num_questions)
        
        return jsonify({
            'success': True,
            'paper': paper,
            'questions': questions,
            'count': len(questions)
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/submit-quiz', methods=['POST'])
def submit_quiz():
    """Submit quiz answers and get results"""
    try:
        data = request.get_json()
        answers = data.get('answers', [])
        questions = data.get('questions', [])
        
        if len(answers) != len(questions):
            return jsonify({'error': 'Answers count mismatch'}), 400
        
        # Calculate score
        correct = 0
        results = []
        
        for i, (question, answer) in enumerate(zip(questions, answers)):
            correct_answer = question.get('correct_answer')
            is_correct = str(answer).lower() == str(correct_answer).lower()
            
            if is_correct:
                correct += 1
            
            results.append({
                'question_index': i,
                'question': question.get('question'),
                'your_answer': answer,
                'correct_answer': correct_answer,
                'is_correct': is_correct,
                'explanation': question.get('explanation', '')
            })
        
        score = (correct / len(questions)) * 100 if questions else 0
        
        return jsonify({
            'success': True,
            'score': round(score, 2),
            'correct': correct,
            'total': len(questions),
            'results': results
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    print("🚀 Starting Quiz Generation API...")
    print("   API will be available at http://localhost:5000")
    print("   Note: For NewsAPI, get a free key from https://newsapi.org/")
    app.run(host='0.0.0.0', port=5000, debug=True)

