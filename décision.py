import streamlit as st
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import arabic_reshaper
from bidi.algorithm import get_display
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import accuracy_score

st.markdown(
    "<h1 style='color: blue;'>الحملات التسويقية</h1>",
    unsafe_allow_html=True
)
# 🔹 1. ضبط اتجاه النصوص في Streamlit
st.markdown(
    """
    <style>
    * {
        direction: rtl;
        text-align: right;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# تخصيص الألوان
st.markdown("""
    <style>
    body {
        background-color: #F0F0F0;  /* خلفية رمادية فاتحة */
        color: #303F9F;  /* نص أزرق داكن */
    }
    h1, h2, h3, h4, h5, h6 {  /* تخصيص الألوان للعناوين */
        color: #1976D2;  /* لون أزرق ساطع */
    }
    p {
        color: #90A4AE;  /* لون رمادي داكن للنصوص */
    }
    .stButton>button {
        background-color: #303F9F;  /* زر أزرق داكن */
        color: white;
        font-size: 18px;
    }
    .stTextInput input {
        color: #303F9F;  /* نص المدخلات */
    }
    .stSelectbox select {
        color: #303F9F;  /* نص القوائم المنسدلة */
    }
    .stTextArea textarea {
        color: #303F9F;  /* نص منطقة النص */
    }
    </style>
""", unsafe_allow_html=True)

# 📌 إعداد الخط لدعم العربية
plt.rcParams['font.family'] = 'Arial'
plt.rcParams['axes.unicode_minus'] = False

# 📌 إعداد واجهة التطبيق
st.title("📊 تطبيق الذكاء الاصطناعي لتحليل الحملات التسويقية")
st.write("🔍 أدخل بيانات حملتك التسويقية للحصول على توصيات تعتمد على الذكاء الاصطناعي.")

# 📌 إدخال بيانات الحملة
الميزانية = st.number_input("💰 ميزانية الحملة (الدرهم المغربي):", min_value=1000, max_value=100000, step=500)
القناة = st.selectbox("📡 القناة التسويقية:", ["إعلانات رقمية", "وسائل التواصل", "تلفزيون", "راديو", "بريد إلكتروني"])
الجمهور = st.selectbox("👥 الفئة المستهدفة:", ["18-24", "25-34", "35-44", "45-54", "55+"])
المدة = st.number_input("⏳ مدة الحملة (بالأيام):", min_value=7, max_value=90, step=7)
حالة_السوق = st.selectbox("🌍 حالة السوق:", ["طبيعية", "أزمة كورونا", "أزمة اقتصادية"])

# زر تحليل البيانات - أضفنا هنا زر للتحليل
تحليل_البيانات = st.button("🚀 تحليل البيانات")

# أضفنا منطق شرطي لعرض التحليل فقط عند الضغط على الزر
if تحليل_البيانات:
    
    # 📌 معالجة البيانات
    df = pd.DataFrame({
         "الميزانية": np.random.randint(1000, 50000, 100),
         "القناة": np.random.choice(["إعلانات رقمية", "وسائل التواصل", "تلفزيون", "راديو", "بريد إلكتروني"], 100),
         "الجمهور": np.random.choice(["18-24", "25-34", "35-44", "45-54", "55+"], 100),
         "المدة": np.random.randint(7, 90, 100),
         "حالة_السوق": np.random.choice(["طبيعية", "أزمة كورونا", "أزمة اقتصادية"], 100),
         "النجاح": np.random.choice([0, 1], 100)
    })

    # 📌 ترميز القيم (إنشاء ترميز منفصل لكل عمود)
    le_القناة = LabelEncoder()
    df["القناة"] = le_القناة.fit_transform(df["القناة"])

    le_الجمهور = LabelEncoder()
    df["الجمهور"] = le_الجمهور.fit_transform(df["الجمهور"])

    le_حالة_السوق = LabelEncoder()
    df["حالة_السوق"] = le_حالة_السوق.fit_transform(df["حالة_السوق"])

    # 📌 إعداد البيانات
    X = df[["الميزانية", "القناة", "الجمهور", "المدة", "حالة_السوق"]]
    y = df["النجاح"]
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # 📌 تدريب النموذج
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)

    # 📊 تحليل الميزات
    importances = model.feature_importances_
    importance_df = pd.DataFrame({"الميزة": X.columns, "الأهمية": importances}).sort_values(by="الأهمية", ascending=False)

    # 📈 دقة النموذج
    accuracy = accuracy_score(y_test, model.predict(X_test))
    st.write(f"📈 **دقة النموذج: {accuracy * 100:.2f} في المئة**")

    # 📊 تفسير النتائج
    # التحقق من وجود الفئات الجديدة وإضافتها إذا لزم الأمر
    if القناة not in le_القناة.classes_:
        le_القناة.classes_ = np.append(le_القناة.classes_, القناة)
    if الجمهور not in le_الجمهور.classes_:
        le_الجمهور.classes_ = np.append(le_الجمهور.classes_, الجمهور)
    if حالة_السوق not in le_حالة_السوق.classes_:
        le_حالة_السوق.classes_ = np.append(le_حالة_السوق.classes_, حالة_السوق)

    # التنبؤ
    new_data = pd.DataFrame([[الميزانية, le_القناة.transform([القناة])[0], le_الجمهور.transform([الجمهور])[0], المدة, le_حالة_السوق.transform([حالة_السوق])[0]]],
                            columns=["الميزانية", "القناة", "الجمهور", "المدة", "حالة_السوق"])

    prediction = model.predict(new_data)[0]
    result = "نجاح 🎯" if prediction == 1 else "فشل ⚠️"

    # 📊 تقرير تحليلي شامل
    analysis = f"""
    📊 **تقرير تحليلي شامل حول أداء الحملة التسويقية**  
        
تم إجراء تحليل شامل للحملة التسويقية بناءً على البيانات المتاحة، مع التركيز على الميزانية، القناة التسويقية، الفئة المستهدفة، ومدة الحملة. كما تم أخذ العوامل الخارجية، مثل حالة السوق، بعين الاعتبار لتقديم توقع دقيق للأداء المتوقع.  

💰 **الميزانية والقناة التسويقية:**  
- تم تخصيص ميزانية قدرها **{الميزانية}** درهم للحملة، مما يؤثر بشكل مباشر على مدى الوصول والاستراتيجيات المستخدمة.  
- تم اختيار القناة التسويقية **{القناة}**، والتي تلعب دورًا مهمًا في تحديد فعالية الحملة بناءً على تفاعل الجمهور عبر هذه القناة.  

    🎯 **تحليل الفئة المستهدفة ومدة الحملة:**  
- الفئة المستهدفة هي **{الجمهور}**، مما يعني ضرورة تخصيص المحتوى واستراتيجيات الإعلانات بما يتناسب مع اهتماماتهم وسلوكياتهم.  
- مدة الحملة محددة بـ **{المدة} أيام**، وهو عامل مهم في تحديد مدى تأثير الحملة على تحقيق الأهداف التسويقية.  

    📉 **تأثير حالة السوق على نجاح الحملة:**  
- تم تقييم وضع السوق الحالي على أنه **{حالة_السوق}**، مما قد يؤثر على سلوك المستهلكين واستجابتهم للحملة.  
- في حال كان السوق يعاني من ركود أو تقلبات، قد يكون من المفيد تكييف استراتيجيات التسويق لمواكبة هذه التغيرات.  

    📈 **نتيجة التنبؤ:**  
# وفقًا للتحليل القائم على البيانات الحالية، يُتوقع أن تحقق الحملة **{result}**.  
- هذه النسبة تشير إلى أن الحملة لديها فرصة جيدة للوصول إلى الأهداف المحددة. ومع ذلك، يظل هناك بعض العوامل المتغيرة مثل استجابة الجمهور أو التغيرات في السوق، التي قد تؤثر على النتيجة النهائية.
- بناءً على ذلك، ينبغي متابعة الأداء عن كثب وإجراء التعديلات اللازمة لضمان تحقيق أفضل نتائج.
    

    🔬 **تحليل الميزات المؤثرة على نجاح الحملة:**  
"""

    for index, row in importance_df.iterrows():
        analysis += f"- **{row['الميزة']}**: مستوى تأثيره على النجاح هو **{row['الأهمية']:.2f}**.\n"

    st.write(analysis)

    # إعادة تشكيل النصوص العربية
    importance_df["الميزة"] = importance_df["الميزة"].apply(lambda x: get_display(arabic_reshaper.reshape(x)))

    st.subheader("🔑 أهمية الميزات في اتخاذ القرار")
    fig, ax = plt.subplots()

    # تفعيل دعم اللغة العربية
    plt.rcParams['font.family'] = 'Arial'
    plt.rcParams['axes.unicode_minus'] = False

    # إعادة تشكيل النص العربي ليظهر بشكل صحيح
    title = get_display(arabic_reshaper.reshape("مخطط أهمية الميزات"))
    xlabel = get_display(arabic_reshaper.reshape("الأهمية"))
    ylabel = get_display(arabic_reshaper.reshape("الميزة"))

    # رسم المخطط باستخدام Seaborn
    sns.barplot(x="الأهمية", y="الميزة", data=importance_df, palette="Blues", ax=ax)

    # ضبط عنوان المخطط والعناوين الفرعية
    ax.set_title(title, fontsize=16, fontweight='bold', fontname='Arial', loc='center')
    ax.set_xlabel(xlabel, fontsize=14, fontname='Arial')
    ax.set_ylabel(ylabel, fontsize=14, fontname='Arial')

    # ضبط اتجاه النص على المحاور
    plt.xticks(fontsize=12, fontname='Arial')
    plt.yticks(fontsize=12, fontname='Arial')

    # قلب ترتيب الميزات لعرضها من الأعلى للأسفل
    plt.gca().invert_yaxis()

    st.pyplot(fig)

    # 📝 تحليل مخطط أهمية الميزات
    # إعادة تشكيل النصوص من DataFrame لضمان ظهورها بشكل صحيح
    الميزة_الأكثر_أهمية = get_display(arabic_reshaper.reshape(importance_df.iloc[0]["الميزة"]))
    الميزة_الأقل_أهمية = get_display(arabic_reshaper.reshape(importance_df.iloc[-1]["الميزة"]))

    st.markdown(f"""
        🔍 **تحليل أهمية الميزات في نجاح الحملات التسويقية:**  

    📊 يعكس المخطط أعلاه مدى تأثير كل ميزة على نجاح الحملات، حيث تُظهر البيانات أن **الميزة الأكثر أهمية** هي **{الميزة_الأكثر_أهمية}**.  
    يشير ذلك إلى أن التركيز على تحسين هذه الميزة يمكن أن يعزز أداء الحملات التسويقية بشكل كبير، نظراً لدورها المحوري في جذب الجمهور المستهدف وتحقيق الأهداف التسويقية.  

    🔹 **لماذا هذه الميزة مهمة؟**  
    - تلعب دورًا رئيسيًا في تحفيز تفاعل العملاء وزيادة معدل التحويل.  
    - قد تكون مرتبطة بجودة المحتوى، استهداف الجمهور، أو تجربة المستخدم.  
    - تحسين هذه الميزة قد يؤدي إلى تحسين شامل في أداء الحملة.  

        🧐 **ماذا عن الميزات الأقل أهمية؟**  
    من ناحية أخرى، تُظهر البيانات أن **{الميزة_الأقل_أهمية}** هي الأقل تأثيرًا على نجاح الحملات.  
    هذا لا يعني أنها غير ضرورية، ولكن قد لا يكون الاستثمار الكبير في تحسينها بنفس الفعالية مقارنةً بالميزات الأكثر أهمية.  

        📌 **توصيات بناءً على التحليل:**  
    ✅ **تركيز الجهود على {الميزة_الأكثر_أهمية}** عبر تحسينها واختبار استراتيجيات مختلفة لتعزيز تأثيرها.  
    ✅ **عدم إهمال الميزات الأخرى**، ولكن يمكن إعادة توزيع الموارد بناءً على مدى تأثير كل ميزة.  
    ✅ **تحليل متغيرات أخرى** قد تؤثر على النجاح، مثل التفاعل مع الجمهور وتخصيص المحتوى وفقًا لاحتياجات العملاء.  

        📈 باستخدام هذه البيانات، يمكن توجيه الاستثمارات التسويقية بذكاء لضمان تحقيق أفضل النتائج وتحسين الأداء العام للحملات. 🚀
    """)

    # 📊 رسم العلاقة بين الميزانية والنجاح
    st.subheader("💸 تأثير الميزانية على نجاح الحملة")
    fig2, ax2 = plt.subplots()

    # تفعيل دعم اللغة العربية
    plt.rcParams['font.family'] = 'Arial'
    plt.rcParams['axes.unicode_minus'] = False

    # رسم المخطط مع تعديل التصنيفات
    df["النجاح_المعدل"] = df["النجاح"].map({0: "نجاح", 1: "فشل"}).apply(lambda x: get_display(arabic_reshaper.reshape(x)))
    sns.boxplot(x="النجاح_المعدل", y="الميزانية", data=df, palette="Blues", ax=ax2)

    # إعادة تشكيل النص العربي ليظهر بشكل صحيح
    title = get_display(arabic_reshaper.reshape("تأثير الميزانية على نجاح الحملة"))
    xlabel = get_display(arabic_reshaper.reshape("النجاح"))
    ylabel = get_display(arabic_reshaper.reshape("الميزانية"))

    # ضبط عنوان المخطط والعناوين الفرعية
    ax2.set_title(title, fontsize=16, fontweight='bold', fontname='Arial', loc='center')
    ax2.set_xlabel(xlabel, fontsize=14, fontname='Arial')
    ax2.set_ylabel(ylabel, fontsize=14, fontname='Arial')

    # ضبط اتجاه النص على المحاور
    plt.xticks(fontsize=12, fontname='Arial')
    plt.yticks(fontsize=12, fontname='Arial')

    st.pyplot(fig2)

        # 📝 تحويل القيم الرقمية إلى نصوص
df["النجاح_نصي"] = df["النجاح"].map({1: "فشل", 0: "نجاح"})

    # 📝 تحليل العلاقة بين الميزانية والنجاح
متوسط_ميزانية_النجاح = df[df["النجاح_نصي"] == "نجاح"]["الميزانية"].mean()
متوسط_ميزانية_الفشل = df[df["النجاح_نصي"] == "فشل"]["الميزانية"].mean()

    # 📝 تحليل نجاح الحملات حسب المزانية
st.markdown(f"""
        🔍 **تحليل تأثير الميزانية على نجاح الحملات التسويقية:**  

    📊 من خلال تحليل البيانات، تبين أن **المتوسط التقريبي للميزانية في الحملات الناجحة** يبلغ حوالي **{متوسط_ميزانية_النجاح:.2f} درهم**،  
    بينما **المتوسط التقريبي للميزانية في الحملات غير الناجحة** هو **{متوسط_ميزانية_الفشل:.2f} درهم**.  

    💡 **ما الذي تعنيه هذه الأرقام؟**  
    - يُظهر هذا التحليل أن الحملات ذات الميزانيات الأعلى تميل إلى تحقيق نجاح أكبر، مما يشير إلى وجود علاقة إيجابية بين حجم الميزانية ومستوى الأداء.  
    - قد يكون ذلك بسبب القدرة على الاستثمار في استراتيجيات تسويقية أكثر فعالية، مثل استهداف الجمهور المناسب، واستخدام محتوى عالي الجودة، والاستفادة من الإعلانات المدفوعة بشكل أفضل.  
    - في المقابل، قد تعاني الحملات ذات الميزانيات المنخفضة من ضعف الوصول إلى الجمهور المستهدف أو محدودية الموارد اللازمة لتنفيذ استراتيجيات تسويقية قوية.

        📌 **توصيات عملية بناءً على التحليل:**  
    ✅ **إعادة تقييم توزيع الميزانية:** التركيز على تخصيص موارد كافية للحملات ذات العائد المرتفع.  
    ✅ **تحسين كفاءة الإنفاق:** استخدام أدوات تحليل البيانات لضمان استثمار الميزانية في القنوات والإعلانات الأكثر فاعلية.  
    ✅ **تجربة استراتيجيات مختلفة:** اختبار حملات بميزانيات متدرجة لمعرفة الحد الأدنى الفعّال لتحقيق النجاح.  

        📈 الاستثمار الذكي في التسويق يمكن أن يؤدي إلى تحسين ملحوظ في معدلات النجاح، لذا يُنصح بوضع استراتيجيات مالية مبنية على بيانات دقيقة لضمان تحقيق أقصى استفادة من الميزانية.
    """)

    # 📡 تأثير القناة التسويقية على نجاح الحملة
st.subheader("📡 تأثير القناة التسويقية على نجاح الحملة")
fig3, ax3 = plt.subplots()

    # تفعيل دعم اللغة العربية
plt.rcParams['font.family'] = 'Arial'
plt.rcParams['axes.unicode_minus'] = False

    # إعادة تشكيل النص العربي ليظهر بشكل صحيح
title = get_display(arabic_reshaper.reshape("نجاح الحملات حسب القناة"))
xlabel = get_display(arabic_reshaper.reshape("القناة التسويقية"))
ylabel = get_display(arabic_reshaper.reshape("عدد الحملات"))
legend_title = get_display(arabic_reshaper.reshape("النجاح"))

    # إعادة تشكيل النصوص العربية في القناة والنجاح
df["القناة_المعدلة"] = df["القناة"].map({
    0: "إعلانات رقمية",
    1: "وسائل التواصل",
    2: "تلفزيون",
    3: "راديو",
    4: "بريد إلكتروني"
}).apply(lambda x: get_display(arabic_reshaper.reshape(x)))

    # رسم المخطط مع استخدام الأعمدة المعدلة
sns.countplot(
    data=df,
    x="القناة_المعدلة",
    hue="النجاح_المعدل",
    palette="Blues",
    ax=ax3
)

    # إعادة تشكيل النصوص لعناوين المخطط
ax3.set_title(get_display(arabic_reshaper.reshape("نجاح الحملات حسب القناة")), fontsize=16, fontweight='bold')
ax3.set_xlabel(get_display(arabic_reshaper.reshape("القناة التسويقية")), fontsize=14)
ax3.set_ylabel(get_display(arabic_reshaper.reshape("عدد الحملات")), fontsize=14)

    # إضافة وسيلة الإيضاح
ax3.legend(title=get_display(arabic_reshaper.reshape("النجاح")), fontsize=12, title_fontsize=14, loc="upper right")

    # ضبط إعدادات الخطوط
plt.xticks(fontsize=12)
plt.yticks(fontsize=12)

st.pyplot(fig3)

    # Convert back 'القناة' to categorical for proper ordering
df_for_analysis = df.copy()
df_for_analysis["القناة"] = df_for_analysis["القناة"].map({
    0: "إعلانات رقمية",
    1: "وسائل التواصل",
    2: "تلفزيون",
    3: "راديو",
    4: "بريد إلكتروني"
}).astype("category")

    # ✅ تحويل النجاح إلى نصوص مفهومة
df_for_analysis["النجاح"] = df_for_analysis["النجاح"].map({1: "فشل", 0: "نجاح"})
    # ✅ حساب معدل النجاح الصحيح
معدلات_نجاح_القنوات = df_for_analysis.groupby("القناة")["النجاح"].apply(lambda x: (x == "نجاح").mean()).sort_values(ascending=False)

    # Identify Best & Worst Channels
أفضل_قناة = معدلات_نجاح_القنوات.idxmax()
معدل_نجاح_أفضل_قناة = معدلات_نجاح_القنوات.max() * 100
أسوأ_قناة = معدلات_نجاح_القنوات.idxmin()
معدل_نجاح_أسوأ_قناة = معدلات_نجاح_القنوات.min() * 100

    # 📝 تحليل نجاح الحملات حسب القناة
st.markdown(f"""
    🔍 **تحليل أداء الحملات التسويقية حسب القناة:**

يكشف تحليل البيانات أن القناة الأكثر نجاحًا هي **{أفضل_قناة}**، حيث حققت نسبة نجاح بلغت حوالي **{معدل_نجاح_أفضل_قناة:.2f} في المئة**.  
يشير هذا إلى أن هذه القناة تساهم بشكل كبير في تحقيق الأهداف التسويقية، مما يجعلها خيارًا مثاليًا لتوجيه المزيد من الاستثمارات والجهود التسويقية.  

من ناحية أخرى، تُظهر البيانات أن القناة الأقل نجاحًا هي **{أسوأ_قناة}**، مع نسبة نجاح تبلغ حوالي**{معدل_نجاح_أسوأ_قناة:.2f} في المئة**.  
قد يعود ذلك إلى عوامل مختلفة مثل ضعف التفاعل، عدم ملاءمة المحتوى للجمهور المستهدف، أو الحاجة إلى تحسين استراتيجيات التنفيذ.

📊 **توصيات بناءً على التحليل:**  
    - التركيز على **{أفضل_قناة}** كقناة رئيسية لتعزيز الحملات التسويقية وزيادة العائد على الاستثمار.  
    - تحليل أسباب ضعف أداء **{أسوأ_قناة}**، وإجراء تحسينات على استراتيجياتها أو إعادة تخصيص الميزانية لقنوات أكثر فاعلية.  
    - الاستفادة من البيانات لتحسين استهداف الجمهور وتعزيز التفاعل عبر القنوات المختلفة لضمان تحقيق أقصى استفادة من الميزانية التسويقية.
    """)
