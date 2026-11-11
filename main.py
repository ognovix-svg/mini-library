class BankAccount:
    def __init__(self, owner, balance=0):
        self.owner = owner
        self.balance = balance

    def deposit(self, amount):
        self.balance += amount
        return self.balance

    def withdraw(self, amount):
        if amount > self.balance:
            print(f"Помилка: Недостатньо коштів! Баланс: {self.balance} грн.")
            return False
        self.balance -= amount
        print(f"Знято {amount} грн. Залишок: {self.balance} грн.")
        return self.balance

    def transfer(self, to, amount):
        if amount > self.balance:
            print("Переказ неможливий: недостатньо коштів.")
            return False

        self.balance -= amount
        to.deposit(amount)
        print(f"Переказано {amount} грн для {to.owner}. Залишок: {self.balance} грн.")
        return True
    def __str__(self):
        return f"Рахунок: {self.owner} | Баланс: {self.balance} грн"

    def __eq__(self, other):
        return self.balance == other.balance

    def __add__(self, other):
        joint_owner = f"{self.owner} та {other.owner}"
        joint_balance = self.balance + other.balance
        return BankAccount(joint_owner, joint_balance)

# --- КОД НИЖЧЕ ПИШЕТЬСЯ ВЖЕ З КРАЮ (0 пробілів) ---

acc1 = BankAccount("Іван", 1000)
acc2 = BankAccount("Олена", 200)

acc1.withdraw(1500)
acc1.transfer(acc2, 400)

print(f"Баланс Олени: {acc2.balance} грн.")
acc1 = BankAccount("Іван", 1000)
acc2 = BankAccount("Олена", 1000)

# 1. Тест __str__
print(acc1)

# 2. Тест __eq__ (має бути True, бо в обох по 1000)
print("Баланси однакові?", acc1 == acc2)

# 3. Тест __add__ (об'єднання рахунків через звичайний плюс!)
family_acc = acc1 + acc2
print(family_acc)