print("คำนวณคะแนนรวม 3 วิชา")
point1 = int(input("point1"))
point2 = int(input("point2"))
point3 = int(input("point3"))
total = (point1 + point2 + point3)
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