// API Configuration
const API_URL = ''; // Relative to the server path
// Global State
let employeesCache = [];
let logsCache = [];
// DOM Elements
const sidebarNav = document.querySelector('.nav-menu');
const navItems = document.querySelectorAll('.nav-item');
const sections = document.querySelectorAll('.tab-content');
const pageTitle = document.getElementById('page-title');
const liveDateEl = document.getElementById('live-date');
// Form elements
const formRegister = document.getElementById('form-register');
const formLogHours = document.getElementById('form-loghours');
const formCalculate = document.getElementById('form-calculate');
// Input fields
const regNameInput = document.getElementById('reg-name');
const regCnicInput = document.getElementById('reg-cnic');
const logCnicSelect = document.getElementById('log-cnic-select');
const logHoursInput = document.getElementById('log-hours-input');
const hoursBubble = document.getElementById('hours-bubble');
const calcCnicSelect = document.getElementById('calc-cnic-select');
const calcRateInput = document.getElementById('calc-rate');
// Search elements
const employeeSearchInput = document.getElementById('employee-search');
const logsSearchInput = document.getElementById('logs-search');
// Modal Elements
const salaryModal = document.getElementById('salary-modal');
const btnCloseModal = document.getElementById('btn-close-modal');
const btnDismissModal = document.getElementById('btn-dismiss-modal');
const btnPrintReceipt = document.getElementById('btn-print-receipt');
// Modal Receipt Fields
const receiptEmpName = document.getElementById('receipt-emp-name');
const receiptEmpCnic = document.getElementById('receipt-emp-cnic');
const receiptDate = document.getElementById('receipt-date');
const receiptTotalHours = document.getElementById('receipt-total-hours');
const receiptRate = document.getElementById('receipt-rate');
const receiptSalary = document.getElementById('receipt-salary');
// Toast Container
const toastContainer = document.getElementById('toast-container');
// ==========================================
// Initializer & System Clock
// ==========================================
document.addEventListener('DOMContentLoaded', () => {
    initApp();
});
function initApp() {
    updateClock();
    setInterval(updateClock, 60000);
    
    setupTabNavigation();
    setupCNICFormatting();
    setupHoursSlider();
    setupRateChips();
    setupFormSubmissions();
    setupModalEvents();
    setupSearchFilters();
    
    // Initial fetch of dataset
    loadData();
}
function updateClock() {
    const days = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'];
    const months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'];
    
    const now = new Date();
    const dayName = days[now.getDay()];
    const monthName = months[now.getMonth()];
    const date = now.getDate();
    const year = now.getFullYear();
    
    liveDateEl.textContent = `${dayName}, ${monthName} ${date}, ${year}`;
}
// ==========================================
// Visual Toast Notification System
// ==========================================
function showToast(message, type = 'success') {
    const toast = document.createElement('div');
    toast.className = `toast ${type}`;
    
    let iconSvg = '';
    if (type === 'success') {
        iconSvg = `<svg class="toast-icon" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" /></svg>`;
    } else if (type === 'error') {
        iconSvg = `<svg class="toast-icon" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 14l2-2m0 0l2-2m-2 2l-2-2m2 2l2 2m7-2a9 9 0 11-18 0 9 9 0 0118 0z" /></svg>`;
    } else {
        iconSvg = `<svg class="toast-icon" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" /></svg>`;
    }
    
    toast.innerHTML = `
        ${iconSvg}
        <div class="toast-content">
            <p class="toast-message">${message}</p>
        </div>
    `;
    
    toastContainer.appendChild(toast);
    
    // Automatically remove after 4 seconds
    setTimeout(() => {
        toast.style.animation = 'slideInToast 0.3s cubic-bezier(0.34, 1.56, 0.64, 1) reverse forwards';
        toast.addEventListener('animationend', () => {
            toast.remove();
        });
    }, 4000);
}
// ==========================================
// Tab Layout Switching Logic
// ==========================================
function setupTabNavigation() {
    navItems.forEach(item => {
        item.addEventListener('click', () => {
            const tabId = item.getAttribute('data-tab');
            switchTab(tabId);
        });
    });
}
function switchTab(tabId) {
    // Update active nav button
    navItems.forEach(btn => {
        if (btn.getAttribute('data-tab') === tabId) {
            btn.classList.add('active');
        } else {
            btn.classList.remove('active');
        }
    });
    // Update active section view
    sections.forEach(sec => {
        if (sec.id === `tab-${tabId}`) {
            sec.classList.add('active');
        } else {
            sec.classList.remove('active');
        }
    });
    // Header updates
    const titleMap = {
        'dashboard': 'Dashboard Overview',
        'register': 'New Employee Registration',
        'loghours': 'Log Daily Work Hours',
        'calculate': 'Generate Salary Statement',
        'logs': 'System Hourly Log Feed'
    };
    pageTitle.textContent = titleMap[tabId] || 'Salary Dynamics';
}
// ==========================================
// Interactive Inputs Formatting & Sliders
// ==========================================
function setupCNICFormatting() {
    // Pakistan CNIC template format: XXXXX-XXXXXXX-X (13 digits total)
    regCnicInput.addEventListener('input', (e) => {
        let value = e.target.value.replace(/\D/g, ''); // strip out non-digits
        if (value.length > 13) {
            value = value.slice(0, 13);
        }
        
        let formatted = '';
        if (value.length > 0) {
            formatted += value.slice(0, Math.min(value.length, 5));
        }
        if (value.length > 5) {
            formatted += '-' + value.slice(5, Math.min(value.length, 12));
        }
        if (value.length > 12) {
            formatted += '-' + value.slice(12, 13);
        }
        
        e.target.value = formatted;
        
        // Show live validation info
        const validationMsg = document.getElementById('cnic-validation-msg');
        if (value.length === 13) {
            validationMsg.textContent = 'CNIC format is valid.';
            validationMsg.style.color = 'var(--success)';
        } else {
            validationMsg.textContent = 'Must be 13 digits (format: xxxxx-xxxxxxx-x).';
            validationMsg.style.color = 'var(--text-muted)';
        }
    });
}
function setupHoursSlider() {
    logHoursInput.addEventListener('input', (e) => {
        hoursBubble.textContent = `${e.target.value} hrs`;
    });
}
function setupRateChips() {
    const chips = document.querySelectorAll('.rate-chip');
    chips.forEach(chip => {
        chip.addEventListener('click', () => {
            const rate = chip.getAttribute('data-rate');
            calcRateInput.value = rate;
            
            // Toggle active state
            chips.forEach(c => c.classList.remove('active'));
            chip.classList.add('active');
        });
    });
    // Clear active chip style if user manually changes number input
    calcRateInput.addEventListener('input', () => {
        chips.forEach(c => {
            if (c.getAttribute('data-rate') === calcRateInput.value) {
                c.classList.add('active');
            } else {
                c.classList.remove('active');
            }
        });
    });
}
// ==========================================
// Network Operations & JSON APIs
// ==========================================
async function loadData() {
    try {
        // Parallel fetches
        const [empResponse, logsResponse] = await Promise.all([
            fetch(`${API_URL}/api/employees`),
            fetch(`${API_URL}/api/logs`)
        ]);
        if (empResponse.ok && logsResponse.ok) {
            employeesCache = await empResponse.json();
            logsCache = await logsResponse.json();
            
            updateDashboardMetrics();
            populateDropdowns();
            renderEmployeesTable(employeesCache);
            renderLogsTable(logsCache);
        } else {
            showToast('Unable to fetch data ledger from the server.', 'error');
        }
    } catch (error) {
        console.error('Error fetching data:', error);
        showToast('Server connection failed. Is app.py running?', 'error');
    }
}
function updateDashboardMetrics() {
    // Total Employees
    document.getElementById('stat-total-employees').textContent = employeesCache.length;
    // Total hours and logs count
    const totalHours = logsCache.reduce((acc, log) => acc + log.hours, 0);
    document.getElementById('stat-total-hours').textContent = `${totalHours}h`;
    document.getElementById('stat-total-entries').textContent = logsCache.length;
}
function populateDropdowns() {
    // Clear select elements, keeping the first placeholder option
    logCnicSelect.innerHTML = '<option value="" disabled selected>-- Select Registered Employee --</option>';
    calcCnicSelect.innerHTML = '<option value="" disabled selected>-- Select Registered Employee --</option>';
    
    // Sort employees alphabetically
    const sortedEmployees = [...employeesCache].sort((a, b) => a.name.localeCompare(b.name));
    sortedEmployees.forEach(emp => {
        const optionText = `${emp.name} (${formatCnicDisplay(emp.cnic)})`;
        
        const opt1 = document.createElement('option');
        opt1.value = emp.cnic;
        opt1.textContent = optionText;
        logCnicSelect.appendChild(opt1);
        const opt2 = document.createElement('option');
        opt2.value = emp.cnic;
        opt2.textContent = optionText;
        calcCnicSelect.appendChild(opt2);
    });
}
function formatCnicDisplay(cnic) {
    if (cnic.length === 13) {
        return `${cnic.slice(0, 5)}-${cnic.slice(5, 12)}-${cnic.slice(12)}`;
    }
    return cnic;
}
// ==========================================
// Tables Rendering & Real-Time Filtering
// ==========================================
function renderEmployeesTable(list) {
    const tbody = document.getElementById('employees-list-body');
    tbody.innerHTML = '';
    
    if (list.length === 0) {
        tbody.innerHTML = `<tr><td colspan="3" class="empty-state">No matching employees found.</td></tr>`;
        return;
    }
    list.forEach(emp => {
        const tr = document.createElement('tr');
        tr.innerHTML = `
            <td style="font-weight: 600;">${emp.name}</td>
            <td style="font-family: monospace; letter-spacing: 0.05em;">${formatCnicDisplay(emp.cnic)}</td>
            <td>
                <div class="action-group">
                    <button class="btn-action" onclick="quickLogHours('${emp.cnic}')">
                        <svg width="14" height="14" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" /></svg>
                        Log Hours
                    </button>
                    <button class="btn-action secondary" onclick="quickCalculateSalary('${emp.cnic}')">
                        <svg width="14" height="14" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 7h6m0 10v-3m-3 3h.01M9 17h.01" /></svg>
                        Salary
                    </button>
                </div>
            </td>
        `;
        tbody.appendChild(tr);
    });
}
function renderLogsTable(list) {
    const tbody = document.getElementById('logs-list-body');
    tbody.innerHTML = '';
    if (list.length === 0) {
        tbody.innerHTML = `<tr><td colspan="4" class="empty-state">No matching hours logged.</td></tr>`;
        return;
    }
    // Sort descending by date
    const sortedLogs = [...list].reverse();
    sortedLogs.forEach(log => {
        const tr = document.createElement('tr');
        tr.innerHTML = `
            <td style="color: var(--text-secondary);">${log.date}</td>
            <td style="font-weight: 500;">${log.name}</td>
            <td style="font-family: monospace; font-size: 0.9rem;">${formatCnicDisplay(log.cnic)}</td>
            <td>
                <span class="slider-bubble" style="padding: 0.2rem 0.6rem; font-size: 0.8rem;">${log.hours} hrs</span>
            </td>
        `;
        tbody.appendChild(tr);
    });
}
function setupSearchFilters() {
    // Employees Search
    employeeSearchInput.addEventListener('input', (e) => {
        const query = e.target.value.toLowerCase().replace(/-/g, '');
        const filtered = employeesCache.filter(emp => 
            emp.name.toLowerCase().includes(query) || 
            emp.cnic.includes(query)
        );
        renderEmployeesTable(filtered);
    });
    // Logs Search
    logsSearchInput.addEventListener('input', (e) => {
        const query = e.target.value.toLowerCase().replace(/-/g, '');
        const filtered = logsCache.filter(log => 
            log.name.toLowerCase().includes(query) || 
            log.cnic.includes(query) ||
            log.date.includes(query)
        );
        renderLogsTable(filtered);
    });
}
// ==========================================
// Quick Link Event Actions
// ==========================================
window.quickLogHours = function(cnic) {
    switchTab('loghours');
    logCnicSelect.value = cnic;
};
window.quickCalculateSalary = function(cnic) {
    switchTab('calculate');
    calcCnicSelect.value = cnic;
};
// ==========================================
// Form Submission Handlers
// ==========================================
function setupFormSubmissions() {
    // 1. Employee Registration
    formRegister.addEventListener('submit', async (e) => {
        e.preventDefault();
        const name = regNameInput.value.trim();
        const cnic = regCnicInput.value.replace(/-/g, '').trim();
        const btnSubmit = document.getElementById('btn-submit-register');
        btnSubmit.disabled = true;
        try {
            const response = await fetch(`${API_URL}/api/register`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ name, cnic })
            });
            const result = await response.json();
            if (response.ok && result.success) {
                showToast(result.message, 'success');
                formRegister.reset();
                document.getElementById('cnic-validation-msg').textContent = 'Must be 13 digits (format: xxxxx-xxxxxxx-x).';
                document.getElementById('cnic-validation-msg').style.color = 'var(--text-muted)';
                await loadData();
                switchTab('dashboard');
            } else {
                showToast(result.message || 'Registration failed.', 'error');
            }
        } catch (error) {
            showToast('Server connection lost.', 'error');
        } finally {
            btnSubmit.disabled = false;
        }
    });
    // 2. Logging Hours
    formLogHours.addEventListener('submit', async (e) => {
        e.preventDefault();
        const cnic = logCnicSelect.value;
        const hours = logHoursInput.value;
        const btnSubmit = document.getElementById('btn-submit-log');
        btnSubmit.disabled = true;
        try {
            const response = await fetch(`${API_URL}/api/log-hours`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ cnic, hours })
            });
            const result = await response.json();
            if (response.ok && result.success) {
                showToast(result.message, 'success');
                formLogHours.reset();
                hoursBubble.textContent = '8 hrs';
                logHoursInput.value = 8;
                await loadData();
                switchTab('logs');
            } else {
                showToast(result.message || 'Logging hours failed.', 'error');
            }
        } catch (error) {
            showToast('Server connection lost.', 'error');
        } finally {
            btnSubmit.disabled = false;
        }
    });
    // 3. Calculating Salary
    formCalculate.addEventListener('submit', async (e) => {
        e.preventDefault();
        const cnic = calcCnicSelect.value;
        const rate = calcRateInput.value;
        const btnSubmit = document.getElementById('btn-submit-calc');
        btnSubmit.disabled = true;
        try {
            const response = await fetch(`${API_URL}/api/calculate-salary`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ cnic, rate })
            });
            const result = await response.json();
            if (response.ok && result.success) {
                showReceipt(result);
            } else {
                showToast(result.message || 'Calculation failed.', 'error');
            }
        } catch (error) {
            showToast('Server connection lost.', 'error');
        } finally {
            btnSubmit.disabled = false;
        }
    });
}
// ==========================================
// Modal Receipts & Print Setup
// ==========================================
function showReceipt(data) {
    receiptEmpName.textContent = data.name;
    receiptEmpCnic.textContent = `CNIC: ${formatCnicDisplay(data.cnic)}`;
    
    // Formatting today's date
    const today = new Date();
    const yyyy = today.getFullYear();
    let mm = today.getMonth() + 1;
    let dd = today.getDate();
    if (dd < 10) dd = '0' + dd;
    if (mm < 10) mm = '0' + mm;
    receiptDate.textContent = `${yyyy}-${mm}-${dd}`;
    
    receiptTotalHours.textContent = `${data.total_hours} Hours`;
    receiptRate.textContent = `Rs. ${parseFloat(data.rate).toLocaleString()}/hr`;
    receiptSalary.textContent = `Rs. ${parseFloat(data.salary).toLocaleString()}`;
    
    salaryModal.classList.add('active');
}
function setupModalEvents() {
    const hideModal = () => {
        salaryModal.classList.remove('active');
    };
    btnCloseModal.addEventListener('click', hideModal);
    btnDismissModal.addEventListener('click', hideModal);
    
    // Click outside modal card to close
    salaryModal.addEventListener('click', (e) => {
        if (e.target === salaryModal) {
            hideModal();
        }
    });
    // Print functionality
    btnPrintReceipt.addEventListener('click', () => {
        window.print();
    });
}
