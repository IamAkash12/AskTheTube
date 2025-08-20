from get_transcript import get_youtube_transcript
from store_embeddings import store_transcript_as_embeddings
from qa_system import answer_questio
def extract_video_id(url):
    # Simple extraction for common YouTube URLs
    import re
    match = re.search(r"(?:v=|\/)([0-9A-Za-z_-]{11}).*", url)
    return match.group(1) if match else None

def main():
    url = input("Enter YouTube video URL: ")
    video_id = extract_video_id(url)
    if not video_id:
        print("Invalid YouTube URL.")
        return

    print(video_id)
    print("Fetching transcript...")
    transcript = get_youtube_transcript(video_id)
    print("Storing transcript as embeddings...")
    store_transcript_as_embeddings(transcript)

    while True:
        question = input("Ask a question about the video (or type 'exit'): ")
        if question.lower() == 'exit':
            break
        answer = answer_question(question)
        print("Answer:", answer)

if __name__ == "__main__":
    main()

