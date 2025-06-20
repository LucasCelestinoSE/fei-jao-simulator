import os
import random
import cv2
template_dir = "storage/templates/awnser"
saurce_dir = "storage/saurces"
folder_destiny = "storage/results/"
def file_counter(path):
    print(os.listdir(path))

#file_counter("storage/templates/awnser")
#file_counter("storage/saurces")
numero_aleatorio = random.random()



def get_random_file(path):
    list_files = os.listdir(path)
    random_element = random.choice(list_files)
    complete_path = path + "/" + random_element
    return complete_path

def get_original_name(template_str,source_str):
    return template_str+source_str

def read_image(img_str):
    image = cv2.imread(img_str)
    if image is None:
        raise ValueError("Erro ao carregar a imagem.")
    return image

def toGrayScale(image):
    return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

def threshold_image(imagem):
    _, imagem_limiarizada = cv2.threshold(imagem, 10, 255, cv2.THRESH_BINARY_INV)
    return imagem_limiarizada
def save_image(image, folder_destiny, name):
    folder_destiny = folder_destiny + name
    cv2.imwrite(folder_destiny, image)
    print(f"Imagem salva como {folder_destiny}")
def find_largest_contour_position(imagem_binarizada):
   
    contornos, _ = cv2.findContours(imagem_binarizada, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    largest_contour = None
    max_area = 0

    for contour in contornos:
        area = cv2.contourArea(contour)

        if area > 100:
            if area > max_area:
                max_area = area
                largest_contour = contour
    
    if largest_contour is not None:
        x, y, w, h = cv2.boundingRect(largest_contour)
        return (x, y, w, h)
    else:
        return None
    


def generate_meme(template: str, source: str) -> None:
    """Gera um meme combinando um template e uma imagem de origem."""
    print(f"Template path: {template}")

    # Carregar a imagem do template
    template_base = read_image(template)
    if template_base is None:
        print(f"Erro ao carregar o template: {template}")
        return

    template_gray = toGrayScale(template_base)
    template_bin = threshold_image(template_gray)
    source_bin = read_image(source)

    pos = find_largest_contour_position(template_bin)
    if pos:
        x, y, w, h = pos
        print(f"Contorno encontrado em: x={x}, y={y}, w={w}, h={h}")

        # Redimensionar a imagem de origem para o tamanho correto
        source_bin = cv2.resize(source_bin, (w, h))

        # Inserir a imagem de origem no template
        template_base[y:y+h, x:x+w] = source_bin

        # Salvar a imagem resultante
        save_image(template_base, folder_destiny, "meme_gerado.jpg")
    else:
        print("Nenhum contorno encontrado no template.")













saurce_file = get_random_file(saurce_dir)
template_file = get_random_file(template_dir)
generate_meme(template_file, saurce_file)

