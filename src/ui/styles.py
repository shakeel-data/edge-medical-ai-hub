# src/ui/styles.py
import streamlit as st

def inject_premium_css():
    """Inject NVIDIA-inspired premium CSS"""
    css = """
    <style>
    /* Import Google Fonts for premium typography */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    /* Root variables - NVIDIA Green + Google Blue palette */
    :root {
        --primary-green: #76B900;
        --google-blue: #4285F4;
        --dark-bg: #0F0F0F;
        --surface: #1A1A1A;
        --text-primary: #E8EAED;
        --text-secondary: #9AA0A6;
        --accent-orange: #FF6B35;
        --success: #34A853;
        --warning: #FBBC05;
        --error: #EA4335;
    }
    
    /* Main app styling */
    .stApp {
        background: linear-gradient(135deg, #0F0F0F 0%, #1A1A1A 100%);
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
        color: var(--text-primary);
    }
    
    /* Premium header with gradient */
    .main-header {
        background: linear-gradient(90deg, var(--primary-green), var(--google-blue));
        padding: 2rem;
        border-radius: 12px;
        margin-bottom: 2rem;
        box-shadow: 0 8px 32px rgba(118, 185, 0, 0.2);
    }
    
    /* Glass morphism cards */
    .glass-card {
        background: rgba(26, 26, 26, 0.7);
        backdrop-filter: blur(20px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 16px;
        padding: 1.5rem;
        margin: 1rem 0;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
        transition: all 0.3s ease;
    }
    
    .glass-card:hover {
        transform: translateY(-4px);
        box-shadow: 0 12px 48px rgba(118, 185, 0, 0.15);
        border-color: var(--primary-green);
    }
    
    /* Animated progress bars */
    .progress-container {
        background: rgba(255, 255, 255, 0.1);
        border-radius: 8px;
        overflow: hidden;
        height: 8px;
        margin: 0.5rem 0;
    }
    
    .progress-bar {
        height: 100%;
        background: linear-gradient(90deg, var(--primary-green), var(--google-blue));
        border-radius: 8px;
        animation: shimmer 2s infinite;
    }
    
    @keyframes shimmer {
        0% { background-position: -200px 0; }
        100% { background-position: 200px 0; }
    }
    
    /* Custom buttons */
    .stButton > button {
        background: linear-gradient(45deg, var(--primary-green), var(--google-blue));
        color: white;
        border: none;
        border-radius: 8px;
        padding: 0.75rem 1.5rem;
        font-weight: 500;
        transition: all 0.3s ease;
        box-shadow: 0 4px 16px rgba(118, 185, 0, 0.3);
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 24px rgba(118, 185, 0, 0.4);
    }
    
    /* Sidebar styling */
    .css-1d391kg {
        background: rgba(15, 15, 15, 0.95);
        backdrop-filter: blur(20px);
    }
    
    /* Metric cards */
    .metric-card {
        background: var(--surface);
        border-radius: 12px;
        padding: 1rem;
        text-align: center;
        border-left: 4px solid var(--primary-green);
        margin: 0.5rem 0;
    }
    
    /* File uploader */
    .stFileUploader {
        border: 2px dashed var(--primary-green);
        border-radius: 12px;
        background: rgba(118, 185, 0, 0.05);
        transition: all 0.3s ease;
    }
    
    .stFileUploader:hover {
        border-color: var(--google-blue);
        background: rgba(66, 133, 244, 0.05);
    }
    
    /* Loading animations */
    .loading-spinner {
        border: 3px solid rgba(118, 185, 0, 0.1);
        border-radius: 50%;
        border-top: 3px solid var(--primary-green);
        width: 30px;
        height: 30px;
        animation: spin 1s linear infinite;
    }
    
    @keyframes spin {
        0% { transform: rotate(0deg); }
        100% { transform: rotate(360deg); }
    }
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)
