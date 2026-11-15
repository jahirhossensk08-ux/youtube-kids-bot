import os
import json
import time
import random
import urllib.request
import urllib.error

# =====================================================================
# 1. CONFIGURATION & API KEYS (फ्यूचर-प्रूफ सेटअप)
# =====================================================================
# अगर भविष्य में आप GitHub Secrets में की डालें तो वहाँ से लेगा, वरना आपकी दी हुई Key इस्तेमाल करेगा
GEMINI_API_KEY = os.environ.get(
    "GEMINI_API_KEY", 
    "AQ.Ab8RN6LYwTy4uxCtviZ9HmyJHlQmfRTNUJVPglDhixRCOUR5rg"
)

# 3 बैकअप मॉडल्स: अगर पहला काम न करे तो दूसरा अपने आप चलेगा
GEMINI_MODELS = [
    "gemini-2.5-flash",
    "gemini-flash-latest",
    "gemini-2.0-flash"
]

HISTORY_FILE = "used_topics.json"
OUTPUT_SCRIPT_FILE = "latest_video_plan.json"

# US Kids के लिए हाई-सीपीएम (High-CPM) और पॉपुलर थीम्स
KIDS_THEMES = [
    "A little panda learning the magic of sharing in a glowing forest",
    "A brave tiny tiger who was afraid of the dark until he met a friendly firefly",
    "A curious monkey building a cardboard rocket to visit the cheese moon",
    "A kind little bunny helping a lost baby dragon find its mother",
    "Three animal friends solving the mystery of the missing rainbow colors",
    "A cheerful little train that delivers happy dreams to sleeping animals",
    "A smart little squirrel who planted a magical golden acorn"
]

# =====================================================================
# 2. MEMORY SYSTEM (ताकि कोई भी कहानी दोबारा रिपीट न हो)
# =====================================================================
def load_used_topics():
    if os.path.exists(HISTORY_FILE):
        try:
            with open(HISTORY_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return []
    return []

def save_used_topic(topic):
    topics = load_used_topics()
    if topic not in topics:
        topics.append(topic)
        with open(HISTORY_FILE, "w", encoding="utf-8") as f:
            json.dump(topics[-100:], f, indent=2)  # पिछली 100 कहानियों का रिकॉर्ड रखेगा

def pick_fresh_topic():
    used = load_used_topics()
    available = [t for t in KIDS_THEMES if t not in used]
    if not available:
        return f"A brand new magical adventure of cute forest animals #{random.randint(100, 999)}"
    return random.choice(available)

# =====================================================================
# 3. AI BRAIN ENGINE (Auto-Retry और 3 Model Fallbacks के साथ)
# =====================================================================
def call_gemini_api(prompt):
    for model_name in GEMINI_MODELS:
        url = f"https://generativelanguage.googleapis.com/v1beta/models/{model_name}:generateContent"
        headers = {
            "Content-Type": "application/json",
            "X-goog-api-key": GEMINI_API_KEY
        }
        payload = {
            "contents": [{"parts": [{"text": prompt}]}],
            "generationConfig": {
                "temperature": 0.7,
                "responseMimeType": "application/json"
            }
        }
        
        data = json.dumps(payload).encode("utf-8")
        
        # हर मॉडल पर 3 बार कोशिश करेगा (अगर इंटरनेट स्लो हो)
        for attempt in range(1, 4):
            try:
                print(f"[AI Brain] Trying model '{model_name}' (Attempt {attempt}/3)...")
                req = urllib.request.Request(url, data=data, headers=headers, method="POST")
                with urllib.request.urlopen(req, timeout=45) as response:
                    res_body = response.read().decode("utf-8")
                    res_json = json.loads(res_body)
                    text_output = res_json["candidates"][0]["content"]["parts"][0]["text"]
                    return json.loads(text_output)
            except Exception as e:
                print(f"[Warning] {model_name} attempt {attempt} failed: {e}")
                time.sleep(3)
                
    raise RuntimeError("All AI models failed after multiple retries. Please check API Key or quota.")

# =====================================================================
# 4. STUDIO SCRIPT & VISUAL GENERATOR (US Kids Audience के लिए)
# =====================================================================
def generate_studio_video_plan():
    topic = pick_fresh_topic()
    print(f"\n[Selected Concept]: {topic}")
    
    prompt = f"""
    You are an award-winning Pixar/Disney creative director for the US Kids YouTube channel 'ToonTales Hub'.
    Create a complete, highly engaging 60-second animated story production plan based on this concept: "{topic}".
    Target Audience: Children aged 3 to 8 in the USA, UK, and Canada.
    
    Return STRICTLY a valid JSON object with this exact structure:
    {{
      "title": "Catchy, high-CTR YouTube title for kids (max 60 chars)",
      "description": "SEO-optimized YouTube description for parents and kids with moral of the story",
      "tags": ["kids cartoon", "bedtime stories", "toontales hub", "3d animation", "moral stories"],
      "character_style_seed": "Exact 3D Pixar-style character description to keep visuals 100% consistent in every scene",
      "thumbnail_prompt": "Vibrant 3D Pixar style YouTube thumbnail prompt, ultra-expressive cute characters, bright colors",
      "scenes": [
        {{
          "scene_number": 1,
          "voiceover_english": "Warm, lively, storytelling narration for scene 1 (15-20 words)",
          "voiceover_hindi": "उसी सीन का आसान और मज़ेदार हिंदी अनुवाद (बैकअप/डबिंग के लिए)",
          "image_prompt": "Full 3D Pixar studio quality scene description including the exact character_style_seed, vibrant lighting, 8k",
          "camera_motion": "slow_zoom_in"
        }}
      ]
    }}
    Make sure there are exactly 5 scenes that tell a complete story with a happy moral ending.
    """
    
    video_plan = call_gemini_api(prompt)
    
    # फाइल में सेव करें ताकि अगला स्टेप (आवाज़ और वीडियो एडिटर) इसे सीधे पढ़ सके
    with open(OUTPUT_SCRIPT_FILE, "w", encoding="utf-8") as f:
        json.dump(video_plan, f, indent=2, ensure_ascii=False)
        
    save_used_topic(topic)
    return video_plan

# =====================================================================
# 5. MAIN EXECUTION (बोट का स्टार्ट बटन)
# =====================================================================
if __name__ == "__main__":
    print("====================================================")
    print("   TOONTALES HUB - AI STUDIO BOT INITIALIZING       ")
    print("====================================================")
    
    try:
        plan = generate_studio_video_plan()
        print("\n✅ SUCCESS! Studio Video Plan Generated Successfully!")
        print(f"📌 Video Title: {plan.get('title')}")
        print(f"🎬 Total Scenes Created: {len(plan.get('scenes', []))}")
        print(f"💾 Saved to file: {OUTPUT_SCRIPT_FILE}")
        print("====================================================")
    except Exception as err:
        print(f"\n❌ ERROR: {err}")
        exit(1)

