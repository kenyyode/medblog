from medblog import db, app
from slugify import slugify
from sqlalchemy.orm import relationship


class blog(db.Model):
    post_id = db.Column(db.Integer(), primary_key=True)
    body = db.Column(db.Text(), nullable=False)
    head = db.Column(db.String(), nullable=False)
    date_created = db.Column(db.DateTime(), nullable=False, default=db.func.current_timestamp())
    slug = db.Column(db.String(100), nullable=False, unique=True)
    user_id = db.Column(db.Integer(), nullable=False)
    liked_by_user_ids = db.Column(db.String(255))
   
    ##relationships
    comments = relationship ('Comment', backref='blog', lazy=True)
    likes = relationship ('Like', backref='blog', lazy=True)
    #likes = relationship("Postlike", backref="blog", lazy=True)

    def generate_slug(self):
        return slugify(self.head)  # Generate the slug from the title

    def save(self):
        # Generate and set the slug
        self.slug = self.generate_slug()
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()


    def serialize(self):
        return {
        'id': self.post_id,
        'title': self.head,
        'content': self.body}


    def __repr__(self):
        return f'<Blog {self.id}: {self.head}>'

class Comment(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    text = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer(), nullable=False)
    blog_id = db.Column(db.Integer(), db.ForeignKey("blog.post_id"), nullable=False)  

    def save(self): 
        db.session.add(self) 
        db.session.commit()
    
    def serialize(self):
        return {
            "id":self.id,
            "text": self.text,
            "user_id": self.user_id
        }
    def __repr__(self):
        return f'<Comment {self.id}: {self.text}'

class Like(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    likes = db.Column(db.Integer(), nullable=False)
    user_id = db.Column(db.Integer(), nullable=False)
    blog_id = db.Column(db.Integer(), db.ForeignKey("blog.post_id"), nullable=False)  

    def save(self): 
        db.session.add(self) 
        db.session.commit()
    
    def serialize(self):
        return {
            "id":self.id,
            "likes": self.likes,
            "user_id": self.user_id
        }
    def __repr__(self):
        return f'<Like {self.id}: {self.likes}'

