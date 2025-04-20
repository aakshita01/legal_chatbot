import os
import pdfplumber

# Input and output folders
input_folder = "data"
output_folder = "extract_text"

# Make sure output folder exists
os.makedirs(output_folder, exist_ok=True)

# Loop over all PDF files
for filename in os.listdir(input_folder):
    if filename.endswith(".pdf"):
        file_path = os.path.join(input_folder, filename)
        with pdfplumber.open(file_path) as pdf:
            text = ""
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"

        # Save extracted text
        output_path = os.path.join(output_folder, filename.replace(".pdf", ".txt"))
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(text)

print("✅ Text extraction complete!")
