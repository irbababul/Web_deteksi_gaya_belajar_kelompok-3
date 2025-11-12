import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime
import io
from PIL import Image
import base64

from database import init_database, get_session, Responden, Jawaban, HasilAnalisis
from kuisioner_data import KUISIONER, PILIHAN_JAWABAN
from expert_system import SistemPakarGayaBelajar, get_rekomendasi
from team_data import TEAM_MEMBERS, REFERENSI, FAQ_DATA
from pdf_generator import generate_pdf

st.set_page_config(
    page_title="Sistem Deteksi Gaya Belajar Siswa",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

init_database()

def apply_custom_css():
    st.markdown("""
    <style>
    .main {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
    }
    
    .hero-section {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 3rem 2rem;
        border-radius: 15px;
        text-align: center;
        color: white;
        margin-bottom: 2rem;
        box-shadow: 0 10px 30px rgba(0,0,0,0.2);
    }
    
    .hero-title {
        font-size: 3rem;
        font-weight: 800;
        margin-bottom: 1rem;
    }
    
    .hero-subtitle {
        font-size: 1.3rem;
        margin-bottom: 0;
        opacity: 0.95;
    }
    
    .team-card {
        background: white;
        padding: 1.5rem;
        border-radius: 12px;
        text-align: center;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        transition: transform 0.3s ease;
        height: 100%;
    }
    
    .team-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 25px rgba(0,0,0,0.15);
    }
    
    .avatar-placeholder {
        width: 120px;
        height: 120px;
        border-radius: 50%;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 3rem;
        font-weight: bold;
        color: white;
        margin: 0 auto 1rem;
    }
    
    .gaya-card {
        background: white;
        padding: 2rem;
        border-radius: 12px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        height: 100%;
        border-left: 5px solid;
    }
    
    .visual-card {
        border-left-color: #3B82F6;
    }
    
    .auditori-card {
        border-left-color: #10B981;
    }
    
    .kinestetik-card {
        border-left-color: #F59E0B;
    }
    
    .stButton>button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        font-weight: 600;
        border: none;
        padding: 0.75rem 2rem;
        border-radius: 8px;
        font-size: 1.1rem;
        transition: all 0.3s ease;
    }
    
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 20px rgba(102, 126, 234, 0.4);
    }
    
    .faq-item {
        background: white;
        padding: 1.5rem;
        border-radius: 8px;
        margin-bottom: 1rem;
        box-shadow: 0 2px 8px rgba(0,0,0,0.08);
    }
    
    .progress-bar {
        background: #e0e0e0;
        border-radius: 10px;
        height: 20px;
        overflow: hidden;
    }
    
    .progress-fill {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        height: 100%;
        transition: width 0.3s ease;
    }
    
    .hasil-dominan {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 2rem;
        border-radius: 15px;
        text-align: center;
        font-size: 2rem;
        font-weight: bold;
        margin: 2rem 0;
        box-shadow: 0 10px 30px rgba(0,0,0,0.2);
    }
    
    .rekomendasi-box {
        background: white;
        padding: 2rem;
        border-radius: 12px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        margin: 1rem 0;
    }
    
    .footer {
        background: #2d3748;
        color: white;
        padding: 3rem 2rem;
        border-radius: 12px;
        margin-top: 3rem;
    }
    
    .referensi-item {
        background: #f8f9fa;
        padding: 1rem;
        border-radius: 6px;
        margin-bottom: 0.75rem;
        border-left: 3px solid #667eea;
    }
    </style>
    """, unsafe_allow_html=True)

def init_session_state():
    if 'page' not in st.session_state:
        st.session_state.page = 'home'
    if 'responden_data' not in st.session_state:
        st.session_state.responden_data = None
    if 'jawaban_kuisioner' not in st.session_state:
        st.session_state.jawaban_kuisioner = {}
    if 'current_question' not in st.session_state:
        st.session_state.current_question = 0
    if 'hasil_analisis' not in st.session_state:
        st.session_state.hasil_analisis = None
    if 'responden_id' not in st.session_state:
        st.session_state.responden_id = None

def create_avatar_placeholder(initial, size=120):
    return f"""
    <div style="width: {size}px; height: {size}px; border-radius: 50%; 
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                display: flex; align-items: center; justify-content: center;
                font-size: {size//3}px; font-weight: bold; color: white; 
                margin: 0 auto 1rem;">
        {initial}
    </div>
    """

def sidebar_menu():
    with st.sidebar:
        st.markdown("### 🎓 Menu Navigasi")
        
        if st.button("🏠 Beranda", use_container_width=True):
            st.session_state.page = 'home'
            st.rerun()
        
        if st.button("📝 Mulai Tes", use_container_width=True):
            st.session_state.page = 'form_responden'
            st.rerun()
        
        if st.button("📚 Tentang Gaya Belajar", use_container_width=True):
            st.session_state.page = 'tentang_gaya_belajar'
            st.rerun()
        
        if st.button("❓ FAQ", use_container_width=True):
            st.session_state.page = 'faq'
            st.rerun()
        
        if st.button("📞 Kontak", use_container_width=True):
            st.session_state.page = 'kontak'
            st.rerun()
        
        if st.button("📊 Riwayat Tes", use_container_width=True):
            st.session_state.page = 'riwayat'
            st.rerun()
        
        st.markdown("---")
        st.markdown("**Kelompok 3**")
        st.markdown("Sistem Pakar Deteksi Gaya Belajar")

def page_home():
    st.markdown("""
    <div class="hero-section">
        <h1 class="hero-title">🎓 Temukan Gaya Belajar Anda!</h1>
        <p class="hero-subtitle">Ketahui apakah Anda tipe Visual, Auditori, atau Kinestetik<br>
        dan dapatkan rekomendasi metode belajar yang paling sesuai</p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        if st.button("🚀 MULAI DETEKSI", use_container_width=True, type="primary"):
            st.session_state.page = 'form_responden'
            st.rerun()
    
    with col2:
        if st.button("📚 PELAJARI LEBIH LANJUT", use_container_width=True):
            st.session_state.page = 'tentang_gaya_belajar'
            st.rerun()
    
    st.markdown("---")
    
    st.markdown("### 👥 Tim Pengembang - Kelompok 3")
    
    cols = st.columns(4)
    for idx, member in enumerate(TEAM_MEMBERS):
        with cols[idx]:
            st.markdown(create_avatar_placeholder(member['initial']), unsafe_allow_html=True)
            st.markdown(f"**{member['nama']}**")
            st.markdown(f"NIM: {member['nim']}")
            st.markdown(f"_{member['peran']}_")
    
    st.markdown("---")
    
    st.markdown("### 📖 Apa itu Gaya Belajar?")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="gaya-card visual-card">
            <h2 style="text-align: center;">👁️ VISUAL</h2>
            <p style="text-align: center;">Belajar melalui melihat dan mengamati. 
            Lebih mudah mengingat dengan gambar, diagram, dan visualisasi.</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="gaya-card auditori-card">
            <h2 style="text-align: center;">👂 AUDITORI</h2>
            <p style="text-align: center;">Belajar melalui mendengar. 
            Lebih mudah mengingat dengan penjelasan verbal dan diskusi.</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="gaya-card kinestetik-card">
            <h2 style="text-align: center;">✋ KINESTETIK</h2>
            <p style="text-align: center;">Belajar melalui praktik dan gerakan. 
            Lebih mudah mengingat dengan melakukan langsung.</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    st.markdown("### 🎯 Cara Kerja Sistem")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        #### 1️⃣ Isi Data Diri
        Masukkan nama, usia, jenjang pendidikan, dan data diri Anda
        """)
    
    with col2:
        st.markdown("""
        #### 2️⃣ Jawab Kuisioner
        Jawab 25 pertanyaan tentang kebiasaan belajar Anda (5-10 menit)
        """)
    
    with col3:
        st.markdown("""
        #### 3️⃣ Lihat Hasil
        Dapatkan analisis lengkap dan rekomendasi metode belajar
        """)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    col_center = st.columns([1, 2, 1])
    with col_center[1]:
        if st.button("🚀 MULAI TES SEKARANG", use_container_width=True, type="primary"):
            st.session_state.page = 'form_responden'
            st.rerun()
    
    st.markdown("---")
    
    st.markdown("### ❓ FAQ (Pertanyaan yang Sering Diajukan)")
    
    for faq in FAQ_DATA[:3]:
        with st.expander(faq['pertanyaan']):
            st.write(faq['jawaban'])
    
    if st.button("Lihat Semua FAQ →"):
        st.session_state.page = 'faq'
        st.rerun()
    
    st.markdown("---")
    
    st.markdown("""
    <div class="footer">
        <h3>📚 Daftar Referensi</h3>
    """, unsafe_allow_html=True)
    
    for ref in REFERENSI:
        st.markdown(f"""
        <div class="referensi-item">
            <strong>[{ref['nomor']}]</strong> {ref['teks']}
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("""
        <div style="text-align: center; margin-top: 2rem; padding-top: 2rem; border-top: 1px solid rgba(255,255,255,0.2);">
            <p>© 2025 Kelompok 3 - Sistem Deteksi Gaya Belajar Siswa</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

def page_form_responden():
    st.title("📋 Data Responden")
    st.markdown("Sebelum memulai tes, mohon isi data berikut:")
    
    with st.form("form_responden"):
        col1, col2 = st.columns([2, 1])
        
        with col1:
            nama = st.text_input("Nama Lengkap *", placeholder="Masukkan nama lengkap Anda")
            usia = st.number_input("Usia *", min_value=5, max_value=100, value=15)
            jenjang = st.selectbox("Jenjang Pendidikan *", 
                                   ["", "SD/MI", "SMP/MTs", "SMA/SMK/MA", "Perguruan Tinggi"])
            jenis_kelamin = st.radio("Jenis Kelamin *", ["Laki-laki", "Perempuan"])
        
        with col2:
            st.markdown("#### Foto Profil (Opsional)")
            uploaded_file = st.file_uploader("Upload Foto", type=['jpg', 'jpeg', 'png'], 
                                            help="Format: JPG, PNG (Max 2MB)")
            
            if uploaded_file:
                image = Image.open(uploaded_file)
                st.image(image, caption="Preview", use_container_width=True)
        
        submitted = st.form_submit_button("LANJUT KE KUISIONER →", use_container_width=True, type="primary")
        
        if submitted:
            if not nama or not jenjang:
                st.error("❌ Mohon isi semua field yang wajib (*)")
            else:
                foto_bytes = None
                if uploaded_file:
                    foto_bytes = uploaded_file.getvalue()
                
                st.session_state.responden_data = {
                    'nama': nama,
                    'usia': usia,
                    'jenjang_pendidikan': jenjang,
                    'jenis_kelamin': jenis_kelamin,
                    'foto': foto_bytes
                }
                
                st.session_state.current_question = 0
                st.session_state.jawaban_kuisioner = {}
                st.session_state.page = 'kuisioner'
                st.success("✅ Data tersimpan! Mengarahkan ke kuisioner...")
                st.rerun()

def page_kuisioner():
    if not st.session_state.responden_data:
        st.warning("⚠️ Silakan isi data responden terlebih dahulu")
        if st.button("← Kembali ke Form Data"):
            st.session_state.page = 'form_responden'
            st.rerun()
        return
    
    st.title("📝 Kuisioner Gaya Belajar")
    
    current_q = st.session_state.current_question
    total_q = len(KUISIONER)
    
    progress = (current_q / total_q) * 100
    st.markdown(f"""
    <div style="margin-bottom: 2rem;">
        <p style="margin-bottom: 0.5rem;">Progress: <strong>{current_q}/{total_q} pertanyaan</strong> ({progress:.0f}%)</p>
        <div class="progress-bar">
            <div class="progress-fill" style="width: {progress}%;"></div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    if current_q < total_q:
        pertanyaan = KUISIONER[current_q]
        
        st.markdown(f"""
        <div style="background: white; padding: 2rem; border-radius: 12px; box-shadow: 0 4px 15px rgba(0,0,0,0.1); margin-bottom: 2rem;">
            <h3 style="color: #667eea;">Pertanyaan {pertanyaan['nomor']} dari {total_q}</h3>
            <p style="font-size: 1.3rem; margin-top: 1rem;">{pertanyaan['pertanyaan']}</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("#### Pilih jawaban Anda:")
        
        current_answer = st.session_state.jawaban_kuisioner.get(pertanyaan['nomor'], None)
        
        jawaban_value = st.radio(
            "Pilihan:",
            options=[p['nilai'] for p in PILIHAN_JAWABAN],
            format_func=lambda x: next(p['label'] for p in PILIHAN_JAWABAN if p['nilai'] == x),
            index=current_answer - 1 if current_answer else None,
            key=f"q_{pertanyaan['nomor']}"
        )
        
        st.session_state.jawaban_kuisioner[pertanyaan['nomor']] = jawaban_value
        
        col1, col2, col3 = st.columns([1, 1, 1])
        
        with col1:
            if current_q > 0:
                if st.button("← Sebelumnya", use_container_width=True):
                    st.session_state.current_question -= 1
                    st.rerun()
        
        with col3:
            if current_q < total_q - 1:
                if st.button("Selanjutnya →", use_container_width=True, type="primary"):
                    st.session_state.current_question += 1
                    st.rerun()
            else:
                if st.button("SELESAI ✓", use_container_width=True, type="primary"):
                    if len(st.session_state.jawaban_kuisioner) == total_q:
                        proses_hasil()
                    else:
                        st.error("❌ Mohon jawab semua pertanyaan")
    
def proses_hasil():
    with st.spinner("🔄 Menganalisis jawaban Anda..."):
        session = get_session()
        
        try:
            responden_data = st.session_state.responden_data
            responden = Responden(
                nama=responden_data['nama'],
                usia=responden_data['usia'],
                jenjang_pendidikan=responden_data['jenjang_pendidikan'],
                jenis_kelamin=responden_data['jenis_kelamin'],
                foto=responden_data.get('foto')
            )
            session.add(responden)
            session.commit()
            
            responden_id = responden.id
            st.session_state.responden_id = responden_id
            
            jawaban_list = []
            for nomor, nilai in st.session_state.jawaban_kuisioner.items():
                pertanyaan = next(q for q in KUISIONER if q['nomor'] == nomor)
                
                jawaban = Jawaban(
                    responden_id=responden_id,
                    nomor_pertanyaan=nomor,
                    nilai_jawaban=nilai,
                    kategori=pertanyaan['kategori']
                )
                session.add(jawaban)
                jawaban_list.append({'nomor': nomor, 'nilai': nilai})
            
            session.commit()
            
            sistem_pakar = SistemPakarGayaBelajar(jawaban_list)
            hasil = sistem_pakar.analisis_lengkap()
            
            tied_types_str = ",".join(hasil.get('tied_types', [])) if hasil.get('is_tied', False) else None
            
            hasil_db = HasilAnalisis(
                responden_id=responden_id,
                skor_visual=hasil['skor']['visual'],
                skor_auditori=hasil['skor']['auditori'],
                skor_kinestetik=hasil['skor']['kinestetik'],
                persentase_visual=hasil['persentase']['visual'],
                persentase_auditori=hasil['persentase']['auditori'],
                persentase_kinestetik=hasil['persentase']['kinestetik'],
                tipe_dominan=hasil['tipe_dominan'],
                is_tied=hasil.get('is_tied', False),
                tied_types=tied_types_str
            )
            session.add(hasil_db)
            session.commit()
            
            st.session_state.hasil_analisis = hasil
            st.session_state.page = 'hasil'
            st.rerun()
            
        except Exception as e:
            session.rollback()
            st.error(f"❌ Terjadi kesalahan: {str(e)}")
        finally:
            session.close()

def page_hasil():
    if not st.session_state.hasil_analisis:
        st.warning("⚠️ Tidak ada hasil analisis. Silakan isi kuisioner terlebih dahulu.")
        if st.button("← Mulai Tes"):
            st.session_state.page = 'form_responden'
            st.rerun()
        return
    
    hasil = st.session_state.hasil_analisis
    responden = st.session_state.responden_data
    
    st.title("🎉 Hasil Analisis Gaya Belajar Anda")
    
    col1, col2 = st.columns([1, 3])
    
    with col1:
        if responden.get('foto'):
            image = Image.open(io.BytesIO(responden['foto']))
            st.image(image, use_container_width=True)
        else:
            nama_parts = responden['nama'].split()
            initial = ''.join([p[0].upper() for p in nama_parts[:2]])
            st.markdown(create_avatar_placeholder(initial, 150), unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div style="background: white; padding: 1.5rem; border-radius: 12px; box-shadow: 0 4px 15px rgba(0,0,0,0.1);">
            <h3>{responden['nama']}</h3>
            <p><strong>Usia:</strong> {responden['usia']} tahun</p>
            <p><strong>Jenjang:</strong> {responden['jenjang_pendidikan']}</p>
            <p><strong>Jenis Kelamin:</strong> {responden['jenis_kelamin']}</p>
            <p><strong>Tanggal Tes:</strong> {datetime.now().strftime('%d %B %Y')}</p>
        </div>
        """, unsafe_allow_html=True)
    
    tipe_display = hasil['tipe_dominan'].upper()
    persentase_dominan = hasil['persentase'][hasil['tipe_dominan'].lower()]
    
    if hasil.get('is_tied', False):
        other_tied = [t for t in hasil['tied_types'] if t != hasil['tipe_dominan']]
        if other_tied:
            tied_text = " / ".join(other_tied)
            tipe_display = f"{tipe_display} (Seri dengan {tied_text})"
    
    st.markdown(f"""
    <div class="hasil-dominan">
        🏆 GAYA BELAJAR DOMINAN ANDA:<br>
        <span style="font-size: 3rem;">{tipe_display}</span><br>
        <span style="font-size: 1.5rem;">({persentase_dominan:.1f}%)</span>
    </div>
    """, unsafe_allow_html=True)
    
    if hasil.get('is_tied', False):
        st.info(f"ℹ️ Hasil Anda menunjukkan gaya belajar yang seimbang antara {' dan '.join(hasil['tied_types'])}. Ini berarti Anda dapat belajar dengan berbagai metode yang fleksibel!")
    
    st.markdown("### 📊 Distribusi Gaya Belajar Anda")
    
    col1, col2 = st.columns(2)
    
    with col1:
        fig_radar = go.Figure(data=go.Scatterpolar(
            r=[hasil['persentase']['visual'], 
               hasil['persentase']['auditori'], 
               hasil['persentase']['kinestetik']],
            theta=['Visual', 'Auditori', 'Kinestetik'],
            fill='toself',
            line=dict(color='#667eea', width=2),
            fillcolor='rgba(102, 126, 234, 0.3)'
        ))
        
        fig_radar.update_layout(
            polar=dict(
                radialaxis=dict(
                    visible=True,
                    range=[0, 100]
                )
            ),
            showlegend=False,
            title="Radar Chart Gaya Belajar",
            height=400
        )
        
        st.plotly_chart(fig_radar, use_container_width=True)
    
    with col2:
        fig_pie = go.Figure(data=[go.Pie(
            labels=['Visual', 'Auditori', 'Kinestetik'],
            values=[hasil['persentase']['visual'], 
                   hasil['persentase']['auditori'], 
                   hasil['persentase']['kinestetik']],
            hole=0.4,
            marker=dict(colors=['#3B82F6', '#10B981', '#F59E0B'])
        )])
        
        fig_pie.update_layout(
            title="Pie Chart Distribusi",
            height=400
        )
        
        st.plotly_chart(fig_pie, use_container_width=True)
    
    fig_bar = go.Figure(data=[
        go.Bar(name='Visual', x=['Visual'], y=[hasil['skor']['visual']], marker_color='#3B82F6'),
        go.Bar(name='Auditori', x=['Auditori'], y=[hasil['skor']['auditori']], marker_color='#10B981'),
        go.Bar(name='Kinestetik', x=['Kinestetik'], y=[hasil['skor']['kinestetik']], marker_color='#F59E0B')
    ])
    
    fig_bar.update_layout(
        title="Bar Chart Skor Gaya Belajar",
        yaxis_title="Skor",
        height=400
    )
    
    st.plotly_chart(fig_bar, use_container_width=True)
    
    rekomendasi = get_rekomendasi(hasil['tipe_dominan'])
    
    st.markdown("### 💡 Rekomendasi untuk Anda")
    
    st.markdown(f"""
    <div class="rekomendasi-box">
        <h4>Tentang Gaya Belajar {hasil['tipe_dominan']}</h4>
        <p>{rekomendasi['deskripsi']}</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("#### ✅ Metode Belajar yang Cocok:")
    for metode in rekomendasi['metode_belajar']:
        st.markdown(f"- {metode}")
    
    st.markdown("#### 📱 Tools & Aplikasi yang Direkomendasikan:")
    for tool in rekomendasi['tools']:
        st.markdown(f"- {tool}")
    
    st.markdown("#### 📖 Tips Menghadapi Ujian:")
    for tip in rekomendasi['tips_ujian']:
        st.markdown(f"- {tip}")
    
    st.markdown("---")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("📥 Download PDF", use_container_width=True, type="primary"):
            pdf_bytes = generate_pdf(responden, hasil, rekomendasi)
            st.download_button(
                label="💾 Simpan PDF",
                data=pdf_bytes,
                file_name=f"hasil_gaya_belajar_{responden['nama'].replace(' ', '_')}.pdf",
                mime="application/pdf",
                use_container_width=True
            )
    
    with col2:
        if st.button("🔄 Tes Ulang", use_container_width=True):
            st.session_state.responden_data = None
            st.session_state.jawaban_kuisioner = {}
            st.session_state.current_question = 0
            st.session_state.hasil_analisis = None
            st.session_state.page = 'form_responden'
            st.rerun()
    
    with col3:
        if st.button("🏠 Kembali ke Beranda", use_container_width=True):
            st.session_state.page = 'home'
            st.rerun()

def page_tentang_gaya_belajar():
    st.title("📚 Mengenal Gaya Belajar")
    
    st.markdown("""
    Gaya belajar adalah cara atau metode yang paling efektif bagi seseorang untuk menyerap, 
    memproses, dan mengingat informasi. Model VAK (Visual, Auditory, Kinesthetic) adalah 
    salah satu pendekatan yang paling populer untuk mengidentifikasi gaya belajar.
    """)
    
    st.markdown("---")
    
    st.markdown("""
    <div class="gaya-card visual-card" style="margin-bottom: 2rem;">
        <h2>👁️ VISUAL (Pembelajar Visual)</h2>
        <h4>Belajar melalui melihat dan mengamati</h4>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**Karakteristik:**")
        st.markdown("""
        - Suka membaca dan melihat gambar
        - Mengingat wajah lebih baik dari nama
        - Lebih suka demonstrasi visual
        - Senang membuat catatan dengan warna
        - Mudah belajar dari diagram dan chart
        """)
    
    with col2:
        st.markdown("**Strategi Belajar:**")
        st.markdown("""
        - Gunakan mind map dan diagram
        - Tonton video pembelajaran
        - Buat catatan berwarna
        - Gunakan flashcard dengan gambar
        - Visualisasikan konsep
        """)
    
    st.markdown("---")
    
    st.markdown("""
    <div class="gaya-card auditori-card" style="margin-bottom: 2rem;">
        <h2>👂 AUDITORI (Pembelajar Auditori)</h2>
        <h4>Belajar melalui mendengar</h4>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**Karakteristik:**")
        st.markdown("""
        - Suka diskusi dan penjelasan verbal
        - Mengingat dengan mendengar
        - Senang musik dan ritme
        - Mudah terganggu oleh kebisingan
        - Belajar baik dengan mendengarkan
        """)
    
    with col2:
        st.markdown("**Strategi Belajar:**")
        st.markdown("""
        - Rekam penjelasan untuk didengar ulang
        - Dengarkan podcast edukatif
        - Belajar dalam kelompok diskusi
        - Bacakan materi dengan suara keras
        - Gunakan musik untuk mengingat
        """)
    
    st.markdown("---")
    
    st.markdown("""
    <div class="gaya-card kinestetik-card" style="margin-bottom: 2rem;">
        <h2>✋ KINESTETIK (Pembelajar Kinestetik)</h2>
        <h4>Belajar melalui praktik dan gerakan</h4>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**Karakteristik:**")
        st.markdown("""
        - Suka hands-on dan eksperimen
        - Aktif bergerak saat belajar
        - Belajar dengan melakukan
        - Suka aktivitas fisik
        - Mengingat melalui pengalaman
        """)
    
    with col2:
        st.markdown("**Strategi Belajar:**")
        st.markdown("""
        - Lakukan praktik langsung
        - Gunakan model dan simulasi
        - Buat project praktis
        - Belajar sambil bergerak
        - Tulis ulang catatan dengan tangan
        """)
    
    st.markdown("---")
    
    st.markdown("### 🎯 Mengapa Penting Mengetahui Gaya Belajar?")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        #### Efektivitas Belajar
        Dengan mengetahui gaya belajar, Anda dapat memilih metode yang paling efektif
        """)
    
    with col2:
        st.markdown("""
        #### Hemat Waktu
        Fokus pada cara belajar yang cocok membuat proses belajar lebih cepat
        """)
    
    with col3:
        st.markdown("""
        #### Hasil Lebih Baik
        Metode yang sesuai meningkatkan pemahaman dan hasil belajar
        """)
    
    if st.button("🚀 Mulai Tes Gaya Belajar", use_container_width=True, type="primary"):
        st.session_state.page = 'form_responden'
        st.rerun()

def page_faq():
    st.title("❓ Pertanyaan yang Sering Diajukan (FAQ)")
    
    for idx, faq in enumerate(FAQ_DATA):
        with st.expander(f"**{faq['pertanyaan']}**", expanded=(idx == 0)):
            st.write(faq['jawaban'])
    
    st.markdown("---")
    
    st.markdown("### 💬 Masih ada pertanyaan?")
    st.markdown("Hubungi kami melalui halaman kontak atau mulai tes untuk mengetahui gaya belajar Anda!")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("📞 Halaman Kontak", use_container_width=True):
            st.session_state.page = 'kontak'
            st.rerun()
    
    with col2:
        if st.button("🚀 Mulai Tes", use_container_width=True, type="primary"):
            st.session_state.page = 'form_responden'
            st.rerun()

def page_kontak():
    st.title("📞 Kontak Kami")
    
    st.markdown("""
    Terima kasih atas minat Anda terhadap Sistem Deteksi Gaya Belajar Siswa. 
    Jika Anda memiliki pertanyaan, saran, atau feedback, jangan ragu untuk menghubungi tim kami.
    """)
    
    st.markdown("---")
    
    st.markdown("### 👥 Tim Pengembang - Kelompok 3")
    
    for member in TEAM_MEMBERS:
        col1, col2 = st.columns([1, 3])
        
        with col1:
            st.markdown(create_avatar_placeholder(member['initial'], 100), unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
            <div style="background: white; padding: 1.5rem; border-radius: 12px; box-shadow: 0 4px 15px rgba(0,0,0,0.1); margin-bottom: 1rem;">
                <h4>{member['nama']}</h4>
                <p><strong>NIM:</strong> {member['nim']}</p>
                <p><strong>Peran:</strong> {member['peran']}</p>
                <p><em>Email: (akan ditambahkan)</em></p>
            </div>
            """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    st.markdown("### 📧 Informasi Kontak")
    
    st.info("""
    **Email Tim:** (akan ditambahkan)  
    **GitHub:** (akan ditambahkan)  
    **Instagram:** (akan ditambahkan)
    
    Atau Anda dapat menghubungi kami melalui dosen pembimbing mata kuliah Sistem Pakar.
    """)
    
    if st.button("← Kembali ke Beranda", use_container_width=True):
        st.session_state.page = 'home'
        st.rerun()

def page_riwayat():
    st.title("📊 Riwayat Tes")
    
    session = get_session()
    
    try:
        results = session.query(Responden, HasilAnalisis).join(
            HasilAnalisis, Responden.id == HasilAnalisis.responden_id
        ).order_by(Responden.tanggal_tes.desc()).all()
        
        if not results:
            st.info("📭 Belum ada riwayat tes. Mulai tes pertama Anda!")
            if st.button("🚀 Mulai Tes", use_container_width=True, type="primary"):
                st.session_state.page = 'form_responden'
                st.rerun()
            return
        
        st.markdown(f"Total tes yang telah dilakukan: **{len(results)}**")
        st.markdown("---")
        
        for responden, hasil in results:
            col1, col2, col3 = st.columns([2, 2, 1])
            
            with col1:
                st.markdown(f"""
                <div style="background: white; padding: 1rem; border-radius: 8px; box-shadow: 0 2px 8px rgba(0,0,0,0.1);">
                    <h4>{responden.nama}</h4>
                    <p><strong>Tanggal:</strong> {responden.tanggal_tes.strftime('%d %B %Y, %H:%M')}</p>
                    <p><strong>Usia:</strong> {responden.usia} tahun | <strong>Jenjang:</strong> {responden.jenjang_pendidikan}</p>
                </div>
                """, unsafe_allow_html=True)
            
            with col2:
                tipe_display_riwayat = hasil.tipe_dominan
                if hasil.is_tied and hasil.tied_types:
                    tied_list = hasil.tied_types.split(',')
                    other_tied = [t for t in tied_list if t != hasil.tipe_dominan]
                    if other_tied:
                        tipe_display_riwayat = f"{hasil.tipe_dominan} (Seri: {'/'.join(other_tied)})"
                
                st.markdown(f"""
                <div style="background: white; padding: 1rem; border-radius: 8px; box-shadow: 0 2px 8px rgba(0,0,0,0.1);">
                    <h4>Hasil: {tipe_display_riwayat}</h4>
                    <p>🔵 Visual: {hasil.persentase_visual:.1f}%</p>
                    <p>🟢 Auditori: {hasil.persentase_auditori:.1f}%</p>
                    <p>🟠 Kinestetik: {hasil.persentase_kinestetik:.1f}%</p>
                </div>
                """, unsafe_allow_html=True)
            
            with col3:
                st.markdown("<br>", unsafe_allow_html=True)
                if st.button(f"Lihat Detail", key=f"detail_{responden.id}", use_container_width=True):
                    st.info("Fitur detail akan segera ditambahkan")
            
            st.markdown("---")
    
    except Exception as e:
        st.error(f"❌ Terjadi kesalahan: {str(e)}")
    finally:
        session.close()
    
    if st.button("← Kembali ke Beranda", use_container_width=True):
        st.session_state.page = 'home'
        st.rerun()

def main():
    apply_custom_css()
    init_session_state()
    sidebar_menu()
    
    if st.session_state.page == 'home':
        page_home()
    elif st.session_state.page == 'form_responden':
        page_form_responden()
    elif st.session_state.page == 'kuisioner':
        page_kuisioner()
    elif st.session_state.page == 'hasil':
        page_hasil()
    elif st.session_state.page == 'tentang_gaya_belajar':
        page_tentang_gaya_belajar()
    elif st.session_state.page == 'faq':
        page_faq()
    elif st.session_state.page == 'kontak':
        page_kontak()
    elif st.session_state.page == 'riwayat':
        page_riwayat()

if __name__ == "__main__":
    main()
