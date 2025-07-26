import streamlit as st
import sys
import os
from datetime import datetime
from typing import List, Dict
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from src.planner import Planner
from src.executor import Executor
from src.memory import Memory
from src.insight import Insight

# Add current directory to path for imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

class MotivAgentWeb:
    def __init__(self):
        if 'planner' not in st.session_state:
            st.session_state.planner = Planner()
            st.session_state.executor = Executor()
            st.session_state.memory = Memory()
            st.session_state.insight = Insight(st.session_state.memory)

    def run(self):
        st.set_page_config(
            page_title="🤖 MotivAgent",
            page_icon="🤖",
            layout="wide",
            initial_sidebar_state="expanded"
        )

        # Modern Dark Glassmorphism Theme with Enhanced Visual Appeal
        st.markdown("""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap');

        /* Global Dark Theme */
        html, body, [class*="css"] {
            font-family: 'Poppins', sans-serif;
            background: linear-gradient(135deg, #0f0f23 0%, #1a1a2e 50%, #16213e 100%);
            background-attachment: fixed;
            min-height: 100vh;
            color: #e2e8f0;
        }

        /* Animated background particles */
        body::before {
            content: '';
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background-image: 
                radial-gradient(circle at 20% 80%, rgba(120, 119, 198, 0.1) 0%, transparent 50%),
                radial-gradient(circle at 80% 20%, rgba(255, 119, 198, 0.1) 0%, transparent 50%),
                radial-gradient(circle at 40% 40%, rgba(120, 219, 255, 0.1) 0%, transparent 50%);
            pointer-events: none;
            z-index: -1;
        }

        /* Enhanced Header with Gradient Text */
        .main-header {
            background: rgba(15, 15, 35, 0.8);
            backdrop-filter: blur(20px);
            border: 1px solid rgba(255, 255, 255, 0.1);
            padding: 3rem 2rem;
            border-radius: 24px;
            margin-bottom: 2rem;
            text-align: center;
            box-shadow: 
                0 20px 40px rgba(0, 0, 0, 0.3),
                0 0 0 1px rgba(255, 255, 255, 0.05),
                inset 0 1px 0 rgba(255, 255, 255, 0.1);
            position: relative;
            overflow: hidden;
        }

        .main-header::before {
            content: '';
            position: absolute;
            top: 0;
            left: -100%;
            width: 100%;
            height: 100%;
            background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.05), transparent);
            animation: shimmer 3s infinite;
        }

        @keyframes shimmer {
            0% { left: -100%; }
            100% { left: 100%; }
        }

        .main-header h1 {
            margin: 0;
            font-size: 3.5rem;
            font-weight: 700;
            letter-spacing: -2px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 50%, #f093fb 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            text-shadow: 0 0 30px rgba(102, 126, 234, 0.3);
            position: relative;
            z-index: 1;
        }

        .main-header h3 {
            color: #94a3b8;
            margin: 1rem 0;
            font-weight: 400;
            font-size: 1.3rem;
            text-shadow: 0 2px 10px rgba(0, 0, 0, 0.3);
        }

        .main-header p {
            color: #64748b;
            margin: 0;
            font-weight: 300;
            font-style: italic;
            font-size: 1rem;
            opacity: 0.8;
        }

        .metric-container {
            background: rgba(15, 15, 35, 0.6);
            backdrop-filter: blur(15px);
            border: 1px solid rgba(255, 255, 255, 0.1);
            padding: 2rem 1.5rem;
            border-radius: 20px;
            text-align: center;
            margin: 0.5rem 0;
            box-shadow: 
                0 8px 32px rgba(0, 0, 0, 0.3),
                inset 0 1px 0 rgba(255, 255, 255, 0.1);
            transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
            position: relative;
            overflow: hidden;
        }

        .metric-container::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background: linear-gradient(135deg, rgba(102, 126, 234, 0.1) 0%, rgba(118, 75, 162, 0.1) 100%);
            opacity: 0;
            transition: opacity 0.3s ease;
        }

        .metric-container:hover {
            transform: translateY(-8px) scale(1.02);
            box-shadow: 
                0 20px 40px rgba(102, 126, 234, 0.2),
                0 0 0 1px rgba(102, 126, 234, 0.3),
                inset 0 1px 0 rgba(255, 255, 255, 0.2);
        }

        .metric-container:hover::before {
            opacity: 1;
        }

        .metric-container h2 {
            font-size: 2.5rem;
            margin: 0 0 0.5rem 0;
            filter: drop-shadow(0 4px 8px rgba(0, 0, 0, 0.3));
            position: relative;
            z-index: 1;
        }

        .metric-container h3 {
            color: #e2e8f0;
            margin: 0.5rem 0;
            font-weight: 600;
            font-size: 1.6rem;
            text-shadow: 0 2px 10px rgba(0, 0, 0, 0.3);
            position: relative;
            z-index: 1;
        }

        .metric-container p {
            color: #94a3b8;
            margin: 0;
            font-size: 0.9rem;
            font-weight: 500;
            position: relative;
            z-index: 1;
        }

        .activity-card {
            background: rgba(15, 15, 35, 0.7);
            backdrop-filter: blur(15px);
            border: 1px solid rgba(255, 255, 255, 0.1);
            border-radius: 16px;
            padding: 2rem;
            margin: 1.5rem 0;
            border-left: 4px solid #667eea;
            box-shadow: 
                0 8px 32px rgba(0, 0, 0, 0.3),
                inset 0 1px 0 rgba(255, 255, 255, 0.1);
            transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
            position: relative;
            overflow: hidden;
        }

        .activity-card::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background: linear-gradient(135deg, rgba(102, 126, 234, 0.05) 0%, rgba(118, 75, 162, 0.05) 100%);
            opacity: 0;
            transition: opacity 0.3s ease;
        }

        .activity-card:hover {
            transform: translateY(-4px) scale(1.01);
            box-shadow: 
                0 16px 40px rgba(102, 126, 234, 0.2),
                0 0 0 1px rgba(102, 126, 234, 0.2),
                inset 0 1px 0 rgba(255, 255, 255, 0.15);
        }

        .activity-card:hover::before {
            opacity: 1;
        }

        .activity-card h4 {
            color: #f1f5f9;
            margin: 0 0 1rem 0;
            font-weight: 600;
            font-size: 1.2rem;
            position: relative;
            z-index: 1;
        }

        .productivity-high {
            border-left-color: #10b981 !important;
            background: linear-gradient(135deg, rgba(15, 15, 35, 0.7) 0%, rgba(16, 185, 129, 0.1) 100%);
        }

        .productivity-medium {
            border-left-color: #f59e0b !important;
            background: linear-gradient(135deg, rgba(15, 15, 35, 0.7) 0%, rgba(245, 158, 11, 0.1) 100%);
        }

        .productivity-low {
            border-left-color: #ef4444 !important;
            background: linear-gradient(135deg, rgba(15, 15, 35, 0.7) 0%, rgba(239, 68, 68, 0.1) 100%);
        }

        .roast-message {
            background: linear-gradient(135deg, rgba(255, 59, 48, 0.15) 0%, rgba(255, 149, 0, 0.1) 100%) !important;
            backdrop-filter: blur(15px) !important;
            border: 2px solid rgba(255, 59, 48, 0.4) !important;
            padding: 1.8rem !important;
            border-radius: 16px !important;
            margin: 1.5rem 0 !important;
            color: #ffffff !important;
            box-shadow: 
                0 12px 35px rgba(255, 59, 48, 0.25),
                0 4px 15px rgba(0, 0, 0, 0.1),
                inset 0 1px 0 rgba(255, 255, 255, 0.15) !important;
            position: relative !important;
            overflow: hidden !important;
            font-size: 1.05rem !important;
            line-height: 1.6 !important;
            text-shadow: 0 1px 3px rgba(0, 0, 0, 0.3) !important;
            animation: roastGlow 0.6s ease-out !important;
        }

        @keyframes roastGlow {
            0% {
                opacity: 0;
                transform: translateY(20px) scale(0.95);
                box-shadow: 0 0 0 rgba(255, 59, 48, 0);
            }
            100% {
                opacity: 1;
                transform: translateY(0) scale(1);
                box-shadow: 
                    0 12px 35px rgba(255, 59, 48, 0.25),
                    0 4px 15px rgba(0, 0, 0, 0.1),
                    inset 0 1px 0 rgba(255, 255, 255, 0.15);
            }
        }

        .roast-message::before {
            content: '' !important;
            position: absolute !important;
            top: 0 !important;
            left: 0 !important;
            width: 6px !important;
            height: 100% !important;
            background: linear-gradient(180deg, #ff3b30, #ff9500, #ff3b30) !important;
            border-radius: 0 3px 3px 0 !important;
            box-shadow: 0 0 15px rgba(255, 59, 48, 0.5) !important;
        }

        .roast-message::after {
            content: '🎭' !important;
            position: absolute !important;
            top: 1rem !important;
            right: 1rem !important;
            font-size: 1.5rem !important;
            opacity: 0.7 !important;
            animation: float 3s ease-in-out infinite !important;
        }

        .roast-message strong {
            color: #ffcc02 !important;
            text-shadow: 0 2px 10px rgba(255, 204, 2, 0.4) !important;
            font-weight: 700 !important;
            font-size: 1.1rem !important;
            display: inline-block !important;
            margin-bottom: 0.5rem !important;
        }

        .roast-message br {
            line-height: 2 !important;
        }

        /* Force override any conflicting styles */
        div.roast-message,
        div[class*="roast-message"] {
            background: linear-gradient(135deg, rgba(255, 59, 48, 0.15) 0%, rgba(255, 149, 0, 0.1) 100%) !important;
            border: 2px solid rgba(255, 59, 48, 0.4) !important;
            color: #ffffff !important;
            padding: 1.8rem !important;
            border-radius: 16px !important;
            margin: 1.5rem 0 !important;
            font-size: 1.05rem !important;
        }

        .sidebar-content {
            background: rgba(15, 15, 35, 0.8);
            backdrop-filter: blur(15px);
            border: 1px solid rgba(255, 255, 255, 0.1);
            padding: 1.5rem;
            border-radius: 16px;
            margin-bottom: 1rem;
            box-shadow: 
                0 8px 32px rgba(0, 0, 0, 0.3),
                inset 0 1px 0 rgba(255, 255, 255, 0.1);
        }

        .insight-card {
            background: rgba(15, 15, 35, 0.8);
            backdrop-filter: blur(15px);
            border: 1px solid rgba(255, 255, 255, 0.1);
            padding: 2rem;
            border-radius: 16px;
            margin: 1rem 0;
            border-left: 4px solid #8b5cf6;
            box-shadow: 
                0 8px 32px rgba(0, 0, 0, 0.3),
                inset 0 1px 0 rgba(255, 255, 255, 0.1);
            background: linear-gradient(135deg, rgba(15, 15, 35, 0.8) 0%, rgba(139, 92, 246, 0.1) 100%);
            position: relative;
            overflow: hidden;
        }

        .insight-card::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background: linear-gradient(135deg, rgba(139, 92, 246, 0.05) 0%, rgba(168, 85, 247, 0.05) 100%);
            opacity: 0;
            transition: opacity 0.3s ease;
        }

        .insight-card:hover::before {
            opacity: 1;
        }

        .insight-card h3 {
            color: #f1f5f9;
            margin: 0 0 1rem 0;
            font-weight: 600;
            position: relative;
            z-index: 1;
        }

        .stTabs [data-baseweb="tab-list"] {
            gap: 0.75rem;
            background: none;
            border-bottom: none;
            padding: 0.5rem;
        }

        .stTabs [data-baseweb="tab"] {
            background: rgba(15, 15, 35, 0.6);
            backdrop-filter: blur(10px);
            border: 1px solid rgba(255, 255, 255, 0.1);
            color: #94a3b8;
            border-radius: 12px;
            font-weight: 500;
            padding: 1rem 2rem;
            margin-bottom: 0.5rem;
            transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
            box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
        }

        .stTabs [data-baseweb="tab"]:hover {
            background: rgba(15, 15, 35, 0.8);
            border-color: rgba(102, 126, 234, 0.3);
            transform: translateY(-2px);
            color: #e2e8f0;
        }

        .stTabs [aria-selected="true"] {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: #ffffff;
            transform: translateY(-3px);
            box-shadow: 
                0 8px 25px rgba(102, 126, 234, 0.4),
                0 0 0 1px rgba(255, 255, 255, 0.1),
                inset 0 1px 0 rgba(255, 255, 255, 0.2);
            border-color: rgba(102, 126, 234, 0.5);
        }

        /* Enhanced Dark Streamlit Component Overrides */
        .stButton > button {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border: 1px solid rgba(255, 255, 255, 0.1);
            border-radius: 12px;
            padding: 1rem 2rem;
            font-weight: 600;
            font-family: 'Poppins', sans-serif;
            transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
            box-shadow: 
                0 8px 25px rgba(102, 126, 234, 0.3),
                inset 0 1px 0 rgba(255, 255, 255, 0.2);
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }

        .stButton > button:hover {
            transform: translateY(-3px) scale(1.02);
            box-shadow: 
                0 12px 35px rgba(102, 126, 234, 0.4),
                0 0 0 1px rgba(255, 255, 255, 0.2),
                inset 0 1px 0 rgba(255, 255, 255, 0.3);
        }

        .stTextArea > div > div > textarea {
            background: rgba(15, 15, 35, 0.8) !important;
            backdrop-filter: blur(15px);
            border: 1px solid rgba(255, 255, 255, 0.1) !important;
            border-radius: 12px !important;
            color: #e2e8f0 !important;
            font-family: 'JetBrains Mono', monospace !important;
            padding: 1rem !important;
            box-shadow: 
                0 8px 25px rgba(0, 0, 0, 0.3),
                inset 0 1px 0 rgba(255, 255, 255, 0.1) !important;
        }

        .stTextArea > div > div > textarea:focus {
            border-color: rgba(102, 126, 234, 0.5) !important;
            box-shadow: 
                0 0 0 3px rgba(102, 126, 234, 0.2),
                0 8px 25px rgba(0, 0, 0, 0.3),
                inset 0 1px 0 rgba(255, 255, 255, 0.1) !important;
        }

        .stSelectbox > div > div > div {
            background: rgba(15, 15, 35, 0.8) !important;
            backdrop-filter: blur(15px);
            border: 1px solid rgba(255, 255, 255, 0.1) !important;
            border-radius: 12px !important;
            color: #e2e8f0 !important;
            box-shadow: 
                0 8px 25px rgba(0, 0, 0, 0.3),
                inset 0 1px 0 rgba(255, 255, 255, 0.1);
        }

        .stRadio > div {
            background: rgba(15, 15, 35, 0.8);
            backdrop-filter: blur(15px);
            border: 1px solid rgba(255, 255, 255, 0.1);
            padding: 1.5rem;
            border-radius: 16px;
            box-shadow: 
                0 8px 25px rgba(0, 0, 0, 0.3),
                inset 0 1px 0 rgba(255, 255, 255, 0.1);
        }

        .stRadio > div > label {
            background: rgba(15, 15, 35, 0.6);
            backdrop-filter: blur(10px);
            border: 1px solid rgba(255, 255, 255, 0.1);
            color: #94a3b8;
            padding: 1rem 1.5rem;
            border-radius: 12px;
            margin: 0.5rem;
            transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
            box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
        }

        .stRadio > div > label:hover {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            transform: translateY(-2px) scale(1.02);
            box-shadow: 
                0 8px 25px rgba(102, 126, 234, 0.3),
                0 0 0 1px rgba(255, 255, 255, 0.2),
                inset 0 1px 0 rgba(255, 255, 255, 0.2);
            border-color: rgba(102, 126, 234, 0.5);
        }

        .stRadio input[type="radio"]:checked + div {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
            color: white !important;
            box-shadow: 
                0 8px 25px rgba(102, 126, 234, 0.4),
                0 0 0 1px rgba(255, 255, 255, 0.2),
                inset 0 1px 0 rgba(255, 255, 255, 0.2) !important;
        }

        /* Enhanced Dark Progress Bars */
        .stProgress > div > div > div > div {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
            box-shadow: 
                0 2px 10px rgba(102, 126, 234, 0.3),
                inset 0 1px 0 rgba(255, 255, 255, 0.2);
            border-radius: 6px;
        }

        .stProgress > div > div > div {
            background: rgba(15, 15, 35, 0.6) !important;
            border-radius: 6px;
            border: 1px solid rgba(255, 255, 255, 0.1);
        }

        /* Scroll Stack Statistics Styles */
        .stats-scroll-stack {
            background: rgba(248, 250, 252, 0.95);
            backdrop-filter: blur(20px);
            border-radius: 20px;
            padding: 1.5rem;
            margin-bottom: 1rem;
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.12);
            border: 1px solid rgba(226, 232, 240, 0.5);
        }

        .stats-header {
            text-align: center;
            margin-bottom: 1.5rem;
            position: relative;
        }

        .stats-header h3 {
            color: #1a202c;
            margin: 0;
            font-size: 1.2rem;
            font-weight: 600;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
        }

        .stats-subtitle {
            color: #718096;
            font-size: 0.8rem;
            font-style: italic;
            margin-top: 0.25rem;
        }

        .scroll-stack-container {
            position: relative;
            perspective: 1000px;
        }

        .stack-card {
            position: relative;
            background: linear-gradient(135deg, rgba(248, 250, 252, 0.9) 0%, rgba(241, 245, 249, 0.8) 100%);
            border-radius: 16px;
            padding: 1.25rem;
            margin-bottom: 0.75rem;
            border: 1px solid rgba(226, 232, 240, 0.6);
            transform-origin: top center;
            transition: all 0.6s cubic-bezier(0.4, 0, 0.2, 1);
            overflow: hidden;
            backdrop-filter: blur(10px);
            box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
        }

        .stack-card:hover {
            transform: translateY(-8px) scale(1.02) rotateX(5deg);
            box-shadow: 0 12px 40px rgba(102, 126, 234, 0.2);
            border-color: rgba(102, 126, 234, 0.3);
        }

        .stack-card[data-index="0"] {
            transform: translateY(0px) scale(1);
            z-index: 4;
        }

        .stack-card[data-index="1"] {
            transform: translateY(-8px) scale(0.98);
            z-index: 3;
        }

        .stack-card[data-index="2"] {
            transform: translateY(-16px) scale(0.96);
            z-index: 2;
        }

        .stack-card[data-index="3"] {
            transform: translateY(-24px) scale(0.94);
            z-index: 1;
        }

        .card-glow {
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            border-radius: 16px;
            background: linear-gradient(135deg, rgba(102, 126, 234, 0.1) 0%, rgba(118, 75, 162, 0.1) 100%);
            opacity: 0;
            transition: opacity 0.3s ease;
        }

        .stack-card:hover .card-glow {
            opacity: 1;
        }

        .warning-card {
            background: linear-gradient(135deg, rgba(254, 242, 242, 0.9) 0%, rgba(254, 226, 226, 0.8) 100%);
            border-color: rgba(245, 101, 101, 0.3);
        }

        .warning-glow {
            background: linear-gradient(135deg, rgba(245, 101, 101, 0.1) 0%, rgba(239, 68, 68, 0.1) 100%);
        }

        .metric-icon {
            font-size: 2rem;
            margin-bottom: 0.5rem;
            display: block;
            text-align: center;
            filter: drop-shadow(0 2px 4px rgba(0, 0, 0, 0.1));
            animation: float 3s ease-in-out infinite;
        }

        @keyframes float {
            0%, 100% { transform: translateY(0px); }
            50% { transform: translateY(-5px); }
        }

        .metric-value {
            font-size: 1.8rem;
            font-weight: 700;
            color: #1a202c;
            text-align: center;
            margin-bottom: 0.25rem;
            text-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
        }

        .metric-label {
            font-size: 0.85rem;
            color: #4a5568;
            text-align: center;
            font-weight: 500;
            margin-bottom: 0.75rem;
        }

        .card-progress {
            height: 3px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            border-radius: 2px;
            transition: width 0.8s ease-out;
            position: relative;
            overflow: hidden;
        }

        .card-progress::after {
            content: '';
            position: absolute;
            top: 0;
            left: -100%;
            width: 100%;
            height: 100%;
            background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.6), transparent);
            animation: shimmer 2s infinite;
        }

        @keyframes shimmer {
            0% { left: -100%; }
            100% { left: 100%; }
        }

        .warning-pulse {
            position: absolute;
            top: 10px;
            right: 10px;
            width: 8px;
            height: 8px;
            background: #ef4444;
            border-radius: 50%;
            animation: pulse 2s infinite;
        }

        @keyframes pulse {
            0%, 100% { opacity: 1; transform: scale(1); }
            50% { opacity: 0.5; transform: scale(1.2); }
        }

        /* Enhanced Scroll Indicators and Animations */
        @keyframes stackEntry {
            0% {
                opacity: 0;
                transform: translateY(50px) scale(0.8) rotateX(-20deg);
                filter: blur(10px);
            }
            100% {
                opacity: 1;
                transform: translateY(0) scale(1) rotateX(0deg);
                filter: blur(0px);
            }
        }

        @keyframes fadeInUp {
            0% {
                opacity: 0;
                transform: translateY(30px);
            }
            100% {
                opacity: 1;
                transform: translateY(0);
            }
        }

        @keyframes glow {
            0%, 100% {
                box-shadow: 0 0 20px rgba(102, 126, 234, 0.3);
            }
            50% {
                box-shadow: 0 0 40px rgba(102, 126, 234, 0.5);
            }
        }

        .stack-card {
            animation: stackEntry 0.8s cubic-bezier(0.4, 0, 0.2, 1);
        }

        .stack-card[data-index="1"] {
            animation-delay: 0.15s;
        }

        .stack-card[data-index="2"] {
            animation-delay: 0.3s;
        }

        .stack-card[data-index="3"] {
            animation-delay: 0.45s;
        }

        /* Smooth page transitions */
        .main > div {
            animation: fadeInUp 0.6s ease-out;
        }

        /* Add subtle scroll indicator */
        .scroll-indicator {
            position: fixed;
            top: 0;
            left: 0;
            height: 3px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            z-index: 9999;
            transition: width 0.3s ease;
        }

        /* Custom scrollbar */
        ::-webkit-scrollbar {
            width: 8px;
        }

        ::-webkit-scrollbar-track {
            background: rgba(15, 15, 35, 0.5);
        }

        ::-webkit-scrollbar-thumb {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            border-radius: 4px;
        }

        ::-webkit-scrollbar-thumb:hover {
            background: linear-gradient(135deg, #5a6fd8 0%, #6b46c1 100%);
        }

        /* Keyframe animation for sliding in elements */
        @keyframes slideInUp {
            0% {
                opacity: 0;
                transform: translateY(30px) scale(0.95);
            }
            100% {
                opacity: 1;
                transform: translateY(0) scale(1);
            }
        }
        </style>
        """, unsafe_allow_html=True)

        # Clean Header
        st.markdown("""
        <div class="main-header">
            <h1>MotivAgent</h1>
            <h3>Your Personal Activity Coach</h3>
            <p>Track, analyze, and improve your daily habits</p>
        </div>
        """, unsafe_allow_html=True)

        # Enhanced Sidebar with Scroll Stack Animation
        with st.sidebar:
            st.markdown("""
            <div class="stats-scroll-stack">
                <div class="stats-header">
                    <h3>📊 Statistics Dashboard</h3>
                    <div class="stats-subtitle">Your productivity journey</div>
                </div>
            """, unsafe_allow_html=True)

            streak_info = st.session_state.memory.get_streak_info()

            # Native Streamlit metrics with enhanced styling
            st.markdown("### 🔥 Current Streak")
            st.metric(
                label="Days", 
                value=streak_info['current_streak'],
                delta=None if streak_info['current_streak'] == 0 else "🔥 On fire!"
            )

            st.markdown("### 📊 Total Sessions")
            st.metric(
                label="Activities Logged", 
                value=streak_info['total_sessions'],
                delta=f"+{streak_info.get('sessions_this_week', 0)} this week"
            )

            st.markdown("### 🏆 Best Streak")
            st.metric(
                label="Personal Record", 
                value=streak_info['longest_streak'],
                delta="Days" if streak_info['longest_streak'] > 1 else "Day"
            )

            if streak_info['is_streak_broken']:
                st.markdown("### ⏰ Days Inactive")
                st.error(f"**{streak_info['days_inactive']} days** without activity")
                st.markdown("💡 *Time to get back on track!*")

            st.markdown("</div>", unsafe_allow_html=True)

            # Progress visualization
            if streak_info['current_streak'] > 0:
                progress = min(streak_info['current_streak'] / 30, 1.0)  # 30-day goal
                st.markdown("### 🎯 Progress to 30-Day Goal")
                st.progress(progress)
                st.write(f"{int(progress * 100)}% Complete")

        # Main content tabs
        tab1, tab2, tab3, tab4 = st.tabs(["Log Activities", "Weekly Insights", "Smart Analytics", "Test Mode"])

        with tab1:
            self.activity_logger()

        with tab2:
            self.weekly_insights()

        with tab3:
            self.smart_analytics()

        with tab4:
            self.test_mode()

    def activity_logger(self):
        st.markdown("### Daily Activity Log")

        # Input methods
        input_method = st.radio(
            "Input Method",
            ["Text Input", "Quick Actions"],
            horizontal=True
        )

        if input_method == "Text Input":
            st.markdown("#### Describe your activities")
            user_input = st.text_area(
                "Activities",
                placeholder="e.g., 'walked 45 minutes, studied for 2 hours, watched 1 episode of a show'",
                height=100,
                help="Be specific about duration and activities for better tracking"
            )

            if st.button("Analyze Activities", type="primary", use_container_width=True):
                if user_input.strip():
                    self.process_activities(user_input)
                else:
                    st.warning("Please enter some activities to analyze")

        else:
            st.markdown("#### Quick Activity Buttons")
            st.markdown("*One-click activity logging with smart suggestions*")

            # Context-aware quick activities
            current_hour = datetime.now().hour
            if current_hour < 10:
                time_context = "morning"
                suggested_activities = [
                    ("Morning Walk", "took a refreshing 30-minute morning walk", "🚶"),
                    ("Workout", "did an energizing 45-minute morning workout", "💪"),
                    ("Meditation", "started the day with 15 minutes of meditation", "🧘"),
                    ("Coffee & News", "enjoyed coffee while reading news for 20 minutes", "☕"),
                    ("Stretching", "did gentle morning stretches for 10 minutes", "🤸"),
                    ("Planning", "spent 15 minutes planning my day", "📋")
                ]
            elif current_hour < 17:
                time_context = "afternoon"
                suggested_activities = [
                    ("Study Session", "focused studying for 1 hour", "📚"),
                    ("Work Project", "worked productively on projects for 2 hours", "💼"),
                    ("Lunch Break", "enjoyed a relaxing 30-minute lunch break", "🍽️"),
                    ("Quick Exercise", "did a quick 20-minute workout", "💪"),
                    ("Creative Work", "spent 45 minutes on creative projects", "🎨"),
                    ("Learning", "watched educational content for 30 minutes", "🎓")
                ]
            else:
                time_context = "evening"
                suggested_activities = [
                    ("Evening Walk", "took a peaceful 30-minute evening walk", "🌅"),
                    ("Netflix Binge", "watched 3 episodes of my favorite show", "📺"),
                    ("Gaming", "played games for 1.5 hours", "🎮"),
                    ("Cooking", "cooked a nice dinner for 45 minutes", "🍳"),
                    ("Reading", "read a book for 40 minutes before bed", "📖"),
                    ("Social Time", "spent quality time with friends for 2 hours", "👥")
                ]

            st.caption(f"*{time_context.title()} suggestions - or create your own below*")

            cols = st.columns(3)
            for i, (button_text, activity_text, icon) in enumerate(suggested_activities):
                col = cols[i % 3]
                if col.button(f"{icon} {button_text}", use_container_width=True):
                    self.process_activities(activity_text)

            # Custom quick activity builder
            with st.expander("🛠️ Build Custom Activity", expanded=False):
                col1, col2, col3 = st.columns(3)

                with col1:
                    custom_activity = st.selectbox("Activity Type", [
                        "walked", "ran", "studied", "worked on", "watched", "played",
                        "cooked", "cleaned", "read", "meditated", "exercised"
                    ])

                with col2:
                    custom_duration = st.number_input("Duration (minutes)", min_value=5, max_value=480, value=30)

                with col3:
                    custom_details = st.text_input("Details (optional)", placeholder="e.g., 'at the gym', 'with friends'")

                custom_text = f"{custom_activity} for {custom_duration} minutes"
                if custom_details:
                    custom_text += f" {custom_details}"

                if st.button("🚀 Log Custom Activity", use_container_width=True):
                    self.process_activities(custom_text)

    def process_activities(self, user_input):
        with st.spinner("🧠 Analyzing your life choices... This might sting a little..."):
            # Parse activities
            activities = st.session_state.planner.parse_input(user_input)

            # Process with executor
            processed = st.session_state.executor.process_activities(activities)

            # Store in memory
            st.session_state.memory.store_session(processed)

            # Display results with enhanced styling
            st.success("✅ Analysis Complete! Brace yourself...")

            total_calories = sum(a['calories_burned'] for a in processed)
            avg_productivity = sum(a['productivity_score'] for a in processed) / len(processed)

            # Enhanced summary metrics
            col1, col2, col3, col4 = st.columns(4)

            with col1:
                st.markdown(f"""
                <div class="metric-container">
                    <h2 style="color: #ff6b6b;">🔥</h2>
                    <h3>{total_calories}</h3>
                    <p>Calories Burned</p>
                </div>
                """, unsafe_allow_html=True)

            with col2:
                color = "#4caf50" if avg_productivity >= 7 else "#ff9800" if avg_productivity >= 4 else "#f44336"
                st.markdown(f"""
                <div class="metric-container">
                    <h2 style="color: {color};">📊</h2>
                    <h3>{avg_productivity:.1f}/10</h3>
                    <p>Avg Productivity</p>
                </div>
                """, unsafe_allow_html=True)

            with col3:
                st.markdown(f"""
                <div class="metric-container">
                    <h2 style="color: #667eea;">📝</h2>
                    <h3>{len(processed)}</h3>
                    <p>Activities</p>
                </div>
                """, unsafe_allow_html=True)

            with col4:
                total_time = sum(a['duration'] for a in processed)
                st.markdown(f"""
                <div class="metric-container">
                    <h2 style="color: #764ba2;">⏰</h2>
                    <h3>{total_time}</h3>
                    <p>Total Minutes</p>
                </div>
                """, unsafe_allow_html=True)

            # Individual activity results with enhanced cards
        st.markdown("### 🎭 RoastBot's Individual Verdicts")

        for i, activity in enumerate(processed, 1):
            productivity_class = "productivity-high" if activity['productivity_score'] >= 7 else \
                               "productivity-medium" if activity['productivity_score'] >= 4 else "productivity-low"

            # Build context display
            context_info = []
            context = activity.get('context', {})
            if 'location' in context:
                context_info.append(f"📍 {context['location']}")
            if context.get('with_others'):
                context_info.append("👥 With others")
            elif context.get('with_others') == False:
                context_info.append("🚶 Solo")
            if 'time_of_day' in context:
                context_info.append(f"🕐 {context['time_of_day']}")

            mood_emoji = {'positive': '😊', 'negative': '😔', 'neutral': '😐'}
            mood_display = mood_emoji.get(activity.get('mood', 'neutral'), '😐')

            subcategory = activity.get('subcategory', 'general')
            subcategory_display = f" ({subcategory})" if subcategory != 'general' else ""

            confidence = activity.get('confidence', 0)
            confidence_display = "🎯 High" if confidence > 0.7 else "🤔 Medium" if confidence > 0.3 else "❓ Low"

            animation_delay = (i-1)*0.1
            st.markdown(f"""
            <div class="activity-card {productivity_class}" style="animation: slideInUp 0.6s ease-out; animation-delay: {animation_delay}s; animation-fill-mode: both;">
                <div style="display: flex; align-items: center; margin-bottom: 1rem;">
                    <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); width: 40px; height: 40px; border-radius: 50%; display: flex; align-items: center; justify-content: center; margin-right: 1rem; font-size: 1.2rem; box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);">
                        📌
                    </div>
                    <h4 style="margin: 0; flex: 1; color: #f1f5f9; font-size: 1.3rem; font-weight: 600;">Activity {i}: {activity['text']}</h4>
                </div>

                <div style="display: grid; grid-template-columns: 2fr 1fr; gap: 2rem; margin: 1.5rem 0; background: rgba(255, 255, 255, 0.03); padding: 1.5rem; border-radius: 12px; border: 1px solid rgba(255, 255, 255, 0.1);">
                    <div style="color: #e2e8f0;">
                        <div style="margin-bottom: 0.8rem;"><span style="color: #94a3b8; font-weight: 500;">Category:</span> <span style="color: #60a5fa; font-weight: 600;">{activity['category'].title()}{subcategory_display}</span></div>
                        <div style="margin-bottom: 0.8rem;"><span style="color: #94a3b8; font-weight: 500;">Duration:</span> <span style="color: #34d399; font-weight: 600;">{activity['duration']} minutes</span></div>
                        <div style="margin-bottom: 0.8rem;"><span style="color: #94a3b8; font-weight: 500;">Intensity:</span> <span style="color: #fbbf24; font-weight: 600;">{activity['intensity'].title()}</span></div>
                        <div><span style="color: #94a3b8; font-weight: 500;">Mood:</span> <span style="font-weight: 600;">{mood_display} {activity.get('mood', 'neutral').title()}</span></div>
                    </div>
                    <div style="text-align: center;">
                        <div style="background: linear-gradient(135deg, #ef4444 0%, #f97316 100%); color: white; padding: 0.8rem; border-radius: 12px; margin-bottom: 1rem; box-shadow: 0 4px 15px rgba(239, 68, 68, 0.3);">
                            <div style="font-size: 1.8rem; font-weight: 700; margin-bottom: 0.2rem;">{activity['calories_burned']}</div>
                            <div style="font-size: 0.9rem; opacity: 0.9;">calories</div>
                        </div>
                        <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 0.8rem; border-radius: 12px; margin-bottom: 0.5rem; box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);">
                            <div style="font-size: 1.8rem; font-weight: 700; margin-bottom: 0.2rem;">{activity['productivity_score']}/10</div>
                            <div style="font-size: 0.9rem; opacity: 0.9;">productivity</div>
                        </div>
                        <div style="color: #64748b; font-size: 0.8rem; opacity: 0.8;">Parse: {confidence_display}</div>
                    </div>
                </div>

                {f'<div style="margin: 1rem 0; color: #94a3b8; font-size: 0.95rem; padding: 0.8rem; background: rgba(255, 255, 255, 0.02); border-radius: 8px; border-left: 3px solid #667eea;"><strong>Context:</strong> {" • ".join(context_info)}</div>' if context_info else ''}
            </div>
            """, unsafe_allow_html=True)

            # Use Streamlit components for roast message
            st.markdown(f"""
            <div style="
                background: linear-gradient(135deg, rgba(255, 59, 48, 0.15) 0%, rgba(255, 149, 0, 0.1) 100%);
                backdrop-filter: blur(15px);
                border: 2px solid rgba(255, 59, 48, 0.4);
                padding: 1.8rem;
                border-radius: 16px;
                margin: 1.5rem 0;
                color: #ffffff;
                box-shadow: 0 12px 35px rgba(255, 59, 48, 0.25), 0 4px 15px rgba(0, 0, 0, 0.1), inset 0 1px 0 rgba(255, 255, 255, 0.15);
                position: relative;
                overflow: hidden;
                font-size: 1.05rem;
                line-height: 1.6;
                text-shadow: 0 1px 3px rgba(0, 0, 0, 0.3);
                animation: roastGlow 0.6s ease-out;
            ">
                <div style="color: #ffcc02; text-shadow: 0 2px 10px rgba(255, 204, 2, 0.4); font-weight: 700; font-size: 1.1rem; margin-bottom: 0.5rem;">
                    🎭 RoastBot Says:
                </div>
                {activity['motivation_message']}
                <div style="position: absolute; top: 1rem; right: 1rem; font-size: 1.5rem; opacity: 0.7;">🎭</div>
            </div>
            """, unsafe_allow_html=True)

    def weekly_insights(self):
        st.markdown("### Weekly Overview")

        insights = st.session_state.insight.analyze_weekly_trends()
        weekly_summary = st.session_state.memory.get_weekly_summary()

        # Clean summary cards
        col1, col2, col3, col4 = st.columns(4)

        metrics = [
            ("📊", "Activities", weekly_summary.get('total_activities', 0), "#3498db"),
            ("🔥", "Calories", f"{weekly_summary.get('total_calories', 0)}", "#e74c3c"),
            ("⭐", "Avg Score", f"{weekly_summary.get('avg_productivity', 0):.1f}/10", "#27ae60"),
            ("📈", "Trend", insights['trend'].title(), "#9b59b6")
        ]

        for col, (icon, label, value, color) in zip([col1, col2, col3, col4], metrics):
            col.markdown(f"""
            <div class="metric-container">
                <h2 style="color: {color};">{icon}</h2>
                <h3>{value}</h3>
                <p>{label}</p>
            </div>
            """, unsafe_allow_html=True)

        # Weekly summary
        st.markdown(f"""
        <div class="insight-card">
            <h3>Weekly Summary</h3>
            <p>{insights['roast_summary']}</p>
        </div>
        """, unsafe_allow_html=True)

        # Create columns for insights and breakdown
        col1, col2 = st.columns([1, 1])

        with col1:
            st.markdown("### 💡 Key Insights")
            for insight in insights['insights']:
                st.markdown(f"• {insight}")

        with col2:
            st.markdown("### 📋 Activity Breakdown")
            if insights['category_analysis']['breakdown']:
                breakdown_data = []
                for category, stats in insights['category_analysis']['breakdown'].items():
                    breakdown_data.append({
                        'Category': category.title(),
                        'Count': stats['count'],
                        'Time (min)': stats['total_time']
                    })

                df = pd.DataFrame(breakdown_data)

                # Create a pie chart
                fig = px.pie(df, values='Count', names='Category', 
                           title="Activity Distribution",
                           color_discrete_sequence=px.colors.qualitative.Set3)
                fig.update_layout(height=400)
                st.plotly_chart(fig, use_container_width=True)

        # Suggestions with enhanced styling
        suggestions = st.session_state.insight.suggest_improvements()
        st.markdown("### 🎯 Improvement Suggestions")
        for i, suggestion in enumerate(suggestions, 1):
            st.markdown(f"""
            <div style="background: linear-gradient(135deg, #e3f2fd 0%, #f3e5f5 100%); 
                        padding: 1rem; border-radius: 10px; margin: 0.5rem 0; 
                        border-left: 4px solid #2196f3;">
                <strong>{i}.</strong> {suggestion}
            </div>
            """, unsafe_allow_html=True)

    def smart_analytics(self):
        st.markdown("### 🧠 Smart Analytics Dashboard")
        st.markdown("*Advanced insights powered by enhanced activity understanding*")

        # Get enhanced data
        weekly_data = st.session_state.memory.get_weekly_data()
        if not weekly_data:
            st.info("📊 No data available yet. Start logging activities to see advanced analytics!")
            return

        # Extract all activities for analysis
        all_activities = []
        for session in weekly_data:
            all_activities.extend(session.get('activities', []))

        if not all_activities:
            st.info("📊 No activities found in recent data.")
            return

        # Analytics sections
        col1, col2 = st.columns(2)

        with col1:
            st.markdown("#### 🎯 Activity Patterns")

            # Category distribution with subcategories
            category_data = {}
            subcategory_data = {}

            for activity in all_activities:
                cat = activity.get('category', 'other')
                subcat = activity.get('subcategory', 'general')

                category_data[cat] = category_data.get(cat, 0) + 1
                key = f"{cat} - {subcat}" if subcat != 'general' else cat
                subcategory_data[key] = subcategory_data.get(key, 0) + 1

            # Create category chart
            if category_data:
                df_cat = pd.DataFrame(list(category_data.items()), columns=['Category', 'Count'])
                fig = px.bar(df_cat, x='Category', y='Count', 
                           title="Activity Categories",
                           color='Count',
                           color_continuous_scale='viridis')
                fig.update_layout(height=300)
                st.plotly_chart(fig, use_container_width=True)

        with col2:
            st.markdown("#### ⏰ Time Patterns")

            # Duration analysis
            durations = [activity.get('duration', 0) for activity in all_activities]
            if durations:
                avg_duration = sum(durations) / len(durations)
                max_duration = max(durations)
                total_time = sum(durations)

                st.metric("Average Duration", f"{avg_duration:.1f} min")
                st.metric("Longest Session", f"{max_duration} min") 
                st.metric("Total Time Tracked", f"{total_time//60}h {total_time%60}m")

        # Productivity trends
        st.markdown("#### 📈 Productivity Intelligence")

        col1, col2, col3 = st.columns(3)

        with col1:
            # Mood analysis
            moods = [activity.get('mood', 'neutral') for activity in all_activities]
            mood_counts = {mood: moods.count(mood) for mood in set(moods)}

            st.markdown("**Mood Distribution**")
            for mood, count in mood_counts.items():
                percentage = (count / len(moods)) * 100
                emoji = {'positive': '😊', 'negative': '😔', 'neutral': '😐'}
                st.write(f"{emoji.get(mood, '😐')} {mood.title()}: {percentage:.1f}%")

        with col2:
            # Intensity patterns
            intensities = [activity.get('intensity', 'medium') for activity in all_activities]
            intensity_counts = {i: intensities.count(i) for i in set(intensities)}

            st.markdown("**Intensity Levels**")
            for intensity, count in intensity_counts.items():
                percentage = (count / len(intensities)) * 100
                emoji = {'high': '🔥', 'medium': '⚡', 'low': '🌱'}
                st.write(f"{emoji.get(intensity, '⚡')} {intensity.title()}: {percentage:.1f}%")

        with col3:
            # Context insights
            social_activities = sum(1 for a in all_activities if a.get('context', {}).get('with_others'))
            solo_activities = sum(1 for a in all_activities if a.get('context', {}).get('with_others') == False)

            st.markdown("**Social vs Solo**")
            if social_activities + solo_activities > 0:
                social_pct = (social_activities / (social_activities + solo_activities)) * 100
                st.write(f"👥 Social: {social_pct:.1f}%")
                st.write(f"🚶 Solo: {100-social_pct:.1f}%")

        # Advanced insights
        st.markdown("#### 🔮 AI-Powered Insights")

        # Generate smart insights
        insights = self._generate_smart_insights(all_activities)

        for insight in insights:
            st.markdown(f"""
            <div style="background: linear-gradient(135deg, #f0f9ff 0%, #e0f2fe 100%); 
                        padding: 1rem; border-radius: 10px; margin: 0.5rem 0; 
                        border-left: 4px solid #0ea5e9;">
                {insight}
            </div>
            """, unsafe_allow_html=True)

        # Parsing quality analysis
        st.markdown("#### 🎯 Input Understanding Quality")

        confidence_scores = [activity.get('confidence', 0) for activity in all_activities]
        if confidence_scores:
            avg_confidence = sum(confidence_scores) / len(confidence_scores)
            high_confidence = sum(1 for c in confidence_scores if c > 0.7)

            col1, col2, col3 = st.columns(3)
            col1.metric("Average Parse Confidence", f"{avg_confidence:.2f}")
            col2.metric("High Confidence Parses", f"{high_confidence}/{len(confidence_scores)}")
            col3.metric("Parse Success Rate", f"{(high_confidence/len(confidence_scores)*100):.1f}%")

    def _generate_smart_insights(self, activities: List[Dict]) -> List[str]:
        """Generate AI-powered insights from activity data"""
        insights = []

        if not activities:
            return ["No activities to analyze yet!"]

        # Productivity patterns
        prod_scores = [a.get('productivity_score', 5) for a in activities]
        avg_prod = sum(prod_scores) / len(prod_scores)

        if avg_prod > 7:
            insights.append("🏆 **Productivity Champion**: You're consistently hitting high productivity scores! Keep up the excellent work.")
        elif avg_prod < 4:
            insights.append("📈 **Growth Opportunity**: Your productivity scores suggest room for improvement. Consider adding more structured activities.")

        # Time management insights
        durations = [a.get('duration', 0) for a in activities]
        if durations:
            long_sessions = sum(1 for d in durations if d > 120)
            if long_sessions > len(durations) * 0.3:
                insights.append("⏰ **Marathon Sessions**: You tend to do long activity sessions. Consider breaking them up with short breaks for better focus.")

        # Mood correlation
        positive_moods = sum(1 for a in activities if a.get('mood') == 'positive')
        if positive_moods > len(activities) * 0.6:
            insights.append("😊 **Positive Vibes**: You report positive moods frequently! This suggests good activity choices that align with your preferences.")

        # Category diversity
        categories = set(a.get('category') for a in activities)
        if len(categories) > 5:
            insights.append("🌈 **Well-Rounded**: You engage in diverse activity types, which is excellent for balanced personal development.")
        elif len(categories) < 3:
            insights.append("🎯 **Specialization**: You focus on fewer activity types. Consider exploring new categories for variety.")

        # Context insights
        social_count = sum(1 for a in activities if a.get('context', {}).get('with_others'))
        if social_count > len(activities) * 0.5:
            insights.append("👥 **Social Butterfly**: You frequently engage in activities with others. Great for building relationships!")
        elif social_count < len(activities) * 0.2:
            insights.append("🧘 **Solo Focus**: You prefer individual activities. Consider occasional social activities for balance.")

        return insights if insights else ["🤖 Analyzing your patterns... More data needed for deeper insights!"]

    def test_mode(self):
        st.markdown("### Test Scenarios")
        st.markdown("*Try different activity patterns to see how the enhanced system responds*")

        test_scenarios = [
            ("Active Morning", "went for an energizing 45-minute run at the park, feeling great this morning"),
            ("Study Focus", "studied advanced calculus for 3 hours with intense concentration at the library"),
            ("Gaming Binge", "played video games alone for 6 hours straight, got totally absorbed"),
            ("Wellness Day", "meditated peacefully for 30 minutes, did gentle yoga, and journaled about my thoughts"),
            ("Netflix Marathon", "binge-watched an entire season of my favorite show with friends, laughing all evening"),
            ("Productive Work", "worked on important projects for 4 hours at the office, feeling accomplished"),
            ("Creative Session", "painted for 2 hours at home, experimenting with new techniques and colors"),
            ("Social Evening", "had dinner with family for 1.5 hours, enjoyed great conversation and connection"),
            ("Mixed Day", "worked out hard for 1 hour at the gym, then studied programming for 2 hours, and relaxed watching Netflix"),
            ("Lazy Sunday", "slept in late, browsed social media for 2 hours, and watched movies all afternoon")
        ]

        cols = st.columns(2)
        for i, (title, scenario) in enumerate(test_scenarios):
            col = cols[i % 2]
            with col:
                if st.button(f"{title}", key=f"test_{i}", use_container_width=True):
                    st.markdown(f"**Testing scenario:** *{scenario}*")
                    self.process_activities(scenario)

if __name__ == "__main__":
    app = MotivAgentWeb()
    app.run()