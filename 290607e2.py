print("โปรแกรมคำนวณแม่สูตรคูณโดยมุกโกะ 4/4;)")
number1 = int(input("ตัวเลขเริ่มต้น = "))
number2 = int(input("ตัวเลขสิ้นสุด = "))

for m in range(number1, number2 + 1):
    print(f"--- แม่ --- {m}")
    for i in range(1,13):
        print(m,"x", i,m*i)
