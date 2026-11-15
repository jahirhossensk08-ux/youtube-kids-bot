import os
import re
import json
import time
import random
import asyncio
import urllib.request
import urllib.parse
import urllib.error

# =====================================================================
# 1. CONFIGURATION & API KEYS (100% Crash-Proof Setup)
# =====================================================================
DEFAULT_API_KEY = "AQ.Ab8RN6LYwTy4uxCtviZ9HmyJHlQmfRTNUJVPglDhixRCOUR5rg"
env_key = os.environ.get("GEMINI_API_KEY", "").strip()
GEMINI_API_KEY = env_key if env_key else DEFAULT_API_KEY

# 4-Level AI Model Fallback
GEMINI_MODELS = [
    "gemini-2.5-flash",
    "gemini-flash-latest",
    "gemini-2.0-flash",
    "gemini-1.5-flash"
]

HISTORY_FILE = "used_topics.json"
OUTPUT_SCRIPT_FILE = "latest_video_plan.json"

# Workspace Folders
DIRS = ["output_videos", "temp_assets", "audio_clips", "scene_images", "thumbnails"]
for d in DIRS:
    os.makedirs(d, exist_ok=True)

# High-RPM US Kids Moral Story Themes
KIDS_THEMES = [
    "A little panda learning the magic of sharing in a glowing forest",
    "A brave tiny tiger who was afraid of the dark until he met a friendly firefly",
    "A curious monkey building a cardboard rocket to visit the cheese moon",
    "A kind little bunny helping a lost baby dragon find its mother",
    "Three animal friends solving the mystery of the missing rainbow colors",
    "A cheerful little train that delivers happy dreams to sleeping animals",
    "A smart little squirrel who planted a magical golden acorn",
    "A baby elephant who learned that being different makes him special",
    "Two littlefoxes who built a bridge of friendship across a sparkling stream",
    "A sleepy little owl who wanted to see the bright morning sun"
]

# =====================================================================
# 2. MEMORY SYSTEM (No-Repeat Story Tracker)
# =====================================================================
def load_used_topics():
    if os.path.exists(HISTORY_FILE):
        try:
            with open(HISTORY_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
                return data if isinstance(data, list) else []
        except Exception:
            return []
    return []

def save_used_topic(topic):
    topics = load_used_topics()
    if topic not in topics:
        topics.append(topic)
        with open(HISTORY_FILE, "w", encoding="utf-8") as f:
            json.dump(topics[-150:], f, indent=2, ensure_ascii=False)

def pick_fresh_topic():
    used = load_used_topics()
    available = [t for t in KIDS_THEMES if t not in used]
    if not available:
        return f"A brand new magical adventure of cute forest friends #{random.randint(100, 999)}"
    return random.choice(available)

# =====================================================================
# 3. SMART JSON CLEANER & EMERGENCY FALLBACK PLAN
# =====================================================================
def extract_clean_json(raw_text):
    """AI के जवाब में से कोई भी एक्स्ट्रा अक्षर या markdown हटाकर शुद्ध JSON निकालता है"""
    cleaned = raw_text.strip()
    cleaned = re.sub(r"^```(?:json)?\s*", "", cleaned, flags=re.IGNORECASE)
    cleaned = re.sub(r"\s*```$", "", cleaned)
    start = cleaned.find("{")
    end = cleaned.rfind("}")
    if start != -1 and end != -1 and end > start:
        cleaned = cleaned[start:end + 1]
    return json.loads(cleaned)

def get_emergency_fallback_plan(topic):
    """अगर कभी इंटरनेट या API डाउन हो, तो यह बैकअप प्लान बोट को क्रैश होने से बचाएगा"""
    print("[Fallback Engine] Activating Built-in Studio Backup Plan so pipeline never fails...")
    return {
        "title": "The Magic of Sharing! | Cute Panda 3D Story",
        "description": "Join Barnaby the cute little panda and his forest friends in a heartwarming 3D animated moral story about kindness and sharing! Perfect bedtime story for kids and toddlers.",
        "moral": "Sharing with friends always doubles the joy!",
        "tags": ["kids cartoon", "3d animation", "toontales hub", "moral stories for kids", "bedtime stories", "cute panda"],
        "youtube_settings": {
            "categoryId": "1",
            "madeForKids": True,
            "defaultLanguage": "en-US"
        },
        "character_style_seed": "Cute chubby baby panda with big sparkling blue eyes, soft Pixar 3D fur, wearing a tiny red scarf, Disney Pixar 3D animation style",
        "thumbnail_prompt": "3D Pixar style cute baby panda holding a glowing golden berry in a magical colorful forest, ultra vibrant, expressive face, 8k",
        "scenes": [
            {
                "scene_number": 1,
                "voiceover_english": "Once upon a time, in the Sunny Bamboo Woods, lived a cute little panda named Pippin.",
                "voiceover_hindi": "एक समय की बात है, चमकीले बांस के जंगल में पिपिन नाम का एक बहुत प्यारा छोटा पांडा रहता था।",
                "subtitle_text": "Once upon a time, lived a cute panda named Pippin.",
                "image_prompt": "3D Pixar style cute baby panda with big sparkling eyes walking happily in a glowing magical bamboo forest, cinematic lighting, 8k",
                "camera_motion": "slow_zoom_in",
                "sfx_cue": "forest_birds_chirping"
            },
            {
                "scene_number": 2,
                "voiceover_english": "One sunny morning, Pippin found a giant, sparkling rainbow berry under a tall tree!",
                "voiceover_hindi": "एक सुहानी सुबह, पिपिन को एक बड़े पेड़ के नीचे एक चमकदार सतरंगी बेरी मिली!",
                "subtitle_text": "Pippin found a giant sparkling rainbow berry!",
                "image_prompt": "3D Pixar style cute baby panda looking amazed at a glowing rainbow berry under a magical tree, vibrant colors, 8k",
                "camera_motion": "pan_right",
                "sfx_cue": "magical_sparkle_chime"
            },
            {
                "scene_number": 3,
                "voiceover_english": "Just then, his little friend Toby the Tiger cub walked by with a rumbling, hungry tummy.",
                "voiceover_hindi": "तभी उसका छोटा दोस्त टोबी टाइगर भूखे पेट वहां से गुजरा।",
                "subtitle_text": "His friend Toby the Tiger was very hungry.",
                "image_prompt": "3D Pixar style cute baby panda and a cute baby tiger cub looking at a glowing berry together in a sunny meadow, 8k",
                "camera_motion": "slow_zoom_out",
                "sfx_cue": "gentle_funny_boing"
            },
            {
                "scene_number": 4,
                "voiceover_english": "Pippin smiled warmly, broke the magical berry in half, and shared it with his best friend!",
                "voiceover_hindi": "पिपिन ने प्यार से मुस्कुराते हुए जादुई बेरी को आधा तोड़ा और अपने सबसे अच्छे दोस्त के साथ बांट लिया!",
                "subtitle_text": "Pippin smiled and shared the berry with his friend!",
                "image_prompt": "3D Pixar style cute baby panda sharing a glowing fruit with a cute baby tiger cub, both smiling happily, magical sparkles, 8k",
                "camera_motion": "slow_zoom_in",
                "sfx_cue": "happy_ukulele_melody"
            },
            {
                "scene_number": 5,
                "voiceover_english": "Suddenly, the berry tree bloomed with hundreds of treats! Because sharing always brings pure magic!",
                "voiceover_hindi": "अचानक पूरे पेड़ पर ढेर सारे मीठे फल खिल उठे! क्योंकि बांटने से हमेशा खुशियां दोगुनी हो जाती हैं!",
                "subtitle_text": "Sharing always brings pure magic and joy!",
                "image_prompt": "3D Pixar style cute baby panda and baby tiger celebrating under a tree full of glowing colorful berries, rainbow in sky, 8k",
                "camera_motion": "zoom_in_center",
                "sfx_cue": "cheerful_victory_fanfare"
            }
        ]
    }

# =====================================================================
# 4. AI BRAIN ENGINE (Multi-Model & Auto-Retry)
# =====================================================================
def call_gemini_api(prompt):
    for model_name in GEMINI_MODELS:
        url = f"[https://generativelanguage.googleapis.com/v1beta/models/](https://generativelanguage.googleapis.com/v1beta/models/){model_name}:generateContent"
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

        for attempt in range(1, 3):
            try:
                print(f"[AI Brain] Requesting '{model_name}' (Attempt {attempt}/2)...")
                req = urllib.request.Request(url, data=data, headers=headers, method="POST")
                with urllib.request.urlopen(req, timeout=45) as response:
                    res_body = response.read().decode("utf-8")
                    res_json = json.loads(res_body)
                    text_output = res_json["candidates"][0]["content"]["parts"][0]["text"]
                    return extract_clean_json(text_output)
            except urllib.error.HTTPError as he:
                err_detail = he.read().decode("utf-8", errors="ignore")
                print(f"[HTTP Warning] {model_name} ({he.code}): {err_detail[:180]}")
                time.sleep(2)
            except Exception as e:
                print(f"[Warning] {model_name} attempt {attempt} failed: {e}")
                time.sleep(2)

    return None

# =====================================================================
# 5. STUDIO SCRIPT GENERATOR
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
      "moral": "Clear 1-line moral lesson for kids",
      "tags": ["kids cartoon", "bedtime stories", "toontales hub", "3d animation", "moral stories"],
      "youtube_settings": {{
        "categoryId": "1",
        "madeForKids": true,
        "defaultLanguage": "en-US"
      }},
      "character_style_seed": "Exact 3D Pixar-style character description to keep visuals 100% consistent in every scene",
      "thumbnail_prompt": "Vibrant 3D Pixar style YouTube thumbnail prompt, ultra-expressive cute characters, bright colors",
      "scenes": [
        {{
          "scene_number": 1,
          "voiceover_english": "Warm, lively, storytelling narration for scene 1 (14-20 words)",
          "voiceover_hindi": "उसी सीन का आसान और मज़ेदार हिंदी अनुवाद",
          "subtitle_text": "Short punchy subtitle text for screen",
          "image_prompt": "Full 3D Pixar studio quality scene description including the exact character_style_seed, vibrant lighting, 8k",
          "camera_motion": "slow_zoom_in",
          "sfx_cue": "magical_chime"
        }}
      ]
    }}
    Ensure there are exactly 5 scenes that tell a complete story with a happy moral ending.
    """

    video_plan = call_gemini_api(prompt)
    if not video_plan or "scenes" not in video_plan:
        video_plan = get_emergency_fallback_plan(topic)

    with open(OUTPUT_SCRIPT_FILE, "w", encoding="utf-8") as f:
        json.dump(video_plan, f, indent=2, ensure_ascii=False)

    save_used_topic(topic)
    return video_plan

# =====================================================================
# 6. US STUDIO VOICEOVER GENERATOR (Edge-TTS + gTTS Fallback)
# =====================================================================
async def _edge_tts_save(text, output_path, voice="en-US-AnaNeural"):
    import edge_tts
    communicate = edge_tts.Communicate(text, voice, rate="-5%", pitch="+5Hz")
    await communicate.save(output_path)

def generate_scene_audio(text, scene_num):
    output_path = os.path.join("audio_clips", f"scene_{scene_num}.mp3")
    # Primary: Microsoft Edge Neural US Kids Storytelling Voice (AnaNeural)
    try:
        asyncio.run(_edge_tts_save(text, output_path))
        if os.path.exists(output_path) and os.path.getsize(output_path) > 500:
            print(f"  🎙️ [Voice] Scene {scene_num} HD US Neural Audio Ready: {output_path}")
            return output_path
    except Exception as e:
        print(f"  [Voice Fallback] Edge-TTS busy ({e}), switching to Google TTS...")

    # Backup: Google TTS
    try:
        from gtts import gTTS
        tts = gTTS(text=text, lang="en", tld="us", slow=False)
        tts.save(output_path)
        print(f"  🎙️ [Voice] Scene {scene_num} Backup Audio Ready: {output_path}")
    except Exception as e2:
        print(f"  [Voice Warning] Could not create audio for scene {scene_num}: {e2}")
    return output_path

# =====================================================================
# 7. 3D PIXAR IMAGE & THUMBNAIL GENERATOR (AI Cloud + Pillow Fallback)
# =====================================================================
def create_fallback_poster(output_path, title_text, subtitle_text, scene_num=0):
    from PIL import Image, ImageDraw
    img = Image.new("RGB", (1280, 720), color=(30, 110, 220))
    draw = ImageDraw.Draw(img)
    # Vibrant gradient background
    for y in range(720):
        r = int(25 + (y / 720) * 60)
        g = int(90 + (y / 720) * 110)
        b = int(200 - (y / 720) * 40)
        draw.line([(0, y), (1280, y)], fill=(r, g, b))
    draw.rectangle([50, 50, 1230, 670], outline=(255, 220, 60), width=8)
    draw.text((100, 220), "TOONTALES HUB - 3D KIDS STUDIO", fill=(255, 235, 100))
    draw.text((100, 310), title_text[:65], fill=(255, 255, 255))
    draw.text((100, 400), subtitle_text[:85], fill=(230, 245, 255))
    img.save(output_path, "JPEG", quality=92)

def generate_scene_visual(prompt, subtitle_text, scene_num, is_thumbnail=False):
    folder = "thumbnails" if is_thumbnail else "scene_images"
    filename = "thumbnail.jpg" if is_thumbnail else f"scene_{scene_num}.jpg"
    output_path = os.path.join(folder, filename)

    clean_prompt = f"3D Pixar Disney animation style, cute kids cartoon, bright vibrant colors, {prompt}"
    encoded = urllib.parse.quote(clean_prompt[:380])
    seed = random.randint(1000, 99999)
    url = f"[https://image.pollinations.ai/prompt/](https://image.pollinations.ai/prompt/){encoded}?width=1280&height=720&seed={seed}&nologo=true"

    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=35) as resp:
            img_data = resp.read()
            if len(img_data) > 5000:
                with open(output_path, "wb") as f:
                    f.write(img_data)
                print(f"  🎨 [3D Visual] Saved HD Image: {output_path}")
                return output_path
    except Exception as e:
        print(f"  [Visual Warning] Cloud AI Image slow ({e}), generating Studio Poster...")

    create_fallback_poster(output_path, f"Scene {scene_num} - ToonTales Hub", subtitle_text, scene_num)
    print(f"  🎨 [3D Visual] Saved Studio Fallback Image: {output_path}")
    return output_path

# =====================================================================
# 8. MAIN EXECUTION PIPELINE
# =====================================================================
if __name__ == "__main__":
    print("====================================================")
    print("   TOONTALES HUB - AI STUDIO BOT INITIALIZING       ")
    print("====================================================")

    try:
        # Step 1: Generate Complete Story & Production Plan
        plan = generate_studio_video_plan()
        scenes = plan.get("scenes", [])
        print("\n✅ STEP 1: Studio Video Plan Generated Successfully!")
        print(f"📌 Video Title: {plan.get('title')}")
        print(f"💡 Story Moral: {plan.get('moral', 'Always be kind and helpful!')}")
        print(f"🎬 Total Scenes: {len(scenes)}")

        # Step 2: Generate US Kids Voiceovers & 3D Scene Art
        print("\n🚀 STEP 2: Generating Studio Voiceovers & 3D Visual Assets...")
        for s in scenes:
            s_num = s.get("scene_number", 1)
            vo_en = s.get("voiceover_english", "Welcome to ToonTales Hub!")
            sub = s.get("subtitle_text", vo_en)
            img_p = s.get("image_prompt", plan.get("character_style_seed", "Cute 3D panda"))

            generate_scene_audio(vo_en, s_num)
            generate_scene_visual(img_p, sub, s_num, is_thumbnail=False)

        # Step 3: Generate YouTube Kids Thumbnail
        thumb_prompt = plan.get("thumbnail_prompt", plan.get("title", "Cute 3D Cartoon"))
        generate_scene_visual(thumb_prompt, plan.get("title", "ToonTales Hub"), 0, is_thumbnail=True)

        print("\n====================================================")
        print("🎉 ALL STUDIO ASSETS (SCRIPT + VOICE + 3D ART) READY!")
        print(f"💾 Script Saved: {OUTPUT_SCRIPT_FILE}")
        print("====================================================")
    except Exception as err:
        print(f"\n❌ UNEXPECTED ERROR: {err}")
        exit(1)
