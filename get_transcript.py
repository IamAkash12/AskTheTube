from youtube_transcript_api import YouTubeTranscriptApi

def get_youtube_transcript(video_id):
    print(video_id)
    ytt_api = YouTubeTranscriptApi()
    transcript = ytt_api.fetch(video_id)
    # Combine all text segments into a single string
    print(transcript)
    full_text = " ".join([segment.text for segment in transcript])
    print(full_text)
    return full_text

