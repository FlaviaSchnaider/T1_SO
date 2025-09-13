import os
import sys
import struct

def ensure_fifo(path):
    try:
        os.mkfifo(path)
    except FileExistsError:
        pass

def load_as_pgm_bytes(img_path):
    """
    Retorna (w, h, maxv=255, bytes) independente de ser PNG/JPG/PGM.
    Se for PNG/JPG, converte para 'L' (8-bit grayscale).
    """
    ext = os.path.splitext(img_path)[1].lower()
    if ext == ".pgm":
        with open(img_path, "rb") as f:
            if f.readline().strip() != b'P5':
                raise ValueError("PGM não está no modo binário P5")
            line = f.readline() # pula comentários
            while line.startswith(b'#'):
                line = f.readline()
            w, h = map(int, line.split())
            maxv = int(f.readline())
            data = bytearray(f.read())
            if len(data) != w*h:
                raise ValueError("Tamanho do payload PGM inconsistente")
            if maxv != 255:
                data = bytearray(int(px * 255 / maxv) for px in data)
                maxv = 255
            return w, h, maxv, data
    else:
        try:
            from PIL import Image
        except ImportError:
            sys.exit(1)
        im = Image.open(img_path).convert("L")  
        w, h = im.size
        data = bytearray(im.tobytes())
        return w, h, 255, data

def main():
    if len(sys.argv) != 3:
        print(f"Uso: {sys.argv[0]} <fifo_path> <entrada.(png|jpg|pgm)>")
        sys.exit(1)

    fifo = sys.argv[1]
    inpath = sys.argv[2]

    ensure_fifo(fifo)

    w, h, maxv, data = load_as_pgm_bytes(inpath)

    with open(fifo, "wb") as f:
        header = struct.pack("iii", w, h, maxv)
        f.write(header)
        f.write(data)

    print(f"[Sender] {inpath} ({w}x{h}) enviado com sucesso.")

if __name__ == "__main__":
    main()
