import os
import secrets
from PIL import Image
from flask import Blueprint, render_template, request, redirect,flash,jsonify
from .models import Content,Post
from blog.config import db
from flask_login import current_user,login_required


admin = Blueprint('admin', __name__)


@admin.route('/')
def dashboard():
    return render_template("dashboard.html",user=current_user)

@admin.route("/nova_postagem", methods=['GET', 'POST'])
@login_required
def new_post():
    conteudos = Content.query.all()
    if request.method == 'POST':
        title = request.form.get('title')
        description = request.form.get('description')
        content_type = request.form.get('content_type')
        if request.files['image_file'].filename == '':
            image_file = "default.jpg"         
        else:
            image_file = save_raw_picture(request.files['image_file']) 
        new_post = Post(title=title,description=description,image_file=image_file,content_id=content_type,user_id=current_user.id)
        db.session.add(new_post)
        db.session.commit()
        flash('Post adicionado com sucesso!',category='success')
        return render_template("novo_post.html",conteudos=conteudos,user=current_user)

    
    return render_template("novo_post.html",conteudos=conteudos,user=current_user)

@admin.route("/content_type", methods=['GET', 'POST'])
@login_required
def conteudo():
    if request.method == 'POST':
        name = request.form.get('name')
        new_conteudo = Content(name = name)
        db.session.add(new_conteudo)
        db.session.commit()
        flash('Categoria adicionada!',category='success')
        return redirect('./content_type')
    conteudos = Content.query.all()
    return render_template("content_type.html", conteudos=conteudos,user=current_user)


@admin.route("/list", methods=['GET', 'POST'])
@login_required
def list():  
    posts = Post.query.all()
    return render_template("post_list.html", posts=posts,user=current_user)



def save_compressed_picture(form_picture):
    """
    Function that gets the file contained in the parameter `form_picture`, compresses it to a 125x125 pixels image,
    and saves it to the `static/profile_pics` folder.
    """
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(admin.root_path, 'static', 'profile_pics', picture_fn)

    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_fn


def save_raw_picture(form_picture):
    """
    Function that gets the file contained in the parameter `form_picture`,
    and saves it to the `static/profile_pics` folder.
    """
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(admin.root_path, 'static', 'profile_pics', picture_fn)
    form_picture.save(picture_path)

    return picture_fn


@admin.route('/api/data')
def data():
    query =  Post.query
    data = [post.to_dict() for post in query]
    tabela = {
        'data': data,
        'recordsTotal': Post.query.count()
    }
    return jsonify(data)


