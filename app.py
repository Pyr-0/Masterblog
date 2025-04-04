from flask import Flask, render_template, request, redirect, url_for
import json

app = Flask(__name__)


@app.route('/')
def index():
	# Read blog posts from the JSON file
	with open('blog_posts.json', 'r') as file:
		blog_posts = json.load(file)
	return render_template('index.html', posts=blog_posts)


@app.route('/add', methods=['GET', 'POST'])
def add():
	if request.method == 'POST':
		# Read existing blog posts
		with open('blog_posts.json', 'r') as file:
			blog_posts = json.load(file)
		
		# Generate a new unique ID (max existing ID + 1)
		new_id = max(post['id'] for post in blog_posts) + 1 if blog_posts else 1
		
		# Create new blog post
		new_post = {
			'id': new_id,
			'author': request.form.get('author'),
			'title': request.form.get('title'),
			'content': request.form.get('content')
		}
		
		# Add new post to the list
		blog_posts.append(new_post)
		
		# Save updated blog posts back to the JSON file
		with open('blog_posts.json', 'w') as file:
			json.dump(blog_posts, file, indent=4)
		
		return redirect(url_for('index'))
		
	return render_template('add.html')


if __name__ == '__main__':
	app.run(host="0.0.0.0", port=5000, debug=True)