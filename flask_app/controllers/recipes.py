from flask_app import app
from flask import render_template, redirect, request, session
from flask_app.models.user import User
from flask_app.models.recipe import Recipe
from flask import flash


@app.route('/createRecipe')
def createForm():
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        'user_id': session['user_id']
    }
    return render_template('createRecipe.html', loggedUser= User.get_user_by_id(data),)


@app.route('/create/recipe', methods = ['POST'])
def createRecipe():
    if 'user_id' not in session:
        return redirect('/logout')
    if not Recipe.validate_recipe(request.form):
        return redirect(request.referrer)
   
    Recipe.create_recipe(request.form)
    return redirect('/')

@app.route('/delete/<int:id>')
def delete(id):
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        'recipe_id': id,
        'user_id': session['user_id']
    }
    currentRecipe = Recipe.get_recipe_by_id(data)

    if not session['user_id'] == currentRecipe['user_id']:
        flash('You cant delete this', 'noAccessError')
        return redirect('/dashboard')

    Recipe.delete(data)
    return redirect(request.referrer)


@app.route('/recipe/<int:id>')
def showOne(id):
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        'recipe_id': id,
        'user_id': session['user_id']
    }
    return render_template('recipe.html', loggedUser= User.get_user_by_id(data),recipe = Recipe.get_recipe_by_id(data))

@app.route('/edit/<int:id>')
def editForm(id):
    if 'user_id' not in session:
        return redirect('/logout')

    data = {
            'recipe_id': id,
            'user_id': session['user_id']
        }
    currentRecipe = Recipe.get_recipe_by_id(data)

    if not session['user_id'] == currentRecipe['user_id']:
        flash('You cant delete this', 'noAccessError')
        return redirect('/dashboard')

    return render_template('updateRecipe.html', loggedUser= User.get_user_by_id(data), recipe = Recipe.get_recipe_by_id(data))

@app.route('/update/<int:id>', methods = ['POST'])
def updateRecipe(id):
    if 'user_id' not in session:
        return redirect('/logout')
    if not Recipe.validate_recipe(request.form):
        return redirect(request.referrer)
    
    currentRecipe = Recipe.get_recipe_by_id(request.form)

    if not session['user_id'] == currentRecipe['user_id']:
        flash('You cant delete this', 'noAccessError')
        return redirect('/dashboard')
    
    Recipe.update_recipe(request.form)

    return redirect('/')