const reminderInput = document.getElementById('reminder-time');
const saveButton = document.getElementById('save-reminder');
const showNowButton = document.getElementById('show-now');
const nextReminderEl = document.getElementById('next-reminder');
const wordListEl = document.getElementById('word-list');
const reminderStatusEl = document.getElementById('reminder-status');
const progressSummaryEl = document.getElementById('progress-summary');
const progressBarFill = document.getElementById('progress-bar-fill');
const historyListEl = document.getElementById('history-list');
const historyEmptyEl = document.getElementById('history-empty');
const notificationStatusEl = document.getElementById('notification-status');
const emailListTextarea = document.getElementById('email-list');
const emailSubjectInput = document.getElementById('email-subject');
const sendEmailButton = document.getElementById('send-email');
const emailStatusEl = document.getElementById('email-status');

const STORAGE_KEY = 'english-word-reminder';
const DAILY_WORDS_KEY = 'english-word-reminder-words';
const PROGRESS_KEY = 'english-word-reminder-progress';
const HISTORY_KEY = 'english-word-reminder-history';
const SHOWN_DAY_KEY = 'english-word-reminder-shown-date';
const EMAIL_RECIPIENTS_KEY = 'english-word-reminder-email-recipients';

function pad(value) {
    return value.toString().padStart(2, '0');
}

function getTodayKey() {
    const now = new Date();
    return `${now.getFullYear()}-${pad(now.getMonth() + 1)}-${pad(now.getDate())}`;
}

function getReminderData() {
    try {
        return JSON.parse(localStorage.getItem(STORAGE_KEY)) || {};
    } catch (error) {
        return {};
    }
}

function saveReminder(time) {
    localStorage.setItem(STORAGE_KEY, JSON.stringify({ time }));
}

function getDailyWords() {
    const key = getTodayKey();
    const stored = JSON.parse(localStorage.getItem(DAILY_WORDS_KEY) || '{}');
    if (stored.date === key && Array.isArray(stored.words)) {
        return stored.words;
    }
    const shuffled = [...words].sort(() => Math.random() - 0.5);
    const todayWords = shuffled.slice(0, dailyWordCount);
    localStorage.setItem(DAILY_WORDS_KEY, JSON.stringify({ date: key, words: todayWords }));
    return todayWords;
}

function getProgressData() {
    try {
        return JSON.parse(localStorage.getItem(PROGRESS_KEY)) || {};
    } catch (error) {
        return {};
    }
}

function getTodayProgress() {
    const data = getProgressData();
    return Array.isArray(data[getTodayKey()]) ? data[getTodayKey()] : [];
}

function saveTodayProgress(progress) {
    const data = getProgressData();
    data[getTodayKey()] = progress;
    localStorage.setItem(PROGRESS_KEY, JSON.stringify(data));
}

function getEmailRecipients() {
    return localStorage.getItem(EMAIL_RECIPIENTS_KEY) || '';
}

function saveEmailRecipients(value) {
    localStorage.setItem(EMAIL_RECIPIENTS_KEY, value);
}

function parseRecipients(raw) {
    return raw
        .replace(/\s+/g, ',')
        .split(',')
        .map(item => item.trim())
        .filter(Boolean);
}

function toggleLearned(word) {
    const progress = getTodayProgress();
    const index = progress.indexOf(word);
    if (index >= 0) {
        progress.splice(index, 1);
    } else {
        progress.push(word);
    }
    saveTodayProgress(progress);
    updateProgressSummary();
    renderWords(getDailyWords());
}

function getHistory() {
    try {
        return JSON.parse(localStorage.getItem(HISTORY_KEY)) || [];
    } catch (error) {
        return [];
    }
}

function addHistory(action) {
    const history = getHistory();
    history.unshift({ timestamp: new Date().toISOString(), action });
    localStorage.setItem(HISTORY_KEY, JSON.stringify(history.slice(0, 20)));
    renderHistory();
}

function renderHistory() {
    const history = getHistory();
    historyListEl.innerHTML = '';
    if (history.length === 0) {
        historyEmptyEl.style.display = 'block';
        return;
    }
    historyEmptyEl.style.display = 'none';
    history.forEach(entry => {
        const item = document.createElement('li');
        item.className = 'history-item';
        item.innerHTML = `<span class="history-action">${entry.action}</span><span class="history-time">${new Date(entry.timestamp).toLocaleString()}</span>`;
        historyListEl.appendChild(item);
    });
}

function updateProgressSummary() {
    const learnedCount = getTodayProgress().length;
    progressSummaryEl.textContent = `${learnedCount} of ${dailyWordCount} words learned today.`;
    const percent = Math.round((learnedCount / dailyWordCount) * 100);
    progressBarFill.style.width = `${percent}%`;
}

function renderWords(wordsToShow) {
    wordListEl.innerHTML = '';
    const progress = getTodayProgress();
    wordsToShow.forEach(word => {
        const learned = progress.includes(word);
        const card = document.createElement('div');
        card.className = 'word-card';

        const title = document.createElement('div');
        title.className = 'word-title';
        title.textContent = word;

        const definition = document.createElement('div');
        definition.className = 'word-definition';
        definition.textContent = wordDefinitions[word] || 'No definition available.';

        const actions = document.createElement('div');
        actions.className = 'word-actions';

        const button = document.createElement('button');
        button.type = 'button';
        button.className = `word-button ${learned ? 'learned' : 'unlearned'}`;
        button.textContent = learned ? 'Mark as not learned' : 'Mark as learned';
        button.addEventListener('click', () => toggleLearned(word));

        actions.appendChild(button);
        card.appendChild(title);
        card.appendChild(definition);
        card.appendChild(actions);
        wordListEl.appendChild(card);
    });
}

function hideWords() {
    wordListEl.innerHTML = '';
}

function updateReminderDisplay(reminderTime) {
    if (!reminderTime) {
        nextReminderEl.textContent = 'No reminder set yet.';
        reminderStatusEl.textContent = 'Set a time and keep this page open to receive the alert.';
        hideWords();
        return;
    }
    nextReminderEl.textContent = `Reminder set for ${reminderTime} every day.`;
}

function hasReminderPassed(reminderTime) {
    if (!reminderTime) return false;
    const [hour, minute] = reminderTime.split(':').map(Number);
    const now = new Date();
    const target = new Date(now);
    target.setHours(hour, minute, 0, 0);
    return now >= target;
}

function updateNotificationStatus() {
    if (!('Notification' in window)) {
        notificationStatusEl.textContent = 'Browser notifications are not supported in this browser.';
        return;
    }
    if (Notification.permission === 'granted') {
        notificationStatusEl.textContent = 'Notifications enabled. You will receive alerts at reminder time.';
    } else if (Notification.permission === 'denied') {
        notificationStatusEl.textContent = 'Notifications blocked. Please allow them in browser settings.';
    } else {
        notificationStatusEl.textContent = 'Notifications are ready. Save a reminder to request permission.';
    }
}

function requestNotificationPermission() {
    if ('Notification' in window && Notification.permission === 'default') {
        Notification.requestPermission().then(() => updateNotificationStatus());
    }
}

function sendNotification(message) {
    if ('Notification' in window && Notification.permission === 'granted') {
        new Notification('English Word Reminder', { body: message });
    }
}

function markTodayWordsShown() {
    localStorage.setItem(SHOWN_DAY_KEY, getTodayKey());
}

function hasShownToday() {
    return localStorage.getItem(SHOWN_DAY_KEY) === getTodayKey();
}

function checkReminder() {
    const reminderData = getReminderData();
    const reminderTime = reminderData.time;
    const todayWords = getDailyWords();

    if (!reminderTime) {
        updateReminderDisplay(null);
        return;
    }

    reminderInput.value = reminderTime;
    updateReminderDisplay(reminderTime);

    if (hasReminderPassed(reminderTime)) {
        renderWords(todayWords);
        updateProgressSummary();
        reminderStatusEl.textContent = 'Reminder time has arrived! Study your 5 words now.';
        sendNotification('It is time to study your 5 English words.');
        if (!hasShownToday()) {
            addHistory('Reminder triggered and words shown');
            markTodayWordsShown();
        }
        return;
    }

    hideWords();
    const now = new Date();
    const [hour, minute] = reminderTime.split(':').map(Number);
    const target = new Date(now);
    target.setHours(hour, minute, 0, 0);
    const diffMinutes = Math.ceil((target - now) / 60000);
    reminderStatusEl.textContent = `Your words will appear at ${reminderTime}. (${diffMinutes} minutes remaining)`;
}

function setEmailStatus(message, isError = false) {
    emailStatusEl.textContent = message;
    emailStatusEl.style.color = isError ? '#b91c1c' : '#475569';
}

async function sendEmailReminder() {
    const recipients = parseRecipients(emailListTextarea.value);
    const wordsToSend = getDailyWords();

    if (recipients.length === 0) {
        setEmailStatus('Please add at least one valid email address.', true);
        return;
    }

    if (wordsToSend.length === 0) {
        setEmailStatus('No words available to send.', true);
        return;
    }

    const subject = emailSubjectInput.value.trim() || 'Daily English Word Reminder';
    setEmailStatus('Sending email reminder…');
    sendEmailButton.disabled = true;

    try {
        const response = await fetch('/send-email', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                recipients: recipients.join(','),
                subject,
                words: wordsToSend,
            }),
        });

        const data = await response.json();
        if (response.ok && data.success) {
            setEmailStatus('Email reminder sent successfully.');
            saveEmailRecipients(emailListTextarea.value);
            addHistory(`Sent email reminder to ${recipients.length} address${recipients.length === 1 ? '' : 'es'}`);
        } else {
            setEmailStatus(data.error || 'Unable to send email reminder.', true);
        }
    } catch (error) {
        setEmailStatus('Network error. Please try again later.', true);
    } finally {
        sendEmailButton.disabled = false;
    }
}

saveButton.addEventListener('click', () => {
    const time = reminderInput.value;
    if (!time) {
        alert('Please choose a valid reminder time.');
        return;
    }
    saveReminder(time);
    updateReminderDisplay(time);
    reminderStatusEl.textContent = 'Reminder saved! Keep the page open to receive the alert.';
    addHistory(`Reminder saved for ${time}`);
    requestNotificationPermission();
});

showNowButton.addEventListener('click', () => {
    renderWords(getDailyWords());
    updateProgressSummary();
    reminderStatusEl.textContent = 'Showing today’s words now. Study them whenever you are ready.';
    addHistory('Viewed today’s words manually');
});

sendEmailButton.addEventListener('click', sendEmailReminder);

window.addEventListener('load', () => {
    emailListTextarea.value = getEmailRecipients();
    updateNotificationStatus();
    requestNotificationPermission();
    renderHistory();
    updateProgressSummary();
    checkReminder();
    setInterval(checkReminder, 30000);
});
