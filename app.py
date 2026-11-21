import streamlit as st
import pandas as pd
import json
import os
import random
st.set_option("client.toolbarMode", "minimal")
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
st.set_page_config(page_title="شيف تكة تركة الذكي", page_icon="🥘", layout="centered")
# استيراد الردود من ملفك الخاص
from chat_history import (
    greetings_pool, help_pool, how_are_you_pool, identity_pool,
    ingredients_pool, learn_cooking_pool, cooking_tips_pool,
    suggest_recipe_pool, fast_food_pool, storage_pool
)

# ==========================================
# 1. إعدادات الصفحة الأساسية
# ==========================================
st.set_page_config(page_title="شيف تكة تركة الذكي", page_icon="🥘", layout="centered")

# ==========================================
# 2. التصميم والألوان (أخضر وأبيض - RTL)
# ==========================================
st.markdown("""
<style>
    /* 1. الخلفية الخضراء الفاتحة (نفس لون الصورة) */
    .stApp {
        background-color: #D4EDDA !important; /* لون أخضر فاتح جداً ومريح */
        direction: rtl !important;
        text-align: right !important;
    }

    /* 2. تثبيت لون خانة الإدخال (البحث) لتكون بيضاء دائماً */
    .stTextInput > div > div > input, .stTextArea > div > div > textarea {
        background-color: #FFFFFF !important; /* خلفية بيضاء */
        color: #000000 !important;            /* لون النص أسود */
        border: 2px solid #388E3C !important; /* إطار أخضر غامق */
        border-radius: 10px !important;
        direction: rtl !important;
        text-align: right !important;
    }

    /* 3. تثبيت لون الأزرار (ابحث الآن / بحث جديد) */
    .stButton > button {
        background-color: #FFFFFF !important; /* خلفية بيضاء */
        color: #1E5128 !important;            /* لون النص أخضر غامق */
        border: 2px solid #4CAF50 !important; /* إطار أخضر */
        border-radius: 10px !important;
        font-weight: bold !important;
        width: 100%;
        padding: 10px !important;
        transition: all 0.3s ease;
    }

    /* 4. تأثير عند تمرير الماوس على الأزرار */
    .stButton > button:hover {
        background-color: #4CAF50 !important; /* تتحول لأخضر لما تقف عليها */
        color: #FFFFFF !important;            /* والنص يبقى أبيض */
        border: 2px solid #388E3C !important;
    }

    /* 5. إصلاح أي نصوص أو عناوين عشان تبان */
    p, span, div, label, h1, h2, h3, h4, .stMarkdown {
        color: #1E5128 !important; /* نص بلون أخضر غامق عشان يبان على الخلفية الفاتحة */
        direction: rtl !important;
        text-align: right !important;
    }

    /* 6. لوحة التحكم (الكروت الخاصة بالوصفات) */
    .card {
        background-color: #FFFFFF !important;
        padding: 25px;
        border-radius: 15px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        margin-bottom: 20px;
        border-right: 6px solid #388E3C !important; /* شريط جانبي أخضر */
        direction: rtl !important;
        text-align: right !important;
    }

    /* 7. لون عنوان الوصفة داخل الكارت */
    .recipe-title {
        color: #2E7D32 !important; /* أخضر غامق */
        font-size: 22px;
        font-weight: bold;
        margin-bottom: 10px;
    }


/* تنسيق العنوان الرئيسي (كبير جداً) */
.header-title-main { 
    font-size: 36px !important; /* حجم خط كبير جداً */
    font-weight: 900 !important; 
    margin-bottom: 15px !important; 
    color: white !important; 
    text-shadow: 2px 2px 4px rgba(0,0,0,0.2); /* ظل خفيف عشان يبرز */
}

/* تنسيق العنوان الفرعي (أصغر شوية من الرئيسي) */
.header-title-sub { 
    font-size: 22px !important; /* حجم خط متوسط وكبير */
    font-weight: bold !important;
    margin-bottom: 20px !important; 
    color:SeaGreen!important; 
    opacity: 0.95;
}
/* إخفاء أيقونة GitHub والقلم من الشريط العلوي */
.stAppToolbar a[href*="github.com"], 
.stAppToolbar button[aria-label="Edit"], 
.stAppToolbar [data-testid="stAppViewBlockContainer"] button[kind="header"] {
    display: none !important;
}


</style>
""", unsafe_allow_html=True)



# ==========================================
# 3. دالة الردود الذكية (تربط بملف chat_history)
# ==========================================
def get_smart_response(user_text):
    text_lower = user_text.lower()
    
    # الترحيب
    if any(w in text_lower for w in ["مرحب", "مرحبا", "مرحبتين", "هلا", "أهلاً", "ازيك", "كيف حالك", "صباح", "مساء"]):
        return random.choice(greetings_pool)
    # كيف الحال
    elif any(w in text_lower for w in ["كيف الحال", "كيف", "كيف اخبارك", "كيف الصحة", "أخبارك", "عامل شنو"]):
        return random.choice(how_are_you_pool)
    # التعريف بالنفس
    elif any(w in text_lower for w in ["من انت", "مين انت", "اسمك", "عرفني"]):
        return random.choice(identity_pool)
    # المساعدة
    elif any(w in text_lower for w in ["مساعدة", "خدماتك", "ساعد", "تعمل شنو"]):
        return random.choice(help_pool)
    # المكونات
    elif any(w in text_lower for w in ["عندي", "الثلاجة", "مكونات", "لحمة", "دجاج", "بامية", "بصل", "بطاطس"]):
        return random.choice(ingredients_pool)
    # تعلم الطبخ
    elif any(w in text_lower for w in ["أتعلم الطبخ", "أساسيات الطبخ", "فن الطبخ", "علمني الطبخ", "مبتدئ"]):
        return random.choice(learn_cooking_pool)
    # نصائح طبخ
    elif any(w in text_lower for w in ["نصيحة طبخ"]):
        return random.choice(cooking_tips_pool)
    # اقتراح وصفات
    elif any(w in text_lower for w in ["اقترح لي", "رشح لي", "على ذوقك", "أكلة على ذوقك", "ناكل شنو", "اطبخ شنو"]):
        return random.choice(suggest_recipe_pool)
    # أكل سريع
    elif any(w in text_lower for w in ["سريع", "مستعجل", "وجبة سريعة"]):
        return random.choice(fast_food_pool)
    # تخزين
    elif any(w in text_lower for w in ["تخزين", "حفظ", "الثلاجة"]):
        return random.choice(storage_pool)
    
    # رد افتراضي لو ملقاش حاجة
    else:
        return f"معلش يا شيف، مش متأكد من ({user_text}). ممكن تسألني عن وصفة معينة، أو مكونات عندك، أو تطلب نصيحة طبخ! 🥘"

# ==========================================
# 4. تحميل البيانات (ملف recipes.json)
# ==========================================
try:
    with open("recipes.json", "r", encoding="utf-8") as f:
        data = json.load(f)
    if isinstance(data, dict) and "recipes" in data:
        df = pd.DataFrame(data["recipes"])
    else:
        df = pd.DataFrame(data)
except FileNotFoundError:
    st.error("⚠️ خطأ: لم يتم العثور على ملف recipes.json. تأكد من وجوده في نفس المجلد.")
    st.stop()

# ==========================================
# 5. إعداد ذاكرة الدردشة
# ==========================================
if "messages" not in st.session_state:
    st.session_state.messages = [{
        "role": "assistant",
        "content": ("مرحباً بك في شيف تكة تركة الذكي! 🥘🍔🧑🍳\n""أنا مساعدك الذكي في المطبخ أسالني عن مكون او وصفة سودانية,حابب تاكل شنوا كدي خليني اساعدك🍜🍵,نبدا الدردشة اسالني عن الطبخ 🍝🍩🍰\n\n"" ويمكننا الدردشة معاً وكأننا صديق طبخ! 🍰👨")
    }]

# ==========================================
# 6. بناء واجهة المستخدم
# ==========================================

# الهيدر / الترويسة العلوية (مطابق للصورة اللي بعتها)
st.markdown("""
<div class="header-container">
    <div class="header-title-main">👨🍵 شيف تكة تركة الذكي 🥘</div>
    <div class="header-title-sub">أنا شيف تكة الذكي 🍜🥙🧑 مساعدك الذكي في المطبخ</div>
    <div class="header-list">
        عن طريق الخيارات يمكنني مساعدتك:<br>
        🍝🍴 تجهيز وصفة حسب اسم الوصفة<br>
        🍆🍏🍒 بحث عن طريق المكونات الموجودة<br>
        👨🍜 ويمكننا الدردشة معاً وكأننا صديق طبخ<br>
        مرحباً بك! 🥞🍔🥙🧆🍝🍛 🍜🍤🍩🍰🍵
    </div>
</div>
""", unsafe_allow_html=True)

# ==========================================
# 1. لوحة التحكم
# ==========================================
st.markdown('### ⚙️ لوحة التحكم وخيارات البحث')

# ==========================================
# 2. التحكم في الوقت والمستوى
# ==========================================
col1, col2 = st.columns(2)

with col1:
    max_time = 120
    if "prep_time" in df.columns:
        df["prep_time"] = pd.to_numeric(df["prep_time"], errors='coerce').fillna(0)
        max_time = int(df["prep_time"].max()) if df["prep_time"].max() > 0 else 120
        time_filter = st.slider("⏱️ أقصى زمن للتحضير (دقيقة)", 5, max_time, 60)
    else:
        time_filter = None

with col2:
    if "difficulty" in df.columns:
        difficulty_options = ["الكل"] + list(df["difficulty"].dropna().unique())
        difficulty_filter = st.selectbox("📊 الصعوبة", difficulty_options, key="diff_filter")
    else:
        difficulty_filter = "الكل"

st.markdown("---") # خط فاصل

# ==========================================
# 3. اختيار النمط (التبويبات المتباعدة)
# ==========================================
search_mode = st.radio(
    "اختار النمط:", 
    (
        "بحث بالمكونات🍏🍒", 
        "بحث باسم الوصفة🧆", 
        "دردشة الشيف👨🍴"
    ),
    horizontal=True,
    key="top_nav_mode",
    label_visibility="collapsed" # نخفي كلمة "اختار النمط" عشان التصميم
)

st.markdown("<br>", unsafe_allow_html=True) # مسافة صغيرة

# ==========================================
# 4. واجهة الاستخدام (حسب الاختيار)
# ==========================================

# --- البحث بالمكونات ---
if search_mode == "بحث بالمكونات🍏🍒":
    st.markdown("### 🔍 ابحث بالمكونات المتوفرة لديك")
    user_input_ing = st.text_input("اكتب المكونات (مثال: بصل، طماطم، لحمة):", key="ing_search_input")
    
    if st.button("🚀 ابحث عن وصفة", key="search_ing_btn"):
        if not user_input_ing.strip():
            st.warning("⚠️ يرجى إدخال المكونات أولاً!")
        else:
            filtered_df = df.copy()
            if time_filter and "prep_time" in filtered_df.columns:
                filtered_df = filtered_df[filtered_df["prep_time"] <= time_filter]
            if difficulty_filter != "الكل" and "difficulty" in filtered_df.columns:
                filtered_df = filtered_df[filtered_df["difficulty"] == difficulty_filter]

            if filtered_df.empty:
                st.warning("⚠️ لا توجد وصفات تطابق الفلاتر.")
            else:
                vectorizer = TfidfVectorizer(token_pattern=r'\b\w+\b')
                target_column = filtered_df["ingredients"].fillna("")
                X = vectorizer.fit_transform(target_column)
                user_vec = vectorizer.transform([user_input_ing])
                similarity = cosine_similarity(user_vec, X)
                idx = similarity[0].argmax()

                if similarity[0][idx] > 0.01:
                    r = filtered_df.iloc[idx]
                    st.markdown(
                        f"""
                        <div class='card'>
                            <div class='recipe-title'>🍽️ {r.get('name', 'وصفة')}</div>
                            <p><b>المكونات:</b> {r.get('ingredients', 'غير متوفرة')}</p>
                            <p><b>الخطوات:</b><br>{str(r.get('steps', 'غير متوفرة')).replace('.', '.<br>')}</p>
                            <p>⏱️ <b>زمن التحضير:</b> {r.get('prep_time', 'غير محدد')} دقيقة</p>
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )
                    st.success("👨🍳 بالهناء والشفاء! 🍴")
                else:
                    st.warning("🔍 لا توجد وصفة مطابقة.")

# --- البحث باسم الوصفة ---
elif search_mode == "بحث باسم الوصفة🧆":
    st.markdown("### 🔍 ابحث باسم الوصفة")
    user_input_name = st.text_input("اكتب اسم الوصفة (مثال: شكشوكة، ملاح بامية):", key="name_search_input")
    
    if st.button("🚀 ابحث الآن", key="search_name_btn"):
        if not user_input_name.strip():
            st.warning("⚠️ يرجى إدخال اسم الوصفة أولاً!")
        else:
            filtered_df = df.copy()
            if time_filter and "prep_time" in filtered_df.columns:
                filtered_df = filtered_df[filtered_df["prep_time"] <= time_filter]
            if difficulty_filter != "الكل" and "difficulty" in filtered_df.columns:
                filtered_df = filtered_df[filtered_df["difficulty"] == difficulty_filter]

            if filtered_df.empty:
                st.warning("⚠️ لا توجد وصفات تطابق الفلاتر.")
            else:
                vectorizer = TfidfVectorizer(token_pattern=r'\b\w+\b')
                target_column = filtered_df["name"].fillna("")
                X = vectorizer.fit_transform(target_column)
                user_vec = vectorizer.transform([user_input_name])
                similarity = cosine_similarity(user_vec, X)
                idx = similarity[0].argmax()

                if similarity[0][idx] > 0.01:
                    r = filtered_df.iloc[idx]
                    st.markdown(
                        f"""
                        <div class='card'>
                            <div class='recipe-title'>🍽️ {r.get('name', 'وصفة')}</div>
                            <p><b>المكونات:</b> {r.get('ingredients', 'غير متوفرة')}</p>
                            <p><b>الخطوات:</b><br>{str(r.get('steps', 'غير متوفرة')).replace('.', '.<br>')}</p>
                            <p>⏱️ <b>زمن التحضير:</b> {r.get('prep_time', 'غير محدد')} دقيقة</p>
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )
                    st.success("👨🍳 بالهناء والشفاء! 🍴")
                else:
                    st.warning("🔍 لا توجد وصفة مطابقة.")

# --- دردشة الشيف ---
elif search_mode == "دردشة الشيف👨🍴":
    st.markdown("### 💬 دردشة تفاعلية مع الشيف")
    
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if user_chat_input := st.chat_input("اكتب سؤالك هنا..."):
        st.session_state.messages.append({"role": "user", "content": user_chat_input})
        with st.chat_message("user"):
            st.markdown(user_chat_input)
        
        with st.chat_message("assistant"):
            ai_response = get_smart_response(user_chat_input)
            st.markdown(ai_response)
            st.session_state.messages.append({"role": "assistant", "content": ai_response})

# زرار البحث الجديد
st.markdown("---")
if st.button("🔄 بحث جديد", key="reset_search"):
    st.rerun()

