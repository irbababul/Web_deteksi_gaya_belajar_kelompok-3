from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from datetime import datetime
import io

def generate_pdf(responden_data, hasil_analisis, rekomendasi):
    buffer = io.BytesIO()
    
    doc = SimpleDocTemplate(buffer, pagesize=A4,
                           rightMargin=72, leftMargin=72,
                           topMargin=72, bottomMargin=18)
    
    story = []
    
    styles = getSampleStyleSheet()
    
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        textColor=colors.HexColor('#667eea'),
        spaceAfter=30,
        alignment=TA_CENTER,
        fontName='Helvetica-Bold'
    )
    
    heading_style = ParagraphStyle(
        'CustomHeading',
        parent=styles['Heading2'],
        fontSize=16,
        textColor=colors.HexColor('#667eea'),
        spaceAfter=12,
        spaceBefore=12,
        fontName='Helvetica-Bold'
    )
    
    normal_style = styles['Normal']
    
    title = Paragraph("HASIL ANALISIS GAYA BELAJAR", title_style)
    story.append(title)
    story.append(Spacer(1, 0.2*inch))
    
    subtitle = Paragraph("Sistem Deteksi Gaya Belajar Siswa - Kelompok 3", styles['Normal'])
    subtitle.alignment = TA_CENTER
    story.append(subtitle)
    
    story.append(Spacer(1, 0.3*inch))
    
    story.append(Paragraph("DATA RESPONDEN", heading_style))
    
    data_responden = [
        ['Nama', ':', responden_data['nama']],
        ['Usia', ':', f"{responden_data['usia']} tahun"],
        ['Jenjang Pendidikan', ':', responden_data['jenjang_pendidikan']],
        ['Jenis Kelamin', ':', responden_data['jenis_kelamin']],
        ['Tanggal Tes', ':', datetime.now().strftime('%d %B %Y')]
    ]
    
    table = Table(data_responden, colWidths=[2*inch, 0.3*inch, 3.5*inch])
    table.setStyle(TableStyle([
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 11),
        ('TEXTCOLOR', (0, 0), (0, -1), colors.HexColor('#667eea')),
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
    ]))
    
    story.append(table)
    story.append(Spacer(1, 0.3*inch))
    
    story.append(Paragraph("HASIL DETEKSI GAYA BELAJAR", heading_style))
    
    tipe_dominan = hasil_analisis['tipe_dominan']
    persentase_dominan = hasil_analisis['persentase'][tipe_dominan.lower()]
    
    hasil_text = f"""
    <para align=center>
    <font size=18 color="#667eea"><b>TIPE GAYA BELAJAR DOMINAN:</b></font><br/>
    <font size=24 color="#764ba2"><b>{tipe_dominan.upper()}</b></font><br/>
    <font size=16>({persentase_dominan:.1f}%)</font>
    </para>
    """
    
    story.append(Paragraph(hasil_text, normal_style))
    story.append(Spacer(1, 0.2*inch))
    
    story.append(Paragraph("DISTRIBUSI SKOR", heading_style))
    
    data_skor = [
        ['Tipe Gaya Belajar', 'Skor', 'Persentase'],
        ['Visual', str(hasil_analisis['skor']['visual']), f"{hasil_analisis['persentase']['visual']:.1f}%"],
        ['Auditori', str(hasil_analisis['skor']['auditori']), f"{hasil_analisis['persentase']['auditori']:.1f}%"],
        ['Kinestetik', str(hasil_analisis['skor']['kinestetik']), f"{hasil_analisis['persentase']['kinestetik']:.1f}%"]
    ]
    
    table_skor = Table(data_skor, colWidths=[2*inch, 1.5*inch, 2*inch])
    table_skor.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#667eea')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 12),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 1), (-1, -1), 11),
    ]))
    
    story.append(table_skor)
    story.append(Spacer(1, 0.3*inch))
    
    story.append(Paragraph("TENTANG GAYA BELAJAR ANDA", heading_style))
    story.append(Paragraph(rekomendasi['deskripsi'], normal_style))
    story.append(Spacer(1, 0.2*inch))
    
    story.append(Paragraph("REKOMENDASI METODE BELAJAR", heading_style))
    
    for idx, metode in enumerate(rekomendasi['metode_belajar'], 1):
        story.append(Paragraph(f"{idx}. {metode}", normal_style))
    
    story.append(Spacer(1, 0.2*inch))
    
    story.append(Paragraph("TOOLS & APLIKASI YANG COCOK", heading_style))
    
    for idx, tool in enumerate(rekomendasi['tools'], 1):
        story.append(Paragraph(f"{idx}. {tool}", normal_style))
    
    story.append(Spacer(1, 0.2*inch))
    
    story.append(Paragraph("TIPS MENGHADAPI UJIAN", heading_style))
    
    for idx, tip in enumerate(rekomendasi['tips_ujian'], 1):
        story.append(Paragraph(f"{idx}. {tip}", normal_style))
    
    story.append(Spacer(1, 0.3*inch))
    
    footer_text = """
    <para align=center>
    <font size=10 color="gray">
    Dokumen ini digenerate oleh Sistem Deteksi Gaya Belajar Siswa<br/>
    Kelompok 3 - Mata Kuliah Sistem Pakar<br/>
    © 2025
    </font>
    </para>
    """
    
    story.append(Paragraph(footer_text, normal_style))
    
    doc.build(story)
    
    pdf_bytes = buffer.getvalue()
    buffer.close()
    
    return pdf_bytes
