import requests
class example:
    def get_address(request, meta_address):
        address = []
        for item in meta_address:
            try:
                if request.is_ajax():
                    print('работаем')
                    return HttpResponse('pending')
                if item not in address:
                    if request.is_ajax():
                        print('работаем')
                        return HttpResponse('pending')
                    url_geocoder = requests.get("https://geocode-maps.yandex.ru/1.x/?format=json&geocode=" + str(item) +"&results=100")
                    response1 = url_geocoder.json()
                    print(url_geocoder.json())
                    short_address = response1['response']['GeoObjectCollection']['featureMember'][0]['GeoObject']['metaDataProperty']['GeocoderMetaData']['text']

                    only_street = short_address[::-1].split(',')
                    print(short_address)
                    print(only_street[1][::-1] + ',' + only_street[0][::-1])
                    address.append(only_street[1][::-1] + ',' + only_street[0][::-1])
            except:
                pass
        return address
