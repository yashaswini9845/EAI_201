def cleaning_mode(entry):
    modes = {
        1: "Turn on the simple mode.",
        2: "Turn on power mode.",
        3: "Turn on the ultra power mode."
    }
    print(modes.get(entry, "Invalid choice."))


def navigation(choice):
    if choice == "yes":
        print("Let's Start!")
        while True:
            print("\nChoose direction:")
            print("1. Left")
            print("2. Right")
            print("3. Dock")
            print("4. Stop")

            i = input("Enter your guidance: ").lower()

            if i == "left" or h == "1":
                print("Turning Left.")
            elif i == "right" or h == "2":
                print("Turning Right.")
            elif i == "dock" or h == "3":
                print("Docking...")
            elif i == "stop" or h == "4":
                print("Stopping the process.")
                break
            else:
                print("Invalid option. Try again.")
    else:
        print("Process not started. Try again.")


# Main Program
print("=== Cleaning Robot ===")
print("Enter the type of dust:")
print("1. Normal")
print("2. Small crystals or rocks")
print("3. Hard things")

try:
    entry = int(input("Enter the kind (1/2/3): "))
    cleaning_mode(entry)
except ValueError:
    print("Please enter a valid number (1/2/3).")

choice = input("Can we start? (yes/no): ").lower()
navigation(choice)
