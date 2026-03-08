/**
 * Question Paper Difficulty Analyzer - Premium Edition
 * Frontend logic for modern Tailwind CSS version with file upload support
 */

// Global variable to store chart instance
let difficultyChart = null;
let coverageChart = null;

const coveredTopics = 4;
const uncoveredTopics = 3;

/**
 * Show toast notification
 */
function showToast(message, type = 'error') {
    const toast = document.createElement('div');
    const bgColor = type === 'error' ? 'bg-red-500' : type === 'success' ? 'bg-green-500' : 'bg-blue-500';

    toast.className = `fixed bottom-6 right-6 px-6 py-3 rounded-lg text-white font-medium ${bgColor} shadow-lg animate-fade-in-up z-50`;
    toast.textContent = message;

    document.body.appendChild(toast);

    // Auto remove after 4 seconds
    setTimeout(() => {
        toast.style.opacity = '0';
        toast.style.transform = 'translateY(20px)';
        setTimeout(() => toast.remove(), 300);
    }, 4000);
}

/**
 * Tab Switching Functionality
 */
function switchTab(tabId) {
    const tabs = document.querySelectorAll(".tab-content");
    tabs.forEach(tab => {
        tab.classList.add('hidden');
        tab.style.display = "none";
    });

    const target = document.getElementById(tabId);
    if (target) {
        target.classList.remove('hidden');
        target.style.display = "block";
    }

    // Update button states
    document.querySelectorAll('.tab-button').forEach(btn => {
        btn.classList.remove('active');
        if (btn.getAttribute('onclick').includes(tabId)) {
            btn.classList.add('active');
        }
    });

    // Toggle analyze button
    const analyzeBtn = document.getElementById('analyzeBtn');
    if (analyzeBtn) {
        if (tabId === 'file-tab') {
            analyzeBtn.classList.remove('hidden'); // Keep it visible for both now if preferred, or toggle
        } else {
            analyzeBtn.classList.remove('hidden');
        }
    }
}

/**
 * Handle file upload and populate textarea
 */
document.addEventListener('DOMContentLoaded', function () {
    const fileInput = document.getElementById('fileInput');
    const analyzeBtn = document.getElementById('analyzeBtn');
    const uploadArea = document.getElementById('uploadArea');
    const fileNameElement = document.getElementById('file_name');

    console.log("DOM content loaded, initializing listeners...");

    if (analyzeBtn) {
        analyzeBtn.addEventListener('click', () => {
            console.log("Analyze button clicked");
            analyzeQuestion();
        });
    }

    if (fileInput) {
        fileInput.addEventListener('change', function (e) {
            const file = e.target.files[0];
            console.log("Selected file:", file ? file.name : "None");
            if (file) {
                if (fileNameElement) {
                    fileNameElement.textContent = '✓ File selected: ' + file.name;
                    if (file.type.startsWith('image/')) {
                        fileNameElement.innerHTML += '<br><small class="text-slate-500">Processing image with OCR...</small>';
                    }
                }
            }
        });
    }

    if (uploadArea && fileInput) {
        uploadArea.addEventListener('click', () => fileInput.click());

        uploadArea.addEventListener('dragover', (e) => {
            e.preventDefault();
            uploadArea.classList.add('drag-over');
        });

        uploadArea.addEventListener('dragleave', () => uploadArea.classList.remove('drag-over'));

        uploadArea.addEventListener('drop', (e) => {
            e.preventDefault();
            uploadArea.classList.remove('drag-over');
            const files = e.dataTransfer.files;
            if (files.length > 0) {
                fileInput.files = files;
                fileInput.dispatchEvent(new Event('change', { bubbles: true }));
            }
        });
    }
});

/**
 * Show processing animation overlay
 */
function showProcessingAnimation() {
    const overlay = document.getElementById('processingOverlay');
    overlay.classList.add('show');
}

/**
 * Hide processing animation overlay
 */
function hideProcessingAnimation() {
    const overlay = document.getElementById('processingOverlay');
    overlay.classList.remove('show');
}

/**
 * Analyze the question paper
 * Sends the paper text or file to the backend for analysis
 */
async function analyzeQuestion(questionText) {
    const paperText = questionText || document.getElementById('paper_text').value.trim();
    const fileInput = document.getElementById('fileInput');
    const analyzeBtn = document.getElementById('analyzeBtn');

    const hasText = paperText.length > 0;
    const hasFile = fileInput.files && fileInput.files.length > 0;

    if (!hasText && !hasFile) {
        alert('Please upload a question paper first.');
        return;
    }

    console.log("Analysis started. File:", hasFile ? fileInput.files[0].name : "None", "Text:", hasText);

    // Show loading state
    showProcessingAnimation();
    analyzeBtn.disabled = true;
    const originalButtonText = analyzeBtn.innerHTML;
    analyzeBtn.innerHTML = `
        <div class="spinner mr-2"></div>
        <span>Analyzing...</span>
    `;

    try {
        let response;

        if (hasFile) {
            // File upload
            const formData = new FormData();
            formData.append('file', fileInput.files[0]);

            response = await fetch('/analyze', {
                method: 'POST',
                body: formData
            });
        } else {
            // Text input branch - split into arrays
            const questionsArray = paperText.split('\n')
                .map(q => q.trim())
                .filter(q => q.length > 0);

            // Client-side validation: ensure questions are provided
            if (questionsArray.length === 0) {
                alert("Please enter at least one question to analyze.");
                showToast('Questions cannot be empty!', 'error');

                // Reset button state
                analyzeBtn.disabled = false;
                analyzeBtn.innerHTML = originalButtonText;
                hideProcessingAnimation();
                return;
            }

            const syllabusArray = (window.USER_SYLLABUS || "")
                .split(',')
                .map(s => s.trim())
                .filter(s => s.length > 0);

            const requestBody = {
                questions: questionsArray,
                syllabus: syllabusArray,
                filename: 'text-input'
            };

            console.log("Analyzing with Syllabus:", syllabusArray);

            // Debug logging for the request payload
            console.log("Sending JSON request to /analyze:", requestBody);

            response = await fetch('/analyze', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(requestBody)
            });
        }

        const data = await response.json();

        if (response.ok) {
            // Simplified validation per user request
            if (!data.difficulty) {
                console.error("Difficulty not returned from backend:", data);
                showToast('Difficulty level missing from response.', 'error');
                return;
            }

            // Display results
            displayResults(data);
            showToast('Analysis completed successfully!', 'success');
        } else {
            // Show error message from backend
            const errorMsg = data.error || 'An error occurred. Please try again.';
            if (data.raw_response) {
                console.error("Raw AI Response causing error:", data.raw_response);
            }
            showToast(errorMsg, 'error');
        }
    } catch (error) {
        showToast('Error: Unable to connect to the server. Make sure Flask is running.', 'error');
        console.error('Error:', error);
    } finally {
        // Restore button state
        analyzeBtn.disabled = false;
        analyzeBtn.innerHTML = originalButtonText;
        // Hide processing animation
        hideProcessingAnimation();
    }
}

/**
 * Display analysis results with animations
 * Updates the results section with analysis data
 */
function displayResults(data) {
    // Update metric boxes
    if (data.total_questions !== undefined) {
        document.getElementById("totalQuestions").innerText = data.total_questions;
        document.getElementById("easyQuestions").innerText = data.easy_questions;
        document.getElementById("mediumQuestions").innerText = data.medium_questions;
        document.getElementById("hardQuestions").innerText = data.hard_questions;
    }

    // Update Overall Difficulty Section per user request
    const difficultyLevelText = document.getElementById('difficultyLevel');

    if (difficultyLevelText) {
        // Clear previous animations/classes if any
        const level = data.difficulty || 'Medium';
        difficultyLevelText.innerText = level;

        // Optional: Keep the color coding if the box exists
        const box = document.querySelector('.difficulty-box');
        if (box) {
            // Reset colors
            box.classList.remove('text-emerald-600', 'text-amber-600', 'text-rose-600');
            if (level.includes('Easy')) box.classList.add('text-emerald-600');
            else if (level.includes('Hard')) box.classList.add('text-rose-600');
            else box.classList.add('text-amber-600');
        }
    }

    // Update Coverage Chart
    updateCoverageChart();

    // Show results section
    const resultsSection = document.getElementById('results_section');
    if (resultsSection) {
        resultsSection.classList.remove('hidden');
        resultsSection.scrollIntoView({ behavior: 'smooth' });
    }
}


/**
 * Dark Mode & PDF Export Initialization
 */
document.addEventListener('DOMContentLoaded', () => {
    // PDF Download
    const downloadBtn = document.getElementById('download_report');
    if (downloadBtn) {
        downloadBtn.addEventListener('click', async () => {
            const { jsPDF } = window.jspdf;
            const element = document.getElementById('content_wrapper'); // Whole page content

            downloadBtn.innerHTML = '<i class="fas fa-spinner fa-spin me-2"></i> Generating PDF...';
            downloadBtn.disabled = true;

            try {
                const canvas = await html2canvas(element, {
                    scale: 2,
                    useCORS: true,
                    backgroundColor: '#ffffff'
                });

                const imgData = canvas.toDataURL('image/png');
                const pdf = new jsPDF('p', 'mm', 'a4');
                const imgProps = pdf.getImageProperties(imgData);
                const pdfWidth = pdf.internal.pageSize.getWidth();
                const pdfHeight = (imgProps.height * pdfWidth) / imgProps.width;

                pdf.addImage(imgData, 'PNG', 0, 0, pdfWidth, pdfHeight);
                pdf.save(`Analysis_Report_${new Date().getTime()}.pdf`);
            } catch (error) {
                console.error('PDF Error:', error);
                alert('Failed to generate PDF. Please try again.');
            } finally {
                downloadBtn.innerHTML = '<i class="fas fa-file-pdf me-2"></i> Download Analysis Report';
                downloadBtn.disabled = false;
            }
        });
    }
});

/**
 * Reset the analyzer to analyze another paper
 */
function resetAnalyzer() {
    // Clear textarea and file input
    document.getElementById('paper_text').value = '';
    document.getElementById('fileInput').value = '';
    document.getElementById('file_name').textContent = '';

    // Hide results section
    document.getElementById('results_section').classList.add('hidden');

    // Clear error message
    const errorMessageElement = document.getElementById('error_message');
    errorMessageElement.classList.add('hidden');
    document.getElementById('error_text').textContent = '';

    // Reset to text input tab
    document.getElementById('text-tab').classList.remove('hidden');
    document.getElementById('file-tab').classList.add('hidden');
    document.querySelectorAll('.tab-button').forEach((btn, idx) => {
        if (idx === 0) {
            btn.classList.add('active');
        } else {
            btn.classList.remove('active');
        }
    });

    // Focus on textarea
    document.getElementById('paper_text').focus();

    // Smooth scroll to top
    window.scrollTo({ top: 0, behavior: 'smooth' });
}

/**
 * Update Syllabus Coverage Chart using static data
 */
function updateCoverageChart() {
    const ctx = document.getElementById("coverageChart");
    if (!ctx) return;

    if (coverageChart) {
        coverageChart.destroy();
    }

    coverageChart = new Chart(ctx, {
        type: "pie",
        data: {
            labels: ["Covered Topics", "Uncovered Topics"],
            datasets: [{
                data: [coveredTopics, uncoveredTopics],
                backgroundColor: ["#4CAF50", "#F44336"],
                borderWidth: 1,
                borderColor: '#ffffff'
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    position: 'bottom',
                    labels: {
                        padding: 20,
                        usePointStyle: true,
                        font: {
                            size: 14,
                            weight: '600'
                        }
                    }
                },
                tooltip: {
                    callbacks: {
                        label: function (context) {
                            const label = context.label || '';
                            const value = context.raw || 0;
                            const total = coveredTopics + uncoveredTopics;
                            const percentage = Math.round((value / total) * 100);
                            return `${label}: ${value} (${percentage}%)`;
                        }
                    }
                }
            }
        }
    });
}
