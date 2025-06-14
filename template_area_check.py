import cv2


def read_image(img_str):
    imagem = cv2.imread(img_str)
    if imagem is None:
        raise ValueError("Erro ao carregar a imagem.")
    return imagem
def toGrayScale(imagem):
    return cv2.cvtColor(imagem, cv2.COLOR_BGR2GRAY)
def save_image(imagem, filename):
    cv2.imwrite(filename, imagem)
    print(f"Imagem salva como {filename}")
def threshold_image(imagem):
    _, imagem_limiarizada = cv2.threshold(imagem, 10, 255, cv2.THRESH_BINARY_INV)
    return imagem_limiarizada
def create_image_contours(imagem):
    contornos, hierarquia = cv2.findContours(imagem, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    imagem_com_contornos = cv2.cvtColor(imagem, cv2.COLOR_GRAY2BGR)
    cv2.drawContours(imagem_com_contornos, contornos, -1, (0, 255, 0), 2)
    return imagem_com_contornos

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
def inserir_imagem(imagem_base_path, imagem_inserida_path, x, y, largura, altura):
    """
    Insere uma imagem em uma posição específica dentro de outra imagem.

    :param imagem_base_path: Caminho para a imagem base.
    :param imagem_inserida_path: Caminho para a imagem que será inserida.
    :param x: Coordenada X (canto superior esquerdo) onde a imagem será inserida.
    :param y: Coordenada Y (canto superior esquerdo) onde a imagem será inserida.
    :param largura: Largura da imagem a ser inserida.
    :param altura: Altura da imagem a ser inserida.
    """
    imagem_base = cv2.imread(imagem_base_path)

    imagem_inserida = cv2.imread(imagem_inserida_path)

    # Verificar se as imagens foram carregadas corretamente
    if imagem_base is None or imagem_inserida is None:
        print("Erro ao carregar as imagens. Verifique os caminhos.")
        return

    # Redimensionar a imagem a ser inserida
    imagem_inserida = cv2.resize(imagem_inserida, (largura, altura))

    # Inserir a imagem na posição especificada
    imagem_base[y:y+altura, x:x+largura] = imagem_inserida

    

    # Opcional: Salvar a imagem resultante
    img = cv2.imwrite('imagem_resultante.jpg', imagem_base)
    return img

imagem_base = read_image('3.jpg')
imagemCol  = toGrayScale(imagem_base)
imagemCol = threshold_image(imagemCol)
pos = find_largest_contour_position(imagemCol)

if pos:
    x, y, w, h = pos
    print(f"Maior área de contorno encontrada em: x={x}, y={y}, largura={w}, altura={h}")
    insertimg = inserir_imagem("3.jpg","image.png",x,y,w,h)

# save_image(insertimg,"grayScale4.jpg")