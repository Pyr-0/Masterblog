from flask import Flask, render_template, request, redirect, url_for
from werkzeug.wrappers import Response
import json
from typing import Union

app = Flask(__name__)


def load_posts() -> list:
	"""
	Load blog posts from the JSON file.
	
	Returns:
		list: A list of dictionaries containing blog post data.
		Each dictionary has the following keys:
		- id (int): Unique identifier for the post
		- author (str): Name of the post author
		- title (str): Title of the post
		- content (str): Content of the post
		- likes (int): Number of likes for the post
	"""
	with open('blog_posts.json', 'r') as file:
		return json.load(file)


def save_posts(posts: list) -> None:
	"""
	Save blog posts to the JSON file.
	
	Args:
		posts (list): A list of dictionaries containing blog post data
	"""
	with open('blog_posts.json', 'w') as file:
		json.dump(posts, file, indent=4)


@app.route('/')
def index() -> str:
	"""
	Render the home page with all blog posts.
	
	Returns:
		str: Rendered HTML template with all blog posts
	"""
	blog_posts = load_posts()
	return render_template('index.html', posts=blog_posts)


@app.route('/add', methods=['GET', 'POST'])
def add() -> Union[str, Response]:
	"""
	Handle the addition of new blog posts.
	
	GET request: Display the form to add a new post
	POST request: Process the form data and create a new post
	
	Returns:
		Union[str, Response]: On GET - Rendered HTML template with the add form
							On POST - Redirect to the index page after adding the post
	"""
	if request.method == 'POST':
		blog_posts = load_posts()
		
		# Generate a new unique ID (max existing ID + 1)
		new_id = max(post['id'] for post in blog_posts) + 1 if blog_posts else 1
		
		# Create new blog post
		new_post = {
			'id': new_id,
			'author': request.form.get('author'),
			'title': request.form.get('title'),
			'content': request.form.get('content'),
			'likes': 0  # Initialize likes to 0
		}
		
		# Add new post to the list
		blog_posts.append(new_post)
		save_posts(blog_posts)
		
		return redirect(url_for('index'))
	
	return render_template('add.html')


@app.route('/update/<int:post_id>', methods=['GET', 'POST'])
def update(post_id: int) -> Union[str, Response, tuple[str, int]]:
	"""
	Handle the updating of existing blog posts.
	
	Args:
		post_id (int): The ID of the post to update
	
	GET request: Display the form with current post data
	POST request: Process the form data and update the post
	
	Returns:
		Union[str, Response, tuple[str, int]]: 
			On GET - Rendered HTML template with the update form
			On POST - Redirect to the index page after updating
			On post not found - 404 error message with status code
	"""
	blog_posts = load_posts()
	post = next((post for post in blog_posts if post['id'] == post_id), None)
	
	if post is None:
		return "Post not found", 404
	
	if request.method == 'POST':
		# Update the post
		post['author'] = request.form.get('author')
		post['title'] = request.form.get('title')
		post['content'] = request.form.get('content')
		save_posts(blog_posts)
		return redirect(url_for('index'))
	
	return render_template('update.html', post=post)


@app.route('/delete/<int:post_id>')
def delete(post_id: int) -> Response:
	"""
	Delete a blog post.
	
	Args:
		post_id (int): The ID of the post to delete
	
	Returns:
		Response: Redirect to the index page after deletion
	"""
	blog_posts = load_posts()
	blog_posts = [post for post in blog_posts if post['id'] != post_id]
	save_posts(blog_posts)
	return redirect(url_for('index'))


@app.route('/like/<int:post_id>')
def like(post_id: int) -> Response:
	"""
	Increment the like count for a blog post.
	
	Args:
		post_id (int): The ID of the post to like
	
	Returns:
		Response: Redirect to the index page after incrementing likes
	"""
	blog_posts = load_posts()
	post = next((post for post in blog_posts if post['id'] == post_id), None)
	
	if post is not None:
		# Initialize likes if it doesn't exist
		if 'likes' not in post:
			post['likes'] = 0
		post['likes'] += 1
		save_posts(blog_posts)
	
	return redirect(url_for('index'))


if __name__ == '__main__':
	app.run(host="0.0.0.0", port=5000, debug=True)