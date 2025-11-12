import numpy as np
from kuisioner_data import KUISIONER

class SistemPakarGayaBelajar:
    def __init__(self, jawaban_list):
        self.jawaban_list = jawaban_list
        self._hasil_cache = None
        
    def hitung_skor(self):
        skor_visual = 0
        skor_auditori = 0
        skor_kinestetik = 0
        
        for jawaban in self.jawaban_list:
            nomor = jawaban['nomor']
            nilai = jawaban['nilai']
            
            pertanyaan = next((q for q in KUISIONER if q['nomor'] == nomor), None)
            if pertanyaan:
                kategori = pertanyaan['kategori']
                
                if kategori == 'visual':
                    skor_visual += nilai
                elif kategori == 'auditori':
                    skor_auditori += nilai
                elif kategori == 'kinestetik':
                    skor_kinestetik += nilai
        
        return {
            'visual': skor_visual,
            'auditori': skor_auditori,
            'kinestetik': skor_kinestetik
        }
    
    def hitung_persentase(self, skor):
        total_skor = skor['visual'] + skor['auditori'] + skor['kinestetik']
        
        if total_skor == 0:
            return {
                'visual': 0,
                'auditori': 0,
                'kinestetik': 0
            }
        
        return {
            'visual': round((skor['visual'] / total_skor) * 100, 2),
            'auditori': round((skor['auditori'] / total_skor) * 100, 2),
            'kinestetik': round((skor['kinestetik'] / total_skor) * 100, 2)
        }
    
    def tentukan_tipe_dominan(self, skor):
        max_skor = max(skor.values())
        
        tipe_dengan_skor_max = [tipe for tipe, nilai in skor.items() if nilai == max_skor]
        
        tipe_dominan = tipe_dengan_skor_max[0].capitalize()
        is_tied = len(tipe_dengan_skor_max) > 1
        tied_types = [t.capitalize() for t in sorted(tipe_dengan_skor_max)] if is_tied else []
        
        return {
            'tipe': tipe_dominan,
            'is_tied': is_tied,
            'tied_types': tied_types
        }
    
    def analisis_lengkap(self):
        if self._hasil_cache is not None:
            return self._hasil_cache
        
        skor = self.hitung_skor()
        persentase = self.hitung_persentase(skor)
        hasil_dominan = self.tentukan_tipe_dominan(skor)
        
        self._hasil_cache = {
            'skor': skor,
            'persentase': persentase,
            'tipe_dominan': hasil_dominan['tipe'],
            'is_tied': hasil_dominan['is_tied'],
            'tied_types': hasil_dominan['tied_types']
        }
        
        return self._hasil_cache

def get_rekomendasi(tipe_dominan):
    rekomendasi = {
        'Visual': {
            'deskripsi': 'Anda adalah tipe pembelajar visual yang lebih mudah menyerap informasi melalui penglihatan. Anda cenderung mengingat apa yang dilihat dan lebih menyukai penggunaan gambar, diagram, dan visualisasi dalam proses belajar.',
            'metode_belajar': [
                'Gunakan mind map dan diagram alur untuk memahami konsep',
                'Tonton video pembelajaran dan tutorial visual',
                'Buat catatan berwarna dengan highlighter atau stabilo',
                'Gunakan flashcard dengan gambar dan ilustrasi',
                'Belajar dengan infografis dan chart',
                'Gunakan poster atau sticky notes berwarna di tempat belajar',
                'Visualisasikan konsep dalam bentuk gambar mental'
            ],
            'tools': [
                'Canva - Untuk membuat mind map dan infografis',
                'MindMeister - Aplikasi mind mapping',
                'Khan Academy - Platform dengan banyak video edukatif',
                'Quizlet - Flashcard digital dengan gambar',
                'Notion - Catatan visual dengan berbagai format'
            ],
            'tips_ujian': [
                'Visualisasikan konsep dalam bentuk diagram sebelum ujian',
                'Buat rangkuman visual dengan warna-warna berbeda',
                'Gunakan teknik memory palace (istana memori)',
                'Gambar diagram atau sketsa untuk membantu mengingat'
            ]
        },
        'Auditori': {
            'deskripsi': 'Anda adalah tipe pembelajar auditori yang lebih mudah menyerap informasi melalui pendengaran. Anda cenderung mengingat apa yang didengar dan lebih menyukai penjelasan verbal, diskusi, dan pembelajaran melalui suara.',
            'metode_belajar': [
                'Rekam penjelasan guru atau diri sendiri saat belajar',
                'Dengarkan podcast edukatif tentang materi pelajaran',
                'Belajar dalam kelompok dengan diskusi aktif',
                'Bacakan materi pelajaran dengan suara keras',
                'Gunakan musik atau ritme untuk mengingat informasi',
                'Ikuti webinar atau kuliah online dengan penjelasan audio',
                'Jelaskan materi kepada orang lain untuk memperkuat pemahaman'
            ],
            'tools': [
                'Spotify/Apple Podcasts - Podcast edukatif',
                'Voice Recorder - Merekam penjelasan',
                'YouTube - Video pembelajaran dengan penjelasan detail',
                'Audible - Audiobook untuk belajar',
                'Discord/Zoom - Diskusi kelompok online'
            ],
            'tips_ujian': [
                'Baca soal dengan suara pelan (dalam hati dengan "suara")',
                'Ingat penjelasan guru atau diskusi yang pernah dilakukan',
                'Gunakan jingle atau lagu untuk mengingat rumus/konsep',
                'Dengarkan rekaman materi sebelum ujian'
            ]
        },
        'Kinestetik': {
            'deskripsi': 'Anda adalah tipe pembelajar kinestetik yang lebih mudah menyerap informasi melalui praktik dan gerakan. Anda cenderung belajar dengan melakukan, menyentuh, dan mengalami langsung.',
            'metode_belajar': [
                'Lakukan praktik langsung atau eksperimen',
                'Gunakan model atau simulasi untuk memahami konsep',
                'Buat project atau tugas praktis terkait materi',
                'Belajar sambil bergerak atau berjalan',
                'Tulis ulang catatan dengan tangan (bukan ketik)',
                'Gunakan role-play atau simulasi situasi nyata',
                'Ambil break untuk aktivitas fisik saat belajar lama'
            ],
            'tools': [
                'Lab virtual - Simulasi eksperimen online',
                'Notion/OneNote - Menulis catatan dengan stylus',
                'PhET Simulations - Simulasi interaktif',
                'Kahoot - Quiz interaktif',
                'Minecraft Education - Belajar dengan building'
            ],
            'tips_ujian': [
                'Lakukan gerakan kecil (gerakkan kaki, putar pensil) untuk fokus',
                'Bayangkan diri Anda melakukan prosedur atau eksperimen',
                'Tulis jawaban dengan detail, jangan hanya dalam pikiran',
                'Gunakan jari untuk menghitung atau melacak langkah'
            ]
        }
    }
    
    return rekomendasi.get(tipe_dominan, rekomendasi['Visual'])
