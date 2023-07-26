from trains.models import Train


def get_graph(qs):
    graph = {}
    for query in qs:
        graph.setdefault(query.from_city_id, set())
        graph[query.from_city_id].add(query.to_city_id)
        return graph


def get_routes(request, form) -> dict:
    qs = Train.objects.all()
    graph = get_graph(qs)
