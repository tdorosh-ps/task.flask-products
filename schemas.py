from flask_marshmallow import Marshmallow

from models import Product, Review


ma = Marshmallow()


class ReviewRetrieveSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Review


class ReviewCreateSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Review
        fields = ('title', 'body')


class ProductSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Product
        fields = ('id', 'asin', 'title')