class MenuItem:
    """Definicion estandar para un item del menu"""

    def __init__(self, name: str, price : float, origin: str, prep_time_min : int):
        # se establecen variables sencillas y generales para cada plato: nombre, precio, origen y tiempo de preparacion
        self._name = name
        self._price = price
        self._origin = origin
        self._prep_time_min = prep_time_min

    def get_item_info(self):
        # se establece un metodo que retorna una lista con las propiedades generales del objeto
        pass

class Appetizer(MenuItem):
    """Tipo 1 de item del menu: Aperitivo"""

    def __init__(self, name, price, origin, prep_time_min):
        # toma todas las variables de inicio de MenuItem
        super().__init__(name,price, origin, prep_time_min)
        self._cutlery = ["chopsticks"]    # cubierto con el cual se comen las entradas

    def get_item_info(self):
        # se establece un metodo que retorna una lista con las propiedades generales del objeto
        item_info = [
            self._name,
            self._price,
            self._origin,
            self._prep_time_min,
            self._cutlery
        ]
        return item_info

class Beverage(MenuItem):
    """Tipo 2 de item del menu: Bebida"""

    def __init__(self, name, price, origin, prep_time_min, alcohol_percent : int):
        # toma todas las variables de inicio de MenuItem, añadiendo la de porcentaje de alcohol
        super().__init__(name,price, origin, prep_time_min)
        self._alcohol_percent = alcohol_percent

    def get_item_info(self):
        # se establece un metodo que retorna una lista con las propiedades generales del objeto
        item_info = [
            self._name,
            self._price,
            self._origin,
            self._prep_time_min,
            self._alcohol_percent
        ]
        return item_info

class Main_Course(MenuItem):
    """Tipo 3 de item del menu: Plato principal"""

    def __init__(self, name, price, origin, prep_time_min, meat_amount : int):
        # toma todas las variables de inicio de MenuItem, añadiendo la de cantidad de carne
        super().__init__(name,price, origin, prep_time_min)
        self._meat_amount = meat_amount
        self._cutlery = ["chopsticks", "fork", "knife", "spoon"]  # cubierto con el cual se comen los platos principales

    def get_item_info(self):
        # se establece un metodo que retorna una lista con las propiedades generales del objeto
        item_info = [
            self._name,
            self._price,
            self._origin,
            self._prep_time_min,
            self._meat_amount,
            self._cutlery
        ]
        return item_info

class Dessert(MenuItem):
    """Tipo 4 de item del menu: Postre"""

    def __init__(self, name, price, origin, prep_time_min, sweetness : str):
        # toma todas las variables de inicio del MenuItem, añadiendo la de dulzura del postre
        super().__init__(name,price, origin, prep_time_min)
        self._sweetness = sweetness
    def get_item_info(self):
        # se establece un metodo que retorna una lista con las propiedades generales del objeto
        item_info = [
            self._name,
            self._price,
            self._origin,
            self._prep_time_min,
            self._sweetness
        ]
        return item_info

class Order:
    """orden que hara el cliente"""

    def __init__(self):
        # crea una lista vacia privada para registrar los platos a ordenar
        self.__order_list = []

    def add_item(self, plate):
        # verifica que el objeto a ingresar pertenece a la clase MenuItem, para despues agregarlo a la lista order_list
        if isinstance(plate, MenuItem):
            self.__order_list.append(plate)

    def remove_item(self, plate: MenuItem):
        # verifica que el objeto a ingresar pertenece a la clase MenuItem, para despues retirarlo de la lista order_list
        if isinstance(plate, MenuItem):
            self.__order_list.remove(plate)

    def get_list(self):
        # recorre los platos agregados a la lista y agrega sus nombres a una lista vacia para luego retornar esa lista con nombres
        list_names = []
        for i in range(0,len(self.__order_list)):
            list_names.append(self.__order_list[i]._name)
        return list_names
    
    def bill(self):
        # establece un valor de la cuenta en 0, y una lista que registre el tipo de cada plato, recorriendo la lista de la orden y sumando a la cuenta el valor del precio de cada plato, mientras registra el tipo de comida de cada plato, para al final hacer una verificacion de los tipos de platos en la orden para asi realizar un descuento de 10% (plato principal y bebida), o bien del 20% (un plato de cada tipo)
        bill = 0
        plate_type = []

        for i in range(0, len(self.__order_list)):
            plate_type.append(type(self.__order_list[i]))

        if Main_Course in plate_type and Beverage in plate_type:
            bill -= self.__order_list[plate_type.index(Beverage)]._price * 0.10 # descuento de 10% en la bebida si hay un plato principal

        if Main_Course in plate_type and Appetizer in plate_type:
            bill -= self.__order_list[plate_type.index(Main_Course)]._price * 0.10  # descuento de 10% en el plato principal si hay una entrada

        for i in range(0, len(self.__order_list)):
            bill += self.__order_list[i]._price

        if Appetizer in plate_type and Main_Course in plate_type and Beverage in plate_type and Dessert in plate_type:
            bill = bill * 0.80

        elif Beverage in plate_type and Main_Course in plate_type:
            bill = bill * 0.90
        return bill

class MedioPago:
    """superclase para metodo de pago generico"""

    def __init__(self):
        pass

    def pagar(self, monto : float):
        ...

class Efectivo(MedioPago):
    """Subclase de medio de pago en efectivo"""

    def __init__(self, monto_agregado : float):
        # inicializador para un monto de efectivo
        super().__init__()
        self.monto_agregado = monto_agregado
        
    def pagar(self, monto_a_pagar : float):
        # se realiza el descuento del dinero a pagar en el monto de dinero establecido en efectivo, arrojando un error si no hay suficientes fondos
        if self.monto_agregado >= monto_a_pagar:
            print(f"Pago de ${monto_a_pagar} realizado en efectivo. Cambio: ${self.monto_agregado - monto_a_pagar}")
        else:
            print(f"Fondos insuficientes. Faltan ${self.monto_agregado - monto_a_pagar} para completar el pago")
    
class Tarjeta(MedioPago):
    """Subclase de medio de pago en tarjeta"""

    def __init__(self, numero : str, cvv : int):
        # inicializador para ingreso de numero de tarjeta y cvv
        super().__init__()
        self.numero = numero
        self._cvv = cvv
    def pagar(self, monto_a_pagar : float, cvv : int):
        # se realiza el descuento del dinero a pagar si se ingresa correctamente el cvv de la tarjeta al llamar la funcion
        if cvv == self._cvv:
            print(f"Pagando ${monto_a_pagar} con tarjeta {self.numero[-4:]}")
        else:
            print("La clave ingresada es incorrecta, no se ha procesado el pago")

if __name__ == "__main__":
    # Definicion de 3 objetos por cada tipo de comida
    # precios establecidos en USD
    # cantidad de carne en gramos
    appet1 = Appetizer(
        name = "Takoyaki",
        price = 8.5, #USD
        origin = "japan",
        prep_time_min = 15
    )
    appet2 = Appetizer(
        name = "Tteokbokki",
        price = 7,   #USD
        origin = "Korea",
        prep_time_min = 40
    )
    appet3 = Appetizer(
        name = "Mandu",
        price = 8.5, #USD
        origin = "Korea",
        prep_time_min = 50
    )
    bev1 = Beverage(
        name = "Sake bottle",
        price = 15,  #USD
        origin = "Japan",
        prep_time_min = 0,
        alcohol_percent = 15 
    )
    bev2 = Beverage(
        name = "jiuniang",
        price = 12,  #USD
        origin = "China",
        prep_time_min = 30,
        alcohol_percent = 2
    )
    bev3 = Beverage(
        name = "bubble tea",
        price = 15,  #USD
        origin = "Taiwan",
        prep_time_min = 130,
        alcohol_percent = 0
    )
    main1 = Main_Course(
        name = "wagyu",
        price = 25,  #USD
        origin = "Japan",
        prep_time_min = 10,
        meat_amount = 300   #grams
    )
    main2 = Main_Course(
        name = "Curry",
        price = 20,  #USD
        origin = "India",
        prep_time_min = 20,
        meat_amount = 150   #grams
    )
    main3 = Main_Course(
        name = "Ramen",
        price = 20,  #USD
        origin = "Japan",
        prep_time_min = 120,
        meat_amount = 50    #grams
    )
    des1 = Dessert(
        name = "wagashi",
        price = 5,  #USD
        origin = "Japan",
        prep_time_min = 300,
        sweetness = "Moderate"
    )
    des2 = Dessert(
        name = "Yuèbǐng",
        price = 8,  #USD
        origin = "China",
        prep_time_min = 60,
        sweetness = "Low"
    )
    des3 = Dessert(
        name = "Tanghulu",
        price = 6,  #USD
        origin = "China",
        prep_time_min = 30,
        sweetness = "High"
    )

    # impresion de la informacion de todos los platos
    print("Obteniendo informacion de platos... \n")
    print(appet1.get_item_info())
    print(appet2.get_item_info())
    print(appet3.get_item_info())
    print(main1.get_item_info())
    print(main2.get_item_info())
    print(main3.get_item_info())
    print(bev1.get_item_info())
    print(bev2.get_item_info())
    print(bev3.get_item_info())
    print(des1.get_item_info())
    print(des2.get_item_info())
    print(des3.get_item_info())
    print("\n")

    # definicion de orden 1
    Client1 = Order()
    Client1.add_item(appet2)    # agregado de tteokbokki
    Client1.add_item(main2)     # agregado de curry
    Client1.add_item(bev1)      # agregado de sake
    Client1.add_item(des1)      # agregado de wagashi
    client1_bill = Client1.bill()
    print(f"La orden de {Client1.get_list()} tiene un valor de ${client1_bill} USD")   # se imprime los platos pedidos y el precio de estos

    # definicion de orden 2
    Client2 = Order()
    Client2.add_item(appet3)    # agregado de mandu
    Client2.add_item(main3)     # agregado de ramen
    Client2.add_item(bev3)      # agregado de te
    Client2.add_item(des3)      # agregado de tanghulu
    client2_bill = Client2.bill()
    print(f"La orden de {Client2.get_list()} tiene un valor de ${client2_bill} USD")   # se imprime los platos pedidos y el precio de estos

    # definicion de orden 3
    Client3 = Order()
    Client3.add_item(main1)     # agregado de wagyu
    Client3.add_item(bev1)      # agregado de sake
    client3_bill = Client3.bill()
    print(f"La orden de {Client3.get_list()} tiene un valor de ${client3_bill} USD")   # se imprime los platos pedidos y el precio de estos

    # pago de la orden del cliente 1 (en efectivo), y cliente 2 (con tarjeta)
    Client1_payment = Efectivo(50.0)
    Client2_payment = Tarjeta("1441589435", 101)

    print("\n")
    Client1_payment.pagar(client1_bill)
    Client2_payment.pagar(client2_bill, 101)