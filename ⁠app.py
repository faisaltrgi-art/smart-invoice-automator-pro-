import streamlit as st
import pandas as pd
import os
from datetime import datetime

st.title("📄 برنامج أتمتة الفواتير الذكية")
st.write("قم برفع ملف المعاملات (`transactions.csv`) لمعالجة البيانات وتوليد الفواتير.")

# أداة لرفع الملف من المتصفح 📁
uploaded_file = st.file_uploader("اختر ملف المعاملات", type=["csv"])

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    st.write("📊 معاينة البيانات المدخلة:", df.head())

    if st.button("إصدار الفواتير"):
        output_folder = "generated_invoices"
        os.makedirs(output_folder, exist_ok=True)
        
        for client, group in df.groupby('client'):
            invoice_id = f"INV-{datetime.now().strftime('%Y%m%d')}-{client[:3].upper()}"
            total = group['amount'].sum()
            
            invoice_data = {
                "Invoice_ID": [invoice_id],
                "Client": [client],
                "Total_Due": [total],
                "Date": [datetime.now().strftime('%Y-%m-%d')]
            }
            
            pd.DataFrame(invoice_data).to_csv(f"{output_folder}/{client}_invoice.csv", index=False)
        
        st.success(f"✅ تم بنجاح توليد الفواتير لـ {len(df['client'].unique())} عملاء.")
