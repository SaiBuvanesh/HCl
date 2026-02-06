# Deployment Walkthrough

## 1. GitHub (Completed)
The code is on GitHub: [https://github.com/SaiBuvanesh/HCl](https://github.com/SaiBuvanesh/HCl)

## 2. Running Locally (Recommended)
**Since you want to use the Local LLM (Ollama), you MUST run the app locally.**
The Cloud version cannot see your local Ollama.

### How to Run:
```powershell
.\scripts\run_app.bat
```
This enables all features: Risk Analysis, Chat, and Explanations.

---

## 3. Streamlit Cloud (UI Demo Only)
You can deploy the UI to the cloud, but **AI features will be offline** unless your host has Ollama installed (which standard Streamlit Cloud does not).

**URL:** [https://legalsensehclguvi.streamlit.app/](https://legalsensehclguvi.streamlit.app/)
*(Expect "AI Offline" errors here)*
