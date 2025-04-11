import gradio as gr
import PyPDF2
import google.generativeai as genai

# Configure Google Gemini API key
genai.configure(api_key="Enter Your API KEY")

# Function to extract text from PDF
def extract_text_from_pdf(file_path):
    reader = PyPDF2.PdfReader(file_path)
    text = ""
    for page in reader.pages:
        extracted = page.extract_text()
        if extracted:
            text += extracted + "\n"
    return text.strip()

# Function to analyze financial text with Gemini
def analyze_pdf(file):
    try:
        text = extract_text_from_pdf(file.name)

        if not text:
            return "❌ Could not extract text. Make sure the PDF is not scanned or image-only."

        model = genai.GenerativeModel("models/gemini-1.5-pro-latest")
        prompt = f"""
        Analyze the following Paytm transaction history and generate financial insights:
        {text}
        Format your response with the following:
        - Monthly income and expenses
        - Unnecessary expense breakdown
        - Savings percentage
        - Spending trends
        - Category-wise expenses
        - Actionable advice
        """

        response = model.generate_content(prompt)
        return response.text if response else "⚠️ No response from Gemini AI. Try again."

    except Exception as e:
        return f"⚠️ Error during analysis: {e}"

# Build Gradio UI
app = gr.Interface(
    fn=analyze_pdf,
    inputs=gr.File(label="📄 Upload Paytm Transaction PDF", file_types=[".pdf"]),
    outputs=gr.Textbox(label="📊 Financial Insights", lines=30),
    title="💰 AI-Powered Personal Finance Assistant",
    description="Upload your Paytm transaction PDF. Google Gemini will analyze your spending and provide smart financial advice.",
    theme="soft"
)

# Launch the app
app.launch()
