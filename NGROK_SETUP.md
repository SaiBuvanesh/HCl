# How to Connect Local Ollama to Streamlit Cloud

This guide explains how to keep your local Ollama accessible from the Streamlit Cloud app.

## Prerequisites

- Ollama must be running locally
- Ngrok must be installed and configured
- Streamlit Cloud secrets must be configured

## Quick Start

### 1. Start Ollama (if not already running)

```bash
ollama serve
```

Keep this terminal open.

### 2. Start Ngrok Tunnel

**Option A: Use the batch script**
```bash
.\scripts\start_ngrok.bat
```

**Option B: Run manually**
```bash
d:\HCL\ngrok\ngrok.exe http 11434
```

Keep this terminal open. You'll see output like:
```
Forwarding  https://varous-wimpishly-amiyah.ngrok-free.dev -> http://localhost:11434
```

### 3. Update Streamlit Cloud (if URL changed)

If you restarted ngrok and got a new URL:

1. Go to https://share.streamlit.io/
2. Click your app → Settings → Secrets
3. Update `OLLAMA_BASE_URL` with the new ngrok URL
4. Save

## Important Notes

⚠️ **Keep terminals running** - Both Ollama and ngrok must stay running
⚠️ **Computer must be on** - Your local machine must be powered on and connected
⚠️ **URL changes** - Free ngrok URLs change when you restart ngrok

## Troubleshooting

**Problem: "Local LLM Not Available" on cloud**
- Check if ngrok terminal is still running
- Verify the ngrok URL matches what's in Streamlit Cloud secrets
- Restart ngrok if needed and update the URL in secrets

**Problem: Ngrok tunnel disconnected**
- Restart ngrok using the batch script
- Copy the new URL
- Update Streamlit Cloud secrets

## Running Everything

To run the complete local + cloud setup:

1. **Terminal 1:** `ollama serve`
2. **Terminal 2:** `.\scripts\start_ngrok.bat`
3. **Terminal 3 (optional):** `.\scripts\run_app.bat` (for local testing)

Your cloud app at https://legalsensehclguvi.streamlit.app/ will now have access to your local Ollama!
