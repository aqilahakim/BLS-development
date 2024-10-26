import streamlit as st
import pandas as pd
import os

# Fungsi untuk menyimpan data ke file CSV
def save_to_csv(data, filename):
    df = pd.DataFrame(data)
    df.to_csv(filename, index=False)

# Fungsi untuk memuat data dari file CSV dengan pengecekan tambahan
def load_from_csv(filename, columns, date_columns=[]):
    if os.path.exists(filename):
        try:
            df = pd.read_csv(filename)
            if not df.empty:
                # Konversi kolom tanggal dari string ke datetime
                for date_column in date_columns:
                    if date_column in df.columns:
                        df[date_column] = pd.to_datetime(df[date_column], errors='coerce')
                return df.to_dict(orient='records')
            else:
                return pd.DataFrame(columns=columns).to_dict(orient='records')
        except pd.errors.EmptyDataError:
            return pd.DataFrame(columns=columns).to_dict(orient='records')
    else:
        return pd.DataFrame(columns=columns).to_dict(orient='records')

# Inisialisasi session_state dengan kolom default untuk file CSV
if 'tasks' not in st.session_state:
    st.session_state['tasks'] = load_from_csv('tasks.csv', columns=['title', 'due_date', 'description'], date_columns=['due_date'])

if 'exams' not in st.session_state:
    st.session_state['exams'] = load_from_csv('exams.csv', columns=['title', 'exam_date', 'description'], date_columns=['exam_date'])

if 'agenda' not in st.session_state:
    st.session_state['agenda'] = load_from_csv('agenda.csv', columns=['title', 'agenda_date', 'description'], date_columns=['agenda_date'])

# Menyisipkan Google Fonts dan memperbaiki gaya teks serta latar belakang
st.markdown("""
    <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@400;600&family=Montserrat:wght@700&display=swap" rel="stylesheet">
    <style>
    body {
        font-family: 'Poppins', sans-serif;
    }
    .big-font {
        font-size:50px !important;
        color: #4CAF50;
        text-align: center;
        font-family: 'Montserrat', sans-serif;  /* Menggunakan Montserrat untuk judul */
    }
    .small-font {
        font-size:20px !important;
        color: #6C757D;
        text-align: center;
        font-family: 'Poppins', sans-serif;  /* Menggunakan Poppins untuk subjudul */
    }
    .card {
        background-color: #FFFFFF;
        color: #333333;
        padding: 20px;
        margin-bottom: 20px;
        border-radius: 10px;
        box-shadow: 2px 2px 8px rgba(0,0,0,0.1);
        font-family: 'Poppins', sans-serif;
    }
    .btn {
        background-color: #4CAF50;
        color: white;
        border: none;
        padding: 10px 20px;
        text-align: center;
        border-radius: 8px;
        cursor: pointer;
        font-family: 'Poppins', sans-serif;
    }
    .btn:hover {
        background-color: #45a049;
    }
    .task-title {
        display: flex;
        align-items: center;
        font-size: 24px;
        font-weight: 600;
        color: #333333;
    }
    .task-icon {
        margin-right: 10px;
    }
    </style>
    """, unsafe_allow_html=True)

st.markdown('<p class="big-font">BIONOVA LEARNING SYSTEM</p>', unsafe_allow_html=True)
st.markdown('<p class="small-font">📝 Sistem Manajemen Tugas, Ujian, dan Agenda Kuliah</p>', unsafe_allow_html=True)

# Fungsi untuk memperbarui UI tanpa refresh penuh
def update_ui():
    st.session_state.updated = True

# Fungsi untuk menambahkan tugas, ujian, dan agenda
def add_task(title, due_date, description):
    st.session_state['tasks'].append({
        'title': title,
        'due_date': due_date,
        'description': description
    })
    save_to_csv(st.session_state['tasks'], 'tasks.csv')
    update_ui()

def add_exam(title, exam_date, description):
    st.session_state['exams'].append({
        'title': title,
        'exam_date': exam_date,
        'description': description
    })
    save_to_csv(st.session_state['exams'], 'exams.csv')
    update_ui()

def add_agenda(title, agenda_date, description):
    st.session_state['agenda'].append({
        'title': title,
        'agenda_date': agenda_date,
        'description': description
    })
    save_to_csv(st.session_state['agenda'], 'agenda.csv')
    update_ui()

# Fungsi untuk menghapus tugas, ujian, dan agenda
def remove_task(index):
    st.session_state['tasks'].pop(index)
    save_to_csv(st.session_state['tasks'], 'tasks.csv')
    update_ui()

def remove_exam(index):
    st.session_state['exams'].pop(index)
    save_to_csv(st.session_state['exams'], 'exams.csv')
    update_ui()

def remove_agenda(index):
    st.session_state['agenda'].pop(index)
    save_to_csv(st.session_state['agenda'], 'agenda.csv')
    update_ui()

# Fungsi untuk menampilkan kalender dengan tampilan Notion-like
def show_notion_like_calendar(data, date_column, title_column, description_column):
    # Mengatasi error: konversi tipe data agar bekerja dengan baik
    data[date_column] = pd.to_datetime(data[date_column], errors='coerce')
    grouped_data = data.groupby(data[date_column].dt.date)  # Konversi ke .date untuk menghindari perbandingan antara Timestamp dan date
    for date, items in grouped_data:
        st.markdown(f"### 📅 {date.strftime('%A, %d %B %Y')}")
        for _, row in items.iterrows():
            st.markdown(f"**{row[title_column]}**")
            st.markdown(f"📋 {row[description_column]}")
            st.markdown("---")

# Sidebar navigasi
st.sidebar.header("Navigasi Halaman 📚")
page = st.sidebar.radio("Pilih halaman:", ["Tugas 📝", "Ujian 📅", "Agenda 🎓"])

icon_url = "https://img.icons8.com/ios-filled/50/000000/task.png"  # URL ikon yang sama untuk semua halaman

if page == "Tugas 📝":
    st.header("Daftar Tugas 📝")

    # Input Tugas
    col1, col2 = st.columns(2)
    with col1:
        task_title = st.text_input("Judul Tugas")
    with col2:
        task_due_date = st.date_input("Tanggal Jatuh Tempo Tugas")
    task_description = st.text_area("Keterangan Tugas")

    if st.button("Tambah Tugas", key="add_task"):
        add_task(task_title, task_due_date, task_description)
        st.success("Tugas berhasil ditambahkan!")

    # Menampilkan daftar tugas dan fitur hapus
    for i, task in enumerate(st.session_state['tasks']):
        st.markdown(f"""
        <div class="card">
            <div class="task-title">
                <img src="{icon_url}" class="task-icon" width="30"/>
                <span>{task['title']}</span>
            </div>
            <p>🗓 <b>Jatuh Tempo:</b> {task['due_date']}</p>
            <p>📋 <b>Keterangan:</b> {task['description']}</p>
        </div>
        """, unsafe_allow_html=True)

        if st.button(f"Hapus Tugas {i+1}", key=f"delete_task_{i}"):
            remove_task(i)

    # Menampilkan kalender Notion-like untuk tugas
    st.header("Kalender Tugas 🗓")
    if st.session_state['tasks']:
        tasks_data = pd.DataFrame(st.session_state['tasks'])
        show_notion_like_calendar(tasks_data, 'due_date', 'title', 'description')

elif page == "Ujian 📅":
    st.header("Daftar Ujian 📅")

    # Input Ujian
    col1, col2 = st.columns(2)
    with col1:
        exam_title = st.text_input("Judul Ujian")
    with col2:
        exam_date = st.date_input("Tanggal Ujian")
    exam_description = st.text_area("Keterangan Ujian")

    if st.button("Tambah Ujian", key="add_exam"):
        add_exam(exam_title, exam_date, exam_description)
        st.success("Ujian berhasil ditambahkan!")

    # Menampilkan daftar ujian dan fitur hapus
    for i, exam in enumerate(st.session_state['exams']):
        st.markdown(f"""
        <div class="card">
            <div class="task-title">
                <img src="{icon_url}" class="task-icon" width="30"/>
                <span>{exam['title']}</span>
            </div>
            <p>🗓 <b>Tanggal Ujian:</b> {exam['exam_date']}</p>
            <p>📋 <b>Keterangan:</b> {exam['description']}</p>
        </div>
        """, unsafe_allow_html=True)

        if st.button(f"Hapus Ujian {i+1}", key=f"delete_exam_{i}"):
            remove_exam(i)

    # Menampilkan kalender Notion-like untuk ujian
    st.header("Kalender Ujian 📅")
    if st.session_state['exams']:
        exams_data = pd.DataFrame(st.session_state['exams'])
        show_notion_like_calendar(exams_data, 'exam_date', 'title', 'description')

elif page == "Agenda 🎓":
    st.header("Daftar Agenda 🎓")

    # Input Agenda
    col1, col2 = st.columns(2)
    with col1:
        agenda_title = st.text_input("Judul Agenda")
    with col2:
        agenda_date = st.date_input("Tanggal Agenda")
    agenda_description = st.text_area("Keterangan Agenda")

    if st.button("Tambah Agenda", key="add_agenda"):
        add_agenda(agenda_title, agenda_date, agenda_description)
        st.success("Agenda berhasil ditambahkan!")

    # Menampilkan daftar agenda dan fitur hapus
    for i, item in enumerate(st.session_state['agenda']):
        st.markdown(f"""
        <div class="card">
            <div class="task-title">
                <img src="{icon_url}" class="task-icon" width="30"/>
                <span>{item['title']}</span>
            </div>
            <p>🗓 <b>Tanggal Agenda:</b> {item['agenda_date']}</p>
            <p>📋 <b>Keterangan:</b> {item['description']}</p>
        </div>
        """, unsafe_allow_html=True)

        if st.button(f"Hapus Agenda {i+1}", key=f"delete_agenda_{i}"):
            remove_agenda(i)

    # Menampilkan kalender Notion-like untuk agenda
    st.header("Kalender Agenda 🎓")
    if st.session_state['agenda']:
        agenda_data = pd.DataFrame(st.session_state['agenda'])
        show_notion_like_calendar(agenda_data, 'agenda_date', 'title', 'description')
