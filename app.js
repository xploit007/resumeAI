// Resume Tailor Pro - JavaScript functionality

// Sample data from the application
const sampleData = {
    resume: `John Smith
Software Engineer
john.smith@email.com | (555) 123-4567

PROFESSIONAL SUMMARY
Experienced software engineer with 5+ years developing web applications. Skilled in full-stack development with expertise in JavaScript, Python, and database design.

EXPERIENCE

Software Developer - Tech Corp
Jan 2020 - Present
• Developed web applications using JavaScript and Python frameworks
• Collaborated with cross-functional teams to deliver projects on time
• Improved application performance by 25% through code optimization
• Mentored junior developers and conducted code reviews

Junior Developer - StartupXYZ
Jun 2018 - Dec 2019
• Built responsive web interfaces using HTML, CSS, and JavaScript
• Worked with APIs to integrate third-party services
• Participated in agile development processes
• Fixed bugs and maintained existing codebase

EDUCATION
Bachelor of Science in Computer Science
University of Technology, 2018

SKILLS
JavaScript, Python, React, Node.js, SQL, Git, HTML/CSS, REST APIs`,

    jobDescription: `Senior Data Scientist - HealthTech Solutions

We are seeking a Senior Data Scientist to join our healthcare analytics team. The ideal candidate will have strong experience in machine learning, statistical analysis, and healthcare data.

Responsibilities:
• Develop predictive models for patient outcomes using machine learning algorithms
• Analyze large healthcare datasets to identify trends and insights
• Collaborate with medical professionals to translate business requirements into analytical solutions
• Build data pipelines and automate model deployment processes
• Present findings to stakeholders through compelling visualizations

Requirements:
• 5+ years of experience in data science or analytics
• Strong proficiency in Python, R, or similar languages
• Experience with machine learning libraries (scikit-learn, TensorFlow, PyTorch)
• Knowledge of statistical analysis and hypothesis testing
• Experience with SQL and database technologies
• Healthcare industry experience preferred
• Strong communication and presentation skills

Preferred Qualifications:
• Advanced degree in Statistics, Computer Science, or related field
• Experience with cloud platforms (AWS, Azure, GCP)
• Knowledge of healthcare regulations (HIPAA, FDA)
• Experience with big data technologies (Spark, Hadoop)`,

    tailoredOutput: {
        keyThemes: "This Senior Data Scientist role at HealthTech Solutions focuses on predictive healthcare analytics, requiring strong machine learning expertise and the ability to work with medical data. The position emphasizes both technical depth in data science methodologies and business acumen to translate medical requirements into analytical solutions.",
        
        experience: `**Tech Corp** - Software Developer (Data-Focused)
*Jan 2020 - Present*

• Developed predictive analytics applications using Python and machine learning libraries, improving decision-making processes by 25%
• Collaborated with cross-functional teams including healthcare professionals to deliver data-driven solutions on time
• Optimized data processing pipelines and statistical models, enhancing application performance and analytical accuracy
• Mentored junior developers on data science best practices and conducted code reviews for analytics projects

**StartupXYZ** - Junior Data Analyst
*Jun 2018 - Dec 2019*

• Built interactive data visualization dashboards using Python and JavaScript to present analytical insights
• Integrated healthcare APIs and third-party data services to enhance analytical capabilities
• Participated in agile analytics sprints, contributing to rapid development of data science solutions
• Maintained and debugged existing statistical models and data processing workflows`,

        projects: `**Healthcare Outcome Prediction Model** – Academic Research Project
Sep 2023 – Dec 2023
• Developed machine learning model using Python and scikit-learn to predict patient readmission rates with 85% accuracy
• Processed and analyzed 10,000+ patient records while ensuring HIPAA compliance and data privacy standards

**Medical Data Pipeline Automation** – Independent Project  
Mar 2023 – May 2023
• Built automated data processing pipeline using Python and SQL to handle large-scale healthcare datasets
• Implemented statistical analysis workflows that reduced data processing time by 40% and improved analytical insights`,

        missingKeywords: ["machine learning", "statistical analysis", "healthcare data", "predictive modeling", "TensorFlow", "PyTorch", "scikit-learn", "R", "hypothesis testing", "data pipelines", "AWS", "Azure", "HIPAA", "healthcare analytics", "patient outcomes"]
    }
};

// Global state
let currentStep = 1;
let processingInterval;

// DOM elements
let resumeUpload, jobUpload, resumeFile, jobFile, resumeText, jobText, tailorBtn;

// Initialize the application
document.addEventListener('DOMContentLoaded', function() {
    // Initialize DOM elements after page load
    resumeUpload = document.getElementById('resumeUpload');
    jobUpload = document.getElementById('jobUpload');
    resumeFile = document.getElementById('resumeFile');
    jobFile = document.getElementById('jobFile');
    resumeText = document.getElementById('resumeText');
    jobText = document.getElementById('jobText');
    tailorBtn = document.getElementById('tailorBtn');
    
    initializeFileUploads();
    initializeTabs();
    initializeSampleButtons();
    
    // Add smooth scrolling for anchor links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });
});

// Initialize sample buttons with proper event listeners
function initializeSampleButtons() {
    const sampleResumeBtn = document.querySelector('button[onclick="loadSampleResume()"]');
    const sampleJobBtn = document.querySelector('button[onclick="loadSampleJob()"]');
    
    if (sampleResumeBtn) {
        // Remove inline onclick and add proper event listener
        sampleResumeBtn.removeAttribute('onclick');
        sampleResumeBtn.addEventListener('click', function(e) {
            e.preventDefault();
            loadSampleResume();
        });
    }
    
    if (sampleJobBtn) {
        // Remove inline onclick and add proper event listener
        sampleJobBtn.removeAttribute('onclick');
        sampleJobBtn.addEventListener('click', function(e) {
            e.preventDefault();
            loadSampleJob();
        });
    }
}

// File upload functionality
function initializeFileUploads() {
    // Resume file upload
    setupFileUpload(resumeUpload, resumeFile, handleResumeFile);
    
    // Job description file upload
    setupFileUpload(jobUpload, jobFile, handleJobFile);
}

function setupFileUpload(uploadArea, fileInput, handleFile) {
    // Click to upload
    uploadArea.addEventListener('click', () => {
        fileInput.click();
    });
    
    // Drag and drop
    uploadArea.addEventListener('dragover', (e) => {
        e.preventDefault();
        uploadArea.classList.add('dragover');
    });
    
    uploadArea.addEventListener('dragleave', (e) => {
        e.preventDefault();
        uploadArea.classList.remove('dragover');
    });
    
    uploadArea.addEventListener('drop', (e) => {
        e.preventDefault();
        uploadArea.classList.remove('dragover');
        
        const files = e.dataTransfer.files;
        if (files.length > 0) {
            handleFile(files[0]);
        }
    });
    
    // File input change
    fileInput.addEventListener('change', (e) => {
        if (e.target.files.length > 0) {
            handleFile(e.target.files[0]);
        }
    });
}

function handleResumeFile(file) {
    const fileName = file.name;
    const fileSize = (file.size / 1024).toFixed(1) + ' KB';
    
    // Update UI to show file selected
    const uploadContent = resumeUpload.querySelector('.file-upload-content');
    uploadContent.innerHTML = `
        <div class="file-upload-icon">✅</div>
        <p><strong>${fileName}</strong></p>
        <p class="file-upload-hint">${fileSize} - Click to change</p>
    `;
    
    // In a real app, you would read the file content here
    // For demo purposes, we'll just show it's uploaded
}

function handleJobFile(file) {
    const fileName = file.name;
    const fileSize = (file.size / 1024).toFixed(1) + ' KB';
    
    // Update UI to show file selected
    const uploadContent = jobUpload.querySelector('.file-upload-content');
    uploadContent.innerHTML = `
        <div class="file-upload-icon">✅</div>
        <p><strong>${fileName}</strong></p>
        <p class="file-upload-hint">${fileSize} - Click to change</p>
    `;
}

// Load sample data
function loadSampleResume() {
    if (resumeText) {
        resumeText.value = sampleData.resume;
        showNotification('Sample resume loaded successfully!', 'success');
    } else {
        console.error('Resume text area not found');
    }
}

function loadSampleJob() {
    if (jobText) {
        jobText.value = sampleData.jobDescription;
        showNotification('Sample job description loaded successfully!', 'success');
    } else {
        console.error('Job text area not found');
    }
}

// Main tailoring functionality
function startTailoring() {
    // Validate inputs
    if (!validateInputs()) {
        return;
    }
    
    // Hide input section and show processing
    document.getElementById('inputSection').classList.add('hidden');
    document.getElementById('processingSection').classList.remove('hidden');
    
    // Start processing simulation
    simulateProcessing();
}

function validateInputs() {
    const hasResume = resumeText && (resumeText.value.trim() || resumeFile.files.length > 0);
    const hasJob = jobText && (jobText.value.trim() || jobFile.files.length > 0);
    
    if (!hasResume) {
        showNotification('Please provide your resume content or upload a file.', 'error');
        return false;
    }
    
    if (!hasJob) {
        showNotification('Please provide the job description or upload a file.', 'error');
        return false;
    }
    
    return true;
}

function simulateProcessing() {
    currentStep = 1;
    
    processingInterval = setInterval(() => {
        // Update current step
        const currentStepElement = document.getElementById(`step${currentStep}`);
        if (currentStepElement) {
            currentStepElement.classList.remove('active');
            currentStepElement.classList.add('completed');
        }
        
        currentStep++;
        
        // Update next step
        const nextStepElement = document.getElementById(`step${currentStep}`);
        if (nextStepElement) {
            nextStepElement.classList.add('active');
        }
        
        // Complete processing
        if (currentStep > 6) {
            clearInterval(processingInterval);
            completeProcessing();
        }
    }, 800);
}

function completeProcessing() {
    // Hide processing section
    document.getElementById('processingSection').classList.add('hidden');
    
    // Show results
    displayResults();
    document.getElementById('resultsSection').classList.remove('hidden');
    
    // Scroll to results
    document.getElementById('resultsSection').scrollIntoView({
        behavior: 'smooth',
        block: 'start'
    });
}

function displayResults() {
    // Display key themes
    const keyThemesElement = document.getElementById('keyThemes');
    if (keyThemesElement) {
        keyThemesElement.textContent = sampleData.tailoredOutput.keyThemes;
    }
    
    // Display tailored experience
    const experienceElement = document.getElementById('experienceContent');
    if (experienceElement) {
        experienceElement.textContent = sampleData.tailoredOutput.experience;
    }
    
    // Display projects
    const projectsElement = document.getElementById('projectsContent');
    if (projectsElement) {
        projectsElement.textContent = sampleData.tailoredOutput.projects;
    }
    
    // Display keywords
    const keywordsContainer = document.getElementById('keywordsContent');
    if (keywordsContainer) {
        keywordsContainer.innerHTML = '';
        
        sampleData.tailoredOutput.missingKeywords.forEach(keyword => {
            const tag = document.createElement('span');
            tag.className = 'keyword-tag';
            tag.textContent = keyword;
            keywordsContainer.appendChild(tag);
        });
    }
}

// Tab functionality
function initializeTabs() {
    // Use event delegation for tab buttons
    document.addEventListener('click', function(e) {
        if (e.target.classList.contains('tab-button')) {
            const tabName = e.target.textContent.split(' ')[1].toLowerCase();
            switchTab(tabName, e.target);
        }
    });
}

function switchTab(tabName, clickedButton) {
    // Remove active class from all buttons and panels
    document.querySelectorAll('.tab-button').forEach(btn => btn.classList.remove('active'));
    document.querySelectorAll('.tab-panel').forEach(panel => panel.classList.remove('active'));
    
    // Add active class to selected button and panel
    clickedButton.classList.add('active');
    
    // Map tab names to panel IDs
    const tabMap = {
        'themes': 'themesPanel',
        'experience': 'experiencePanel',
        'projects': 'projectsPanel',
        'keywords': 'keywordsPanel'
    };
    
    const panelId = tabMap[tabName];
    const panel = document.getElementById(panelId);
    if (panel) {
        panel.classList.add('active');
    }
}

// Download functionality (mock)
function downloadResume() {
    const formatSelect = document.getElementById('outputFormat');
    const format = formatSelect ? formatSelect.value : 'text';
    const fileName = `tailored_resume.${format === 'word' ? 'docx' : 'txt'}`;
    
    // Create mock download content
    const content = createDownloadContent();
    
    // Create and trigger download
    const blob = new Blob([content], { type: 'text/plain' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = fileName;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
    
    showNotification(`Resume downloaded as ${fileName}`, 'success');
}

function createDownloadContent() {
    return `TAILORED RESUME - Generated by Resume Tailor Pro

✅ Key Themes From the Role & Company:
${sampleData.tailoredOutput.keyThemes}

🛠 Tailored Experience Content:
${sampleData.tailoredOutput.experience}

🎓 Tailored Projects:
${sampleData.tailoredOutput.projects}

🧩 Extra Keywords to Add to Skills Section:
${sampleData.tailoredOutput.missingKeywords.join(', ')}

---
Generated on: ${new Date().toLocaleDateString()}
Tool: Resume Tailor Pro
`;
}

// Reset functionality
function startOver() {
    // Reset all sections
    document.getElementById('inputSection').classList.remove('hidden');
    document.getElementById('processingSection').classList.add('hidden');
    document.getElementById('resultsSection').classList.add('hidden');
    
    // Reset forms
    if (resumeText) resumeText.value = '';
    if (jobText) jobText.value = '';
    
    const apiKeyInput = document.getElementById('apiKey');
    if (apiKeyInput) apiKeyInput.value = '';
    
    // Reset file uploads
    resetFileUpload(resumeUpload, 'resume');
    resetFileUpload(jobUpload, 'job description');
    
    // Reset processing state
    currentStep = 1;
    if (processingInterval) {
        clearInterval(processingInterval);
    }
    
    // Reset progress steps
    document.querySelectorAll('.progress-step').forEach((step, index) => {
        step.classList.remove('active', 'completed');
        if (index === 0) {
            step.classList.add('active');
        }
    });
    
    // Scroll to top
    scrollToTool();
    
    showNotification('Ready to tailor a new resume!', 'success');
}

function resetFileUpload(uploadArea, type) {
    if (!uploadArea) return;
    
    const uploadContent = uploadArea.querySelector('.file-upload-content');
    if (uploadContent) {
        uploadContent.innerHTML = `
            <div class="file-upload-icon">📁</div>
            <p>Drop your ${type} file here or click to browse</p>
            <p class="file-upload-hint">Supports ${type === 'resume' ? '.docx, .txt' : '.pdf, .txt'} files</p>
        `;
    }
}

// Utility functions
function scrollToTool() {
    const toolSection = document.getElementById('tool');
    if (toolSection) {
        toolSection.scrollIntoView({
            behavior: 'smooth',
            block: 'start'
        });
    }
}

function showNotification(message, type = 'info') {
    // Create notification element
    const notification = document.createElement('div');
    notification.className = `notification notification--${type}`;
    notification.innerHTML = `
        <span>${message}</span>
        <button onclick="this.parentElement.remove()" style="background: none; border: none; color: inherit; cursor: pointer; margin-left: auto;">×</button>
    `;
    
    // Add styles if not already present
    if (!document.querySelector('#notification-styles')) {
        const style = document.createElement('style');
        style.id = 'notification-styles';
        style.textContent = `
            .notification {
                position: fixed;
                top: 20px;
                right: 20px;
                padding: 12px 16px;
                border-radius: 6px;
                color: white;
                display: flex;
                align-items: center;
                gap: 12px;
                z-index: 1000;
                animation: slideIn 0.3s ease;
                max-width: 400px;
            }
            .notification--success { background: var(--color-success); }
            .notification--error { background: var(--color-error); }
            .notification--info { background: var(--color-info); }
            @keyframes slideIn {
                from { transform: translateX(100%); opacity: 0; }
                to { transform: translateX(0); opacity: 1; }
            }
        `;
        document.head.appendChild(style);
    }
    
    // Add to page
    document.body.appendChild(notification);
    
    // Auto remove after 5 seconds
    setTimeout(() => {
        if (notification.parentElement) {
            notification.remove();
        }
    }, 5000);
}