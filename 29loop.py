import random
random_number = random.randint(1,100)
count = 0
while True:
    guess = int(input("ทายเลข: "))
    count += 1

    if guess > random_number:
        print("มากไป")
    elif guess < random_number:
        print("น้อยไป")
    else:
        print(f"ถูกต้อง! ทายไปทั้งหมด {count} ครั้ง")
    