/**
 * Question Paper Difficulty Analyzer - Premium Edition
 * Frontend logic for modern Tailwind CSS version with file upload support
 */

// Global variable to store chart instance
let difficultyChart = null;

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
function switchTab(tabName) {
    // Hide all tabs
    document.getElementById('text-tab').classList.add('hidden');
    document.getElementById('file-tab').classList.add('hidden');

    // Remove active class from all buttons
    document.querySelectorAll('.tab-button').forEach(btn => {
        btn.classList.remove('active');
    });

    // Show selected tab
    document.getElementById(tabName + '-tab').classList.remove('hidden');

    // Add active class to clicked button
    event.target.closest('.tab-button').classList.add('active');

    // Show/hide analyze button based on tab
    const analyzeBtn = document.getElementById('analyze_btn');
    if (tabName === 'file') {
        // Hide button for file uploads (auto-submit enabled)
        analyzeBtn.classList.add('hidden');
    } else {
        // Show button for text input
        analyzeBtn.classList.remove('hidden');
    }
}

/**
 * Handle file upload and populate textarea
 */
document.addEventListener('DOMContentLoaded', function () {
    const fileInput = document.getElementById('file_upload');
    const uploadArea = document.getElementById('uploadArea');
    const fileNameElement = document.getElementById('file_name');

    // SINGLE file input change listener - handles all file selection methods
    if (fileInput) {
        fileInput.addEventListener('change', function (e) {
            const file = e.target.files[0];
            if (file) {
                // Show file name
                fileNameElement.textContent = '✓ File selected: ' + file.name;

                // For image files, show a message
                if (file.type.startsWith('image/')) {
                    fileNameElement.innerHTML += '<br><small class="text-slate-500">Processing image with OCR...</small>';
                }

                // AUTO-SUBMIT: Immediately trigger analysis without click button
                showProcessingAnimation();
                setTimeout(() => analyzeQuestion(), 400); // Small delay for UX
            }
        });
    }

    // Upload area - ONLY click handler (no duplicate onclick attribute in HTML)
    if (uploadArea) {
        uploadArea.addEventListener('click', () => {
            fileInput.click();
        });

        // Drag and drop functionality
        uploadArea.addEventListener('dragover', (e) => {
            e.preventDefault();
            uploadArea.classList.add('drag-over');
        });

        uploadArea.addEventListener('dragleave', () => {
            uploadArea.classList.remove('drag-over');
        });

        uploadArea.addEventListener('drop', (e) => {
            e.preventDefault();
            uploadArea.classList.remove('drag-over');

            const files = e.dataTransfer.files;
            if (files.length > 0) {
                fileInput.files = files;
                // Trigger the change event
                const event = new Event('change', { bubbles: true });
                fileInput.dispatchEvent(event);
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
async function analyzeQuestion() {
    const paperText = document.getElementById('paper_text').value.trim();
    const fileInput = document.getElementById('file_upload');
    const errorMessageElement = document.getElementById('error_message');
    const errorText = document.getElementById('error_text');
    const analyzeBtn = document.getElementById('analyze_btn');

    // Clear previous error messages
    errorMessageElement.classList.add('hidden');
    errorText.textContent = '';

    // Validate input
    const hasText = paperText.length > 0;
    const hasFile = fileInput.files && fileInput.files.length > 0;

    if (!hasText && !hasFile) {
        showToast('Please enter or upload a question paper before analyzing.', 'error');
        return;
    }

    // Show loading state
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
            // Validate data structure before rendering
            if (!data.detailed_analysis && !data.questions) {
                console.error("Missing detailed analysis in response:", data);
                showToast('Analysis failed to produce detailed results.', 'error');
                return;
            }

            // Handle both potential key names for questions list
            data.questions = data.detailed_analysis || data.questions;

            if (data.questions.length === 0) {
                showToast('No questions were found to analyze.', 'error');
                return;
            }

            // Display results with animation
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
 * Updates the results section with analysis data and creates a chart
 */
function displayResults(data) {
    // Total questions
    const totalElement = document.getElementById('total_questions');
    if (totalElement) {
        animateCounter('total_questions', 0, data.total_questions, 1200);
    }

    // Individual counts
    animateCounter('covered_count', 0, data.from_covered_syllabus, 1200);
    animateCounter('uncovered_count', 0, data.from_uncovered_syllabus, 1200);
    animateCounter('out_count', 0, data.out_of_syllabus, 1200);

    // Percentages with decimal count-up
    animateCounter('covered_percent', 0, data.covered_percentage, 1200, true);
    animateCounter('uncovered_percent', 0, data.uncovered_percentage, 1200, true);
    animateCounter('out_percent', 0, data.out_percentage, 1200, true);

    // Create coverage chart with animation
    createChart(data.from_covered_syllabus, data.from_uncovered_syllabus, data.out_of_syllabus, data.total_questions);

    // Update Overall Difficulty Section
    const difficultyCard = document.getElementById('difficulty_card');
    const difficultyLevelText = document.getElementById('difficulty_level_text');

    if (difficultyCard && difficultyLevelText) {
        difficultyCard.classList.remove('bg-success-subtle', 'text-success', 'bg-warning-subtle', 'text-warning', 'bg-danger-subtle', 'text-danger');
        const level = data.overall_difficulty;
        difficultyLevelText.textContent = level;

        if (level === 'Easy Paper') {
            difficultyCard.classList.add('bg-success-subtle', 'text-success');
        } else if (level === 'Hard Paper') {
            difficultyCard.classList.add('bg-danger-subtle', 'text-danger');
        } else {
            difficultyCard.classList.add('bg-warning-subtle', 'text-warning');
        }
    }

    // Show results section
    const resultsSection = document.getElementById('results_section');
    if (resultsSection) {
        resultsSection.classList.remove('hidden');
        resultsSection.scrollIntoView({ behavior: 'smooth' });
    }
}

/**
 * Enhanced Count-Up Animation
 */
function animateCounter(elementId, start, end, duration, isPercent = false) {
    const obj = document.getElementById(elementId);
    if (!obj) return;

    let startTimestamp = null;
    const step = (timestamp) => {
        if (!startTimestamp) startTimestamp = timestamp;
        const progress = Math.min((timestamp - startTimestamp) / duration, 1);
        const value = progress * (end - start) + start;

        if (isPercent) {
            obj.textContent = value.toFixed(1) + '%';
        } else {
            obj.textContent = Math.floor(value);
        }

        if (progress < 1) {
            window.requestAnimationFrame(step);
        } else {
            obj.textContent = isPercent ? end + '%' : end;
        }
    };
    window.requestAnimationFrame(step);
}

/**
 * Animate number counting
 */
function animateValue(elementId, start, end, duration) {
    const element = document.getElementById(elementId);
    if (!element) return;

    let current = start;
    const increment = (end - start) / (duration / 16);

    const timer = setInterval(() => {
        current += increment;
        if (current >= end) {
            element.textContent = end;
            clearInterval(timer);
        } else {
            element.textContent = Math.floor(current);
        }
    }, 16);
}

/**
 * Create a beautiful donut chart showing syllabus coverage
 */
function createChart(covered, uncovered, out, total) {
    const canvas = document.getElementById('coverageChart');
    if (!canvas) return;
    const ctx = canvas.getContext('2d');

    // Destroy previous chart if it exists
    if (difficultyChart) {
        difficultyChart.destroy();
    }

    // Custom plugin for center text
    const centerTextPlugin = {
        id: 'centerText',
        beforeDraw: (chart) => {
            const { ctx, width, height } = chart;
            ctx.restore();
            const fontSize = (height / 160).toFixed(2);
            ctx.font = `bold ${fontSize}em Plus Jakarta Sans`;
            ctx.textBaseline = 'middle';
            ctx.fillStyle = '#0f172a';

            const text = total.toString();
            const textX = Math.round((width - ctx.measureText(text).width) / 2);
            const textY = height / 2 - 10;
            ctx.fillText(text, textX, textY);

            ctx.font = `600 0.8em Inter`;
            ctx.fillStyle = '#64748b';
            const subtext = "Questions";
            const subtextX = Math.round((width - ctx.measureText(subtext).width) / 2);
            const subtextY = height / 2 + 15;
            ctx.fillText(subtext, subtextX, subtextY);

            ctx.save();
        }
    };

    difficultyChart = new Chart(ctx, {
        type: 'doughnut',
        data: {
            labels: ['Covered', 'Uncovered', 'Out of Syllabus'],
            datasets: [{
                data: [covered, uncovered, out],
                backgroundColor: [
                    'rgba(16, 185, 129, 0.85)',
                    'rgba(245, 158, 11, 0.85)',
                    'rgba(239, 68, 68, 0.85)'
                ],
                borderWidth: 0,
                hoverOffset: 20,
                borderRadius: 8,
                spacing: 4
            }]
        },
        options: {
            cutout: '75%',
            responsive: true,
            maintainAspectRatio: false,
            animation: {
                duration: 1500,
                easing: 'easeOutQuart',
                animateRotate: true,
                animateScale: true
            },
            plugins: {
                legend: {
                    position: 'bottom',
                    labels: {
                        color: document.body.classList.contains('dark-mode') ? '#f8fafc' : '#0f172a',
                        padding: 20,
                        usePointStyle: true,
                        font: { size: 12, weight: '600' }
                    }
                },
                tooltip: {
                    padding: 12,
                    backgroundColor: 'rgba(15, 23, 42, 0.9)',
                    callbacks: {
                        label: (context) => {
                            const val = context.raw;
                            const pct = ((val / total) * 100).toFixed(1);
                            return ` ${context.label}: ${val} (${pct}%)`;
                        }
                    }
                }
            }
        },
        plugins: [centerTextPlugin]
    });
}

/**
 * Dark Mode & PDF Export Initialization
 */
document.addEventListener('DOMContentLoaded', () => {
    // Theme Toggle
    const themeBtn = document.getElementById('theme_toggle');
    const body = document.body;

    if (localStorage.getItem('theme') === 'dark') {
        body.classList.add('dark-mode');
        themeBtn.querySelector('i').className = 'fas fa-sun text-amber-400 text-xl';
    }

    themeBtn.addEventListener('click', () => {
        body.classList.toggle('dark-mode');
        const isDark = body.classList.contains('dark-mode');
        localStorage.setItem('theme', isDark ? 'dark' : 'light');
        themeBtn.querySelector('i').className = isDark ? 'fas fa-sun text-amber-400 text-xl' : 'fas fa-moon text-slate-600 text-xl';

        // Refresh chart legend color
        if (difficultyChart) {
            difficultyChart.options.plugins.legend.labels.color = isDark ? '#f8fafc' : '#0f172a';
            difficultyChart.update();
        }
    });

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
                    backgroundColor: body.classList.contains('dark-mode') ? '#0f172a' : '#ffffff'
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
    document.getElementById('file_upload').value = '';
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
