from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates
db = SQLAlchemy()

class Author(db.Model):
    __tablename__ = 'authors'
    
    id = db.Column(db.Integer, primary_key=True)
    name= db.Column(db.String, unique=True, nullable=False)
    phone_number = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    # Add validators 
    @validates("name")
    def validate_name(self, key, value):
        if len(value) == 0:
            raise ValueError("Name cannot be empty")
        elif self.query.filter_by(name=value).first() is not None:
            raise ValueError("Name already exists")
        return value
    
    @validates("phone_number")
    def validate_number(self, key, value):
        print(f"Validating phone number: {value}, Type: {type(value)}")
        if len(value) != 10 or not value.isdigit():
            raise ValueError("Phone number must be 10 digits")
        return value
        

    def __repr__(self):
        return f'Author(id={self.id}, name={self.name})'

class Post(db.Model):
    __tablename__ = 'posts'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    content = db.Column(db.String)
    category = db.Column(db.String)
    summary = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    # Add validators  
    @validates("content")
    def content_validator(self, key, value):
        if len(value) < 250:
            raise ValueError("Post Content must be at least 250 characters long")
        return value
    
    @validates("summary")
    def summary_validator(self, key, value):
        if len(value) > 250:
            raise ValueError("Summary must be a maximum of 250 characters long")
        return value
        
    @validates("category")
    def category_validator(self, key, value):
        if value == "Fiction" or value == "Non-Fiction":
            return value
        else:
            raise ValueError("Category must be either Fiction or Non-Fiction")
    
    @validates("title")
    def title_validator(self, key, value):
        key_words = ["Won't Believe", "Secret", "Top", "Guess"]
        for word in key_words:
            if word in value:
                return value
        raise ValueError("Post Title should contain one of these: Won't Believe, Secret, Top or Guess")

            


    def __repr__(self):
        return f'Post(id={self.id}, title={self.title} content={self.content}, summary={self.summary})'
