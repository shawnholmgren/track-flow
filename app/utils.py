def remove_images(data):
    if isinstance(data, dict):
        if 'images' in data:
            del data['images']
        if 'external_urls' in data:
            del data['external_urls']
        if 'href' in data:
            del data['href']
        if 'genres' in data:
            del data['genres']
        if 'followers' in data:
            del data['followers']
        if 'uri' in data:
            del data['uri']
        for key in data:
            remove_images(data[key])
    elif isinstance(data, list):
        for item in data:
            remove_images(item)
    return data

