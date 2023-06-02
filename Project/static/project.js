// open a window to introduce the amount of a expense
async function call_wind(element) {
    const subcategory = element.getAttribute('data-subcategory');
    const category = element.getAttribute('data-category');
    const sub = subcategory === "" ? '<input id="swal-input3" class="swal2-input" placeholder="Subcategory...">' : "";
    const { value: formValues } = await Swal.fire({
        title: 'Add the amount and the date of your expense',
        html:
            // <-- in case we click on the button others, you have to add an input type text in the window so the user can write the name of the subcategory-->
            '<input id="swal-input1" class="swal2-input" placeholder="Amount...">' +
            `<input id="swal-input2" type="date" placeholder="dd-mm-yyyy" name="trip-start" value=${new Date().toJSON().slice(0, 10)
                } min = "2023-01-01" >`.concat(sub),

        focusConfirm: false,
        showCancelButton: true,
        preConfirm: () => {
            // checking if we have an amount
            if (document.getElementById('swal-input1').value) {
                return [
                    document.getElementById('swal-input1').value,
                    document.getElementById('swal-input2').value,
                    subcategory === "" && document.getElementById('swal-input3').value
                ]
                // in case we dont have an amount, we ask for it   
            } else {
                Swal.showValidationMessage('You need to write an amount')
            }
        }
    })

    if (formValues) {
        if (localStorage.getItem('data') == null) {
            localArray = [];
        } else {
            localArray = JSON.parse(localStorage.getItem('data'))
        }

        localArray.push({ category: category, subcategory: subcategory === '' ? formValues[2] : subcategory, amount: formValues[0], date_expense: formValues[1] })
        localStorage.setItem('data', JSON.stringify(localArray));
        Swal.fire('Added!', '', 'success')
    }
}

// saving the expenses
async function send_data() {
    Swal.fire({
        title: 'Are you sure?',
        text: "You won't be able to revert this!",
        icon: 'warning',
        showCancelButton: true,
        confirmButtonColor: '#3085d6',
        cancelButtonColor: '#d33',
        confirmButtonText: 'Yes!'
    }).then(async (result) => {
        if (result.isConfirmed) {
            const localStorageData = localStorage.getItem('data')
            debugger
            if (localStorageData != null) {
                const localArray = JSON.parse(localStorageData)
                const result = await fetch("http://127.0.0.1:5000/save_expenses", {
                    method: "POST", headers: {
                        'Accept': 'application/json',
                        'Content-Type': 'application/json'
                    }, body: JSON.stringify(localArray)
                })
                const response = await result.json();
                localStorage.clear()
                console.log(response)
                Swal.fire(
                    'Saved!',
                    'Your expenses have been saved.',
                    'success'
                )
            }
        }
    })
}

// selecting the amount you want to save in the week challenge
function btnDone(element) {
    if (this.style.backgroundColor != "rgb(20, 156, 147)" && this.style.color != "rgb(255, 255, 255)") {
        Swal.fire({
            title: 'Do you want to save the changes?',
            showDenyButton: true,
            showCancelButton: false,
            confirmButtonText: 'Save',
            denyButtonText: `Don't save`,
        }).then((result) => {
            // once we confirm, the color of the cell changes so we know we have already saved that amount of money
            if (result.isConfirmed) {
                this.style.backgroundColor = "#149c93";
                this.style.color = "#fff";
                send_week(this.innerHTML)
                // Swal.fire('Saved!', '', 'success')

            }
        })
    } else {
        Swal.fire({
            // in case we try to save an amountof money already saved
            title: "You've already saved this amount of money",
            showDenyButton: false,
            showCancelButton: false,
            confirmButtonText: 'Ok',
        })
    }
}

// we send the amount of the week and we check how many amounts are already saved
async function send_week(week) {
    const result = await fetch("http://127.0.0.1:5000/save_savings", {
        method: "POST", headers: {
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        }, body: JSON.stringify(week)
    })
    const response = await result.json();
    // we check how many amounts are already saved, if the result is 52 it means that we have already completed the table
    if (response.status === 'Table is full') {
        checkWeeksInDatabase();
        Swal.fire({
            title: "<el style='padding-bottom: 10px'>Congratulations</el>",
            // and you get an alert telling you the amount you've saved
            html: "<p style='font-size: 22px; color: #125e59; text-align: center; font-weight: bold;'>You have saved 1378 CHF</p>",
            iconHtml: '<img style="height: 100px;" src="static/img/trophy.png">',
            showCancelButton: false,
            confirmButtonColor: '#3085d6',
            confirmButtonText: 'Ok'
        }).then(async (result) => {
            if (result.isConfirmed) {
                window.location.reload()
            }
        })
    }
}

// element addEventListener to all the cells so we can click on any of them
async function on_load() {
    const numbers = document.getElementsByClassName("week_number");
    for (let i = 0; i < numbers.length; i++) {
        numbers[i].addEventListener("click", btnDone)
    }

    checkWeeksInDatabase();
}

// every time we open the aplication we need to check the numbers of the week challenge that are already saved
async function checkWeeksInDatabase() {
    const result = await fetch("http://127.0.0.1:5000/get_savings")
    const data = await result.json();
    console.log(data)

    for (d of data) {
        // showing them in a different color
        document.getElementById(d[0]).style.backgroundColor = "#149c93";
        document.getElementById(d[0]).style.color = "#fff";
    }
}

// function to get what Cris and Luis are doing and write it in a paragraph
async function on_load_project() {
    const content = document.getElementById("content")
    const newPara = document.createElement("p")

    const result = await fetch("http://127.0.0.1:5000/activity")
    const activity = await result.json();
    newPara.innerText = activity["text"]
    content.append(newPara)
}


// clicking on the button to see what we have already saved in the week challenge
async function on_load_savings() {
    const result = await fetch("http://127.0.0.1:5000/week_challenge")
    const amount_challenge = await result.json();
    Swal.fire(amount_challenge["savings"])
}


// adding the salary amount and its month
async function wind_salary() {
    const salary = document.getElementById("salary");
    const { value: formValues } = await Swal.fire({
        title: 'Salary details',
        html:

            `<input id="swal-inp1" type="date" placeholder="dd-mm-yyyy" name="month" value=${new Date().toJSON().slice(0, 10)
            } min = "2023-01-01" >` +
            '<input id="swal-inp2" class="swal2-input" placeholder="Amount...">',

        focusConfirm: false,
        showCancelButton: true,
        preConfirm: () => {

            if (document.getElementById('swal-inp2').value) {
                return [
                    document.getElementById('swal-inp1').value,
                    document.getElementById('swal-inp2').value
                ]
            } else {
                // the amount is mandatory
                Swal.showValidationMessage('You need to write an amount')
            }
        }
    })

    // confirming that we want to save the salary
    if (formValues) {
        const result = await fetch("http://127.0.0.1:5000/save_salary", {
            method: "POST", headers: {
                'Accept': 'application/json',
                'Content-Type': 'application/json'
            }, body: JSON.stringify(formValues)
        })
        const response = await result.json();
        Swal.fire(
            'Your salary has been saved'
        )
    }
}


async function on_load_summary() {
    const month = document.getElementsByClassName("month");
    for (let i = 0; i < month.length; i++) {
        month[i].addEventListener("click", btnDone)
    }

    checkWeeksInDatabase();
}

async function get_summary(month) {
    await fetch('http://127.0.0.1:5000/summary?' + new URLSearchParams({
        month: month
    }))
}


async function getSummary(month) {
    const result = await fetch("http://127.0.0.1:5000/summary", {
        method: "POST",
        headers: {
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(month)
    })
    const response = await result.json();
    console.log(response)
}