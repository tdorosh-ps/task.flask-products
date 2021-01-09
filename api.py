from flask import Blueprint, request, jsonify

from models import db, Product, Review
from schemas import ReviewRetrieveSchema, ReviewCreateSchema, ProductSchema
from caches import cache


api = Blueprint('api', __name__)


@api.route('/product/<int:prod_id>/', methods=['GET'])
@cache.cached(timeout=30)
def get_product(prod_id):
    product = Product.query.get_or_404(prod_id)
    page = int(request.args.get('page', 1))
    per_page = int(request.args.get('per_page', 1))
    reviews = product.reviews.paginate(page=page, per_page=per_page)
    product_schema = ProductSchema()
    review_schema = ReviewRetrieveSchema()
    data = {
        'product': product_schema.jsonify(product).json,
        'reviews': review_schema.jsonify(reviews.items, many=True).json,
        'page': reviews.page,
        'per_page': reviews.per_page,
        'total': reviews.total,
        'total_pages': reviews.pages
    }
    return jsonify(data), 200


@api.route('/product/<int:prod_id>/add_review/', methods=['PUT'])
def add_review(prod_id):
    product = Product.query.get_or_404(prod_id)
    request_data = request.get_json()
    if not request_data:
        return jsonify({'message': 'Invalid request'}), 400
    if not request_data.get('title') and not request_data.get('body'):
        return jsonify({'message': 'Title and body must be passed'}), 400
    schema = ReviewCreateSchema()
    errors = schema.validate(request_data)
    if errors:
        return jsonify(errors), 400
    review_data = schema.load(request_data)
    review = Review(product_id=product.id, asin=product.asin,
                    title=review_data['title'], body=review_data['body'], )
    product.reviews.append(review)
    db.session.add(product)
    db.session.commit()
    return jsonify(message='New review was added successfully'), 200


