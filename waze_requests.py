import requests
import json
import datetime

'''
streetNames
routeNameStreetIds
routeType (list)
'''

# url = 'https://www.waze.com/row-RoutingManager/routingRequest?from=x:15.895349979400637+y:45.75747835716078&to=x:14.5925861+y:45.08093559999999&at=0&returnJSON=true&returnGeometries=true&returnInstructions=true&timeout=60000&nPaths=3&clientVersion=4.0.0&options=AVOID_TRAILS:t,ALLOW_UTURNS:t'
# url = 'https://www.waze.com/row-RoutingManager/routingRequest?from=x:17.0838628+y:48.1663921&to=x:17.1358266+y:48.17539219999999&at=0&returnJSON=true&timeout=60000&nPaths=3&clientVersion=4.0.0&options=AVOID_TRAILS:t,ALLOW_UTURNS:t'
# url = 'https://www.waze.com/row-RoutingManager/routingRequest?from=x:16.6981462+y:46.42023210000001&to=x:15.243803977966309+y:44.117332458496094&at=0&returnJSON=true&returnGeometries=true&returnInstructions=true&timeout=60000&nPaths=3&clientVersion=4.0.0&options=AVOID_TRAILS:t,ALLOW_UTURNS:t'
URL = 'https://www.waze.com/row-RoutingManager/routingRequest?from=x:{}+y:{}&to=x:{}+y:{}&at=0&returnJSON=true&timeout=60000&nPaths=3&clientVersion=4.0.0&options=AVOID_TRAILS:t,ALLOW_UTURNS:t'


def main(route):
    print(route)

    with open('config.json') as config_file:
        conf = json.load(config_file)
        route_from = conf['routes'][route]['from']
        route_to = conf['routes'][route]['to']
        route_from_x = conf['locations'][route_from]['x']
        route_from_y = conf['locations'][route_from]['y']
        route_to_x = conf['locations'][route_to]['x']
        route_to_y = conf['locations'][route_to]['y']
        url = URL.format(route_from_x, route_from_y, route_to_x, route_to_y)
        print(url)

    with requests.Session() as s:
        # livemap = s.get('https://www.waze.com/login/get')

        headers = {
            'Host': 'www.waze.com',
            'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:43.0) Gecko/20100101 Firefox/43.0',
            'Accept': '*/*',
            'X-Requested-With': 'XMLHttpRequest',
            'Referer': 'https://www.waze.com/livemap',
        }

        response = s.get(url, headers=headers)
        print(response)
        data = response.json()
        datestring = datetime.datetime.today().strftime('%Y%m%d%H%M%S')
        path = 'downloaded/{}-{}.json'.format(route, datestring)
        with open(path, 'w') as f:
            json.dump(data, f)

        print('alternatives:')
        for a in data['alternatives']:
            res = a['response']
            print(res['routeName'])
            print(res['totalRouteTime'])


if __name__ == '__main__':
    import sys
    if len(sys.argv) < 2:
        print('Usage: python -m waze_requests [route]')
        exit(1)
    route = sys.argv[1]
    main(route)
