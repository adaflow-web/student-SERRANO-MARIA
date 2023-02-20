#python -m flask --app myparty.py run

import flask
app= flask.Flask("myparty")

def get_html(page_name):
    html_file= open(page_name + ".html")
    content= html_file.read()
    html_file.close()
    return content


def get_guests():
    partydb = open("partydb.txt")
    content = partydb.read()
    partydb.close()
    guests = content.split("\n")
    return sorted(guests)

@app.route("/")
def homepage():
    return get_html("party")

@app.route("/guests")
def guests():
    html_page = get_html("guests")
    guests = get_guests()
    actual_values = ""
    for guest in guests:
        actual_values += "<p>" + guest + "</p>"
    return html_page.replace("$$GUESTS$$", actual_values)