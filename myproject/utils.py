def validate_product_data(data):
    errors = []
    if not data.get('name'):
        errors.append("Product name is required.")
    if not data.get('price') or int(data.get('price')) <= 0:
        errors.append("Price must be a positive number.")
    if not data.get('description'):
        errors.append("Description is required.")
    return errors