import customtkinter as ctk
from tkinter import messagebox, filedialog
import database
import ai_helper
import ui_components
import os
import time

ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        # TIÊU ĐỀ 
        self.title("Smart Study AI - Chi Cuong") 
        self.geometry("1250x750")
        
        database.init_db()
        self.current_user = None
        self.current_role = None
        self.pomo_running = False 

        self.show_login()

    # --- LOGIN ---
    def show_login(self):
        for w in self.winfo_children(): w.destroy()
        frame = ctk.CTkFrame(self, width=400, height=500)
        frame.place(relx=0.5, rely=0.5, anchor="center")
        
        ctk.CTkLabel(frame, text="SMART STUDY LOGIN", font=("Impact", 30)).pack(pady=40)
        self.u_entry = ctk.CTkEntry(frame, width=250, placeholder_text="Username")
        self.u_entry.pack(pady=10)
        self.p_entry = ctk.CTkEntry(frame, width=250, placeholder_text="Password", show="*")
        self.p_entry.pack(pady=10)
        
        ctk.CTkButton(frame, text="Đăng Nhập", width=250, command=self.login).pack(pady=10)
        ctk.CTkButton(frame, text="Đăng Ký", width=250, fg_color="transparent", border_width=1, command=self.reg).pack(pady=5)
        self.add_footer(frame)

    def login(self):
        u, p = self.u_entry.get(), self.p_entry.get()
        user = database.login_user(u, p)
        if user:
            self.current_user = user[0]
            self.current_role = user[2]
            self.show_main()
        else: messagebox.showerror("Lỗi", "Sai tài khoản/mật khẩu")

    def reg(self):
        u, p = self.u_entry.get(), self.p_entry.get()
        role = "admin" if u == "admin" else "user"
        if database.register_user(u, p, role): messagebox.showinfo("OK", "Đăng ký thành công")
        else: messagebox.showerror("Lỗi", "Tên đã tồn tại")

    # --- GIAO DIỆN CHÍNH ---
    def show_main(self):
        for w in self.winfo_children(): w.destroy()
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.create_sidebar()
        self.create_content()
        self.show_dashboard()

    def create_sidebar(self):
        sb = ctk.CTkFrame(self, width=220, corner_radius=0)
        sb.grid(row=0, column=0, sticky="nsew")
        
        # Header Admin
        ctk.CTkLabel(sb, text=f"Hi, {self.current_user}", font=("Arial", 18, "bold")).pack(pady=20)
        
        # MENU 
        self.btn_menu(sb, "🏠 Trang Chủ / C/C++", self.show_dashboard)
        self.btn_menu(sb, "🤖 Chat AI Đa Năng", self.show_chat)
        self.btn_menu(sb, "📂 Chia Sẻ Tài Liệu", self.show_docs)
        self.btn_menu(sb, "📸 AI Vision (Ảnh)", self.show_vision)
        
        # --- CÁC TÍNH NĂNG 
        ctk.CTkLabel(sb, text="--- TIỆN ÍCH ---", text_color="gray").pack(pady=5)
        self.btn_menu(sb, "⏱️ Pomodoro Focus", self.show_pomodoro)
        self.btn_menu(sb, "📝 Ghi Chú Nhanh", self.show_notes)
        self.btn_menu(sb, "🇬🇧 Dịch Thuật AI", self.show_translate)
        self.btn_menu(sb, "📅 Lịch Thi & Deadline", self.show_events)
        
        if self.current_role == "admin":
            ctk.CTkLabel(sb, text="--- ADMIN ---", text_color="gray").pack(pady=5)
            self.btn_menu(sb, "👮 Quản Lý User (Admin)", self.show_admin, color="#cc0000")

      
        ctk.CTkButton(sb, text="Đăng Xuất", fg_color="#555555", command=self.show_login).pack(side="bottom", pady=10, padx=10, fill="x")
        self.add_footer(sb)

    def btn_menu(self, parent, text, cmd, color="transparent"):
        ctk.CTkButton(parent, text=text, anchor="w", fg_color=color, border_width=0 if color!="transparent" else 1, command=cmd).pack(pady=4, padx=10, fill="x")

    def create_content(self):
        self.main = ctk.CTkFrame(self)
        self.main.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)

    def clear(self):
        for w in self.main.winfo_children(): w.destroy()

    # --- 1. DASHBOARD C/C++ ---
    def show_dashboard(self):
        self.clear()
        ctk.CTkLabel(self.main, text="Luyện Code C/C++ & Trắc Nghiệm", font=("Arial", 24, "bold")).pack(pady=10)
        self.entry_code = ctk.CTkEntry(self.main, width=600, placeholder_text="Nhập đề bài code...")
        self.entry_code.pack(pady=5)
        ctk.CTkButton(self.main, text="Giải & Phân Tích", command=lambda: self.run_ai(self.entry_code.get(), "code")).pack(pady=5)
        self.txt_out = ctk.CTkTextbox(self.main, width=800, height=450)
        self.txt_out.pack(pady=10)

    # --- 2. POMODORO (MỚI) ---
    def show_pomodoro(self):
        self.clear()
        ctk.CTkLabel(self.main, text="Đồng Hồ Tập Trung Pomodoro", font=("Arial", 24, "bold")).pack(pady=20)
        self.lbl_timer = ctk.CTkLabel(self.main, text="25:00", font=("Impact", 100), text_color="#00FF00")
        self.lbl_timer.pack(pady=30)
        
        f = ctk.CTkFrame(self.main, fg_color="transparent")
        f.pack()
        ctk.CTkButton(f, text="Bắt Đầu", fg_color="green", width=150, height=50, command=self.start_pomo).pack(side="left", padx=10)
        ctk.CTkButton(f, text="Dừng / Reset", fg_color="red", width=150, height=50, command=self.reset_pomo).pack(side="left", padx=10)
        self.pomo_seconds = 25 * 60

    def start_pomo(self):
        if not self.pomo_running:
            self.pomo_running = True
            self.count_down()
            
    def count_down(self):
        if self.pomo_running and self.pomo_seconds > 0:
            m, s = divmod(self.pomo_seconds, 60)
            self.lbl_timer.configure(text=f"{m:02d}:{s:02d}")
            self.pomo_seconds -= 1
            self.after(1000, self.count_down)
        elif self.pomo_seconds == 0:
            self.pomo_running = False
            messagebox.showinfo("Xong!", "Hết giờ học! Hãy nghỉ giải lao.")

    def reset_pomo(self):
        self.pomo_running = False
        self.pomo_seconds = 25 * 60
        self.lbl_timer.configure(text="25:00")

    # --- 3. GHI CHÚ  ---
    def show_notes(self):
        self.clear()
        ctk.CTkLabel(self.main, text="Sổ Tay Ghi Chú", font=("Arial", 24, "bold")).pack(pady=10)
        
        f_in = ctk.CTkFrame(self.main)
        f_in.pack(fill="x", padx=20)
        self.e_note = ctk.CTkEntry(f_in, width=500, placeholder_text="Ghi nhanh ý tưởng...")
        self.e_note.pack(side="left", padx=10, pady=10)
        ctk.CTkButton(f_in, text="Lưu", width=100, command=self.save_note).pack(side="left")
        
        self.scroll_notes = ctk.CTkScrollableFrame(self.main, width=700, height=400)
        self.scroll_notes.pack(pady=20)
        self.load_notes()

    def save_note(self):
        if self.e_note.get():
            database.add_note(self.current_user, self.e_note.get())
            self.e_note.delete(0, 'end')
            self.load_notes()

    def load_notes(self):
        for w in self.scroll_notes.winfo_children(): w.destroy()
        for n in database.get_notes(self.current_user):
            # n[2] content, n[3] time, n[0] id
            c = ctk.CTkFrame(self.scroll_notes)
            c.pack(fill="x", pady=2)
            ctk.CTkLabel(c, text=f"[{n[3]}] {n[2]}", anchor="w").pack(side="left", padx=10)
            ctk.CTkButton(c, text="Xóa", width=50, fg_color="red", command=lambda id=n[0]: [database.delete_note(id), self.load_notes()]).pack(side="right")

    # --- 4. DỊCH THUẬT ---
    def show_translate(self):
        self.clear()
        ctk.CTkLabel(self.main, text="Dịch Thuật Chuyên Ngành IT", font=("Arial", 24, "bold")).pack(pady=10)
        self.e_trans = ctk.CTkTextbox(self.main, height=100, width=700)
        self.e_trans.pack(pady=10)
        self.e_trans.insert("1.0", "Paste text here to translate...")
        
        ctk.CTkButton(self.main, text="Dịch Ngay 🇬🇧 🔁 🇻🇳", command=lambda: self.run_ai(self.e_trans.get("1.0", "end"), "translate")).pack()
        
        self.txt_out = ctk.CTkTextbox(self.main, height=200, width=700)
        self.txt_out.pack(pady=10)

    # --- 5. LỊCH THI ---
    def show_events(self):
        self.clear()
        ctk.CTkLabel(self.main, text="Lịch Thi & Deadline", font=("Arial", 24, "bold")).pack(pady=10)
        f = ctk.CTkFrame(self.main)
        f.pack()
        self.e_evt = ctk.CTkEntry(f, placeholder_text="Môn thi / Deadline")
        self.e_evt.pack(side="left", padx=5)
        self.e_date = ctk.CTkEntry(f, placeholder_text="Ngày (DD/MM)")
        self.e_date.pack(side="left", padx=5)
        ctk.CTkButton(f, text="Thêm", command=self.add_evt).pack(side="left")
        
        self.scroll_evt = ctk.CTkScrollableFrame(self.main, width=500)
        self.scroll_evt.pack(pady=20)
        self.load_evts()

    def add_evt(self):
        if self.e_evt.get():
            database.add_event(self.current_user, self.e_evt.get(), self.e_date.get())
            self.load_evts()

    def load_evts(self):
        for w in self.scroll_evt.winfo_children(): w.destroy()
        for e in database.get_events(self.current_user):
            ctk.CTkLabel(self.scroll_evt, text=f"📅 {e[3]}: {e[2]}", font=("Arial", 16)).pack(anchor="w", padx=10, pady=5)
            # Thêm nút xóa nếu cần (tương tự Note)

    # --- CÁC HÀM CŨ (Chat, Vision, Docs, Admin) ---
    def show_chat(self):
        self.clear()
        ctk.CTkLabel(self.main, text="Chat AI Mentor", font=("Arial", 24)).pack(pady=10)
        self.e_chat = ctk.CTkEntry(self.main, width=600)
        self.e_chat.pack()
        ctk.CTkButton(self.main, text="Gửi", command=lambda: self.run_ai(self.e_chat.get(), "chat")).pack(pady=5)
        self.txt_out = ctk.CTkTextbox(self.main, width=800, height=400)
        self.txt_out.pack()

    def show_vision(self):
        self.clear()
        ctk.CTkLabel(self.main, text="AI Vision", font=("Arial", 24)).pack(pady=10)
        ctk.CTkButton(self.main, text="Chọn Ảnh", command=self.process_vision).pack()
        self.txt_out = ctk.CTkTextbox(self.main, width=800, height=400)
        self.txt_out.pack(pady=10)

    def show_docs(self):
        self.clear()
        ctk.CTkLabel(self.main, text="Kho Tài Liệu", font=("Arial", 24)).pack(pady=10)
        ctk.CTkButton(self.main, text="Upload File", command=self.up_doc).pack()
        self.scroll_docs = ctk.CTkScrollableFrame(self.main, width=800, height=400)
        self.scroll_docs.pack(pady=10)
        self.load_docs()

    def show_admin(self):
        self.clear()
        ctk.CTkLabel(self.main, text="ADMIN PANEL", text_color="red", font=("Arial", 24)).pack()
        for u in database.get_all_users():
            ctk.CTkLabel(self.main, text=f"User: {u[0]} | Role: {u[1]}").pack()

    # --- LOGIC XỬ LÝ CHUNG ---
    def run_ai(self, txt, mode):
        self.txt_out.delete("1.0", "end")
        self.txt_out.insert("1.0", "⏳ Đang xử lý...")
        self.update()
        res = ai_helper.ask_ai_comprehensive(txt, mode)
        self.txt_out.delete("1.0", "end")
        self.txt_out.insert("1.0", res)

    def process_vision(self):
        path = filedialog.askopenfilename()
        if path:
            self.txt_out.delete("1.0", "end")
            self.txt_out.insert("1.0", "⏳ Đang nhìn ảnh...")
            self.update()
            res = ai_helper.analyze_image_study(path, "Giải thích chi tiết")
            self.txt_out.delete("1.0", "end")
            self.txt_out.insert("1.0", res)

    def up_doc(self):
        path = filedialog.askopenfilename()
        if path:
            database.share_document(self.current_user, os.path.basename(path), path, "")
            self.load_docs()

    def load_docs(self):
        for w in self.scroll_docs.winfo_children(): w.destroy()
        for d in database.get_all_documents():
            ui_components.InfoCard(self.scroll_docs, d[2], d[3], f"By: {d[1]}", "Mở", lambda p=d[3]: os.startfile(p))

    # --- FOOTER G ---
    def add_footer(self, master):
        f = ctk.CTkFrame(master, fg_color="transparent")
        f.pack(side="bottom", pady=20)
        ctk.CTkLabel(f, text="Developed by Nguyen Chi Cuong", font=("Arial", 11, "bold")).pack()
        ctk.CTkLabel(f, text="Email: chicuong9802@gmail.com", font=("Arial", 10), text_color="gray").pack()

if __name__ == "__main__":
    app = App()
    app.mainloop()