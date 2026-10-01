def check_number(number):
    if number % 2 == 0:
        return "even"
    else:
        return "odd"

# Ask the user to enter a whole number
user_input = input("Enter a whole number: ")

# Convert the input string to an integer
num = int(user_input)

# Call the function and store the result
result = check_number(num)

# Print the final sentence using an f-string
print(f"{num} is an {result} number.")
