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
# 1. CONFIGURATION & V19 HYPER-CINEMATIC APEX SETTINGS
# =====================================================================
DEFAULT_API_KEY = "AQ.Ab8RN6LYwTy4uxCtviZ9HmyJHlQmfRTNUJVPglDhixRCOUR5rg"
env_key = os.environ.get("GEMINI_API_KEY", "").strip()
GEMINI_API_KEY = env_key if env_key else DEFAULT_API_KEY

GEMINI_MODELS = [
    "gemini-2.5-flash",
    "gemini-flash-latest",
    "gemini-2.0-flash",
    "gemini-1.5-flash"
]

HISTORY_FILE = "used_topics.json"
OUTPUT_SCRIPT_FILE = "latest_video_plan.json"
FINAL_LONG_VIDEO_PATH = os.path.join("output_videos", "jarvis_apex_5min_story.mp4")
SHORTS_OUTPUT_DIR = os.path.join("output_videos", "viral_shorts_clips")
SEO_REPORT_PATH = os.path.join("output_videos", "youtube_seo_metadata.txt")

DIRS = ["output_videos", "temp_assets", "audio_clips", "scene_images", "thumbnails", SHORTS_OUTPUT_DIR]
for d in DIRS:
    os.makedirs(d, exist_ok=True)

# 45 Ultra-Engaging US Kids Moral Story Themes with High Search Intent
KIDS_THEMES = [
    "A magical glowing tree in the enchanted forest that grants kind wishes",
    "A brave little star who fell from the night sky and needed his friends to guide him back",
    "A clever little bunny who built a flying carrot-car to explore the clouds",
    "A friendly baby dragon who learned to breathe warm rainbow bubbles instead of fire",
    "An underwater kingdom adventure with a singing dolphin and a glowing pearl",
    "A cheerful little bear who opened a honey bakery for all the forest animals",
    "A tiny magical fairy who repaired broken toys with fairy dust and laughter",
    "A curious little puppy who discovered a secret rainbow tunnel behind his doghouse",
    "A wise old owl who taught a young squirrel how patience brings the sweetest nuts",
    "A bouncy little frog who wanted to jump high enough to touch the fluffy moon",
    "A sweet kitten who baked star-shaped cookies to make her grumpy neighbor smile",
    "A tiny turtle who built a tiny sailboat to cross the sparkling garden pond",
    "A cheerful little cloud who brought refreshing rainbow rain to thirsty flowers",
    "A brave baby penguin who led his colony to a valley of endless ice slides",
    "A magical paintbrush that brings colorful drawings to life in a sleepy town",
    "A polite little fox who learned the true power of saying Please and Thank You",
    "A sparkling bluebird who sang cheerful morning songs to wake up the sun",
    "A gentle giant elephant who used his big ears as a parachute for baby birds",
    "A little hedgehog who shared his warm cozy scarf on a snowy winter morning",
    "A playful dolphin who organized a musical sea festival for ocean friends",
    "A smart squirrel who planted a golden acorn that grew into a castle of sweets",
    "A sleepy little koala who threw a forest talent show for everyone to enjoy",
    "A courageous mouse who sailed across a puddle in a giant leaf sailboat",
    "A baby tiger who overcame his fear of the dark with a glowing firefly friend",
    "A happy little train that delivered sweet dreams to sleeping animals every night",
    "A tiny firefly who learned that even the smallest light can brighten a dark cave",
    "A clever little beaver who built a water slide for all the river animals",
    "A joyful little lamb who discovered a meadow of singing flowers",
    "A hardworking honeybee who shared her golden nectar with a thirsty butterfly",
    "A magical music box that filled the sleepy village with dancing stars"
]

US_KIDS_VOICES = [
    "en-US-AnaNeural",
    "en-US-AriaNeural",
    "en-US-JennyNeural"
]

# =====================================================================
# 2. MEMORY SYSTEM (NO REPEAT STORIES TRACKER)
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
            json.dump(topics[-450:], f, indent=2, ensure_ascii=False)

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
    print("[Apex Engine] Activating Cinematic Studio Backup Plan...")
    return {
        "title": "The Magical Glowing Tree! | 3D Pixar Style Cartoon",
        "thumbnail_badge": "MAGIC SECRET!",
        "viral_hook": "Wait! Look at that glowing magic tree shining bright in the enchanted forest!",
        "moral": "Kindness and sharing bring true magical rewards!",
        "tags": ["kids cartoon", "3d animation", "toontales hub", "bedtime stories", "moral stories", "pixar animation"],
        "youtube_settings": {"categoryId": "1", "madeForKids": True, "defaultLanguage": "en-US"},
        "character_style_seed": "Ultra vibrant 3D Pixar Disney animation style, cinematic studio lighting, highly detailed fur and textures, 8k",
        "thumbnail_prompt": "Vibrant 3D Pixar style magical glowing tree with golden leaves in a colorful fairy forest, highly detailed, 8k",
        "scenes": [
            {
                "scene_number": 1,
                "voiceover_english": "Wait! Look at that magical glowing tree shining bright in the middle of the enchanted forest!",
                "subtitle_text": "Look at that magical glowing tree shining bright!",
                "highlight_words": ["magical", "glowing"],
                "image_prompt": "Ultra vibrant 3D Pixar style glowing magical tree with sparkling golden leaves in a fairy forest, cinematic lighting, 8k",
                "camera_motion": "zoom_in",
                "sfx_type": "sparkle"
            },
            {
                "scene_number": 2,
                "voiceover_english": "Little Barnaby the Bear rushed over and found a shiny golden crown resting on the roots!",
                "subtitle_text": "Barnaby found a shiny golden crown!",
                "highlight_words": ["golden", "crown!"],
                "image_prompt": "3D Pixar style cute chubby bear looking amazed at a shiny golden crown on tree roots, colorful magical background, 8k",
                "camera_motion": "pan_right",
                "sfx_type": "pop"
            },
            {
                "scene_number": 3,
                "voiceover_english": "Instead of keeping it, Barnaby shared it with all his tired woodland friends!",
                "subtitle_text": "Barnaby shared it with all his friends!",
                "highlight_words": ["shared", "friends!"],
                "image_prompt": "3D Pixar style cute baby bear sharing a glowing crown with forest animals, joyful expressions, vibrant colors, 8k",
                "camera_motion": "zoom_out",
                "sfx_type": "whoosh"
            },
            {
                "scene_number": 4,
                "voiceover_english": "Suddenly, the entire forest burst into a shower of rainbow fireworks and joyful music!",
                "subtitle_text": "The entire forest burst into rainbow fireworks!",
                "highlight_words": ["rainbow", "fireworks!"],
                "image_prompt": "3D Pixar style forest animals celebrating under colorful rainbow fireworks in the night sky, magical sparkles, 8k",
                "camera_motion": "zoom_in",
                "sfx_type": "fanfare"
            },
            {
                "scene_number": 5,
                "voiceover_english": "And from that day on, everyone in the enchanted forest learned that sharing is true magic!",
                "subtitle_text": "Sharing is true magic for everyone!",
                "highlight_words": ["sharing", "magic!"],
                "image_prompt": "3D Pixar style forest animals cheering together happily under a rainbow sky, 8k",
                "camera_motion": "zoom_in",
                "sfx_type": "fanfare"
            },
            {
                "scene_number": 6,
                "voiceover_english": "Remember kids, a kind heart shines brighter than the biggest star in the night sky!",
                "subtitle_text": "A kind heart shines brighter than the stars!",
                "highlight_words": ["kind", "heart"],
                "image_prompt": "3D Pixar style cute animals looking up at a starry night sky smiling, warm cozy lighting, 8k",
                "camera_motion": "zoom_out",
                "sfx_type": "sparkle"
            }
        ]
    }

# =====================================================================
# 4. AI SCRIPT GENERATOR
# =====================================================================
def call_gemini_api(prompt):
    for model_name in GEMINI_MODELS:
        url = f"https://generativelanguage.googleapis.com/v1beta/models/{model_name}:generateContent"
        headers = {"Content-Type": "application/json", "X-goog-api-key": GEMINI_API_KEY}
        payload = {
            "contents": [{"parts": [{"text": prompt}]}],
            "generationConfig": {"temperature": 0.85, "responseMimeType": "application/json"}
        }
        data = json.dumps(payload).encode("utf-8")
        for attempt in range(1, 3):
            try:
                print(f"[Apex Brain] Requesting '{model_name}' (Attempt {attempt}/2)...")
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
    You are an expert Hollywood Pixar Creative Director and Child Psychologist. Create an ultra-engaging rich animated story plan (with 6 detailed rich scenes) based on: "{topic}".
    Target Audience: Children aged 3 to 8 in USA, UK, Canada, Australia.
    VIRAL RULES:
    - Scene 1 MUST start with an immediate exciting hook.
    - Provide 1-2 'highlight_words' per scene for vibrant yellow caption highlighting.
    - Provide engaging camera_motion ("zoom_in", "zoom_out", "pan_right") and sfx_type ("sparkle", "pop", "whoosh", "fanfare").

    Return STRICTLY valid JSON:
    {{
      "title": "Catchy Viral YouTube Title for Kids (max 60 chars)",
      "thumbnail_badge": "MAGIC SECRET!",
      "viral_hook": "1-sentence exciting opening hook",
      "moral": "Clear 1-line moral lesson",
      "tags": ["kids cartoon", "3d animation", "toontales hub", "bedtime stories"],
      "youtube_settings": {{"categoryId": "1", "madeForKids": true, "defaultLanguage": "en-US"}},
      "character_style_seed": "Ultra vibrant 3D Pixar Disney animation style, cinematic lighting, 8k",
      "thumbnail_prompt": "Vibrant 3D Pixar style thumbnail prompt, ultra-expressive cute characters, 8k",
      "scenes": [
        {{
          "scene_number": 1,
          "voiceover_english": "Engaging narration sentence for scene 1 (25-30 words rich storytelling)",
          "subtitle_text": "Punchy short subtitle text",
          "highlight_words": ["magical", "secret"],
          "image_prompt": "Ultra vibrant 3D Pixar studio quality scene description, 8k",
          "camera_motion": "zoom_in",
          "sfx_type": "sparkle"
        }}
      ]
    }}
    Include exactly 6 wonderful scenes to make a rich, long narrative story.
    """
    plan = call_gemini_api(prompt)
    if not plan or "scenes" not in plan or not isinstance(plan.get("scenes"), list):
        plan = get_emergency_fallback_plan(topic)

    with open(OUTPUT_SCRIPT_FILE, "w", encoding="utf-8") as f:
        json.dump(plan, f, indent=2, ensure_ascii=False)

    try:
        with open(SEO_REPORT_PATH, "w", encoding="utf-8") as sf:
            sf.write(f"TITLE: {plan.get('title')}\n")
            sf.write(f"HOOK: {plan.get('viral_hook')}\n")
            sf.write(f"MORAL: {plan.get('moral')}\n\n")
            sf.write(f"TAGS: {', '.join(plan.get('tags', []))}\n")
    except Exception:
        pass

    save_used_topic(topic)
    return plan

# =====================================================================
# 5. AUDIO & SYNTHESIZER
# =====================================================================
async def _edge_tts_save(text, output_path, voice="en-US-AnaNeural"):
    import edge_tts
    communicate = edge_tts.Communicate(text, voice, rate="-3%", pitch="+5Hz")
    await communicate.save(output_path)

def generate_scene_audio(text, scene_num, chosen_voice="en-US-AnaNeural"):
    output_path = os.path.join("audio_clips", f"scene_{scene_num}.mp3")
    try:
        asyncio.run(_edge_tts_save(text, output_path, voice=chosen_voice))
        if os.path.exists(output_path) and os.path.getsize(output_path) > 500:
            return output_path
    except Exception:
        pass

    try:
        from gtts import gTTS
        tts = gTTS(text=text, lang="en", tld="us", slow=False)
        tts.save(output_path)
        if os.path.exists(output_path) and os.path.getsize(output_path) > 300:
            return output_path
    except Exception:
        pass

    wav_fallback = os.path.join("audio_clips", f"scene_{scene_num}.wav")
    sample_rate = 22050
    total_samples = int(4.5 * sample_rate)
    with wave.open(wav_fallback, "w") as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(sample_rate)
        wf.writeframes(b"\x00\x00" * total_samples)
    return wav_fallback

def generate_cartoon_sfx_wav(sfx_type="sparkle", output_wav="temp_assets/sfx.wav"):
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
            env = math.sin(math.pi * progress) * math.exp(-2.0 * progress)
            if sfx_type == "pop":
                freq = 280.0 + 600.0 * (progress ** 0.5)
                val = math.sin(2.0 * math.pi * freq * t) * env
            elif sfx_type == "whoosh":
                freq = 180.0 + 350.0 * math.sin(math.pi * progress)
                val = math.sin(2.0 * math.pi * freq * t) * env * 0.7
            elif sfx_type == "fanfare":
                notes = [523.25, 659.25, 783.99, 1046.50]
                idx = min(int(progress * len(notes)), len(notes) - 1)
                freq = notes[idx]
                val = (math.sin(2.0 * math.pi * freq * t) + 0.5 * math.sin(4.0 * math.pi * freq * t)) * env * 0.7
            else:
                notes = [1046.50, 1318.51, 1567.98, 2093.00]
                idx = min(int(progress * len(notes)), len(notes) - 1)
                freq = notes[idx]
                val = math.sin(2.0 * math.pi * freq * t) * env
            sample = int(val * 4200)
            frames.extend(struct.pack("<h", max(-32767, min(32767, sample))))
        wav_file.writeframes(frames)
    return output_wav

def generate_kids_background_music(duration_sec, output_wav="temp_assets/bg.wav"):
    sample_rate = 22050
    total_samples = int(duration_sec * sample_rate)
    melody_notes = [523.25, 659.25, 783.99, 880.00, 783.99, 659.25, 587.33, 523.25]
    note_len = int(sample_rate * 0.75)
    with wave.open(output_wav, "w") as wav_file:
        wav_file.setnchannels(1)
        wav_file.setsampwidth(2)
        wav_file.setframerate(sample_rate)
        frames = bytearray()
        for i in range(total_samples):
            t = i / float(sample_rate)
            idx = (i // note_len) % len(melody_notes)
            freq = melody_notes[idx]
            pos = (i % note_len) / float(note_len)
            env = math.exp(-3.0 * pos) * math.sin(math.pi * pos)
            val = math.sin(2.0 * math.pi * freq * t) * env
            sample = int(val * 1800)
            frames.extend(struct.pack("<h", max(-32767, min(32767, sample))))
        wav_file.writeframes(frames)
    return output_wav

# =====================================================================
# 6. VISUALS & SUBTITLES DECORATOR
# =====================================================================
def get_font(size):
    for fp in [
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
        "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf",
        "/usr/share/fonts/truetype/freefont/FreeSansBold.ttf"
    ]:
        if os.path.exists(fp):
            try:
                return ImageFont.truetype(fp, size)
            except Exception:
                pass
    return ImageFont.load_default()

def decorate_scene_with_subtitles(image_path, subtitle_text, highlight_words=None, scene_idx=1, total_scenes=6, is_vertical=False):
    target_w, target_h = (1080, 1920) if is_vertical else (1280, 720)
    try:
        base = Image.open(image_path).convert("RGB")
    except Exception:
        base = Image.new("RGB", (target_w, target_h), color=(30, 100, 200))

    src_w, src_h = base.size
    scale = max(target_w / float(src_w), target_h / float(src_h))
    new_w, new_h = int(src_w * scale), int(src_h * scale)
    resized = base.resize((new_w, new_h), PIL.Image.LANCZOS)
    left = (new_w - target_w) // 2
    top = (new_h - target_h) // 2
    canvas = resized.crop((left, top, left + target_w, top + target_h))

    draw = ImageDraw.Draw(canvas, "RGBA")

    # Branding Badge
    badge_font = get_font(26 if not is_vertical else 34)
    draw.rounded_rectangle([24, 24, 320, 78], radius=18, fill=(15, 15, 40, 210), outline=(255, 215, 0, 255), width=3)
    draw.text((44, 36 if not is_vertical else 40), "★ ToonTales Hub", fill=(255, 235, 80, 255), font=badge_font)

    # Scene Progress Dots Tracker
    dot_r = 10 if not is_vertical else 13
    start_x = target_w - (total_scenes * (dot_r * 3)) - 35
    for idx in range(1, total_scenes + 1):
        cx = start_x + idx * (dot_r * 3)
        cy = 50 if not is_vertical else 58
        color = (255, 220, 50, 255) if idx <= scene_idx else (255, 255, 255, 110)
        draw.ellipse([cx - dot_r, cy - dot_r, cx + dot_r, cy + dot_r], fill=color, outline=(20, 20, 40, 200), width=2)

    # Subtitles Box
    if subtitle_text:
        sub_font = get_font(36 if not is_vertical else 46)
        words = subtitle_text.split()
        lines, current = [], []
        max_chars = 38 if not is_vertical else 22
        for w in words:
            if len(" ".join(current + [w])) <= max_chars:
                current.append(w)
            else:
                if current:
                    lines.append(current)
                current = [w]
        if current:
            lines.append(current)
        lines = lines[:2]

        box_h = 60 * len(lines) + 32
        box_y1 = target_h - box_h - (45 if not is_vertical else 180)
        box_y2 = box_y1 + box_h
        margin_x = 70 if not is_vertical else 40

        draw.rounded_rectangle([margin_x, box_y1, target_w - margin_x, box_y2], radius=24, fill=(10, 12, 35, 230), outline=(255, 220, 60, 255), width=4)

        hl_set = set(w.lower().strip(".,!?") for w in (highlight_words or []))
        for l_idx, word_list in enumerate(lines):
            text_y = box_y1 + 18 + l_idx * 58
            cur_x = margin_x + 30
            for w_idx, word in enumerate(word_list):
                clean_w = word.lower().strip(".,!?")
                is_hl = (clean_w in hl_set) or (len(clean_w) >= 6 and w_idx % 2 == 1)
                fill_color = (255, 230, 50, 255) if is_hl else (255, 255, 255, 255)
                draw.text((cur_x + 2, text_y + 2), word, fill=(0, 0, 0, 220), font=sub_font)
                draw.text((cur_x, text_y), word, fill=fill_color, font=sub_font)
                try:
                    bbox = draw.textbbox((cur_x, text_y), word + " ", font=sub_font)
                    cur_x = bbox[2]
                except Exception:
                    cur_x += int(len(word + " ") * 22)

    out_suffix = "_vert.jpg" if is_vertical else "_sub.jpg"
    out_path = image_path.replace(".jpg", out_suffix)
    canvas.save(out_path, "JPEG", quality=95)
    return out_path

def create_end_screen_card(moral_text, is_vertical=False):
    target_w, target_h = (1080, 1920) if is_vertical else (1280, 720)
    img = Image.new("RGB", (target_w, target_h), color=(25, 35, 85))
    draw = ImageDraw.Draw(img, "RGBA")
    for y in range(target_h):
        r = int(25 + (y / float(target_h)) * 60)
        g = int(40 + (y / float(target_h)) * 90)
        b = int(110 + (y / float(target_h)) * 110)
        draw.line([(0, y), (target_w, y)], fill=(r, g, b))

    pad = 50
    draw.rounded_rectangle([pad, pad, target_w - pad, target_h - pad], radius=36, fill=(15, 20, 50, 220), outline=(255, 215, 0, 255), width=8)

    title_font = get_font(46 if not is_vertical else 52)
    moral_font = get_font(34 if not is_vertical else 40)
    cta_font = get_font(38 if not is_vertical else 44)

    center_y = target_h // 2 - 140
    draw.text((pad + 50, center_y), "★ MORAL OF THE STORY ★", fill=(255, 225, 70, 255), font=title_font)
    draw.text((pad + 50, center_y + 90), (moral_text or "Sharing and kindness always bring magic!")[:62], fill=(255, 255, 255, 255), font=moral_font)

    pill_y = center_y + 200
    draw.rounded_rectangle([pad + 50, pill_y, target_w - pad - 50, pill_y + 85], radius=24, fill=(230, 35, 55, 255), outline=(255, 255, 255, 255), width=4)
    draw.text((pad + 85, pill_y + 20), "👍 LIKE & SUBSCRIBE TO TOONTALES HUB!", fill=(255, 255, 255, 255), font=cta_font)

    out_path = os.path.join("temp_assets", "outro_vert.jpg" if is_vertical else "outro_land.jpg")
    img.save(out_path, "JPEG", quality=95)
    return out_path

def generate_scene_visual(prompt, subtitle_text, scene_num, is_thumbnail=False, badge_text="3D KIDS STORY!"):
    folder = "thumbnails" if is_thumbnail else "scene_images"
    filename = "thumbnail.jpg" if is_thumbnail else f"scene_{scene_num}.jpg"
    output_path = os.path.join(folder, filename)

    clean_prompt = f"Ultra vibrant 3D Pixar Disney animation style, cinematic lighting, sharp detailed textures, expressive cute characters, {prompt}"
    encoded = urllib.parse.quote(clean_prompt[:380])
    seed = random.randint(1000, 99999)
    url = f"https://image.pollinations.ai/prompt/{encoded}?width=1280&height=720&seed={seed}&nologo=true"

    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=35) as resp:
            img_data = resp.read()
            if len(img_data) > 5000:
                with open(output_path, "wb") as f:
                    f.write(img_data)
                if is_thumbnail:
                    img = Image.open(output_path).convert("RGB")
                    draw = ImageDraw.Draw(img)
                    draw.rectangle([10, 10, 1270, 710], outline=(255, 215, 0), width=14)
                    badge_font = get_font(38)
                    draw.rounded_rectangle([820, 32, 1242, 108], radius=24, fill=(235, 35, 55, 245), outline=(255, 240, 100, 255), width=5)
                    draw.text((848, 48), f"★ {badge_text.upper()[:16]}", fill=(255, 255, 255), font=badge_font)
                    img.save(output_path, "JPEG", quality=96)
                return output_path
    except Exception:
        pass

    img = Image.new("RGB", (1280, 720), color=(30, 110, 220))
    img.save(output_path, "JPEG", quality=95)
    return output_path

# =====================================================================
# 7. MASTER COMPILER (SEPARATE 5-MIN LONG VIDEO & MULTI-SHORTS GENERATOR)
# =====================================================================
def render_master_videos_and_shorts(plan):
    from moviepy.editor import ImageClip, AudioFileClip, CompositeAudioClip, concatenate_videoclips, vfx

    scenes = plan.get("scenes", [])
    total_scenes = max(1, len(scenes))
    landscape_clips = []
    vertical_clips = []

    print("\n🎬 [Apex Studio] Compiling 5-Min Master Video & Cutting Viral Shorts...")
    for idx, s in enumerate(scenes, start=1):
        s_num = s.get("scene_number", idx)
        vo_text = s.get("voiceover_english", "Welcome to ToonTales Hub!")
        sub_text = s.get("subtitle_text", vo_text)
        hl_words = s.get("highlight_words", [])
        cam_motion = s.get("camera_motion", "zoom_in")
        sfx_type = s.get("sfx_type", "sparkle")

        img_raw = os.path.join("scene_images", f"scene_{s_num}.jpg")
        aud_path = os.path.join("audio_clips", f"scene_{s_num}.mp3")
        if not os.path.exists(aud_path):
            aud_path = os.path.join("audio_clips", f"scene_{s_num}.wav")

        if not os.path.exists(img_raw):
            generate_scene_visual(s.get("image_prompt", "3D cartoon"), sub_text, s_num)

        img_land = decorate_scene_with_subtitles(img_raw, sub_text, hl_words, idx, total_scenes, is_vertical=False)
        img_vert = decorate_scene_with_subtitles(img_raw, sub_text, hl_words, idx, total_scenes, is_vertical=True)

        voice_clip = None
        duration = 7.0  # Extended duration for rich 5-min feel
        if os.path.exists(aud_path) and os.path.getsize(aud_path) > 300:
            try:
                voice_clip = AudioFileClip(aud_path)
                duration = max(5.0, voice_clip.duration + 0.5)
            except Exception:
                pass

        try:
            sfx_wav = generate_cartoon_sfx_wav(sfx_type, os.path.join("temp_assets", f"sfx_{s_num}.wav"))
            sfx_clip = AudioFileClip(sfx_wav)
            combined_audio = CompositeAudioClip([voice_clip, sfx_clip]) if voice_clip else sfx_clip
        except Exception:
            combined_audio = voice_clip

        # Landscape Clip (For 5-Min Long Video)
        clip_l = ImageClip(img_land).set_duration(duration)
        if cam_motion == "zoom_out":
            clip_l = clip_l.resize(lambda t, d=duration: 1.05 - 0.04 * (t / d))
        elif cam_motion == "pan_right":
            clip_l = clip_l.resize(lambda t, d=duration: 1.02 + 0.03 * (t / d))
        else:
            clip_l = clip_l.resize(lambda t, d=duration: 1.0 + 0.045 * (t / d))
        clip_l = clip_l.fx(vfx.fadein, 0.4).fx(vfx.fadeout, 0.4)
        if combined_audio:
            clip_l = clip_l.set_audio(combined_audio)
        landscape_clips.append(clip_l)

        # Vertical Clip (For Individual Shorts)
        clip_v = ImageClip(img_vert).set_duration(duration)
        clip_v = clip_v.fx(vfx.fadein, 0.3).fx(vfx.fadeout, 0.3)
        if combined_audio:
            clip_v = clip_v.set_audio(combined_audio)
        vertical_clips.append(clip_v)

    # 1. Render 5-Minute Master Long Video (Landscape)
    try:
        moral_str = plan.get("moral", "Sharing with friends always doubles the joy!")
        outro_l_img = create_end_screen_card(moral_str, is_vertical=False)
        outro_sfx = generate_cartoon_sfx_wav("fanfare", os.path.join("temp_assets", "outro_fanfare.wav"))
        outro_aud = AudioFileClip(outro_sfx)
        outro_l_clip = ImageClip(outro_l_img).set_duration(4.0).set_audio(outro_aud).fx(vfx.fadein, 0.3)
        landscape_clips.append(outro_l_clip)
    except Exception:
        pass

    final_land = concatenate_videoclips(landscape_clips, method="compose")

    try:
        bg_wav = generate_kids_background_music(final_land.duration + 1.0)
        bg_audio = AudioFileClip(bg_wav).subclip(0, final_land.duration)
        if final_land.audio:
            mixed_audio = CompositeAudioClip([final_land.audio, bg_audio])
            final_land = final_land.set_audio(mixed_audio)
    except Exception:
        pass

    print(f"  📽️ Rendering 5-Minute Master Long Video -> {FINAL_LONG_VIDEO_PATH}")
    final_land.write_videofile(FINAL_LONG_VIDEO_PATH, fps=24, codec="libx264", audio_codec="aac", threads=2, preset="ultrafast", logger=None)
    final_land.close()

    # 2. Render 5 to 10 Independent Viral YouTube Shorts (Vertical 9:16)
    print(f"  📱 Generating Independent YouTube Shorts into '{SHORTS_OUTPUT_DIR}'...")
    for s_idx, v_clip in enumerate(vertical_clips, start=1):
        short_path = os.path.join(SHORTS_OUTPUT_DIR, f"apex_viral_short_{s_idx}.mp4")
        try:
            v_clip.write_videofile(short_path, fps=24, codec="libx264", audio_codec="aac", threads=2, preset="ultrafast", logger=None)
            print(f"    -> Short #{s_idx} Saved Successfully: {short_path}")
        except Exception as se:
            print(f"    [Short Notice] Error rendering short {s_idx}: {se}")
        v_clip.close()

    print("  ✅ Apex Studio: Both Long Video and All Shorts Rendered Successfully!")

# =====================================================================
# 8. MAIN EXECUTION PIPELINE
# =====================================================================
if __name__ == "__main__":
    print("====================================================")
    print("   TOONTALES HUB - V19 HYPER-CINEMATIC APEX STUDIO  ")
    print("====================================================")

    try:
        plan = generate_studio_video_plan()
        scenes = plan.get("scenes", [])
        chosen_voice = random.choice(US_KIDS_VOICES)
        print(f"\n✅ STEP 1: Master Script & Story Plan Generated!")
        print(f"📌 Video Title : {plan.get('title')}")
        print(f"💡 Story Moral : {plan.get('moral', 'Always be kind!')}")
        print(f"🎙️ Narrator    : {chosen_voice}")

        print("\n🚀 STEP 2: Generating HD Audio & 3D Visual Assets...")
        for idx, s in enumerate(scenes, start=1):
            s_num = s.get("scene_number", idx)
            vo_en = s.get("voiceover_english", "Welcome to ToonTales Hub!")
            sub = s.get("subtitle_text", vo_en)
            img_p = s.get("image_prompt", plan.get("character_style_seed", "Cute 3D panda"))

            generate_scene_audio(vo_en, s_num, chosen_voice=chosen_voice)
            generate_scene_visual(img_p, sub, s_num, is_thumbnail=False)

        thumb_prompt = plan.get("thumbnail_prompt", plan.get("title", "Cute 3D Cartoon"))
        badge_txt = plan.get("thumbnail_badge", "MAGIC SECRET!")
        generate_scene_visual(thumb_prompt, plan.get("title", "ToonTales Hub"), 0, is_thumbnail=True, badge_text=badge_txt)

        render_master_videos_and_shorts(plan)

        print("\n====================================================")
        print("🎉 100% COMPLETE! 5-MIN LONG VIDEO & MULTI-SHORTS READY!")
        print(f"🎬 5-Min Master Video : {FINAL_LONG_VIDEO_PATH}")
        print(f"📱 Viral Shorts Folder: {SHORTS_OUTPUT_DIR}")
        print(f"📄 SEO Report         : {SEO_REPORT_PATH}")
        print("====================================================")
    except Exception as err:
        print(f"\n❌ UNEXPECTED ERROR: {err}")
        exit(1)
