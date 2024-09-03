from flask import Blueprint, render_template, request, flash, redirect, url_for, jsonify
from flask_login import login_required, current_user
from .models import Tree
from . import db
import json

views = Blueprint('views', __name__)

@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    user_trees = Tree.query.filter_by(user_id=current_user.id).all()
    return render_template("home.html", user=current_user, trees=user_trees)

@views.route('/plant-tree', methods=['POST'])
@login_required
def plant_tree():
    # Add a new tree to the database
    tree = Tree(user_id=current_user.id)
    db.session.add(tree)
    db.session.commit()
    return jsonify({'success': True})

@views.route('/delete-tree', methods=['POST'])
@login_required
def delete_tree():
    data = json.loads(request.data)
    tree_id = data['treeId']
    tree = Tree.query.get(tree_id)
    if tree and tree.user_id == current_user.id:
        db.session.delete(tree)
        db.session.commit()
        return jsonify({'success': True})
    return jsonify({'success': False})
