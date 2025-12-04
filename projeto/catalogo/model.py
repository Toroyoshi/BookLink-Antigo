class Catalogo:
    def __init__(self, obras, autores, exemplares, disponibilidade, metadados ):
        self.obras = obras
        self.autores = autores
        self.exemplares = exemplares
        self.disponibilidade = disponibilidade
        self.metadados = metadados
        pass

    def to_json(self):
        return {}