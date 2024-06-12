import json
import os
import pandas as pd

OWNER_USERNAME = "owner"
OWNER_PASSWORD = "owner123"

# ფუნცქია ქმნის და ინახავს Rage Room Tbilisi-ს კვირის გრაფიკს
def create_and_save_timetable(filename="timetable.xlsx"):
    times = [f"{i}AM" for i in range(10, 12)] + [f"{i}PM" for i in range(1, 10)]
    days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    timetable = pd.DataFrame("free", index=times, columns=days)
    timetable.to_excel(filename, engine='openpyxl')

# ფუნქცია უზრუნველყოფს გრაფიკის წაკითხვას ფაილიდან
def read_timetable(filename="timetable.xlsx"):
    if os.path.exists(filename):
        try:
            timetable = pd.read_excel(filename, index_col=0, engine='openpyxl')
            return timetable
        except Exception as e:
            print(f"Error reading timetable file: {e}")
            return None
    else:
        return None

# დეკორატორი ზღუდავს წვდომას მფლობელების ფუნქციებზე
def owner_required(func):
    def wrapper(self, *args, **kwargs):
        if not self.current_owner:
            print("Access denied. This action requires owner privileges.")
            return
        return func(self, *args, **kwargs)
    return wrapper

# ვქმნი ადამიანის (Person-ის) მშობელ, base კლასს
class Person:
    def __init__(self, username, password):
        self._username = username
        self._password = password

    def get_username(self):
        return self._username

    def get_password(self):
        return self._password
    
# მომხმარებლის კლასი, რომელიც მემკვიდრეობას იღებს Person კლასიდან
class User(Person):
    filename = "users.json"

    def __init__(self, username="", password="", age=0, balance=0, orders=None):
        super().__init__(username, password)
        if orders is None:
            orders = []
        self._age = age
        self._balance = balance
        self._orders = orders

    def get_age(self):
        return self._age

    def get_balance(self):
        return self._balance

    def set_balance(self, value):
        self._balance = value

    def get_orders(self):
        return self._orders

# მონაცემებს გადავაქცევთ ლექსიკონად
    def to_dict(self):
        return {
            "username": self.get_username(),
            "password": self.get_password(),
            "age": self.get_age(),
            "balance": self.get_balance(),
            "orders": self.get_orders(),
        }
    
# მომხმარებლის მონაცემებს ვინახავთ ფაილში
    def save_to_file(self):
        try:
            users = self.load_users()
            for i, u in enumerate(users):
                if u['username'] == self.get_username():
                    users[i] = self.to_dict()
                    break
            else:
                users.append(self.to_dict())

            with open(User.filename, "w") as f:
                json.dump(users, f, indent=4)
        except Exception as e:
            print(f"An error occurred while saving user data: {e}")

# ვტვირთავთ მომხმარებლებს ფაილიდან
    def load_users(self):
        if os.path.exists(User.filename):
            with open(User.filename, "r") as f:
                try:
                    return json.load(f)
                except json.JSONDecodeError:
                    return []
        return []
    
# მოცემული ფუნქცია პოულობს მომხმარებელს username-ს და პაროლის გამოყენებით
    def find_user(self, username, password):
        users = self.load_users()
        for u in users:
            if u['username'] == username and u['password'] == password:
                return User(u['username'], u['password'], u['age'], u['balance'], u.get('orders', []))
        return None
    
# ახალ მომხმარებელს ვარეგისტრირებთ 
    def register_user(self):
        users = self.load_users()
        
        while True:
            username = input("Enter username: ")
            username_exists = False
            for u in users:
                if u['username'] == username:
                    username_exists = True
                    break

            # თუ username არსებობს, მომხმარებელს ვეუბნებით ამის შესახებ და ვთხოვთ შეიყვანოს სხვა username
            if username_exists:
                print("Username already exists. Please choose a different username.")
            else:
                break

        # პაროლის ვალიდაციას ვაკეთებთ (მინიმუმ 8 სიმბოლოსგან უნდა შედგებოდეს)
        while True:
            password = input("Enter password (minimum 8 characters): ")
            if len(password) < 8:
                print("Password must be at least 8 characters long.")
            else:
                break

        # პოტენციური ერორებისგან ვიცავთ თავს და ვალიდაციას ვაკეთებთ ასაკის შეყვანისას
        while True:
            try:
                age = int(input("Enter your age: "))
                if age <= 0:
                    print("Age must be a positive integer.")
                else:
                    break
            except ValueError:
                print("Invalid input, please enter a valid integer for age.")

        # ბალანსის მიღებასთან ერთად, ბალანსის ვალიდაციას ვახდენთ
        while True:
            try:
                balance = float(input("Enter your balance: "))
                if balance < 0:
                    print("Balance cannot be negative.")
                else:
                    break
            except ValueError:
                print("Invalid input, please enter a valid number for balance.")

        new_user = User(username, password, age, balance)
        new_user.save_to_file()
        print("User registered successfully!")
        return new_user
    
    # შევდივართ არსებული ანგარიშით (account-ით)
    def sign_in(self):
        username = input("Enter username: ")
        password = input("Enter password: ")

        user = self.find_user(username, password)
        if user:
            print(f"Welcome back, {username}!")
            return user
        
        print("Incorrect username or password. Please try again or create an account.")
        return None
    
    # მომხმარებლის ანგარიშზე შეგვაქვს თანხა
    def deposit(self, amount):
        if amount > 0:
            self._balance += amount
            self.save_to_file()
            print(f"Deposited {amount} successfully. New balance now is {self._balance}.")
        else:
            print("Deposit amount must be positive.")

# Person-ის ახალი ქვეკლასი, რომელიც განკუთვნილია ე.წ. მფლობელისთვის 
class Owner(Person):
    def __init__(self, username, password):
        super().__init__(username, password)

    def validate_password(self, password):
        return self._password == password

# ჯავშნების კლასი
class Order:
    TIMETABLE_FILE = "timetable.xlsx"
    PACKAGE_PRICES = {
        "Mozart": 25,
        "Vivaldi": 45,
        "Beethoven": 85,
        "Strauss": 135,
        "MEGA": 300,
        "2X MEGA": 500
    }

    def __init__(self, user=None):
        self.user = user
        self.timetable = self.load_timetable()
        self.current_owner = None

    # ახალი გრაფიკის ინიციალიზაცია 
    def initialize_timetable(self):
        times = [f"{i}AM" for i in range(10, 12)] + [f"{i}PM" for i in range(1, 10)]
        days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
        timetable = pd.DataFrame("free", index=times, columns=days)
        self.save_timetable(timetable)
        return timetable
    
    # ვტვირთავთ გრაფიკს ფაილიდან
    def load_timetable(self):
        if os.path.exists(Order.TIMETABLE_FILE):
            try:
                return pd.read_excel(Order.TIMETABLE_FILE, index_col=0, engine='openpyxl')
            except Exception as e:
                print(f"Error reading timetable file: {e}. Initializing new timetable.")
                return self.initialize_timetable()
        else:
            return self.initialize_timetable()
        
    # გრაფიკს ვინახავთ ფაილში
    def save_timetable(self, timetable=None):
        if timetable is None:
            timetable = self.timetable
        timetable.to_excel(Order.TIMETABLE_FILE, engine='openpyxl')

    def correct_package_name(self, package):
        corrected_package = package.title()
        return corrected_package if corrected_package in self.PACKAGE_PRICES else None
    
    # ვჯავშნით ოთახს შესაბამისი პაკეტებით
    def book_room(self, day, time_interval, packages):
        if not self.user:
            print("You need to be signed in to book a room.")
            return
        day = day.capitalize()
        time_interval = time_interval.upper()
        if day not in self.timetable.columns:
            print(f"Invalid day: {day}. Please enter a correct day (e.g., Monday).")
            return
        if time_interval not in self.timetable.index:
            print(f"Invalid time interval: {time_interval}. Please enter a correct time (e.g., 10AM).")
            return
        total_price = 0
        corrected_packages = []
        for package in packages:
            corrected_package = self.correct_package_name(package)
            if corrected_package is None:
                print(f"Invalid package: {package}.")
                return
            package_price = Order.PACKAGE_PRICES[corrected_package]
            total_price += package_price
            corrected_packages.append(corrected_package)
        if self.user.get_balance() < total_price:
            print("Insufficient balance. Please deposit more money to book these packages.")
            return
        if self.timetable.at[time_interval, day] == "free":
            self.timetable.at[time_interval, day] = f"booked ({', '.join(corrected_packages)})"
            self.user.get_orders().append((day, time_interval, corrected_packages))
            self.user.set_balance(self.user.get_balance() - total_price)
            self.user.save_to_file()
            self.save_timetable()
            package_counts = {}
            for package in corrected_packages:
                if package in package_counts:
                    package_counts[package] += 1
                else:
                    package_counts[package] = 1

            formatted_packages = []
            for package, count in package_counts.items():
                if count > 1:
                    formatted_packages.append(f"{count} {package}s")
                else:
                    formatted_packages.append(package)

            print(f"Room booked successfully for {day} at {time_interval} with packages {', '.join(formatted_packages)}!")
        else:
            print("This time slot is not available.")

    # ჯავშნის გაუქმება
    def cancel_order(self, day, time_interval):
        if not self.user:
            print("You need to be signed in to cancel an order.")
            return False
        day = day.capitalize()
        time_interval = time_interval.upper()
        for order in self.user.get_orders():
            if order[0] == day and order[1] == time_interval:
                package_names = order[2]
                refund_amount = sum(Order.PACKAGE_PRICES[package] for package in package_names)
                self.user.set_balance(self.user.get_balance() + refund_amount)
                self.user.get_orders().remove(order)
                self.timetable.at[time_interval, day] = "free"
                self.user.save_to_file()
                self.save_timetable()
                print(f"Refunded {refund_amount} GEL to your balance.")
                return True
        return False

    # ამ ფუნქციით განრიგს ვაჩვენებთ
    def display_timetable(self):
        print("\nTimetable:")
        print(self.timetable)

    # სტატისტიკის შეგროვება და ჩვენება, რომელიც განკუთვნილია მხოლოდ მფლობელებისთვის (სპეციალური username-ის და პაროლის შეყვანით)
    @owner_required
    def gather_statistics(self):
        users = User().load_users()
        if not users:
            print("No user data available.")
            return

        ages = [user['age'] for user in users]
        orders = [order for user in users for order in user['orders']]

        if not ages:
            print("No user age data available.")
            return

        if not orders:
            print("No order data available.")
            return

        most_common_age = self.most_common(ages)
        most_common_package = self.most_common([package for order in orders for package in order[2]])
        
        orders_per_day = {}
        for order in orders:
            day = order[0]
            if day not in orders_per_day:
                orders_per_day[day] = 0
            orders_per_day[day] += 1
        
        most_orders_day = max(orders_per_day, key=orders_per_day.get)
        most_orders_count = orders_per_day[most_orders_day]

        average_age = sum(ages) / len(ages)

        print("\nStatistics:")
        print(f"Most common package: {most_common_package[0]} (Count: {most_common_package[1]})")
        print(f"Most common age: {most_common_age[0]} (Count: {most_common_age[1]})")
        print(f"Average age of users: {average_age:.2f}")
        for day, count in orders_per_day.items():
            print(f"Orders on {day}: {count}")
        print(f"Day with most orders: {most_orders_day} (Count: {most_orders_count})")

    # ეს ფუნქცია გვეხმარება ვიპოვოთ ყველაზე ხშირად განმეორებადი ელემენტი სიაში
    def most_common(self, lst):
        return max(set(lst), key=lst.count), lst.count(max(set(lst), key=lst.count))

# მთავარი მენიუს გაშვების ფუნქცია
def display_menu():
    print("\nEnter 1 to see the menu")
    print("Enter 2 to create an account")
    print("Enter 3 to sign in to your account")
    print("Enter 4 to exit program")

# შექმილი იუზერისთვის განკუთვნილი მენიუს გაშვების ფუნქცია
def display_user_menu(balance):
    print("\nEnter 1 to see general timetable")
    print(f"Enter 2 to deposit money (Your current balance: {balance:.2f} GEL)")
    print("Enter 3 to book room")
    print("Enter 4 to see your orders")
    print("Enter 5 to cancel your order")
    print("Enter 6 to sign out")

# მფლობელისთვის განკუთვნილი მენიუს გაშვების ფუნქცია
def display_owner_menu():
    print("\nEnter 1 to view statistics")
    print("Enter 2 to sign out")
    print("Enter 3 to exit program")

# პაკეტების გაშვებისთვის განკუთვნილი ფუნქცია
def display_package_menu():
    print("\nRage Room Tbilisi packages menu: ")
    print("\nPackage Mozart - 25 Gel; 15 items (bottles, jars, plates)")
    print("Package Vivaldi - 45 Gel; 15 items + small gadget🛢 (bottles, plates, jars,)")
    print("Package Beethoven - 85 Gel; 30 items + small gadget🛢 (bottles, plates, jars, tiles)")
    print("Package Strauss - 135 Gel; 35 items+ standard gadget🛢 (bottles, plates, jars, tiles)")
    print("MEGA package - 300 Gel; BIG Gadget 📺 🛢 +50 items (bottles, plates, jars, tiles)")
    print("2X MEGA PACKAGE - 500 Gel; 2 HUGE Gadgets 📺 🛢 + 100 items")

# მთავარი ფუნქცია საიდანაც აპლიკაციის გაშვება ხდება
def main():
    print("\nWelcome to Rage Room Tbilisi")
    
    # ცვლადების ინიციალიზაცია ხდება მიმდინარე მომხმარებლისთვის და მფლობელისთვის
    current_user = None
    current_owner = None
    order_system = Order()

    if not os.path.exists(Order.TIMETABLE_FILE):
        create_and_save_timetable(Order.TIMETABLE_FILE)

    while True:
        # შესაბამისი მენიუს გაშვება ხდება მომხმარებლის მდგომარეობიდან გამომდინარე
        if not current_user and not current_owner:
            display_menu()
        elif current_owner:
            display_owner_menu()
        else:
            display_user_menu(current_user.get_balance())

        while True:
            # ვთხოვთ მომხმარებელს შეიყვანოს მისთვის სასურველი ბრძანება
            try:
                if not current_user and not current_owner:
                    choice = int(input("\nPlease choose an option (1-4): "))
                    # input-ის ვალიდაცია
                    if choice in [1, 2, 3, 4]:
                        break
                    else:
                        print("Invalid choice. Please enter a number between 1 and 4.")
                elif current_user:
                    # input-ის ვალიდაცია მომხმარებლისთვის
                    choice = int(input("\nPlease choose an option (1-6): "))
                    if choice in [1, 2, 3, 4, 5, 6]:
                        break
                    else:
                        print("Invalid choice. Please enter a number between 1 and 6.")
                elif current_owner:
                    choice = int(input("\nPlease choose an option (1-3): "))
                    # input-ის ვალიდაცია მფლობელისთვის
                    if choice in [1, 2, 3]:
                        break
                    else:
                        print("Invalid choice. Please enter a number between 1 and 3.")
            except ValueError:
                print("Invalid input. Please enter a valid number.")

        try:
            # კოდი მუშაობს იმის მიხედვით, როცა აპლიკაცია არის ახალი ჩართული და არც მომხმარებელია სისტემაში შესული და არც მფლობელი
            if not current_user and not current_owner:
                if choice == 1:
                    display_package_menu()
                elif choice == 2:
                    current_user = User().register_user()
                    order_system = Order(current_user)  
                elif choice == 3:
                    username = input("Enter username: ")
                    password = input("Enter password: ")
                    if username == OWNER_USERNAME and password == OWNER_PASSWORD:
                        current_owner = Owner(username, password)
                        order_system.current_owner = current_owner
                        print(f"\nWelcome back, {username}!")
                    else:
                        current_user = User().find_user(username, password)
                        if current_user:
                            order_system = Order(current_user)
                            print(f"Welcome back, {username}!")
                        else:
                            print("Incorrect username or password. Please try again or create an account.")
                elif choice == 4:
                    break
            # ეს კოდი კი უზრულველყოფს მომხმარებელს, რომელმაც sign in გაიარა, რიცხვის შეყვანით შესაბამისი მოქმედებები განახორციელოს
            elif current_user:
                if choice == 1:
                    order_system.display_timetable()
                elif choice == 2:
                    print(f"Your current balance is: {current_user.get_balance():.2f} GEL")
                    try:
                        amount = float(input("Enter the amount to deposit: "))
                        current_user.deposit(amount)
                    except ValueError:
                        print("Invalid input. Please enter a valid number for the deposit amount.")
                elif choice == 3:
                    while True:
                        # ოთახის დაჯავშნა და input-ების ვალიდაცია, მოთხოვნებთან შესაბამისად
                        day = input("Enter the day you want to book (e.g., Monday): ").capitalize()
                        if day not in order_system.timetable.columns:
                            print(f"Invalid day: {day}. Please enter a correct day (e.g., Monday).")
                            continue
                        while True:
                            time_interval = input("Enter the time interval you want to book (e.g., 10AM): ").upper()
                            if time_interval not in order_system.timetable.index:
                                print(f"Invalid time interval: {time_interval}. Please enter a correct time (e.g., 10AM).")
                            else:
                                break
                        break
                    display_package_menu()
                    packages_input = input("\nEnter the packages you want to buy (e.g 'Mozart' or 'Mozart and Vivaldi' , max 2 packages): ").strip()
                    packages = packages_input.replace(' and ', ',').split(',')
                    packages = [package.strip().title() for package in packages]

                    if len(packages) > 2:
                        print("You can only buy up to 2 packages.")
                    else:
                        valid_packages = []
                        for package in packages:
                            corrected_package = order_system.correct_package_name(package)
                            if corrected_package is None:
                                print(f"Invalid package: {package}.")
                            else:
                                valid_packages.append(corrected_package)
                        
                        if valid_packages:
                            order_system.book_room(day, time_interval, valid_packages)
                elif choice == 4:
                    orders = current_user.get_orders()
                    # მომხმარებლისთვის მათი ჯავშნების ჩვენება
                    if orders:
                        for order in orders:
                            day, time_interval, packages = order
                            print(f"Your order is on {day} at {time_interval}, package(s): {', '.join(packages)}")
                    else:
                        print("You have no orders.")
                    # ჯავშნის გაუქმება
                elif choice == 5:
                    while True:
                        day = input("Enter the day you want to cancel (e.g., Monday): ").capitalize()
                        if day not in order_system.timetable.columns:
                            print(f"Invalid day: {day}. Please enter a correct day (e.g., Monday).")
                            continue
                        while True:
                            time_interval = input("Enter the time interval you want to cancel (e.g., 10AM): ").upper()
                            if time_interval not in order_system.timetable.index:
                                print(f"Invalid time interval: {time_interval}. Please enter a correct time (e.g., 10AM).")
                            else:
                                if order_system.cancel_order(day, time_interval):
                                    print(f"Order for {day} at {time_interval} canceled successfully.")
                                else:
                                    print("This order does not exist.")
                                break
                        break
                # მიმდინარე მომხმარებლის ანგარიშიდან გამოსვლა
                elif choice == 6:
                    current_user = None
                    order_system = Order()
                    print("Signed out successfully.")

            # კოდი უზრუნველყოფს მენიუსთვის შესაბამისი ბრძანებების შესრულებას, როდესაც მფლობელი არის შესული
            elif current_owner:
                if choice == 1:
                    order_system.gather_statistics()
                elif choice == 2:
                    # მფლობელის გამოსვლა მისთის განკუთვნილი სისტემიდან
                    current_owner = None
                    order_system.current_owner = None
                    print("Signed out successfully.")
                elif choice == 3:
                    print("Exiting the program...")
                    break

        except ValueError:
            print("Invalid input. Please enter a valid number.")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    main()
