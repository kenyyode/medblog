from medblog import db, app
from slugify import slugify
from sqlalchemy.orm import relationship

class blog(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    body = db.Column(db.Text(), nullable=False)
    Head = db.Column(db.String(), nullable=False)
    date_created = db.Column(db.DateTime(), nullable=False, default=db.func.current_timestamp())
    slug = db.Column(db.String(100), nullable=False, unique=True)
    comments = relationship ('Comment', backref='blog', lazy=True)

    def generate_slug(self):
        return slugify(self.Head)  # Generate the slug from the title

    def save(self):
        # Generate and set the slug
        self.slug = self.generate_slug()
        db.session.add(self)
        db.session.commit()

    def __repr__(self):
        return f'<Blog {self.id}: {self.Head}>'

class Comment(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    text = db.Column(db.Text, nullable=True)
    blog_id = db.Column(db.Integer(), db.ForeignKey("blog.id"), nullable=True)