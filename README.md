AI Book Analyzer Pro


A powerful AI-powered web application that automatically analyzes books and documents to generate comprehensive summaries, important questions, FAQs, and enables interactive Q&A about the content.

 Features
 AI-Powered Analysis
Smart Summarization: Generate detailed, multi-section summaries from book content

Question Generation: Automatically create important discussion questions

FAQ Creation: Generate frequently asked questions with comprehensive answers

Interactive Q&A: Chat with AI about specific book content

 Advanced Processing
PDF Document Support: Process any PDF book or document

Smart Text Chunking: Advanced text segmentation for optimal analysis

Multi-format Export: Download reports in TXT, JSON, and HTML formats

Real-time Progress Tracking: Visual feedback during processing

 User Experience
Beautiful UI: Custom CSS with gradient designs and modern cards

Responsive Design: Works perfectly on desktop and mobile

Session Management: Persistent chat history and analysis data

Three-Tab Interface: Organized workflow (Analysis, Chat, Export)

 Quick Start
Prerequisites
Python 3.8 or higher

pip (Python package manager)

Installation
Clone the repository

bash
git clone https://github.com/yourusername/ai-book-analyzer.git
cd ai-book-analyzer
Create virtual environment (Recommended)

bash
python -m venv venv
# On Windows:
venv\Scripts\activate
# On Mac/Linux:
source venv/bin/activate
Install dependencies

bash
pip install -r requirements.txt
Run the application

bash
streamlit run book_analyzer.py
Open your browser

The app will automatically open at http://localhost:8501

If not, manually navigate to the URL shown in terminal

 Requirements
Create a requirements.txt file with:

txt
streamlit>=1.28.0
PyPDF2>=3.0.0
langchain>=0.0.300
transformers>=4.30.0
torch>=2.0.0
sentencepiece>=0.1.99
accelerate>=0.20.0
 How to Use
1. Upload Your Book
Click "Drag and drop your PDF file here"

Supported: PDF documents up to 200MB

The system will automatically process and chunk the text

2. Generate Analysis (Analysis Dashboard Tab)
Smart Summary: Get comprehensive book overview

Important Questions: Generate discussion questions

FAQs: Create frequently asked questions

3. Chat with AI (AI Assistant Tab)
Ask any question about the book content

Get AI-powered answers based on the actual text

Use quick questions for common queries

4. Export Results (Export Center Tab)
Text Report: Comprehensive analysis in TXT format

JSON Data: Structured data for developers

HTML Report: Beautiful web-ready report

Chat History: Export your Q&A conversations

 Technical Architecture
text
AI Book Analyzer Pro
├── Frontend (Streamlit)
│   ├── Custom CSS Styling
│   ├ Three-Tab Interface
│   └── Real-time Components
├── Processing Engine
│   ├── PDF Text Extraction
│   ├── Smart Text Chunking
│   └── Content Analysis
├── AI Components
│   ├── Summary Generation
│   ├── Question Creation
│   └── FAQ Generation
└── Export System
    ├── Multi-format Support
    ├── Report Generation
    └── Chat History Management
 Customization
Adding New Analysis Types
python
def custom_analysis(chunks):
    # Add your custom analysis logic here
    return analysis_result
Modifying UI Components
The app uses custom CSS for styling. Modify the inject_custom_css() function to change the appearance.

Extending Export Formats
Add new export formats in the create_comprehensive_document() function.

📸 Screenshots
(Add your screenshots here)

Main Interface: Show the upload and analysis dashboard

Chat Feature: Demonstrate the Q&A functionality

Export Options: Display the multiple download formats

Use Cases
 Students & Researchers
Quickly analyze academic papers and textbooks

Generate study questions and summaries

Export analysis for reference

 Professionals
Process business documents and reports

Create executive summaries

Generate discussion points for meetings

 Book Clubs & Readers
Prepare for book discussions

Create reading guides

Share analysis with group members
