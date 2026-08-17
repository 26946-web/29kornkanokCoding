import tkinter as tk
from tkinter import messagebox
import random


# ============================================================
# 1. คลังข้อสอบ
# ============================================================

dataset = {
    "วิทยาศาสตร์ - การสังเคราะห์ด้วยแสง": [
        {
            "question": "กระบวนการ Light Reaction ในพืชเกิดขึ้นที่บริเวณใดของคลอโรพลาสต์?",
            "options": [
                "สโตรมา (Stroma)",
                "ไทลาคอยด์ (Thylakoid)",
                "เยื่อหุ้มชั้นนอก",
                "ไรโบโซม"
            ],
            "answer": "2"
        },
        {
            "question": "สารใดไม่ใช่ผลิตภัณฑ์ที่ได้จากปฏิกิริยาใช้แสง (Light Reaction)?",
            "options": [
                "ATP",
                "NADPH",
                "แก๊สออกซิเจน (O2)",
                "น้ำตาลกลูโคส"
            ],
            "answer": "4"
        }
    ],

    "ประวัติศาสตร์ - รัตนโกสินทร์ตอนต้น": [
        {
            "question": "พระมหากษัตริย์พระองค์ใดทรงสถาปนากรุงเทพมหานครเป็นราชธานี?",
            "options": [
                "รัชกาลที่ 1",
                "รัชกาลที่ 2",
                "รัชกาลที่ 3",
                "รัชกาลที่ 4"
            ],
            "answer": "1"
        },
        {
            "question": "สนธิสัญญาเบอร์นีเกิดขึ้นในรัชสมัยใด?",
            "options": [
                "รัชกาลที่ 1",
                "รัชกาลที่ 2",
                "รัชกาลที่ 3",
                "รัชกาลที่ 5"
            ],
            "answer": "3"
        }
    ]
}


# ============================================================
# 2. ตั้งค่าหน้าต่าง
# ============================================================

root = tk.Tk()

root.title("ระบบแบบทดสอบประเมินตนเอง")

root.geometry("900x650")

root.minsize(750, 550)

root.configure(bg="#f4f6fb")


# ============================================================
# 3. ตัวแปรระบบ
# ============================================================

all_questions = []

current_question = 0

user_answers = []

performance = {}


# ============================================================
# 4. เตรียมข้อสอบ
# ============================================================

def prepare_questions():

    global all_questions

    all_questions = []

    for topic, questions in dataset.items():

        for question in questions:

            item = question.copy()

            item["topic"] = topic

            all_questions.append(item)

    random.shuffle(all_questions)


# ============================================================
# 5. ล้างหน้าจอ
# ============================================================

def clear_screen():

    for widget in root.winfo_children():

        widget.destroy()


# ============================================================
# 6. หน้าแรก
# ============================================================

def show_home():

    clear_screen()

    title = tk.Label(
        root,
        text="🧠 ระบบแบบทดสอบประเมินตนเอง",
        font=("Tahoma", 28, "bold"),
        bg="#f4f6fb",
        fg="#263238"
    )

    title.pack(pady=(60, 10))


    subtitle = tk.Label(
        root,
        text="ทดสอบความรู้ • วิเคราะห์จุดแข็ง • วิเคราะห์จุดอ่อน",
        font=("Tahoma", 14),
        bg="#f4f6fb",
        fg="#607d8b"
    )

    subtitle.pack(pady=10)


    # กล่องข้อมูล

    info = tk.Frame(
        root,
        bg="white",
        padx=30,
        pady=25
    )

    info.pack(
        padx=100,
        pady=30,
        fill="x"
    )


    topic_count = len(dataset)

    question_count = sum(
        len(q)
        for q in dataset.values()
    )


    tk.Label(
        info,
        text=f"📚 มีทั้งหมด {topic_count} หมวด",
        font=("Tahoma", 16, "bold"),
        bg="white",
        fg="#333333"
    ).pack(pady=5)


    tk.Label(
        info,
        text=f"📝 มีทั้งหมด {question_count} ข้อ",
        font=("Tahoma", 16),
        bg="white",
        fg="#333333"
    ).pack(pady=5)


    start_button = tk.Button(
        root,
        text="🚀 เริ่มทำข้อสอบ",
        font=("Tahoma", 18, "bold"),
        bg="#4f46e5",
        fg="white",
        activebackground="#4338ca",
        activeforeground="white",
        padx=50,
        pady=15,
        cursor="hand2",
        command=start_quiz
    )

    start_button.pack(pady=20)


# ============================================================
# 7. เริ่มข้อสอบ
# ============================================================

def start_quiz():

    global current_question
    global user_answers
    global performance

    prepare_questions()

    current_question = 0

    user_answers = []

    performance = {}

    show_question()


# ============================================================
# 8. แสดงข้อสอบ
# ============================================================

def show_question():

    clear_screen()

    if current_question >= len(all_questions):

        show_result()

        return


    question_data = all_questions[current_question]


    # ----------------------------
    # Header
    # ----------------------------

    header = tk.Frame(
        root,
        bg="#4f46e5",
        height=80
    )

    header.pack(
        fill="x"
    )


    tk.Label(
        header,
        text="🧠 Quiz App",
        font=("Tahoma", 20, "bold"),
        bg="#4f46e5",
        fg="white"
    ).pack(
        side="left",
        padx=30,
        pady=20
    )


    progress_text = (
        f"ข้อ {current_question + 1} "
        f"/ {len(all_questions)}"
    )


    tk.Label(
        header,
        text=progress_text,
        font=("Tahoma", 15),
        bg="#4f46e5",
        fg="white"
    ).pack(
        side="right",
        padx=30
    )


    # ----------------------------
    # เนื้อหาข้อสอบ
    # ----------------------------

    content_frame = tk.Frame(
        root,
        bg="#f4f6fb"
    )

    content_frame.pack(
        fill="both",
        expand=True,
        padx=60,
        pady=30
    )


    topic_label = tk.Label(
        content_frame,
        text=f"📖 {question_data['topic']}",
        font=("Tahoma", 13, "bold"),
        bg="#f4f6fb",
        fg="#4f46e5"
    )

    topic_label.pack(
        anchor="w",
        pady=(0, 15)
    )


    question_label = tk.Label(
        content_frame,
        text=question_data["question"],
        font=("Tahoma", 19, "bold"),
        bg="#f4f6fb",
        fg="#263238",
        wraplength=760,
        justify="left"
    )

    question_label.pack(
        anchor="w",
        pady=(0, 30)
    )


    # ----------------------------
    # ตัวเลือก
    # ----------------------------

    selected_answer = tk.StringVar(
        value=""
    )


    letters = ["1", "2", "3", "4"]


    for index, option in enumerate(
        question_data["options"]
    ):

        radio = tk.Radiobutton(
            content_frame,
            text=f"{letters[index]}. {option}",
            variable=selected_answer,
            value=letters[index],
            font=("Tahoma", 15),
            bg="white",
            activebackground="#eef2ff",
            selectcolor="#c7d2fe",
            anchor="w",
            padx=20,
            pady=15,
            cursor="hand2",
            wraplength=700
        )

        radio.pack(
            fill="x",
            pady=6
        )


    # ----------------------------
    # ปุ่มถัดไป
    # ----------------------------

    def next_question():

        answer = selected_answer.get()


        if answer == "":

            messagebox.showwarning(
                "ยังไม่ได้เลือกคำตอบ",
                "กรุณาเลือกคำตอบก่อนครับ"
            )

            return


        user_answers.append(answer)


        if answer == question_data["answer"]:

            messagebox.showinfo(
                "ผลคำตอบ",
                "✅ ถูกต้อง!"
            )

        else:

            correct = question_data["answer"]

            messagebox.showinfo(
                "ผลคำตอบ",
                f"❌ ยังไม่ถูก\n\n"
                f"คำตอบที่ถูกคือข้อ {correct}"
            )


        global current_question

        current_question += 1

        show_question()


    next_button = tk.Button(
        content_frame,
        text=(
            "ดูผลคะแนน 🏆"
            if current_question ==
            len(all_questions) - 1
            else
            "ข้อต่อไป →"
        ),
        font=("Tahoma", 16, "bold"),
        bg="#4f46e5",
        fg="white",
        activebackground="#4338ca",
        activeforeground="white",
        padx=35,
        pady=12,
        cursor="hand2",
        command=next_question
    )

    next_button.pack(
        pady=25
    )


# ============================================================
# 9. วิเคราะห์ผล
# ============================================================

def calculate_performance():

    performance.clear()


    # สร้างข้อมูลแต่ละหัวข้อ

    for topic in dataset:

        performance[topic] = {
            "correct": 0,
            "total": 0
        }


    answer_index = 0


    for question in all_questions:

        topic = question["topic"]

        user_answer = user_answers[
            answer_index
        ]

        performance[topic]["total"] += 1


        if user_answer == question["answer"]:

            performance[topic]["correct"] += 1


        answer_index += 1


    for topic in performance:

        total = performance[topic]["total"]

        correct = performance[topic]["correct"]


        if total > 0:

            performance[topic]["percentage"] = (
                correct / total
            ) * 100

        else:

            performance[topic]["percentage"] = 0


# ============================================================
# 10. หน้าแสดงผล
# ============================================================

def show_result():

    calculate_performance()

    clear_screen()


    # ----------------------------
    # หาคะแนนรวม
    # ----------------------------

    total = len(all_questions)

    correct = 0


    for index, question in enumerate(
        all_questions
    ):

        if (
            user_answers[index]
            == question["answer"]
        ):

            correct += 1


    percentage = (
        correct / total * 100
    )


    # ----------------------------
    # Header
    # ----------------------------

    tk.Label(
        root,
        text="🏆 ผลการทำแบบทดสอบ",
        font=("Tahoma", 28, "bold"),
        bg="#f4f6fb",
        fg="#263238"
    ).pack(
        pady=(35, 5)
    )


    tk.Label(
        root,
        text=f"{correct} / {total}",
        font=("Tahoma", 45, "bold"),
        bg="#f4f6fb",
        fg="#4f46e5"
    ).pack()


    tk.Label(
        root,
        text=f"คะแนน {percentage:.0f}%",
        font=("Tahoma", 18),
        bg="#f4f6fb",
        fg="#607d8b"
    ).pack(
        pady=5
    )


    # ----------------------------
    # กล่องวิเคราะห์
    # ----------------------------

    result_frame = tk.Frame(
        root,
        bg="#f4f6fb"
    )

    result_frame.pack(
        fill="both",
        expand=True,
        padx=50,
        pady=20
    )


    strengths_frame = tk.Frame(
        result_frame,
        bg="white",
        padx=20,
        pady=15
    )

    strengths_frame.pack(
        side="left",
        fill="both",
        expand=True,
        padx=10
    )


    weaknesses_frame = tk.Frame(
        result_frame,
        bg="white",
        padx=20,
        pady=15
    )

    weaknesses_frame.pack(
        side="right",
        fill="both",
        expand=True,
        padx=10
    )


    tk.Label(
        strengths_frame,
        text="💪 จุดแข็ง",
        font=("Tahoma", 18, "bold"),
        bg="white",
        fg="#16a34a"
    ).pack(
        anchor="w",
        pady=(0, 10)
    )


    tk.Label(
        weaknesses_frame,
        text="⚠️ จุดอ่อน / ควรทบทวน",
        font=("Tahoma", 18, "bold"),
        bg="white",
        fg="#ea580c"
    ).pack(
        anchor="w",
        pady=(0, 10)
    )


    strengths = []

    weaknesses = []


    for topic, stat in performance.items():

        score = stat["percentage"]

        text = (
            f"{topic}\n"
            f"{stat['correct']}/{stat['total']} "
            f"({score:.0f}%)"
        )


        if score >= 70:

            strengths.append(text)

        else:

            weaknesses.append(text)


    if not strengths:

        strengths.append(
            "ยังไม่มีหัวข้อที่ผ่านเกณฑ์ 70%"
        )


    if not weaknesses:

        weaknesses.append(
            "🎉 ยอดเยี่ยม!\n"
            "คุณทำได้ดีทุกหัวข้อ"
        )


    for item in strengths:

        tk.Label(
            strengths_frame,
            text="✅ " + item,
            font=("Tahoma", 12),
            bg="#f0fdf4",
            fg="#166534",
            justify="left",
            anchor="w",
            padx=10,
            pady=10,
            wraplength=330
        ).pack(
            fill="x",
            pady=5
        )


    for item in weaknesses:

        tk.Label(
            weaknesses_frame,
            text="🔍 " + item,
            font=("Tahoma", 12),
            bg="#fff7ed",
            fg="#9a3412",
            justify="left",
            anchor="w",
            padx=10,
            pady=10,
            wraplength=330
        ).pack(
            fill="x",
            pady=5
        )


    # ----------------------------
    # ปุ่ม
    # ----------------------------

    button_frame = tk.Frame(
        root,
        bg="#f4f6fb"
    )

    button_frame.pack(
        pady=20
    )


    tk.Button(
        button_frame,
        text="🔄 ทำข้อสอบอีกครั้ง",
        font=("Tahoma", 14, "bold"),
        bg="#4f46e5",
        fg="white",
        padx=25,
        pady=12,
        cursor="hand2",
        command=start_quiz
    ).pack(
        side="left",
        padx=10
    )


    tk.Button(
        button_frame,
        text="🏠 หน้าหลัก",
        font=("Tahoma", 14, "bold"),
        bg="white",
        fg="#4f46e5",
        padx=25,
        pady=12,
        cursor="hand2",
        command=show_home
    ).pack(
        side="left",
        padx=10
    )


# ============================================================
# 11. เริ่มโปรแกรม
# ============================================================

show_home()

root.mainloop()