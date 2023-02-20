#python -m flask --app address.py run

import flask
app= flask.Flask("address")

def get_html(page_name):
    html_file = open(page_name + ".html")
    content =html_file.read()
    html_file.close()
    return content

def get_contacts():
    contactsdb= open("contactsdb.txt")
    content= contactsdb.read()
    contactsdb.close()
    contacts= content.split("\n")
    return contacts

@app.route("/")
def homepage():
    return get_html("address_book")

@app.route("/contacts")
def contacts():
    html_page= get_html("contacts")
    contacts= get_contacts()

    actual_values = ""
    for contact in contacts:
        actual_values += "<p>" + contact + "</p>"
    return html_page.replace("$$CONTACTS$$", actual_values )

@app.route("/search")
def searching():
    html_page = get_html("contacts")
    question= flask.request.args.get("q")
    contacts= get_contacts()
    result=""
    
    for contact in contacts:
        if contact.upper().find(question.upper()) != -1:
            result += "<p>" + contact + "</p>" + ("\n")
    if result == "":
        result= "<p>No result found</p>"
    
    return html_page.replace("$$CONTACTS$$", result)