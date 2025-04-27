import requests

def get_map_image(ll, spn, l, filename):
    url = f"https://static-maps.yandex.ru/1.x/?ll={ll}&spn={spn}&l={l}"
    response = requests.get(url)
    if response.status_code == 200:
        with open(filename, 'wb') as f:
            f.write(response.content)
        print(f"Изображение сохранено как {filename}")
    else:
        print("Ошибка при получении изображения:", response.status_code)

get_map_image("86.092233,55.351848", "0.01,0.01", "map", "kemgu_map.png")
get_map_image("86.194744,54.690470", "0.001,0.001", "map", "groove_street.png")
get_map_image("86.169071,54.670292", "0.01,0.01", "map", "lk_map.png")
get_map_image("2.2945,48.8584", "0.01,0.01", "sat", "eiffel.png")
get_map_image("158.6633,53.0369", "0.01,0.01", "sat", "vulkan.png")
get_map_image("105.0009,53.5587", "0.05,0.05", "sat", "baikal.png")
get_map_image("63.3055,45.9656", "0.05,0.05", "sat", "baikonur.png")