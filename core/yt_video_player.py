import webbrowser
from youtubesearchpython import VideosSearch

def play_on_youtube(query):
    try:
        search = VideosSearch(query, limit=1)
        result = search.result()
        video_url = result['result'][0]['link']
        print(f"🎥 Now playing: {video_url}")
        webbrowser.open(video_url)
    except Exception as e:
        print(f"❌ Error: {e}")

# ✅ Example voice input
voice_input = "Play Shafire on YouTube"

# Parse intent manually
if "play" in voice_input.lower():
    # Extract song title
    query = voice_input.lower().replace("play", "").strip()
    play_on_youtube(query)
else:
    print("🛑 No play intent detected")
