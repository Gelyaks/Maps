import requests
import os
import sys
import pygame
from geocoder import get_coordinates

print('' + '\n' + 'Добро пожаловать в MapsOnPy!')

while True:
    read = input('' + '\n' + 'Пожалуйста, выберите режим работы:' + '\n' + 'Введите 1, если хотите изменять масштаб '
                 'клавишами PageUP и PageDOWN' + '\n' +
                 'Введите 2, если хотите изменять масштаб клавишами ПЛЮС и МИНУС' + '\n' +
                 'Ваш режим: ')
    if read == '1' or read == '2':
        break
    else:
        print('' + '\n' + 'Не понимаем ваш запрос, пожалуйста, повторите:')

if read == '1':
    c = input('' + '\n' + '' + '\n' + '' + 'Горячие клавиши:' + '\n' +
              'PageUP и PageDOWN - изменить масштаб' + '\n' + 'TAB - изменить тип карты' + '\n' +
              'Стрелки - перемещение на карте\n' +
              'Для поиска объекта введите его нaзвание в поле и нажмите ENTER' +
              '\nЧтобы сбросить метку, нажмите СБРОС' +
              '\n' + '' + '\n' + 'Пример ввода: 53.5099, 49.4188' + '\n' + '' + '\n' +
              'Введите свои координаты: ').split(', ')
else:
    c = input('' + '\n' + '' + '\n' + '' + 'Горячие клавиши:' + '\n' +
              'ПЛЮС и МИНУС - изменить масштаб' + '\n' + 'TAB - изменить тип карты' + '\n' +
              'Стрелки - перемещение на карте' +
              'Для поиска объекта введите его нaзвание в поле и нажмите ENTER\n' +
              'Чтобы сбросить метку, нажмите СБРОС' +
              '\n' + '' + '\n' + 'Пример ввода: 53.5099, 49.4188' + '\n' + '' + '\n' +
              'Введите свои координаты: ').split(', ')

c_flag = c[:]


class Button:
    def __init__(self, text, x=0, y=0, width=30, height=30):
        self.text = text
        self.image_normal = pygame.Surface((width, height))
        self.image_normal.fill((255, 180, 51))
        self.image_hovered = pygame.Surface((width, height))
        self.image_hovered.fill('grey')
        self.image = self.image_normal
        self.rect = self.image.get_rect()

        font = pygame.font.SysFont('Arial', 20)

        text_image = font.render(text, True, 'black')
        text_rect = text_image.get_rect(center=self.rect.center)

        self.image_normal.blit(text_image, text_rect)
        self.image_hovered.blit(text_image, text_rect)
        self.rect.topleft = (x, y)

        self.hovered = False

    def update(self):
        if self.hovered:
            self.image = self.image_hovered
        else:
            self.image = self.image_normal

    def draw(self, screen):
        screen.blit(self.image, self.rect)


def show_map(ll_spn=None, map_type="map", add_params=None, z='0.004,0.0019'):
    if ll_spn:
        map_request = f"http://static-maps.yandex.ru/1.x/?{ll_spn}&spn={z}&l={map_type}"
    else:
        map_request = f"http://static-maps.yandex.ru/1.x/?l={map_type}"
    if add_params:
        map_request += "&" + add_params
    response = requests.get(map_request)
    if not response:
        print('Error')
        print(map_request)
        print('HTTP статус:', response.status_code)
        print(response.reason)
        sys.exit(1)

    map_file = 'map.png'

    with open(map_file, 'wb') as file:
        file.write(response.content)
    return map_file


pygame.init()
screen = pygame.display.set_mode((600, 450))
pygame.display.set_caption('Map')
zoom = [0.0065 * 8, 0]
q = 4
type = 'map'
font = pygame.font.Font(None, 32)
clock = pygame.time.Clock()
input_box = pygame.Rect(0, 0, 140, 32)
color_inactive = pygame.Color('lightblue')
btn1 = Button('СБРОС', 0, 33, 80, 40)
color_active = pygame.Color('blue')
color = color_inactive
active = False
df = False
text = ''
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT or event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            running = False
        elif event.type == pygame.KEYUP:
            if read == '1':
                if event.key == pygame.K_PAGEUP and q != 15:
                    q += 1
                    zoom[0] *= 2
                    zoom[1] *= 2
                elif event.key == pygame.K_PAGEDOWN and q != 1:
                    zoom[0] /= 2
                    zoom[1] /= 2
                    q -= 1
            else:
                if event.key == pygame.K_MINUS and q != 15:
                    q += 1
                    zoom[0] *= 2
                    zoom[1] *= 2
                elif event.key == pygame.K_EQUALS and q != 1:
                    zoom[0] /= 2
                    zoom[1] /= 2
                    q -= 1

            if event.key == pygame.K_UP:
                if float(c[0]) + zoom[0] / 4 > 80:
                    c[0] = '80'
                else:
                    print(0)
                    c[0] = str(float(c[0]) + zoom[0] / 4)
            elif event.key == pygame.K_DOWN:
                if float(c[0]) - zoom[0] / 4 < -80:
                    c[0] = '-80'
                else:
                    c[0] = str(float(c[0]) - zoom[0] / 4)

            elif event.key == pygame.K_RIGHT:
                if float(c[1]) + zoom[0] / 2 > 179.9:
                    c[1] = '179.9'
                else:
                    c[1] = str(float(c[1]) + zoom[0] / 2)
            elif event.key == pygame.K_LEFT:
                if float(c[1]) - zoom[0] / 2 < -179.9:
                    c[1] = '-179.9'
                else:
                    c[1] = str(float(c[1]) - zoom[0] / 2)

            elif event.key == pygame.K_TAB:
                if type == 'map':
                    type = 'sat'
                elif type == 'sat':
                    type = 'sat,skl'
                elif type == 'sat,skl':
                    type = 'map'
        if event.type == pygame.MOUSEMOTION:
            btn1.hovered = btn1.rect.collidepoint(event.pos)
        if event.type == pygame.MOUSEBUTTONDOWN:
            if btn1.hovered:
                df = True
            if input_box.collidepoint(event.pos):
                active = not active
            else:
                active = False
            color = color_active if active else color_inactive
        if event.type == pygame.KEYDOWN:
            if active:
                if event.key == pygame.K_RETURN:
                    if text[-1] in '1234567890':
                        zoom[1] = 0.0005
                        zoom[0] = 0.00164
                    else:
                        zoom = [0.0065 * 8, 0.00000001]
                    c = list(get_coordinates(text))
                    c_flag = c[:]
                    text = ''
                    df = False
                elif event.key == pygame.K_BACKSPACE:
                    text = text[:-1]
                else:
                    text += event.unicode

        if df:
            map_file = show_map(ll_spn=f'll={c[1]},{c[0]}', z=f'{zoom[0]},{zoom[1]}', map_type=type)
        else:
            map_file = show_map(ll_spn=f'll={c[1]},{c[0]}', z=f'{zoom[0]},{zoom[1]}', map_type=type,
                                add_params=f'pt={c_flag[1]},{c_flag[0]},flag')
        screen.blit(pygame.image.load(map_file), (0, 0))
        txt_surface = font.render(text, True, color)
        width = max(200, txt_surface.get_width() + 10)
        input_box.w = width
        btn1.update()
        btn1.draw(screen)
        screen.blit(txt_surface, (input_box.x + 5, input_box.y + 5))
        pygame.draw.rect(screen, color, input_box, 2)
        pygame.display.flip()
        clock.tick(30)

pygame.quit()
os.remove(map_file)
