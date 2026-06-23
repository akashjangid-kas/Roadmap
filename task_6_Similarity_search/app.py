from flask import Flask, render_template, request

from rerank import rank_query

app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def home():

    results = []
    query = ""

    if request.method == "POST":

        query = request.form["query"]

        if query.strip():
            results = rank_query(query)

    return render_template(
        "index.html",
        query=query,
        results=results
    )


if __name__ == "__main__":
    app.run(debug=True)