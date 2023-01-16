import random

from data import api_connection as rest_api
from data import api_images as unsplash
from flask import Flask, render_template, request

app = Flask(__name__, static_url_path='/static')


@app.route("/")
@app.route("/quote")
def random_quote():
    quotes = [rest_api.get_quote()]
    return render_template('home.html', quotes=quotes)


@app.route("/quotes")
def random_quotes():
    qry = {'limit': random.randint(2, 15)}
    quotes = rest_api.get_quotes(qry=qry)
    return render_template('home.html', quotes=quotes)


@app.route("/authors", methods=['GET'])
def authors_quotes():
    author_name = request.args.get("author", '')
    quotes = rest_api.get_author_quotes(sub_url=f"author/{author_name}")
    quotes_with_images = unsplash.add_images(quotes=quotes, search=author_name)
    return render_template('home.html', quotes=quotes_with_images)


@app.route("/tags", methods=['GET'])
def quotes_tags():
    tag = request.args.get("tag", '')
    quotes = rest_api.get_author_quotes(sub_url=f"tags/{tag}")
    quotes_with_images = unsplash.add_images(quotes=quotes, search=tag)

    return render_template('home.html', quotes=quotes_with_images)


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=1031)
