import os

def main():
    while [e.name for e in os.scandir('waitlist') if e.is_file()]:
        target = [e.name for e in os.scandir('waitlist') if e.is_file()][0]
        print()
        print("--------------------------------")
        print()
        print(f"Processing {target} from waitlist.")
        with open(f"waitlist/{target}", 'r') as f:
            content = f.read()
        print(f"Content of {target}:\n\n<<<<<<<<<<\n\n{content}\n\n>>>>>>>>>>\n\n")
        inp = input(f"Do you want to move {target} to the garden? (y/n): ")
        if inp.lower() == 'y':
            with open(f"garden/{target}", 'w') as f:
                f.write(content)
            os.remove(f"waitlist/{target}")
            print(f"{target} has been moved to the garden.")
        else:
            print(f"{target} remains in the waitlist.")

if __name__ == "__main__":
    main()