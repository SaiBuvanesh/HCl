import streamlit as st
import sys
import os

# Add the project root to sys.path so we can import 'app'
# This is required because the script is inside app/ui/
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from pathlib import Path
from app.core.config import APP_NAME

# Page Config MUST be the first Streamlit command
st.set_page_config(
    page_title=APP_NAME,
    page_icon="⚖️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Load CSS
def load_css():
    css_path = Path("app/ui/styles.css")
    if css_path.exists():
        with open(css_path, "r") as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
    else:
        st.warning("Styles not found!")

load_css()

# Sidebar
with st.sidebar:
    st.header("LegalSense AI")
    st.markdown("Your Intelligent Contract Guardian")
    
    st.markdown("---")
    st.markdown("#### Configuration")
    
    enable_ai = st.toggle("Enable AI Insights", value=True)
    
    # Import LLM service to check provider
    from app.core.llm import llm_service
    
    # Display Active LLM Provider
    st.markdown("#### Analysis Engine")
    
    # Always show both options
    provider_options = ["☁️ Cloud LLM (Gemini)", "🖥️ Local LLM (Ollama)"]
    
    # Default selection based on current provider
    default_idx = 0 if getattr(llm_service, 'provider', 'gemini') == "gemini" else 1
    
    selected_provider = st.radio(
        "Select Provider",
        provider_options,
        index=default_idx,
        label_visibility="collapsed"
    )
    
    # Update provider based on selection
    if "Cloud" in selected_provider:
        if getattr(llm_service, 'gemini_available', False):
            llm_service.switch_provider("gemini")
            st.success(f"**Active:** {llm_service.active_model}")
            st.caption("Powered by Google Gemini")
        else:
            st.error("**Cloud LLM Not Configured**")
            st.caption("Add GOOGLE_API_KEY to .env file")
        
    elif "Local" in selected_provider:
        available_models = getattr(llm_service, 'available_models', [])
        if available_models:
            llm_service.switch_provider("ollama")
            
            # Ollama mode with model selection
            model_type = st.radio(
                "Local Model",
                ["Standard (Speed)", "DeepSeek R1 (Reasoning)"],
                captions=["Mistral/Llama", "Chain-of-Thought"],
                index=0,
                label_visibility="collapsed"
            )
            
            if "DeepSeek" in model_type:
                llm_service.set_mode("reasoning")
            else:
                llm_service.set_mode("standard")
            
            st.info(f"**Active:** {llm_service.active_model}")
        else:
            st.error("**Ollama Not Running**")
            st.caption("Start Ollama to use local models")
    
    st.markdown("---")
    st.caption(f"System v1.0 • Secure Environment")

# Main Content
st.title("AI Contract Review System")
st.markdown("""
<div style='padding: 15px 0px; margin-bottom: 20px;'>
    <p style='margin:0; font-size: 1.1rem; color: #475569;'>
        Instantly analyze agreements for legal loopholes, hidden risks, and compliance issues with ease.
    </p>
</div>
""", unsafe_allow_html=True)

# Upload Section
upload_container = st.container()
with upload_container:
    col1, col2 = st.columns([2, 1])
    with col1:
        uploaded_file = st.file_uploader("Upload Your Contract (PDF, DOCX, TXT)", type=["pdf", "docx", "txt"])
    
    with col2:
        if uploaded_file:
            st.info(f"Ready: {uploaded_file.name}")
            # Determine file type
            file_type = uploaded_file.name.split(".")[-1].lower()
            
            if st.button("Analyze Now", type="primary"):
                with st.spinner("Processing document..."):
                    from app.core.pipeline import ContractPipeline
                    
                    # RUN PIPELINE
                    results = ContractPipeline.run(uploaded_file, file_type, enable_ai=enable_ai)
                    
                    if "error" in results:
                        st.error(f"Analysis Error: {results['error']}")
                    else:
                        st.session_state['results'] = results
                        st.success("Processing Complete")

# Dashboard - Display Results if available
if 'results' in st.session_state:
    results = st.session_state['results']
    
    st.markdown("### Analysis Report")
    
    # Summary Metrics
    risk_summary = results["risk_summary"]
    # Metric cards will be styled by CSS
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Clauses", len(results["clauses"]))
    c2.metric("High Priority", risk_summary["High"])
    c3.metric("Medium Priority", risk_summary["Medium"])
    c4.metric("Entities", sum(len(v) for v in results["entities"].values()))
    
    st.markdown("---")
    
    # Tabs
    tab1, tab2, tab3, tab4 = st.tabs(["Key Terms Explained", "Risk Radar", "Smart Summary", "Ask an Expert"])
    
    with tab1:
        st.markdown("#### 📖 Document Walkthrough")
        st.markdown("_A simplified breakdown of the key terms in this agreement._")
        
        # Group clauses for better UX
        # 1. High Risks first
        # 2. Then by type
        
        # Filter out boring definitions unless they are risky
        display_clauses = [c for c in results["clauses"] if c['type'] != 'Definition/Neutral' or c['risk'] != 'Low']
        
        if not display_clauses:
             st.info("No major functional clauses detected. This might be a very simple or non-standard document.")
             display_clauses = results["clauses"] # Fallback

        for clause in display_clauses:
            # CARD STYLE LAYOUT
            # Uses a container with a background color from CSS
            with st.container():
                c1, c2 = st.columns([0.05, 0.95])
                
                # Icon based on type
                icon = "📄"
                if clause['type'] == 'Obligation': icon = "⚡" # Action required
                if clause['type'] == 'Prohibition': icon = "⛔" # Don't do this
                if clause['type'] == 'Right': icon = "✅"   # Good for you
                if clause['risk'] == 'High': icon = "🔴"
                
                with c1:
                    st.markdown(f"### {icon}")
                
                with c2:
                    # Heading: Type + ID
                    st.markdown(f"**{clause['type'].upper()}** • Clause {clause['id']}")
                    
                    # PRIMARY CONTENT: The Explanation (Plain English)
                    if clause.get("explanation"):
                        st.info(f"{clause['explanation']}")
                    else:
                        st.caption("Standard text.")
                    
                    # RISK WARNING (If any)
                    if clause['risk'] != 'Low':
                         st.markdown(f"**:red[Risk Warning:]** {clause['risk_reason']}")
                    
                    # SECONDARY CONTENT: The Raw Text (Hidden by default)
                    with st.expander("Show Original Legalese"):
                        st.code(clause['text'], language=None)
            
            st.divider()
    
    with tab2:
        st.markdown("#### Critical Issues")
        high_risks = [c for c in results["clauses"] if c['risk'] == 'High']
        if high_risks:
            for hr in high_risks:
                with st.container():
                     st.error(f"**Clause {hr['id']}**: {hr['risk_reason']}")
                     st.caption(f"_{hr['text'][:300]}..._")
                     if hr.get("remedy"):
                          with st.expander("Mitigation Strategy", expanded=True):
                               st.markdown(hr["remedy"])
        else:
            st.success("No critical high-risk clauses identified.")
            
        st.markdown("---")
        st.markdown("#### Cautionary Items")
        medium_risks = [c for c in results["clauses"] if c['risk'] == 'Medium']
        if medium_risks:
            for mr in medium_risks:
                st.warning(f"**Clause {mr['id']}**: {mr['risk_reason']}")
                st.caption(f"_{mr['text'][:300]}..._")
                if mr.get("remedy"):
                    with st.expander("Recommendation"):
                        st.markdown(mr["remedy"])
        else:
            st.info("No medium-risk clauses identified.")
            
    with tab3:
        st.markdown("#### 📝 One-Page Summary")
        if results.get("comprehensive_summary"):
             st.info(results["comprehensive_summary"])
        else:
             st.caption("Detailed summary unavailable.")
             
        st.divider()
        
        st.markdown("#### Strategic Risk Overview")
        if results.get("ai_summary"):
            st.markdown(results["ai_summary"])
        else:
            st.info("No summary available.")
            
        st.markdown("---")
        st.markdown("#### Key Entities")
        
        entities = results["entities"]
        if any(entities.values()):
             # Convert to simple text format for professional look
             for type_, items in entities.items():
                if items:
                    st.text(f"{type_}: {', '.join(items)}")
        else:
            st.caption("No entities detected.")
            
    with tab4:
        st.markdown("#### 💬 Ask the Legal Expert")
        st.caption("Ask questions about this specific contract. Answers are based on Indian Corporate Law.")
        
        # Initialize chat history
        if "messages" not in st.session_state:
            st.session_state.messages = []

        # Display chat messages from history on app rerun
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

        # React to user input
        if prompt := st.chat_input("Ex: What is the termination notice period?"):
            # Display user message
            st.chat_message("user").markdown(prompt)
            # Add user message to history
            st.session_state.messages.append({"role": "user", "content": prompt})
            
            # Generate response
            with st.chat_message("assistant"):
                from app.core.llm import llm_service
                doc_text = results.get("full_text", "")
                
                with st.spinner("Analyzing contract..."):
                    response = llm_service.chat_with_document(prompt, doc_text)
                
                st.markdown(response)
                
            # Add assistant response to history
            st.session_state.messages.append({"role": "assistant", "content": response})

