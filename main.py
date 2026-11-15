import os
import re
import math
import wave
import json
import time
import struct
import random
import asyncio
import urllib.request
import urllib.parse
import urllib.error

# =====================================================================
# 0. PILLOW 10+ & MOVIEPY 1.0.3 COMPATIBILITY PATCH (100% CRASH-PROOF)
# =====================================================================
import PIL.Image
if not hasattr(PIL.Image, "ANTIALIAS"):
    PIL.Image.ANTIALIAS = PIL.Image.LANCZOS

from PIL import Image, ImageDraw, ImageFont

# =====================================================================
# 1. CONFIGURATION & API KEYS (FUTURE-PROOF SETUP)
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
FINAL_VIDEO_PATH = os.path.join("output_videos", "final_story_1080p.mp4")
FINAL_SHORT_PATH = os.path.join("output_videos", "final_short_vertical.mp4")
SEO_REPORT_PATH = os.path.join("output_videos", "youtube_seo_metadata.txt")

DIRS = ["output_videos", "temp_assets", "audio_clips", "scene_images", "thumbnails"]
for d in DIRS:
    os.makedirs(d, exist_ok=True)

# 20 High-RPM US Kids Moral Story Themes
KIDS_THEMES = [
    "A little panda learning the magic of sharing in a glowing forest",
    "A brave tiny tiger who was afraid of the dark until he met a friendly firefly",
    "A curious monkey building a cardboard rocket to visit the cheese moon",
    "A kind little bunny helping a lost baby dragon find its mother",
    "Three animal friends solving the mystery of the missing rainbow colors",
    "A cheerful little train that delivers happy dreams to sleeping animals",
    "A smart little squirrel who planted a magical golden acorn",
    "A baby elephant who learned that being different makes him special",
    "Two little foxes who built a bridge of friendship across a sparkling stream",
    "A sleepy little owl who wanted to see the bright morning sun",
    "A friendly little dinosaur who loved baking star-shaped cookies for his friends",
    "A tiny penguin who wished to fly and built colorful paper wings",
    "A golden puppy who found a magical paintbrush that brings drawings to life",
    "A polite little bear who learned the power of saying Please and Thank You",
    "A playful baby dolphin who helped clean up the sparkling coral reef",
    "A little hedgehog who shared his warm cozy scarf on a snowy morning",
    "A singing bluebird who cheered up a grumpy old turtle",
    "A tiny duckling who discovered the joy of telling the truth",
    "A cute little koala who organized a forest talent show for everyone",
    "A brave little mouse who sailed across a puddle in a leaf boat"
]

# Multi-Voice US Neural Storytelling Cast
US_KIDS_VOICES = [
    "en-US-AnaNeural",      # Cute child-like warm storytelling voice
    "en-US-AriaNeural",     # Expressive lively narrator
    "en-US-JennyNeural"     # Warm friendly motherly bedtime voice
]

# =====================================================================
# 2. MEMORY SYSTEM (NO-REPEAT STORY TRACKER)
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
            json.dump(topics[-250:], f, indent=2, ensure_ascii=False)

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
    cleaned = raw_text.strip()
    cleaned = re.sub(r"^```(?:json)?\s*", "", cleaned, flags=re.IGNORECASE)
    cleaned = re.sub(r"\s*```$", "", cleaned)
    start = cleaned.find("{")
    end = cleaned.rfind("}")
    if start != -1 and end != -1 and end > start:
        cleaned = cleaned[start:end + 1]
    return json.loads(cleaned)

def get_emergency_fallback_plan(topic):
    print("[Fallback Engine] Activating Built-in Studio Backup Plan so pipeline never fails...")
    return {
        "title": "The Magic of Sharing! | Cute Panda 3D Story",
        "thumbnail_badge": "MAGIC BERRY!",
        "viral_hook": "What happens when you find a glowing magic berry in the woods?",
        "interactive_question": "Kids! Can you count how many glowing berries are on the tree?",
        "description": "Join Pippin the cute little panda and his forest friends in a heartwarming 3D animated moral story about kindness and sharing! Perfect bedtime story for kids and toddlers.\n\n#kidscartoon #3danimation #bedtimestories #toontaleshub #moralstories #shorts",
        "moral": "Sharing with friends always doubles the joy!",
        "tags": ["kids cartoon", "3d animation", "toontales hub", "moral stories for kids", "bedtime stories", "cute panda", "pixar style story"],
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
                "voiceover_english": "Wait! Look at that glowing light in the Sunny Bamboo Woods! Little Pippin the Panda just discovered a secret!",
                "voiceover_hindi": "रुको! चमकीले बांस के जंगल में उस जादुई रोशनी को देखो! नन्हे पिपिन पांडा को अभी-अभी एक रहस्य मिला है!",
                "subtitle_text": "Look at that glowing light! Pippin found a secret!",
                "highlight_words": ["glowing", "secret!"],
                "image_prompt": "3D Pixar style cute baby panda with big sparkling eyes walking happily in a glowing magical bamboo forest, cinematic lighting, 8k",
                "camera_motion": "slow_zoom_in",
                "sfx_type": "sparkle"
            },
            {
                "scene_number": 2,
                "voiceover_english": "Under the giant tree sat a sparkling rainbow berry! It smelled like sweet strawberries and warm sunshine!",
                "voiceover_hindi": "बड़े पेड़ के नीचे एक चमकदार सतरंगी बेरी रखी थी! उसकी खुशबू मीठी स्ट्रॉबेरी और धूप जैसी थी!",
                "subtitle_text": "Under the tree sat a sparkling rainbow berry!",
                "highlight_words": ["sparkling", "rainbow"],
                "image_prompt": "3D Pixar style cute baby panda looking amazed at a glowing rainbow berry under a magical tree, vibrant colors, 8k",
                "camera_motion": "slow_zoom_out",
                "sfx_type": "pop"
            },
            {
                "scene_number": 3,
                "voiceover_english": "Just then, his best friend Toby the Tiger cub walked by with a very rumbling, hungry tummy!",
                "voiceover_hindi": "तभी उसका सबसे अच्छा दोस्त टोबी टाइगर भूखे पेट वहां से गुजरा!",
                "subtitle_text": "His friend Toby the Tiger was very hungry!",
                "highlight_words": ["Toby", "hungry!"],
                "image_prompt": "3D Pixar style cute baby panda and a cute baby tiger cub looking at a glowing berry together in a sunny meadow, 8k",
                "camera_motion": "slow_zoom_in",
                "sfx_type": "whoosh"
            },
            {
                "scene_number": 4,
                "voiceover_english": "Pippin smiled warmly, broke the magical berry in half, and shared it with his best friend Toby!",
                "voiceover_hindi": "पिपिन ने प्यार से मुस्कुराते हुए जादुई बेरी को आधा तोड़ा और अपने दोस्त टोबी के साथ बांट लिया!",
                "subtitle_text": "Pippin smiled and shared the magical berry!",
                "highlight_words": ["smiled", "shared"],
                "image_prompt": "3D Pixar style cute baby panda sharing a glowing fruit with a cute baby tiger cub, both smiling happily, magical sparkles, 8k",
                "camera_motion": "slow_zoom_out",
                "sfx_type": "sparkle"
            },
            {
                "scene_number": 5,
                "voiceover_english": "Suddenly, the whole tree bloomed with hundreds of treats! Because sharing with friends always creates pure magic!",
                "voiceover_hindi": "अचानक पूरे पेड़ पर ढेर सारे मीठे फल खिल उठे! क्योंकि दोस्तों के साथ बांटने से हमेशा सच्चा जादू होता है!",
                "subtitle_text": "Sharing with friends always creates pure magic!",
                "highlight_words": ["Sharing", "magic!"],
                "image_prompt": "3D Pixar style cute baby panda and baby tiger celebrating under a tree full of glowing colorful berries, rainbow in sky, 8k",
                "camera_motion": "slow_zoom_in",
                "sfx_type": "fanfare"
            }
        ]
    }

# =====================================================================
# 4. AI BRAIN ENGINE (MULTI-MODEL & VIRAL RETENTION HOOKS)
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
                "temperature": 0.75,
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
            except Exception as e:
                print(f"[Warning] {model_name} attempt {attempt} failed: {e}")
                time.sleep(2)
    return None

def generate_studio_video_plan():
    topic = pick_fresh_topic()
    print(f"\n[Selected Concept]: {topic}")

    prompt = f"""
    You are an award-winning Pixar/Disney creative director and YouTube Viral Strategist for the US Kids channel 'ToonTales Hub'.
    Create a complete, ultra-engaging 60-second animated story production plan based on this concept: "{topic}".
    Target Audience: Children aged 3 to 8 in the USA, UK, Canada, and Australia.

    VIRAL RULES:
    - Scene 1 MUST start with an immediate 3-second curiosity hook (e.g., "Wait! Look at that glowing box!", "Oh no! Where did the little star go?").
    - Every scene must use lively, sensory, emotional storytelling language.
    - Include 1 or 2 'highlight_words' per scene so our video engine colors them bright yellow on screen!

    Return STRICTLY a valid JSON object with this exact structure:
    {{
      "title": "Catchy, high-CTR YouTube title for kids (max 60 chars)",
      "thumbnail_badge": "2-3 word punchy badge for thumbnail (e.g. MAGIC SECRET!)",
      "viral_hook": "1-sentence exciting opening hook",
      "interactive_question": "Fun question for kids to answer",
      "description": "SEO-optimized YouTube description for parents and kids with moral of the story and hashtags",
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
          "voiceover_english": "Exciting, warm storytelling narration for scene 1 (14-20 words)",
          "voiceover_hindi": "उसी सीन का आसान और मज़ेदार हिंदी अनुवाद",
          "subtitle_text": "Short punchy subtitle text for screen (max 9 words)",
          "highlight_words": ["magic", "secret"],
          "image_prompt": "Full 3D Pixar studio quality scene description including the exact character_style_seed, vibrant lighting, 8k",
          "camera_motion": "slow_zoom_in",
          "sfx_type": "sparkle"
        }}
      ]
    }}
    Ensure there are exactly 5 scenes that tell a complete story with a happy moral ending.
    Allowed sfx_type values: "sparkle", "pop", "whoosh", "fanfare".
    Allowed camera_motion values: "slow_zoom_in", "slow_zoom_out".
    """

    video_plan = call_gemini_api(prompt)
    if not video_plan or "scenes" not in video_plan or not isinstance(video_plan.get("scenes"), list):
        video_plan = get_emergency_fallback_plan(topic)

    with open(OUTPUT_SCRIPT_FILE, "w", encoding="utf-8") as f:
        json.dump(video_plan, f, indent=2, ensure_ascii=False)

    # Save a clean human-readable SEO metadata text file as well
    try:
        with open(SEO_REPORT_PATH, "w", encoding="utf-8") as sf:
            sf.write(f"TITLE: {video_plan.get('title')}\n")
            sf.write(f"MORAL: {video_plan.get('moral')}\n\n")
            sf.write(f"DESCRIPTION:\n{video_plan.get('description')}\n\n")
            sf.write(f"TAGS: {', '.join(video_plan.get('tags', []))}\n")
    except Exception:
        pass

    save_used_topic(topic)
    return video_plan

# =====================================================================
# 5. US STUDIO VOICEOVER + CARTOON SFX + LULLABY SYNTHESIZER
# =====================================================================
async def _edge_tts_save(text, output_path, voice="en-US-AnaNeural"):
    import edge_tts
    communicate = edge_tts.Communicate(text, voice, rate="-4%", pitch="+6Hz")
    await communicate.save(output_path)

def generate_silent_wav(output_path, duration_sec=4.0):
    sample_rate = 22050
    total_samples = int(duration_sec * sample_rate)
    with wave.open(output_path, "w") as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(sample_rate)
        wf.writeframes(b"\x00\x00" * total_samples)
    return output_path

def generate_scene_audio(text, scene_num, chosen_voice="en-US-AnaNeural"):
    output_path = os.path.join("audio_clips", f"scene_{scene_num}.mp3")
    try:
        asyncio.run(_edge_tts_save(text, output_path, voice=chosen_voice))
        if os.path.exists(output_path) and os.path.getsize(output_path) > 500:
            print(f"  🎙️ [Voice] Scene {scene_num} HD US Neural Audio ({chosen_voice}) Ready")
            return output_path
    except Exception as e:
        print(f"  [Voice Fallback] Edge-TTS busy ({e}), switching to Google TTS...")

    try:
        from gtts import gTTS
        tts = gTTS(text=text, lang="en", tld="us", slow=False)
        tts.save(output_path)
        if os.path.exists(output_path) and os.path.getsize(output_path) > 300:
            print(f"  🎙️ [Voice] Scene {scene_num} Backup gTTS Audio Ready")
            return output_path
    except Exception as e2:
        print(f"  [Voice Warning] gTTS failed ({e2}), generating clean fallback wave...")

    wav_backup = os.path.join("audio_clips", f"scene_{scene_num}.wav")
    return generate_silent_wav(wav_backup, duration_sec=4.5)

def generate_cartoon_sfx_wav(sfx_type="sparkle", output_wav="temp_assets/sfx_sparkle.wav"):
    """बिना किसी बाहरी फाइल के 100% कॉपीराइट-फ्री कार्टून साउंड इफेक्ट्स (Chime, Pop, Whoosh, Fanfare) बनाता है"""
    sample_rate = 22050
    duration = 0.65
    total_samples = int(duration * sample_rate)

    with wave.open(output_wav, "w") as wav_file:
        wav_file.setnchannels(1)
        wav_file.setsampwidth(2)
        wav_file.setframerate(sample_rate)

        frames = bytearray()
        for i in range(total_samples):
            t = i / float(sample_rate)
            progress = i / float(total_samples)
            env = math.sin(math.pi * progress) * math.exp(-2.2 * progress)

            if sfx_type == "pop":
                freq = 280.0 + 620.0 * (progress ** 0.6)
                val = math.sin(2.0 * math.pi * freq * t) * env
            elif sfx_type == "whoosh":
                freq = 180.0 + 300.0 * math.sin(math.pi * progress)
                val = math.sin(2.0 * math.pi * freq * t) * env * 0.7
            elif sfx_type == "fanfare":
                notes = [523.25, 659.25, 783.99, 1046.50]
                idx = min(int(progress * len(notes)), len(notes) - 1)
                freq = notes[idx]
                val = (math.sin(2.0 * math.pi * freq * t) + 0.5 * math.sin(4.0 * math.pi * freq * t)) * env * 0.7
            else:  # sparkle chime
                notes = [1046.50, 1318.51, 1567.98, 2093.00]
                idx = min(int(progress * len(notes)), len(notes) - 1)
                freq = notes[idx]
                val = math.sin(2.0 * math.pi * freq * t) * env

            sample = int(val * 4200)
            frames.extend(struct.pack("<h", max(-32767, min(32767, sample))))
        wav_file.writeframes(frames)
    return output_wav

def generate_kids_background_music(duration_sec, output_wav="temp_assets/bg_music.wav"):
    """100% कॉपीराइट-फ्री जेंटल बच्चों की लोरी (Music Box + Warm Pad Harmony) जनरेट करता है"""
    sample_rate = 22050
    total_samples = int(duration_sec * sample_rate)
    melody_notes = [523.25, 659.25, 783.99, 880.00, 783.99, 659.25, 587.33, 523.25]
    bass_notes = [261.63, 261.63, 349.23, 349.23, 392.00, 392.00, 261.63, 261.63]
    note_len = int(sample_rate * 0.70)

    with wave.open(output_wav, "w") as wav_file:
        wav_file.setnchannels(1)
        wav_file.setsampwidth(2)
        wav_file.setframerate(sample_rate)

        frames = bytearray()
        for i in range(total_samples):
            t = i / float(sample_rate)
            idx = (i // note_len) % len(melody_notes)
            m_freq = melody_notes[idx]
            b_freq = bass_notes[idx]
            pos = (i % note_len) / float(note_len)

            # Soft music box pluck + warm underlying pad
            pluck_env = math.exp(-3.2 * pos) * math.sin(math.pi * min(1.0, pos * 10))
            pad_env = math.sin(math.pi * pos) * 0.35

            melody_wave = math.sin(2.0 * math.pi * m_freq * t) * pluck_env
            pad_wave = math.sin(2.0 * math.pi * b_freq * t) * pad_env
            combined = (melody_wave * 0.75) + (pad_wave * 0.25)

            sample = int(combined * 3000)  # Gentle background level (~9.5%)
            frames.extend(struct.pack("<h", max(-32767, min(32767, sample))))
        wav_file.writeframes(frames)
    return output_wav

# =====================================================================
# 6. 3D PIXAR IMAGE, HIGH-CTR THUMBNAIL & COLORED SUBTITLE ENGINE
# =====================================================================
def get_font(size):
    font_paths = [
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
        "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf",
        "/usr/share/fonts/truetype/freefont/FreeSansBold.ttf"
    ]
    for fp in font_paths:
        if os.path.exists(fp):
            try:
                return ImageFont.truetype(fp, size)
            except Exception:
                pass
    return ImageFont.load_default()

def create_fallback_poster(output_path, title_text, subtitle_text):
    img = Image.new("RGB", (1280, 720), color=(30, 110, 220))
    draw = ImageDraw.Draw(img)
    for y in range(720):
        r = int(35 + (y / 720) * 75)
        g = int(95 + (y / 720) * 110)
        b = int(225 - (y / 720) * 55)
        draw.line([(0, y), (1280, y)], fill=(r, g, b))
    draw.rectangle([36, 36, 1244, 684], outline=(255, 220, 60), width=10)
    font_lg = get_font(44)
    font_md = get_font(30)
    draw.text((85, 210), "TOONTALES HUB - 3D KIDS STUDIO", fill=(255, 235, 90), font=font_lg)
    draw.text((85, 310), title_text[:55], fill=(255, 255, 255), font=font_lg)
    draw.text((85, 405), subtitle_text[:75], fill=(235, 245, 255), font=font_md)
    img.save(output_path, "JPEG", quality=95)

def polish_viral_thumbnail(thumb_path, badge_text="3D KIDS STORY!"):
    """थंबनेल के चारों तरफ चमकदार गोल्डन बॉर्डर और ऊपर हाई-CTR बैज लगाता है ताकि बच्चे तुरंत क्लिक करें"""
    try:
        img = Image.open(thumb_path).convert("RGB").resize((1280, 720), PIL.Image.LANCZOS)
        draw = ImageDraw.Draw(img, "RGBA")
        # Bright golden outer frame
        draw.rectangle([10, 10, 1270, 710], outline=(255, 215, 0, 255), width=14)
        # Top-right viral badge
        badge_font = get_font(38)
        badge_clean = (badge_text or "NEW 3D STORY!").upper()[:18]
        draw.rounded_rectangle([820, 32, 1242, 108], radius=24, fill=(235, 35, 55, 245), outline=(255, 240, 100, 255), width=5)
        draw.text((848, 48), f"★ {badge_clean}", fill=(255, 255, 255, 255), font=badge_font)
        img.save(thumb_path, "JPEG", quality=96)
    except Exception as e:
        print(f"  [Thumbnail Polish Notice] {e}")

def decorate_scene_with_subtitles(image_path, subtitle_text, highlight_words=None, scene_idx=1, total_scenes=5, is_vertical=False):
    """फोटो के ऊपर 2-कलर हाइलाइटेड सबटाइटल्स (पीला + सफेद), प्रोग्रेस बार और ToonTales बैज लगाता है"""
    target_w, target_h = (1080, 1920) if is_vertical else (1280, 720)
    try:
        base = Image.open(image_path).convert("RGB")
    except Exception:
        base = Image.new("RGB", (target_w, target_h), color=(40, 120, 220))

    src_w, src_h = base.size
    scale = max(target_w / float(src_w), target_h / float(src_h))
    new_w, new_h = int(src_w * scale), int(src_h * scale)
    resized = base.resize((new_w, new_h), PIL.Image.LANCZOS)
    left = (new_w - target_w) // 2
    top = (new_h - target_h) // 2
    canvas = resized.crop((left, top, left + target_w, top + target_h))

    draw = ImageDraw.Draw(canvas, "RGBA")

    # 1. Top-left Studio Branding Badge
    badge_font = get_font(26 if not is_vertical else 34)
    badge_w = 315 if not is_vertical else 390
    badge_h = 54 if not is_vertical else 66
    draw.rounded_rectangle([24, 24, 24 + badge_w, 24 + badge_h], radius=18, fill=(18, 18, 42, 200), outline=(255, 215, 0, 255), width=3)
    draw.text((44, 36 if not is_vertical else 40), "★ ToonTales Hub", fill=(255, 235, 85, 255), font=badge_font)

    # 2. Scene Progress Dots (Top-right visual engagement tracker)
    dot_r = 10 if not is_vertical else 13
    start_x = target_w - (total_scenes * (dot_r * 3)) - 35
    for idx in range(1, total_scenes + 1):
        cx = start_x + idx * (dot_r * 3)
        cy = 50 if not is_vertical else 58
        color = (255, 220, 50, 255) if idx <= scene_idx else (255, 255, 255, 110)
        draw.ellipse([cx - dot_r, cy - dot_r, cx + dot_r, cy + dot_r], fill=color, outline=(20, 20, 40, 200), width=2)

    # 3. Bottom Two-Tone Subtitle Box (Yellow Keywords + White Text)
    if subtitle_text:
        sub_font = get_font(34 if not is_vertical else 44)
        words = subtitle_text.split()
        lines, current = [], []
        max_chars = 42 if not is_vertical else 24

        for w in words:
            tentative = " ".join(current + [w])
            if len(tentative) <= max_chars:
                current.append(w)
            else:
                if current:
                    lines.append(current)
                current = [w]
        if current:
            lines.append(current)
        lines = lines[:2]

        line_height = 56 if not is_vertical else 68
        box_h = line_height * len(lines) + 34
        box_y1 = target_h - box_h - (42 if not is_vertical else 190)
        box_y2 = box_y1 + box_h
        margin_x = 75 if not is_vertical else 45

        draw.rounded_rectangle(
            [margin_x, box_y1, target_w - margin_x, box_y2],
            radius=24,
            fill=(12, 14, 34, 220),
            outline=(255, 215, 60, 245),
            width=4
        )

        hl_set = set(w.lower().strip(".,!?") for w in (highlight_words or []))

        for l_idx, word_list in enumerate(lines):
            text_y = box_y1 + 18 + l_idx * line_height
            cur_x = margin_x + 32
            for w_idx, word in enumerate(word_list):
                clean_w = word.lower().strip(".,!?")
                # Highlight important words or the longest exciting word in bright yellow
                is_hl = (clean_w in hl_set) or (len(clean_w) >= 7 and w_idx % 2 == 1)
                fill_color = (255, 230, 55, 255) if is_hl else (255, 255, 255, 255)
                # Subtle dark text shadow for readability
                draw.text((cur_x + 2, text_y + 2), word, fill=(0, 0, 0, 220), font=sub_font)
                draw.text((cur_x, text_y), word, fill=fill_color, font=sub_font)
                # Advance x coordinate cleanly
                try:
                    bbox = draw.textbbox((cur_x, text_y), word + " ", font=sub_font)
                    cur_x = bbox[2]
                except Exception:
                    cur_x += int(len(word + " ") * (20 if not is_vertical else 25))

    out_suffix = "_vert.jpg" if is_vertical else "_sub.jpg"
    out_path = image_path.replace(".jpg", out_suffix)
    canvas.save(out_path, "JPEG", quality=95)
    return out_path

def create_end_screen_card(moral_text, is_vertical=False):
    """वीडियो के अंत में 3 सेकंड का सुंदर Moral Lesson + Subscribe कार्ड बनाता है"""
    target_w, target_h = (1080, 1920) if is_vertical else (1280, 720)
    img = Image.new("RGB", (target_w, target_h), color=(25, 35, 85))
    draw = ImageDraw.Draw(img, "RGBA")

    for y in range(target_h):
        r = int(25 + (y / float(target_h)) * 60)
        g = int(40 + (y / float(target_h)) * 90)
        b = int(110 + (y / float(target_h)) * 110)
        draw.line([(0, y), (target_w, y)], fill=(r, g, b))

    pad = 50
    draw.rounded_rectangle([pad, pad, target_w - pad, target_h - pad], radius=36, fill=(15, 20, 50, 200), outline=(255, 215, 0, 255), width=8)

    title_font = get_font(46 if not is_vertical else 52)
    moral_font = get_font(34 if not is_vertical else 40)
    cta_font = get_font(38 if not is_vertical else 44)

    center_y = target_h // 2 - 140
    draw.text((pad + 50, center_y), "★ MORAL OF THE STORY ★", fill=(255, 225, 70, 255), font=title_font)
    draw.text((pad + 50, center_y + 90), (moral_text or "Sharing and kindness always bring magic!")[:62], fill=(255, 255, 255, 255), font=moral_font)

    # Subscribe Callout Pill
    pill_y = center_y + 200
    draw.rounded_rectangle([pad + 50, pill_y, target_w - pad - 50, pill_y + 85], radius=24, fill=(230, 35, 55, 255), outline=(255, 255, 255, 255), width=4)
    draw.text((pad + 85, pill_y + 20), "👍 LIKE & SUBSCRIBE TO TOONTALES HUB!", fill=(255, 255, 255, 255), font=cta_font)

    out_path = os.path.join("temp_assets", "outro_vert.jpg" if is_vertical else "outro_land.jpg")
    img.save(out_path, "JPEG", quality=95)
    return out_path

def generate_scene_visual(prompt, subtitle_text, scene_num, is_thumbnail=False, badge_text="3D STORY!"):
    folder = "thumbnails" if is_thumbnail else "scene_images"
    filename = "thumbnail.jpg" if is_thumbnail else f"scene_{scene_num}.jpg"
    output_path = os.path.join(folder, filename)

    clean_prompt = f"3D Pixar Disney animation style, cute kids cartoon, bright vibrant colors, expressive eyes, {prompt}"
    encoded = urllib.parse.quote(clean_prompt[:360])
    seed = random.randint(1000, 99999)
    url = f"https://image.pollinations.ai/prompt/{encoded}?width=1280&height=720&seed={seed}&nologo=true"

    saved = False
    for attempt in range(1, 3):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
            with urllib.request.urlopen(req, timeout=35) as resp:
                img_data = resp.read()
                if len(img_data) > 5000:
                    with open(output_path, "wb") as f:
                        f.write(img_data)
                    print(f"  🎨 [3D Visual] Saved HD Image: {output_path}")
                    saved = True
                    break
        except Exception as e:
            print(f"  [Visual Retry {attempt}/2] Cloud AI Image busy ({e})...")
            time.sleep(2)

    if not saved:
        create_fallback_poster(output_path, f"Scene {scene_num} - ToonTales Hub", subtitle_text)
        print(f"  🎨 [3D Visual] Saved Studio Fallback Image: {output_path}")

    if is_thumbnail:
        polish_viral_thumbnail(output_path, badge_text=badge_text)

    return output_path

# =====================================================================
# 7. FULL MOVIEPY VIDEO COMPILER (16:9 HD + 9:16 SHORTS + SFX + MUSIC)
# =====================================================================
def render_complete_videos(plan):
    from moviepy.editor import (
        ImageClip,
        AudioFileClip,
        CompositeAudioClip,
        concatenate_videoclips
    )

    scenes = plan.get("scenes", [])
    total_scenes = max(1, len(scenes))
    landscape_clips = []
    vertical_clips = []

    print("\n🎬 STEP 3: Compiling 3D Video Clips, Colored Subtitles, SFX & Voiceovers...")
    for idx, s in enumerate(scenes, start=1):
        s_num = s.get("scene_number", idx)
        vo_text = s.get("voiceover_english", "Welcome to ToonTales Hub!")
        sub_text = s.get("subtitle_text", vo_text)
        hl_words = s.get("highlight_words", [])
        cam_motion = s.get("camera_motion", "slow_zoom_in")
        sfx_type = s.get("sfx_type", "sparkle")

        img_raw = os.path.join("scene_images", f"scene_{s_num}.jpg")
        aud_path = os.path.join("audio_clips", f"scene_{s_num}.mp3")
        if not os.path.exists(aud_path):
            aud_path = os.path.join("audio_clips", f"scene_{s_num}.wav")

        if not os.path.exists(img_raw):
            create_fallback_poster(img_raw, f"Scene {s_num}", sub_text)

        img_land = decorate_scene_with_subtitles(img_raw, sub_text, hl_words, idx, total_scenes, is_vertical=False)
        img_vert = decorate_scene_with_subtitles(img_raw, sub_text, hl_words, idx, total_scenes, is_vertical=True)

        voice_clip = None
        duration = 5.5
        if os.path.exists(aud_path) and os.path.getsize(aud_path) > 300:
            try:
                voice_clip = AudioFileClip(aud_path)
                duration = max(3.5, voice_clip.duration + 0.40)
            except Exception as e:
                print(f"  [Audio Load Warning] Scene {s_num}: {e}")

        # Combine voiceover with subtle cartoon sound effect at start of scene
        combined_scene_audio = voice_clip
        try:
            sfx_wav = generate_cartoon_sfx_wav(sfx_type, os.path.join("temp_assets", f"sfx_{s_num}.wav"))
            sfx_clip = AudioFileClip(sfx_wav)
            if voice_clip:
                combined_scene_audio = CompositeAudioClip([voice_clip, sfx_clip])
            else:
                combined_scene_audio = sfx_clip
        except Exception:
            pass

        # Dynamic Zoom Effect (Alternating Zoom-In and Zoom-Out for high visual retention)
        clip_l = ImageClip(img_land).set_duration(duration)
        if cam_motion == "slow_zoom_out":
            clip_l = clip_l.resize(lambda t, d=duration: 1.04 - 0.035 * (t / d))
        else:
            clip_l = clip_l.resize(lambda t, d=duration: 1.0 + 0.04 * (t / d))

        if combined_scene_audio:
            clip_l = clip_l.set_audio(combined_scene_audio)
        landscape_clips.append(clip_l)

        # Vertical 9:16 Shorts Clip
        clip_v = ImageClip(img_vert).set_duration(duration)
        if combined_scene_audio:
            clip_v = clip_v.set_audio(combined_scene_audio)
        vertical_clips.append(clip_v)

    # Add 2.8-second interactive Moral + Subscribe Outro Card
    try:
        moral_str = plan.get("moral", "Sharing with friends always doubles the joy!")
        outro_l_img = create_end_screen_card(moral_str, is_vertical=False)
        outro_v_img = create_end_screen_card(moral_str, is_vertical=True)
        outro_sfx = generate_cartoon_sfx_wav("fanfare", os.path.join("temp_assets", "outro_fanfare.wav"))
        outro_aud = AudioFileClip(outro_sfx)

        outro_l_clip = ImageClip(outro_l_img).set_duration(2.8).set_audio(outro_aud)
        outro_v_clip = ImageClip(outro_v_img).set_duration(2.8).set_audio(outro_aud)
        landscape_clips.append(outro_l_clip)
        vertical_clips.append(outro_v_clip)
    except Exception as oe:
        print(f"  [Outro Notice] {oe}")

    final_land = concatenate_videoclips(landscape_clips, method="compose")
    final_vert = concatenate_videoclips(vertical_clips, method="compose")

    # Mix gentle background music box lullaby under the entire video
    try:
        bg_wav = generate_kids_background_music(final_land.duration + 1.0)
        bg_audio = AudioFileClip(bg_wav).subclip(0, final_land.duration)
        if final_land.audio:
            mixed_audio = CompositeAudioClip([final_land.audio, bg_audio])
            final_land = final_land.set_audio(mixed_audio)
            final_vert = final_vert.set_audio(mixed_audio)
        else:
            final_land = final_land.set_audio(bg_audio)
            final_vert = final_vert.set_audio(bg_audio)
    except Exception as e:
        print(f"  [BG Music Notice] Proceeding with voiceover audio: {e}")

    print(f"  📽️ Rendering Full HD Landscape Video -> {FINAL_VIDEO_PATH}")
    final_land.write_videofile(
        FINAL_VIDEO_PATH,
        fps=24,
        codec="libx264",
        audio_codec="aac",
        threads=2,
        preset="ultrafast",
        logger=None
    )

    print(f"  📱 Rendering Vertical YouTube Short -> {FINAL_SHORT_PATH}")
    final_vert.write_videofile(
        FINAL_SHORT_PATH,
        fps=24,
        codec="libx264",
        audio_codec="aac",
        threads=2,
        preset="ultrafast",
        logger=None
    )

    final_land.close()
    final_vert.close()
    print("  ✅ Both Full Video (16:9) & YouTube Short (9:16) Rendered Successfully!")

# =====================================================================
# 8. AUTOMATIC YOUTUBE UPLOADER (OPTIONAL VIA GITHUB SECRETS)
# =====================================================================
def upload_to_youtube_if_configured(plan, video_path):
    client_id = os.environ.get("YOUTUBE_CLIENT_ID", "").strip()
    client_secret = os.environ.get("YOUTUBE_CLIENT_SECRET", "").strip()
    refresh_token = os.environ.get("YOUTUBE_REFRESH_TOKEN", "").strip()

    if not (client_id and client_secret and refresh_token):
        print("\nℹ️ [YouTube Auto-Upload]: YouTube API Secrets not added yet.")
        print("   Your MP4 videos are safely saved in 'output_videos/' and GitHub Artifacts for direct download!")
        return None

    print("\n🚀 STEP 4: Uploading Video Directly to YouTube Channel...")
    try:
        from google.oauth2.credentials import Credentials
        from googleapiclient.discovery import build
        from googleapiclient.http import MediaFileUpload

        creds = Credentials(
            None,
            refresh_token=refresh_token,
            token_uri="https://oauth2.googleapis.com/token",
            client_id=client_id,
            client_secret=client_secret
        )
        youtube = build("youtube", "v3", credentials=creds)

        body = {
            "snippet": {
                "title": plan.get("title", "Cute 3D Kids Moral Story | ToonTales Hub")[:95],
                "description": plan.get("description", "Fun 3D animated moral story for kids!"),
                "tags": plan.get("tags", ["kids cartoon", "3d animation", "moral stories"]),
                "categoryId": "1",
                "defaultLanguage": "en-US"
            },
            "status": {
                "privacyStatus": "public",
                "selfDeclaredMadeForKids": True
            }
        }

        media = MediaFileUpload(video_path, chunksize=-1, resumable=True, mimetype="video/mp4")
        request = youtube.videos().insert(part="snippet,status", body=body, media_body=media)
        response = request.execute()
        video_id = response.get("id")
        print(f"🎉 YOUTUBE UPLOAD SUCCESS! Live Video URL: https://youtu.be/{video_id}")

        thumb_path = os.path.join("thumbnails", "thumbnail.jpg")
        if os.path.exists(thumb_path) and video_id:
            try:
                youtube.thumbnails().set(
                    videoId=video_id,
                    media_body=MediaFileUpload(thumb_path, mimetype="image/jpeg")
                ).execute()
                print("🖼️ Custom High-CTR 3D Thumbnail uploaded to YouTube!")
            except Exception as te:
                print(f"  [Thumbnail Notice] Custom thumbnail skipped: {te}")

        return video_id
    except Exception as e:
        print(f"⚠️ [YouTube Upload Warning] Could not auto-upload ({e}). Video is safely stored in Artifacts!")
        return None

# =====================================================================
# 9. MAIN EXECUTION PIPELINE
# =====================================================================
if __name__ == "__main__":
    print("====================================================")
    print("   TOONTALES HUB - VIRAL 3D AI STUDIO BOT V10       ")
    print("====================================================")

    try:
        # Step 1: Story & Viral Script Plan
        plan = generate_studio_video_plan()
        scenes = plan.get("scenes", [])
        chosen_voice = random.choice(US_KIDS_VOICES)
        print("\n✅ STEP 1: Viral Studio Video Plan Generated Successfully!")
        print(f"📌 Video Title : {plan.get('title')}")
        print(f"💡 Story Moral : {plan.get('moral', 'Always be kind and helpful!')}")
        print(f"🎙️ Narrator    : {chosen_voice}")

        # Step 2: Voiceovers & 3D Images
        print("\n🚀 STEP 2: Generating Studio Voiceovers & 3D Visual Assets...")
        for idx, s in enumerate(scenes, start=1):
            s_num = s.get("scene_number", idx)
            vo_en = s.get("voiceover_english", "Welcome to ToonTales Hub!")
            sub = s.get("subtitle_text", vo_en)
            img_p = s.get("image_prompt", plan.get("character_style_seed", "Cute 3D panda"))

            generate_scene_audio(vo_en, s_num, chosen_voice=chosen_voice)
            generate_scene_visual(img_p, sub, s_num, is_thumbnail=False)

        # High-CTR Thumbnail with Golden Frame & Badge
        thumb_prompt = plan.get("thumbnail_prompt", plan.get("title", "Cute 3D Cartoon"))
        badge_txt = plan.get("thumbnail_badge", "3D KIDS STORY!")
        generate_scene_visual(thumb_prompt, plan.get("title", "ToonTales Hub"), 0, is_thumbnail=True, badge_text=badge_txt)

        # Step 3: Render MP4 Videos (16:9 Full + 9:16 Shorts + SFX + Outro)
        render_complete_videos(plan)

        # Step 4: Auto-Upload to YouTube (if Secrets exist)
        upload_to_youtube_if_configured(plan, FINAL_VIDEO_PATH)

        print("\n====================================================")
        print("🎉 100% COMPLETE! VIRAL MP4 VIDEOS, SFX & THUMBNAIL READY!")
        print(f"🎬 Main Video  : {FINAL_VIDEO_PATH}")
        print(f"📱 Short Video : {FINAL_SHORT_PATH}")
        print(f"📄 SEO Report  : {SEO_REPORT_PATH}")
        print("====================================================")
    except Exception as err:
        print(f"\n❌ UNEXPECTED ERROR: {err}")
        exit(1)
