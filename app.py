import streamlit as st
import os
import re
from dotenv import load_dotenv
from get_transcript import get_youtube_transcript
from store_embeddings import store_transcript_as_embeddings
from qa_system import answer_question

# Load environment variables
load_dotenv()

# Page configuration
st.set_page_config(
    page_title="YouTube Transcript Q&A",
    page_icon="🎥",
    layout="wide"
)

def extract_video_id(url):
    """Extract video ID from YouTube URL"""
    match = re.search(r"(?:v=|\/)([0-9A-Za-z_-]{11}).*", url)
    return match.group(1) if match else None

def initialize_session_state():
    """Initialize session state variables"""
    if 'transcript_processed' not in st.session_state:
        st.session_state.transcript_processed = False
    if 'current_video_id' not in st.session_state:
        st.session_state.current_video_id = None
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []
    if 'transcript_text' not in st.session_state:
        st.session_state.transcript_text = ""

def main():
    initialize_session_state()
    
    # Header
    st.title("🎥 YouTube Transcript Q&A System")
    st.markdown("Ask questions about YouTube videos using AI-powered analysis")
    
    # Sidebar for video processing
    with st.sidebar:
        st.header("📺 Video Processing")
        
        # Check if OpenAI API key exists
        if not os.getenv("OPENAI_API_KEY"):
            st.error("⚠️ OpenAI API key not found! Please add it to your .env file.")
            st.stop()
        else:
            st.success("✅ OpenAI API key loaded")
        
        # YouTube URL input
        youtube_url = st.text_input(
            "Enter YouTube URL:",
            placeholder="https://www.youtube.com/watch?v=..."
        )
        
        if st.button("🔄 Process Video", type="primary"):
            if youtube_url:
                video_id = extract_video_id(youtube_url)
                
                if not video_id:
                    st.error("❌ Invalid YouTube URL. Please check the format.")
                else:
                    # Check if this is a new video
                    if video_id != st.session_state.current_video_id:
                        st.session_state.current_video_id = video_id
                        st.session_state.transcript_processed = False
                        st.session_state.chat_history = []
                    
                    with st.spinner("Processing video transcript..."):
                        try:
                            # Fetch transcript
                            st.info("📥 Fetching transcript...")
                            transcript = get_youtube_transcript(video_id)
                            st.session_state.transcript_text = transcript
                            
                            # Store embeddings
                            st.info("🧠 Creating embeddings...")
                            store_transcript_as_embeddings(transcript, video_id)
                            
                            st.session_state.transcript_processed = True
                            st.success("✅ Video processed successfully!")
                            
                        except Exception as e:
                            st.error(f"❌ Error processing video: {str(e)}")
                            st.error("This might happen if the video doesn't have captions or is private.")
            else:
                st.warning("⚠️ Please enter a YouTube URL")
        
        # Video info display
        if st.session_state.current_video_id:
            st.markdown("---")
            st.subheader("📋 Current Video")
            st.write(f"**Video ID:** {st.session_state.current_video_id}")
            
            # Embed YouTube video
            video_url = f"https://www.youtube.com/watch?v={st.session_state.current_video_id}"
            st.video(video_url)
            
            # Show transcript preview
            if st.session_state.transcript_text:
                with st.expander("📜 View Transcript"):
                    st.text_area(
                        "Full Transcript:",
                        st.session_state.transcript_text,
                        height=200,
                        disabled=True
                    )
    
    # Main content area
    if st.session_state.transcript_processed:
        st.success("🎯 Ready for questions! Ask anything about the video content.")
        
        # Chat interface
        st.subheader("💬 Ask Questions")
        
        # Display chat history
        for i, (question, answer) in enumerate(st.session_state.chat_history):
            st.markdown(f"**🙋 Question {i+1}:** {question}")
            st.markdown(f"**🤖 Answer:** {answer}")
            st.markdown("---")
        
        # Question input
        question = st.text_input(
            "Ask a question about the video:",
            placeholder="What is the main topic discussed in this video?",
            key="question_input"
        )
        
        col1, col2 = st.columns([1, 5])
        with col1:
            ask_button = st.button("❓ Ask", type="primary")
        with col2:
            if st.button("🗑️ Clear Chat"):
                st.session_state.chat_history = []
                st.rerun()
        
        if ask_button and question:
            with st.spinner("🤔 Thinking..."):
                try:
                    answer_result = answer_question(question, st.session_state.current_video_id)
                    # Extract the answer text from the result
                    answer_text = answer_result.get('result', str(answer_result))
                    
                    # Add to chat history
                    st.session_state.chat_history.append((question, answer_text))
                    
                    # Clear the input
                    st.rerun()
                    
                except Exception as e:
                    st.error(f"❌ Error getting answer: {str(e)}")
        
        # Quick question suggestions
        st.subheader("💡 Suggested Questions")
        suggestions = [
            "What is the main topic of this video?",
            "Can you summarize the key points?",
            "What are the most important takeaways?",
            "Are there any specific examples mentioned?",
            "What recommendations are given?"
        ]
        cols = st.columns(len(suggestions))
        def set_question(suggestion):
            st.session_state.question_input = suggestion

        for i, suggestion in enumerate(suggestions):
            with cols[i]:
                st.button(
                suggestion,
                key=f"suggestion_{i}",
                on_click=set_question,
                args=(suggestion,)
            )

        # for i, suggestion in enumerate(suggestions):
        #     with cols[i]:
        #         if st.button(suggestion, key=f"suggestion_{i}"):
        #             st.session_state.question_input = suggestion
        #             st.rerun()
    
    else:
        # Welcome screen
        st.info("👆 Please enter a YouTube URL in the sidebar to get started!")
        
        st.markdown("""
        ### 🚀 How it works:
        1. **Enter a YouTube URL** in the sidebar
        2. **Click "Process Video"** to fetch and analyze the transcript
        3. **Ask questions** about the video content
        4. **Get AI-powered answers** based on the transcript
        
        ### ✨ Features:
        - 🎯 Extract transcripts from any YouTube video with captions
        - 🧠 AI-powered question answering using advanced language models
        - 💾 Persistent storage for faster follow-up questions
        - 🔄 Interactive chat interface
        - 📱 Mobile-friendly design
        
        ### 📋 Supported Video Types:
        - Videos with auto-generated captions
        - Videos with manual captions/subtitles
        - Public videos (not private or unlisted)
        """)

if __name__ == "__main__":
    main()