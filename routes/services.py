from trains.models import Train


def dfs_paths(graph, start, end):
    """функция поиска всех возможных маршрутов
    из одного города в другой. Вариант посещения
     одного и тогоже города более одного раза
     не рассматривается
     """
    stack = [(start, [start])]
    while stack:
        (vertex, path) = stack.pop()
        if vertex in graph.keys():
            for next_ in graph[vertex] - set(path):
                if next_ == end:
                    yield path + [next_]
                else:
                    stack.append((next_, path + [next_]))


def get_graph(qs) -> dict:
    """функция создает словарь где key=id городов
    а value=связи с другими городами"""
    graph = {}
    for q in qs:
        graph.setdefault(q.from_city_id, set())
        graph[q.from_city_id].add(q.to_city_id)
    return graph


def get_routes(request, form) -> dict:
    """функция поиска маршрутов"""
    context = {'form': form}
    qs = Train.objects.all()
    graph = get_graph(qs)
    data = form.cleaned_data
    from_city = data['from_city']
    to_city = data['to_city']
    cities = data['cities']
    travelling_time = data['travelling_time']

    all_ways = list(dfs_paths(graph, from_city.id, to_city.id))
    if not len(all_ways):
        # если нет ни одного маршрута для данного поиска
        raise ValueError('Маршрута не существует')
    if cities:
        # проверяем есть  ли города, через которые нужно проехать в списке all_ways
        _cities = [city.id for city in cities]  # получем id города
        right_ways = []
        for route in all_ways:
            if all(city in route for city in _cities):
                right_ways.append(route)
        if not right_ways:
            # если список маршрутов пуст
            raise ValueError('Маршрут через эти города невозможен')
    else:
        right_ways = all_ways
    # создаем словарь all_trains с key=(id) городов и возможным маршрутами
    routes = []
    all_trains = {}
    for q in qs:
        all_trains.setdefault((q.from_city_id, q.to_city_id), [])
        all_trains[(q.from_city_id, q.to_city_id)].append(q)

    for route in right_ways:
        tmp = dict()
        tmp['trains'] = []
        total_time = 0
        for i in range(len(route) - 1):
            qs = all_trains[(route[i], route[i + 1])]
            q = qs[0]
            total_time += q.travel_time
            tmp['trains'].append(q)
        tmp['total_time'] = total_time
        if total_time <= travelling_time:
            # если общее время в пути, меньше заданного,
            # то добавляем маршрут в общий список
            routes.append(tmp)
    if not routes:
        # если список пуст, то нет таких маршрутов,
        # которые удовлетворяли бы заданным условиям
        raise ValueError('Время в пути больше заданного')

    # создаем список отсортированных по времени маршрутов
    sorted_routes = []
    if len(routes) == 1:
        sorted_routes = routes
    else:
        times = list(set(r['total_time'] for r in routes))
        times = sorted(times)
        for time in times:
            for route in routes:
                if time == route['total_time']:
                    sorted_routes.append(route)

    context['routes'] = sorted_routes
    context['cities'] = {'from_city': from_city.name, 'to_city': to_city.name}
    return context