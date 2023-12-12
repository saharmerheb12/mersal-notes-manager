import os
import sys
import utilities as util
sys.path.append('packages')
from packages import qrcode


video_path = os.environ['VIDEO_PATH']
audio_path = os.environ['AUDIO_PATH']

qr_scale = float(os.environ['QR_SCALE'])

add_logo = os.environ['ADD_LOGO']
logo_path = "./assets/logo.jpg"
logo_scale = float(os.environ['LOGO_SCALE'])

add_envelop = os.environ['ADD_ENVELOP']
envelop_path = "./assets/envelop.png"

def generate(id, extension):
    try:
        if extension == 'mp3':
            path = audio_path
        elif extension == 'mp4':
            path = video_path
        else:
            return False, 'invalid type, supported options are: mp3 or mp4', ''
        
        content = f'{path}?id={id}'
        qr_code_name = f"{id}.png"
        qr_code_path = os.path.join("/tmp", qr_code_name)

        img = qrcode.make(content, border=0)

        img = img.convert('RGB')  # Ensure colors for the output

        if add_logo== 'true':
            logo_img = util.resize(logo_path, img.size[1] * logo_scale)
            img.paste(logo_img, box= ((img.size[0] - logo_img.size[0]) // 2, (img.size[1] - logo_img.size[1]) // 2))

        img.save(qr_code_path)

        if add_envelop == 'true':
            util.overlay_image_on_background(background_path=envelop_path, image_path=qr_code_path, output_path=qr_code_path, position=(0.5,0.1), scale=qr_scale)

    except Exception as e :
        return False, e,''

    return True, qr_code_path, qr_code_name