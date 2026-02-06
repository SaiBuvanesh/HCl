# AI Contract Review System

An intelligent contract analysis system powered by AI that helps identify risks, unfair clauses, and provides comprehensive legal insights.

## 🚀 Live Demo

**Streamlit Cloud:** https://legalsensehclguvi.streamlit.app/

**Demo Video:** https://drive.google.com/file/d/1OKPVjtIbWNjCa5DNSNckiotYJxHud13-/view?usp=sharing

## ✨ Features

- **Risk Analysis**: Automatically identifies and categorizes contract risks
- **Clause Classification**: Classifies contract clauses by type and importance
- **AI-Powered Insights**: Get explanations and recommendations using LLM
- **Dual LLM Support**: 
  - ☁️ Cloud LLM (Google Gemini) - for cloud deployment
  - 🖥️ Local LLM (Ollama) - for local development
- **Document Support**: Upload PDF, DOCX, or TXT files
- **OCR Support**: Extracts text from scanned documents

## 🛠️ Tech Stack

- **Frontend**: Streamlit
- **NLP**: spaCy, NLTK
- **LLM**: Google Gemini API, Ollama
- **Document Processing**: pdfplumber, python-docx, OCR
- **ML**: scikit-learn, sentence-transformers

## 📦 Installation

### Prerequisites
- Python 3.10+
- (Optional) Ollama for local LLM

### Setup

1. Clone the repository:
```bash
git clone https://github.com/SaiBuvanesh/HCl.git
cd HCl
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Configure environment variables:
Create a `.env` file in the root directory:
```env
GOOGLE_API_KEY=your_gemini_api_key_here
```

4. Run the application:
```bash
streamlit run app/ui/main.py
```

Or use the batch script (Windows):
```bash
.\scripts\run_app.bat
```

## 🔧 Configuration

### Cloud LLM (Gemini)
Add your Google Gemini API key to `.env` file or Streamlit Cloud secrets.

### Local LLM (Ollama)
1. Install Ollama: https://ollama.com/download
2. Pull a model:
```bash
ollama pull mistral
```
3. Start Ollama service:
```bash
ollama serve
```

### Connect Local Ollama to Streamlit Cloud (Optional)

To use your local Ollama from the cloud app:

1. **Start ngrok tunnel:**
```bash
.\scripts\start_ngrok.bat
```

2. **Copy the ngrok URL** from the terminal output

3. **Add to Streamlit Cloud secrets:**
```toml
OLLAMA_BASE_URL = "https://your-ngrok-url.ngrok-free.dev"
```

See [NGROK_SETUP.md](NGROK_SETUP.md) for detailed instructions.

**Note:** Your computer must stay on with ngrok running for this to work.

## 📝 Usage

1. **Upload a contract** (PDF, DOCX, or TXT)
2. **Select LLM provider** (Cloud or Local)
3. **Enable AI Insights** for advanced analysis
4. **Review results**:
   - Risk scores and classifications
   - Identified clauses
   - AI-powered explanations
   - Missing clause detection

## 🌐 Deployment

### Streamlit Cloud
1. Push code to GitHub
2. Connect repository to Streamlit Cloud
3. Add `GOOGLE_API_KEY` to secrets
4. Deploy!

### Local Development
Use the provided `run_app.bat` script or run directly with Streamlit.

## 📄 License

This project is open source and available under the MIT License.

## 👤 Author

**Sai Buvanesh**

- GitHub: [@SaiBuvanesh](https://github.com/SaiBuvanesh)
- Project: [HCl](https://github.com/SaiBuvanesh/HCl)
