class Container:
    maxId = 0
    def __init__(self):
        self.id = Container.maxId
        Container.maxId += 1

    def __str__(self):
        return str(f'{self.id}')
