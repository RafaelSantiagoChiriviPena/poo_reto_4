from math import atan2
from math import degrees

class Shape:
    """Se define una clase general con metodos planos para poder ser sobreescritos en las clases heredadas"""

    def __init__(self):
        pass
    def compute_area(self):
        pass
    def compute_perimeter(self):
        pass
    def compute_inner_angles(self):
        pass

class Point:
    """Se define un punto del espacio"""

    def __init__(self,x,y):
        # se establecen coordenadas x,y para el punto
        self.x = x
        self.y = y

    def compute_distance(self, point: "Point")-> float:
        # determina la diferencia entre cada eje de coordenadas entre los puntos, y obteniendo su distancia por medio de pitagoras
        distance = ((self.x - point.x)**2+(self.y - point.y)**2)**(0.5)
        return distance


class Line:
    """Linea con un punto de inicio y uno de final"""

    def __init__(self,start: Point,end: Point):
        # se inicializa un inicio y un final aclarando que estos pertenecen a la clase Point
        self.start = start
        self.end = end

    def compute_lenght(self):
        # hace una diferencia en el eje x y el eje y para asi calcular la longitud mediante pitagoras (a^2 + b^2 = h^2)
        horizontal_lenght = self.end.x-self.start.x
        vertical_lenght = self.end.y - self.start.y
        lenght = (vertical_lenght**2 + horizontal_lenght**2)**(1/2)
        return lenght
    
    def compute_slope(self):
        # usando atan2 calcula en radianes el angulo formado por los componentes x y y del triangulo que forma la recta, para luego transformarlo a grados
        return degrees(atan2(abs(self.end.y - self.start.y), abs(self.end.x-self.start.x)))
    
    def compute_horizontal_cross(self):
        # verifica que la linea corte el eje x multiplicando su inicio y fin en y, si es negativo, pasa por el eje (Teorema de bolzano)
        if self.start.y * self.end.y <= 0:
            print("La recta corta al eje x")

    def compute_vertical_cross(self):
        # verifica que la linea corte el eje y multiplicando su inicio x fin en x, si es negativo, pasa por el eje (Teorema de bolzano)
        if self.start.x * self.end.x <= 0:
            print("La recta corta al eje y")

    def discretize_line(self, n):
        # toma un numero de puntos para discretizar la linea, y define el avance que se hara en cada eje segun la diferencia en los ejes, para luego crear una lista con cada uno de los puntos, iterando hasta que una variable i llegue al valor del n ingresado para la cantidad de puntos
        array_points = []
        x_advance = (self.end.x - self.start.x)/n
        y_advance = (self.end.y - self.start.y)/n
        i = 0
        while i <= n:
            array_points.append((self.start.x, self.start.y))
            self.start.x = self.start.x + x_advance
            self.start.y = self.start.y + y_advance     
            i += 1
        return array_points

class Rectangle(Shape):
    """Reinvencion de la clase Rectangle, añadiendo vertices, aristas y angulos internos a su definicion"""
    is_regular = False  # atributo de regularidad falso

    def __init__(self, vertices : list, edges : list, inner_angles : list):
        # se define cada una de las listas
        super().__init__()
        self._vertices = vertices
        self._edges = edges #orden: height1, width1, height2, width2
        self._inner_angles = inner_angles

    def compute_area(self):
        # toma coordenadas de los puntos de las lineas para determinar altura y anchura del rectangulo para asi calcular el area
        return ((self._edges[0].end.y-self._edges[0].start.y) * (self._edges[3].end.x - self._edges[3].start.x))
        
    def compute_perimeter(self):
        # toma coordenadas de los puntos de las lineas para determinar altura y anchura del rectangulo para asi calcular el perimetro
        return 2 * ((self._edges[0].end.y-self._edges[0].start.y) + (self._edges[3].end.x - self._edges[3].start.x))
    
    def get_vertices(self):
        # obtiene los compnentes x y y de cada punto definido para el objeto, ubicandolo en tuplas que seran puestas en una lista que es el retorno de la funcion
        vertices_get = []
        for i in range(0, len(self._vertices)):
            point_get = (self._vertices[i].x , self._vertices[i].y)
            vertices_get.append(point_get)
        return vertices_get
    
    def get_edges(self):
        # obtiene los puntos de inicio y final de cada linea, escribiendola como una cadena de la forma "(x1,y1) - (x2,y2)" para luego poner cada cadena en una lista que es el retorno de la funcion
        edges_get = []
        for i in range(0, len(self._edges)):
            line_get = f"({self._edges[i].start.x},{self._edges[i].start.y}) - ({self._edges[i].end.x},{self._edges[i].end.y})"
            edges_get.append(line_get)
        return edges_get
        
    def get_inner_angles(self):
        # retorna la lista definida de angulos internos
        return self._inner_angles
    
class Square(Rectangle, Shape):
    """Clase que hereda todos los metodos de rectangle, con una unica diferencia en su definicion, las lineas deben tener la misma longitud"""
    is_regular = True   #atributo de regularidad verdadero

    def __init__(self, vertices : list, edges : list, inner_angles : list):
        super().__init__(vertices, edges, inner_angles)

class Triangle(Shape):
    """Subclase de Shape, una figura de 3 lados"""
    is_regular = False  #atributo de regularidad falso

    def __init__(self, vertices : list, edges : list):
        # se define cada una de las listas
        super().__init__()
        self._vertices = vertices
        self._edges = edges

    def compute_perimeter(self):
        # se recorre la lista de aristas para poder calcular su longitud y asi sumarla a una variable perimetro
        perimeter = 0
        for i in range(0, len(self._edges)):
            perimeter += self._edges[i].compute_lenght()
        return perimeter
    
    def compute_area(self):
        # se utiliza la formula de heron que se apoya en el semiperimetro y las longitudes de los lados para determinar el area de cualquier triangulo
        semiperimeter = self.compute_perimeter() / 2
        return (semiperimeter * (semiperimeter - self._edges[0].compute_lenght()) * (semiperimeter - self._edges[1].compute_lenght()) * (semiperimeter - self._edges[2].compute_lenght())) ** 0.5
    
    def get_vertices(self):
        # obtiene los compnentes x y y de cada punto definido para el objeto, ubicandolo en tuplas que seran puestas en una lista que es el retorno de la funcion
        vertices_get = []
        for i in range(0, len(self._vertices)):
            point_get = (self._vertices[i].x , self._vertices[i].y)
            vertices_get.append(point_get)
        return vertices_get
    
    def get_edges(self):
        # obtiene los puntos de inicio y final de cada linea, escribiendola como una cadena de la forma "(x1,y1) - (x2,y2)" para luego poner cada cadena en una lista que es el retorno de la funcion
        edges_get = []
        for i in range(0, len(self._edges)):
            line_get = f"({self._edges[i].start.x},{self._edges[i].start.y}) - ({self._edges[i].end.x},{self._edges[i].end.y})"
            edges_get.append(line_get)
        return edges_get

class Isosceles(Triangle, Shape):
    """Clase que hereda todos los metodos de Triangle, siendo un triangulo de 2 lados iguales y 1 diferente en su definicion"""
    is_regular = False  #atributo de regularidad falso

    def __init__(self, vertices : list, edges : list):
        super().__init__(vertices, edges)

class Equilateral(Triangle, Shape):
    """Clase que hereda todos los metodos de Triangle, siendo un triangulo de 3 lados iguales en su definicion"""
    is_regular = True   #atributo de regularidad verdadero

    def __init__(self, vertices : list, edges : list):
        super().__init__(vertices, edges)

class Scalene(Triangle, Shape):
    """Clase que hereda todos los metodos de Triangle, siendo un triangulo de 3 lados diferentes en su definicion"""
    is_regular = False  #atributo de regularidad falso

    def __init__(self, vertices : list, edges : list):
        super().__init__(vertices, edges)

class TriRectangle(Triangle, Shape):
    """Clase que hereda todos los metodos de Triangle, siendo un triangulo en que uno de sus angulos internos es de 90 grados"""
    is_regular = False  #atributo de regularidad falso

    def __init__(self, vertices : list, edges : list):
        super().__init__(vertices, edges)

if __name__ == "__main__":
    # definicion para cada tipo de figura, y aplicando sus metodos con la estructura: vertices, aristas, angulos, perimetro y area
    rectangle_test = Rectangle(
        vertices = (
            Point(0,0),
            Point(3,2),
            Point(0,2),
            Point(3,0)
        ),
        edges= (
            Line(
                start = Point(0,0),
                end = Point(0,2)
            ),
            Line(
                start = Point(0,2),
                end = Point(3,2)
            ),
            Line(
                start = Point(3,2),
                end = Point(3,0)
            ),
            Line(
                start = Point(0,0),
                end = Point(3,0)
            )
        ),
        inner_angles=(90, 90, 90, 90)
    )

    print(rectangle_test.get_vertices())
    print(rectangle_test.get_edges())
    print(rectangle_test.get_inner_angles())
    print(f"El perimetro del rectangulo es de {rectangle_test.compute_perimeter()} unidades")
    print(f"El area del rectangulo es de {rectangle_test.compute_area()} unidades cuadradas \n")

    square_test = Square(
        vertices= (
            Point(0,0),
            Point(3,3),
            Point(0,3),
            Point(3,0)
        ),
        edges= (
            Line(
                start = Point(0,0),
                end = Point(0,3)
            ),
            Line(
                start = Point(0,3),
                end = Point(3,3)
            ),
            Line(
                start = Point(3,3),
                end = Point(3,0)
            ),
            Line(
                start = Point(0,0),
                end = Point(3,0)
            )
        ),
        inner_angles= [90, 90, 90, 90]
    )

    print(square_test.get_vertices())
    print(square_test.get_edges())
    print(square_test.get_inner_angles())
    print(f"El perimetro del cuadrado es de {square_test.compute_perimeter()} unidades")
    print(f"El area del cuadrado es de {square_test.compute_area()} unidades cuadradas \n")

    IsosTriangle_test = Isosceles(
        vertices = (
            Point(0,0),
            Point(4,0),
            Point(2,21 ** 0.5)
        ),
        edges = (
            Line(
                start = Point(0,0),
                end = Point(4,0),
            ),
            Line(
                start = Point(4,0),
                end = Point(2, 21 ** 0.5)
            ),
            Line(
                start = Point(2, 21 ** 0.5),
                end = Point(0,0)
            )
        )
    )

    print(IsosTriangle_test.get_vertices())
    print(IsosTriangle_test.get_edges())
    print(f"El perimetro del triangulo es de {IsosTriangle_test.compute_perimeter()} unidades")
    print(f"El area del triangulo es de {IsosTriangle_test.compute_area()} unidades cuadradas \n")

    EquiTriangle_test = Equilateral(
        vertices = (
            Point(0,0),
            Point(4,0),
            Point(2,12 ** 0.5)
        ),
        edges = (
            Line(
                start = Point(0,0),
                end = Point(4,0),
            ),
            Line(
                start = Point(4,0),
                end = Point(2, 12 ** 0.5)
            ),
            Line(
                start = Point(2, 12 ** 0.5),
                end = Point(0,0)
            )
        )
    )

    print(EquiTriangle_test.get_vertices())
    print(EquiTriangle_test.get_edges())
    print(f"El perimetro del triangulo es de {EquiTriangle_test.compute_perimeter()} unidades")
    print(f"El area del triangulo es de {EquiTriangle_test.compute_area()} unidades cuadradas \n")

    ScalTriangle_test = Scalene(
        vertices = (
            Point(0,0),
            Point(3,0),
            Point(1,16 ** 0.5)
        ),
        edges = (
            Line(
                start = Point(0,0),
                end = Point(3,0),
            ),
            Line(
                start = Point(3,0),
                end = Point(1, 16 ** 0.5)
            ),
            Line(
                start = Point(1, 16 ** 0.5),
                end = Point(0,0)
            )
        )
    )

    print(ScalTriangle_test.get_vertices())
    print(ScalTriangle_test.get_edges())
    print(f"El perimetro del triangulo es de {ScalTriangle_test.compute_perimeter()} unidades")
    print(f"El area del triangulo es de {ScalTriangle_test.compute_area()} unidades cuadradas \n")

    TriRect_test = TriRectangle(
        vertices = (
            Point(0,0),
            Point(3,0),
            Point(3,4)
        ),
        edges = (
            Line(
                start = Point(0,0),
                end = Point(3,0),
            ),
            Line(
                start = Point(3,0),
                end = Point(3,4)
            ),
            Line(
                start = Point(3,4),
                end = Point(0,0)
            )
        )
    )

    print(TriRect_test.get_vertices())
    print(TriRect_test.get_edges())
    print(f"El perimetro del triangulo es de {TriRect_test.compute_perimeter()} unidades")
    print(f"El area del triangulo es de {TriRect_test.compute_area()} unidades cuadradas \n")