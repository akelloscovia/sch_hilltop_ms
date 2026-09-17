from flask import Blueprint, request, jsonify, current_app, send_from_directory
from werkzeug.utils import secure_filename
import os
from app import db
from app.models.website import Gallery

website_gallery_bp = Blueprint('website_gallery', __name__)


ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'mp4', 'mov', 'avi', 'mkv'}

GALLERY_CATEGORIES = ['Sports', 'Visitations', 'MDD', 'Campus Updates']
DEFAULT_GALLERY_CATEGORY = 'Campus Updates'


def normalize_category(value):
    if not value:
        return DEFAULT_GALLERY_CATEGORY
    for category in GALLERY_CATEGORIES:
        if category.lower() == value.strip().lower():
            return category
    return DEFAULT_GALLERY_CATEGORY


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def get_upload_folder():
    return current_app.config.get('UPLOAD_FOLDER') or os.path.join(current_app.static_folder, 'uploads', 'gallery')


def get_upload_url(filename):
    return f'/api/v1/gallery/files/{filename}'

# Get available gallery categories
@website_gallery_bp.route('/categories', methods=['GET'], strict_slashes=False)
def get_gallery_categories():
    return jsonify(GALLERY_CATEGORIES)


# Get all gallery items, optionally filtered by category
@website_gallery_bp.route('/', methods=['GET'], strict_slashes=False)
def get_gallery():
   category = request.args.get('category')
   query = Gallery.query
   if category:
       query = query.filter_by(category=normalize_category(category))
   items = query.all()
   return jsonify([item.to_dict() for item in items])

# Upload a new image/video
@website_gallery_bp.route('/', methods=['POST'], strict_slashes=False)
def upload_media():
    files = (
        request.files.getlist('images')
        or request.files.getlist('images[]')
        or request.files.getlist('gallery_images')
        or request.files.getlist('gallery_images[]')
        or request.files.getlist('file')
        or request.files.getlist('files')
        or request.files.getlist('image')
    )
    if not files:
        return jsonify({'error': 'No files provided'}), 400

    category = normalize_category(request.form.get('category'))

    upload_folder = get_upload_folder()
    os.makedirs(upload_folder, exist_ok=True)
    created_items = []

    for file in files:
        if file.filename == '':
            continue
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filepath = os.path.join(upload_folder, filename)
            file.save(filepath)

            media_type = 'video' if filename.rsplit('.', 1)[1].lower() in {'mp4', 'mov', 'avi', 'mkv'} else 'image'
            new_item = Gallery(filename=filename, media_type=media_type, category=category)
            db.session.add(new_item)
            db.session.commit()
            created_items.append(new_item.to_dict())

    if not created_items:
        return jsonify({'error': 'No valid files uploaded'}), 400

    return jsonify(created_items), 201

# Get a single image/video by id

@website_gallery_bp.route('/files/<path:filename>', methods=['GET'], strict_slashes=False)
def serve_gallery_file(filename):
    upload_folder = get_upload_folder()
    return send_from_directory(upload_folder, filename)


@website_gallery_bp.route('/<int:item_id>', methods=['GET'], strict_slashes=False)
def get_media(item_id):
    item = Gallery.query.get_or_404(item_id)
    upload_folder = get_upload_folder()
    return send_from_directory(upload_folder, item.filename)

# Update an item's category
@website_gallery_bp.route('/<int:item_id>', methods=['PUT'])
def update_media_category(item_id):
    item = Gallery.query.get_or_404(item_id)
    data = request.get_json(silent=True) or request.form.to_dict(flat=True)

    if 'category' not in data:
        return jsonify({'error': 'category is required'}), 400

    item.category = normalize_category(data.get('category'))
    db.session.commit()

    return jsonify(item.to_dict())


# Delete an image/video
@website_gallery_bp.route('/<int:item_id>', methods=['DELETE'])
def delete_media(item_id):
    item = Gallery.query.get_or_404(item_id)
    upload_folder = get_upload_folder()

    try:
        os.remove(os.path.join(upload_folder, item.filename))
    except FileNotFoundError:
        pass

    db.session.delete(item)
    db.session.commit()

    return jsonify({'message': 'Item deleted'}), 200
