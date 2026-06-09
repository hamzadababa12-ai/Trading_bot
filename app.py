import streamlit as st
import requests
from PIL import Image
import io
import base64

# إعدادات واجهة التطبيق
st.set_page_config(page_title="SMC & ICT Trading Bot", page_icon="📊", layout="centered")

# عنوان التطبيق الرئيسي
st.title("🛡️ نظام التحليل الذكي | SMC & ICT")
st.subheader("تطبيق التداول الخاص بك")
st.markdown("---")

# مفتاح الـ API الخاص بك من OpenRouter تم وضعه هنا مباشرة
OPENROUTER_API_KEY = "Sk-or-v1-11ea0c3e43370b5878ce9ec4a82cc62097b46b27c52141f21cbdb9a5b09fb8ad"

# أزرار الخيارات لتحديد نوع السوق
st.markdown("### 1️⃣ اختر سوق التداول الحالي:")
market_type = st.radio(
    "نوع السوق المستهدف:",
    ["سوق الذهب والفضة (XAUUSD / XAGUSD)", "أزواج العملات الأجنبية (Forex)", "أسواق خارج البورصة (OTC)"],
    index=0
)

# خيارات استراتيجية التحليل المفضلة
st.markdown("### 2️⃣ اختر الإستراتيجية الأساسية للتأكيد:")
strategy_type = st.selectbox(
    "إستراتيجية التحليل المعتمدة:",
    ["دمج SMC + ICT (المفضل)", "Order Blocks & FVG فقط", "المتوسطات المتحركة + RSI + Price Action"]
)

# رفع صورة الشارت من الهاتف
st.markdown("### 3️⃣ ارفع لقطة شاشة للشارت (Screenshot):")
uploaded_file = st.file_uploader("اضغط هنا لرفع الصورة...", type=["jpg", "jpeg", "png"])

# البرومبت الاحترافي الصارم
PROMPT_TEMPLATE = f"""
أنت متداول محترف ومحلل مالي عبقري متخصص في خوارزميات أسواق المال وصناعة السوق. 
أمامك صورة شارت خاصة بـ ({market_type})، والمطلوب منك تحليلها بناءً على إستراتيجية ({strategy_type}).

قم بفحص الشارت بدقة فائقة واستخرج الآتي:
1. بنية السوق الحالية (Market Structure) وتحديد نقاط الـ BOS و CHoCH.
2. تحديد الفجوات السعرية العادلة Fair Value Gaps (FVG) ومناطق الـ Order Blocks (OB) غير الملموسة.
3. دمج مؤشرات الزخم (RSI) والمتوسطات المتحركة (Moving Averages) إذا كانت ظاهرة لتأكيد الدخول.

⚠️ شروط صارمة جداً:
- ممنوع منعاً باتاً إعطاء منطقة محايدة أو قول 'السوق غير واضح'.
- يجب أن تختار قراراً حتمياً بناءً على الاحتمالية الأعلى: إما (شراء BUY) أو (بيع SELL).
- يجب تحديد نقاط رقمية دقيقة أو واضحة بناءً على معطيات الشارت.

صغ النتيجة باللغة العربية بتنسيق احترافي كالتالي:
🚨 القرار النهائي: [شراء صريح / بيع صريح]
🎯 نقطة الدخول المفضلة (Entry Zone): [حدد السعر أو المنطقة]
💰 أهداف جني الأرباح (Take Profit):
   - الهدف الأول: 
   - الهدف الثاني: 
🛑 وقف الخسارة الصارم (Stop Loss): [نقطة الستوب لحماية الحساب]
📊 الأسباب الفنية والدوافع: [اشرح باختصار لماذا اخترت هذا القرار بناءً على السيولة والـ FVG والـ OB]
"""

# دالة لتحويل الصورة إلى صيغة Base64 لإرسالها لـ OpenRouter
def encode_image(uploaded_file):
    return base64.b64encode(uploaded_file.getvalue()).decode('utf-8')

# زر بدء التحليل
if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="📸 لقطة الشارت التي تم رفعها", use_container_width=True)
    
    st.markdown("---")
    if st.button("🚀 ابدأ تحليل الشارت الآن وإعطاء الإشارة"):
        with st.spinner("🔄 جاري إرسال الشارت وتحليل السيولة عبر OpenRouter... انتظر لحظة"):
            try:
                base64_image = encode_image(uploaded_file)
                
                # الاتصال بـ OpenRouter واستدعاء نموذج قراءة الصور المتطور
                headers = {
                    "Authorization": f"Bearer {OPENROUTER_API_KEY}",
                    "Content-Type": "application/json"
                }
                
                # سنستخدم نموذج جوجل الفلاش السريع والقوي في قراءة الصور عبر OpenRouter
                data = {
                    "model": "google/gemini-2.5-flash", 
                    "messages": [
                        {
                            "role": "user",
                            "content": [
                                {"type": "text", "text": PROMPT_TEMPLATE},
                                {
                                    "type": "image_url",
                                    "image_url": {
                                        "url": f"data:image/jpeg;base64,{base64_image}"
                                    }
                                }
                            ]
                        }
                    ]
                }
                
                response = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, json=data)
                result = response.json()
                
                if "choices" in result:
                    analysis_text = result["choices"][0]["message"]["content"]
                    st.success("✅ تم الانتهاء من التحليل بنجاح!")
                    st.markdown("### 📋 تقرير الإشارة والتحليل الفني:")
                    st.markdown(analysis_text)
                else:
                    st.error(f"❌ فشل التحليل. تأكد من وجود رصيد في حسابك على OpenRouter. تفاصيل: {result}")
                    
            except Exception as e:
                st.error(f"❌ حدث خطأ أثناء الاتصال بالخادم الفني. تفاصيل الخطأ: {e}")
