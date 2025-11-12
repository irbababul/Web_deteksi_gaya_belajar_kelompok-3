import os
from sqlalchemy import create_engine, Column, Integer, String, DateTime, Text, Float, LargeBinary, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
import streamlit as st

Base = declarative_base()

class Responden(Base):
    __tablename__ = 'responden'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    nama = Column(String(255), nullable=False)
    usia = Column(Integer, nullable=False)
    jenjang_pendidikan = Column(String(100), nullable=False)
    jenis_kelamin = Column(String(20), nullable=False)
    foto = Column(LargeBinary, nullable=True)
    tanggal_tes = Column(DateTime, default=datetime.now)

class Jawaban(Base):
    __tablename__ = 'jawaban'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    responden_id = Column(Integer, nullable=False)
    nomor_pertanyaan = Column(Integer, nullable=False)
    nilai_jawaban = Column(Integer, nullable=False)
    kategori = Column(String(50), nullable=False)
    tanggal_jawab = Column(DateTime, default=datetime.now)

class HasilAnalisis(Base):
    __tablename__ = 'hasil_analisis'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    responden_id = Column(Integer, nullable=False)
    skor_visual = Column(Float, nullable=False)
    skor_auditori = Column(Float, nullable=False)
    skor_kinestetik = Column(Float, nullable=False)
    persentase_visual = Column(Float, nullable=False)
    persentase_auditori = Column(Float, nullable=False)
    persentase_kinestetik = Column(Float, nullable=False)
    tipe_dominan = Column(String(50), nullable=False)
    is_tied = Column(Boolean, default=False)
    tied_types = Column(Text, nullable=True)
    tanggal_analisis = Column(DateTime, default=datetime.now)

@st.cache_resource
def get_database_engine():
    database_url = os.getenv('DATABASE_URL')
    if not database_url:
        raise ValueError("DATABASE_URL environment variable not found")
    engine = create_engine(database_url, pool_pre_ping=True)
    return engine

def init_database():
    engine = get_database_engine()
    Base.metadata.create_all(engine)
    return engine

def get_session():
    engine = get_database_engine()
    Session = sessionmaker(bind=engine)
    return Session()
