#python -m flask --app project.py run
import flask
from flask_cors import CORS
from flask import request
import sqlite3
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import io
import base64
import numpy as np
from datetime import datetime

PINK = "#ffbde3"

app = flask.Flask("project")
CORS(app)

if __name__ == "__main__":
    app.run(debug=True)

def get_time():
    date= datetime.now()
    time=date.strftime("%H:%M")
    weekday= date.strftime("%A")

    return {date: date, time: time, weekday: weekday}


#2 people with properties and methods

class Person:
    def __init__(self, name, age, nationality, studies):
        self.name = name
        self.age = age        
        self.nationality= nationality
        self.studies = studies
                
    # Establishing activities depending on the time and the day of the week
    def activity(self):  
        date, time, weekday = get_time()      
        if time > "07:30" and time <= "08:00" or time >= "12:00" and time <= "13:00" or time >= "19:00" and time <= "21:00":
            return self.eating()
        elif time > "07:00" and time<= "07:30":
            return self.running()
        elif time >="16:00" and time <= "18:30":
            if self== p:
                return self.shopping("mall")
            else:
                return self.playing("video games") 
        elif time >"22:00" and time <= "23:59" or time >= "00:00" and time <="06:50":
            return self.sleeping()
        elif weekday != "Saturday" and weekday != "Sunday":
            if time >"08:00" and time <"12:00" or time >"13:00" and time <"16:00":  
                return self.working()
            else:
                return self.at_home()
        else:
            return self.at_home()

    # getting the meal to eat   
    def eating(self):
        date, time, weekday = get_time()
        if time > "07:30" and time <= "08:00":
            meal= "breakfast"
        elif time>= "12:00" and time <= "13:00":
            meal= "lunch"
        elif time >= "19:00" and time <= "21:00":
            meal= "dinner"

        if self== p:
            return self.name + " is having " + meal
        else:
            return self.name + " is having " + meal + " too"

    def working(self):
        if self== p:
                return self.name + " is working in her office"
        else:
            return self.name + " is working from home"
    def running(self):
        return self.name + " is running"
    def playing(self, what):
        return self.name + " is playing " + what
    def shopping(self, place):
        message = self.name + " is doing shopping at the " + place
        return message
    def at_home(self):
        if self== p:
            return self.name + " is resting at home"
        else:
            return self.name + " is resting at home too"
    def sleeping(self):
        if self== p:
            return self.name + " is sleeping"
        else:
            return self.name + " is sleeping too"
    
#2 people with properties and methods
p= Person("Cris", 32, "Spanish", "translator and interpreter")
p1= Person("Luis", 30, "Spanish", "computer engineer")


#function to get the page
def get_html(page_name):
    html_file= open(page_name + ".html")
    content= html_file.read()
    html_file.close()
    return content

# Checking what Cris and Luis are doing. Class and methods
@app.route("/activity")
def get_activity(): 
    date, time, weekday = get_time()
    msg= '''Looks like they can't, so I'm going to explain it to you. Cris and Luis divide their income in five accounts, 
    the 55% of it goes to the account 'Basic needs', a 20% goes to the account 'Long-term savings', a 10% goes to the account 'Personal development', another 10% goes to the account 'Leisure', and a 5% goes to the account 'Donations'.
    \n If you go to 'Expenses', you'll see that there's a button to 'Add your Salary' (and its date), and buttons to click on so you can add the expense and its date. Don't forget to click on 'Save Expenses' afterwards. \n If you click on 'Summary', you'll have a table with all the categories,
    the assigned budgets to each one and the remaining amount in each of them. You will also find chart pies of the categories with more subcategories inside so you can see where your money is going.'''
    Luis= p1.activity()
    Cris= p.activity()   
    return {"text": p.name + " is a " + p.studies + ", and " + p1.name + " is a " + p1.studies + ". They're " + p.nationality + " and they live in Granada." + "\n" + 
            "Today is " + weekday + ". It's " + time + " h, let's see if they can explain it to you. " + Cris + ", " + Luis + "... " + msg}

# Checking how much money you've already saved
@app.route("/week_challenge")
def get_amount_challenge():
    file= sqlite3.connect("Expenses.db")
    cursor= file.cursor()
    cursor.execute("select sum(amount) from savings")
    amount= cursor.fetchone()[0]
    msg= "You have already saved "
    msg1= " CHF"
    if amount == None:
        amount= 0
    cursor.close()
    return {"savings" : msg + str(amount) + msg1}

#homepage
@app.route("/")
def homepage():
    return get_html("project")
                
# expenses
@app.route("/expenses")
def expenses():
    html_page = get_html("expenses")    
    return html_page

# savings
@app.route("/savings")
def savings():
    html_page = get_html("savings")    
    return html_page



# Saving the expenses
@app.route("/save_expenses", methods= ["POST"])
def save_expenses():
    date, time, weekday = get_time()
    data=request.get_json()

    file= sqlite3.connect("Expenses.db")
    cursor= file.cursor()
    for element in data:
        date_object = datetime.strptime(element['date_expense'], '%Y-%m-%d')
        month_name = date_object.strftime('%B')
        subcategory = element["subcategory"] if element["subcategory"] != "" else "Others"
        cursor.execute("insert into Expenses values(Null, ?,?,?,?,?)", [element["category"], subcategory, element["amount"], month_name, date.strftime("%d-%m-%Y")])
        file.commit()
    cursor.close()
    return {"status": "ok"}

# Saving the amount in savings
@app.route("/save_savings", methods=["POST"])
def save_savings():
    date, time, weekday = get_time()
    data=request.get_json()
    file= sqlite3.connect("Expenses.db")
    cursor= file.cursor()
    cursor.execute("insert into Savings values(Null, ?,?)", [data, date.strftime("%d-%m-%Y")])
    cursor.execute("SELECT COUNT (*) FROM SAVINGS")  
    week_number = cursor.fetchall()
    file.commit()
    cursor.close()
    if week_number== [(52,)]:
        cursor= file.cursor()
        cursor.execute("DELETE FROM SAVINGS")  
        file.commit()
        cursor.close()
        return {"status": "Table is full"}
    return{"status": "ok"}

# checking which amounts you have already saved in the week challenge
@app.route("/get_savings")
def get_savings():
    file= sqlite3.connect("Expenses.db")
    cursor= file.cursor()
    cursor.execute("select amount from savings")
    rows = cursor.fetchall()    
    cursor.close()
    return rows

# saving the salary
@app.route("/save_salary", methods=["POST"])
def save_salary():
    date, time, weekday = get_time()
    data=request.get_json()
    date_object = datetime.strptime(data[0], '%Y-%m-%d')

    # extract the name of the month
    month_name = date_object.strftime('%B')
    file= sqlite3.connect("Expenses.db")
    cursor= file.cursor()    
    cursor.execute("insert into Salary values(NULL,?,?,?)", [month_name, data[1], date.strftime("%d-%m-%Y")])
    file.commit()
    cursor.close()
    return {"status": "ok"}

# getting the salary amount of a given month
def get_month_salary(month):
    file= sqlite3.connect("Expenses.db")
    cursor= file.cursor()
    month_salary = cursor.execute("select amount from salary where month = ?", [month])
    month_salary = month_salary.fetchone()
    if month_salary == None or month_salary[0]== None:
        month_salary = 0
    else:
        month_salary = month_salary[0]           
    cursor.close()
    return int(month_salary) 

# Getting the sum of the salaries
def get_total_salary():
    file= sqlite3.connect("Expenses.db")
    cursor= file.cursor()
    total_salary = cursor.execute("select sum(amount) from salary ")
    total_salary = total_salary.fetchone()
    if total_salary == None or total_salary[0]== None:
        total_salary = 0
    else:
        total_salary = total_salary[0]           
    cursor.close()
    return int(total_salary) 

# getting the long_term_savings amount of a given month
def get_long_term_savings(month):
    month_salary = get_month_salary(month)
    return int(month_salary)*0.20

# getting the basic_needs expenses of a given month
def get_needs_expenses(month):
    file= sqlite3.connect("Expenses.db")
    cursor= file.cursor()
    needs_expenses = cursor.execute("select sum(amount) from expenses where category like 'Basic_needs%' and date_expense = ?", [month])
    needs_expenses = needs_expenses.fetchone()
    if needs_expenses == None  or needs_expenses[0] == None:
        needs_expenses = 0
    else:
        needs_expenses = needs_expenses[0]    
    cursor.close()
    return int(needs_expenses)

# getting the basic_needs_budget per month
def get_needs_budget(month):
    month_salary = get_month_salary(month)
    return int(month_salary)*0.55

# getting the remaining amount of a category of a given month
def get_needs_remaining(month):
    budget= get_needs_budget(month)
    expenses= get_needs_expenses(month)
    remaining= int(budget) - int(expenses)
    return remaining

# total needs expenses
def get_total_needs_expenses():
    file= sqlite3.connect("Expenses.db")
    cursor= file.cursor()
    total_needs_expenses = cursor.execute("select sum(amount) from expenses where category like 'Basic_needs%'")
    total_needs_expenses = total_needs_expenses.fetchone()
    if total_needs_expenses == None  or total_needs_expenses[0] == None:
        total_needs_expenses = 0
    else:
        total_needs_expenses = total_needs_expenses[0]    
    cursor.close()
    return int(total_needs_expenses)

# getting the total remaining amount of a category
def get_total_needs_remaining():
    salary= get_total_salary()
    budget= salary * 0.55
    expenses= get_total_needs_expenses()
    remaining= int(budget) - int(expenses)
    return remaining

# calculating the budget of personal development and leisure
def get_10percentage_budget(month):
    month_salary = get_month_salary(month)
    return int(month_salary)*0.10

# getting the expenses of personal development
def get_personal_development(month):
    file= sqlite3.connect("Expenses.db")
    cursor= file.cursor()
    personal_development = cursor.execute("select sum(amount) from expenses where category like 'Personal_development' and date_expense = ?", [month])
    personal_development = personal_development.fetchone()
    if personal_development == None  or personal_development[0] == None:
        personal_development = 0
    else:
        personal_development = personal_development[0]   
    cursor.close()
    return int(personal_development)

# getting the remaining amount of a category of a given month
def get_personal_remaining(month):
    budget= get_10percentage_budget(month)
    expenses= get_personal_development(month)
    remaining= int(budget) - int(expenses)
    return remaining

# getting the total expenses of personal development
def get_total_personal_development():
    file= sqlite3.connect("Expenses.db")
    cursor= file.cursor()
    total_personal_development = cursor.execute("select sum(amount) from expenses where category like 'Personal_development'")
    total_personal_development = total_personal_development.fetchone()
    if total_personal_development == None  or total_personal_development[0] == None:
        total_personal_development = 0
    else:
        total_personal_development = total_personal_development[0]   
    cursor.close()
    return int(total_personal_development)

# getting the total remaining amount of personal development
def get_total_personal_remaining():
    salary= get_total_salary()
    budget= salary * 0.10
    expenses= get_total_personal_development()
    remaining= int(budget) - int(expenses)
    return remaining

# getting the expenses of leisure of a given month
def get_leisure(month):
    file= sqlite3.connect("Expenses.db")
    cursor= file.cursor()
    leisure = cursor.execute("select sum(amount) from expenses where category like 'Leisure' and date_expense = ?", [month])
    leisure = leisure.fetchone()
    if leisure == None  or leisure[0] == None:
        leisure = 0
    else:
        leisure = leisure[0]   
    cursor.close()
    return int(leisure)

# getting the remaining amount of a given month
def get_leisure_remaining(month):
    budget= get_10percentage_budget(month)
    expenses= get_leisure(month)
    remaining= int(budget) - int(expenses)
    return remaining

# getting the total expenses of leisure
def get_total_leisure():
    file= sqlite3.connect("Expenses.db")
    cursor= file.cursor()
    total_leisure = cursor.execute("select sum(amount) from expenses where category like 'Leisure'")
    total_leisure = total_leisure.fetchone()  
    if total_leisure == None  or total_leisure[0] == None:
        total_leisure = 0
    else:
        total_leisure = total_leisure[0]
    cursor.close()
    return int(total_leisure)

# getting the total remaining of leisure
def get_leisure_total_remaining():
    salary= get_total_salary()
    budget= salary * 0.10
    expenses= get_total_leisure()
    remaining= int(budget) - int(expenses)
    return remaining

# getting the expenses of donations of a given month
def get_donations(month):
    file= sqlite3.connect("Expenses.db")
    cursor= file.cursor()
    donations = cursor.execute("select sum(amount) from expenses where category like 'Donations' and date_expense = ?", [month])
    donations = donations.fetchone()
    if donations == None  or donations[0] == None:
        donations = 0
    else:
        donations = donations[0]   
    cursor.close()
    return int(donations)

# getting the donations budget
def get_donations_budget(month):
    month_salary = get_month_salary(month)
    return int(month_salary)*0.05

# getting the remaining of donations of a given month
def get_donations_remaining(month):
    budget= get_donations_budget(month)
    expenses= get_donations(month)
    remaining= int(budget) - int(expenses)
    return remaining

# getting the total expenses of donations
def get_total_donations():
    file= sqlite3.connect("Expenses.db")
    cursor= file.cursor()
    total_donations = cursor.execute("select sum(amount) from expenses where category like 'Donations'")
    total_donations = total_donations.fetchone()
    if total_donations == None  or total_donations[0] == None:
        total_donations = 0
    else:
        total_donations = total_donations[0]   
    cursor.close()
    return int(total_donations)

# getting the total remaining of donations
def get_total_donations_remaining():
    salary= get_total_salary()
    budget= salary * 0.05
    expenses= get_total_donations()
    remaining= int(budget) - int(expenses)
    return remaining

# getting the info for the basic_needs pie chart
def get_basics_chart(month):
    query = ''
    if month != None:
        query = f'''select Subcategory, sum(amount) from expenses where Date_expense="{month}" group by Subcategory having Category like "Basic_needs%"'''
    else:
        query = f'''select Subcategory, sum(amount) from expenses group by Subcategory having Category like "Basic_needs%"'''
    file= sqlite3.connect("Expenses.db")
    cursor= file.cursor()
    basics_chart = cursor.execute(query)
    basics_chart = basics_chart.fetchall()  
    cursor.close()
    values=[]
    labels = []
    if basics_chart != None:
        for element in basics_chart:
            values.append(element[1])
            labels.append(element[0].replace("_", " ").replace("-", " / "))    
    return {'values': values, 'labels': labels}

# getting the info for the leisure pie chart
def get_leisure_chart(month):
    query = ''
    if month != None:
        query = f'''select Subcategory, sum(amount) from expenses where Date_expense="{month}" group by Subcategory having Category = "Leisure"'''
    else:
        query = f'''select Subcategory, sum(amount) from expenses group by Subcategory having Category = "Leisure"'''
    
    file= sqlite3.connect("Expenses.db")
    cursor= file.cursor()
    basics_chart = cursor.execute(query)
    basics_chart = basics_chart.fetchall()  
    cursor.close()
    values=[]
    labels = []
    if basics_chart != None or len(basics_chart[0]) != 0:
        for element in basics_chart:
            values.append(element[1])
            labels.append(element[0].replace("_", " ").replace("-", " / "))        
    return {'values': values, 'labels': labels}

# function to create the pies chart
def create_pie_chart(category, month):
        # Create some data for the chart
    if category == "Basics":
        dict = get_basics_chart(month)
        plt.title("Basic needs\n")
    else:
        dict = get_leisure_chart(month)
        plt.title("Leisure\n")

    values= dict['values']
    labels= dict['labels']
    my_explode= np.full(len(values), 0.2)
    my_colors = ["#63bfb9", "#125e59", "#febc67", PINK, "grey", "#0b0"]
        # Create the pie chart
    plt.pie(values, labels=labels, explode = my_explode, shadow= True, colors= my_colors, autopct='%1.2f%%', startangle = 90)

    # Save the chart to a BytesIO object
    buffer = io.BytesIO()
    plt.savefig(buffer, format="png")
    buffer.seek(0)
    # Clear the figure
    plt.clf()

    # Encode the BytesIO object to base64
    img_str = base64.b64encode(buffer.read()).decode("utf-8")

    # Display the image using an HTML tag
    img = '<img src="data:image/png;base64,{0}">'.format(img_str)
    buffer = None
    return img

# summary
@app.route("/summary", methods=['GET'])
def get_summary():
    month = request.args.get('month')
    html_page = get_html("summary")
    file= sqlite3.connect("Expenses.db")
    cursor= file.cursor()    
    t_salary = cursor.execute("select sum(amount) from salary")   
    if t_salary != None: 
        total_salary = t_salary.fetchone()[0]
        if total_salary != None:                 
            basic_needs = total_salary * 0.55
            long_term_savingsT = total_salary * 0.20
            personal_development = total_salary * 0.10
            leisure = total_salary * 0.10
            donations = total_salary * 0.05
            img= create_pie_chart("Basics", month)
            img2= create_pie_chart("Leisure", month)
        else:
            basic_needs = 0
            long_term_savingsT = 0
            personal_development = 0
            leisure = 0
            donations = 0
            total_salary = 0
            img = ""
            img2 = ""

    cursor.close()



# creating a table to show the expenses information
    html = f'''
    
    
    <table class= summary>
        <col>
        <colgroup span="2"></colgroup>
        <colgroup span="2"></colgroup>
        <tr>
            <td style="background-color:white; color: #125e59; font-size: 40px; font-weight: bold; text-align: center;" rowspan="2">Salary</td>
            <th style="text-align: center; background-color:#63bfb9; color: #125e59;" colspan="1" scope="colgroup"><a style="text-decoration: none" href="http://127.0.0.1:5000/summary?month=January">January</a></th>
            <th style="text-align: center; background-color:#63bfb9; color: #125e59;" colspan="1" scope="colgroup"><a style="text-decoration: none" href="http://127.0.0.1:5000/summary?month=February">February</a></th>
            <th style="text-align: center; background-color:#63bfb9; color: #125e59;" colspan="1" scope="colgroup"><a style="text-decoration: none" href="http://127.0.0.1:5000/summary?month=March">March</a></th>
            <th style="text-align: center; background-color:#63bfb9; color: #125e59;" colspan="1" scope="colgroup"><a style="text-decoration: none" href="http://127.0.0.1:5000/summary?month=April">April</a></th>
            <th style="text-align: center; background-color:#63bfb9; color: #125e59;" colspan="1" scope="colgroup"><a style="text-decoration: none" href="http://127.0.0.1:5000/summary?month=May">May</a></th>
            <th style="text-align: center; background-color:#63bfb9; color: #125e59;" colspan="1" scope="colgroup"><a style="text-decoration: none" href="http://127.0.0.1:5000/summary?month=June">June</a></th>
            <th style="text-align: center; background-color:#63bfb9; color: #125e59;" colspan="1" scope="colgroup"><a style="text-decoration: none" href="http://127.0.0.1:5000/summary?month=July">July</a></th>
            <th style="text-align: center; background-color:#63bfb9; color: #125e59;" colspan="1" scope="colgroup"><a style="text-decoration: none" href="http://127.0.0.1:5000/summary?month=August">August</a></th>
            <th style="text-align: center; background-color:#63bfb9; color: #125e59;" colspan="1" scope="colgroup"><a style="text-decoration: none" href="http://127.0.0.1:5000/summary?month=September">September</a></th>
            <th style="text-align: center; background-color:#63bfb9; color: #125e59;" colspan="1" scope="colgroup"><a style="text-decoration: none" href="http://127.0.0.1:5000/summary?month=October">October</a></th>
            <th style="text-align: center; background-color:#63bfb9; color: #125e59;" colspan="1" scope="colgroup"><a style="text-decoration: none" href="http://127.0.0.1:5000/summary?month=November">November</a></th>
            <th style="text-align: center; background-color:#63bfb9; color: #125e59;" colspan="1" scope="colgroup"><a style="text-decoration: none" href="http://127.0.0.1:5000/summary?month=December">December</a></th>
            <th style="text-align: center; background-color:#63bfb9; color: #125e59;" colspan="1" scope="colgroup">Total per category</th>
        </tr>
        <tr>
            <th style="text-align: center; scope="col">{get_month_salary('January'):.2f}</th>
            <th style="text-align: center; scope="col">{get_month_salary('February'):.2f}</th>
            <th style="text-align: center; scope="col">{get_month_salary('March'):.2f}</th>
            <th style="text-align: center; scope="col">{get_month_salary('April'):.2f}</th>
            <th style="text-align: center; scope="col">{get_month_salary('May'):.2f}</th>
            <th style="text-align: center; scope="col">{get_month_salary('June'):.2f}</th>
            <th style="text-align: center; scope="col">{get_month_salary('July'):.2f}</th>
            <th style="text-align: center; scope="col">{get_month_salary('August'):.2f}</th>
            <th style="text-align: center; scope="col">{get_month_salary('September'):.2f}</th>
            <th style="text-align: center; scope="col">{get_month_salary('October'):.2f}</th>
            <th style="text-align: center; scope="col">{get_month_salary('November'):.2f}</th>
            <th style="text-align: center; scope="col">{get_month_salary('December'):.2f}</th>
            <th style="text-align: center; scope="col">{total_salary:.2f}</th>
        </tr>
        <tr>
            <th style="background-color:#63bfb9; color: #125e59;" scope="row">Basic needs budget</th>
            <td style="text-align: center; background-color:#63bfb9; color: #125e59; font-weight: 650 ">{get_needs_budget("January"):.2f}</td>
            <td style="text-align: center; background-color:#63bfb9; color: #125e59; font-weight: 650 ">{get_needs_budget("February"):.2f}</td>
            <td style="text-align: center; background-color:#63bfb9; color: #125e59; font-weight: 650 ">{get_needs_budget("March"):.2f}</td>
            <td style="text-align: center; background-color:#63bfb9; color: #125e59; font-weight: 650 ">{get_needs_budget("April"):.2f}</td>
            <td style="text-align: center; background-color:#63bfb9; color: #125e59; font-weight: 650 ">{get_needs_budget("May"):.2f}</td>
            <td style="text-align: center; background-color:#63bfb9; color: #125e59; font-weight: 650 ">{get_needs_budget("June"):.2f}</td>
            <td style="text-align: center; background-color:#63bfb9; color: #125e59; font-weight: 650 ">{get_needs_budget("July"):.2f}</td>
            <td style="text-align: center; background-color:#63bfb9; color: #125e59; font-weight: 650 ">{get_needs_budget("August"):.2f}</td>
            <td style="text-align: center; background-color:#63bfb9; color: #125e59; font-weight: 650 ">{get_needs_budget("September"):.2f}</td>
            <td style="text-align: center; background-color:#63bfb9; color: #125e59; font-weight: 650 ">{get_needs_budget("October"):.2f}</td>
            <td style="text-align: center; background-color:#63bfb9; color: #125e59; font-weight: 650 ">{get_needs_budget("November"):.2f}</td>
            <td style="text-align: center; background-color:#63bfb9; color: #125e59; font-weight: 650 ">{get_needs_budget("December"):.2f}</td>
            <td style="text-align: center; background-color:#63bfb9; color: #125e59; font-weight: 650 ">{basic_needs:.2f}</td>
        </tr>
        <tr>
            <th style="background-color:white; color: #125e59;" scope="row">Spent</th>
            <td style="text-align: center; background-color:white; color: #125e59; font-weight: 650 ">{get_needs_expenses("January"):.2f}</td>
            <td style="text-align: center; background-color:white; color: #125e59; font-weight: 650 ">{get_needs_expenses("February"):.2f}</td>
            <td style="text-align: center; background-color:white; color: #125e59; font-weight: 650 ">{get_needs_expenses("March"):.2f}</td>
            <td style="text-align: center; background-color:white; color: #125e59; font-weight: 650 ">{get_needs_expenses("April"):.2f}</td>
            <td style="text-align: center; background-color:white; color: #125e59; font-weight: 650 ">{get_needs_expenses("May"):.2f}</td>
            <td style="text-align: center; background-color:white; color: #125e59; font-weight: 650 ">{get_needs_expenses("June"):.2f}</td>
            <td style="text-align: center; background-color:white; color: #125e59; font-weight: 650 ">{get_needs_expenses("July"):.2f}</td>
            <td style="text-align: center; background-color:white; color: #125e59; font-weight: 650 ">{get_needs_expenses("August"):.2f}</td>
            <td style="text-align: center; background-color:white; color: #125e59; font-weight: 650 ">{get_needs_expenses("September"):.2f}</td>
            <td style="text-align: center; background-color:white; color: #125e59; font-weight: 650 ">{get_needs_expenses("October"):.2f}</td>
            <td style="text-align: center; background-color:white; color: #125e59; font-weight: 650 ">{get_needs_expenses("November"):.2f}</td>
            <td style="text-align: center; background-color:white; color: #125e59; font-weight: 650 ">{get_needs_expenses("December"):.2f}</td>
            <td style="text-align: center; background-color:white; color: #125e59; font-weight: 650 ">{get_total_needs_expenses():.2f}</td>
        </tr>
        <tr>
            <th style="background-color:white; color: #125e59;" scope="row">Remaining</th>
            <td style="text-align: center; background-color:white; color: #125e59; font-weight: 650 ">{get_needs_remaining("January"):.2f}</td>
            <td style="text-align: center; background-color:white; color: #125e59; font-weight: 650 ">{get_needs_remaining("February"):.2f}</td>
            <td style="text-align: center; background-color:white; color: #125e59; font-weight: 650 ">{get_needs_remaining("March"):.2f}</td>
            <td style="text-align: center; background-color:white; color: #125e59; font-weight: 650 ">{get_needs_remaining("April"):.2f}</td>
            <td style="text-align: center; background-color:white; color: #125e59; font-weight: 650 ">{get_needs_remaining("May"):.2f}</td>
            <td style="text-align: center; background-color:white; color: #125e59; font-weight: 650 ">{get_needs_remaining("June"):.2f}</td>
            <td style="text-align: center; background-color:white; color: #125e59; font-weight: 650 ">{get_needs_remaining("July"):.2f}</td>
            <td style="text-align: center; background-color:white; color: #125e59; font-weight: 650 ">{get_needs_remaining("August"):.2f}</td>
            <td style="text-align: center; background-color:white; color: #125e59; font-weight: 650 ">{get_needs_remaining("September"):.2f}</td>
            <td style="text-align: center; background-color:white; color: #125e59; font-weight: 650 ">{get_needs_remaining("October"):.2f}</td>
            <td style="text-align: center; background-color:white; color: #125e59; font-weight: 650 ">{get_needs_remaining("November"):.2f}</td>
            <td style="text-align: center; background-color:white; color: #125e59; font-weight: 650 ">{get_needs_remaining("December"):.2f}</td>
            <td style="text-align: center; background-color:white; color: #125e59; font-weight: 650 ">{get_total_needs_remaining():.2f}</td>
        </tr>
        
        <tr>
            <th style="background-color:#63bfb9; color: #125e59;" scope="row">Personal development budget</th>
            <td style="text-align: center; background-color:#63bfb9; color: #125e59; font-weight: 650 ">{get_10percentage_budget("January"):.2f}</td>
            <td style="text-align: center; background-color:#63bfb9; color: #125e59; font-weight: 650 ">{get_10percentage_budget("February"):.2f}</td>
            <td style="text-align: center; background-color:#63bfb9; color: #125e59; font-weight: 650 ">{get_10percentage_budget("March"):.2f}</td>
            <td style="text-align: center; background-color:#63bfb9; color: #125e59; font-weight: 650 ">{get_10percentage_budget("April"):.2f}</td>
            <td style="text-align: center; background-color:#63bfb9; color: #125e59; font-weight: 650 ">{get_10percentage_budget("May"):.2f}</td>
            <td style="text-align: center; background-color:#63bfb9; color: #125e59; font-weight: 650 ">{get_10percentage_budget("June"):.2f}</td>
            <td style="text-align: center; background-color:#63bfb9; color: #125e59; font-weight: 650 ">{get_10percentage_budget("July"):.2f}</td>
            <td style="text-align: center; background-color:#63bfb9; color: #125e59; font-weight: 650 ">{get_10percentage_budget("August"):.2f}</td>
            <td style="text-align: center; background-color:#63bfb9; color: #125e59; font-weight: 650 ">{get_10percentage_budget("September"):.2f}</td>
            <td style="text-align: center; background-color:#63bfb9; color: #125e59; font-weight: 650 ">{get_10percentage_budget("October"):.2f}</td>
            <td style="text-align: center; background-color:#63bfb9; color: #125e59; font-weight: 650 ">{get_10percentage_budget("November"):.2f}</td>
            <td style="text-align: center; background-color:#63bfb9; color: #125e59; font-weight: 650 ">{get_10percentage_budget("December"):.2f}</td>
            <td style="text-align: center; background-color:#63bfb9; color: #125e59; font-weight: 650 ">{personal_development:.2f}</td>
        </tr>
        <tr>
            <th scope="row">Spent</th>
            <td style="text-align: center; background-color:white; color: #125e59; font-weight: 650 ">{get_personal_development("January"):.2f}</td>
            <td style="text-align: center; background-color:white; color: #125e59; font-weight: 650 ">{get_personal_development("February"):.2f}</td>
            <td style="text-align: center; background-color:white; color: #125e59; font-weight: 650 ">{get_personal_development("March"):.2f}</td>
            <td style="text-align: center; background-color:white; color: #125e59; font-weight: 650 ">{get_personal_development("April"):.2f}</td>
            <td style="text-align: center; background-color:white; color: #125e59; font-weight: 650 ">{get_personal_development("May"):.2f}</td>
            <td style="text-align: center; background-color:white; color: #125e59; font-weight: 650 ">{get_personal_development("June"):.2f}</td>
            <td style="text-align: center; background-color:white; color: #125e59; font-weight: 650 ">{get_personal_development("July"):.2f}</td>
            <td style="text-align: center; background-color:white; color: #125e59; font-weight: 650 ">{get_personal_development("August"):.2f}</td>
            <td style="text-align: center; background-color:white; color: #125e59; font-weight: 650 ">{get_personal_development("September"):.2f}</td>
            <td style="text-align: center; background-color:white; color: #125e59; font-weight: 650 ">{get_personal_development("October"):.2f}</td>
            <td style="text-align: center; background-color:white; color: #125e59; font-weight: 650 ">{get_personal_development("November"):.2f}</td>
            <td style="text-align: center; background-color:white; color: #125e59; font-weight: 650 ">{get_personal_development("December"):.2f}</td>
            <td style="text-align: center; background-color:white; color: #125e59; font-weight: 650 ">{get_total_personal_development():.2f}</td>
        </tr>
        <tr>
            <th scope="row">Remaining</th>
            <td style="text-align: center; background-color:white; color: #125e59; font-weight: 650 ">{get_personal_remaining("January"):.2f}</td>
            <td style="text-align: center; background-color:white; color: #125e59; font-weight: 650 ">{get_personal_remaining("February"):.2f}</td>
            <td style="text-align: center; background-color:white; color: #125e59; font-weight: 650 ">{get_personal_remaining("March"):.2f}</td>
            <td style="text-align: center; background-color:white; color: #125e59; font-weight: 650 ">{get_personal_remaining("April"):.2f}</td>
            <td style="text-align: center; background-color:white; color: #125e59; font-weight: 650 ">{get_personal_remaining("May"):.2f}</td>
            <td style="text-align: center; background-color:white; color: #125e59; font-weight: 650 ">{get_personal_remaining("June"):.2f}</td>
            <td style="text-align: center; background-color:white; color: #125e59; font-weight: 650 ">{get_personal_remaining("July"):.2f}</td>
            <td style="text-align: center; background-color:white; color: #125e59; font-weight: 650 ">{get_personal_remaining("August"):.2f}</td>
            <td style="text-align: center; background-color:white; color: #125e59; font-weight: 650 ">{get_personal_remaining("September"):.2f}</td>
            <td style="text-align: center; background-color:white; color: #125e59; font-weight: 650 ">{get_personal_remaining("October"):.2f}</td>
            <td style="text-align: center; background-color:white; color: #125e59; font-weight: 650 ">{get_personal_remaining("November"):.2f}</td>
            <td style="text-align: center; background-color:white; color: #125e59; font-weight: 650 ">{get_personal_remaining("December"):.2f}</td>
            <td style="text-align: center; background-color:white; color: #125e59; font-weight: 650 ">{get_total_personal_remaining():.2f}</td>
        </tr>
        <tr>
            <th style="background-color:#63bfb9; color: #125e59;" scope="row">Leisure budget</th>
            <td style="text-align: center; background-color:#63bfb9; color: #125e59; font-weight: 650 ">{get_10percentage_budget("January"):.2f}</td>
            <td style="text-align: center; background-color:#63bfb9; color: #125e59; font-weight: 650 ">{get_10percentage_budget("February"):.2f}</td>
            <td style="text-align: center; background-color:#63bfb9; color: #125e59; font-weight: 650 ">{get_10percentage_budget("March"):.2f}</td>
            <td style="text-align: center; background-color:#63bfb9; color: #125e59; font-weight: 650 ">{get_10percentage_budget("April"):.2f}</td>
            <td style="text-align: center; background-color:#63bfb9; color: #125e59; font-weight: 650 ">{get_10percentage_budget("May"):.2f}</td>
            <td style="text-align: center; background-color:#63bfb9; color: #125e59; font-weight: 650 ">{get_10percentage_budget("June"):.2f}</td>
            <td style="text-align: center; background-color:#63bfb9; color: #125e59; font-weight: 650 ">{get_10percentage_budget("July"):.2f}</td>
            <td style="text-align: center; background-color:#63bfb9; color: #125e59; font-weight: 650 ">{get_10percentage_budget("August"):.2f}</td>
            <td style="text-align: center; background-color:#63bfb9; color: #125e59; font-weight: 650 ">{get_10percentage_budget("September"):.2f}</td>
            <td style="text-align: center; background-color:#63bfb9; color: #125e59; font-weight: 650 ">{get_10percentage_budget("October"):.2f}</td>
            <td style="text-align: center; background-color:#63bfb9; color: #125e59; font-weight: 650 ">{get_10percentage_budget("November"):.2f}</td>
            <td style="text-align: center; background-color:#63bfb9; color: #125e59; font-weight: 650 ">{get_10percentage_budget("December"):.2f}</td>
            <td style="text-align: center; background-color:#63bfb9; color: #125e59; font-weight: 650 ">{leisure:.2f}</td>
        </tr>
        <tr>
            <th scope="row">Spent</th>
            <td style="text-align: center; background-color:white; color: #125e59; font-weight: 650 ">{get_leisure("January"):.2f}</td>
            <td style="text-align: center; background-color:white; color: #125e59; font-weight: 650 ">{get_leisure("February"):.2f}</td>
            <td style="text-align: center; background-color:white; color: #125e59; font-weight: 650 ">{get_leisure("March"):.2f}</td>
            <td style="text-align: center; background-color:white; color: #125e59; font-weight: 650 ">{get_leisure("April"):.2f}</td>
            <td style="text-align: center; background-color:white; color: #125e59; font-weight: 650 ">{get_leisure("May"):.2f}</td>
            <td style="text-align: center; background-color:white; color: #125e59; font-weight: 650 ">{get_leisure("June"):.2f}</td>
            <td style="text-align: center; background-color:white; color: #125e59; font-weight: 650 ">{get_leisure("July"):.2f}</td>
            <td style="text-align: center; background-color:white; color: #125e59; font-weight: 650 ">{get_leisure("August"):.2f}</td>
            <td style="text-align: center; background-color:white; color: #125e59; font-weight: 650 ">{get_leisure("September"):.2f}</td>
            <td style="text-align: center; background-color:white; color: #125e59; font-weight: 650 ">{get_leisure("October"):.2f}</td>
            <td style="text-align: center; background-color:white; color: #125e59; font-weight: 650 ">{get_leisure("November"):.2f}</td>
            <td style="text-align: center; background-color:white; color: #125e59; font-weight: 650 ">{get_leisure("December"):.2f}</td>
            <td style="text-align: center; background-color:white; color: #125e59; font-weight: 650 ">{get_total_leisure():.2f}</td>
        </tr>
        <tr>
            <th scope="row">Remaining</th>
            <td style="text-align: center; background-color:white; color: #125e59; font-weight: 650 ">{get_leisure_remaining("January"):.2f}</td>
            <td style="text-align: center; background-color:white; color: #125e59; font-weight: 650 ">{get_leisure_remaining("February"):.2f}</td>
            <td style="text-align: center; background-color:white; color: #125e59; font-weight: 650 ">{get_leisure_remaining("March"):.2f}</td>
            <td style="text-align: center; background-color:white; color: #125e59; font-weight: 650 ">{get_leisure_remaining("April"):.2f}</td>
            <td style="text-align: center; background-color:white; color: #125e59; font-weight: 650 ">{get_leisure_remaining("May"):.2f}</td>
            <td style="text-align: center; background-color:white; color: #125e59; font-weight: 650 ">{get_leisure_remaining("June"):.2f}</td>
            <td style="text-align: center; background-color:white; color: #125e59; font-weight: 650 ">{get_leisure_remaining("July"):.2f}</td>
            <td style="text-align: center; background-color:white; color: #125e59; font-weight: 650 ">{get_leisure_remaining("August"):.2f}</td>
            <td style="text-align: center; background-color:white; color: #125e59; font-weight: 650 ">{get_leisure_remaining("September"):.2f}</td>
            <td style="text-align: center; background-color:white; color: #125e59; font-weight: 650 ">{get_leisure_remaining("October"):.2f}</td>
            <td style="text-align: center; background-color:white; color: #125e59; font-weight: 650 ">{get_leisure_remaining("November"):.2f}</td>
            <td style="text-align: center; background-color:white; color: #125e59; font-weight: 650 ">{get_leisure_remaining("December"):.2f}</td>
            <td style="text-align: center; background-color:white; color: #125e59; font-weight: 650 ">{get_leisure_total_remaining():.2f}</td>
        </tr>
        <tr>
            <th style="background-color:#63bfb9; color: #125e59;" scope="row">Donations budget</th>
            <td style="text-align: center; background-color:#63bfb9; color: #125e59; font-weight: 650 ">{get_donations_budget("January"):.2f}</td>
            <td style="text-align: center; background-color:#63bfb9; color: #125e59; font-weight: 650 ">{get_donations_budget("February"):.2f}</td>
            <td style="text-align: center; background-color:#63bfb9; color: #125e59; font-weight: 650 ">{get_donations_budget("March"):.2f}</td>
            <td style="text-align: center; background-color:#63bfb9; color: #125e59; font-weight: 650 ">{get_donations_budget("April"):.2f}</td>
            <td style="text-align: center; background-color:#63bfb9; color: #125e59; font-weight: 650 ">{get_donations_budget("May"):.2f}</td>
            <td style="text-align: center; background-color:#63bfb9; color: #125e59; font-weight: 650 ">{get_donations_budget("June"):.2f}</td>
            <td style="text-align: center; background-color:#63bfb9; color: #125e59; font-weight: 650 ">{get_donations_budget("July"):.2f}</td>
            <td style="text-align: center; background-color:#63bfb9; color: #125e59; font-weight: 650 ">{get_donations_budget("August"):.2f}</td>
            <td style="text-align: center; background-color:#63bfb9; color: #125e59; font-weight: 650 ">{get_donations_budget("September"):.2f}</td>
            <td style="text-align: center; background-color:#63bfb9; color: #125e59; font-weight: 650 ">{get_donations_budget("October"):.2f}</td>
            <td style="text-align: center; background-color:#63bfb9; color: #125e59; font-weight: 650 ">{get_donations_budget("November"):.2f}</td>
            <td style="text-align: center; background-color:#63bfb9; color: #125e59; font-weight: 650 ">{get_donations_budget("December"):.2f}</td>
            <td style="text-align: center; background-color:#63bfb9; color: #125e59; font-weight: 650 ">{donations:.2f}</td>
        </tr>
        <tr>
            <th scope="row">Spent</th>
            <td style="text-align: center; background-color:white; color: #125e59; font-weight: 650 ">{get_donations("January"):.2f}</td>
            <td style="text-align: center; background-color:white; color: #125e59; font-weight: 650 ">{get_donations("February"):.2f}</td>
            <td style="text-align: center; background-color:white; color: #125e59; font-weight: 650 ">{get_donations("March"):.2f}</td>
            <td style="text-align: center; background-color:white; color: #125e59; font-weight: 650 ">{get_donations("April"):.2f}</td>
            <td style="text-align: center; background-color:white; color: #125e59; font-weight: 650 ">{get_donations("May"):.2f}</td>
            <td style="text-align: center; background-color:white; color: #125e59; font-weight: 650 ">{get_donations("June"):.2f}</td>
            <td style="text-align: center; background-color:white; color: #125e59; font-weight: 650 ">{get_donations("July"):.2f}</td>
            <td style="text-align: center; background-color:white; color: #125e59; font-weight: 650 ">{get_donations("August"):.2f}</td>
            <td style="text-align: center; background-color:white; color: #125e59; font-weight: 650 ">{get_donations("September"):.2f}</td>
            <td style="text-align: center; background-color:white; color: #125e59; font-weight: 650 ">{get_donations("October"):.2f}</td>
            <td style="text-align: center; background-color:white; color: #125e59; font-weight: 650 ">{get_donations("November"):.2f}</td>
            <td style="text-align: center; background-color:white; color: #125e59; font-weight: 650 ">{get_donations("December"):.2f}</td>
            <td style="text-align: center; background-color:white; color: #125e59; font-weight: 650 ">{get_total_donations():.2f}</td>
        </tr>
        <tr>
            <th scope="row">Remaining</th>
            <td style="text-align: center; background-color:white; color: #125e59; font-weight: 650 ">{get_donations_remaining("January"):.2f}</td>
            <td style="text-align: center; background-color:white; color: #125e59; font-weight: 650 ">{get_donations_remaining("February"):.2f}</td>
            <td style="text-align: center; background-color:white; color: #125e59; font-weight: 650 ">{get_donations_remaining("March"):.2f}</td>
            <td style="text-align: center; background-color:white; color: #125e59; font-weight: 650 ">{get_donations_remaining("April"):.2f}</td>
            <td style="text-align: center; background-color:white; color: #125e59; font-weight: 650 ">{get_donations_remaining("May"):.2f}</td>
            <td style="text-align: center; background-color:white; color: #125e59; font-weight: 650 ">{get_donations_remaining("June"):.2f}</td>
            <td style="text-align: center; background-color:white; color: #125e59; font-weight: 650 ">{get_donations_remaining("July"):.2f}</td>
            <td style="text-align: center; background-color:white; color: #125e59; font-weight: 650 ">{get_donations_remaining("August"):.2f}</td>
            <td style="text-align: center; background-color:white; color: #125e59; font-weight: 650 ">{get_donations_remaining("September"):.2f}</td>
            <td style="text-align: center; background-color:white; color: #125e59; font-weight: 650 ">{get_donations_remaining("October"):.2f}</td>
            <td style="text-align: center; background-color:white; color: #125e59; font-weight: 650 ">{get_donations_remaining("November"):.2f}</td>
            <td style="text-align: center; background-color:white; color: #125e59; font-weight: 650 ">{get_donations_remaining("December"):.2f}</td>
            <td style="text-align: center; background-color:white; color: #125e59; font-weight: 650 ">{get_total_donations_remaining():.2f}</td>
        </tr>
        <tr>
            <th style="background-color:#63bfb9; color: #125e59;" scope="row">Long-term savings</th>
            <td style="text-align: center; background-color:#63bfb9; color: #125e59; font-weight: 650 ">{get_long_term_savings("January"):.2f}</td>
            <td style="text-align: center; background-color:#63bfb9; color: #125e59; font-weight: 650 ">{get_long_term_savings("February"):.2f}</td>
            <td style="text-align: center; background-color:#63bfb9; color: #125e59; font-weight: 650 ">{get_long_term_savings("March"):.2f}</td>
            <td style="text-align: center; background-color:#63bfb9; color: #125e59; font-weight: 650 ">{get_long_term_savings("April"):.2f}</td>
            <td style="text-align: center; background-color:#63bfb9; color: #125e59; font-weight: 650 ">{get_long_term_savings("May"):.2f}</td>
            <td style="text-align: center; background-color:#63bfb9; color: #125e59; font-weight: 650 ">{get_long_term_savings("June"):.2f}</td>
            <td style="text-align: center; background-color:#63bfb9; color: #125e59; font-weight: 650 ">{get_long_term_savings("July"):.2f}</td>
            <td style="text-align: center; background-color:#63bfb9; color: #125e59; font-weight: 650 ">{get_long_term_savings("August"):.2f}</td>
            <td style="text-align: center; background-color:#63bfb9; color: #125e59; font-weight: 650 ">{get_long_term_savings("September"):.2f}</td>
            <td style="text-align: center; background-color:#63bfb9; color: #125e59; font-weight: 650 ">{get_long_term_savings("October"):.2f}</td>
            <td style="text-align: center; background-color:#63bfb9; color: #125e59; font-weight: 650 ">{get_long_term_savings("November"):.2f}</td>
            <td style="text-align: center; background-color:#63bfb9; color: #125e59; font-weight: 650 ">{get_long_term_savings("December"):.2f}</td>
            <td style="text-align: center; background-color:#63bfb9; color: #125e59; font-weight: 650 ">{long_term_savingsT:.2f}</td>
        </tr>
        
    </table>
    {img}
    {img2}

    '''

    # to replace the word SUMMARY for the html
    return html_page.replace("$$SUMMARY$$", html) 


