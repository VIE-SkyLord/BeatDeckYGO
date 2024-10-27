from flask import Flask, render_template
import os
import urllib.parse

app = Flask(__name__)

def load_images():
    # Đường dẫn tới thư mục chứa hình ảnh chính và ảnh pop-up
    image_directory = "imageDecks"
    popup_image_directory = "imagePopups"

    # Kiểm tra xem thư mục có tồn tại và có hình ảnh không
    if not os.path.exists(image_directory):
        print(f"Thư mục '{image_directory}' không tồn tại.")
        return [], []
    elif not os.path.exists(popup_image_directory):
        print(f"Thư mục '{popup_image_directory}' không tồn tại.")
        return [], []
    
    images = os.listdir(image_directory)
    popup_images = os.listdir(popup_image_directory)

    return images, popup_images

@app.route('/')
def index():
    images, popup_images = load_images()
    return render_template('gallery.html', images=images, popup_images=popup_images)

if __name__ == '__main__':
    app.run(debug=True)
