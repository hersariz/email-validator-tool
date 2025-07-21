import streamlit as st
import pandas as pd
import io
import time
import json
import plotly.express as px
import plotly.graph_objects as go
from validator import validate_email

st.set_page_config(
    page_title="Email Validator Tool",
    page_icon="✉️",
    layout="wide"
)

def main():
    st.title("✉️ Email Validator Tool")
    st.markdown("""
    Alat ini membantu Anda memvalidasi daftar email untuk:
    - Memastikan format email valid
    - Mengecek ketersediaan domain
    - Memverifikasi keberadaan MX record
    - Mendeteksi email disposable/sementara
    - Mengkategorikan email personal vs business
    """)
    
    # Sidebar
    st.sidebar.title("Tentang Aplikasi")
    st.sidebar.info(
        """
        **Email Validator Tool** adalah aplikasi yang dirancang untuk membantu 
        tim sales atau growth dalam memvalidasi daftar email dari hasil scraping 
        atau lead list.
        
        **Tujuan:**
        - Meningkatkan akurasi data
        - Menghindari email bounce
        - Mengelompokkan jenis email (personal vs bisnis)
        
        """
    )
    
    # Notifikasi tentang penggunaan API
    st.sidebar.title("Validasi API")
    st.sidebar.info(
        """
        Aplikasi ini menggunakan AbstractAPI Email Validation untuk hasil validasi 
        yang akurat dan detail. API ini memberikan informasi lengkap tentang:
        
        ✅ Format dan sintaks email
        ✅ Ketersediaan domain dan MX record
        ✅ Disposable email detection
        ✅ Free/role email detection
        ✅ SMTP validation
        ✅ Suggestion koreksi otomatis
        """
    )
    
    # Tab untuk input
    tabs = st.tabs(["Upload CSV", "Input Manual", "Hasil"])
    
    # Tab Upload CSV
    with tabs[0]:
        st.header("Upload File CSV")
        uploaded_file = st.file_uploader("Pilih file CSV yang berisi kolom email", type=["csv"])
        
        if uploaded_file is not None:
            try:
                # Baca file CSV
                df = pd.read_csv(uploaded_file)
                
                # Cek apakah kolom 'email' ada dalam CSV
                if 'email' not in df.columns:
                    st.error("File CSV harus memiliki kolom 'email'.")
                else:
                    st.success(f"Berhasil membaca {len(df)} email dari file CSV.")
                    st.session_state.emails_to_validate = df['email'].tolist()
                    st.session_state.uploaded_df = df
                    
                    # Tunjukkan pratinjau data
                    st.subheader("Pratinjau Data:")
                    st.dataframe(df.head())
                    
                    # Tombol untuk proses validasi
                    if st.button("Validasi Email", key="validate_csv"):
                        with st.spinner("Memvalidasi email..."):
                            validate_emails()
            except Exception as e:
                st.error(f"Error membaca file CSV: {e}")
    
    # Tab Input Manual
    with tabs[1]:
        st.header("Input Email Manual")
        
        # Input area untuk email
        email_input = st.text_area(
            "Masukkan daftar email (satu email per baris)",
            height=200
        )
        
        # Tombol untuk proses validasi
        if st.button("Validasi Email", key="validate_manual"):
            if email_input:
                # Split input menjadi list email
                email_list = [email.strip() for email in email_input.split('\n') if email.strip()]
                st.session_state.emails_to_validate = email_list
                
                with st.spinner("Memvalidasi email..."):
                    validate_emails()
            else:
                st.warning("Harap masukkan minimal satu email untuk divalidasi.")
    
    # Tab Hasil
    with tabs[2]:
        if 'validation_results' in st.session_state:
            st.header("Hasil Validasi Email")
            
            # Konversi hasil validasi ke dataframe
            results = st.session_state.validation_results
            
            # Ekstrak data API untuk analisis
            api_data = extract_api_data(results)
            
            # Buat dataframe dari hasil ekstraksi
            if api_data:
                results_df = pd.DataFrame(api_data)
                
                # Dashboard analisis hasil validasi
                display_validation_dashboard(results_df)
                
                # Tampilkan tabel hasil
                display_validation_table(results_df)
                
                # Detail validasi untuk email yang dipilih
                display_email_details(results)
            else:
                st.error("Tidak dapat mengekstrak data API dari hasil validasi.")
        else:
            st.info("Belum ada hasil validasi. Silakan validasi email terlebih dahulu di tab Upload CSV atau Input Manual.")


def extract_api_data(validation_results):
    """
    Ekstrak dan strukturkan data penting dari hasil API untuk dianalisis
    """
    api_data = []
    
    for result in validation_results:
        email = result.get('email', '')
        api_result = result.get('api_validation', {})
        
        if not api_result:
            continue
        
        # Ekstrak data dari API result
        entry = {
            'email': email,
            'category': result.get('category', 'unknown'),
            'quality_score': api_result.get('quality_score', 0),
            'deliverability': api_result.get('deliverability', 'UNKNOWN'),
            'is_valid_format': api_result.get('is_valid_format', {}).get('value', False) if isinstance(api_result.get('is_valid_format'), dict) else False,
            'is_free_email': api_result.get('is_free_email', {}).get('value', False) if isinstance(api_result.get('is_free_email'), dict) else False,
            'is_disposable': api_result.get('is_disposable_email', {}).get('value', False) if isinstance(api_result.get('is_disposable_email'), dict) else False,
            'is_role_email': api_result.get('is_role_email', {}).get('value', False) if isinstance(api_result.get('is_role_email'), dict) else False,
            'is_catchall': api_result.get('is_catchall_email', {}).get('value', False) if isinstance(api_result.get('is_catchall_email'), dict) else False,
            'has_mx_record': api_result.get('is_mx_found', {}).get('value', False) if isinstance(api_result.get('is_mx_found'), dict) else False,
            'is_smtp_valid': api_result.get('is_smtp_valid', {}).get('value', False) if isinstance(api_result.get('is_smtp_valid'), dict) else False,
            'autocorrect': api_result.get('autocorrect', '')
        }
        
        api_data.append(entry)
    
    return api_data


def display_validation_dashboard(df):
    """
    Menampilkan dashboard dengan chart dan statistik dari hasil validasi
    """
    st.subheader("Dashboard Validasi Email")
    
    # Statistik Ringkasan
    col1, col2, col3, col4 = st.columns(4)
    
    total = len(df)
    
    with col1:
        deliverable = sum(df['deliverability'] == 'DELIVERABLE')
        st.metric("Deliverable", f"{deliverable}/{total}", f"{deliverable/total*100:.1f}%")
    
    with col2:
        valid_format = sum(df['is_valid_format'].fillna(False))
        st.metric("Format Valid", f"{valid_format}/{total}", f"{valid_format/total*100:.1f}%")
    
    with col3:
        valid_mx = sum(df['has_mx_record'].fillna(False))
        st.metric("MX Record Valid", f"{valid_mx}/{total}", f"{valid_mx/total*100:.1f}%")
    
    with col4:
        # Handle None values before applying ~ operator
        non_disposable = total - sum(df['is_disposable'].fillna(False))
        st.metric("Non-Disposable", f"{non_disposable}/{total}", f"{non_disposable/total*100:.1f}%")
    
    # Chart Baris 1: Deliverability dan Kategori Email
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### Deliverability Status")
        deliverability_counts = df['deliverability'].value_counts().reset_index()
        deliverability_counts.columns = ['deliverability', 'count']
        
        fig = px.pie(deliverability_counts, names='deliverability', values='count', 
                     color='deliverability',
                     color_discrete_map={
                         'DELIVERABLE': '#00CC96', 
                         'RISKY': '#FFA15A',
                         'UNDELIVERABLE': '#EF553B',
                         'UNKNOWN': '#636EFA'
                     },
                     title='Email Deliverability Status')
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.markdown("#### Email Category")
        category_counts = df['category'].value_counts().reset_index()
        category_counts.columns = ['category', 'count']
        
        fig = px.pie(category_counts, names='category', values='count',
                     title='Business vs Personal Emails')
        st.plotly_chart(fig, use_container_width=True)
    
    # Chart Baris 2: Validasi dan Quality Score
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### Validasi Parameter")
        
        # Hitung jumlah email yang memenuhi setiap parameter validasi
        # Handle None values with fillna(False) before applying ~ operator
        validation_data = {
            'Parameter': [
                'Format Valid', 'MX Record Valid', 'SMTP Valid', 
                'Non-Disposable', 'Non-Role Email', 'Non-Catchall'
            ],
            'Valid': [
                sum(df['is_valid_format'].fillna(False)),
                sum(df['has_mx_record'].fillna(False)),
                sum(df['is_smtp_valid'].fillna(False)),
                sum(~df['is_disposable'].fillna(False)),
                sum(~df['is_role_email'].fillna(False)),
                sum(~df['is_catchall'].fillna(False))
            ],
            'Invalid': [
                sum(~df['is_valid_format'].fillna(False)),
                sum(df['has_mx_record'].fillna(False) == False),
                sum(df['is_smtp_valid'].fillna(False) == False),
                sum(df['is_disposable'].fillna(False)),
                sum(df['is_role_email'].fillna(False)),
                sum(df['is_catchall'].fillna(False))
            ]
        }
        
        validation_df = pd.DataFrame(validation_data)
        
        fig = px.bar(validation_df, x='Parameter', y=['Valid', 'Invalid'], 
                     title='Validasi Parameter',
                     barmode='group',
                     color_discrete_map={
                         'Valid': '#00CC96',
                         'Invalid': '#EF553B'
                     })
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.markdown("#### Quality Score Distribution")
        
        # Histogram Quality Score
        fig = px.histogram(df, x='quality_score', 
                          title='Distribusi Quality Score', 
                          range_x=[0, 1],
                          nbins=10)
        fig.update_traces(marker_color='#636EFA')
        st.plotly_chart(fig, use_container_width=True)


def display_validation_table(df):
    """
    Menampilkan tabel hasil validasi email
    """
    st.subheader("Tabel Hasil Validasi")
    
    # Buat copy dataframe untuk tampilan
    display_df = df.copy()
    
    # Format quality_score sebagai persentase
    display_df['quality_score'] = display_df['quality_score'].apply(lambda x: f"{float(x)*100:.1f}%" if isinstance(x, (int, float)) else x)
    
    # Konversi boolean ke tanda centang dan silang
    bool_columns = ['is_valid_format', 'has_mx_record', 'is_smtp_valid', 'is_free_email', 'is_role_email', 'is_disposable', 'is_catchall']
    for col in bool_columns:
        if col in display_df.columns:
            # Untuk field negatif, invert nilai untuk konsistensi
            if col in ['is_role_email', 'is_disposable', 'is_catchall']:
                display_df[col] = display_df[col].apply(lambda x: "❌" if x else "✅")
            else:
                display_df[col] = display_df[col].apply(lambda x: "✅" if x else "❌")
    
    # Rename kolom untuk tampilan yang lebih baik
    display_df = display_df.rename(columns={
        'email': 'Email',
        'category': 'Jenis Email',
        'quality_score': 'Skor Kualitas',
        'deliverability': 'Deliverability',
        'is_valid_format': 'Format Valid',
        'is_free_email': 'Free Email',
        'is_disposable': 'Non-Disposable',
        'is_role_email': 'Non-Role Email',
        'is_catchall': 'Non-Catchall',
        'has_mx_record': 'MX Record',
        'is_smtp_valid': 'SMTP Valid',
        'autocorrect': 'Koreksi Otomatis'
    })
    
    # Atur urutan kolom
    column_order = ['Email', 'Jenis Email', 'Deliverability', 'Skor Kualitas', 
                   'Format Valid', 'MX Record', 'SMTP Valid', 
                   'Non-Disposable', 'Free Email', 'Non-Role Email', 'Non-Catchall',
                   'Koreksi Otomatis']
    display_df = display_df[[col for col in column_order if col in display_df.columns]]
    
    # Tampilkan tabel
    st.dataframe(display_df)
    
    # Download hasil sebagai CSV
    csv = df.to_csv(index=False)
    st.download_button(
        label="Download Hasil sebagai CSV",
        data=csv,
        file_name="email_validation_results.csv",
        mime="text/csv"
    )


def display_email_details(results):
    """
    Menampilkan detail validasi untuk email yang dipilih
    """
    st.subheader("Detail Validasi Email")
    
    # Buat list email yang valid untuk dropdown
    email_list = []
    for result in results:
        if result.get('api_validation'):
            email_list.append(result.get('email'))
    
    if email_list:
        selected_email = st.selectbox("Pilih email untuk melihat detail validasi:", email_list)
        
        # Cari hasil validasi untuk email yang dipilih
        selected_result = next((r for r in results if r.get('email') == selected_email), None)
        
        if selected_result and selected_result.get('api_validation'):
            api_result = selected_result.get('api_validation')
            
            # Tampilkan hasil API dalam format yang lebih rapi dan mudah dibaca
            st.markdown(f"### Hasil Validasi untuk: {api_result.get('email', selected_email)}")
            
            # Baris 1: Skor dan Deliverability
            col1, col2 = st.columns(2)
            with col1:
                quality_score = api_result.get('quality_score', 'N/A')
                if isinstance(quality_score, (int, float)):
                    quality_percentage = f"{float(quality_score)*100:.1f}%"
                    st.metric("Skor Kualitas", quality_percentage)
                else:
                    st.metric("Skor Kualitas", quality_score)
            
            with col2:
                deliverability = api_result.get('deliverability', 'N/A')
                color = "green" if deliverability == "DELIVERABLE" else ("orange" if deliverability == "RISKY" else "red")
                st.markdown(f"**Status Deliverability:** <span style='color:{color};font-weight:bold'>{deliverability}</span>", unsafe_allow_html=True)
            
            # Baris 2: Autocorrect
            autocorrect = api_result.get('autocorrect', '')
            if autocorrect:
                st.info(f"📝 **Koreksi Otomatis:** {autocorrect}")
            
            # Baris 3: Domain Info
            if 'domain' in api_result:
                domain_info = api_result['domain']
                st.markdown("#### Informasi Domain")
                
                domain_data = {}
                if isinstance(domain_info, dict):
                    for key, value in domain_info.items():
                        if key != 'name':  # Skip domain name karena sudah ada di email
                            domain_data[key] = value
                
                if domain_data:
                    domain_df = pd.DataFrame([domain_data])
                    st.dataframe(domain_df)
            
            # Baris 4: Informasi validasi dalam tabel
            st.markdown("#### Hasil Validasi Detail")
            
            # Ekstrak hasil validasi dari API
            validation_data = {
                "Parameter": [
                    "Format Email Valid",
                    "Free Email",
                    "Disposable Email",
                    "Role Email",
                    "Catchall Email",
                    "MX Record Ditemukan",
                    "SMTP Valid"
                ],
                "Status": [],
                "Detail": []
            }
            
            # Ambil nilai status dari hasil API
            for key, label in [
                ('is_valid_format', "Format Email Valid"),
                ('is_free_email', "Free Email"),
                ('is_disposable_email', "Disposable Email"),
                ('is_role_email', "Role Email"),
                ('is_catchall_email', "Catchall Email"),
                ('is_mx_found', "MX Record Ditemukan"),
                ('is_smtp_valid', "SMTP Valid")
            ]:
                if key in api_result and isinstance(api_result[key], dict) and 'value' in api_result[key]:
                    value = api_result[key]['value']
                    text = api_result[key].get('text', str(value))
                    
                    if isinstance(value, bool):
                        icon = "✅" if value else "❌"
                        if key == 'is_disposable_email' or key == 'is_role_email' or key == 'is_catchall_email':
                            # Untuk parameter negatif, balik ikonnya
                            icon = "❌" if value else "✅"
                        validation_data["Status"].append(icon)
                    else:
                        validation_data["Status"].append(str(value))
                    
                    validation_data["Detail"].append(text)
                else:
                    validation_data["Status"].append("N/A")
                    validation_data["Detail"].append("N/A")
            
            # Buat dataframe untuk tampilan
            validation_df = pd.DataFrame(validation_data)
            
            # Tampilkan tabel dengan gaya khusus
            st.table(validation_df)
            
            # Tambahkan vizualisasi skor kualitas
            if isinstance(quality_score, (int, float)):
                st.markdown("#### Skor Kualitas")
                fig = go.Figure(go.Indicator(
                    mode="gauge+number",
                    value=quality_score * 100,
                    domain={'x': [0, 1], 'y': [0, 1]},
                    title={'text': "Skor Kualitas Email"},
                    gauge={
                        'axis': {'range': [0, 100]},
                        'bar': {'color': "darkblue"},
                        'steps': [
                            {'range': [0, 40], 'color': "red"},
                            {'range': [40, 70], 'color': "orange"},
                            {'range': [70, 100], 'color': "green"}
                        ],
                        'threshold': {
                            'line': {'color': "black", 'width': 4},
                            'thickness': 0.75,
                            'value': quality_score * 100
                        }
                    }
                ))
                
                fig.update_layout(height=300)
                st.plotly_chart(fig, use_container_width=True)
            
            # Petunjuk interpretasi
            st.markdown("#### Petunjuk Interpretasi")
            st.markdown("""
            - **Skor Kualitas**: Persentase kepercayaan validitas email (lebih tinggi = lebih baik)
            - **Deliverability**: Kemungkinan email dapat dikirim dengan sukses
            - **Format Email Valid**: Apakah format email valid secara sintaksis
            - **Free Email**: Apakah email menggunakan layanan gratis (Gmail, Yahoo, dll)
            - **Disposable Email**: Apakah email menggunakan layanan sementara (❌ = bukan disposable)
            - **Role Email**: Apakah email adalah alamat peran umum seperti info@, support@, dll (❌ = bukan email peran)
            - **Catchall Email**: Apakah domain menggunakan catchall yang menerima semua email (❌ = bukan catchall)
            - **MX Record Ditemukan**: Apakah domain memiliki record MX yang valid
            - **SMTP Valid**: Apakah server email dapat menerima email
            """)
        else:
            st.error(f"Tidak dapat menemukan detail validasi untuk email: {selected_email}")
    else:
        st.info("Tidak ada data validasi API tersedia untuk ditampilkan.")


def validate_emails():
    """
    Fungsi untuk memvalidasi daftar email menggunakan API dan menyimpan hasilnya ke session state
    """
    if 'emails_to_validate' not in st.session_state:
        st.error("Tidak ada email untuk divalidasi.")
        return
    
    emails = st.session_state.emails_to_validate
    
    # Inisialisasi progress bar
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    results = []
    total_emails = len(emails)
    
    for i, email in enumerate(emails):
        # Update progress
        progress = (i + 1) / total_emails
        progress_bar.progress(progress)
        status_text.text(f"Memvalidasi email {i+1}/{total_emails}: {email}")
        
        # Validasi email menggunakan API
        result = validate_email(email, use_api=True)
        results.append(result)
    
    # Simpan hasil validasi ke session state
    st.session_state.validation_results = results
    
    # Reset progress bar dan status
    progress_bar.empty()
    status_text.empty()
    
    # Pindah ke tab hasil
    st.session_state.active_tab = "Hasil"
    
    # Tampilkan notifikasi sukses
    st.success(f"Berhasil memvalidasi {total_emails} email!")


if __name__ == "__main__":
    # Inisialisasi session state jika belum ada
    if 'emails_to_validate' not in st.session_state:
        st.session_state.emails_to_validate = []
    
    if 'active_tab' not in st.session_state:
        st.session_state.active_tab = "Upload CSV"
    
    main() 