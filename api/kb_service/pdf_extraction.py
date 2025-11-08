import PyPDF2

def extract_pdf_to_txt(pdf_path, txt_path):
    with open(pdf_path, 'rb') as pdf_file:
        reader = PyPDF2.PdfReader(pdf_file)
        text = ""
        for page in reader.pages:
            text += page.extract_text() or ""
    with open(txt_path, 'w', encoding='utf-8') as txt_file:
        txt_file.write(text)
    return text

if __name__ == "__main__":   
   file_path = r"D:\GenAI_PJ\KB_Creation\assets\The Economic Times Bangalore 27 10 2025.pdf"
   file_save_path = r"D:\GenAI_PJ\KB_Creation\assets\The Economic Times Bangalore 27 10 2025.txt"

   extract_pdf_to_txt(file_path, file_save_path)
# print("hi")