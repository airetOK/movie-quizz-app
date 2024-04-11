class Movie():

    def __init__(self, id, title) -> None:
        self.id = id
        self.title = title
        self.image_url = None

    def get_id(self):
        return self.id
    
    def get_title(self):
        return self.title

    def set_image_url(self, image_url):
        self.image_url = image_url

    def get_image_url(self):
        return self.image_url