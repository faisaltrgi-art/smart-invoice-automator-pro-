import streamlit as st
import pandas as pd
from fpdf import FPDF

# 1. إعداد واجهة الصفحة
st.set_page_config(
    page_title="نظام أتمتة الفواتير الذكي Pro",
    page_icon="📄",
    layout="wide"
)

# عنوان التطبيق الرئيسي
st.title("📄 نظام أتمتة الفواتير والتحليل الذكي")
st.markdown("---")

# 2. القائمة الجانبية لرفع الملفات
st.sidebar.header("📥 رفع البيانات")
uploaded_file = st.sidebar.file_uploader("اختر ملف المعاملات (CSV)", type=["csv"])

if uploaded_file is not None:
    try:
        df = pd.read_csv(uploaded_file)
        
        # 3. التحقق من جودة وصحة البيانات (Data Validation)
        required_cols = ["Invoice_ID", "Customer", "Amount", "Date"]
        missing_cols = [col for col in required_cols if col not in df.columns]
        
        if missing_cols:
            st.error(f"⚠️ الملف المرفوع غير مكتمل! الأعمدة المفقودة: {', '.join(missing_cols)}")
            st.info("💡 تأكد من أن الملف يحتوي على الأعمدة: Invoice_ID, Customer, Amount, Date")
        else:
            st.success("✅ تم التحقق من صحة هيكل البيانات بنجاح!")
            
            # 4. لوحة المؤشرات والإحصائيات (Dashboard)
            st.subheader("📊 لوحة المؤشرات الرئيسية (KPIs)")
            col1, col2, col3, col4 = st.columns(4)
            
            total_revenue = df["Amount"].sum()
            total_invoices = len(df)
            avg_invoice = df["Amount"].mean()
            top_customer = df.groupby("Customer")["Amount"].sum().idxmax()
            
            col1.metric("إجمالي المبيعات", f"${total_revenue:,.2f}")
            col2.metric("عدد الفواتير", f"{total_invoices}")
            col3.metric("متوسط القيمة", f"${avg_invoice:,.2f}")
            col4.metric("أكبر عميل", str(top_customer))
            
            st.markdown("---")
            
            # 5. التحليل الذكي وكشف القيم الشاذة (AI Anomaly Detection)
            st.subheader("🤖 التحليل الذكي ورصد المعاملات الشاذة")
            threshold = avg_invoice + (2 * df["Amount"].std()) if len(df) > 1 else avg_invoice
            anomalies = df[df["Amount"] > threshold]
            
            if not anomalies.empty:
                st.warning(f"🚨 تم رصد {len(anomalies)} فاتورة بقيم مرتفعة جداً عن المعدل الطبيعي:")
                st.dataframe(anomalies)
            else:
                st.info("💡 جميع الفواتير ضمن النطاق الطبيعي للمبيعات.")
                
            # رسم بياني لتوزيع المبيعات حسب العميل
            st.subheader("📈 توزيع المبيعات حسب العميل")
            chart_data = df.groupby("Customer")["Amount"].sum()
            st.bar_chart(chart_data)
            
            # 6. معاينة البيانات وتصدير تقرير PDF
            st.subheader("📑 معاينة الجدول وتصدير التقرير")
            st.dataframe(df, use_container_width=True)
            
            # دالة إنشاء تقرير PDF
            def generate_pdf(dataframe):
                pdf = FPDF()
                pdf.add_page()
                pdf.set_font("Arial", 'B', 16)
                pdf.cell(200, 10, txt="Smart Invoices Executive Summary", ln=True, align='C')
                pdf.ln(10)
                pdf.set_font("Arial", size=11)
                
                for idx, row in dataframe.iterrows():
                    text_line = f"ID: {row['Invoice_ID']} | Customer: {row['Customer']} | Amount: ${row['Amount']} | Date: {row['Date']}"
                    pdf.cell(0, 8, txt=text_line, ln=True)
                
                return pdf.output(dest='S').encode('latin-1', errors='replace')
            
            pdf_bytes = generate_pdf(df)
            
            st.download_button(
                label="📥 تنزيل تقرير الفواتير المجمع (PDF)",
                data=pdf_bytes,
                file_name="Invoices_Summary_Report.pdf",
                mime="application/pdf"
            )

    except Exception as e:
        st.error(f"حدث خطأ أثناء معالجة البيانات: {e}")
else:
    st.info("👈 يرجى رفع ملف CSV من القائمة الجانبية لبدء المعالجة والتحليل.")
