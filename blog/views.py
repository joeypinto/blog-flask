from flask import Blueprint, render_template, request, flash, jsonify
from .models import Content,Post
from flask_login import current_user
from blog.config import db
import markdown

views = Blueprint('views', __name__)



@views.route("/", methods=['GET', 'POST'])
def home():
    contents = Content.query.all() 
    if request.method == 'POST':
        id = request.form.get('search')
        id = '%' + id +'%'
        posts = Post.query.filter(Post.title.like(id))
        return render_template("home.html",posts=posts,contents=contents,user=current_user)
    for i in request.args.keys():
        if i == 'content_type':
            id = request.args.get('content_type') 
            print(id) 
            posts = Post.query.filter(Post.content_id == id)              
            return render_template("home.html",posts=posts,contents=contents,user=current_user)
    posts = Post.query.all()       
    return render_template("home.html",posts=posts,contents=contents,user=current_user)

@views.route("/view")
def post_view():    
    contents = Content.query.all() 
    key = request.args.keys()
    for i in request.args.keys():
        if i == 'id':
            id = request.args.get('id')
            posts = Post.query.get(id)    
            posts.description = markdown.markdown(posts.description)
            return render_template("post_view.html",posts=posts,contents=contents,user=current_user)             
        
