from medblog import db, app
from slugify import slugify
from sqlalchemy.orm import relationship

class blog(db.Model):
    post_id = db.Column(db.Integer(), primary_key=True)
    body = db.Column(db.Text(), nullable=False)
    Head = db.Column(db.String(), nullable=False)
    date_created = db.Column(db.DateTime(), nullable=False, default=db.func.current_timestamp())
    slug = db.Column(db.String(100), nullable=False, unique=True)
    comments = relationship ('Comment', backref='blog', lazy=True)
    user_id = db.Column(db.Integer(), nullable=False)
    liked_by_user_ids = db.Column(db.String(255))

    def generate_slug(self):
        return slugify(self.Head)  # Generate the slug from the title

    def save(self):
        # Generate and set the slug
        self.slug = self.generate_slug()
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def like_post(self, user_id):
        # Check if user_id is not already in the liked_by_user_ids
        if str(user_id) not in self.liked_by_user_ids.split(','):
            self.liked_by_user_ids = f"{self.liked_by_user_ids},{user_id}"
            db.session.commit()

    def unlike_post(self, user_id):
        # Check if user_id is in the liked_by_user_ids
        user_id_str = str(user_id)
        if user_id_str in self.liked_by_user_ids.split(','):
            liked_users = self.liked_by_user_ids.split(',')
            liked_users.remove(user_id_str)
            self.liked_by_user_ids = ','.join(liked_users)
            db.session.commit()

    def __repr__(self):
        return f'<Blog {self.id}: {self.head}>'

class Comment(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    text = db.Column(db.Text, nullable=True)
    blog_id = db.Column(db.Integer(), db.ForeignKey("blog.post_id"), nullable=True)    
