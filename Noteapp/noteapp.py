#python -m flask --app noteapp.py run
import flask

app= flask.Flask("noteapp")

def get_html(page_name):
    html_file= open(page_name + ".html")
    content= html_file.read()
    html_file.close()
    return content

def get_notes():
    notedb = open("notedb.txt")
    content = notedb.read()
    notedb.close()
    notes = content.split("\n")
    return notes

@app.route("/")
def homepage():
    return get_html("noteapp")

@app.route("/notes")
def notes():
    html_page = get_html("notes")
    notes = get_notes()
    actual_values = ""
    for note in notes:
        actual_values += "<p>" + note + "</p>"
    return html_page.replace("$$NOTES$$", actual_values)

@app.route("/write")
def writing():
    input= flask.request.args.get("w")    
    file= open('notedb.txt', 'a')
    file.write(input + ("\n"))
    file.close()
    message= "<a class='link' href='http://localhost:5000'>Go to homepage</a>" + "<p style= 'font-size: 30px; color: green '><i><b>" + input + "</b></i> is correctly saved in notes""</p>" + "<blooquote></blockquote>"
    return message

@app.route("/search")
def searching():
    html_page = get_html("notes")
    question= flask.request.args.get("q")
    notes= get_notes()
    result=""
    
    for note in notes:
        if note.upper().find(question.upper()) != -1:
            result += "<p>" + note + "</p>" + ("\n")
    if result == "":
        result= "<p>No result found</p>"
    
    return html_page.replace("$$NOTES$$", result)



 