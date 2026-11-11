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

# إعداد الصفحة وتوجيه النص من اليمين لليسار (RTL)
st.set_page_config(
    page_title="شيف نانو - مساعدك الذكي في المطبخ", page_icon="🍳", layout="centered"
)

# تصميم الواجهة بالألوان الدافئة واتجاه اليمين لليسار
st.markdown(
    """
<style>
    .stApp {
        background: linear-gradient(135deg, #FFF5EC 0%, #FEEBE2 50%, #FCE4D6 100%);
        color: #2D3748;
        direction: rtl;
        text-align: right;
    }
    [data-testid="stSidebar"] {
        background-color: #ffffff !important;
        border-right: 1px solid #fed7aa;
        direction: rtl;
        text-align: right;
    }
    .header-box {
        background: linear-gradient(135deg, #FF7A00 0%, #FF4D00 100%);
        padding: 25px;
        border-radius: 20px;
        color: white;
        text-align: center;
        box-shadow: 0 8px 20px rgba(255, 122, 0, 0.2);
        margin-bottom: 25px;
    }
    .header-title {
        font-size: 28px;
        font-weight: bold;
        margin-bottom: 8px;
    }
    .header-sub {
        font-size: 14px;
        opacity: 0.9;
    }
    .card {
        background-color: #ffffff;
        padding: 25px;
        border-radius: 18px;
        box-shadow: 0 4px 15px rgba(255, 100, 0, 0.08);
        margin-bottom: 20px;
        border-right: 6px solid #FF7A00;
        direction: rtl;
        text-align: right;
    }
    .recipe-title {
        color: #C2410C;
        font-size: 24px;
        font-weight: bold;
        margin-bottom: 15px;
    }
    p, span, div, label, h3 {
        direction: rtl;
        text-align: right;
    }
</style>
""",
    unsafe_allow_html=True,
)

# الترويسة العلوية المطابقة للتصميم المطلوب
st.markdown(
    """
    <div class="header-box">
        <div class="header-title">👨🍳 شيف نانو - مساعدك الذكي في المطبخ</div>
        <div class="header-sub">مساعدك الذكي لتحضير وصفات لذيذة • خطوات سهلة • نصائح فورية</div>
    </div>
""",
    unsafe_allow_html=True,
)


# دالة ذكية لفهم المرادفات وتوزيع الأسئلة على القوائم بدقة
def get_smart_response(user_text):
  text_lower = user_text.lower()

  # 1. كيف الحال والأخبار
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

  # 2. تعلم الطبخ والأساسيات
  elif any(
      w in text_lower
      for w in [
          "أتعلم الطبخ",
          "أساسيات الطبخ",
          "فن الطبخ",
          "أعلمني الطبخ",
          "مبتدئ",
          " عايزا اتعلم الطبيخ",
          "عايزا اعرف الطبخ",
          "حابة اتعلم الطبيخ",
          "عايزا اعرف اساسيات الطبخ",
          "علمني كيف اطبخ",
          "كيف اقدراطبخ",
          "علمني الطبيخ",
          "كيف اطبخ",
          "عايزا اطبخ",

      ]
  ):
    return random.choice(learn_cooking_pool)

  # 3. طلب نصيحة طبخ
  elif any(
      w in text_lower for w in ["نصيحة طبخ", "نصيحة للمطبخ", "أعطيني نصيحة"]
  ):
    return random.choice(cooking_tips_pool)

  # 4. اقترح لي وصفة / على ذوقك
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

  # 5. الترحيب العام
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

  # 6. الهوية والتعريف
  elif any(
      w in text_lower
      for w in ["من انت", "مين انت", "اسمك", "تعريف", "عرفني", "شيف", "نانو"]
  ):
    return random.choice(identity_pool)

  # 7. المساعدة
  elif any(
      w in text_lower
      for w in ["تساعد", "خدماتك", "مساعدة", "تقدر تسوي", "شنو", "عمل شنو"]
  ):
    return random.choice(help_pool)

  # 8. مكونات الثلاجة
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

  # 9. طلب الوصفات وطريقة الطبخ
  elif any(
      w in text_lower for w in ["طريقة", "كيف أعمل", "كيف أطبخ", "وصفة", "أريد طبخ"]
  ):
    return random.choice(recipe_request_pool)

  # 10. الأكل الباظ وإصلاحه
  elif any(
      w in text_lower
      for w in ["باظ", "حرق", "ملح", "خرب", "إصلاح", "معجن", "حامض"]
  ):
    return random.choice(fix_food_pool)

  # 11. الدايت والسعرات
  elif any(
      w in text_lower for w in ["دايت", "سعرات", "صحي", "رجيم", "وزن", "بروتين"]
  ):
    return random.choice(diet_pool)

  # 12. الجدول الأسبوعي
  elif any(w in text_lower for w in ["جدول", "أسبوعي", "فطور وغدا", "تخطيط"]):
    return random.choice(weekly_plan_pool)

  # 13. البدائل
  elif any(
      w in text_lower for w in ["بديل", "مافي", "بدون", "لا توجد", "مفروش"]
  ):
    return random.choice(substitutes_pool)

  # 14. العزومات
  elif any(w in text_lower for w in ["عزومة", "عزومات", "ضيوف", "مفاجئين"]):
    return random.choice(عزومات_pool)

  # 15. الأكل المستعجل
  elif any(w in text_lower for w in ["سريع", "مستعجل", "بسرعة", "دقايق"]):
    return random.choice(fast_food_pool)

  # 16. التخزين
  elif any(w in text_lower for w in ["تخزين", "حفظ", "فريزر", "تفريز"]):
    return random.choice(storage_pool)

  # 17. العصويات والحلويات
  elif any(
      w in text_lower for w in ["عصير", "كركديه", "حلويات", "مديدة", "حلو"]
  ):
    return random.choice(sweets_drinks_pool)

  # 18. المقادير
  elif any(w in text_lower for w in ["مقادير", "قياس", "كوب", "جرام", "ملعقة"]):
    return random.choice(measurements_pool)

  # 19. الأسئلة الخارجية
  elif any(
      w in text_lower
      for w in ["سياسة", "كورة", "تاريخ", "رياضة", "برمجة", "فيزياء"]
  ):
    return random.choice(outside_pool)

  # الرد الافتراضي
  else:
    return (
        f"يا زول ابشر! بالنسبة لطلبك ({user_text})، اقترح علي مكونات متاحة أو"
        " اكتب اسم الوصفة وسأساعدك فوراً بتكة وتظبط!"
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

# القائمة الجانبية
st.sidebar.header("⚙️ خيارات التصفية والتحكم")
search_mode = st.sidebar.radio(
    "اختر نمط البحث:",
    (
        "البحث بالمكونات المتوفرة",
        "البحث باسم الوصفة",
        "دردشة الشيف الذكي 🤖",
    ),
    key="sidebar_mode_final_v4",
)

max_time = 120
if "prep_time" in df.columns:
  df["prep_time"] = pd.to_numeric(df["prep_time"], errors="coerce").fillna(60)
  max_time = int(df["prep_time"].max())
  time_filter = st.sidebar.slider(
      "⏱️ الحد الأقصى لوقت التحضير (بالدقائق)",
      5,
      max_time,
      max_time,
      key="time_slider_final_v4",
  )
else:
  time_filter = None

if "difficulty" in df.columns:
  difficulty_options = ["الكل"] + list(df["difficulty"].dropna().unique())
  difficulty_filter = st.sidebar.selectbox(
      "📊 مستوى صعوبة الوصفة",
      difficulty_options,
      key="difficulty_box_final_v4",
  )
else:
  difficulty_filter = "الكل"

if st.sidebar.button("🗑️ مسح ذاكرة الدردشة", key="clear_chat_btn_final_v4"):
  st.session_state.messages = [{
      "role": "assistant",
      "content": "تم مسح الذاكرة بنجاح! أنا جاهز من جديد 🍽️.",
  }]
  st.rerun()

# واجهة الاستخدام الرئيسية (الشات أو البحث)
if search_mode == "دردشة الشيف الذكي 🤖":
  st.markdown("### 💬 دردشة تفاعلية مع الشيف")

  for message in st.session_state.messages:
    with st.chat_message(message["role"]):
      st.markdown(message["content"])

  if user_chat_input := st.chat_input(
      "اكتب سؤالك الآن... مثل: كيف أعد دجاج بالكاري بطريقة سهلة؟",
      key="main_chat_input_final_v4",
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
        "🍳 ما هي المكونات المتوفرة لديك؟", key="ingredients_input_final_v4"
    )
  else:
    user_input = st.text_input(
        "🔍 ما هي الوصفة التي تبحث عنها؟", key="recipe_name_input_final_v4"
    )

  if st.button("🚀 ابحث الآن", key="search_exec_btn_final_v4"):
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
              "🔍 اسف  الوصفة دي ما وقعت لي . ممكن تدخل مكونات اخري."
          )

  if st.button("🔄 بحث جديد", key="reset_search_btn_final_v4"):
    st.rerun()

