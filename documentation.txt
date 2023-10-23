# Python Internship Challenges
  
  
## What You Need to Do:
1. If unfamiliar, start by learning the basics of Git. There are numerous free resources and tutorials available online.
2. Head over to [GitHub](https://github.com/) and *create a new private repository*. Name it `task-expense-analysis`.
3. Work on the task(s) described below. (As you make progress or reach milestones in your solution, commit your changes. It is good to have commit messages that are meaningful and descriptive.)
4. Once you've completed the task(s), *push your solution to the `task-expense-analysis` repository.*
5. *Invite `dev@wtech.com.np` to your private repository to allow for review.* You can do this under the "Settings" -> "Collaborators" -> "Manage access" section of your `task-expense-analysis` repository in GitHub.
6. Lastly, don't forget to fill up [this internship application form](https://forms.gle/D6KsLwmUkvokyjoK6) with all the necessary details and submit it.

All the best, and looking forward to your submission!
  
  
# Task 1 - Data Processing Challenge: Expense Analysis

### **Objective:**
Your task is to process and analyze a dataset containing a record of expenses using core Python functionalities. The dataset is provided as a CSV file named `expenses.csv`. The main objective is to extract insightful summaries from this data.

## IMPORTANT: Use of external libraries like `Pandas`, `NumPy`, or other data processing libraries is not allowed for this challenge. Please only use core Python functionalities and data structures for processing the data. The `csv` library is permissible for reading the dataset.


### **Data:**
The CSV file contains the following columns:
1. `expense_id`
2. `expense_type`: The category/type of the expense (e.g., Groceries, Utilities, Dining, etc).
3. `amount`: The amount of the expense.
4. `expense_date`: The date on which the expense occurred (format: YYYY-MM-DD). 
5. `payment_method`: The method used for the payment (e.g., Credit Card, Cash).

Note: Some data might be missing from the CSV. Your solution should be robust enough to handle this.

### **Task:**
Write a Python script that reads this CSV file and outputs:

1. The total expense.
2. The total expense for each expense type.
3. The total expense for each payment method.
4. The top 3 most expensive expense_type categories.
5. The day with the highest expenses.
6. Monthly total expenses.
7. A *structured table* that breaks down expenses by `expense_type` and further subdivides each type by `payment_method`. This table should also display totals for each `expense_type` and `payment_method`.

If you save your python script in `report.py` file, you should be able to run the script by running the `python report.py` command.

### **Output:**
The output should be printed to the console. A possible output format might be,

```
(virtualenv)$ python report.py

Total Expense: $56969.79

Total by Expense Type:
Groceries: $3183.58
Transport: $2763.10
Entertainment: $2917.11
Rent: $44466.11
Utilities: $3639.89

Total by Payment Method:
Credit Card: $30322.86
Cash: $26646.93

Top 3 Expense Types:
Rent: $44466.11
Utilities: $3639.89
Groceries: $3183.58

Day with Highest Expenses: 2023-07-30 with $995.52

Month-wise Total Expenses:
01: $4775.88
02: $3052.63
03: $4585.14
04: $4048.55
05: $5169.52
06: $6642.37
07: $7869.60
08: $4320.92
09: $4554.28
10: $5115.51
11: $3368.00
12: $3467.39

Expense Type Breakdown by Payment Method:
Expense Type         Credit Card     Cash            Total          
-----------------------------------------------------------------
Groceries            $1443.41        $1740.17        $3183.58       
Transport            $1447.68        $1315.42        $2763.10       
Entertainment        $1489.62        $1427.49        $2917.11       
Rent                 $24335.58       $20130.53       $44466.11      
Utilities            $1606.57        $2033.32        $3639.89       
-----------------------------------------------------------------
Total                $30322.86       $26646.93       $56969.79
```
  
  
# Task 2 - Python Web API Challenge: Expense Data Service

As you will be building a lot of web api backends when working with us, it is a plus if you already know some basics of coding one.

### **Objective:**
Building upon the solution you developed in Task 1, your next task is to create a web API that serves the summaries and analyses that you generated in a JSON format. This will allow any application, be it a web frontend or mobile app, to fetch and utilize the processed data.

### **Tasks:**
1. Setting Up:
- Set up a web server using a Python web framework of your choice (e.g., Flask, Django, FastAPI).
- Make sure your server can read and process the `expenses.csv` file

2. Create the following API Endpoints:
- GET `/expense_by_type`: Returns the total expense for each expense type in JSON format.
- GET `/monthly_expenses`: Returns the monthly total expenses in JSON format.
- GET `/detailed_breakdown`: Returns a structured JSON containing the breakdown of expenses by expense_type, further subdivided by payment_method.

Your code should be able to run and serve the API endpoints locally. Provide clear documentation on how to set up and serve the API.

### **Output:**
For example, a GET call to `/expense_by_type` might return:

```json
{
    "Groceries": 3200.50,
    "Utilities": 1200.20,
    "Dining": 450.00
}
```
  
  
# Evaluation Criteria:

- **Functionality:** Your code should run without errors and produce correct outputs.
- **Code Quality:** Prioritize clarity, organization, and readability in your code. Ensure that your logic is easily understood by fellow developers.
- **Documentation:** Include a brief README in your repository, explaining **how to set up and run your code**. If relevant, highlight any significant design choices or assumptions you've made.
- **Error Handling:** Both your data processing code and the web service should be resilient. They should handle potential anomalies in the data or requests gracefully, returning helpful error messages when needed.
- **Performance:** Be mindful of the efficiency of your solutions.

**Bonus Points:**
- if you implement solution using Object Oriented Programming.
- if you write and include unit tests for your code.

Your approach to the problems, the techniques you employ, and your coding style will all play a role in the evaluation process. Aim for clarity, efficiency, and maintainability in your solutions.

