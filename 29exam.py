print("คำนวณค่าBMI")
wieght = float(input("น้ำหนักของคุณคือ: "))
higth = float(input("ส่วนสูงของคุณคือ: "))
total = (higth*higth)
bmi = (wieght/total)
print("ค่าbmiของคุณคือ " , bmi, "หน่วย")
if bmi < 18.5 :
    print("น้ำหนักน้อย")

elif bmi < 18.5-22.9 :
    print("ปกติ")

elif bmi < 23-24.9 :
    print("น้ำหนักเกิน")

else:
    print("อ้วน")