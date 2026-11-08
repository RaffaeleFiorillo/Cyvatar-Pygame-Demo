from pygame import Surface
from .common import *
import pygame
pygame.display.init()
pygame.font.init()  # Initiate the pygame text fonts


# returns an image ready to be displayed on the screen. "convert_alpha" makes it much faster to display
# it is possible to automatically resize the image using the parameter size=(width, height)
def load_image(directory: str, size=(0, 0), scale=1.0) -> Surface:
    try:
        image = pygame.image.load(f"assets/images/{directory}")
    except FileNotFoundError:
        exit(f"Error: Directory *assets/images/{directory}* Not Found")

    if size != (0, 0):
        return pygame.transform.scale(image, size)
    elif scale != 1.0:
        size = image.get_size()
        return pygame.transform.scale(image, (size[0]*scale, size[1]*scale))
    return image.convert_alpha()



# return a text image that fits into a set size, with some customizations (like color and font size)
def create_sized_text(max_size_image: int, max_size_letter: int, text: str,
                      color: (int, int, int), min_size_letter=30) -> Surface:
    rendered_text = None
    for i in range(min_size_letter, max_size_letter)[::-1]:
        text_font = pygame.font.SysFont('Times New Roman', i)
        text_font.set_bold(True)
        rendered_text = text_font.render(text, True, color)
        if rendered_text.get_size()[0] <= max_size_image:
            break
    return rendered_text.convert_alpha()


# writes the name and password typed by a User in the Create User Menu
def write_name_password(screen: Surface, name: [str], password: [str], active: int, hide: bool) -> None:
    coordinates1 = [(330, 205), (330, 351)]
    pygame.draw.rect(screen, (0, 0, 255), (coordinates1[active], (422, 57)), 8)
    screen.blit(load_image("menu/menu/navigation/pointer.png"),
                (coordinates1[active][0] + 450, coordinates1[active][1]))
    coordinates2 = [(385, 217), (385, 363)]
    if hide:
        password = "".join(["*" for letter in password if str(letter).isalnum()])
    else:
        password = "".join(password)
    name = "".join(name)
    name_text = create_sized_text(330, 32, name, (255, 255, 255), 20)
    password_text = create_sized_text(330, 32, password, (255, 255, 255), 16)
    screen.blit(name_text, coordinates2[0])
    screen.blit(password_text, coordinates2[1])


# Writes the password typed by a User when Insert Password Menu appears (hides it with "*" if the hide variable is True)
def write_password(screen: Surface, password: [str], hide: bool) -> None:
    pygame.font.init()
    if hide:
        password = "".join(["*" for letter in password if str(letter).isalnum()])
    else:
        password = "".join(password)
    text_font = pygame.font.SysFont('Times New Roman', 32)
    text_font.set_bold(True)
    password_text = text_font.render(password, True, (0, 0, 0)).convert_alpha()
    screen.blit(password_text, (290, 330))


# modifies a specific color turning it slightly different from the original
def modify_color(color: (int, int, int)) -> (int, int, int):
    new_color = []
    for i in range(3):
        while True:
            new_tone = color[i] + randint(0, 50) * choice([-1, 1])
            if 0 <= new_tone < 256:
                break
        new_color.append(new_tone)
    return tuple(new_color)


# creates a sample of colors, which are slightly modifications of pre-existing colors
def create_firework_colors(color_number: int) -> [(int, int, int)]:
    base_colors = [(255, 0, 0), (34, 177, 76), (0, 0, 255), (0, 255, 0), (255, 255, 0), (0, 255, 255), (255, 0, 255),
                   (255, 90, 0), (130, 0, 255)]
    return [modify_color(choice(base_colors)) for _ in range(color_number)]


# returns x and y values for a square like firework
def calculate_rs_rhomb(x: int, y: int, radius: int) -> (int, int):
    if random() > 0.5:
        additional = randint(0, int(radius)) * choice([-1, 1])
        r_x = x + additional
        max_y_size = int(radius - abs(additional))
        r_y = y + randint(0, max_y_size) * choice([-1, 1])
    else:
        additional = randint(0, int(radius)) * choice([-1, 1])
        r_y = y + additional
        max_x_size = int(radius - abs(additional))
        r_x = x + randint(0, max_x_size) * choice([-1, 1])
    return r_x, r_y


# returns x and y values for a square like firework
def calculate_rs_square(x: int, y: int, radius: int) -> (int, int):
    r_x = x + randint(0, int(radius - radius * 0.3)) * choice([-1, 1])
    r_y = y + randint(0, int(radius - radius * 0.3)) * choice([-1, 1])
    return r_x, r_y


# returns x and y values for a circle like firework
def calculate_rs_circle(x: int, y: int, radius: int) -> (int, int):
    # condition for a point to be inside a circle: (x - center_x)**2 + (y - center_y)**2 < radius**2
    if random() > 0.5:
        r_x = x + randint(0, int(radius)) * choice([-1, 1])
        r_y = y + randint(0, int(abs(((r_x - x) ** 2 - radius ** 2) ** (1 / 2)))) * choice([-1, 1])
    else:
        r_y = y + randint(0, int(radius)) * choice([-1, 1])
        r_x = x + randint(0, int(abs(((r_y - y) ** 2 - radius ** 2) ** (1 / 2)))) * choice([-1, 1])
    return r_x, r_y
