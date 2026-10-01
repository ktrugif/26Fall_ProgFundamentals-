print("Hello World!!")

print("What is your name?")

def bark():
    print("Woof!")
bark()#defining a function and calling it

def details():
    print("Hello My name is Bob")
    print("i like the numbers: 1, 5, 7, 3")
    details()#defining a function and calling it

def details(name, age, height):
    print (f"{name}, is {age} years old and her height is {height} meters.")

details("Alice", 30, 1.65)
