from reportlab.pdfgen import canvas
from PyPDF2 import PdfReader, PdfWriter
import os

directory = r'in-pdf'  # Input directory

picture_path = 'watermark.png'  # Watermark image location

# Create watermark png to PDF
c = canvas.Canvas('temp/watermark.pdf')
c.drawImage(picture_path, 170, 300, 250, 250, mask='auto')
c.save()

# Open watermark PDF
watermark_pdf = PdfReader(open("temp/watermark.pdf", "rb"))
watermark_page = watermark_pdf.pages[0]  # Get the first page of the watermark PDF

# Loop through all PDFs in the directory 'in-pdf'
for filename in os.listdir(directory):
    if filename.endswith(".pdf"):  # Take only PDF files to watermark
        input_file = f"in-pdf/{filename}"  # Place your files to watermark in this directory
        output_file = f"out-pdf/{filename}"  # Watermarked files appear here after being watermarked

        with open(input_file, 'rb') as f:
            pdf_reader = PdfReader(f)
            output = PdfWriter()

            for page_number, page in enumerate(pdf_reader.pages):  # Loop through each page of the PDF file
                page.merge_page(watermark_page)  # Apply watermark to the current page
                output.add_page(page)
                print(f"{page_number + 1} of {len(pdf_reader.pages)} pages processed for file: {filename}")

            with open(output_file, "wb") as merged_file:
                output.write(merged_file)  # Write watermarked file to the directory 'out-pdf'
        print(f"File Watermarked: {filename}")
    else:
        continue
