const adminState = {
  token: localStorage.getItem('rag_admin_token'),
  username: localStorage.getItem('rag_admin_username'),
  pendingAction: 'borrow',
};

const adminEls = {
  loginView: document.getElementById('loginView'),
  dashboardView: document.getElementById('dashboardView'),
  loginForm: document.getElementById('loginForm'),
  loginError: document.getElementById('loginError'),
  adminUsername: document.getElementById('adminUsername'),
  adminPassword: document.getElementById('adminPassword'),
  logoutButton: document.getElementById('logoutButton'),
  adminMeta: document.getElementById('adminMeta'),
  stats: document.getElementById('stats'),
  adminInsightCards: document.getElementById('adminInsightCards'),
  adminBooks: document.getElementById('adminBooks'),
  categoryBreakdown: document.getElementById('categoryBreakdown'),
  lowStockList: document.getElementById('lowStockList'),
  activityList: document.getElementById('activityList'),
  systemList: document.getElementById('systemList'),
  operationForm: document.getElementById('operationForm'),
  operationUserId: document.getElementById('operationUserId'),
  operationBookId: document.getElementById('operationBookId'),
  operationStatus: document.getElementById('operationStatus'),
};

function escapeHtml(value) {
  return String(value)
    .replaceAll('&', '&amp;')
    .replaceAll('<', '&lt;')
    .replaceAll('>', '&gt;')
    .replaceAll('"', '&quot;')
    .replaceAll("'", '&#039;');
}

function authHeaders() {
  return {
    Authorization: `Bearer ${adminState.token}`,
  };
}

function showLogin(message = '') {
  adminEls.loginView.classList.remove('hidden');
  adminEls.dashboardView.classList.add('hidden');
  adminEls.loginError.textContent = message;
  adminEls.adminPassword.value = '';
  adminEls.adminUsername.focus();
}

function showDashboard() {
  adminEls.loginView.classList.add('hidden');
  adminEls.dashboardView.classList.remove('hidden');
}

async function login(username, password) {
  const response = await fetch('/api/admin/login', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ username, password }),
  });

  if (!response.ok) {
    throw new Error('Username or password is incorrect.');
  }

  const data = await response.json();
  adminState.token = data.token;
  adminState.username = data.username;
  localStorage.setItem('rag_admin_token', data.token);
  localStorage.setItem('rag_admin_username', data.username);
}

async function logout() {
  if (adminState.token) {
    await fetch('/api/admin/logout', {
      method: 'POST',
      headers: authHeaders(),
    });
  }

  adminState.token = null;
  adminState.username = null;
  localStorage.removeItem('rag_admin_token');
  localStorage.removeItem('rag_admin_username');
  showLogin();
}

async function loadDashboard() {
  if (!adminState.token) {
    showLogin();
    return;
  }

  const response = await fetch('/api/admin/summary', {
    headers: authHeaders(),
  });

  if (response.status === 401) {
    await logout();
    showLogin('Session expired. Please sign in again.');
    return;
  }

  const data = await response.json();
  renderDashboard(data);
  showDashboard();
}

function groupByCategory(books) {
  return books.reduce((groups, book) => {
    const current = groups[book.category] || { books: 0, total: 0, available: 0 };
    current.books += 1;
    current.total += book.total_copies ?? book.available_copies;
    current.available += book.available_copies;
    groups[book.category] = current;
    return groups;
  }, {});
}

function renderDashboard(data) {
  const borrowedCopies = data.totals.total_copies - data.totals.available_copies;
  const utilization = data.totals.total_copies
    ? Math.round((borrowedCopies / data.totals.total_copies) * 100)
    : 0;

  adminEls.adminMeta.textContent = `Signed in as ${data.admin.username}`;
  adminEls.stats.innerHTML = [
    ['Books', data.totals.books, 'BK', 'blue', 'Catalog records'],
    ['Total copies', data.totals.total_copies, 'CP', 'teal', 'Physical inventory'],
    ['Available', data.totals.available_copies, 'AV', 'green', 'Ready to borrow'],
    ['Active borrows', data.totals.active_borrows, 'BR', 'amber', 'Open circulation'],
  ].map(([label, value, icon, tone, delta]) => `
    <article class="stat-card ${tone}">
      <div class="stat-top">
        <span class="stat-label">${escapeHtml(label)}</span>
        <span class="stat-icon">${escapeHtml(icon)}</span>
      </div>
      <strong class="stat-value">${escapeHtml(value)}</strong>
      <span class="stat-delta">${escapeHtml(delta)}</span>
    </article>
  `).join('');

  adminEls.adminInsightCards.innerHTML = [
    ['Circulation utilization', `${utilization}%`, 'Borrowed copies divided by all copies'],
    ['Unavailable books', data.totals.unavailable_books, 'Titles with zero available copies'],
    ['Returned records', data.totals.returned, 'Closed borrow transactions'],
  ].map(([label, value, note]) => `
    <article class="insight-card">
      <span>${escapeHtml(label)}</span>
      <strong>${escapeHtml(value)}</strong>
      <p>${escapeHtml(note)}</p>
    </article>
  `).join('');

  adminEls.adminBooks.innerHTML = data.books.map((book) => {
    const totalCopies = book.total_copies ?? book.available_copies;
    const availablePercent = totalCopies ? Math.round((book.available_copies / totalCopies) * 100) : 0;
    return `
      <tr>
        <td>
          <strong class="table-book-title">${escapeHtml(book.title)}</strong>
          <small>${escapeHtml(book.id)} - ${escapeHtml(book.isbn)}</small>
        </td>
        <td>${escapeHtml(book.author)}</td>
        <td><span class="book-category">${escapeHtml(book.category)}</span></td>
        <td>
          <div class="copy-meter">
            <span>${escapeHtml(book.available_copies)} / ${escapeHtml(totalCopies)}</span>
            <div class="progress-bar"><div class="progress-fill" style="width:${availablePercent}%"></div></div>
          </div>
        </td>
        <td>${escapeHtml(book.location)}</td>
      </tr>
    `;
  }).join('');

  renderCategoryBreakdown(data.books);
  renderLowStock(data.books);
  renderActivity(data.borrowed);
  renderSystem(data.system);
}

function renderCategoryBreakdown(books) {
  const groups = groupByCategory(books);
  adminEls.categoryBreakdown.innerHTML = Object.entries(groups).map(([category, value]) => {
    const borrowed = value.total - value.available;
    const utilization = value.total ? Math.round((borrowed / value.total) * 100) : 0;
    return `
      <article class="category-row">
        <div>
          <strong>${escapeHtml(category)}</strong>
          <span>${escapeHtml(value.books)} titles - ${escapeHtml(value.available)} available copies</span>
        </div>
        <div class="category-progress">
          <div class="progress-bar"><div class="progress-fill" style="width:${utilization}%"></div></div>
          <span>${escapeHtml(utilization)}%</span>
        </div>
      </article>
    `;
  }).join('');
}

function renderLowStock(books) {
  const lowStock = books
    .filter((book) => book.available_copies <= 1)
    .sort((a, b) => a.available_copies - b.available_copies);

  if (!lowStock.length) {
    adminEls.lowStockList.innerHTML = '<div class="empty-state">All tracked titles have comfortable availability.</div>';
    return;
  }

  adminEls.lowStockList.innerHTML = lowStock.map((book) => `
    <article class="stock-item ${book.available_copies === 0 ? 'is-empty' : ''}">
      <strong>${escapeHtml(book.title)}</strong>
      <span>${escapeHtml(book.available_copies)} copies available - ${escapeHtml(book.location)}</span>
    </article>
  `).join('');
}

function renderActivity(borrowed) {
  if (borrowed.length) {
    adminEls.activityList.innerHTML = borrowed.map((item) => `
      <article class="activity-item">
        <strong>${escapeHtml(item.book_title || item.book_id)}</strong>
        <span>${escapeHtml(item.user_id)} - ${escapeHtml(item.status)}</span>
      </article>
    `).join('');
  } else {
    adminEls.activityList.innerHTML = '<div class="empty-state">No borrowing activity yet.</div>';
  }
}

function renderSystem(system) {
  adminEls.systemList.innerHTML = [
    ['Backend', system.backend],
    ['LLM', system.llm_model],
    ['Embedding', system.embedding_model],
    ['Vector DB', system.vector_database],
  ].map(([label, value]) => `
    <div>
      <dt>${escapeHtml(label)}</dt>
      <dd>${escapeHtml(value)}</dd>
    </div>
  `).join('');
}

async function submitOperation(action) {
  const userId = adminEls.operationUserId.value.trim();
  const bookId = adminEls.operationBookId.value.trim();
  if (!userId || !bookId) return;

  adminEls.operationStatus.textContent = 'Processing operation...';
  adminEls.operationStatus.dataset.tone = 'neutral';

  const response = await fetch(`/api/${action}`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ user_id: userId, book_id: bookId }),
  });
  const result = await response.json();
  adminEls.operationStatus.textContent = result.message;
  adminEls.operationStatus.dataset.tone = result.success ? 'success' : 'danger';
  await loadDashboard();
}

adminEls.loginForm.addEventListener('submit', async (event) => {
  event.preventDefault();
  adminEls.loginError.textContent = '';
  try {
    await login(adminEls.adminUsername.value.trim(), adminEls.adminPassword.value);
    await loadDashboard();
  } catch (err) {
    showLogin(err.message);
  }
});

adminEls.logoutButton.addEventListener('click', logout);

adminEls.operationForm.addEventListener('click', (event) => {
  const button = event.target.closest('[data-action]');
  if (button) {
    adminState.pendingAction = button.dataset.action;
  }
});

adminEls.operationForm.addEventListener('submit', (event) => {
  event.preventDefault();
  submitOperation(adminState.pendingAction);
});

loadDashboard();
