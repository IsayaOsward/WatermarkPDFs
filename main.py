from PyPDF2 import PdfReader, PdfWriter
import base64

# Convert watermark image to Base64
def image_to_base64(image_path):
    print(f"[INFO] Converting image at '{image_path}' to Base64...")
    try:
        with open(image_path, "rb") as image_file:
            base64_image = base64.b64encode(image_file.read()).decode("utf-8")
            print("[SUCCESS] Image converted to Base64.")
            return base64_image
    except FileNotFoundError:
        print(f"[ERROR] Image file not found: {image_path}")
        raise

# Generate JavaScript for constant-time watermarking
def generate_constant_time_watermark_js(base64_image):
    print("[INFO] Generating JavaScript for watermarking...")
    js = f"""
    var watermarkImage = '{base64_image}';
    var img = app.newImage(watermarkImage, 0, 0, 0.5, 0.5);
    this.addWatermarkFromImage({{
        cDI: img,
        nOpacity: 0.5,    // Transparency level (0.0 to 1.0)
        nScale: 0.5,      // Scale of the watermark (0.0 to 1.0)
        nHorizAlign: app.constants.align.center,  // Center horizontally
        nVertAlign: app.constants.align.center   // Center vertically
    }});
    """
    print("[SUCCESS] JavaScript for watermarking generated.")
    return js

# Embed JavaScript for constant-time watermarking
def embed_javascript(pdf_path, output_path, js_code):
    print(f"[INFO] Embedding JavaScript into the PDF at '{pdf_path}'...")
    try:
        with open(pdf_path, 'rb') as input_file:
            reader = PdfReader(input_file)
            writer = PdfWriter()

            print("[INFO] Copying pages from the input PDF...")
            for page in reader.pages:
                writer.add_page(page)
            print("[SUCCESS] All pages copied to the writer.")

            print("[INFO] Adding JavaScript to the PDF...")
            writer.add_js(js_code)
            print("[SUCCESS] JavaScript embedded into the PDF.")

            print(f"[INFO] Writing the updated PDF to '{output_path}'...")
            with open(output_path, 'wb') as output_file:
                writer.write(output_file)
            print("[SUCCESS] Updated PDF saved.")
    except FileNotFoundError:
        print(f"[ERROR] PDF file not found: {pdf_path}")
        raise

# Main execution
if __name__ == "__main__":
    print("[INFO] Starting the watermarking process...")

    # Paths
    input_pdf = r"C:\Users\ionth\OneDrive\Desktop\testingpdf.pdf"  # Correct input PDF file path
    output_pdf = r"C:\Users\ionth\OneDrive\Desktop\output_with_watermark.pdf"  # Output PDF with JavaScript
    watermark_image = r"C:\Users\ionth\OneDrive\Desktop\WatermarkPDFs\watermark.png"  # Correct watermark image path

    try:
        # Convert watermark image to Base64
        base64_image = image_to_base64(watermark_image)

        # Generate JavaScript for watermarking
        watermark_js = generate_constant_time_watermark_js(base64_image)

        # Embed the JavaScript into the PDF
        embed_javascript(input_pdf, output_pdf, watermark_js)

        print(f"[SUCCESS] Watermarked PDF saved as '{output_pdf}'.")
    except Exception as e:
        print(f"[ERROR] An error occurred: {e}")
