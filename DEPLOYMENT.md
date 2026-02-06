# Deployment Walkthrough

## 1. GitHub (Completed)
The code is on GitHub: [https://github.com/SaiBuvanesh/HCl](https://github.com/SaiBuvanesh/HCl)

## 2. Streamlit Cloud Deployment

### Why Streamlit Cloud?
- **Free** for public repositories.
- **Native Support** for Streamlit apps.
- **Auto-Updates** on git push.

### Steps:
1.  Go to [share.streamlit.io](https://share.streamlit.io/) and sign in with GitHub.
2.  Click **"New app"**.
3.  Select your repository: `SaiBuvanesh/HCl`.
4.  **Branch**: `main`.
5.  **Main file path**: `app/ui/main.py`.
6.  Click **Deploy**.

> **System Dependencies**: A `packages.txt` file is included to install `poppler-utils` and other required libraries automatically.
