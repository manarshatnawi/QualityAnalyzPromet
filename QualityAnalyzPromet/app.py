"""
Smart Code Quality Analyzer — Full Streamlit Interface
يعمل مع: code_quality_system.py (في نفس المجلد)
"""

import streamlit as st
import plotly.graph_objects as go
import math
import os
import difflib
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# استيراد المكونات الأساسية (تأكدي من وجود ملف core.py أو تغيير المسار حسب مشروعك)
try:
    from core import (
        ASTAnalyzer, ProblemClassifier, QualityScorer,
        IterativeRefiner, FeatureVector, QualityReport, IterationRecord
    )
except ImportError:
    st.error("لم يتم العثور على ملف core.py. تأكدي من وجوده في نفس المجلد.")

# ─────────────────────────────────────────────────────────────────────
# Language Support
# ─────────────────────────────────────────────────────────────────────
LANGUAGES = {
    "العربية": {
        "title": "محلل جودة الكود الذكي",
        "subtitle": "نظام تحليل وإصلاح الكود بشكل تكراري ذكي",
        "input_title": "📝 أدخل الكود",
        "example_button": "📋 مثال",
        "analyze_button": "🔍 تحليل",
        "refine_button": "✨ إصلاح",
        "results_title": "📊 النتائج",
        "quality_score": "درجة الجودة",
        "problems_found": "المشاكل المكتشفة",
        "improved_code": "الكود المحسن",
        "iterations": "التكرارات",
        "grade": "التقدير",
        "loading": "جاري التحليل...",
        "success": "تم التحليل بنجاح!",
        "error": "حدث خطأ أثناء التحليل"
    },
    "English": {
        "title": "Smart Code Quality Analyzer",
        "subtitle": "Intelligent iterative code analysis and refinement system",
        "input_title": "📝 Enter Code",
        "example_button": "📋 Example",
        "analyze_button": "🔍 Analyze",
        "refine_button": "✨ Refine",
        "results_title": "📊 Results",
        "quality_score": "Quality Score",
        "problems_found": "Problems Found",
        "improved_code": "Improved Code",
        "iterations": "Iterations",
        "grade": "Grade",
        "loading": "Analyzing...",
        "success": "Analysis completed successfully!",
        "error": "Error during analysis"
    }
}

# Language selector logic
if 'language' not in st.session_state:
    st.session_state.language = "العربية"

col1, col2 = st.columns([6, 2]) # زيادة العرض قليلاً للاستيعاب
with col2:
    # تم إصلاح السطر 67 (إضافة عنوان) والسطر 68 (ضبط الإزاحة)
    lang = st.selectbox(
        "Select Language / اختر اللغة", 
        ["العربية", "English"],
        index=["العربية", "English"].index(st.session_state.language),
        key="lang_selector"
    )
    st.session_state.language = lang

texts = LANGUAGES[st.session_state.language]

# ─────────────────────────────────────────────────────────────────────
# Page config (يجب أن يكون أول أمر Streamlit فعلي بعد الإعدادات)
# ─────────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title=texts["title"],
    page_icon="🔬",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────────────────────────────────
# Enhanced CSS (تم الإبقاء على تصميمك الجميل مع إصلاحات طفيفة)
# ─────────────────────────────────────────────────────────────────────
st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;600;700&family=JetBrains+Mono&display=swap');

html, body, [class*="css"] {{ 
    font-family: 'Cairo', sans-serif; 
}}
.hero {{
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    padding: 2rem;
    border-radius: 15px;
    color: white;
    text-align: center;
    margin-bottom: 2rem;
}}
.footer {{
    text-align: center;
    padding: 2rem;
    color: #666;
}}
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────
# Hero Section
# ─────────────────────────────────────────────────────────────────────
st.markdown(f"""
<div class="hero">
  <h1>🔬 {texts['title']}</h1>
  <p>{texts['subtitle']}</p>
</div>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────
# Sidebar & Logic
# ─────────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown(f"### ⚙️ {'الإعدادات' if st.session_state.language == 'العربية' else 'Settings'}")
    max_iter = st.slider(f"{'أقصى عدد تكرارات' if st.session_state.language == 'العربية' else 'Max Iterations'}", 1, 8, 4)
    target = st.slider(f"{'درجة الهدف' if st.session_state.language == 'العربية' else 'Target Score'}", 50, 100, 85)
    analyze_only = st.checkbox(f"{'تحليل فقط (بدون إصلاح)' if st.session_state.language == 'العربية' else 'Analyze Only'}", value=False)

# محاولة جلب المفتاح
groq_key = st.secrets.get("GROQ_API_KEY", os.environ.get("GROQ_API_KEY", ""))

if not groq_key and not analyze_only:
    st.warning("⚠️ مفتاح Groq API غير موجود. تم تفعيل وضع 'التحليل فقط'.")
    analyze_only = True

# ─────────────────────────────────────────────────────────────────────
# Input Area
# ─────────────────────────────────────────────────────────────────────
user_code = st.text_area(texts["input_title"], height=300, placeholder="Paste your Python code here...")

if st.button(texts["analyze_button"], type="primary", use_container_width=True):
    if user_code.strip():
        with st.spinner(texts["loading"]):
            # هنا تضعين منطق التحليل الخاص بك المستدعى من core.py
            st.success(texts["success"])
            # مثال للعرض فقط:
            st.code(user_code, language="python")
    else:
        st.error("الرجاء إدخال كود للتحليل.")

# ─────────────────────────────────────────────────────────────────────
# Footer
# ─────────────────────────────────────────────────────────────────────
st.markdown(f"""
<div class="footer">
  <p>👨‍💻 فريق العمل: حسين النصار | منار شطناوي | محمد الجراح</p>
  <p>© 2026 - جميع الحقوق محفوظة - جامعة إربد الأهلية</p>
</div>
""", unsafe_allow_html=True)
