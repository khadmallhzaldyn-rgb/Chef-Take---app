from chat_history import (
    cooking_tips_pool,
    diet_pool,
    fast_food_pool,
    fix_food_pool,
    greetings_pool,
    help_pool,
    how_are_you_pool,
    identity_pool,
    ingredients_pool,
    learn_cooking_pool,
    measurements_pool,
    outside_pool,
    recipe_request_pool,
    storage_pool,
    substitutes_pool,
    suggest_recipe_pool,
    sweets_drinks_pool,
    weekly_plan_pool,
    عزومات_pool,
)
import json
import os
import random
import pandas as pd
import streamlit as st

# إعداد الصفحة وتوجيه النص من اليمين لليسار (RTL) مع إخفاء القائمة الجانبية وأيقونات الـ GitHub والقلم العلوية
st.set_page_config(
    page_title="شيف نانو - مساعدك الذكي في المطبخ", page_icon="🍳", layout="centered"
)

st.markdown(
    """
<style>
    /* إخفاء شريط أدوات Streamlit العلوي (أيقونة GitHub، القلم، المشاركة) */
    #MainMenu {visibility: hidden;}
    header {visibility: hidden;}
    footer {visibility: hidden;}
    
    .stApp {
        background: linear-gradient(135deg, #FFF5EC 0%, #FEEBE2 50%, #FCE4D6 100%);
        color: #2D3748;
        direction: rtl;
        text-align: right;
    }
    .header-box {
        background: linear-gradient(135deg, #FF7A00 0%, #FF4D00 100%);
        padding: 20px;
        border-radius: 20px;
        color: white;
        text-align: center;
        box-shadow: 0 8px 20px rgba(255, 122, 0, 0.2);
        margin-bottom: 20px;
    }
    .header-title {
        font-size: 24px;
        font-weight: bold;
        margin-bottom: 5px;
    }
    .header-sub {
        font-size: 13px;
        opacity: 0.9;
    }
    .card {
        background-color: #ffffff;
        padding: 20px;
        border-radius: 18px;
        box-shadow: 0 4px 15px rgba(255, 100, 0, 0.08);
        margin-bottom: 15px;
        border-right: 6px solid #FF7A00;
        direction: rtl;
        text-align: right;
    }
    .recipe-title {
        color: #C2410C;
        font-size: 22px;
        font-weight: bold;
        margin-bottom: 10px;
    }
    p, span, div, label, h3 {
        direction: rtl;
        text-align: right;
    }
</style>
""",
    unsafe_allow_html=True,
)

# الترويسة العلوية
st.markdown(
    """
    <div class="header-box">
        <div class="header-title">👨🍳 شيف نانو - مساعدك الذكي في المطبخ</div>
        <div class="header-sub">مساعدك الذكي لتحضير وصفات لذيذة • خطوات سهلة • نصائح فورية</div>
    </div>
""",
    unsafe_allow_html=True,
)


# دالة الردود الذكية
def get_smart_response(user_text):
  text_lower = user_text.lower()
  if any(
      w in text_lower
      for w in [
          "كيف الحال",
          "كيفك",
          "كيف اخبارك",
          "كيف الصحة",
          "أخبارك",
          "عامل شنو",
      ]
  ):
    return random.choice(how_are_you_pool)
  elif any(
      w in text_lower
      for w in [
          "أتعلم الطبخ",
          "أساسيات الطبخ",
          "فن الطبخ",
          "أعلمني الطبخ",
          "مبتدئ",

          "عايزا أتعلم الطبخ",
          " علمني الطبخ",
          "عايزا اعرف الطبخ",
          "وريني كيف اطبخ",
          "عايزا اعرف الطبيخ ",
      ]
  ):
    return random.choice(learn_cooking_pool)
  elif any(
      w in text_lower for w in ["نصيحة طبخ", "نصيحة للمطبخ", "أعطيني نصيحة"]
  ):
    return random.choice(cooking_tips_pool)
  elif any(
      w in text_lower
      for w in [
          "اقترح لي",
          "رشح لي",
          "على ذوقك",
          "أكلة على ذوقك",
          "ناكل شنو",
          "اطبخ شنو",
      ]
  ):
    return random.choice(suggest_recipe_pool)
  elif any(
      w in text_lower
      for w in [
          "مرحب",
          "مرحبا",
          "مرحبتين",
          "هلا",
          "أهلاً",
          "ازيك",
          "كيف حالك",
          "صباح",
          "مساء",
      ]
  ):
    return random.choice(greetings_pool)
  elif any(
      w in text_lower
      for w in ["من انت", "مين انت", "اسمك", "تعريف", "عرفني", "شيف", "نانو"]
  ):
    return random.choice(identity_pool)
  elif any(
      w in text_lower
      for w in ["تساعد", "خدماتك", "مساعدة", "تقدر تسوي", "شنو", "عمل شنو"]
  ):
    return random.choice(help_pool)
  elif any(
      w in text_lower
      for w in [
          "عندي",
          "الثلاجة",
          "مكونات",
          "لحمة",
          "دجاج",
          "بامية",
          "بصل",
          "بطاطس",
      ]
  ):
    return random.choice(ingredients_pool)
  elif any(
      w in text_lower for w in ["طريقة", "كيف أعمل", "كيف أطبخ", "وصفة", "أريد طبخ"]
  ):
    return random.choice(recipe_request_pool)
  elif any(
      w in text_lower
      for w in ["باظ", "حرق", "ملح", "خرب", "إصلاح", "معجن", "حامض"]
  ):
    return random.choice(fix_food_pool)
  elif any(
      w in text_lower for w in ["دايت", "سعرات", "صحي", "رجيم", "وزن", "بروتين"]
  ):
    return random.choice(diet_pool)
  elif any(w in text_lower for w in ["جدول", "أسبوعي", "فطور وغدا", "تخطيط"]):
    return random.choice(weekly_plan_pool)
  elif any(
      w in text_lower for w in ["بديل", "مافي", "بدون", "لا توجد", "مفروش"]
  ):
    return random.choice(substitutes_pool)
  elif any(w in text_lower for w in ["عزومة", "عزومات", "ضيوف", "مفاجئين"]):
    return random.choice(عزومات_pool)
  elif any(w in text_lower for w in ["سريع", "مستعجل", "بسرعة", "دقايق"]):
    return random.choice(fast_food_pool)
  elif any(w in text_lower for w in ["تخزين", "حفظ", "فريزر", "تفريز"]):
    return random.choice(storage_pool)
  elif any(
      w in text_lower for w in ["عصير", "كركديه", "حلويات", "مديدة", "حلو"]
  ):
    return random.choice(sweets_drinks_pool)
  elif any(w in text_lower for w in ["مقادير", "قياس", "كوب", "جرام", "ملعقة"]):
    return random.choice(measurements_pool)
  elif any(
      w in text_lower
      for w in ["سياسة", "كورة", "تاريخ", "رياضة", "برمجة", "فيزياء"]
  ):
    return random.choice(outside_pool)
  else:
    return (
        f"معليش بنسبة لي  ({user_text})، اقترح علي مكونات متاحة أو"
        "  ما وقعت في اكتب اسم الوصفة وسأساعدك فوراً بتكة وتظبط!"
    )


# تحميل ملف الوصفات
try:
  with open("recipes.json", "r", encoding="utf-8") as f:
    data = json.load(f)
  if isinstance(data, dict) and "recipes" in data:
    df = pd.DataFrame(data["recipes"])
  else:
    df = pd.DataFrame(data)
except FileNotFoundError:
  st.error("خطأ: لم يتم العثور على ملف recipes.json.")
  st.stop()

# إعداد ذاكرة الدردشة في الـ Session State
if "messages" not in st.session_state:
  st.session_state.messages = [{
      "role": "assistant",
      "content": (
          "أنا شيف نانو، مساعدك الذكي في المطبخ\nكيف يمكنني مساعدتك اليوم؟ اطلب"
          " وصفة، اقترح مكونات متاحة، أو اسأل عن نصيحة طهي - وسأرد عليك فوراً!"
      ),
  }]

# تحويل الخيارات لتكون في أعلى الصفحة (بدلاً من القائمة الجانبية لتناسب الجوالات)
st.markdown("### ⚙️ لوحة التحكم وخيارات البحث")
search_mode = st.radio(
    "اختر النمط:",
    (
        "البحث بالمكونات المتوفرة",
        "البحث باسم الوصفة",
        "دردشة الشيف الذكي 🤖",
    ),
    horizontal=True,
    key="top_nav_mode",
)

# استخدام أعمدة مرتبة للتحكم في الوقت والصعوبة لتظهر بشكل جميل على الموبايل
col1, col2 = st.columns(2)

with col1:
  max_time = 120
  if "prep_time" in df.columns:
    df["prep_time"] = pd.to_numeric(df["prep_time"], errors="coerce").fillna(60)
    max_time = int(df["prep_time"].max())
    time_filter = st.slider(
        "⏱️ أقصى زمن للتحضير (دقيقة)", 5, max_time, max_time, key="time_filter_mob"
    )
  else:
    time_filter = None

with col2:
  if "difficulty" in df.columns:
    difficulty_options = ["الكل"] + list(df["difficulty"].dropna().unique())
    difficulty_filter = st.selectbox(
        "📊 الصعوبة", difficulty_options, key="diff_filter_mob"
    )
  else:
    difficulty_filter = "الكل"

if st.button("🗑️ مسح ذاكرة الدردشة", key="clear_chat_mob"):
  st.session_state.messages = [{
      "role": "assistant",
      "content": "تم مسح الذاكرة بنجاح! أنا جاهز من جديد 🍽️.",
  }]
  st.rerun()

st.markdown("---")

# واجهة الاستخدام الرئيسية (الشات أو البحث)
if search_mode == "دردشة الشيف الذكي 🤖":
  st.markdown("### 💬 دردشة تفاعلية مع الشيف")

  for message in st.session_state.messages:
    with st.chat_message(message["role"]):
      st.markdown(message["content"])

  if user_chat_input := st.chat_input(
      "اكتب سؤالك هنا...", key="main_chat_input_mob"
  ):
    st.session_state.messages.append(
        {"role": "user", "content": user_chat_input}
    )
    with st.chat_message("user"):
      st.markdown(user_chat_input)

    with st.chat_message("assistant"):
      ai_response = get_smart_response(user_chat_input)
      st.markdown(ai_response)
      st.session_state.messages.append(
          {"role": "assistant", "content": ai_response}
      )

else:
  if search_mode == "البحث بالمكونات المتوفرة":
    user_input = st.text_input(
        "🍳 ما هي المكونات المتوفرة لديك؟", key="ingredients_input_mob"
    )
  else:
    user_input = st.text_input(
        "🔍 ما هي الوصفة التي تبحث عنها؟", key="recipe_name_input_mob"
    )

  if st.button("🚀 ابحث الآن", key="search_exec_btn_mob"):
    if not user_input.strip():
      st.warning("⚠️ يرجى إدخال كلمات للبحث أولاً!")
    else:
      filtered_df = df.copy()

      if time_filter and "prep_time" in filtered_df.columns:
        filtered_df = filtered_df[filtered_df["prep_time"] <= time_filter]
      if (
          difficulty_filter != "الكل"
          and "difficulty" in filtered_df.columns
      ):
        filtered_df = filtered_df[
            filtered_df["difficulty"] == difficulty_filter
        ]

      if filtered_df.empty:
        st.warning("⚠️ لا توجد وصفات تطابق خيارات التصفية ☹️")
      else:
        from sklearn.feature_extraction.text import TfidfVectorizer
        from sklearn.metrics.pairwise import cosine_similarity

        vectorizer = TfidfVectorizer()
        if search_mode == "البحث باسم الوصفة":
          target_column = filtered_df["name"].astype(str)
        else:
          target_column = filtered_df["ingredients"].astype(str)

        X = vectorizer.fit_transform(target_column)
        user_vec = vectorizer.transform([user_input])
        similarity = cosine_similarity(user_vec, X)
        idx = similarity[0].argmax()

        if similarity[0][idx] > 0.12:
          r = filtered_df.iloc[idx]
          st.markdown(
              f"""
                    <div class='card'>
                        <div class='recipe-title'>🍽️ {r.get('name', 'وصفة مميزة')}</div>
                        <p><b>المكونات:</b> {r.get('ingredients', '')}</p>
                        <p><b>الخطوات:</b><br>{r.get('steps', '')}</p>
                        <p>⏱️ <b>زمن التحضير:</b> {r.get('prep_time', 'غير محدد')} دقيقة</p>
                    </div>
                """,
              unsafe_allow_html=True,
          )
          st.success("بالهناء والشفاء! 👩🍳")
        else:
          st.warning(
              "🔍 عذراً، لم أجد وصفة مطابقة تماماً. حاول إدخال مكونات أخرى."
          )

  if st.button("🔄 بحث جديد", key="reset_search_btn_mob"):
    st.rerun()

