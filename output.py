import csv

class Expenses:
   
    def __init__(self):
       self.expense_data = []

    def readExpensesFile(self):
        with open('expenses.csv', 'r') as csv_file:
            data_file = csv.DictReader(csv_file)
            next(data_file)
            for row in data_file:
               amount= row['amount']
               if amount:
                Amount= float(amount)
               else:
                Amount= 0
               expense = {
                    'Expense_ID': int(row['expense_id']),
                   'Expense_Type': str(row['expense_type']),
                   'Amount': Amount,
                    'Expense_Date': row['expense_date'],
                    'Payment_Method': str(row['payment_method'])
                }
               self.expense_data.append(expense)
    
    def totalExpense(self):
        total= sum(single_expense['Amount'] for single_expense in self.expense_data)
        print(f"Total Expense: ${total:.4f}")
      
    def expensesByType(self):
        expenses_by_type = {}
        rent_expense = transport_expense = entertainment_expense = groceries_expense = utilities_expense = r_cash_expense = r_credit_expense = t_cash_expense = t_credit_expense = e_cash_expense = e_credit_expense= g_cash_expense= g_credit_expense= u_cash_expense= u_credit_expense = 0
        for expense in self.expense_data:
            type = expense['Expense_Type']
            match type:
                case "Rent":
                    rent_expense += expense['Amount']
                    if expense['Payment_Method'] == "Cash":
                       r_cash_expense += expense['Amount']
                    else:
                       r_credit_expense += expense['Amount']
                case "Transport":
                   transport_expense += expense['Amount']
                   if expense['Payment_Method'] == "Cash":
                    t_cash_expense += expense['Amount']
                   else:
                    t_credit_expense += expense['Amount']
                case "Entertainment":
                    entertainment_expense += expense['Amount']
                    if expense['Payment_Method'] == "Cash":
                       e_cash_expense += expense['Amount']
                    else:
                       e_credit_expense += expense['Amount']
                case "Groceries":
                    groceries_expense += expense['Amount']
                    if expense['Payment_Method'] == "Cash":
                       g_cash_expense += expense['Amount']
                    else:
                       g_credit_expense += expense['Amount']
                case "Utilities":
                    utilities_expense += expense['Amount']
                    if expense['Payment_Method'] == "Cash":
                       u_cash_expense += expense['Amount']
                    else:
                       u_credit_expense += expense['Amount']
                case _:
                    groceries_expense += expense['Amount']
                    if expense['Payment_Method'] == "Cash":
                       g_cash_expense += expense['Amount']
                    else:
                       g_credit_expense += expense['Amount']

        print(f"Total by Expense Type: \n Groceries: ${groceries_expense:.4f}\n Transport: ${transport_expense:.4f}\n Entertainment: ${entertainment_expense:.4f} \n Rent: ${rent_expense:.4f} \n Utilities: ${utilities_expense:.4f}")
        data = {
            'Groceries': {
            'Credit Card': g_credit_expense, 
            'Cash': g_cash_expense
            },
            'Transport': {
            'Credit Card': t_credit_expense, 
            'Cash': t_cash_expense
            },
            'Entertainment': {
            'Credit Card': e_credit_expense, 
            'Cash': e_cash_expense
                },
            'Rent': {
            'Credit Card': r_credit_expense, 
            'Cash': r_cash_expense
            },
            'Utilities': {
            'Credit Card': u_credit_expense, 
            'Cash': u_cash_expense
            }
        }
        return data

        # return g_cash_expense, g_credit_expense, t_cash_expense, t_credit_expense, e_cash_expense, e_credit_expense, r_cash_expense, r_credit_expense, u_cash_expense, u_credit_expense


    
    def expensesByPaymentMethod(self):
        expenses_by_payment_method = {}
        cash_expense = credit_card_expense = 0
        for expense in self.expense_data:
            method = expense['Payment_Method']
            match method:
                case "Cash":
                    cash_expense += expense['Amount']
                case "Credit Card":
                   credit_card_expense += expense['Amount']
                case _:
                    cash_expense += expense['Amount']                   
                    
        print(f"Total by Payment Method: \n Cash: ${cash_expense:.4f}\n Credit Card: ${credit_card_expense:.4f}")

    def highestExpense(self):
        highest_expense = -1.0
        for expense in self.expense_data:
          if expense['Amount'] and expense['Expense_Date']:
            if expense['Amount'] > highest_expense:
                highest_expense = expense['Amount']
                date = expense['Expense_Date']
        print(f"Day with Highest Expenses: {date} with ${highest_expense:.4f}")



    def monthwiseExpenses(self):
        month1_expense = month2_expense =month3_expense = month4_expense = month5_expense = month6_expense =0
        month7_expense = month8_expense= month9_expense= month10_expense= month11_expense = month12_expense = 0
        for expense in self.expense_data:
          if expense['Amount'] and expense['Expense_Date']:
            date = expense['Expense_Date'].split('-')
            year_month = f"{date[0]}-{date[1]}"
            match year_month:
               case "2023-01":
                  month1_expense += expense['Amount']
               case "2023-02":
                  month2_expense += expense['Amount']
               case "2023-03":
                  month3_expense += expense['Amount']
               case "2023-04":
                  month4_expense += expense['Amount']
               case "2023-05":
                  month5_expense += expense['Amount']
               case "2023-06":
                  month6_expense += expense['Amount']
               case "2023-07": 
                  month7_expense += expense['Amount']
               case "2023-08":
                  month8_expense += expense['Amount']
               case "2023-09": 
                  month9_expense += expense['Amount']
               case "2023-10":
                  month10_expense += expense['Amount']
               case "2023-11":
                  month11_expense += expense['Amount']
               case "2023-12":  
                  month12_expense += expense['Amount']  
               case _:
                 month12_expense += expense['Amount'] 
        print(f" 01: ${month1_expense:.4f} \n 02: ${month2_expense:.4f} \n 03: ${month3_expense:.4f} \n 04: ${month4_expense:.4f} \n 05: ${month5_expense:.4f} \n 06: ${month6_expense:.4f} \n 07: ${month7_expense:.4f} \n 08: ${month8_expense:.4f} \n 09: ${month9_expense:.4f} \n 10: ${month10_expense:.4f} \n 11: ${month11_expense:.4f} \n 12: ${month12_expense:.4f}") 

    def structuredTable(self, data):
          print("Expense Type Breakdown by Payment Method: ")
          header = ["Expense Type", "Credit Card", "Cash", "Total"]

          print(f"{header[0]:<20} {header[1]:<22} {header[2]:<20} {header[3]:<20}")
          print("-" * 72)

          total_credit_card = 0
          total_cash = 0

          for expense_type, payment_data in data.items():
            credit_card = f"{payment_data['Credit Card']:.3f}"
            cash = f"{payment_data['Cash']:.3f}"
            total = f"{float(credit_card) + float(cash):.3f}"

            total_credit_card += payment_data['Credit Card']
            total_cash += payment_data['Cash']

            print(f"{expense_type:<20} ${credit_card:<14}        ${cash:<10}        ${total:<8}")

          print("-" * 72)

          print(f"Total                ${total_credit_card:.2f}              ${total_cash:.2f}          ${total_credit_card + total_cash:.2f}")



a = Expenses()
a.readExpensesFile()
a.totalExpense()
print()
values = a.expensesByType()
print()
a.expensesByPaymentMethod()
print()
a.highestExpense()
print()
a.monthwiseExpenses()
print()
a.structuredTable(values)
