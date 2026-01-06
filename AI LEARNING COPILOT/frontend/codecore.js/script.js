/* ============================================
   AI-DRIVEN SUBJECTS & TOPICS MANAGEMENT
   Pure Frontend - No Hardcoded Data
   ============================================ */

// Global state management
const AppState = {
    subjects: JSON.parse(localStorage.getItem('subjects')) || [],
    currentSubject: null,
    currentTopic: null
};

// Save state to localStorage
function saveState() {
    localStorage.setItem('subjects', JSON.stringify(AppState.subjects));
}

/* ============================================
   API-ONLY CONFIGURATION
   All content generation via API endpoints
   ============================================ */

/* ============================================
   SUBJECT MANAGEMENT
   ============================================ */

/**
 * Generate a new subject with AI-generated topics (using backend API)
 */
async function generateSubject() {
    const input = document.getElementById('subjectInput');
    const subjectName = input.value.trim();

    if (!subjectName) {
        showError('Please enter a subject name', '⚠️ Warning');
        return;
    }

    // Check if subject already exists
    const existingSubject = AppState.subjects.find(
        s => s.name.toLowerCase() === subjectName.toLowerCase()
    );

    if (existingSubject) {
        showError('This subject already exists!', '⚠️ Info');
        return;
    }

    try {
        // Show loading
        showLoading(`Generating topics for ${subjectName}...`);

        // API-only generation (no fallback)
        const response = await apiClient.generateContent(subjectName);

        // Create subject object with API response
        const newSubject = {
            id: Date.now(),
            name: subjectName,
            topics: response.topics.map((topic, idx) => ({
                id: `topic-${idx}`,
                name: topic.topic,
                questions: topic.questions || []
            })),
            isAI: true,
            createdAt: new Date().toISOString()
        };

        // Add to state
        AppState.subjects.unshift(newSubject);
        saveState();

        // Clear input
        input.value = '';

        // Hide loading
        hideLoading();

        // Render
        renderSubjects();

        // Show success
        showSuccess(
            `✅ Generated ${response.total_topics} topics with ${response.total_questions} questions!`,
            'Success'
        );

    } catch (error) {
        hideLoading();
        console.error('Error generating subject:', error);
        
        // Check for specific API errors
        let errorMessage = '';
        let errorTitle = '❌ Generation Error';
        
        if (error.message.includes('429') || error.message.includes('quota') || error.message.includes('exceeded')) {
            errorMessage = 
                '⚠️ Google Gemini API quota exceeded.\n\n' +
                'The free tier has daily limits. Solutions:\n\n' +
                '1. Wait 24 hours for quota reset\n' +
                '2. Get a new API key from: https://makersuite.google.com/app/apikey\n' +
                '3. Upgrade to paid tier for higher limits\n\n' +
                'Current API key can be changed in backend/.env file';
            errorTitle = '⚠️ API Quota Exceeded';
        } else if (error.message.includes('fetch') || error.message.includes('connection') || error.message.includes('NetworkError')) {
            errorMessage = 
                '🔌 Cannot connect to backend server.\n\n' +
                'Please ensure:\n' +
                '1. Backend is running: cd backend && python -m uvicorn app.main:app --reload\n' +
                '2. Server is accessible at http://127.0.0.1:8000\n' +
                '3. Check terminal for backend errors';
            errorTitle = '🔌 Connection Error';
        } else if (error.message.includes('API key') || error.message.includes('401') || error.message.includes('403')) {
            errorMessage = 
                '🔑 Invalid API key.\n\n' +
                'Please:\n' +
                '1. Get API key from: https://makersuite.google.com/app/apikey\n' +
                '2. Update backend/.env file: GEMINI_API_KEY=your-key-here\n' +
                '3. Restart the backend server';
            errorTitle = '🔑 API Key Error';
        } else {
            errorMessage = 
                `AI Connection Failed: ${error.message}\n\n` +
                'Please ensure:\n' +
                '1. Backend server is running at http://127.0.0.1:8000\n' +
                '2. Internet connection is active\n' +
                '3. Gemini API key is configured in backend/.env';
            errorTitle = '❌ AI Connection Error';
        }
        
        showError(errorMessage, errorTitle);
    }
}



/**
 * Handle Enter key press in subject input
 */
function handleEnterKey(event) {
    if (event.key === 'Enter') {
        generateSubject();
    }
}

/**
 * Delete a subject
 */
function deleteSubject(subjectId) {
    if (confirm('Are you sure you want to delete this subject?')) {
        AppState.subjects = AppState.subjects.filter(s => s.id !== subjectId);
        saveState();
        renderSubjects();
    }
}

/**
 * Navigate to topic questions
 */
function viewTopicQuestions(subjectId, topicId) {
    const subject = AppState.subjects.find(s => s.id === subjectId);
    if (!subject) return;

    const topic = subject.topics.find(t => t.id === topicId);
    if (!topic) return;

    // Store subject and topic info for task page
    // Task page will automatically generate questions via API
    localStorage.setItem('currentTaskData', JSON.stringify({
        subjectId: subjectId,
        topicId: topicId,
        subject: subject.name,
        topic: topic.name,
        questions: topic.questions, // Existing questions as fallback
        needsGeneration: true, // Flag to trigger AI generation
        apiGenerated: false
    }));

    // Navigate to task page
    window.location.href = 'task.html';
}

/* ============================================
   ASYNC API FUNCTIONS
   ============================================ */

/**
 * Render all subjects as cards
 */
function renderSubjects() {
    const container = document.getElementById('subjectsContainer');
    const emptyState = document.getElementById('emptyState');

    if (AppState.subjects.length === 0) {
        container.innerHTML = '';
        emptyState.style.display = 'block';
        return;
    }

    emptyState.style.display = 'none';
    
    container.innerHTML = AppState.subjects.map(subject => `
        <div class="subject-card" data-subject-id="${subject.id}">
            <div class="subject-card-header">
                <h3>${subject.name}</h3>
                <button onclick="deleteSubject(${subject.id})" class="btn-delete" title="Delete subject">
                    ✕
                </button>
            </div>
            <div class="subject-card-body">
                <p class="topic-count">${subject.topics.length} Topics Available</p>
                <div class="topics-list">
                    ${subject.topics.slice(0, 3).map(topic => `
                        <div style="display: flex; gap: 8px; align-items: center; margin-bottom: 8px;">
                            <button 
                                class="topic-item" 
                                onclick="viewTopicQuestions(${subject.id}, '${topic.id}')"
                                style="flex: 1;"
                            >
                                <span class="topic-icon">📚</span>
                                <span class="topic-name">${topic.name}</span>
                                <span class="topic-arrow">→</span>
                            </button>
                            <button 
                                onclick="startQuizForTopic('${topic.name}')"
                                style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; border: none; padding: 8px 16px; border-radius: 8px; cursor: pointer; font-size: 13px; white-space: nowrap;"
                                title="Take quiz on this topic"
                            >
                                🎯 Quiz
                            </button>
                        </div>
                    `).join('')}
                    ${subject.topics.length > 3 ? `
                        <button class="topic-item show-more" onclick="toggleTopics(${subject.id})">
                            <span>Show ${subject.topics.length - 3} more topics...</span>
                        </button>
                    ` : ''}
                </div>
            </div>
            <div class="subject-card-footer">
                <small>Created: ${new Date(subject.createdAt).toLocaleDateString()}</small>
            </div>
        </div>
    `).join('');
}

/**
 * Show/hide loading state
 */
function showLoading(show) {
    const loading = document.getElementById('loadingState');
    const container = document.getElementById('subjectsContainer');
    const loadingText = document.getElementById('loading-text');
    const loadingIndicator = document.getElementById('loading-indicator');
    
    if (typeof show === 'string') {
        // New style: show(message)
        loadingText.textContent = show;
        loadingIndicator.style.display = 'flex';
    } else {
        // Old style: show(boolean)
        if (show) {
            loading && (loading.style.display = 'flex');
            container && (container.style.opacity = '0.5');
        } else {
            loading && (loading.style.display = 'none');
            container && (container.style.opacity = '1');
        }
    }
}

/**
 * Hide loading indicator
 */
function hideLoading() {
    const loadingIndicator = document.getElementById('loading-indicator');
    const loading = document.getElementById('loadingState');
    const container = document.getElementById('subjectsContainer');
    
    loadingIndicator && (loadingIndicator.style.display = 'none');
    loading && (loading.style.display = 'none');
    container && (container.style.opacity = '1');
}

/**
 * Toggle mobile navigation menu
 */
function toggleMobileMenu() {
    const navbar = document.getElementById('navbar');
    navbar.classList.toggle('active');
}

/* ============================================
   TASK PAGE FUNCTIONS
   ============================================ */

/**
 * Load task page with subject, topic, and questions
 */
async function loadTaskPage() {
    const taskData = JSON.parse(localStorage.getItem('currentTaskData') || 'null');
    const emptyState = document.getElementById('taskEmptyState');
    const questionsContainer = document.getElementById('questionsContainer');

    if (!taskData) {
        emptyState.style.display = 'flex';
        questionsContainer.style.display = 'none';
        return;
    }

    emptyState.style.display = 'none';
    questionsContainer.style.display = 'block';

    // Update header
    document.getElementById('currentSubject').textContent = taskData.subject;
    document.getElementById('currentTopic').textContent = taskData.topic;

    // Check if we need to generate questions via AI
    if (taskData.needsGeneration) {
        await generateQuestionsForTopic(taskData);
    } else {
        // Render existing questions
        renderTaskQuestions(taskData.questions);
    }
}

/**
 * Generate questions for a specific topic using AI
 */
async function generateQuestionsForTopic(taskData) {
    const questionsContainer = document.getElementById('questionsContainer');
    
    try {
        showLoading('Generating AI-powered questions for ' + taskData.topic + '...');
        
        // Show loading state in questions container
        questionsContainer.innerHTML = `
            <div class="questions-header">
                <h3>🤖 Generating Questions...</h3>
                <p>AI is creating personalized questions for ${taskData.topic}</p>
            </div>
            <div style="text-align: center; padding: 40px;">
                <div style="border: 4px solid #f3f3f3; border-top: 4px solid #667eea; border-radius: 50%; width: 60px; height: 60px; animation: spin 1s linear infinite; margin: 0 auto 20px;"></div>
                <p>Please wait while we generate high-quality questions...</p>
            </div>
        `;

        // Call API to generate questions
        const response = await apiClient.generateQuestions(
            taskData.subject,
            taskData.topic,
            5 // Generate 5 questions
        );

        hideLoading();

        // Extract questions from response
        let questions = [];
        if (response && response.questions && Array.isArray(response.questions)) {
            questions = response.questions.map(q => ({
                question: typeof q === 'string' ? q : q.question || q.text || String(q)
            }));
        } else if (response && Array.isArray(response)) {
            questions = response.map(q => ({
                question: typeof q === 'string' ? q : q.question || q.text || String(q)
            }));
        } else {
            throw new Error('Invalid response format from API');
        }

        // Update localStorage with generated questions
        taskData.questions = questions;
        taskData.apiGenerated = true;
        taskData.needsGeneration = false;
        localStorage.setItem('currentTaskData', JSON.stringify(taskData));

        // Update the subject's topic questions in AppState
        const subject = AppState.subjects.find(s => s.id === taskData.subjectId);
        if (subject) {
            const topic = subject.topics.find(t => t.id === taskData.topicId);
            if (topic) {
                topic.questions = questions;
                saveState();
            }
        }

        // Render the questions
        renderTaskQuestions(questions);
        
        showSuccess(
            `Generated ${questions.length} AI-powered questions for ${taskData.topic}!`,
            'Success'
        );

    } catch (error) {
        hideLoading();
        console.error('Error generating questions:', error);
        
        // Show error and fallback to existing questions
        questionsContainer.innerHTML = `
            <div class="error-message" style="background: #fee; border: 1px solid #fcc; padding: 20px; border-radius: 8px; margin-bottom: 20px;">
                <h3>⚠️ AI Generation Failed</h3>
                <p>${error.message}</p>
                <p style="margin-top: 10px;">Showing previously generated questions instead.</p>
            </div>
        `;
        
        // Render fallback questions
        if (taskData.questions && taskData.questions.length > 0) {
            renderTaskQuestions(taskData.questions);
        } else {
            questionsContainer.innerHTML += `
                <div class="empty-state">
                    <p>No questions available. Please go back and try again.</p>
                    <button onclick="window.location.href='subjects.html'" class="btn-primary">Back to Subjects</button>
                </div>
            `;
        }
    }
}

/**
 * Render questions in the task page
 */
function renderTaskQuestions(questions) {
    const questionsContainer = document.getElementById('questionsContainer');
    
    if (!questions || questions.length === 0) {
        questionsContainer.innerHTML = `
            <div class="empty-state">
                <div class="empty-icon">📝</div>
                <h3>No Questions Available</h3>
                <p>No questions were generated for this topic.</p>
                <button onclick="window.location.href='subjects.html'" class="btn-primary">Back to Subjects</button>
            </div>
        `;
        return;
    }

    // Store questions globally for answer checking - normalize to ensure .question property
    const normalizedQuestions = questions.map((q, idx) => {
        if (typeof q === 'string') {
            return { question: q };
        } else if (q && typeof q === 'object' && q.question) {
            return q;
        } else if (q && typeof q === 'object') {
            // Try to extract text from any object
            return { question: q.text || q.title || String(q) };
        } else {
            return { question: String(q) };
        }
    });
    
    console.log('Storing normalized questions:', normalizedQuestions);
    window.currentTaskQuestions = normalizedQuestions;
    window.taskAnswers = new Array(normalizedQuestions.length).fill(null);
    window.taskScores = new Array(normalizedQuestions.length).fill(null);

    questionsContainer.innerHTML = `
        <div class="questions-header">
            <h3>📝 AI-Generated Questions</h3>
            <p>${normalizedQuestions.length} questions for practice</p>
        </div>
        <div class="questions-grid">
            ${normalizedQuestions.map((q, index) => `
                <div class="question-card" style="border: 2px solid #e5e7eb; border-radius: 12px; padding: 24px; margin-bottom: 20px; background: white;">
                    <div style="display: flex; align-items: center; gap: 12px; margin-bottom: 16px;">
                        <span style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; width: 40px; height: 40px; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-weight: 700;">
                            Q${index + 1}
                        </span>
                    </div>
                    <p style="font-size: 16px; font-weight: 500; margin-bottom: 20px; color: #0f172a; line-height: 1.6;">${q.question}</p>
                    
                    <div style="margin-bottom: 16px;">
                        <label style="display: block; font-weight: 600; margin-bottom: 8px; color: #374151;">Your Answer:</label>
                        <textarea 
                            id="answer-${index}" 
                            placeholder="Type your answer here..." 
                            style="width: 100%; min-height: 80px; padding: 12px; border: 2px solid #e5e7eb; border-radius: 8px; font-size: 14px; font-family: inherit; resize: vertical;"
                        ></textarea>
                    </div>

                    <div style="display: flex; gap: 10px; flex-wrap: wrap;">
                        <button onclick="submitTaskAnswer(${index})" style="padding: 10px 20px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; border: none; border-radius: 8px; font-weight: 600; cursor: pointer;">
                            ✓ Check Answer
                        </button>
                    </div>

                    <div id="result-${index}" style="margin-top: 16px; display: none;">
                        <div id="result-status-${index}" style="padding: 12px 16px; border-radius: 8px; font-weight: 600; text-align: center;"></div>
                    </div>
                </div>
            `).join('')}
        </div>

        <div style="margin-top: 30px; text-align: center;">
            <button onclick="submitAllTaskAnswers()" style="padding: 14px 40px; background: linear-gradient(135deg, #10b981 0%, #059669 100%); color: white; border: none; border-radius: 12px; font-weight: 700; font-size: 16px; cursor: pointer;">
                📊 Submit All Answers
            </button>
        </div>
    `;
}

/**
 * Submit individual answer for AI verification
 */
async function submitTaskAnswer(questionIndex) {
    const answerText = document.getElementById(`answer-${questionIndex}`).value.trim();
    
    if (!answerText) {
        alert('Please enter an answer first!');
        return;
    }

    const questionObj = window.currentTaskQuestions[questionIndex];
    console.log(`Question object at index ${questionIndex}:`, questionObj);
    
    // Handle both object with .question property and plain string questions
    let questionText = '';
    if (typeof questionObj === 'string') {
        questionText = questionObj;
    } else if (questionObj && typeof questionObj === 'object') {
        // Try multiple properties that might contain the question
        questionText = questionObj.question || questionObj.text || questionObj.title || '';
        // If still empty, try toString or JSON.stringify
        if (!questionText) {
            questionText = String(questionObj).substring(0, 500);
        }
    } else if (questionObj) {
        // Fallback: convert to string
        questionText = String(questionObj);
    }
    
    // Final trim and validation
    questionText = String(questionText).trim();
    
    console.log(`Extracted question text: "${questionText}"`);
    console.log(`Question text length: ${questionText.length}`);
    
    if (questionText.length === 0) {
        alert('Error: Question not found!');
        console.error('Question text is empty after extraction');
        console.log('Full question object:', JSON.stringify(questionObj));
        return;
    }

    const resultDiv = document.getElementById(`result-${questionIndex}`);
    const statusDiv = document.getElementById(`result-status-${questionIndex}`);

    try {
        // Show checking status
        resultDiv.style.display = 'block';
        statusDiv.innerHTML = '⏳ AI is checking your answer...';
        statusDiv.style.background = '#fef3c7';
        statusDiv.style.color = '#92400e';

        // Call API to verify answer
        const apiClient = new APIClient({ BASE_URL: 'http://127.0.0.1:8000/api' });
        console.log(`Calling verifyAnswer with question: "${questionText}" (length: ${questionText.length}) and answer: "${answerText}" (length: ${answerText.length})`);
        const response = await apiClient.verifyAnswer(questionText, answerText);

        // Store answer
        window.taskAnswers[questionIndex] = answerText;

        // Get verification result - handle different response formats
        let isCorrect = false;
        let feedback = 'Answer checked by AI';
        let score = 0;
        
        if (response && response.data) {
            isCorrect = response.data.is_correct === true;
            feedback = response.data.feedback || feedback;
            score = isCorrect ? 1 : 0;
        } else if (response && response.is_correct !== undefined) {
            isCorrect = response.is_correct === true;
            feedback = response.feedback || feedback;
            score = isCorrect ? 1 : 0;
        }

        window.taskScores[questionIndex] = score;

        // Display result
        if (isCorrect) {
            statusDiv.innerHTML = `✅ Correct! <br><small>${feedback}</small>`;
            statusDiv.style.background = '#d1fae5';
            statusDiv.style.color = '#065f46';
        } else {
            statusDiv.innerHTML = `❌ Incorrect. <br><small>${feedback}</small>`;
            statusDiv.style.background = '#fee2e2';
            statusDiv.style.color = '#991b1b';
        }

    } catch (error) {
        console.error('Error verifying answer:', error);
        statusDiv.innerHTML = `⚠️ Could not verify answer. Error: ${error.message}`;
        statusDiv.style.background = '#fee2e2';
        statusDiv.style.color = '#991b1b';
        resultDiv.style.display = 'block';
    }
}

/**
 * Submit all answers and calculate final score
 */
async function submitAllTaskAnswers() {
    const taskData = JSON.parse(localStorage.getItem('currentTaskData') || 'null');
    
    if (!taskData) {
        alert('No task data found!');
        return;
    }

    const totalQuestions = window.currentTaskQuestions.length;
    const answeredQuestions = window.taskAnswers.filter(a => a !== null).length;

    if (answeredQuestions < totalQuestions) {
        if (!confirm(`You have answered ${answeredQuestions}/${totalQuestions} questions. Submit anyway?`)) {
            return;
        }
    }

    // Calculate score
    const correctAnswers = window.taskScores.filter(s => s === 1).length;
    const score = Math.round((correctAnswers / totalQuestions) * 100);

    // Save to task history in localStorage
    const taskHistory = JSON.parse(localStorage.getItem('taskHistory') || '[]');
    taskHistory.push({
        subject: taskData.subject,
        topic: taskData.topic,
        totalQuestions: totalQuestions,
        correctAnswers: correctAnswers,
        score: score,
        date: new Date().toISOString(),
        timestamp: Date.now()
    });
    localStorage.setItem('taskHistory', JSON.stringify(taskHistory));

    // Show results
    alert(`Task Complete!\n\nScore: ${correctAnswers}/${totalQuestions} (${score}%)\n\nYour progress has been saved!`);

    // Optionally navigate to progress page
    window.location.href = 'progress.html';
}

/**
 * Handle answering a question
 */
function answerQuestion(questionIndex) {
    // This is now handled by the textarea and submit button
    console.log(`Question ${questionIndex} answer space is ready`);
}

/**
 * Add note for a question
 */
function addNote(questionIndex) {
    const note = prompt('Add your note:');
    if (note) {
        alert(`Note saved for Question ${questionIndex + 1}`);        // Save to localStorage or backend
    }
}

/**
 * Start quiz for a specific topic
 */
function startQuizForTopic(topicName) {
    // Save topic to localStorage for quiz page
    localStorage.setItem('currentQuizTopic', topicName);
    localStorage.setItem('needsQuizGeneration', 'true');
    
    // Navigate to quiz page
    window.location.href = '../codecore.html/quize.html';
}

/* ============================================
   INITIALIZATION
   ============================================ */

// Initialize subjects page on load
if (document.getElementById('subjects')) {
    renderSubjects();
}

// Initialize task page on load
if (document.getElementById('questionsContainer')) {
    loadTaskPage();
}
