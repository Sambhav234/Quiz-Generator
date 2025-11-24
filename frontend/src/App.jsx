import React, { useState, useEffect } from 'react'
import axios from 'axios'
import './App.css'

const API_URL = 'http://localhost:5000/api'

function App() {
  const [activeTab, setActiveTab] = useState('news') // 'news' or 'papers'
  const [newsArticles, setNewsArticles] = useState([])
  const [researchPapers, setResearchPapers] = useState([])
  const [selectedArticle, setSelectedArticle] = useState(null)
  const [selectedPaper, setSelectedPaper] = useState(null)
  const [quizQuestions, setQuizQuestions] = useState([])
  const [quizAnswers, setQuizAnswers] = useState({})
  const [quizResults, setQuizResults] = useState(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)
  const [searchQuery, setSearchQuery] = useState('machine learning')

  // Fetch news articles
  const fetchNews = async (category = 'technology') => {
    setLoading(true)
    setError(null)
    try {
      const response = await axios.get(`${API_URL}/news`, {
        params: { category, limit: 10 }
      })
      setNewsArticles(response.data.articles || [])
    } catch (err) {
      setError('Failed to fetch news. Using fallback RSS feeds.')
      console.error(err)
    } finally {
      setLoading(false)
    }
  }

  // Fetch research papers
  const fetchPapers = async (query = 'machine learning') => {
    setLoading(true)
    setError(null)
    try {
      const response = await axios.get(`${API_URL}/papers`, {
        params: { query, limit: 10 }
      })
      setResearchPapers(response.data.papers || [])
    } catch (err) {
      setError('Failed to fetch research papers.')
      console.error(err)
    } finally {
      setLoading(false)
    }
  }

  // Generate quiz from news article
  const generateQuizFromNews = async (article, numQuestions = 5) => {
    setLoading(true)
    setError(null)
    try {
      const response = await axios.post(`${API_URL}/generate-from-news`, {
        article_id: newsArticles.indexOf(article),
        category: 'technology',
        num_questions: numQuestions
      })
      setQuizQuestions(response.data.questions || [])
      setQuizAnswers({})
      setQuizResults(null)
    } catch (err) {
      setError('Failed to generate quiz. ' + (err.response?.data?.error || err.message))
      console.error(err)
    } finally {
      setLoading(false)
    }
  }

  // Generate quiz from research paper
  const generateQuizFromPaper = async (paper, numQuestions = 5) => {
    setLoading(true)
    setError(null)
    try {
      const response = await axios.post(`${API_URL}/generate-from-paper`, {
        query: searchQuery,
        paper_index: researchPapers.indexOf(paper),
        num_questions: numQuestions
      })
      setQuizQuestions(response.data.questions || [])
      setQuizAnswers({})
      setQuizResults(null)
    } catch (err) {
      setError('Failed to generate quiz. ' + (err.response?.data?.error || err.message))
      console.error(err)
    } finally {
      setLoading(false)
    }
  }

  // Submit quiz
  const submitQuiz = async () => {
    if (quizQuestions.length === 0) return

    setLoading(true)
    try {
      const answers = quizQuestions.map((q, idx) => quizAnswers[idx] || '')
      const response = await axios.post(`${API_URL}/submit-quiz`, {
        questions: quizQuestions,
        answers: answers
      })
      setQuizResults(response.data)
    } catch (err) {
      setError('Failed to submit quiz.')
      console.error(err)
    } finally {
      setLoading(false)
    }
  }

  // Load data on tab change
  useEffect(() => {
    if (activeTab === 'news') {
      fetchNews()
    } else {
      fetchPapers(searchQuery)
    }
  }, [activeTab, searchQuery])

  const handleAnswerChange = (questionIndex, answer) => {
    setQuizAnswers(prev => ({
      ...prev,
      [questionIndex]: answer
    }))
  }

  return (
    <div className="app">
      <div className="container">
        <header className="header">
          <h1>🧠 AI-Powered Quiz Generator</h1>
          <p>Generate authentic quizzes from latest news and research papers</p>
        </header>

        <div className="tabs">
          <button
            className={`tab ${activeTab === 'news' ? 'active' : ''}`}
            onClick={() => setActiveTab('news')}
          >
            📰 Latest News
          </button>
          <button
            className={`tab ${activeTab === 'papers' ? 'active' : ''}`}
            onClick={() => setActiveTab('papers')}
          >
            📚 Research Papers
          </button>
        </div>

        {activeTab === 'papers' && (
          <div className="search-bar">
            <input
              type="text"
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              placeholder="Search research papers (e.g., 'artificial intelligence', 'quantum computing')"
              className="search-input"
            />
            <button onClick={() => fetchPapers(searchQuery)} className="search-btn">
              🔍 Search
            </button>
          </div>
        )}

        {error && (
          <div className="error-message">
            ⚠️ {error}
          </div>
        )}

        {loading && (
          <div className="loading">
            <div className="spinner"></div>
            <p>Loading...</p>
          </div>
        )}

        {!loading && (
          <div className="content-grid">
            {/* Source Content */}
            <div className="source-section">
              <h2>{activeTab === 'news' ? '📰 News Articles' : '📚 Research Papers'}</h2>
              <div className="source-list">
                {activeTab === 'news' ? (
                  newsArticles.map((article, idx) => (
                    <div
                      key={idx}
                      className={`source-item ${selectedArticle === article ? 'selected' : ''}`}
                      onClick={() => setSelectedArticle(article)}
                    >
                      <h3>{article.title}</h3>
                      <p className="source-meta">
                        {article.source} • {new Date(article.publishedAt).toLocaleDateString()}
                      </p>
                      <p className="source-preview">{article.description || article.content?.substring(0, 150)}...</p>
                      <button
                        className="generate-btn"
                        onClick={(e) => {
                          e.stopPropagation()
                          generateQuizFromNews(article)
                        }}
                      >
                        Generate Quiz
                      </button>
                    </div>
                  ))
                ) : (
                  researchPapers.map((paper, idx) => (
                    <div
                      key={idx}
                      className={`source-item ${selectedPaper === paper ? 'selected' : ''}`}
                      onClick={() => setSelectedPaper(paper)}
                    >
                      <h3>{paper.title}</h3>
                      <p className="source-meta">
                        {paper.authors?.join(', ')} • {new Date(paper.published).toLocaleDateString()}
                      </p>
                      <p className="source-preview">{paper.abstract?.substring(0, 200)}...</p>
                      <button
                        className="generate-btn"
                        onClick={(e) => {
                          e.stopPropagation()
                          generateQuizFromPaper(paper)
                        }}
                      >
                        Generate Quiz
                      </button>
                    </div>
                  ))
                )}
              </div>
            </div>

            {/* Quiz Section */}
            <div className="quiz-section">
              <h2>📝 Generated Quiz</h2>
              {quizQuestions.length === 0 ? (
                <div className="empty-state">
                  <p>Select a news article or research paper to generate a quiz</p>
                </div>
              ) : (
                <>
                  <div className="quiz-questions">
                    {quizQuestions.map((question, idx) => (
                      <div key={idx} className="question-card">
                        <div className="question-header">
                          <span className="question-number">Question {idx + 1}</span>
                          <span className="question-type">{question.type}</span>
                        </div>
                        <h3 className="question-text">{question.question}</h3>

                        {question.type === 'multiple_choice' ? (
                          <div className="options">
                            {question.options?.map((option, optIdx) => (
                              <label key={optIdx} className="option-label">
                                <input
                                  type="radio"
                                  name={`question-${idx}`}
                                  value={option}
                                  checked={quizAnswers[idx] === option}
                                  onChange={() => handleAnswerChange(idx, option)}
                                  disabled={quizResults !== null}
                                />
                                <span>{option}</span>
                              </label>
                            ))}
                          </div>
                        ) : (
                          <div className="options">
                            <label className="option-label">
                              <input
                                type="radio"
                                name={`question-${idx}`}
                                value="true"
                                checked={quizAnswers[idx] === 'true'}
                                onChange={() => handleAnswerChange(idx, 'true')}
                                disabled={quizResults !== null}
                              />
                              <span>True</span>
                            </label>
                            <label className="option-label">
                              <input
                                type="radio"
                                name={`question-${idx}`}
                                value="false"
                                checked={quizAnswers[idx] === 'false'}
                                onChange={() => handleAnswerChange(idx, 'false')}
                                disabled={quizResults !== null}
                              />
                              <span>False</span>
                            </label>
                          </div>
                        )}

                        {quizResults && (
                          <div className={`answer-feedback ${quizResults.results[idx]?.is_correct ? 'correct' : 'incorrect'}`}>
                            <p>
                              <strong>
                                {quizResults.results[idx]?.is_correct ? '✅ Correct!' : '❌ Incorrect'}
                              </strong>
                            </p>
                            <p>Correct answer: {quizResults.results[idx]?.correct_answer}</p>
                            <p className="explanation">{quizResults.results[idx]?.explanation}</p>
                          </div>
                        )}
                      </div>
                    ))}
                  </div>

                  {!quizResults && (
                    <button className="submit-btn" onClick={submitQuiz}>
                      Submit Quiz
                    </button>
                  )}

                  {quizResults && (
                    <div className="quiz-results">
                      <h3>Quiz Results</h3>
                      <div className="score-display">
                        <div className="score-circle">
                          <span className="score-value">{quizResults.score}%</span>
                        </div>
                        <p className="score-text">
                          You got {quizResults.correct} out of {quizResults.total} questions correct!
                        </p>
                      </div>
                      <button
                        className="reset-btn"
                        onClick={() => {
                          setQuizQuestions([])
                          setQuizAnswers({})
                          setQuizResults(null)
                        }}
                      >
                        Generate New Quiz
                      </button>
                    </div>
                  )}
                </>
              )}
            </div>
          </div>
        )}
      </div>
    </div>
  )
}

export default App

