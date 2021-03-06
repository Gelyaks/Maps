import requests
import os
import sys
import pygame

c = input('' + '\n' + 'Пример ввода: 49.422, 53.51' + '\n' + 'Введите свои координаты: ').split(', ')


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
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT or event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            running = False
        elif event.type == pygame.KEYUP:

            if event.key == pygame.K_PAGEUP and q != 15:
                q += 1
                zoom[0] *= 2
            elif event.key == pygame.K_PAGEDOWN and q != 1:
                zoom[0] /= 2
                q -= 1

            elif event.key == pygame.K_RIGHT:
                if float(c[0]) + zoom[0] / 2 > 179.9:
                    c[0] = '179.9'
                else:
                    c[0] = str(float(c[0]) + zoom[0] / 2)
            elif event.key == pygame.K_LEFT:
                if float(c[0]) - zoom[0] / 2 < -179.9:
                    c[0] = '-179.9'
                else:
                    c[0] = str(float(c[0]) - zoom[0] / 2)

            elif event.key == pygame.K_UP:
                if float(c[1]) + zoom[0] / 4 > 80:
                    c[1] = '80'
                else:
                    c[1] = str(float(c[1]) + zoom[0] / 4)
            elif event.key == pygame.K_DOWN:
                if float(c[1]) - zoom[0] / 4 < -80:
                    c[1] = '-80'
                else:
                    c[1] = str(float(c[1]) - zoom[0] / 4)

        map_file = show_map(ll_spn=f'll={c[0]},{c[1]}', z=f'{zoom[0]},{zoom[1]}')
        screen.blit(pygame.image.load(map_file), (0, 0))
        pygame.display.flip()
pygame.quit()
os.remove(map_file)

# Примеры ввода:
# 133.795, -25.695    Австралия
# 49.422, 53.51       Тольятти
