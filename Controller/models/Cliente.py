class Cliente:
    def __init__(self, id, nombre, edad, profesion, foto,idEquipo=None):
        self.id = id
        self.nombre = nombre
        self.edad = edad
        self.profesion = profesion
        self.foto = foto
        self.idEquipo = idEquipo