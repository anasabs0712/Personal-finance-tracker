# ============================================================
#   Personal Finance Tracker
#   TCS iON Industry Project
#   Author: [Your Name]
#   Language: Python 3
# ============================================================

from datetime import datetime
from collections import defaultdict


# ──────────────────────────────────────────────
#  BASE CLASS  (mimics abstract class in Java)
# ──────────────────────────────────────────────
class Transaction:
    """
    Base class for all transactions.
    Encapsulates amount, category, and date.
    apply() is meant to be overridden by child classes (Polymorphism).
    """

    def __init__(self, amount: float, category: str, date: str = None):
        # Encapsulation: attributes are "protected" using single underscore
        self._amount = amount
        self._category = category
        self._date = date if date else datetime.today().strftime("%d-%m-%Y")

    # Getters (Encapsulation)
    def get_amount(self):
        return self._amount

    def get_category(self):
        return self._category

    def get_date(self):
        return self._date

    # To be overridden by child classes (Polymorphism / Abstraction)
    def apply(self, balance: float) -> float:
        raise NotImplementedError("apply() must be implemented by subclass")

    def __str__(self):
        return f"{self._date} | {self._category} | ₹{self._amount:.2f}"


# ──────────────────────────────────────────────
#  CHILD CLASS 1 – Income  (Inheritance)
# ──────────────────────────────────────────────
class Income(Transaction):
    """
    Inherits from Transaction.
    apply() ADDS amount to balance.
    """

    def __init__(self, amount: float, category: str, date: str = None):
        super().__init__(amount, category, date)

    def apply(self, balance: float) -> float:
        # Polymorphism: Income adds to balance
        return balance + self._amount

    def __str__(self):
        return f"[INCOME]  {super().__str__()}"


# ──────────────────────────────────────────────
#  CHILD CLASS 2 – Expense  (Inheritance)
# ──────────────────────────────────────────────
class Expense(Transaction):
    """
    Inherits from Transaction.
    apply() SUBTRACTS amount from balance.
    """

    def __init__(self, amount: float, category: str, date: str = None):
        super().__init__(amount, category, date)

    def apply(self, balance: float) -> float:
        # Polymorphism: Expense subtracts from balance
        return balance - self._amount

    def __str__(self):
        return f"[EXPENSE] {super().__str__()}"


# ──────────────────────────────────────────────
#  ACCOUNT CLASS  (Encapsulation)
# ──────────────────────────────────────────────
class Account:
    """
    Manages the user's balance and transaction history.
    Private attributes accessed only through methods (Encapsulation).
    """

    def __init__(self, owner_name: str):
        self.__owner = owner_name          # private
        self.__balance = 0.0              # private
        self.__transactions = []          # private list of Transaction objects

    def get_balance(self):
        return self.__balance

    def get_owner(self):
        return self.__owner

    def get_transactions(self):
        return self.__transactions

    def add_transaction(self, txn: Transaction):
        """Validates and records a transaction, then updates balance."""
        if txn.get_amount() <= 0:
            print("\n  ❌  Amount must be greater than 0. Transaction cancelled.\n")
            return False

        self.__balance = txn.apply(self.__balance)   # Polymorphism in action
        self.__transactions.append(txn)
        return True


# ──────────────────────────────────────────────
#  REPORT GENERATOR CLASS  (Abstraction)
# ──────────────────────────────────────────────
class ReportGenerator:
    """
    Generates financial summary and category-wise breakdown.
    Hides internal logic from the user (Abstraction).
    """

    @staticmethod
    def generate(account: Account):
        transactions = account.get_transactions()

        if not transactions:
            print("\n  No transactions recorded yet.\n")
            return

        total_income = 0.0
        total_expense = 0.0
        category_expense = defaultdict(float)   # HashMap equivalent

        for txn in transactions:
            if isinstance(txn, Income):
                total_income += txn.get_amount()
            elif isinstance(txn, Expense):
                total_expense += txn.get_amount()
                category_expense[txn.get_category()] += txn.get_amount()

        net_balance = total_income - total_expense

        # ── Print Report ──
        print("\n" + "=" * 50)
        print(f"   FINANCIAL REPORT  —  {account.get_owner()}")
        print("=" * 50)
        print(f"  Total Income   : ₹{total_income:.2f}")
        print(f"  Total Expense  : ₹{total_expense:.2f}")
        print(f"  Net Balance    : ₹{net_balance:.2f}")
        print("-" * 50)

        if category_expense:
            print("  CATEGORY-WISE EXPENSE BREAKDOWN")
            print("-" * 50)
            for cat, amt in category_expense.items():
                pct = (amt / total_expense * 100) if total_expense else 0
                print(f"  {cat:<15} : ₹{amt:.2f}  ({pct:.1f}%)")

        print("-" * 50)
        print("  TRANSACTION HISTORY")
        print("-" * 50)
        for txn in transactions:
            print(f"  {txn}")
        print("=" * 50 + "\n")


# ──────────────────────────────────────────────
#  HELPER – Input Validation
# ──────────────────────────────────────────────
def get_amount() -> float:
    while True:
        try:
            amt = float(input("  Enter Amount (₹): "))
            if amt <= 0:
                print("  ⚠  Amount must be positive. Try again.")
            else:
                return amt
        except ValueError:
            print("  ⚠  Invalid input. Please enter a number.")


def get_category(txn_type: str) -> str:
    if txn_type == "income":
        cats = ["Salary", "Freelance", "Business", "Investment", "Other"]
    else:
        cats = ["Food", "Rent", "Travel", "Shopping", "Health", "Education", "Entertainment", "Other"]

    print(f"\n  Categories:")
    for i, c in enumerate(cats, 1):
        print(f"    {i}. {c}")

    while True:
        try:
            choice = int(input("  Choose category (number): "))
            if 1 <= choice <= len(cats):
                return cats[choice - 1]
            else:
                print(f"  ⚠  Enter a number between 1 and {len(cats)}.")
        except ValueError:
            print("  ⚠  Invalid input. Enter a number.")


# ──────────────────────────────────────────────
#  MAIN – Command Line Menu
# ──────────────────────────────────────────────
def main():
    print("\n" + "=" * 50)
    print("   PERSONAL FINANCE TRACKER")
    print("   TCS iON Industry Project")
    print("=" * 50)
    name = input("  Enter your name to get started: ").strip() or "User"
    account = Account(name)
    print(f"\n  Welcome, {name}! Your account is ready.\n")

    while True:
        print("\n──────────────────────────────────")
        print("  MAIN MENU")
        print("──────────────────────────────────")
        print("  1. Add Income")
        print("  2. Add Expense")
        print("  3. View Report")
        print("  4. Exit")
        print("──────────────────────────────────")

        choice = input("  Select option (1-4): ").strip()

        # ── Add Income ──
        if choice == "1":
            print("\n  ── ADD INCOME ──")
            amt = get_amount()
            cat = get_category("income")
            txn = Income(amt, cat)
            if account.add_transaction(txn):
                print(f"\n  ✅  Transaction successful!")
                print(f"  Current Balance: ₹{account.get_balance():.2f}\n")

        # ── Add Expense ──
        elif choice == "2":
            print("\n  ── ADD EXPENSE ──")
            amt = get_amount()
            cat = get_category("expense")
            txn = Expense(amt, cat)
            if account.add_transaction(txn):
                print(f"\n  ✅  Transaction successful!")
                print(f"  Current Balance: ₹{account.get_balance():.2f}\n")

        # ── View Report ──
        elif choice == "3":
            ReportGenerator.generate(account)

        # ── Exit ──
        elif choice == "4":
            print(f"\n  Thank you for using Personal Finance Tracker!")
            print(f"  Final Balance: ₹{account.get_balance():.2f}")
            print("  Goodbye! 👋\n")
            break

        else:
            print("\n  ⚠  Invalid option. Please enter 1, 2, 3, or 4.")


# Entry point
if __name__ == "__main__":
    main()
