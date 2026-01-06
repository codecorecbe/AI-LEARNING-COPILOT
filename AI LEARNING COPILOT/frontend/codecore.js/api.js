/**
 * CodeCore AI Backend API Client
 * Connects frontend to FastAPI backend with Google Gemini AI
 * 
 * Usage:
 *   const response = await apiClient.generateContent('Python');
 *   const questions = await apiClient.generateQuestions('Python', 'Functions', 5);
 *   const quiz = await apiClient.generateQuiz('JavaScript', 10, 'medium');
 *   const answer = await apiClient.answerDoubt('What is a variable?', 'Python');
 */

// =====================================================
// CONFIGURATION
// =====================================================

const API_CONFIG = {
    // Backend server URL - MUST match the port your backend is running on
    BASE_URL: 'http://localhost:8000/api',
    
    // Timeout for API requests (milliseconds)
    TIMEOUT: 30000,
    
    // Enable console logging
    DEBUG: true,
    
    // Fallback to algorithmic generation if API fails
    USE_FALLBACK: true
};

// =====================================================
// API CLIENT CLASS
// =====================================================

class APIClient {
    constructor(config = {}) {
        this.config = { ...API_CONFIG, ...config };
        this.baseUrl = this.config.BASE_URL;
        this.timeout = this.config.TIMEOUT;
    }

    /**
     * Make an API request with error handling
     * @private
     */
    async _request(endpoint, method = 'POST', body = null) {
        try {
            if (this.config.DEBUG) {
                console.log(`📡 API Request: ${method} ${endpoint}`);
            }

            const options = {
                method: method,
                headers: {
                    'Content-Type': 'application/json',
                    'Accept': 'application/json'
                }
            };

            if (body) {
                options.body = JSON.stringify(body);
            }

            // Add timeout
            const controller = new AbortController();
            const timeoutId = setTimeout(() => controller.abort(), this.timeout);
            options.signal = controller.signal;

            const response = await fetch(`${this.baseUrl}${endpoint}`, options);
            clearTimeout(timeoutId);

            if (!response.ok) {
                const errorData = await response.json().catch(() => ({}));
                throw new Error(
                    errorData.detail?.message || 
                    errorData.message || 
                    `HTTP ${response.status}: ${response.statusText}`
                );
            }

            const data = await response.json();

            if (this.config.DEBUG) {
                console.log(`✅ API Response:`, data);
            }

            return data;

        } catch (error) {
            console.error(`❌ API Error (${endpoint}):`, error.message);
            throw error;
        }
    }

    /**
     * Generate topics and questions for a subject
     * 
     * @param {string} subject - Subject name (e.g., "Python", "JavaScript")
     * @returns {Promise<Object>} - { subject, topics, total_topics, total_questions }
     */
    async generateContent(subject) {
        try {
            if (!subject || subject.trim().length === 0) {
                throw new Error('Subject cannot be empty');
            }

            const response = await this._request('/generate', 'POST', {
                subject: subject.trim()
            });

            return response;

        } catch (error) {
            console.error('Error generating content:', error);
            throw error;
        }
    }

    /**
     * Generate questions for a specific topic
     * 
     * @param {string} subject - Subject name
     * @param {string} topic - Topic name
     * @param {number} count - Number of questions (default: 5)
     * @returns {Promise<Object>} - { success, data: { subject, topic, questions } }
     */
    async generateQuestions(subject, topic, count = 5) {
        try {
            if (!subject || !topic) {
                throw new Error('Subject and topic are required');
            }

            if (count < 1 || count > 20) {
                throw new Error('Count must be between 1 and 20');
            }

            const params = new URLSearchParams({
                subject: subject.trim(),
                topic: topic.trim(),
                count: count
            });

            const response = await this._request(
                `/generate-questions?${params}`,
                'POST'
            );

            return response.data || response;

        } catch (error) {
            console.error('Error generating questions:', error);
            throw error;
        }
    }

    /**
     * Generate a quiz with multiple choice questions
     * 
     * @param {string} topic - Quiz topic
     * @param {number} count - Number of questions (default: 40)
     * @returns {Promise<Object>} - { success, data: { topic, total_questions, questions } }
     */
    async generateQuiz(topic, count = 40) {
        try {
            if (!topic) {
                throw new Error('Topic is required');
            }

            if (count < 1 || count > 50) {
                throw new Error('Count must be between 1 and 50');
            }

            const params = new URLSearchParams({
                topic: topic.trim(),
                count: count
            });

            const response = await this._request(
                `/generate-quiz?${params}`,
                'POST'
            );

            return response;

        } catch (error) {
            console.error('Error generating quiz:', error);
            throw error;
        }
    }

    /**
     * Answer a student's doubt/question
     * 
     * @param {string} question - Student's question
     * @param {string} context - Optional context (e.g., "Python programming")
     * @returns {Promise<Object>} - { success, data: { question, answer, key_points } }
     */
    async answerDoubt(question, context = '') {
        try {
            if (!question || question.trim().length === 0) {
                throw new Error('Question cannot be empty');
            }

            const params = new URLSearchParams({
                question: question.trim(),
                context: context.trim()
            });

            const response = await this._request(
                `/answer-doubt?${params}`,
                'POST'
            );

            return response.data || response;

        } catch (error) {
            console.error('Error answering doubt:', error);
            throw error;
        }
    }

    /**
     * Verify if a student's answer is correct
     * 
     * @param {string} question - The question being answered
     * @param {string} answer - The student's answer
     * @returns {Promise<Object>} - { success, data: { is_correct, feedback } }
     */
    async verifyAnswer(question, answer) {
        try {
            if (!question || question.trim().length === 0) {
                throw new Error('Question cannot be empty');
            }
            if (!answer || answer.trim().length === 0) {
                throw new Error('Answer cannot be empty');
            }

            const params = new URLSearchParams({
                question: question.trim(),
                answer: answer.trim()
            });

            const response = await this._request(
                `/verify-answer?${params}`,
                'POST'
            );

            return response;

        } catch (error) {
            console.error('Error verifying answer:', error);
            throw error;
        }
    }

    /**
     * Check if the API is available
     * @returns {Promise<boolean>} - true if API is available
     */
    async isAvailable() {
        try {
            const response = await fetch(`${this.baseUrl.replace('/api', '')}/health`, {
                method: 'GET',
                timeout: 5000
            });
            return response.ok;
        } catch {
            return false;
        }
    }

    /**
     * Test the API with a simple request
     * @returns {Promise<boolean>} - true if API works
     */
    async testAPI() {
        try {
            const result = await this.generateContent('Test Subject');
            return result && result.topics && result.topics.length > 0;
        } catch {
            return false;
        }
    }
}

// =====================================================
// GLOBAL API CLIENT INSTANCE
// =====================================================

const apiClient = new APIClient();

// =====================================================
// HELPER FUNCTIONS FOR UI
// =====================================================

/**
 * Show loading indicator
 */
function showLoading(message = 'Loading...') {
    const loader = document.getElementById('loading-indicator');
    if (loader) {
        loader.textContent = message;
        loader.style.display = 'block';
    } else {
        // Fallback: show in console
        console.log(`⏳ ${message}`);
    }
}

/**
 * Hide loading indicator
 */
function hideLoading() {
    const loader = document.getElementById('loading-indicator');
    if (loader) {
        loader.style.display = 'none';
    }
}

/**
 * Show error message to user
 */
function showError(message, title = '❌ Error') {
    console.error(`${title}: ${message}`);
    
    // Try to show in modal/toast
    const errorContainer = document.getElementById('error-container');
    if (errorContainer) {
        const errorDiv = document.createElement('div');
        errorDiv.className = 'error-message';
        errorDiv.innerHTML = `
            <strong>${title}</strong><br/>
            ${message}
            <button onclick="this.parentElement.remove()" style="float: right; cursor: pointer;">✕</button>
        `;
        errorContainer.appendChild(errorDiv);
    }
    
    // Fallback: alert
    if (!errorContainer) {
        alert(`${title}: ${message}`);
    }
}

/**
 * Show success message
 */
function showSuccess(message, title = '✅ Success') {
    console.log(`${title}: ${message}`);
    
    const successContainer = document.getElementById('success-container');
    if (successContainer) {
        const successDiv = document.createElement('div');
        successDiv.className = 'success-message';
        successDiv.innerHTML = `
            <strong>${title}</strong><br/>
            ${message}
        `;
        successContainer.appendChild(successDiv);
        
        // Auto-remove after 3 seconds
        setTimeout(() => successDiv.remove(), 3000);
    }
}

// =====================================================
// EXPORT FOR USE IN OTHER FILES
// =====================================================

// For use in HTML with <script src="api.js"></script>
// Access via: apiClient.generateContent(), etc.

// For modules (if using bundler):
// export { apiClient, APIClient, showLoading, hideLoading, showError, showSuccess };
