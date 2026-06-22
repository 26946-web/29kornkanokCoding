print("โปรแกรมคำนวณคะแนนรวม \n")
History = int(input("คะแนนวิชาประวิติศาสตร์ "))
Sciences = int(input("คะแนนวิชาวิทยาศาสตร์ "))
Math = int(input("คะแนนวิชาคณิตศาสตร์ "))

total = (History + Sciences + Math)
avarage = total/3
print("คะแนนรวมของคุณ \nคือ ", total, "คะแนน")
print("คะแนนเฉลี่ยของคุณ \nคือ ", avarage, "คะแนน")

if total < 60 :
    total = int(input("คะแนนรวมของคุณคือ:"))
    avarage = int(input("คะแนนเฉลี่ยของคุณคือ:"))
    print("ควรปรับปรุง")
elif total < 80 :
    print("ดีเยี่ยม")
else:
    print("ดีเยี่ยม")