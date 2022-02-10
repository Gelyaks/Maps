import requests
import os
import sys
import pygame

c = input('Введите координаты: ').split(', ')


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
zoom = [0.004, 0.0019]
while pygame.event.wait().type != pygame.QUIT:
    map_file = show_map(ll_spn=f'll={c[1]},{c[0]}', z=f'{zoom[0]},{zoom[1]}')
    event = pygame.event.wait()
    if event.type == pygame.KEYUP:
        if event.key == 280 and zoom[0] < 10:
            zoom[0] += 0.01
            zoom[1] += 0.01
        elif event.key == 281 and zoom[0] > 0.001:
            zoom[0] -= 0.01
            zoom[1] += 0.01
    screen.blit(pygame.image.load(map_file), (0, 0))
    pygame.display.flip()
pygame.quit()

os.remove(map_file)
# 55.859564, 37.443721

