const form = document.getElementById('ttsForm');
const generateBtn = document.getElementById('generateBtn');
const btnContent = document.querySelector('.btn-content');
const loader = document.getElementById('loader');
const resultSection = document.getElementById('resultSection');
const audioPlayer = document.getElementById('audioPlayer');
const emotionLabel = document.getElementById('emotionLabel');
const emotionEmoji = document.getElementById('emotionEmoji');
const waveform = document.getElementById('waveform');
const textInput = document.getElementById('textInput');
const charCount = document.getElementById('charCount');
const paramPitch = document.getElementById('paramPitch');
const paramGain = document.getElementById('paramGain');
const paramRate = document.getElementById('paramRate');
const confidenceValue = document.getElementById('confidenceValue');
const scoresGrid = document.getElementById('scoresGrid');
const intensityFill = document.getElementById('intensityFill');
const intensityPercent = document.getElementById('intensityPercent');
const emojiExplosion = document.getElementById('emojiExplosion');

const EMOTION_CONFIG = {
    joy:      { emoji: '😄', emojis: ['🎉', '✨', '🥳', '💛', '🌟', '😁'], color: '#fbbf24' },
    sadness:  { emoji: '😢', emojis: ['💧', '🌧️', '😞', '💙', '🥀'],      color: '#60a5fa' },
    anger:    { emoji: '😡', emojis: ['🔥', '💢', '⚡', '😤', '💥'],       color: '#f87171' },
    fear:     { emoji: '😰', emojis: ['😱', '👻', '💜', '🫣', '😨'],       color: '#c084fc' },
    surprise: { emoji: '😲', emojis: ['🤯', '⭐', '🎊', '😮', '💫'],      color: '#fb923c' },
    disgust:  { emoji: '🤢', emojis: ['🤮', '😖', '💚', '🫠', '😬'],      color: '#a3e635' },
    neutral:  { emoji: '😐', emojis: ['🤔', '😶', '🧊', '➖'],            color: '#94a3b8' }
};

textInput.addEventListener('input', () => {
    charCount.textContent = textInput.value.length;
});

function spawnEmojis(emotion) {
    emojiExplosion.innerHTML = '';
    const cfg = EMOTION_CONFIG[emotion] || EMOTION_CONFIG.neutral;
    for (let i = 0; i < 18; i++) {
        const el = document.createElement('span');
        el.className = 'emoji-particle';
        el.textContent = cfg.emojis[Math.floor(Math.random() * cfg.emojis.length)];
        el.style.left = Math.random() * 100 + '%';
        el.style.top = 60 + Math.random() * 40 + '%';
        el.style.animationDelay = Math.random() * 0.6 + 's';
        el.style.animationDuration = 1.5 + Math.random() * 1.5 + 's';
        emojiExplosion.appendChild(el);
    }
    setTimeout(() => { emojiExplosion.innerHTML = ''; }, 3000);
}

function renderScores(allScores, topEmotion) {
    scoresGrid.innerHTML = '';
    const sorted = Object.entries(allScores).sort((a, b) => b[1] - a[1]);

    sorted.forEach(([emotion, score]) => {
        const isTop = emotion === topEmotion;
        const cfg = EMOTION_CONFIG[emotion] || EMOTION_CONFIG.neutral;
        const pct = Math.round(score * 100);

        const row = document.createElement('div');
        row.className = 'score-row';
        row.innerHTML = `
            <span class="score-emoji">${cfg.emoji}</span>
            <span class="score-name">${emotion}</span>
            <div class="score-track">
                <div class="score-fill ${isTop ? 'top' : 'other'}" style="width: 0%"></div>
            </div>
            <span class="score-percent ${isTop ? 'top' : ''}">${pct}%</span>
        `;
        scoresGrid.appendChild(row);

        requestAnimationFrame(() => {
            requestAnimationFrame(() => {
                row.querySelector('.score-fill').style.width = pct + '%';
            });
        });
    });
}

form.addEventListener('submit', async (e) => {
    e.preventDefault();
    const text = textInput.value.trim();
    if (!text) return;

    generateBtn.disabled = true;
    btnContent.style.display = 'none';
    loader.style.display = 'flex';

    try {
        const response = await fetch('/api/synthesize', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ text })
        });

        if (!response.ok) throw new Error('Synthesis failed');

        const data = await response.json();
        const cfg = EMOTION_CONFIG[data.emotion] || EMOTION_CONFIG.neutral;

        document.body.setAttribute('data-emotion', data.emotion);
        emotionLabel.textContent = data.emotion;
        emotionEmoji.textContent = cfg.emoji;
        confidenceValue.textContent = Math.round(data.confidence * 100) + '%';

        paramPitch.textContent = data.parameters.pitch_st + ' st';
        paramGain.textContent = data.parameters.gain_db + ' dB';
        paramRate.textContent = data.parameters.rate + 'x';

        const intensityPct = Math.round(data.confidence * 100);
        intensityFill.style.width = intensityPct + '%';
        intensityPercent.textContent = intensityPct + '%';

        renderScores(data.all_scores, data.emotion);

        const audioBytes = Uint8Array.from(atob(data.audio_base64), c => c.charCodeAt(0));
        const audioBlob = new Blob([audioBytes], { type: 'audio/wav' });
        audioPlayer.src = URL.createObjectURL(audioBlob);
        resultSection.classList.remove('hidden');

        spawnEmojis(data.emotion);
        audioPlayer.play().catch(() => {});
    } catch (error) {
        alert('Something went wrong. Please check if the backend is running.');
    } finally {
        generateBtn.disabled = false;
        btnContent.style.display = 'flex';
        loader.style.display = 'none';
    }
});

const toggleWave = (on) => waveform.classList.toggle('active', on);
audioPlayer.addEventListener('play', () => toggleWave(true));
audioPlayer.addEventListener('pause', () => toggleWave(false));
audioPlayer.addEventListener('ended', () => toggleWave(false));
