import streamlit as st
import PyPDF2
import re

# PDF Text Extraction Function
def load_pdf(uploaded_file):
    text = ""
    pdf_reader = PyPDF2.PdfReader(uploaded_file)
    for page in pdf_reader.pages:
        text += page.extract_text()
    return text

# Keyword Search Function
def search_keyword(text, keyword):
    matches = re.findall(r'(.{0,50}' + re.escape(keyword) + r'.{0,50})', text, re.IGNORECASE)
    return matches

# Industry Categories & NIC Code Mapping
categories = {
    'Mining or Quarrying': ['quarry', 'mining', 'excavation'],
    'Manufacturing': ['manufacture', 'production', 'assembly'],
    'Construction': ['building', 'construction', 'carcass', 'roof']
}

industry_classification = {
    'Mining or Quarrying': {
        'code': '081',
        'description': 'Quarrying of stone, sand and clay'
    },
    'Manufacturing': {
        'code': '2220',
        'description': 'Manufacture of artificial stone (e.g., cultured marble)'
    },
    'Construction': {
        'code': '2396',
        'description': 'Cutting, shaping and finishing of stone'
    }
}

# Function to classify matches into categories and add NIC code
def classify_matches_with_codes(matches, categories):
    categorized_matches = {category: [] for category in categories}
    for match in matches:
        for category, keywords in categories.items():
            if any(keyword.lower() in match.lower() for keyword in keywords):
                industry_info = industry_classification.get(category, None)
                if industry_info:
                    categorized_matches[category].append({
                        'match': match,
                        'code': industry_info['code'],
                        'description': industry_info['description']
                    })
    return categorized_matches

# Streamlit UI
st.title("Industry Classification Search")

# Upload PDF
pdf_file = st.file_uploader("Upload PDF", type="pdf")

if pdf_file is not None:
    # Extract text from the PDF
    document_text = load_pdf(pdf_file)

    # User Input for Keyword Search
    keyword = st.text_input("Enter a keyword to search")

    if keyword:
        # Search for keyword and classify matches
        matches = search_keyword(document_text, keyword)
        categorized_results = classify_matches_with_codes(matches, categories)

        st.write(f"Found {len(matches)} matches for '{keyword}'.")

        # Display Results by Category
        for category, cat_matches in categorized_results.items():
            if cat_matches:
                st.subheader(f"Category: {category}")
                for match in cat_matches:
                    st.write(f"Match: {match['match']}")
                    st.write(f"NIC Code: {match['code']}")
                    st.write(f"Description: {match['description']}")
                    st.markdown("---")
