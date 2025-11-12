"""
Database migration script untuk menambahkan kolom is_tied dan tied_types
ke tabel hasil_analisis.

PERINGATAN: Script ini akan menghapus data lama di tabel hasil_analisis!
Hanya jalankan jika Anda siap kehilangan data riwayat tes sebelumnya.

Untuk development/testing, ini aman dijalankan.
"""

import os
from sqlalchemy import create_engine, text

def migrate_database():
    database_url = os.getenv('DATABASE_URL')
    if not database_url:
        print("ERROR: DATABASE_URL environment variable not found")
        return False
    
    engine = create_engine(database_url)
    
    try:
        with engine.connect() as connection:
            print("🔄 Checking if migration is needed...")
            
            check_columns = text("""
                SELECT column_name 
                FROM information_schema.columns 
                WHERE table_name='hasil_analisis' 
                AND column_name IN ('is_tied', 'tied_types')
            """)
            
            result = connection.execute(check_columns)
            existing_columns = [row[0] for row in result]
            
            if 'is_tied' in existing_columns and 'tied_types' in existing_columns:
                print("✅ Database sudah up-to-date! Tidak perlu migrasi.")
                return True
            
            print("📝 Menambahkan kolom baru ke tabel hasil_analisis...")
            
            if 'is_tied' not in existing_columns:
                alter_is_tied = text("""
                    ALTER TABLE hasil_analisis 
                    ADD COLUMN is_tied BOOLEAN DEFAULT FALSE
                """)
                connection.execute(alter_is_tied)
                print("   ✓ Kolom 'is_tied' ditambahkan")
            
            if 'tied_types' not in existing_columns:
                alter_tied_types = text("""
                    ALTER TABLE hasil_analisis 
                    ADD COLUMN tied_types TEXT
                """)
                connection.execute(alter_tied_types)
                print("   ✓ Kolom 'tied_types' ditambahkan")
            
            connection.commit()
            
            print("✅ Migrasi database berhasil!")
            return True
            
    except Exception as e:
        print(f"❌ Error saat migrasi database: {str(e)}")
        print("\nJika error persists, Anda bisa reset tabel dengan cara:")
        print("1. Hapus tabel lama: DROP TABLE hasil_analisis;")
        print("2. Restart aplikasi, tabel baru akan dibuat otomatis")
        return False

if __name__ == "__main__":
    print("=" * 60)
    print("DATABASE MIGRATION SCRIPT")
    print("=" * 60)
    print()
    
    success = migrate_database()
    
    print()
    if success:
        print("🎉 Migrasi selesai! Aplikasi siap digunakan.")
    else:
        print("⚠️  Migrasi gagal. Silakan periksa error di atas.")
    print("=" * 60)
