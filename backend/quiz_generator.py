"""
Enhanced Quiz Generator with better NLP techniques
"""
import re
import random
from typing import List, Dict, Tuple
import nltk
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
from nltk.tag import pos_tag

# Download required NLTK data
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt', quiet=True)

try:
    nltk.data.find('corpora/stopwords')
except LookupError:
    nltk.download('stopwords', quiet=True)

try:
    nltk.data.find('taggers/averaged_perceptron_tagger')
except LookupError:
    nltk.download('averaged_perceptron_tagger', quiet=True)


class EnhancedQuizGenerator:
    """Enhanced quiz generator with better NLP processing"""
    
    def __init__(self):
        self.stop_words = set(stopwords.words('english'))
    
    def extract_key_sentences(self, text: str, max_sentences: int = 15) -> List[str]:
        """Extract key sentences that are good for quiz questions"""
        sentences = sent_tokenize(text)
        scored_sentences = []
        
        for sentence in sentences:
            if len(sentence) < 20:  # Skip very short sentences
                continue
            
            score = 0
            
            # Score based on important patterns
            patterns = {
                r'\d+\.?\d*': 3,  # Numbers
                r'\b(?:percent|million|billion|thousand|hundred)\b': 2,  # Quantities
                r'\b(?:January|February|March|April|May|June|July|August|September|October|November|December)\b': 2,  # Dates
                r'\b(?:according to|study shows|research indicates|findings suggest)\b': 2,  # Research language
                r'[A-Z][a-z]+ [A-Z][a-z]+': 1,  # Proper nouns
                r'\b(?:increased|decreased|improved|reduced|discovered|found)\b': 1,  # Action verbs
            }
            
            for pattern, points in patterns.items():
                if re.search(pattern, sentence, re.IGNORECASE):
                    score += points
            
            # Prefer sentences with specific information
            words = word_tokenize(sentence.lower())
            content_words = [w for w in words if w not in self.stop_words and w.isalnum()]
            if len(content_words) > 5:  # Substantial content
                score += 1
            
            scored_sentences.append((sentence, score))
        
        # Sort by score and return top sentences
        scored_sentences.sort(key=lambda x: x[1], reverse=True)
        return [s[0] for s in scored_sentences[:max_sentences]]
    
    def extract_key_terms(self, sentence: str) -> List[Tuple[str, str]]:
        """Extract key terms that could be answers (noun phrases, numbers, etc.)"""
        key_terms = []
        
        # Extract numbers
        numbers = re.findall(r'\d+\.?\d*', sentence)
        for num in numbers:
            key_terms.append((num, 'number'))
        
        # Extract proper nouns (capitalized words)
        words = word_tokenize(sentence)
        tagged = pos_tag(words)
        
        # Find noun phrases
        for i, (word, tag) in enumerate(tagged):
            if tag in ['NNP', 'NNPS'] and len(word) > 2:  # Proper nouns
                key_terms.append((word, 'proper_noun'))
            elif tag in ['CD']:  # Cardinal numbers
                if word not in [t[0] for t in key_terms]:
                    key_terms.append((word, 'number'))
        
        return key_terms
    
    def generate_multiple_choice(self, sentence: str, context: str) -> Dict:
        """Generate a multiple choice question"""
        key_terms = self.extract_key_terms(sentence)
        
        if not key_terms:
            return None
        
        # Use the first significant key term as answer
        answer_term, term_type = key_terms[0]
        
        # Create question by replacing answer with blank
        question_text = sentence.replace(answer_term, "_____", 1)
        
        # If no replacement happened, create a question
        if "_____" not in question_text:
            # Try to create a "what" or "which" question
            if term_type == 'number':
                question_text = f"According to the text, what is the number mentioned: {sentence}?"
            else:
                question_text = f"According to the text, {sentence.lower()}?"
        
        # Generate distractors
        options = [answer_term]
        
        if term_type == 'number':
            base_num = float(re.findall(r'\d+\.?\d*', answer_term)[0])
            distractors = [
                str(int(base_num * 0.5)),
                str(int(base_num * 1.5)),
                str(int(base_num * 2)),
                str(int(base_num * 0.8))
            ]
            # Remove duplicates and keep 3 unique ones
            distractors = [d for d in distractors if d != answer_term][:3]
            options.extend(distractors)
        else:
            # For text answers, create generic distractors
            options.extend([
                "Not mentioned in the text",
                "All of the above",
                "None of the above"
            ])
        
        # Shuffle options but keep track of correct answer index
        correct_index = options.index(answer_term)
        random.shuffle(options)
        correct_answer = options[correct_index]
        
        return {
            'type': 'multiple_choice',
            'question': question_text,
            'options': options,
            'correct_answer': correct_answer,
            'explanation': sentence
        }
    
    def generate_true_false(self, sentence: str) -> Dict:
        """Generate a true/false question"""
        # Create a statement
        statement = sentence.strip()
        
        # Sometimes create a false statement by negating
        if random.random() > 0.5:
            # Create false statement
            false_statement = statement
            
            # Try to negate common verbs
            negations = {
                'is': 'is not',
                'are': 'are not',
                'was': 'was not',
                'were': 'were not',
                'has': 'does not have',
                'have': 'do not have',
                'increased': 'decreased',
                'decreased': 'increased',
                'improved': 'worsened',
                'found': 'did not find'
            }
            
            for word, replacement in negations.items():
                if word in false_statement.lower():
                    false_statement = re.sub(
                        r'\b' + word + r'\b',
                        replacement,
                        false_statement,
                        flags=re.IGNORECASE
                    )
                    break
            
            return {
                'type': 'true_false',
                'question': f"True or False: {false_statement}",
                'correct_answer': False,
                'explanation': f"The correct statement is: {statement}"
            }
        else:
            return {
                'type': 'true_false',
                'question': f"True or False: {statement}",
                'correct_answer': True,
                'explanation': statement
            }
    
    def generate_fill_blank(self, sentence: str) -> Dict:
        """Generate a fill-in-the-blank question"""
        key_terms = self.extract_key_terms(sentence)
        
        if not key_terms:
            return None
        
        answer_term = key_terms[0][0]
        question_text = sentence.replace(answer_term, "_____", 1)
        
        if "_____" not in question_text:
            return None
        
        return {
            'type': 'fill_blank',
            'question': question_text,
            'correct_answer': answer_term,
            'explanation': sentence
        }
    
    def generate_questions(self, text: str, num_questions: int = 5) -> List[Dict]:
        """Generate quiz questions from text"""
        key_sentences = self.extract_key_sentences(text, max_sentences=num_questions * 3)
        
        if not key_sentences:
            return []
        
        questions = []
        question_types = ['multiple_choice', 'true_false', 'fill_blank']
        
        for sentence in key_sentences[:num_questions * 2]:
            if len(questions) >= num_questions:
                break
            
            # Randomly choose question type
            q_type = random.choice(question_types)
            
            question = None
            if q_type == 'multiple_choice':
                question = self.generate_multiple_choice(sentence, text)
            elif q_type == 'true_false':
                question = self.generate_true_false(sentence)
            elif q_type == 'fill_blank':
                question = self.generate_fill_blank(sentence)
            
            if question:
                questions.append(question)
        
        return questions[:num_questions]

