class Bank:
    def __init__(self, total_amount, limit_for_loan, limit_for_withdrawl):
        self.total_amount = total_amount
        self.limit_for_loan = limit_for_loan
        self.limit_for_withdrawl = limit_for_withdrawl
    
    def repeat_withdrawing_money(self, amount, limit_for_withdrawl):
        count = amount // limit_for_withdrawl
        rest = amount & limit_for_withdrawl
        # 반복문
        for i in range(count):
            print(f'This is your money - {limit_for_withdrawl}')
            # 중첩구조
            if i == (count - 1):
                print(f'This is your money - {rest}')
    
    def show_me_the_money(self, amount):
        # 조건문 분기 1
        if amount <= self.total_amount:
            self.repeat_withdrawing_money(amount, self.limit_for_withdrawl)
        # 조건문 분기 2
        elif amount <= (self.total_amount + self.limit_for_loan):
            print('Wait!! Do you want to loan?')
        # 조건문 분기 3
        else:
            print('Your money is not enough')

hana_bank = Bank(1000, 200, 100)
hana_bank.show_me_the_money(450)
print()

sinhan_bank = Bank(500, 500, 50)
sinhan_bank.show_me_the_money(250)