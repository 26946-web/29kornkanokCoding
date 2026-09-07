import tkinter as tk
from tkinter import ttk, messagebox
import random
import re

class QuizApp:
    def __init__(self, root):
        self.root = root
        self.root.title("ระบบสร้างข้อสอบ & วิเคราะห์จุดแข็ง-จุดอ่อน")
        self.root.geometry("950x720")
        self.root.minsize(850, 600)
        self.root.configure(bg="#f4f6fb")

        # ------------------------------------------------------------
        # 1. คลังข้อสอบเริ่มต้น (สามารถเพิ่ม/แปลงเนื้อหาเพิ่มผ่านหน้าแอปได้)
        # ------------------------------------------------------------
        self.dataset = {
            "วิทยาศาสตร์ - การสังเคราะห์ด้วยแสง": [
                {
                    "question": "กระบวนการ Light Reaction ในพืชเกิดขึ้นที่บริเวณใดของคลอโรพลาสต์?",
                    "options": ["สโตรมา (Stroma)", "ไทลาคอยด์ (Thylakoid)", "เยื่อหุ้มชั้นนอก", "ไรโบโซม"],
                    "answer": "2"
                },
                {
                    "question": "สารใดไม่ใช่ผลิตภัณฑ์ที่ได้จากปฏิกิริยาใช้แสง (Light Reaction)?",
                    "options": ["ATP", "NADPH", "แก๊สออกซิเจน (O2)", "น้ำตาลกลูโคส"],
                    "answer": "4"
                }
            ],
            "ประวัติศาสตร์ - รัตนโกสินทร์ตอนต้น": [
                {
                    "question": "พระมหากษัตริย์พระองค์ใดทรงสถาปนากรุงเทพมหานครเป็นราชธานี?",
                    "options": ["รัชกาลที่ 1", "รัชกาลที่ 2", "รัชกาลที่ 3", "รัชกาลที่ 4"],
                    "answer": "1"
                },
                {
                    "question": "สนธิสัญญาเบอร์นีเกิดขึ้นในรัชสมัยใด?",
                    "options": ["รัชกาลที่ 1", "รัชกาลที่ 2", "รัชกาลที่ 3", "รัชกาลที่ 5"],
                    "answer": "3"
                }
            ]
        }

        self.all_questions = []
        self.current_question = 0
        self.user_answers = []
        self.performance = {}

        self.show_home()

    def clear_screen(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    # ------------------------------------------------------------
    # 2. หน้าหลัก (Home Screen)
    # ------------------------------------------------------------
    def show_home(self):
        self.clear_screen()

        title = tk.Label(
            self.root,
            text="🧠 ระบบแบบทดสอบประเมินตนเอง",
            font=("Tahoma", 24, "bold"),
            bg="#f4f6fb",
            fg="#1e293b"
        )
        title.pack(pady=(35, 5))

        subtitle = tk.Label(
            self.root,
            text="แปลงเนื้อหาเป็นข้อสอบช้อย • ทดสอบความรู้ • วิเคราะห์จุดแข็ง-จุดอ่อน",
            font=("Tahoma", 12),
            bg="#f4f6fb",
            fg="#64748b"
        )
        subtitle.pack(pady=(0, 20))

        # กล่องสรุปสถานะคลังข้อสอบ
        info = tk.Frame(self.root, bg="white", padx=30, pady=20, highlightthickness=1, highlightbackground="#cbd5e1")
        info.pack(padx=80, pady=10, fill="x")

        topic_count = len(self.dataset)
        question_count = sum(len(q) for q in self.dataset.values())

        tk.Label(info, text=f"📚 จำนวนหมวดหมู่ในคลัง: {topic_count} หมวด", font=("Tahoma", 14, "bold"), bg="white", fg="#0f172a").pack(pady=4)
        tk.Label(info, text=f"📝 จำนวนข้อสอบทั้งหมด: {question_count} ข้อ", font=("Tahoma", 14), bg="white", fg="#475569").pack(pady=4)

        # ปุ่มควบคุมหลัก
        btn_frame = tk.Frame(self.root, bg="#f4f6fb")
        btn_frame.pack(pady=25)

        start_btn = tk.Button(
            btn_frame,
            text="🚀 เริ่มทำข้อสอบ",
            font=("Tahoma", 15, "bold"),
            bg="#4f46e5",
            fg="white",
            activebackground="#4338ca",
            activeforeground="white",
            padx=35,
            pady=12,
            cursor="hand2",
            command=self.start_quiz
        )
        start_btn.pack(side="left", padx=10)

        add_btn = tk.Button(
            btn_frame,
            text="➕ ใส่เนื้อหา / แปลงเป็นข้อสอบ",
            font=("Tahoma", 15, "bold"),
            bg="#059669",
            fg="white",
            activebackground="#047857",
            activeforeground="white",
            padx=25,
            pady=12,
            cursor="hand2",
            command=self.show_add_content
        )
        add_btn.pack(side="left", padx=10)

        # รายชื่อหมวดหมู่
        list_frame = tk.Frame(self.root, bg="white", padx=20, pady=15, highlightthickness=1, highlightbackground="#cbd5e1")
        list_frame.pack(padx=80, pady=10, fill="both", expand=True)

        tk.Label(list_frame, text="📋 รายการหมวดหมู่ที่มีในระบบ:", font=("Tahoma", 12, "bold"), bg="white", fg="#1e293b", anchor="w").pack(fill="x", pady=(0, 5))
        for topic, q_list in self.dataset.items():
            tk.Label(list_frame, text=f"• {topic} ({len(q_list)} ข้อ)", font=("Tahoma", 11), bg="white", fg="#334155", anchor="w").pack(fill="x", pady=2)

    # ------------------------------------------------------------
    # 3. หน้าใส่เนื้อหาและแปลงเป็นข้อสอบ (Add Content & Converter)
    # ------------------------------------------------------------
    def show_add_content(self):
        self.clear_screen()

        header = tk.Frame(self.root, bg="#059669", height=70)
        header.pack(fill="x")
        
        tk.Label(header, text="➕ ใส่เนื้อหาและแปลงเป็นข้อสอบ", font=("Tahoma", 18, "bold"), bg="#059669", fg="white").pack(side="left", padx=25, pady=15)
        
        back_btn = tk.Button(header, text="🏠 หน้าหลัก", font=("Tahoma", 11, "bold"), bg="white", fg="#059669", cursor="hand2", command=self.show_home)
        back_btn.pack(side="right", padx=25)

        notebook = ttk.Notebook(self.root)
        notebook.pack(fill="both", expand=True, padx=30, pady=15)

        # แท็บที่ 1: ระบบแปลงเนื้อหาสรุปอัตโนมัติ
        tab1 = tk.Frame(notebook, bg="#f4f6fb", padx=20, pady=15)
        notebook.add(tab1, text="⚡ 1. แปลงสรุปเนื้อหาเป็นข้อสอบ")

        tk.Label(tab1, text="ระบุชื่อหมวดหมู่:", font=("Tahoma", 11, "bold"), bg="#f4f6fb").pack(anchor="w")
        topic_entry = tk.Entry(tab1, font=("Tahoma", 11), width=40)
        topic_entry.insert(0, "วิทยาศาสตร์ - โครงสร้างเซลล์")
        topic_entry.pack(anchor="w", pady=(2, 10))

        tk.Label(
            tab1,
            text="วางเนื้อหาสรุป (บรรทัดละข้อ ในรูปแบบ 'โจทย์/หัวข้อ = คำตอบ'):",
            font=("Tahoma", 11, "bold"),
            bg="#f4f6fb"
        ).pack(anchor="w")

        help_txt = (
            "💡 ตัวอย่างเนื้อหาที่วางได้เลย:\n"
            "ออร์กาเนลล์ที่สร้างพลังงานให้แก่เซลล์ = ไมโทคอนเดรีย\n"
            "ศูนย์กลางควบคุมการทำงานและสารพันธุกรรม = นิวเคลียส\n"
            "เยื่อหุ้มชั้นนอกสุดของเซลล์พืชที่สร้างความแข็งแรง = ผนังเซลล์"
        )
        tk.Label(tab1, text=help_txt, font=("Tahoma", 9), bg="#e2e8f0", fg="#334155", justify="left", padx=10, pady=5).pack(anchor="w", fill="x", pady=(0, 10))

        text_auto = tk.Text(tab1, font=("Tahoma", 11), height=8)
        text_auto.pack(fill="both", expand=True, pady=(0, 10))

        def process_auto():
            top = topic_entry.get().strip()
            raw = text_auto.get("1.0", tk.END).strip()

            if not top or not raw:
                messagebox.showwarning("ข้อมูลไม่ครบ", "กรุณากรอกชื่อหมวดหมู่และเนื้อหา")
                return

            gen_qs = self.auto_generate_from_text(top, raw)
            if not gen_qs:
                messagebox.showwarning("รูปแบบไม่ถูกต้อง", "ไม่พบรูปแบบ 'ข้อความ = คำตอบ' ในเนื้อหาที่กรอก")
                return

            if top not in self.dataset:
                self.dataset[top] = []
            self.dataset[top].extend(gen_qs)

            messagebox.showinfo("สำเร็จ", f"แปลงเนื้อหาและเพิ่มข้อสอบสำเร็จ {len(gen_qs)} ข้อ!")
            self.show_home()

        btn_gen = tk.Button(tab1, text="✨ แปลงเนื้อหาเป็นข้อสอบช้อย", font=("Tahoma", 12, "bold"), bg="#059669", fg="white", cursor="hand2", command=process_auto, pady=8)
        btn_gen.pack(anchor="e")

        # แท็บที่ 2: วางรูปแบบข้อสอบช้อยเต็มรูปแบบ
        tab2 = tk.Frame(notebook, bg="#f4f6fb", padx=20, pady=15)
        notebook.add(tab2, text="📝 2. วางข้อสอบรูปแบบเต็ม (Structured Text)")

        inst_txt = (
            "💡 วางข้อความรูปแบบข้อสอบช้อยสำเร็จรูป:\n"
            "[หมวด: ภาษาไทย - คำนาม]\n"
            "คำถาม: ข้อใดต่อไปนี้เป็นคำนาม?\n"
            "1. วิ่ง\n"
            "2. โรงเรียน\n"
            "3. สวยงาม\n"
            "4. อย่างรวดเร็ว\n"
            "เฉลย: 2"
        )
        tk.Label(tab2, text=inst_txt, font=("Tahoma", 9), bg="#e2e8f0", fg="#334155", justify="left", padx=10, pady=5).pack(anchor="w", fill="x", pady=(0, 10))

        text_struct = tk.Text(tab2, font=("Tahoma", 11), height=10)
        text_struct.pack(fill="both", expand=True, pady=(0, 10))

        def process_struct():
            raw = text_struct.get("1.0", tk.END).strip()
            if not raw:
                messagebox.showwarning("ข้อมูลว่างเปล่า", "กรุณากรอกข้อความก่อนกดบันทึก")
                return

            added = self.parse_structured_text(raw)
            if added > 0:
                messagebox.showinfo("สำเร็จ", f"เพิ่มข้อสอบเข้าคลังสำเร็จ {added} ข้อ!")
                self.show_home()
            else:
                messagebox.showwarning("รูปแบบไม่ถูกต้อง", "ไม่สามารถอ่านข้อสอบได้ กรุณาตรวจสอบรูปแบบ")

        btn_parse = tk.Button(tab2, text="💾 บันทึกข้อสอบเข้าคลัง", font=("Tahoma", 12, "bold"), bg="#4f46e5", fg="white", cursor="hand2", command=process_struct, pady=8)
        btn_parse.pack(anchor="e")

    # ------------------------------------------------------------
    # 4. ฟังก์ชันแปลงเนื้อหาสรุปเป็นช้อยอัตโนมัติ (Auto Converter Logic)
    # ------------------------------------------------------------
    def auto_generate_from_text(self, topic, raw_text):
        lines = [line.strip() for line in raw_text.strip().split("\n") if line.strip()]
        generated_questions = []

        default_distractors = [
            "ไมโทคอนเดรีย", "นิวเคลียส", "ไรโบโซม", "สโตรมา", "ผนังเซลล์",
            "แวคิวโอล", "ไซโทพลาซึม", "คลอโรพลาสต์", "ไลโซโซม", "กอลจิบอดี"
        ]

        all_answers = []
        pairs = []

        for line in lines:
            if "=" in line:
                parts = line.split("=", 1)
                q_text = parts[0].strip()
                ans_text = parts[1].strip()
                pairs.append((q_text, ans_text))
                all_answers.append(ans_text)

        for q_text, ans_text in pairs:
            # สุ่มสร้างตัวเลือกหลอก 3 ตัวเลือก
            other_answers = [a for a in all_answers if a != ans_text]
            for d in default_distractors:
                if len(other_answers) >= 3:
                    break
                if d != ans_text and d not in other_answers:
                    other_answers.append(d)

            distractors = random.sample(other_answers, min(3, len(other_answers)))
            options = distractors + [ans_text]
            random.shuffle(options)

            correct_idx = str(options.index(ans_text) + 1)

            generated_questions.append({
                "question": f"ข้อใดคือคำตอบที่ถูกต้องสำหรับ: '{q_text}'?",
                "options": options,
                "answer": correct_idx
            })

        return generated_questions

    def parse_structured_text(self, raw_text):
        lines = [l.strip() for l in raw_text.strip().split("\n") if l.strip()]
        curr_topic = "ทั่วไป"
        curr_q = {}
        options = []
        added_count = 0

        for line in lines:
            if line.startswith("[หมวด:") or line.startswith("[หมวดหมู่:"):
                curr_topic = line.split(":", 1)[1].replace("]", "").strip()
            elif line.startswith("คำถาม:") or line.startswith("Q:"):
                if curr_q and options and "answer" in curr_q:
                    curr_q["options"] = options
                    if curr_topic not in self.dataset:
                        self.dataset[curr_topic] = []
                    self.dataset[curr_topic].append(curr_q)
                    added_count += 1
                    curr_q = {}
                    options = []
                q_text = line.split(":", 1)[1].strip()
                curr_q = {"question": q_text}
            elif any(line.startswith(f"{i}.") for i in range(1, 5)):
                opt_text = line.split(".", 1)[1].strip()
                options.append(opt_text)
            elif line.startswith("เฉลย:") or line.startswith("Ans:"):
                ans_text = line.split(":", 1)[1].strip()
                curr_q["answer"] = ans_text

        if curr_q and options and "answer" in curr_q:
            curr_q["options"] = options
            if curr_topic not in self.dataset:
                self.dataset[curr_topic] = []
            self.dataset[curr_topic].append(curr_q)
            added_count += 1

        return added_count

    # ------------------------------------------------------------
    # 5. หน้าดำเนินแบบทดสอบ (Quiz Screen)
    # ------------------------------------------------------------
    def prepare_questions(self):
        self.all_questions = []
        for topic, questions in self.dataset.items():
            for question in questions:
                item = question.copy()
                item["topic"] = topic
                self.all_questions.append(item)
        random.shuffle(self.all_questions)

    def start_quiz(self):
        if not self.dataset:
            messagebox.showwarning("ไม่มีข้อสอบ", "ยังไม่มีข้อสอบในคลัง กรุณาเพิ่มเนื้อหาก่อนครับ")
            return
        self.prepare_questions()
        self.current_question = 0
        self.user_answers = []
        self.performance = {}
        self.show_question()

    def show_question(self):
        self.clear_screen()
        if self.current_question >= len(self.all_questions):
            self.show_result()
            return

        question_data = self.all_questions[self.current_question]

        header = tk.Frame(self.root, bg="#4f46e5", height=70)
        header.pack(fill="x")

        tk.Label(header, text="🧠 แบบทดสอบประเมินตนเอง", font=("Tahoma", 18, "bold"), bg="#4f46e5", fg="white").pack(side="left", padx=30, pady=15)
        progress_text = f"ข้อ {self.current_question + 1} / {len(self.all_questions)}"
        tk.Label(header, text=progress_text, font=("Tahoma", 14), bg="#4f46e5", fg="white").pack(side="right", padx=30)

        content_frame = tk.Frame(self.root, bg="#f4f6fb")
        content_frame.pack(fill="both", expand=True, padx=60, pady=25)

        tk.Label(content_frame, text=f"📖 หมวดหมู่: {question_data['topic']}", font=("Tahoma", 12, "bold"), bg="#f4f6fb", fg="#4f46e5").pack(anchor="w", pady=(0, 10))
        tk.Label(content_frame, text=question_data["question"], font=("Tahoma", 16, "bold"), bg="#f4f6fb", fg="#1e293b", wraplength=780, justify="left").pack(anchor="w", pady=(0, 25))

        selected_answer = tk.StringVar(value="")
        letters = ["1", "2", "3", "4"]

        for index, option in enumerate(question_data["options"]):
            radio = tk.Radiobutton(
                content_frame,
                text=f"{letters[index]}. {option}",
                variable=selected_answer,
                value=letters[index],
                font=("Tahoma", 14),
                bg="white",
                activebackground="#e0e7ff",
                selectcolor="#c7d2fe",
                anchor="w",
                padx=20,
                pady=12,
                cursor="hand2",
                wraplength=720
            )
            radio.pack(fill="x", pady=5)

        def next_question():
            answer = selected_answer.get()
            if answer == "":
                messagebox.showwarning("ยังไม่ได้เลือกคำตอบ", "กรุณาเลือกคำตอบก่อนครับ")
                return

            self.user_answers.append(answer)

            if answer == question_data["answer"]:
                messagebox.showinfo("ผลคำตอบ", "✅ ถูกต้อง!")
            else:
                correct = question_data["answer"]
                messagebox.showinfo("ผลคำตอบ", f"❌ ยังไม่ถูก\n\nคำตอบที่ถูกคือข้อ {correct}")

            self.current_question += 1
            self.show_question()

        next_button = tk.Button(
            content_frame,
            text="ดูผลคะแนน 🏆" if self.current_question == len(self.all_questions) - 1 else "ข้อต่อไป →",
            font=("Tahoma", 15, "bold"),
            bg="#4f46e5",
            fg="white",
            activebackground="#4338ca",
            activeforeground="white",
            padx=30,
            pady=10,
            cursor="hand2",
            command=next_question
        )
        next_button.pack(pady=20)

    # ------------------------------------------------------------
    # 6. หน้าแสดงจุดแข็ง-จุดอ่อน (Strengths & Weaknesses Analysis)
    # ------------------------------------------------------------
    def calculate_performance(self):
        self.performance.clear()
        for topic in self.dataset:
            self.performance[topic] = {"correct": 0, "total": 0}

        for idx, question in enumerate(self.all_questions):
            topic = question["topic"]
            user_answer = self.user_answers[idx]
            self.performance[topic]["total"] += 1
            if user_answer == question["answer"]:
                self.performance[topic]["correct"] += 1

        for topic in self.performance:
            total = self.performance[topic]["total"]
            correct = self.performance[topic]["correct"]
            if total > 0:
                self.performance[topic]["percentage"] = (correct / total) * 100
            else:
                self.performance[topic]["percentage"] = 0

    def show_result(self):
        self.calculate_performance()
        self.clear_screen()

        total = len(self.all_questions)
        correct = sum(1 for idx, q in enumerate(self.all_questions) if self.user_answers[idx] == q["answer"])
        percentage = (correct / total * 100) if total > 0 else 0

        tk.Label(self.root, text="🏆 ผลการทำแบบทดสอบ", font=("Tahoma", 24, "bold"), bg="#f4f6fb", fg="#1e293b").pack(pady=(25, 5))
        tk.Label(self.root, text=f"{correct} / {total}", font=("Tahoma", 40, "bold"), bg="#f4f6fb", fg="#4f46e5").pack()
        tk.Label(self.root, text=f"คะแนนเฉลี่ยรวม {percentage:.0f}%", font=("Tahoma", 16), bg="#f4f6fb", fg="#64748b").pack(pady=5)

        result_frame = tk.Frame(self.root, bg="#f4f6fb")
        result_frame.pack(fill="both", expand=True, padx=40, pady=15)

        strengths_frame = tk.Frame(result_frame, bg="white", padx=20, pady=15, highlightthickness=1, highlightbackground="#bbf7d0")
        strengths_frame.pack(side="left", fill="both", expand=True, padx=10)

        weaknesses_frame = tk.Frame(result_frame, bg="white", padx=20, pady=15, highlightthickness=1, highlightbackground="#fed7aa")
        weaknesses_frame.pack(side="right", fill="both", expand=True, padx=10)

        tk.Label(strengths_frame, text="💪 จุดแข็ง (ได้ >= 70%)", font=("Tahoma", 16, "bold"), bg="white", fg="#16a34a").pack(anchor="w", pady=(0, 10))
        tk.Label(weaknesses_frame, text="⚠️ จุดอ่อน (ควรทบทวน)", font=("Tahoma", 16, "bold"), bg="white", fg="#ea580c").pack(anchor="w", pady=(0, 10))

        strengths = []
        weaknesses = []

        for topic, stat in self.performance.items():
            if stat["total"] == 0:
                continue
            score = stat["percentage"]
            text = f"{topic}\nทำได้ {stat['correct']}/{stat['total']} ข้อ ({score:.0f}%)"
            if score >= 70:
                strengths.append(text)
            else:
                weaknesses.append(text)

        if not strengths:
            strengths.append("ยังไม่มีหัวข้อที่ผ่านเกณฑ์ 70%")

        if not weaknesses:
            weaknesses.append("🎉 ยอดเยี่ยม!\nคุณทำได้ดีทุกหัวข้อที่ทดสอบ")

        for item in strengths:
            tk.Label(strengths_frame, text="✅ " + item, font=("Tahoma", 11), bg="#f0fdf4", fg="#166534", justify="left", anchor="w", padx=10, pady=8, wraplength=330).pack(fill="x", pady=4)

        for item in weaknesses:
            tk.Label(weaknesses_frame, text="🔍 " + item, font=("Tahoma", 11), bg="#fff7ed", fg="#9a3412", justify="left", anchor="w", padx=10, pady=8, wraplength=330).pack(fill="x", pady=4)

        button_frame = tk.Frame(self.root, bg="#f4f6fb")
        button_frame.pack(pady=15)

        tk.Button(button_frame, text="🔄 ทำข้อสอบอีกครั้ง", font=("Tahoma", 13, "bold"), bg="#4f46e5", fg="white", padx=20, pady=10, cursor="hand2", command=self.start_quiz).pack(side="left", padx=10)
        tk.Button(button_frame, text="🏠 หน้าหลัก", font=("Tahoma", 13, "bold"), bg="white", fg="#4f46e5", padx=20, pady=10, cursor="hand2", command=self.show_home).pack(side="left", padx=10)


if __name__ == "__main__":
    root = tk.Tk()
    app = QuizApp(root)
    root.mainloop()