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
المدة = st.slider("⏳ مدة الحملة (بالأيام):", min_value=7, max_value=90, step=7)
حالة_السوق = st.selectbox("🌍 حالة السوق:", ["طبيعية", "أزمة كورونا", "أزمة اقتصادية"])

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
🔎 **تقرير تحليلي شامل حول الحملة التسويقية:**  
- بناءً على الميزانية المحددة ({الميزانية}) واختيار القناة التسويقية ({القناة})، تم تحليل المعطيات والتنبؤ بنتيجة الحملة.  
- الفئة المستهدفة ({الجمهور}) تلعب دوراً محورياً في نجاح الحملة، بالإضافة إلى مدة الحملة المحددة ({المدة} أيام).  
- تم الأخذ في الاعتبار حالة السوق الحالية ({حالة_السوق}) والتي قد تؤثر بشكل ملحوظ على الأداء.  
- **نتيجة التنبؤ:** الحملة من المحتمل أن تكون بنسبة عالية **{result}**.  
- **تحليل الميزات المؤثرة:**  
"""

for index, row in importance_df.iterrows():
    analysis += f"- **{row['الميزة']}**: مستوى تأثيره على النجاح هو **{row['الأهمية']:.2f}**.\n"

st.write(analysis)

# 📊 رسم المخططات
# مثال لبيانات الأهمية
importance_df = pd.DataFrame({
    "الميزة": ["قناة التسويق", "الفئة العمرية", "الميزانية", "المدة", "حالة السوق"],
    "الأهمية": [0.25, 0.20, 0.30, 0.15, 0.10]
})

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
sns.barplot(x="الأهمية", y="الميزة", data=importance_df, palette="viridis", ax=ax)

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
🔍 **تحليل مخطط أهمية الميزات:**  
يظهر المخطط أعلاه أن الميزة الأكثر أهمية في تحديد نجاح الحملات هي **{الميزة_الأكثر_أهمية}**، مما يشير إلى أن التركيز على هذه الميزة يمكن أن يساهم بشكل كبير في تحقيق النجاح.  
من ناحية أخرى، تُعد ميزة **{الميزة_الأقل_أهمية}** الأقل تأثيرًا، مما يعني أن الاستثمار في تحسينها قد لا يكون له نفس الأثر.  
""")

# 📊 رسم العلاقة بين الميزانية والنجاح
st.subheader("💸 تأثير الميزانية على نجاح الحملة")
fig2, ax2 = plt.subplots()

# تفعيل دعم اللغة العربية
plt.rcParams['font.family'] = 'Arial'
plt.rcParams['axes.unicode_minus'] = False

# رسم المخطط
sns.boxplot(x="النجاح", y="الميزانية", data=df, palette="cool", ax=ax2)

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

# 📝 تحليل العلاقة بين الميزانية والنجاح
متوسط_ميزانية_النجاح = df[df["النجاح"] == 1]["الميزانية"].mean()
متوسط_ميزانية_الفشل = df[df["النجاح"] == 0]["الميزانية"].mean()
st.markdown(f"""
🔍 **تحليل تأثير الميزانية على النجاح:**  
تُظهر البيانات أن الميزانية المتوسطة للحملات الناجحة هي حوالي **{متوسط_ميزانية_النجاح:.2f} درهم**، بينما الميزانية المتوسطة للحملات غير الناجحة هي حوالي **{متوسط_ميزانية_الفشل:.2f} درهم**.  
يشير ذلك إلى أن الحملات ذات الميزانيات الأعلى تميل إلى تحقيق نجاح أكبر. لذلك يُنصح بتخصيص ميزانية مناسبة للحملات لضمان نجاحها.
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

# رسم المخطط مع وسيلة الإيضاح
sns.countplot(data=df, x="القناة", hue="النجاح", palette="cool", ax=ax3)
ax3.set_title(title, fontsize=16, fontweight='bold')
ax3.set_xlabel(xlabel, fontsize=14)
ax3.set_ylabel(ylabel, fontsize=14)

# إضافة وسيلة الإيضاح مع عنوان (إعادة تشكيل النص)
ax3.legend(title=legend_title, fontsize=12, title_fontsize=14, loc="upper right")

# ضبط إعدادات الخطوط
plt.xticks(fontsize=12)
plt.yticks(fontsize=12)

st.pyplot(fig3)

# 📝 تحليل نجاح الحملات حسب القناة
معدلات_نجاح_القنوات = df.groupby("القناة")["النجاح"].mean().sort_values(ascending=False)
أفضل_قناة = معدلات_نجاح_القنوات.idxmax()
معدل_نجاح_أفضل_قناة = معدلات_نجاح_القنوات.max() * 100
أسوأ_قناة = معدلات_نجاح_القنوات.idxmin()
معدل_نجاح_أسوأ_قناة = معدلات_نجاح_القنوات.min() * 100
st.markdown(f"""
🔍 **تحليل نجاح الحملات حسب القناة:**  
من خلال تحليل البيانات، تبيّن أن القناة التسويقية الأكثر نجاحًا هي **{أفضل_قناة}** بنسبة نجاح تبلغ حوالي **{معدل_نجاح_أفضل_قناة:.2f} في المئة**.  
في المقابل، كانت القناة الأقل نجاحًا هي **{أسوأ_قناة}** بنسبة نجاح تبلغ حوالي **{معدل_نجاح_أسوأ_قناة:.2f} في المئة**.  
يوصى بتركيز الجهود على القنوات الأكثر فاعلية بناءً على هذه النتائج لضمان تحقيق أقصى استفادة من الميزانية التسويقية.
""")