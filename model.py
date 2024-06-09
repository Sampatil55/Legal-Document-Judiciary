import streamlit as st
import nltk
import fitz  # PyMuPDF
from nltk.sentiment import SentimentIntensityAnalyzer
from nltk.tokenize import word_tokenize
from nltk import ne_chunk, pos_tag
import matplotlib.pyplot as plt
import re
import pytesseract
from PIL import Image

nltk.download('maxent_ne_chunker')
nltk.download('words')
nltk.download('averaged_perceptron_tagger')

def sentiment_analysis(file_content):
    sia = SentimentIntensityAnalyzer()
    text = file_content.decode("utf-8")
    tokens = word_tokenize(text)
    sentiment = sia.polarity_scores(' '.join(tokens))

    # Convert scores to percentages
    sentiment['neg'] *= 100
    sentiment['neu'] *= 100
    sentiment['pos'] *= 100
    sentiment['compound'] *= 100

    return sentiment

def is_legal_document(sentiment):
    if -10 <= sentiment['compound'] <= 10:
        neu_post = 100 - (sentiment['neg'] + sentiment['pos'])
        return f"<span style='color:red'>Document is highly likely to be illegal. Neutral/Positive: {neu_post:.2f}%</span>"
    elif sentiment['neg'] < 30:
        return "<span style='color:green'>Document is considered legal.</span>"
    else:
        return "<span style='color:orange'>Document might not be legal.</span>"

def highlight_keywords(text, keywords):
    entities = []
    words = word_tokenize(text)
    for chunk in ne_chunk(pos_tag(words)):
        if hasattr(chunk, 'label'):
            entities.append(' '.join(c[0] for c in chunk))
    for keyword in keywords:
        pattern = re.compile(r'\b({0})\b'.format(keyword), flags=re.IGNORECASE)
        text = pattern.sub(r'<mark>\1</mark>', text)
    return text, entities

def main():
    ## Simple navbar using radio buttons
    st.sidebar.title("Navigate")
    nav = st.sidebar.radio("Navigation", ["Home", "Upload Text File", "Upload PDF File", "Upload Image", "About"])

    if nav == "Home":
        st.title("AI-based Legal Document Analysis for Judiciary :mag_right:")
        st.write("Welcome to the AI-based legal document analysis tool for the judiciary. Upload your legal documents for insightful analysis. :page_with_curl:")

    elif nav == "Upload Text File":
        st.title("Upload Text File :page_with_curl:")
        st.write("Upload a text file for analysis:")

        ## File uploader for text file
        uploaded_file = st.file_uploader("Choose a text file", type=["txt"])
        if uploaded_file is not None:
            text = uploaded_file.read().decode("utf-8")
            st.write("File content:")
            highlighted_text, entities = highlight_keywords(text, ["legal", "illegal", "court", "judge", "lawyer"])
            st.write(highlighted_text)
            st.write("Entities:")
            st.write(entities)
            sentiment_result = sentiment_analysis(text.encode("utf-8"))
            st.write("Sentiment Analysis:")
            st.write(sentiment_result)
            legal_status = is_legal_document(sentiment_result)
            st.markdown(legal_status, unsafe_allow_html=True)

            # Data visualization
            st.write("Sentiment Analysis Visualization:")
            fig, ax = plt.subplots()
            ax.bar(sentiment_result.keys(), sentiment_result.values())
            st.pyplot(fig)

    elif nav == "Upload PDF File":
        st.title("Upload PDF File :page_with_curl:")
        st.write("Upload a PDF file for analysis:")

        ## File uploader for PDF file
        uploaded_file = st.file_uploader("Choose a PDF file", type=["pdf"])
        if uploaded_file is not None:
            pdf_bytes = uploaded_file.read()
            pdf_document = fitz.open(stream=pdf_bytes, filetype="pdf")
            text = ""
            for page_num in range(len(pdf_document)):
                page = pdf_document.load_page(page_num)
                text += page.get_text("text")
            st.write("File content:")
            highlighted_text, entities = highlight_keywords(text, ["legal", "illegal", "court", "judge", "lawyer"])
            st.write(highlighted_text)
            st.write("Entities:")
            st.write(entities)
            sentiment_result = sentiment_analysis(text.encode("utf-8"))
            st.write("Sentiment Analysis:")
            st.write(sentiment_result)
            legal_status = is_legal_document(sentiment_result)
            st.markdown(legal_status, unsafe_allow_html=True)

            # Data visualization
            st.write("Sentiment Analysis Visualization:")
            fig, ax = plt.subplots()
            ax.bar(sentiment_result.keys(), sentiment_result.values())
            st.pyplot(fig)

    elif nav == "Upload Image":
        st.title("Upload Image :camera:")
        st.write("Upload an image for text extraction and analysis:")

        ## File uploader for image file
        uploaded_image = st.file_uploader("Choose an image file", type=["jpg", "png", "jpeg"])
        if uploaded_image is not None:
            # Display the uploaded image
            st.image(uploaded_image, caption="Uploaded Image.", use_column_width=True)

            # Perform OCR to extract text from the image
            image = Image.open(uploaded_image)
            extracted_text = pytesseract.image_to_string(image)

            # Display the extracted text
            st.write("Extracted Text:")
            st.write(extracted_text)

            # Analyze the extracted text
            highlighted_text, entities = highlight_keywords(extracted_text, ["legal", "illegal", "court", "judge", "lawyer"])
            st.write("Entities:")
            st.write(entities)
            sentiment_result = sentiment_analysis(extracted_text.encode("utf-8"))
            st.write("Sentiment Analysis:")
            st.write(sentiment_result)
            legal_status = is_legal_document(sentiment_result)
            st.markdown(legal_status, unsafe_allow_html=True)

            # Data visualization
            st.write("Sentiment Analysis Visualization:")
            fig, ax = plt.subplots()
            ax.bar(sentiment_result.keys(), sentiment_result.values())
            st.pyplot(fig)

    elif nav == "About":
        st.title("About :information_source:")
        st.markdown(
            """
            This tool is developed for the judiciary to analyze legal documents using AI. 
            It aims to provide quick and insightful analysis to assist in legal proceedings.
            Developed by: Team
            """
        )

if __name__ == "__main__":
    main()
