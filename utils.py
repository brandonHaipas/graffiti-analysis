import requests

def save_img(pic_url, img_name):
    try:
        response = requests.get(pic_url, stream=True)
        if not response.ok:
            print("Failed to download image:", response.status_code)
            return response.status_code

        with open(img_name, 'wb') as handle:
            for block in response.iter_content(1024):
                if not block:
                    break
                handle.write(block)

        print("Image saved successfully as", img_name)
    except Exception as e:
        print(f"The error {str(e)} ocurred while saving the image")
        return 600
    return response.status_code