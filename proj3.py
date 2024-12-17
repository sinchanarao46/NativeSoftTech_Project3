from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Configure MySQL Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://username:password@localhost/blog_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Define the Blog Post Model
class BlogPost(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)

    def to_dict(self):
        return {"id": self.id, "title": self.title, "content": self.content}

# Create Database Tables
with app.app_context():
    db.create_all()

# API Endpoints

# Create a new blog post
@app.route('/posts', methods=['POST'])
def create_post():
    data = request.json
    new_post = BlogPost(title=data['title'], content=data['content'])
    db.session.add(new_post)
    db.session.commit()
    return jsonify({"message": "Blog post created", "post": new_post.to_dict()}), 201

# Retrieve all blog posts
@app.route('/posts', methods=['GET'])
def get_posts():
    posts = BlogPost.query.all()
    return jsonify([post.to_dict() for post in posts])

# Retrieve a single blog post by ID
@app.route('/posts/<int:id>', methods=['GET'])
def get_post(id):
    post = BlogPost.query.get_or_404(id)
    return jsonify(post.to_dict())

# Update a blog post
@app.route('/posts/<int:id>', methods=['PUT'])
def update_post(id):
    post = BlogPost.query.get_or_404(id)
    data = request.json
    post.title = data['title']
    post.content = data['content']
    db.session.commit()
    return jsonify({"message": "Blog post updated", "post": post.to_dict()})

# Delete a blog post
@app.route('/posts/<int:id>', methods=['DELETE'])
def delete_post(id):
    post = BlogPost.query.get_or_404(id)
    db.session.delete(post)
    db.session.commit()
    return jsonify({"message": "Blog post deleted"})

if __name__ == '__main__':
    app.run(debug=True)
