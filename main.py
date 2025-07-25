import re
import uuid as ud
from datetime import datetime as dt
import os
from typing import List
import json
import time as t

# creating a main function which runs the code
def main():
    print("\n\t\tWelcome To Your Trusted Bank System")
    print("\t====================================================")

    check_login = CheckLogin()
    check_login.check_login()

    if check_login.exit:
        return

    userDetails = UserDetails()

    # call the function based on user input
    if check_login.is_login:
        userDetails.login_account()

        if userDetails.is_return:
            return

        convert_save = ConvertAndSave(
            userDetails.user_id,
            userDetails.user_name,
            userDetails.user_password,
            userDetails.registered_at,
            check_login.is_login,
        )

        convert_save.save_to_file()

    else:
        userDetails.create_account()
        # save the record in a file
        convert_save = ConvertAndSave(
            userDetails.user_id,
            userDetails.user_name,
            userDetails.user_password,
            userDetails.registered_at,
            check_login.is_login,
            userDetails.user_balance,
        )
        convert_save.save_to_file()

    while True:
        bank = Bank(userDetails)
        bank.print_options()
        bank.call_method()

        if bank.exit:
            break


class CheckLogin:

    def __init__(self) -> None:
        self.options: List[str] = [
            "Log in (already have account)",
            "Sign up (create a new account)",
        ]
        self.is_login: bool = False  # to check if the user login
        self.exit: bool = False

    # function which asks the user for login or signup
    def check_login(self):
        while True:
            print("\nCreate or Login to your account:")
            for i, opt in enumerate(self.options, start=1):
                print(f"\n{i}. {opt}.")

            user_input = input("\nEnter the option number(0 for exit): ")

            # if the input is not null and it's a number
            if user_input and user_input.isdigit():
                user_input = int(user_input)

                if user_input == 1:
                    self.is_login = True
                    break
                elif user_input == 2:
                    self.is_login = False
                    break
                elif user_input == 0:
                    self.exit = True
                    print("\n\tYou have exit from the Bank.")
                    break
                else:
                    print("Enter a valid number please!")

            else:
                print("Account is required to proceed! Enter a number please.\n")


class UserDetails:

    # first asks the user for their account name and password and assign a custom id to them
    def __init__(self) -> None:
        self.user_id: str = ""
        self.user_name: str = ""
        self.user_balance: float = 0
        self.user_password: str = ""
        self.registered_at: str = ""
        self.is_return: bool = False

    # method to check if the name exists in the users.json file
    def _check_name(self, user_name: str) -> bool:
        # check if the name is already taken, first check if the file exists
        if os.path.exists("users.json") and os.path.getsize("users.json") > 0:
            with open("users.json", "r") as f:
                try:
                    users = json.load(f)
                    signups = users.get("Signups", [])
                    for user in signups:
                        # check for name only
                        if user.get("user_name", "").lower() == user_name.lower():
                            return True
                except json.JSONDecodeError:
                    print("an error occured!")
        return False

    # method to check if the password is valid for a specific user_name in the users.json file
    def _check_pass(self, user_name: str, user_pass: str) -> bool:
        # check if the name and password are correct, first check if the file exists
        if os.path.exists("users.json") and os.path.getsize("users.json") > 0:
            with open("users.json", "r") as f:
                try:
                    users = json.load(f)
                    signups = users.get("Signups", [])
                    for user in signups:
                        # check for name only
                        if (
                            user.get("user_name", "").lower() == user_name.lower()
                            and user.get("user_password", "").lower()
                            == user_pass.lower()
                        ):
                            return True
                except json.JSONDecodeError:
                    print("an error occured!")
        return False

    # method to check if the password is already exists for any user_name
    def _check_all_pass(self, user_pass: str) -> bool:
        # check for file
        if os.path.exists("users.json") and os.path.getsize("users.json") > 0:
            with open("users.json", "r") as f:
                try:
                    users = json.load(f).get(
                        "Signups", []
                    )  # obtain all the data from users file
                    for user in users:
                        if (
                            user.get("user_password", "").lower() == user_pass.lower()
                        ):  # if the password exists return true
                            return True
                except json.JSONDecodeError:
                    pass
        return False

    # method which creates a new account
    def create_account(self):
        print("\n\tStart creating your account")
        # store name
        while True:
            user_input = input("\nEnter Your Account Name(use only letters): ").strip()
            if user_input:

                # check if the name is valid
                if re.match(r"^[A-Za-z]{3,}$", user_input):
                    name_exists = self._check_name(user_input)

                    # check for name in the file
                    if name_exists:
                        print("This name is already taken. Please choose another one!")
                    else:
                        self.user_name = user_input.title()
                        break

                else:
                    print(
                        "Name cannot have numbers, spaces, any special characters and must have 3 characters!"
                    )
            else:
                print("Name is required!")

        # store password
        while True:
            print(f"\n\t{self.user_name} please add a password to your account")
            user_input = input("\nEnter your password(must be 4 characters): ")
            if user_input:
                if re.match(r"^.{4,10}$", user_input):
                    pass_exists = self._check_all_pass(user_input)

                    if pass_exists:
                        print("Please change your password. It is already taken!")
                    else:
                        self.user_password = user_input
                        break
                else:
                    print("Password can include maximum 10 characters")
            else:
                print("Password is required!")

        # generate a unique id for each user
        self.user_id = str(ud.uuid4())

        # set the account balance
        while True:
            print(f"\n\t{self.user_name} please set your account balance")
            user_input = input("\nEnter your account balance(by default 0): ").strip()

            if user_input:

                if re.match(r"^\d+(\.\d{1,2})?$", user_input):
                    self.user_balance = int(user_input)
                    print(
                        f"\n\t{self.user_name} your current account balance is {self.user_balance}Rs."
                    )
                    break
                else:
                    print("Enter a valid balance please!")
            else:
                default_balance = (
                    input("\nDo you want to set your account balance 0(y/n): ")
                    .strip()
                    .lower()
                )
                if default_balance == "y":
                    self.user_balance = 0
                    print(
                        f"\t{self.user_name} your current account balance is {self.user_balance}Rs."
                    )
                    break

                elif default_balance == "n":
                    pass

        # set register date and time
        self.registered_at = dt.now().strftime("%Y-%m-%d %H:%M:%S")

        print("\nYour account details has saved to 'users.json' file.")

    # method to login in a previous account
    def login_account(self):
        print("\n\tLogin to your account")

        # generate the time of login
        self.registered_at = dt.now().strftime("%Y-%m-%d %H:%M:%S")

        # generate a unique id
        self.user_id = str(ud.uuid4())

        # store name
        counts = 3
        while True:
            if counts == 0:
                print(
                    "\nToo much unsuccessful attempts! wait for 10 seconds then retry"
                )
                t.sleep(10)
                counts = 3

            user_input = input(
                "\nEnter Your Account Name(use only letters, 0 for exit): "
            ).strip()

            if user_input == "0":
                self.is_return = True
                print("\n\tYou have exit from the bank!")
                return

            if user_input:
                # check if the name is valid
                if re.match(r"^[A-Za-z]{3,}$", user_input) and counts >= 1:
                    name_exists = self._check_name(user_input)  # check if the exists

                    if name_exists:
                        self.user_name = user_input.title()
                        counts = 3
                        break
                    else:
                        counts = counts - 1  # decrease the count
                        print(
                            f"No user_name found! Please check your user_name or Sign up (You have {counts} more attempts)."
                        )
                else:
                    print(
                        "Name cannot have numbers, spaces, any special characters and must have 3 characters!"
                    )

            else:
                print("Name is required!")

        # store password
        while True:
            if counts == 0:
                print(
                    "\nToo much unsuccessful attempts! wait for 10 seconds then retry"
                )
                t.sleep(10)
                counts = 3

            user_input = input("\nEnter your password(must be 4 characters): ")
            if user_input:
                # check if the password is valid
                if re.match(r"^.{4,10}$", user_input) and counts >= 1:
                    pass_valid = self._check_pass(self.user_name, user_input)
                    # check if the password is correct
                    if pass_valid and counts >= 1:
                        print(
                            f"\n  Successfully Login! Welcome Back '{self.user_name.title()}'."
                        )
                        self.user_password = user_input
                        break
                    else:
                        counts -= 1
                        print(
                            f"Password is incorrect! You have {counts} more attempts then it locks for 10 seconds."
                        )

                else:
                    print("Password can include maximum 10 characters")
            else:
                print("Password is required!")


class ConvertAndSave:

    def __init__(
        self,
        user_id: str,
        user_name: str,
        user_password: str,
        registered_at: str,
        Login: bool,
        user_balance: float = 0,
    ) -> None:
        self.user_id: str = user_id
        self.user_name: str = user_name
        self.user_password: str = user_password
        self.user_balance: float = user_balance
        self.registered_at: str = registered_at
        self.Login: bool = Login

    # convert the user details in to a dictionary for new account
    def _to_dict_signup(self):
        return {
            "user_id": self.user_id,
            "user_name": self.user_name,
            "user_password": self.user_password,
            "user_balance": self.user_balance,
            "registered_at": self.registered_at,
        }

    # convert and save the data for login details
    def _to_dict_login(self):
        return {
            "user_id": self.user_id,
            "user_name": self.user_name,
            "user_password": self.user_password,
            "registered_at": self.registered_at,
        }

    # function to store the user details in a json file
    def save_to_file(self, filename="users.json"):
        user_data_signup = self._to_dict_signup()
        user_data_login = self._to_dict_login()

        # Structure to hold both signup and login records
        data = {
            "Signups": [],
            "Logins": [],
            "Deposits": [],
            "WithDrawals": [],
            "FastCash": [],
        }

        # if the file exists and is not empty
        try:
            # obtain the json list of userdetails
            with open(filename, "r") as f:
                data = json.load(f)

        except (FileNotFoundError, json.JSONDecodeError):
            pass  # fallback to default data structure that I created above

        # Append current user to the correct section
        if self.Login:
            data["Logins"].append(user_data_login)
        else:
            data["Signups"].append(user_data_signup)

        # now add the data to users.json file
        with open(filename, "w") as f:
            json.dump(data, f, indent=4)


class LoadAndSaveDataMixin:

    def __init__(self):
        if type(self) is LoadAndSaveDataMixin:
            raise TypeError("This is a mixin and cannot be instantiated directly.")

    # method to load the data from users.json file
    def _load_user_data(self):
        # check for file
        if os.path.exists("users.json") and os.path.getsize("users.json") > 0:
            with open("users.json", "r") as f:
                data = json.load(f)  # get the whole data inside the file
                return data
        else:
            print("File not found! or maybe empty")

    # method to save the user data into users.json file
    def _save_user_data(self, data: dict) -> None:
        with open("users.json", "w") as f:
            json.dump(data, f, indent=4)


class Deposit(LoadAndSaveDataMixin):

    def __init__(self, user_name: str) -> None:
        self.user_name = user_name

    # method which returns the deposit value
    def _asks_deposit_amount(self) -> float | None:
        while True:
            user_input = input("\nEnter your deposit amount: ").strip()

            # if user won't enter anything ask again
            if not user_input:
                print("Please add some amount to deposit!")
                continue  # go to the first statement of the loop

            try:
                amount = float(user_input)
                if amount < 1:
                    print("Deposit must atleast 1 or more than it!")
                    continue

                return amount  # safely return amount
            except ValueError:
                print("Please enter a valid amount to deposit!")

    # method which created a dictinary of deposit details
    def _create_deposit_dict(self, amount: float):
        __id = ud.uuid4()
        return {
            "id": str(__id),
            "user_name": self.user_name,
            "deposit_amount": amount,
            "deposit_time": dt.now().strftime("%Y-%m-%d %H:%M:%S"),
        }

    # final method to add deposit in the user_balance inside signups and update the deposits record
    def add_deposit(self):
        amount = self._asks_deposit_amount()
        old_balance = 0

        if not amount:
            return

        print("\n\tDepositing your balance...")
        t.sleep(2)

        # load the data from file
        data = self._load_user_data()

        if not data:
            raise RuntimeError("Failed to load the user data from file!")
            return

        # updating the balance in singpups
        for user in data.get("Signups", []):
            if self.user_name.lower() == user.get("user_name", "").lower():
                user["user_balance"] = user.get("user_balance", 0) + amount
                old_balance = user.get("user_balance", 0) - amount
                break

        # create and store deposit record
        deposit_record = self._create_deposit_dict(amount)
        data["Deposits"].append(deposit_record)

        # save updated data
        try:
            self._save_user_data(data)
        except Exception as e:
            print(f"error saving data: {e}")
            return

        # change the time format into 12 hours
        deposit_time = dt.strptime(deposit_record["deposit_time"], "%Y-%m-%d %H:%M:%S")
        formatted_time = deposit_time.strftime("%Y-%m-%d %I:%M:%S:%p")
        new_balance = old_balance + deposit_record["deposit_amount"]  # after deposit

        # show confirmation
        print(
            f"""
        \tDeposit Successful!
        \n\tUser Name       :  {self.user_name.title()}.
        \n\tAccount Balance :  {old_balance} Rs -> {new_balance} Rs.
        \n\tTime            :  {formatted_time}.
        """
        )
        print(
            f"\nYou have deposited {deposit_record['deposit_amount']} Rs. Currect account balance is: {new_balance} Rs."
        )
        t.sleep(10)


class Withdrawal(LoadAndSaveDataMixin):

    def __init__(self, user_name: str) -> None:
        self.user_name = user_name

    # method which returns the withdrawal value
    def _asks_withdrawal_amount(self) -> float | None:
        while True:
            user_input = input("\nEnter your withdrawal amount: ").strip()

            # if user won't enter anything ask again
            if not user_input:
                print("Please add some amount to withdrawal!")
                continue  # go to the first statement of the loop

            try:
                amount = float(user_input)
                if amount < 1:
                    print("withdrawal must atleast 1 or more than it!")
                    continue

                return amount  # safely return amount
            except ValueError:
                print("Please enter a valid amount to withdrawal!")

    # method which created a dictinary of witdrawal details
    def _create_withdrawal_dict(self, amount: float):
        __id = ud.uuid4()
        return {
            "id": str(__id),
            "user_name": self.user_name,
            "withdrawal_amount": amount,
            "withdrawal_time": dt.now().strftime("%Y-%m-%d %H:%M:%S"),
        }

    # final method to withdraw money from the user_balance inside signups and update the withdrawal record
    def withdraw_money(self):
        amount = self._asks_withdrawal_amount()
        old_balance = 0

        if not amount:
            return

        print("\n\tChecking your balance...")
        t.sleep(2)

        # load the data from file
        data = self._load_user_data()

        if not data:
            raise RuntimeError("Failed to load the user data from file!")
            return

        # updating the balance in singpups
        for user in data.get("Signups", []):
            if self.user_name.lower() == user.get("user_name", "").lower():
                if amount > user.get("user_balance", 0):
                    print("\n\tSorry you don't have enough balance to withdraw!")
                    return
                user["user_balance"] = user.get("user_balance", 0) - amount
                old_balance = user.get("user_balance", 0) + amount
                break

        # create and store deposit record
        Withdrawal_record = self._create_withdrawal_dict(amount)
        data["WithDrawals"].append(Withdrawal_record)

        # save updated data
        try:
            self._save_user_data(data)
        except Exception as e:
            print(f"error saving data: {e}")
            return

        # change the time format into 12 hours
        Withdrawal_time = dt.strptime(
            Withdrawal_record["withdrawal_time"], "%Y-%m-%d %H:%M:%S"
        )
        formatted_time = Withdrawal_time.strftime("%Y-%m-%d %I:%M:%S:%p")
        new_balance = old_balance - amount  # after withdrawal

        # show confirmation
        print(
            f"""
        \tWithdraw Successful!
        \n\tUser Name       :  {self.user_name.title()}.
        \n\tAccount Balance :  {old_balance} Rs -> {new_balance} Rs.
        \n\tTime            :  {formatted_time}.
        """
        )
        print(
            f"\nYou have withdrawal {Withdrawal_record['withdrawal_amount']} Rs. Currect account balance is: {new_balance} Rs."
        )
        t.sleep(10)


class FastCash(LoadAndSaveDataMixin):

    def __init__(self, user_name: str) -> None:
        self.user_name: str = user_name
        self.fastcash_amounts: List[int] = [5000, 10000, 20000, 40000, 50000]

    # method which create the fastcash dictionary
    def create_fastcash_dict(self, amount: int):
        __id = ud.uuid4()
        return {
            "id": str(__id),
            "user_name": self.user_name,
            "fastcash_amount": amount,
            "time": dt.now().strftime("%Y-%m-%d %H:%M:%S"),
        }

    # method to print the fast cash amounts
    def print_fastcash(self):
        print("\n\tFast Cash Amounts:")
        print("=====================================")
        for i, opt in enumerate(self.fastcash_amounts, start=1):
            print(f"\n{i}. {opt: ,}.")

    # method which returns the fast cash amount
    def get_fastcash_num(self):
        while True:
            self.print_fastcash()
            user_input = input("\nEnter the option number(0 for return): ")

            if user_input and user_input.isdigit():
                index = int(user_input)
                if 1 <= index <= len(self.fastcash_amounts):
                    amount = self.fastcash_amounts[index - 1]
                    return amount
                    break

                elif index == 0:
                    return None

                else:
                    print("Enter a valid number please!")
            else:
                print("Enter a positive number please!")

    # method to update the user_balance inside signups and create fastcash record
    def withdraw_fastcash(self):
        amount = self.get_fastcash_num()  # method which returns the fast cash amount
        old_balance = 0

        if not amount:
            return

        print("\n\tChecking your balance...")
        t.sleep(2)

        # load the data from file
        data = self._load_user_data()
        if not data:
            print("File is empty!")
            return

        # updating the user_balance inside signups
        signups = data.get("Signups", [])
        for user in signups:
            if self.user_name.lower() == user.get("user_name", "").lower():
                if amount > user.get("user_balance", 0):
                    print("\nSorry you don't have enough balance!")
                    return

                user["user_balance"] = user.get("user_balance", 0) - amount
                old_balance = user.get("user_balance", 0) + amount
                break

        # creating fastcash dictionary and store it in the file
        fastcash_dict = self.create_fastcash_dict(amount)
        data["FastCash"].append(fastcash_dict)

        # saving the changes in the file
        try:
            self._save_user_data(data)
        except Exception as e:
            print(f"An error occured: {e}")
            return

        # change the time into 12 hours format
        old_time = dt.strptime(fastcash_dict["time"], "%Y-%m-%d %H:%M:%S")
        formatted_time = old_time.strftime("%Y-%m-%d %I:%M:%S:%p")
        new_balance = old_balance - amount

        # show confirmation
        print(
            f"""
        \tWithdraw Successful!
        \n\tUser Name       :  {self.user_name}.
        \n\tAccount Balance :  {old_balance} Rs -> {new_balance} Rs.
        \n\tTime            :  {formatted_time}.
        """
        )
        print(
            f"\nYou have withdrawal {fastcash_dict['fastcash_amount']} Rs. Currect account balance is: {new_balance} Rs."
        )
        t.sleep(10)


class Bank:

    def __init__(self, user_details: UserDetails) -> None:
        self._options: List[str] = [
            "Check Balance",
            "Deposit",
            "Withdrawal",
            "FastCash",
            "Exit",
        ]
        self.user_details: UserDetails = user_details
        self.deposit: Deposit = Deposit(user_details.user_name)  # tightly coupled
        self.withdraw: Withdrawal = Withdrawal(user_details.user_name)
        self.fastcash: FastCash = FastCash(user_details.user_name)
        self.exit: bool = False

    # method to print all the options line by line
    def print_options(self):
        print(f"\n\t Your Bank Account'{self.user_details.user_name.title()}'.")
        print("===========================================")

        for i, opt in enumerate(self._options, start=1):
            print(f"\n{i}. {opt.title()}.")

    # method which returns option number entered by the user
    def _option_num(self):
        while True:
            user_input = input("\nEnter the option number: ")

            if user_input and user_input.isdigit():
                num = int(user_input)
                if 1 <= num <= len(self._options):
                    return num
                    break
                else:
                    print("Enter a valid number please!")
                    self.print_options()
            else:
                print("Enter any positive number please!")
                self.print_options()

    # method which checks the user balance from users.json file
    def _check_balance(self):
        global balance, last_edit
        balance = 0
        last_edit = 0

        # check for the file
        if os.path.exists("users.json") and os.path.getsize("users.json") > 0:
            # open the file
            with open("users.json", "r") as f:
                data = json.load(f)  # store all the data
                # filter the data to store the signups array
                users = data.get("Signups", [])

                for user in users:  # check the whole data
                    if (
                        user.get("user_name", "").lower()
                        == self.user_details.user_name.lower()
                    ):
                        balance = user.get("user_balance", "")
                        last_edit = user.get("registered_at", "")  # actual date time
                        # filter the data to store the signups array
                        date_time = dt.strptime(last_edit, "%Y-%m-%d %H:%M:%S")
                        # convert it in 12 hour
                        last_edit = date_time.strftime("%Y-%m-%d %I:%M:%S %p")
                        break
        else:
            print("No file found! 'users.json'.")

        print("\nChecking your balance (wait for few seconds).")
        t.sleep(2)
        details = f"""\n\tYour current account balance is: {balance} Rs.
        \n\tLast edit at: {last_edit}."""
        print(details)

    # method which calls the other methods based on user input number
    def call_method(self):
        option_num = self._option_num()

        if option_num == 1:
            self._check_balance()

        elif option_num == 2:
            self.deposit.add_deposit()

        elif option_num == 3:
            self.withdraw.withdraw_money()

        elif option_num == 4:
            self.fastcash.withdraw_fastcash()

        elif option_num == 5:
            print("\nExiting...")
            t.sleep(1)
            print("\n\tYou have exit from the bank.")
            self.exit = True


if __name__ == "__main__":
    main()