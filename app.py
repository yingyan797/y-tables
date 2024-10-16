from flask import Flask, request, render_template
from tablevis import read_table, table_process

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    fm = request.form
    html, keywords = fm.get("html"), fm.get("kw")
    table = []
    if html and fm.get("process"):
        rt = read_table(html)
        table = table_process(rt, keywords)
    return render_template("index.html", html="" if not html else html, table=table, keywords="" if not keywords else keywords)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002, debug=True)
