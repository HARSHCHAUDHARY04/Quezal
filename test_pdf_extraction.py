# test_pdf_extraction.py
import PyPDF2
import os

def extract_text_from_pdf(pdf_path):
    """Extract text from PDF file"""
    try:
        with open(pdf_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            text = ""
            
            # Extract text from all pages
            for page_num in range(len(pdf_reader.pages)):
                page = pdf_reader.pages[page_num]
                text += page.extract_text() + "\n"
            
            return text.strip()
    
    except Exception as e:
        print(f"❌ Error reading PDF: {e}")
        return None

# Test with your specific PDF file
def test_with_real_pdf():
    pdf_filename = "Questions_on_Conflict_Serailizability[1].pdf"  # Fixed spelling - matches your actual file
    
    if os.path.exists(pdf_filename):
        print(f"📄 Testing with: {pdf_filename}")
        extracted_text = extract_text_from_pdf(pdf_filename)
        
        if extracted_text:
            print("✅ PDF text extraction successful!")
            print(f"📝 Extracted {len(extracted_text)} characters")
            print("📖 First 300 characters:")
            print(extracted_text[:300] + "...")
            return extracted_text
        else:
            print("❌ Failed to extract text")
            return None
    else:
        print(f"❌ PDF file '{pdf_filename}' not found")
        print("📝 Please make sure the PDF is in the same folder")
        print("📁 Current files in directory:")
        for file in os.listdir("."):
            if file.endswith(".pdf"):
                print(f"   - {file}")
        return None

if __name__ == "__main__":
    test_with_real_pdf()
