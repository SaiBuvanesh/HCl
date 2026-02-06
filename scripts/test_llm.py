
import sys
import os

# Add parent directory to path to allow importing app
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.core.llm import llm_service

print(f"Provider: {llm_service.provider}")
print(f"Active Model: {llm_service.active_model}")
print(f"Offline: {llm_service.is_offline}")

if not llm_service.is_offline:
    print("Testing Generation...")
    try:
        # Bypass _call_llm's try-except to see full traceback if needed, 
        # but _call_llm returns the string error.
        # Let's just print the result and if it starts with "Gemini Error", print it carefully.
        response = llm_service._call_llm("Say 'Hello!'")
        print(f"FULL RESPONSE: {response}", flush=True)
    except Exception as e:
        print(f"CRITICAL FAIL: {e}", flush=True)
    print("DONE", flush=True)
else:
    print("Service is offline.", flush=True)
