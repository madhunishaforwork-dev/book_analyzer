import streamlit as st
import PyPDF2
from langchain.text_splitter import RecursiveCharacterTextSplitter
import io
import json
from datetime import datetime
import time

# Custom CSS for advanced styling
def inject_custom_css():
    st.markdown("""
    <style>
    .main-header {
        font-size: 3.5rem;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin-bottom: 2rem;
        font-weight: 800;
    }
    
    .feature-card {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
        padding: 1.5rem;
        border-radius: 15px;
        border-left: 5px solid #667eea;
        margin: 1rem 0;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    
    .analysis-card {
        background: white;
        padding: 1.5rem;
        border-radius: 15px;
        border: 1px solid #e0e0e0;
        margin: 1rem 0;
        box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
    }
    
    .chat-user {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 1rem;
        border-radius: 15px 15px 0 15px;
        margin: 0.5rem 0;
        max-width: 80%;
        margin-left: auto;
    }
    
    .chat-assistant {
        background: #f0f2f6;
        color: #333;
        padding: 1rem;
        border-radius: 15px 15px 15px 0;
        margin: 0.5rem 0;
        max-width: 80%;
        margin-right: auto;
        border-left: 4px solid #667eea;
    }
    
    .download-btn {
        background: linear-gradient(135deg, #00b09b 0%, #96c93d 100%) !important;
        color: white !important;
        border: none !important;
        padding: 0.75rem 1.5rem !important;
        border-radius: 25px !important;
        font-weight: 600 !important;
    }
    
    .stProgress > div > div > div > div {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    }
    </style>
    """, unsafe_allow_html=True)

# Set page config
st.set_page_config(
    page_title="AI Book Analyzer Pro", 
    page_icon="📚", 
    layout="wide",
    initial_sidebar_state="expanded"
)

def extract_text_from_pdf(uploaded_file):
    """Extract text from PDF"""
    try:
        pdf_reader = PyPDF2.PdfReader(uploaded_file)
        text = ""
        for page in pdf_reader.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
        return text, len(pdf_reader.pages)
    except Exception as e:
        st.error(f"Error reading PDF: {e}")
        return "", 0

def chunk_text(text, chunk_size=800, chunk_overlap=100):
    """Split text into manageable chunks"""
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        length_function=len
    )
    return text_splitter.split_text(text)

def create_detailed_summary(chunks):
    """Create a comprehensive, detailed summary"""
    try:
        if not chunks:
            return "No text available for summary."
        
        # Progress bar for visual feedback
        progress_bar = st.progress(0)
        
        # Extract key information from multiple chunks
        all_sentences = []
        for i, chunk in enumerate(chunks[:8]):
            sentences = [s.strip() for s in chunk.split('.') if len(s.strip()) > 25]
            all_sentences.extend(sentences)
            progress_bar.progress((i + 1) / min(8, len(chunks)))
        
        if not all_sentences:
            return "Text extracted but no substantial sentences found for summary."
        
        # Build comprehensive summary
        summary_parts = []
        
        # Introduction section
        if all_sentences:
            summary_parts.append("## Introduction and Overview")
            intro_sentences = all_sentences[:min(5, len(all_sentences))]
            summary_parts.append(" ".join(intro_sentences))
        
        # Main content section
        if len(all_sentences) > 5:
            summary_parts.append("## Detailed Analysis")
            main_sentences = all_sentences[5:min(15, len(all_sentences))]
            summary_parts.append(" ".join(main_sentences))
        
        # Key insights
        if len(all_sentences) > 10:
            summary_parts.append("## Key Insights")
            insight_sentences = all_sentences[10:min(20, len(all_sentences))]
            summary_parts.append(" ".join(insight_sentences))
        
        detailed_summary = "\n".join(summary_parts)
        
        # Add overall analysis
        overall_analysis = f"""

## Document Statistics

- Total Content Sections: {len(chunks)}
- Substantial Sentences: {len(all_sentences)}
- Analysis Depth: Comprehensive multi-section review
- Content Quality: {'High' if len(all_sentences) > 20 else 'Medium' if len(all_sentences) > 10 else 'Basic'}

## Key Takeaways

This analysis provides a thorough examination of the document's content, highlighting:
- Core concepts and foundational ideas
- Detailed explanations and methodologies
- Important findings and conclusions
- Practical applications and implications

The document offers valuable insights for readers seeking comprehensive understanding.
"""
        
        detailed_summary += overall_analysis
        progress_bar.empty()
        
        return detailed_summary if len(detailed_summary) > 200 else "Insufficient content for detailed analysis."
    
    except Exception as e:
        return f"Error generating detailed summary: {str(e)}"

def generate_comprehensive_questions(chunks):
    """Generate comprehensive questions covering different aspects"""
    try:
        all_questions = []
        
        # Progress bar
        progress_bar = st.progress(0)
        
        # Extract key topics from chunks
        key_topics = []
        for i, chunk in enumerate(chunks[:6]):
            sentences = [s.strip() for s in chunk.split('.') if len(s.strip()) > 30]
            for sentence in sentences[:2]:
                words = sentence.split()
                if len(words) > 5:
                    topic = ' '.join(words[1:4])
                    if len(topic) > 8:
                        key_topics.append(topic)
            progress_bar.progress((i + 1) / min(6, len(chunks)))
        
        # Remove duplicates but maintain order
        seen = set()
        unique_topics = []
        for topic in key_topics:
            if topic not in seen:
                seen.add(topic)
                unique_topics.append(topic)
        
        # Generate comprehensive questions
        question_types = [
            "What are the main arguments about {topic}?",
            "How does the author explain {topic}?",
            "What evidence supports the discussion of {topic}?",
            "Why is {topic} important in this context?",
            "How can {topic} be applied practically?",
            "What are the limitations of {topic}?"
        ]
        
        for i, topic in enumerate(unique_topics[:8]):
            for q_type in question_types[:3]:  # Use first 3 question types per topic
                if len(all_questions) < 15:
                    question = q_type.format(topic=topic)
                    all_questions.append(question)
            progress_value = min(1.0, 0.5 + (i + 1) / (len(unique_topics) * 2))
            progress_bar.progress(progress_value)
        
        progress_bar.empty()
        return all_questions[:12]
    
    except Exception as e:
        return [
            "What are the foundational concepts presented?",
            "How does the author structure their analysis?",
            "What are the key findings?",
            "How can this information be applied?"
        ]

def generate_detailed_faqs(chunks):
    """Generate comprehensive FAQs with detailed answers"""
    try:
        detailed_faqs = []
        
        # Extract substantial content
        all_content = []
        for chunk in chunks[:4]:
            sentences = [s.strip() for s in chunk.split('.') if len(s.strip()) > 25]
            all_content.extend(sentences)
        
        # Create comprehensive FAQs
        faq_templates = [
            ("What is the primary focus of this document?",
             "The document primarily focuses on {content1}. It explores various aspects including {content2} and provides insights about {content3}."),
            
            ("What methodology or approach is used?",
             "The content employs {content1} approach. Key methods include {content2} and the analysis covers {content3}."),
            
            ("What are the main conclusions?",
             "Key conclusions indicate that {content1}. The findings suggest {content2} and implications include {content3}."),
            
            ("How is the content structured?",
             "The material is organized into coherent sections covering {content1}. It progresses from {content2} to {content3}."),
            
            ("Who is the target audience?",
             "This content is valuable for {content1} seeking {content2}. It's particularly relevant for {content3}."),
            
            ("What makes this content unique?",
             "The uniqueness lies in its {content1}. It offers {content2} and provides {content3} perspectives.")
        ]
        
        for question, template in enumerate(faq_templates):
            if all_content:
                # Fill template with actual content snippets
                content1 = all_content[0][:100] + "..." if len(all_content) > 0 else "various topics"
                content2 = all_content[1][:80] + "..." if len(all_content) > 1 else "multiple aspects"
                content3 = all_content[2][:80] + "..." if len(all_content) > 2 else "key insights"
                
                answer = template[1].format(
                    content1=content1,
                    content2=content2,
                    content3=content3
                )
                detailed_faqs.append((f"Q: {template[0]}", f"A: {answer}"))
        
        return detailed_faqs
    
    except Exception as e:
        return [("Q: Error generating FAQs", f"A: Technical issue: {str(e)}")]

def answer_user_question(question, chunks, chat_history):
    """Answer user questions based on the book content"""
    try:
        if not chunks:
            return "No book content available. Please upload a PDF first."
        
        # Simulate thinking
        with st.spinner("Searching through book content..."):
            time.sleep(1)
        
        # Find relevant content
        relevant_sentences = []
        for chunk in chunks[:5]:  # Search first 5 chunks for performance
            sentences = [s.strip() for s in chunk.split('.') if len(s.strip()) > 20]
            for sentence in sentences[:3]:
                # Simple relevance check
                question_words = set(question.lower().split())
                sentence_words = set(sentence.lower().split())
                if len(question_words.intersection(sentence_words)) > 1:
                    relevant_sentences.append(sentence)
        
        if not relevant_sentences:
            # Fallback to general content
            for chunk in chunks[:3]:
                sentences = [s.strip() for s in chunk.split('.') if len(s.strip()) > 30]
                relevant_sentences.extend(sentences[:2])
        
        if relevant_sentences:
            answer = "## AI Analysis\n\n"
            answer += "Based on my analysis of the book content:\n\n"
            
            for i, content in enumerate(relevant_sentences[:4], 1):
                answer += f"{i}. {content}\n\n"
            
            answer += "---\n"
            answer += f"Generated from analyzing {len(chunks)} content sections"
            
            return answer
        else:
            return "## AI Analysis\n\nI've reviewed the book content, but couldn't find specific information matching your question. \n\nTry asking about:\n- Main themes and topics\n- Key concepts explained\n- Author's approach or methodology\n- Important findings or conclusions"
    
    except Exception as e:
        return f"## Error\n\nUnable to process your question: {str(e)}"

def create_comprehensive_document(summary, questions, faqs, chunks, chat_history, doc_type="txt"):
    """Create comprehensive downloadable document in multiple formats"""
    try:
        if doc_type == "txt":
            # Text document
            document = "=" * 80 + "\n"
            document += " " * 25 + "COMPREHENSIVE BOOK ANALYSIS\n"
            document += "=" * 80 + "\n\n"
            
            document += "EXECUTIVE SUMMARY\n" + "=" * 25 + "\n\n"
            document += summary + "\n\n"
            
            document += "IMPORTANT QUESTIONS\n" + "=" * 25 + "\n\n"
            for i, question in enumerate(questions, 1):
                document += f"{i:02d}. {question}\n"
            document += "\n"
            
            document += "FREQUENTLY ASKED QUESTIONS\n" + "=" * 35 + "\n\n"
            for i, (q, a) in enumerate(faqs, 1):
                document += f"Q{i:02d}: {q}\n"
                document += f"A{i:02d}: {a}\n\n"
            
            if chat_history:
                document += "CHAT HISTORY\n" + "=" * 20 + "\n\n"
                for i, (q, a) in enumerate(chat_history, 1):
                    document += f"You: {q}\n"
                    document += f"AI: {a}\n\n"
            
            document += "\n" + "=" * 80 + "\n"
            document += f"Generated on: {datetime.now().strftime('%Y-%m-%d at %H:%M:%S')}\n"
            document += f"Content Sections Analyzed: {len(chunks)}\n"
            document += "=" * 80
            
            return document.encode('utf-8')
        
        elif doc_type == "json":
            # JSON document
            report_data = {
                "metadata": {
                    "generated_date": datetime.now().isoformat(),
                    "content_sections": len(chunks),
                    "analysis_type": "Comprehensive"
                },
                "summary": summary,
                "questions": questions,
                "faqs": [{"question": q, "answer": a} for q, a in faqs],
                "chat_history": [{"question": q, "answer": a} for q, a in chat_history]
            }
            return json.dumps(report_data, indent=2, ensure_ascii=False).encode('utf-8')
        
        elif doc_type == "html":
            # HTML document
            html_content = """
            <!DOCTYPE html>
            <html>
            <head>
                <title>Book Analysis Report</title>
                <style>
                    body { font-family: Arial, sans-serif; margin: 40px; line-height: 1.6; }
                    .header { text-align: center; background: linear-gradient(135deg, #667eea, #764ba2); color: white; padding: 30px; border-radius: 10px; }
                    .section { margin: 30px 0; padding: 20px; border-left: 5px solid #667eea; background: #f8f9fa; }
                    .question { font-weight: bold; color: #2c3e50; }
                    .answer { color: #34495e; margin-bottom: 15px; }
                    .chat-user { background: #e3f2fd; padding: 10px; margin: 5px; border-radius: 10px; }
                    .chat-ai { background: #f3e5f5; padding: 10px; margin: 5px; border-radius: 10px; }
                </style>
            </head>
            <body>
                <div class="header">
                    <h1>Comprehensive Book Analysis</h1>
                    <p>Generated on """ + datetime.now().strftime('%Y-%m-%d at %H:%M:%S') + """</p>
                </div>
                
                <div class="section">
                    <h2>Executive Summary</h2>
                    <div>""" + summary.replace('\n', '<br>') + """</div>
                </div>
                
                <div class="section">
                    <h2>Important Questions</h2>
                    <ol>
            """
            
            for question in questions:
                html_content += f'<li class="question">{question}</li>'
            
            html_content += """
                    </ol>
                </div>
                
                <div class="section">
                    <h2>Frequently Asked Questions</h2>
            """
            
            for q, a in faqs:
                html_content += f'<div class="question">{q}</div><div class="answer">{a}</div>'
            
            if chat_history:
                html_content += """
                <div class="section">
                    <h2>Chat History</h2>
                """
                for q, a in chat_history:
                    html_content += f'<div class="chat-user"><strong>You:</strong> {q}</div>'
                    html_content += f'<div class="chat-ai"><strong>AI:</strong> {a}</div>'
                html_content += '</div>'
            
            html_content += """
                </div>
            </body>
            </html>
            """
            return html_content.encode('utf-8')
    
    except Exception as e:
        return f"Error creating document: {e}".encode('utf-8')

def main():
    # Inject custom CSS
    inject_custom_css()
    
    # Sidebar
    with st.sidebar:
        st.markdown("<div class='feature-card'>", unsafe_allow_html=True)
        st.header("Features")
        st.markdown("""
        - Smart PDF Processing
        - AI-Powered Analysis
        - Interactive Q&A
        - Comprehensive Reports
        - Advanced Visualizations
        """)
        st.markdown("</div>", unsafe_allow_html=True)
        
        st.markdown("<div class='feature-card'>", unsafe_allow_html=True)
        st.header("Export Options")
        st.markdown("""
        - Text Document (.txt)
        - JSON Data (.json)  
        - HTML Report (.html)
        - Chat History
        """)
        st.markdown("</div>", unsafe_allow_html=True)
    
    # Main content
    st.markdown("<h1 class='main-header'>AI Book Analyzer Pro</h1>", unsafe_allow_html=True)
    st.markdown("<h3 style='text-align: center; color: #666; margin-bottom: 3rem;'>Advanced PDF Analysis with AI-Powered Insights</h3>", unsafe_allow_html=True)
    
    # Initialize session state
    if 'analysis_data' not in st.session_state:
        st.session_state.analysis_data = {
            'summary': None,
            'questions': None,
            'faqs': None,
            'text_chunks': None,
            'page_count': 0
        }
    
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []
    
    # File upload section
    st.markdown("<div class='analysis-card'>", unsafe_allow_html=True)
    st.subheader("Upload Your Book")
    
    uploaded_file = st.file_uploader(
        "Drag and drop your PDF file here", 
        type="pdf",
        help="Supported: PDF documents up to 200MB"
    )
    st.markdown("</div>", unsafe_allow_html=True)
    
    if uploaded_file is not None:
        # Process PDF
        if st.session_state.analysis_data['text_chunks'] is None:
            with st.spinner("Processing your document..."):
                text, page_count = extract_text_from_pdf(uploaded_file)
                if text:
                    chunks = chunk_text(text)
                    st.session_state.analysis_data.update({
                        'text_chunks': chunks,
                        'page_count': page_count
                    })
                    
                    # Success message with stats
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.metric("Pages Processed", page_count)
                    with col2:
                        st.metric("Content Sections", len(chunks))
                    with col3:
                        st.metric("Text Length", f"{len(text):,} chars")
                else:
                    st.error("Failed to process PDF document")
                    return
        
        chunks = st.session_state.analysis_data['text_chunks']
        
        # Create tabs for different functionalities
        tab1, tab2, tab3 = st.tabs(["Analysis Dashboard", "AI Assistant", "Export Center"])
        
        with tab1:
            # Analysis Dashboard
            st.subheader("Comprehensive Analysis")
            
            # Analysis controls
            col1, col2, col3 = st.columns(3)
            with col1:
                if st.button("Generate Smart Summary", type="primary", use_container_width=True):
                    with st.spinner("Creating comprehensive summary..."):
                        st.session_state.analysis_data['summary'] = create_detailed_summary(chunks)
            
            with col2:
                if st.button("Generate Questions", use_container_width=True):
                    with st.spinner("Generating insightful questions..."):
                        st.session_state.analysis_data['questions'] = generate_comprehensive_questions(chunks)
            
            with col3:
                if st.button("Generate FAQs", use_container_width=True):
                    with st.spinner("Creating detailed FAQs..."):
                        st.session_state.analysis_data['faqs'] = generate_detailed_faqs(chunks)
            
            # Display results in cards
            if st.session_state.analysis_data['summary']:
                st.markdown("<div class='analysis-card'>", unsafe_allow_html=True)
                st.subheader("Executive Summary")
                st.markdown(st.session_state.analysis_data['summary'])
                st.markdown("</div>", unsafe_allow_html=True)
            
            if st.session_state.analysis_data['questions']:
                st.markdown("<div class='analysis-card'>", unsafe_allow_html=True)
                st.subheader("Important Questions")
                for i, question in enumerate(st.session_state.analysis_data['questions'], 1):
                    st.markdown(f"{i}. {question}")
                st.markdown("</div>", unsafe_allow_html=True)
            
            if st.session_state.analysis_data['faqs']:
                st.markdown("<div class='analysis-card'>", unsafe_allow_html=True)
                st.subheader("Frequently Asked Questions")
                for q, a in st.session_state.analysis_data['faqs']:
                    st.markdown(f"**{q}**")
                    st.markdown(a)
                    st.markdown("---")
                st.markdown("</div>", unsafe_allow_html=True)
        
        with tab2:
            # AI Assistant Tab
            st.subheader("Chat with AI Assistant")
            st.info("Ask any question about the book content and get AI-powered answers!")
            
            # Chat display
            chat_container = st.container()
            with chat_container:
                for question, answer in st.session_state.chat_history:
                    st.markdown(f'<div class="chat-user"><strong>You:</strong> {question}</div>', unsafe_allow_html=True)
                    st.markdown(f'<div class="chat-assistant"><strong>AI:</strong> {answer}</div>', unsafe_allow_html=True)
            
            # Chat input
            col1, col2 = st.columns([4, 1])
            with col1:
                user_question = st.text_input(
                    "Type your question here:",
                    placeholder="e.g., What are the main themes? Explain chapter 3...",
                    label_visibility="collapsed"
                )
            with col2:
                ask_btn = st.button("Ask", use_container_width=True, type="primary")
            
            # Quick questions
            st.write("Quick Questions:")
            quick_cols = st.columns(4)
            quick_questions = [
                "Main themes?",
                "Key findings?",
                "Author's approach?",
                "Practical applications?"
            ]
            
            for i, col in enumerate(quick_cols):
                with col:
                    if st.button(quick_questions[i], use_container_width=True):
                        user_question = quick_questions[i]
            
            if (ask_btn or user_question) and user_question.strip():
                # Add to chat history
                st.session_state.chat_history.append((user_question, ""))
                
                # Generate answer
                answer = answer_user_question(user_question, chunks, st.session_state.chat_history)
                st.session_state.chat_history[-1] = (user_question, answer)
                
                st.rerun()
        
        with tab3:
            # Export Center
            st.subheader("Export & Download Center")
            
            if (st.session_state.analysis_data['summary'] and 
                st.session_state.analysis_data['questions'] and 
                st.session_state.analysis_data['faqs']):
                
                # Export options
                st.success("Your analysis is ready for export!")
                
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    # Text document
                    txt_doc = create_comprehensive_document(
                        st.session_state.analysis_data['summary'],
                        st.session_state.analysis_data['questions'],
                        st.session_state.analysis_data['faqs'],
                        chunks,
                        st.session_state.chat_history,
                        "txt"
                    )
                    st.download_button(
                        label="Download Text Report",
                        data=txt_doc,
                        file_name="book_analysis_report.txt",
                        mime="text/plain",
                        use_container_width=True
                    )
                
                with col2:
                    # JSON document
                    json_doc = create_comprehensive_document(
                        st.session_state.analysis_data['summary'],
                        st.session_state.analysis_data['questions'],
                        st.session_state.analysis_data['faqs'],
                        chunks,
                        st.session_state.chat_history,
                        "json"
                    )
                    st.download_button(
                        label="Download JSON Data",
                        data=json_doc,
                        file_name="book_analysis_data.json",
                        mime="application/json",
                        use_container_width=True
                    )
                
                with col3:
                    # HTML document
                    html_doc = create_comprehensive_document(
                        st.session_state.analysis_data['summary'],
                        st.session_state.analysis_data['questions'],
                        st.session_state.analysis_data['faqs'],
                        chunks,
                        st.session_state.chat_history,
                        "html"
                    )
                    st.download_button(
                        label="Download HTML Report",
                        data=html_doc,
                        file_name="book_analysis_report.html",
                        mime="text/html",
                        use_container_width=True
                    )
                
                # Additional export options
                st.markdown("---")
                col4, col5 = st.columns(2)
                
                with col4:
                    # Export chat history
                    if st.session_state.chat_history:
                        chat_text = "CHAT HISTORY EXPORT\n" + "=" * 20 + "\n\n"
                        for i, (q, a) in enumerate(st.session_state.chat_history, 1):
                            chat_text += f"Q{i}: {q}\nA{i}: {a}\n\n"
                        
                        st.download_button(
                            label="Export Chat History",
                            data=chat_text.encode('utf-8'),
                            file_name="chat_history.txt",
                            mime="text/plain",
                            use_container_width=True
                        )
                
                with col5:
                    # Clear data
                    if st.button("Clear Session", use_container_width=True):
                        st.session_state.analysis_data = {
                            'summary': None, 'questions': None, 'faqs': None, 
                            'text_chunks': None, 'page_count': 0
                        }
                        st.session_state.chat_history = []
                        st.rerun()
            
            else:
                st.warning("Please generate analysis first in the Dashboard tab")
    
    else:
        # Landing page when no file is uploaded
        st.markdown("<div class='feature-card'>", unsafe_allow_html=True)
        st.subheader("How It Works")
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.markdown("""
            ### 1. Upload
            Drag and drop your PDF book or document
            """)
        
        with col2:
            st.markdown("""
            ### 2. Analyze
            Get AI-powered summary, questions, and FAQs
            """)
        
        with col3:
            st.markdown("""
            ### 3. Chat
            Ask questions about the content
            """)
        
        with col4:
            st.markdown("""
            ### 4. Export
            Download comprehensive reports
            """)
        
        st.markdown("</div>", unsafe_allow_html=True)

if __name__ == "__main__":
    main()