import argparse
import os
import cv2
from colorama import Fore, Style
import sys



def style_text(level: str, inp_text: str, *format_args) -> str:
    repl = {
        "{": f"{Fore.GREEN}" + "{",
        "}": "}" + f"{Fore.BLUE}",
    }


    level_repl = {
        "Info": Fore.WHITE,
        "ERROR": Fore.RED,
        "DEBUG": Fore.GREEN,
        "CRITICAL": Fore.RED,
        "WARNING": Fore.RED
    }

    if level not in level_repl:
        return style_text("CRITICAL", "Invalid level, All levels list: {}", ", ".join(ele for ele in level_repl))
    


    text = f"{level_repl[level]}[{level + "]":<10}{Fore.BLUE}  "
    text += "".join(ele if ele not in repl else repl[ele] for ele in inp_text)
    text += f"{Style.RESET_ALL}"
    return text.format(*format_args)


def parse_arguments():
    parser = argparse.ArgumentParser(description="This program helps to change Format and Size of the image")
    
    parser.add_argument('--input', type=str, required=True, help='Path to the input file')
    parser.add_argument('--output', type=str, help='Path to the output file')
    parser.add_argument('--width', type=int, help='Define output image width')
    parser.add_argument('--height', type=int, help='Define output image height')
    parser.add_argument("--over_write", type=int, default=0, help="""
Define should program over write the file if the file with same name as output path exists (1/0)
""")
    parser.add_argument("--show", type=int, default=0, help="Show image after changes (1/0)")
    
    args = parser.parse_args()
    return args


def check_image_file(filepath):
    image_extensions = {'.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff', '.webp'}
    _, ext = os.path.splitext(filepath)

    if ext.lower() not in image_extensions:
        print(style_text("Error", "Unexpectable file format, {}", ext))
        print(style_text("Error", "Enter files with extentions: {}", ", ".join(ele for ele in image_extensions)))
        sys.exit()
    

def clear_args(args):
    input_path = args.input
    output_path = args.output
    
    if (over_write := args.over_write) not in (1, 0):
        print(style_text("Error", "{} argument should contain only {}({}) or {}({})", "--over_write", 1, "yes", 0, "no"))
        sys.exit()

    if (show := args.show) not in (1, 0):
        print(style_text("Error", "{} argument should contain only {}({}) or {}({})", "--show", 1, "yes", 0, "no"))
        sys.exit()

    if output_path is None:
        output_path = input_path

    if not os.path.exists(input_path):
        print(style_text("Error", "File {} does not exists", input_path))
        sys.exit()

    check_image_file(filepath=input_path)

    img = cv2.imread(input_path)

    input_size = args.width, args.height
    overall_size = tuple(s[0] if s[0] is not None else s[1] for s in zip(input_size, img.shape[:2][::-1]))
    return img, output_path, overall_size, over_write, show


def save(over_write, img, output_path):
    if over_write == 1:
        cv2.imwrite(output_path, img)
    
    elif over_write == 0:
        
        if os.path.exists(output_path):
            print(style_text("Info", "File was never saved, file on path {} is exists", output_path))
            print(style_text("Info", "You can insert {} to {}", "--over_write", "Over write"))
        else:
            cv2.imwrite(output_path, img)


def show_image(output_path, img, show):
    if show == 1:
        print(style_text("Info", "Press {} to close the window", "{q}"))

        while 1:
            cv2.imshow(output_path, img)
            if cv2.waitKey(1) & 0xFF == ord("q"):
                cv2.destroyAllWindows()
                break


def main():
    args = parse_arguments()

    img, output_path, overall_size, over_write, show = clear_args(args)
    img = cv2.resize(img, overall_size)
    
    save(over_write, img, output_path)
    show_image(output_path, img, show)


if __name__ == "__main__":
    main()
