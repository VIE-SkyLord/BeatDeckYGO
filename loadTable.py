import os
import urllib.parse

# Đường dẫn tới thư mục chứa hình ảnh chính và ảnh pop-up
image_directory = "imageDecks"
popup_image_directory = "imagePopups"

# Kiểm tra xem thư mục có tồn tại và có hình ảnh không
if not os.path.exists(image_directory):
    print(f"Thư mục '{image_directory}' không tồn tại.")
elif not os.path.exists(popup_image_directory):
    print(f"Thư mục '{popup_image_directory}' không tồn tại.")
else:
    images = os.listdir(image_directory)
    popup_images = os.listdir(popup_image_directory)
    
    if not images:
        print(f"Không có hình ảnh nào trong thư mục '{image_directory}'.")
    elif not popup_images:
        print(f"Không có hình ảnh nào trong thư mục '{popup_image_directory}'.")
    else:
        
        # Mở file HTML để ghi với mã hóa utf-8
        with open("gallery.html", "w", encoding='utf-8') as f:
            # Bắt đầu viết HTML
            f.write("""<!DOCTYPE html>
            <html lang="en">
            <head>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <title>Image Gallery</title>
                <style>
                    body {
                        margin: 0;
                        display: flex;
                        justify-content: center;
                    }
                    .gallery-container {
                        display: grid;
                        grid-template-columns: repeat(auto-fit, minmax(100px, 1fr));
                        gap: 10px;
                        width: 100%;
                        max-width: 1200px;
                        padding: 10px;
                    }
                    .gallery-item {
                        position: relative;
                        border: 1px solid #ccc;
                        overflow: hidden;
                        text-align: center;
                        cursor: pointer;
                    }
                    .gallery-item img {
                        width: 100%;
                        height: auto;
                        display: block;
                    }
                    .popup {
                        display: none;
                        position: fixed;
                        top: 50%;
                        left: 50%;
                        transform: translate(-50%, -50%);
                        background-color: rgba(255, 255, 255, 0.8);
                        border: 2px solid #000;
                        padding: 20px;
                        z-index: 10;
                        width: 80vw;
                        max-height: 90vh;
                        overflow: auto;
                        box-shadow: 0px 4px 8px rgba(0, 0, 0, 0.2);
                    }
                    .gallery-item.active .popup {
                        display: block;
                    }
                    .no-popup-message {
                        color: red;
                        font-weight: bold;
                    }
                    @media (max-width: 600px) {
                        .popup {
                            width: 90vw;
                            max-height: 80vh;
                        }
                    }
                    @media (min-width: 1200px) {
                        .gallery-container {
                            grid-template-columns: repeat(10, 1fr);
                        }
                    }
                </style>
            </head>
            <body>
                <div class="gallery-container">
            """)

            for image in images:
                # Kiểm tra định dạng ảnh
                if image.endswith(('.png', '.jpg', '.jpeg', '.gif', '.webp')):
                    # Mã hóa URL cho hình ảnh
                    encoded_image = urllib.parse.quote(image)
                    # Thay đổi đường dẫn hình ảnh
                    image_path = f"{image_directory}/{encoded_image}"
                    print(f"Đang xử lý ảnh: {image}")

                    # Lấy tên cơ bản của ảnh (không bao gồm phần mở rộng)
                    image_name = os.path.splitext(image)[0]

                    # Tìm ảnh pop-up tương ứng trong thư mục pop-up
                    popup_image = None
                    for ext in ['.png', '.jpg', '.jpeg', '.gif', '.webp']:
                        popup_image_name = f"{image_name}{ext}"
                        if popup_image_name in popup_images:
                            popup_image = urllib.parse.quote(popup_image_name)
                            break

                    # Nếu tìm thấy ảnh pop-up
                    if popup_image:
                        popup_image_path = f"{popup_image_directory}/{popup_image}"
                        f.write(f"""
                            <div class="gallery-item" onclick="togglePopup(this)">
                                <img src="{image_path}" alt="{image}">
                                <p>{image_name}</p>
                                <div class="popup">
                                    <img src="{popup_image_path}" alt="{popup_image}" style="width: 100%; height: auto;">
                                    <p>{image_name}</p>
                                </div>
                            </div>
                        """)
                    else:
                        # Nếu không có ảnh pop-up tương ứng, hiển thị thông báo
                        f.write(f"""
                            <div class="gallery-item" onclick="togglePopup(this)">
                                <img src="{image_path}" alt="{image}">
                                <p>{image_name}</p>
                                <div class="popup">
                                    <p class="no-popup-message">Không có pop-up cho ảnh này</p>
                                </div>
                            </div>
                        """)

            # Kết thúc file HTML
            f.write(""" 
                </div>
                <script>
                    function togglePopup(item) {
                        const popup = item.querySelector('.popup');
                        const isActive = item.classList.toggle('active');
                        if (!isActive) {
                            popup.style.display = 'none';
                        } else {
                            popup.style.display = 'block';
                        }
                    }
                    document.addEventListener('click', function(e) {
                        if (!e.target.closest('.gallery-item')) {
                            const items = document.querySelectorAll('.gallery-item');
                            items.forEach(item => {
                                item.classList.remove('active');
                                item.querySelector('.popup').style.display = 'none';
                            });
                        }
                    });
                </script>
            </body>
            </html>
            """)
