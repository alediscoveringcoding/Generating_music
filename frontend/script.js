/**
 * AI Music Generator - Frontend JavaScript
 * Gestionează comunicarea cu backend-ul și interfața utilizatorului
 */

// Configurare
const API_BASE_URL = "http://127.0.0.1:8000";
const POLL_INTERVAL = 5000; // 5 secunde

// State
let currentGenre = null;
let currentFile = null;
let isGenerating = false;
let genres = {};
let pollInterval = null;

// ============================================
// Inițializare
// ============================================

document.addEventListener("DOMContentLoaded", async () => {
    console.log("🎵 AI Music Generator - Inițializare...");
    
    // Șterge stateful state
    clearStatus();
    
    // Încarcă genurile
    await loadGenres();
    
    // Încarcă istoricul
    await loadHistory();
    
    // Verifică starea serverului
    await checkServerHealth();
    
    // Pornește polling-ul pentru actualizări
    startPolling();
});

// ============================================
// Gestionare Genuri
// ============================================

async function loadGenres() {
    try {
        showStatus("Se încarcă genurile...", "loading");
        console.log("🎵 Fetching genres from:", `${API_BASE_URL}/genres`);
        
        const response = await fetch(`${API_BASE_URL}/genres`);
        console.log("Response status:", response.status);
        
        if (!response.ok) {
            const errorText = await response.text();
            throw new Error(`HTTP ${response.status}: ${errorText}`);
        }
        
        const data = await response.json();
        console.log("Genres data:", data);
        
        // Suportă ambele formate: data.genres și data direct
        genres = data.genres || data;
        console.log("Parsed genres:", genres);
        
        if (!genres || Object.keys(genres).length === 0) {
            throw new Error("Nici un gen disponibil din server");
        }
        
        // Populează dropdown-ul
        const genreSelect = document.getElementById("genre");
        if (!genreSelect) {
            throw new Error("Element 'genre' select nu găsit în DOM");
        }
        
        genreSelect.innerHTML = '<option value="">-- Alege un gen --</option>';
        
        Object.keys(genres).forEach(genre => {
            const option = document.createElement("option");
            option.value = genre;
            option.textContent = genre.charAt(0).toUpperCase() + genre.slice(1);
            genreSelect.appendChild(option);
        });
        
        // Adaugă event listener
        genreSelect.addEventListener("change", onGenreChange);
        
        clearStatus();
        console.log(`✓ ${Object.keys(genres).length} genuri încărcate`);
        showStatus(`✅ ${Object.keys(genres).length} genuri disponibile`, "success");
        
    } catch (error) {
        console.error("❌ Eroare genuri:", error);
        showStatus("Eroare la preluare genuri: " + error.message, "error");
        // Afișează messag de eroare persistent
        setTimeout(() => {
            const statusDiv = document.getElementById("status");
            if (statusDiv) {
                statusDiv.style.display = "block";
            }
        }, 100);
    }
}

function onGenreChange(event) {
    currentGenre = event.target.value;
    
    if (!currentGenre || !genres[currentGenre]) {
        document.getElementById("genre-description").textContent = "";
        return;
    }
    
    const genreInfo = genres[currentGenre];
    document.getElementById("genre-description").textContent = 
        `ℹ️ ${genreInfo.description} (Temp: ${genreInfo.default_temperature}, Steps: ${genreInfo.default_steps})`;
}

// ============================================
// Gestionare Opțiuni Avansate
// ============================================

function toggleAdvanced() {
    const panel = document.getElementById("advanced-panel");
    panel.classList.toggle("hidden");
}

function updateTempValue(value) {
    document.getElementById("temp-value").textContent = parseFloat(value).toFixed(1);
}

function updateStepsValue(value) {
    document.getElementById("steps-value").textContent = value;
}

function updateSeedValue(value) {
    const noteNames = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"];
    const octave = Math.floor(value / 12) - 1;
    const noteName = noteNames[value % 12];
    document.getElementById("seed-value").textContent = `${value} (${noteName}${octave})`;
}

// ============================================
// Generare Muzică
// ============================================

async function generateMusic() {
    if (!currentGenre) {
        showStatus("Selectează un gen muzical!", "error");
        return;
    }
    
    if (isGenerating) {
        showStatus("O generare este în curs...", "warning");
        return;
    }
    
    try {
        isGenerating = true;
        updateGenerateButton();
        
        const temperature = parseFloat(document.getElementById("temperature").value);
        const steps = parseInt(document.getElementById("steps").value);
        const seedNote = parseInt(document.getElementById("seed-note").value);
        
        showStatus(`🎹 Generând muzică ${currentGenre}...`, "loading");
        
        const response = await fetch(`${API_BASE_URL}/generate`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                genre: currentGenre,
                temperature: temperature,
                steps: steps,
                seed_note: seedNote
            })
        });
        
        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.detail || "Eroare generare");
        }
        
        const data = await response.json();
        
        if (!data.success) {
            throw new Error(data.message || "Generare eșuată");
        }
        
        // Salvează fișierul curent
        currentFile = data.metadata;
        
        // Încarcă audiofile-ul
        const audioResponse = await fetch(
            `${API_BASE_URL}/download/${data.metadata.filename}`
        );
        const audioBlob = await audioResponse.blob();
        
        const player = document.getElementById("player");
        player.src = URL.createObjectURL(audioBlob);
        
        // Actualizează UI
        updateNowPlaying(data.metadata.filename);
        document.getElementById("download-btn").disabled = false;
        document.getElementById("delete-btn").disabled = false;
        
        showStatus(
            `✨ Muzică ${currentGenre} generată cu succes! (${(data.metadata.file_size / 1024).toFixed(2)} KB)`,
            "success"
        );
        
        // Joacă automat
        player.play().catch(e => console.log("Autoplay blocat:", e));
        
        // Reîncarcă istoric
        await loadHistory();
        
    } catch (error) {
        console.error("Eroare generare:", error);
        showStatus("Eroare generare: " + error.message, "error");
    } finally {
        isGenerating = false;
        updateGenerateButton();
    }
}

function stopGeneration() {
    isGenerating = false;
    updateGenerateButton();
    showStatus("Generare anulată", "warning");
}

function updateGenerateButton() {
    const generateBtn = document.getElementById("generate-btn");
    const stopBtn = document.getElementById("stop-btn");
    
    if (isGenerating) {
        generateBtn.classList.add("hidden");
        stopBtn.classList.remove("hidden");
    } else {
        generateBtn.classList.remove("hidden");
        stopBtn.classList.add("hidden");
    }
}

// ============================================
// Descărcare și Ștergere
// ============================================

async function downloadCurrentMusic() {
    if (!currentFile) {
        showStatus("Nicio muzică de descărcat", "error");
        return;
    }
    
    try {
        const link = document.createElement("a");
        link.href = `${API_BASE_URL}/download/${currentFile.filename}`;
        link.download = currentFile.filename;
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
        
        showStatus("📥 Descărcarea a început...", "success");
    } catch (error) {
        console.error("Eroare descărcare:", error);
        showStatus("Eroare descărcare: " + error.message, "error");
    }
}

async function deleteCurrentMusic() {
    if (!currentFile) {
        showStatus("Nicio muzică de șters", "error");
        return;
    }
    
    if (!confirm(`Ești sigur că vrei să ștergi ${currentFile.filename}?`)) {
        return;
    }
    
    try {
        showStatus("Se șterge fișierul...", "loading");
        
        const response = await fetch(
            `${API_BASE_URL}/delete/${currentFile.filename}`,
            { method: "DELETE" }
        );
        
        if (!response.ok) throw new Error("Eroare ștergere");
        
        // Curăță player
        document.getElementById("player").src = "";
        updateNowPlaying("Nicio muzică în redare...");
        document.getElementById("download-btn").disabled = true;
        document.getElementById("delete-btn").disabled = true;
        
        currentFile = null;
        
        showStatus("🗑️ Fișier șters cu succes", "success");
        
        // Reîncarcă istoric
        await loadHistory();
        
    } catch (error) {
        console.error("Eroare ștergere:", error);
        showStatus("Eroare ștergere: " + error.message, "error");
    }
}

// ============================================
// Istoric
// ============================================

async function loadHistory() {
    try {
        const response = await fetch(`${API_BASE_URL}/history?limit=10`);
        if (!response.ok) throw new Error("Eroare la preluare istoric");
        
        const data = await response.json();
        const historyList = document.getElementById("history-list");
        
        if (data.count === 0) {
            historyList.innerHTML = '<p class="empty-message">Nu există înregistrări în istoric. Generează o melodie!</p>';
            return;
        }
        
        historyList.innerHTML = data.history.reverse().map(item => `
            <div class="history-item" onclick="playFromHistory('${item.filename}')">
                <div class="history-item-info">
                    <div class="history-item-genre">🎵 ${item.genre.toUpperCase()}</div>
                    <div class="history-item-time">${new Date(item.timestamp).toLocaleString('ro-RO')}</div>
                </div>
                <div class="history-item-actions">
                    <button onclick="event.stopPropagation(); playFromHistory('${item.filename}')">▶️ Play</button>
                    <button onclick="event.stopPropagation(); downloadFromHistory('${item.filename}')">📥</button>
                    <button onclick="event.stopPropagation(); deleteFromHistory('${item.filename}')">🗑️</button>
                </div>
            </div>
        `).join("");
        
    } catch (error) {
        console.error("Eroare istoric:", error);
        document.getElementById("history-list").innerHTML = 
            '<p class="empty-message">Eroare la preluare istoric</p>';
    }
}

async function playFromHistory(filename) {
    try {
        const response = await fetch(`${API_BASE_URL}/download/${filename}`);
        const blob = await response.blob();
        
        const player = document.getElementById("player");
        player.src = URL.createObjectURL(blob);
        player.play();
        
        updateNowPlaying(filename);
        document.getElementById("download-btn").disabled = false;
        document.getElementById("delete-btn").disabled = false;
        
        currentFile = { filename: filename };
        
    } catch (error) {
        console.error("Eroare play din istoric:", error);
        showStatus("Eroare redare", "error");
    }
}

async function downloadFromHistory(filename) {
    const link = document.createElement("a");
    link.href = `${API_BASE_URL}/download/${filename}`;
    link.download = filename;
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
}

async function deleteFromHistory(filename) {
    if (!confirm(`Ești sigur că vrei să ștergi ${filename}?`)) return;
    
    try {
        await fetch(`${API_BASE_URL}/delete/${filename}`, { method: "DELETE" });
        await loadHistory();
        showStatus("Fișier șters", "success");
    } catch (error) {
        showStatus("Eroare ștergere", "error");
    }
}

function clearHistoryUI() {
    document.getElementById("history-list").innerHTML = 
        '<p class="empty-message">Lista golită din UI (fișierele rămân pe server)</p>';
}

function updateNowPlaying(filename) {
    document.getElementById("now-playing").textContent = `🎵 Redare: ${filename}`;
}

// ============================================
// Statistici
// ============================================


async function checkServerHealth() {
    try {
        const response = await fetch(`${API_BASE_URL}/health`);
        const data = await response.json();
        
        const healthEl = document.getElementById("stat-health");
        if (data.status === "healthy") {
            healthEl.textContent = "🟢 Online";
            healthEl.style.color = "var(--success-color)";
        } else {
            healthEl.textContent = "🟡 Caution";
        }
    } catch (error) {
        console.error("Server offline:", error);
        document.getElementById("stat-health").textContent = "🔴 Offline";
    }
}

// ============================================
// Polling și Actualizări
// ============================================

function startPolling() {
    // Verifică status server la fiecare 5 secunde
    pollInterval = setInterval(async () => {
        await checkServerHealth();
    }, POLL_INTERVAL);
}

function stopPolling() {
    if (pollInterval) {
        clearInterval(pollInterval);
    }
}

// ============================================
// Status Messages
// ============================================

function showStatus(message, type = "info") {
    const status = document.getElementById("status");
    status.textContent = message;
    status.className = `status-message ${type}`;
}

function clearStatus() {
    const status = document.getElementById("status");
    status.textContent = "";
    status.className = "status-message";
}

// ============================================
// Cleanup
// ============================================

window.addEventListener("beforeunload", () => {
    stopPolling();
});

// ============================================
// Keyboard Shortcuts
// ============================================

document.addEventListener("keydown", (e) => {
    // Space bar pentru generate
    if (e.code === "Space" && !e.ctrlKey && !e.shiftKey && document.activeElement.tagName !== "INPUT") {
        e.preventDefault();
        if (!isGenerating && currentGenre) {
            generateMusic();
        }
    }
    
    // Ctrl+Shift+H pentru reîncarcă istoric
    if (e.ctrlKey && e.shiftKey && e.key === "H") {
        e.preventDefault();
        loadHistory();
    }
});

// ============================================
// Logging
// ============================================

console.log("🎵 AI Music Generator v1.0");
console.log("API: " + API_BASE_URL);
console.log("Shortcut: Space = Generate | Ctrl+Shift+H = Reload History");
