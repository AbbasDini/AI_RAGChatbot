// Debug script for voice playback issues
console.log("🔍 Starting voice debug...");

// Check browser support
function checkBrowserSupport() {
    console.log("=== Browser Support Check ===");
    
    // Check Web Speech API
    if ('speechSynthesis' in window) {
        console.log("✅ Web Speech API supported");
        console.log("Speech synthesis object:", window.speechSynthesis);
    } else {
        console.error("❌ Web Speech API not supported");
    }
    
    // Check Audio API
    if ('Audio' in window) {
        console.log("✅ Audio API supported");
    } else {
        console.error("❌ Audio API not supported");
    }
    
    // Check fetch API
    if ('fetch' in window) {
        console.log("✅ Fetch API supported");
    } else {
        console.error("❌ Fetch API not supported");
    }
}

// Check available voices
function checkAvailableVoices() {
    console.log("=== Available Voices Check ===");
    
    if ('speechSynthesis' in window) {
        const voices = speechSynthesis.getVoices();
        console.log(`Found ${voices.length} voices:`);
        
        voices.forEach((voice, index) => {
            console.log(`${index + 1}. ${voice.name} (${voice.lang}) - ${voice.default ? 'DEFAULT' : ''}`);
        });
        
        // Check for Persian voices
        const persianVoices = voices.filter(voice => 
            voice.lang.includes('fa') || 
            voice.lang.includes('ir') || 
            voice.name.toLowerCase().includes('persian') ||
            voice.name.toLowerCase().includes('farsi')
        );
        
        console.log(`Persian voices found: ${persianVoices.length}`);
        persianVoices.forEach(voice => {
            console.log(`- ${voice.name} (${voice.lang})`);
        });
        
        return voices;
    }
    
    return [];
}

// Test basic speech synthesis
function testBasicSpeech() {
    console.log("=== Basic Speech Test ===");
    
    if (!('speechSynthesis' in window)) {
        console.error("❌ Speech synthesis not available");
        return false;
    }
    
    try {
        const utterance = new SpeechSynthesisUtterance("Hello, this is a test.");
        utterance.lang = 'en-US';
        utterance.rate = 0.8;
        utterance.pitch = 1.0;
        utterance.volume = 1.0;
        
        utterance.onstart = () => console.log("✅ Speech started");
        utterance.onend = () => console.log("✅ Speech ended");
        utterance.onerror = (event) => console.error("❌ Speech error:", event.error);
        
        speechSynthesis.speak(utterance);
        return true;
    } catch (error) {
        console.error("❌ Speech test failed:", error);
        return false;
    }
}

// Test Persian speech
function testPersianSpeech() {
    console.log("=== Persian Speech Test ===");
    
    if (!('speechSynthesis' in window)) {
        console.error("❌ Speech synthesis not available");
        return false;
    }
    
    try {
        const utterance = new SpeechSynthesisUtterance("سلام، این یک تست است.");
        utterance.lang = 'fa-IR';
        utterance.rate = 0.7;
        utterance.pitch = 1.0;
        utterance.volume = 1.0;
        
        // Try to find Persian voice
        const voices = speechSynthesis.getVoices();
        const persianVoice = voices.find(voice => 
            voice.lang.includes('fa') || 
            voice.lang.includes('ir') ||
            voice.name.toLowerCase().includes('persian') ||
            voice.name.toLowerCase().includes('farsi')
        );
        
        if (persianVoice) {
            utterance.voice = persianVoice;
            console.log("Using Persian voice:", persianVoice.name);
        } else {
            console.log("No Persian voice found, using default");
        }
        
        utterance.onstart = () => console.log("✅ Persian speech started");
        utterance.onend = () => console.log("✅ Persian speech ended");
        utterance.onerror = (event) => console.error("❌ Persian speech error:", event.error);
        
        speechSynthesis.speak(utterance);
        return true;
    } catch (error) {
        console.error("❌ Persian speech test failed:", error);
        return false;
    }
}

// Test advanced TTS API
async function testAdvancedTTS() {
    console.log("=== Advanced TTS API Test ===");
    
    try {
        const response = await fetch('/api/tts', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                text: "سلام، این یک تست TTS پیشرفته است.",
                provider: 'auto',
                voice: ''
            })
        });
        
        console.log("Response status:", response.status);
        console.log("Response headers:", response.headers);
        
        if (response.ok) {
            const audioBlob = await response.blob();
            console.log("✅ Audio blob received, size:", audioBlob.size);
            
            // Test playing the audio
            const audioUrl = URL.createObjectURL(audioBlob);
            const audio = new Audio(audioUrl);
            
            audio.onloadstart = () => console.log("✅ Audio loading started");
            audio.oncanplay = () => console.log("✅ Audio can play");
            audio.onplay = () => console.log("✅ Audio started playing");
            audio.onended = () => console.log("✅ Audio ended");
            audio.onerror = (error) => console.error("❌ Audio error:", error);
            
            await audio.play();
            return true;
        } else {
            const error = await response.json();
            console.error("❌ TTS API error:", error);
            return false;
        }
    } catch (error) {
        console.error("❌ TTS API test failed:", error);
        return false;
    }
}

// Check system audio
function checkSystemAudio() {
    console.log("=== System Audio Check ===");
    
    // Check if audio context is available
    if ('AudioContext' in window || 'webkitAudioContext' in window) {
        console.log("✅ Web Audio API supported");
        
        try {
            const audioContext = new (window.AudioContext || window.webkitAudioContext)();
            console.log("✅ Audio context created successfully");
            
            // Check if audio context is suspended (needs user interaction)
            if (audioContext.state === 'suspended') {
                console.log("⚠️ Audio context is suspended - needs user interaction");
            } else {
                console.log("✅ Audio context is running");
            }
            
            return audioContext;
        } catch (error) {
            console.error("❌ Failed to create audio context:", error);
            return null;
        }
    } else {
        console.error("❌ Web Audio API not supported");
        return null;
    }
}

// Test user interaction requirement
function testUserInteraction() {
    console.log("=== User Interaction Test ===");
    
    // Create a test button
    const testButton = document.createElement('button');
    testButton.textContent = 'Test Audio (Click Me)';
    testButton.style.cssText = `
        position: fixed;
        top: 10px;
        right: 10px;
        z-index: 10000;
        padding: 10px;
        background: #007bff;
        color: white;
        border: none;
        border-radius: 5px;
        cursor: pointer;
    `;
    
    testButton.onclick = async () => {
        console.log("User clicked test button");
        
        // Test audio context
        const audioContext = checkSystemAudio();
        if (audioContext && audioContext.state === 'suspended') {
            await audioContext.resume();
            console.log("✅ Audio context resumed");
        }
        
        // Test speech synthesis
        testBasicSpeech();
        
        // Test Persian speech
        setTimeout(() => testPersianSpeech(), 2000);
        
        // Test advanced TTS
        setTimeout(() => testAdvancedTTS(), 4000);
        
        // Remove button after testing
        setTimeout(() => testButton.remove(), 10000);
    };
    
    document.body.appendChild(testButton);
    console.log("✅ Test button added - click it to test audio");
}

// Main debug function
function runVoiceDebug() {
    console.log("🎵 Starting comprehensive voice debug...");
    
    // Check browser support
    checkBrowserSupport();
    
    // Check available voices
    const voices = checkAvailableVoices();
    
    // Check system audio
    const audioContext = checkSystemAudio();
    
    // Test user interaction requirement
    testUserInteraction();
    
    // Wait for voices to load
    if ('speechSynthesis' in window) {
        speechSynthesis.onvoiceschanged = () => {
            console.log("=== Voices Changed Event ===");
            checkAvailableVoices();
        };
    }
    
    console.log("🔍 Debug complete. Check console for results.");
    console.log("💡 If no sound plays, try clicking the test button in the top-right corner.");
}

// Auto-run debug on page load
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', runVoiceDebug);
} else {
    runVoiceDebug();
}

// Export functions for manual testing
window.voiceDebug = {
    checkBrowserSupport,
    checkAvailableVoices,
    testBasicSpeech,
    testPersianSpeech,
    testAdvancedTTS,
    checkSystemAudio,
    testUserInteraction,
    runVoiceDebug
}; 