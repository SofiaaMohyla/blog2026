from flask import *
from db import *
app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/post/delete/<int:post_id>", methods=["POST", "GET"])
def post_delete_func(post_id):
    post_delete(post_id)
    return redirect(url_for("index"))
@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/post/category/<category_name>", methods=["POST", "GET"])
def show_category(category_name):
    category = get_category_by_name(category_name)
    posts = get_posts(category["category_id"])
    error = None
    if request.method == "POST":
        title = request.form.get("title", "").strip()
        text = request.form.get("text", "").strip()

        if not title or not text:
            error = "Заповніть заголовок і текст поста."
        else:
            add_post(category["category_id"], title, text)
            return redirect(url_for("show_category", category_name=category_name))
    return render_template("post_category.html",
                           category=category,
                           posts=posts,
                           error=error)
@app.route("/post/view/<int:post_id>")
def post_view(post_id):
    post = get_post(post_id)

    return render_template("post_view.html", post=post)


app.run(debug=True)
