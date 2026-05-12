const state = {
  books: [],
  allBooks: [],
  activeCategory: 'All',
  isAsking: false,
};

const elements = {
  books: document.getElementById('books'),
  bookSearch: document.getElementById('bookSearch'),
  catalogCount: document.getElementById('catalogCount'),
  catalogStatus: document.getElementById('catalogStatus'),
  categoryFilters: document.getElementById('categoryFilters'),
  totalBooksStat: document.getElementById('totalBooksStat'),
  availableCopiesStat: document.getElementById('availableCopiesStat'),
  unavailableBooksStat: document.getElementById('unavailableBooksStat'),
  categoryStat: document.getElementById('categoryStat'),
  searchForm: document.getElementById('searchForm'),
  studentId: document.getElementById('studentId'),
  messages: document.getElementById('messages'),
  typing: document.getElementById('typing'),
  chatForm: document.getElementById('chatForm'),
  question: document.getElementById('question'),
  sendButton: document.getElementById('sendButton'),
  clearChatButton: document.getElementById('clearChatButton'),
};

function escapeHtml(value) {
  return String(value)
    .replaceAll('&', '&amp;')
    .replaceAll('<', '&lt;')
    .replaceAll('>', '&gt;')
    .replaceAll('"', '&quot;')
    .replaceAll("'", '&#039;');
}

function formatCount(value, label) {
  return `${value} ${label}${value === 1 ? '' : 's'}`;
}

function getInitials(title) {
  return title
    .split(/\s+/)
    .filter(Boolean)
    .slice(0, 2)
    .map((part) => part[0].toUpperCase())
    .join('');
}

function getAvailabilityClass(book) {
  if (book.available_copies === 0) return 'unavailable';
  if (book.available_copies <= 1) return 'limited';
  return 'available';
}

function setCatalogStatus(message, tone = 'neutral') {
  elements.catalogStatus.textContent = message;
  elements.catalogStatus.dataset.tone = tone;
}

async function loadBooks(options = {}) {
  if (!options.silent) {
    setCatalogStatus('Loading catalog...');
  }

  const response = await fetch('/api/books');
  const books = await response.json();
  state.allBooks = books;
  renderCatalogStats(books);
  renderCategoryFilters(books);
  applyCatalogFilters({ silent: options.silent });

  if (!options.silent) {
    setCatalogStatus('Catalog is ready.', 'success');
  }
}

function renderCatalogStats(books) {
  const availableCopies = books.reduce((sum, book) => sum + book.available_copies, 0);
  const unavailableBooks = books.filter((book) => book.available_copies === 0).length;
  const categories = new Set(books.map((book) => book.category));

  elements.totalBooksStat.textContent = books.length;
  elements.availableCopiesStat.textContent = availableCopies;
  elements.unavailableBooksStat.textContent = unavailableBooks;
  elements.categoryStat.textContent = categories.size;
}

function renderCategoryFilters(books) {
  const categories = ['All', ...new Set(books.map((book) => book.category))];
  elements.categoryFilters.innerHTML = categories.map((category) => `
    <button class="chip ${category === state.activeCategory ? 'active' : ''}" type="button" data-category="${escapeHtml(category)}">
      ${escapeHtml(category)}
    </button>
  `).join('');
}

function applyCatalogFilters(options = {}) {
  const query = elements.bookSearch.value.trim().toLowerCase();
  const filteredBooks = state.allBooks.filter((book) => {
    const matchesCategory = state.activeCategory === 'All' || book.category === state.activeCategory;
    const matchesQuery = !query
      || book.title.toLowerCase().includes(query)
      || book.author.toLowerCase().includes(query)
      || book.category.toLowerCase().includes(query)
      || book.isbn.toLowerCase().includes(query);
    return matchesCategory && matchesQuery;
  });

  state.books = filteredBooks;
  renderBooks(filteredBooks);

  if (!options.silent) {
    setCatalogStatus(
      query || state.activeCategory !== 'All'
        ? `Showing ${formatCount(filteredBooks.length, 'match')}.`
        : 'Catalog is ready.',
      'success',
    );
  }
}

function renderBooks(books) {
  elements.catalogCount.textContent = formatCount(books.length, 'book');

  if (!books.length) {
    elements.books.innerHTML = '<div class="empty-state">No books matched your search.</div>';
    return;
  }

  elements.books.innerHTML = books.map((book, index) => {
    const availabilityClass = getAvailabilityClass(book);
    const isAvailable = book.available_copies > 0;
    const totalCopies = book.total_copies ?? book.available_copies;
    const copyText = `${book.available_copies}/${totalCopies} available`;

    return `
      <article class="book catalog-card" data-id="${escapeHtml(book.id)}" style="animation-delay:${index * 30}ms">
        <div class="catalog-card-main">
          <div class="catalog-spine" aria-hidden="true">${escapeHtml(getInitials(book.title))}</div>
          <div class="book-info">
            <div class="book-topline">
              <span class="book-category">${escapeHtml(book.category)}</span>
              <span class="avail-badge ${availabilityClass}"><span class="dot"></span>${escapeHtml(isAvailable ? copyText : 'Unavailable')}</span>
            </div>
            <h3>${escapeHtml(book.title)}</h3>
            <p>${escapeHtml(book.author)}</p>
            <dl>
              <div><dt>ISBN</dt><dd>${escapeHtml(book.isbn)}</dd></div>
              <div><dt>Copies</dt><dd>${escapeHtml(copyText)}</dd></div>
              <div><dt>Location</dt><dd>${escapeHtml(book.location)}</dd></div>
            </dl>
          </div>
        </div>
        <button class="secondary-button borrow-button" type="button" data-book-id="${escapeHtml(book.id)}" ${isAvailable ? '' : 'disabled'}>
          Borrow
        </button>
      </article>
    `;
  }).join('');
}

function addMessage(text, cls, sources = []) {
  const div = document.createElement('div');
  div.className = `msg ${cls}`;

  const bubble = document.createElement('div');
  bubble.className = 'msg-bubble';
  bubble.textContent = text;
  div.appendChild(bubble);

  if (cls === 'bot' && sources.length) {
    const sourceList = document.createElement('div');
    sourceList.className = 'sources-block';
    sourceList.innerHTML = `
      <div class="sources-title">Sources (${sources.length})</div>
      ${sources.map((source) => `
        <div class="source-item">${escapeHtml(source.source)}, page=${escapeHtml(source.page)}</div>
      `).join('')}
    `;
    div.appendChild(sourceList);
  }

  elements.messages.appendChild(div);
  elements.messages.scrollTop = elements.messages.scrollHeight;
}

function resetChat() {
  elements.messages.innerHTML = '';
  addMessage('Welcome. Ask me about borrowing, returning, admin roles, APIs, architecture, or deployment.', 'bot');
  elements.question.focus();
}

async function borrowBook(bookId) {
  const userId = elements.studentId.value.trim() || 'student-001';
  setCatalogStatus('Processing borrow request...');

  const response = await fetch('/api/borrow', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ user_id: userId, book_id: bookId }),
  });
  const result = await response.json();

  await loadBooks({ silent: true });
  setCatalogStatus(result.message, result.success ? 'success' : 'danger');
}

async function askBot(questionText) {
  const question = questionText || elements.question.value.trim();
  if (!question || state.isAsking) return;

  state.isAsking = true;
  elements.sendButton.disabled = true;
  addMessage(question, 'user');
  elements.question.value = '';
  elements.typing.classList.remove('hidden');

  try {
    const response = await fetch('/api/chat', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ question }),
    });
    if (!response.ok) {
      const error = await response.json().catch(() => ({}));
      throw new Error(error.detail || `Chat API failed with status ${response.status}.`);
    }
    const data = await response.json();
    addMessage(data.answer, 'bot', data.sources || []);
  } catch (err) {
    addMessage(`Error: ${err.message}`, 'bot');
  } finally {
    state.isAsking = false;
    elements.sendButton.disabled = false;
    elements.typing.classList.add('hidden');
    elements.question.focus();
  }
}

elements.searchForm.addEventListener('submit', (event) => {
  event.preventDefault();
  applyCatalogFilters();
});

elements.bookSearch.addEventListener('input', () => applyCatalogFilters({ silent: true }));

elements.categoryFilters.addEventListener('click', (event) => {
  const button = event.target.closest('[data-category]');
  if (!button) return;
  state.activeCategory = button.dataset.category;
  renderCategoryFilters(state.allBooks);
  applyCatalogFilters();
});

elements.books.addEventListener('click', (event) => {
  const button = event.target.closest('[data-book-id]');
  if (!button) return;
  borrowBook(button.dataset.bookId);
});

elements.chatForm.addEventListener('submit', (event) => {
  event.preventDefault();
  askBot();
});

elements.clearChatButton.addEventListener('click', resetChat);

document.querySelectorAll('[data-question]').forEach((button) => {
  button.addEventListener('click', () => askBot(button.dataset.question));
});

resetChat();
loadBooks();
