import flask
from flask import render_template, redirect, url_for, request, abort

import models
import forms


app = flask.Flask(__name__)
app.config["SECRET_KEY"] = "This is secret key"
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://coe:CoEpasswd@localhost:5432/coedb"

models.init_app(app)
db = models.db  # ใช้ db เป็น global ในไฟล์นี้เลย

@app.route("/")
def index():
    notes = db.session.execute(
        db.select(models.Note).order_by(models.Note.title)
    ).scalars()
    return render_template("index.html", notes=notes)

@app.route("/notes/create", methods=["GET", "POST"])
def notes_create():
    form = forms.NoteForm()
    if not form.validate_on_submit():
        print("error", form.errors)
        return render_template("notes-create.html", form=form)

    note = models.Note()
    form.populate_obj(note)
    note.tags = []

    for tag_name in form.tags.data:
        tag = db.session.execute(
            db.select(models.Tag).where(models.Tag.name == tag_name)
        ).scalars().first()

        if not tag:
            tag = models.Tag(name=tag_name)
            db.session.add(tag)

        note.tags.append(tag)

    db.session.add(note)
    db.session.commit()
    return redirect(url_for("index"))

@app.route("/tags/<tag_name>")
def tags_view(tag_name):
    tag = db.session.execute(
        db.select(models.Tag).where(models.Tag.name == tag_name)
    ).scalars().first()

    if not tag:
        abort(404)

    notes = db.session.execute(
        db.select(models.Note).where(models.Note.tags.any(id=tag.id))
    ).scalars()
    return render_template("tags-view.html", tag_name=tag_name, notes=notes)

@app.route("/notes/<int:note_id>/edit", methods=["GET", "POST"])
def notes_edit(note_id):
    note = db.session.get(models.Note, note_id)
    if not note:
        abort(404)

    form = forms.NoteForm(obj=note)
    if form.validate_on_submit():
        form.populate_obj(note)
        note.tags = []

        for tag_name in form.tags.data:
            tag = db.session.execute(
                db.select(models.Tag).where(models.Tag.name == tag_name)
            ).scalars().first()

            if not tag:
                tag = models.Tag(name=tag_name)
                db.session.add(tag)

            note.tags.append(tag)

        db.session.commit()
        return redirect(url_for("index"))

    # Prepopulate tags
    form.tags.data = [tag.name for tag in note.tags]
    return render_template("notes-create.html", form=form)

@app.route("/notes/<int:note_id>/delete", methods=["POST"])
def notes_delete(note_id):
    note = db.session.get(models.Note, note_id)
    if not note:
        abort(404)

    db.session.delete(note)
    db.session.commit()
    return redirect(url_for("index"))

@app.route("/tags/<tag_name>/edit", methods=["GET", "POST"])
def tags_edit(tag_name):
    tag = db.session.execute(
        db.select(models.Tag).where(models.Tag.name == tag_name)
    ).scalars().first()

    if not tag:
        abort(404)

    if request.method == "POST":
        new_name = request.form.get("name", "").strip()
        if new_name and new_name != tag.name:
            tag.name = new_name
            db.session.commit()
            return redirect(url_for("tags_view", tag_name=tag.name))

    return render_template("tags-edit.html", tag=tag)

@app.route("/tags/<tag_name>/delete", methods=["POST"])
def tags_delete(tag_name):
    tag = db.session.execute(
        db.select(models.Tag).where(models.Tag.name == tag_name)
    ).scalars().first()

    if not tag:
        abort(404)

    db.session.delete(tag)
    db.session.commit()
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(debug=True)
