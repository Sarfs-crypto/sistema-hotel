"""
MODELO: Gestión de Habitaciones
Implementa la jerarquía de habitaciones con los 4 pilares de POO
"""

from abc import ABC, abstractmethod
from datetime import datetime


class Habitacion(ABC):
    """Clase abstracta base para todas las habitaciones (ABSTRACCION)"""
    
    def __init__(self, numero: int, piso: int, tarifa_base: float):
        # Atributos privados (ENCAPSULAMIENTO)
        self.__numero = numero
        self.__piso = piso
        self.__estado = "disponible"  # disponible, ocupada, limpieza, mantenimiento
        self.__tarifa_base = tarifa_base
        
        # Atributos protegidos
        self._servicios_incluidos = []
        self._historial_huespedes = []
    
    # ========== METODOS ABSTRACTOS ==========
    @abstractmethod
    def calcular_tarifa_noche(self) -> float:
        """Calcula tarifa por noche (POLIMORFISMO)"""
        pass
    
    @abstractmethod
    def capacidad_maxima(self) -> int:
        """Retorna capacidad máxima"""
        pass
    
    # ========== METODOS CONCRETOS ==========
    def cambiar_estado(self, nuevo_estado: str):
        """Cambia el estado de la habitación"""
        estados_validos = ["disponible", "ocupada", "limpieza", "mantenimiento"]
        if nuevo_estado in estados_validos:
            self.__estado = nuevo_estado
            return True
        return False
    
    def agregar_huesped_al_historial(self, huesped: str):
        """Agrega un huesped al historial"""
        registro = {
            "huesped": huesped,
            "fecha": datetime.now().strftime("%Y-%m-%d %H:%M"),
            "habitacion": f"{self.__numero} ({self.__class__.__name__})"
        }
        self._historial_huespedes.append(registro)
    
    # ========== METODOS PRIVADOS ==========
    def __calcular_impuestos(self, subtotal: float) -> float:
        """Calcula impuestos (método privado)"""
        return subtotal * 0.24
    
    # ========== GETTERS Y SETTERS ==========
    @property
    def numero(self) -> int:
        return self.__numero
    
    @property
    def piso(self) -> int:
        return self.__piso
    
    @property
    def estado(self) -> str:
        return self.__estado
    
    @property
    def tarifa_base(self) -> float:
        return self.__tarifa_base
    
    @property
    def servicios_incluidos(self):
        return self._servicios_incluidos.copy()
    
    @property
    def historial_huespedes(self):
        return self._historial_huespedes.copy()
    
    def __str__(self):
        return f"Habitación {self.__numero} - {self.__class__.__name__}"


class HabitacionSimple(Habitacion):
    """Habitación simple (HERENCIA)"""
    
    def __init__(self, numero: int, piso: int, cama_individual: bool, vista: str, baño_compartido: bool):
        super().__init__(numero, piso, tarifa_base=50.0)
        self.cama_individual = cama_individual
        self.vista = vista
        self.baño_compartido = baño_compartido
        self._servicios_incluidos = ["Wi-Fi", "TV básica", "Aire acondicionado"]
    
    def calcular_tarifa_noche(self) -> float:
        """Implementación específica (POLIMORFISMO)"""
        tarifa = self.tarifa_base
        
        if self.vista == "calle":
            tarifa += 10
        elif self.vista == "jardin":
            tarifa += 15
        
        if self.baño_compartido:
            tarifa -= 5
        
        impuestos = self._Habitacion__calcular_impuestos(tarifa)
        return tarifa + impuestos
    
    def capacidad_maxima(self) -> int:
        return 1
    
    def __str__(self):
        baño_info = "Compartido" if self.baño_compartido else "Privado"
        return (f"Simple #{self.numero} | Piso {self.piso} | Vista: {self.vista} | "
                f"Baño: {baño_info} | ${self.calcular_tarifa_noche():,.0f}/noche")


class HabitacionDoble(Habitacion):
    """Habitación doble (HERENCIA)"""
    
    def __init__(self, numero: int, piso: int, tipo_camas: str, vista: str, baño_privado: bool):
        super().__init__(numero, piso, tarifa_base=80.0)
        self.tipo_camas = tipo_camas
        self.vista = vista
        self.baño_privado = baño_privado
        self._servicios_incluidos = ["Wi-Fi premium", "TV 32\"", "Minibar", "Aire acondicionado"]
    
    def calcular_tarifa_noche(self) -> float:
        tarifa = self.tarifa_base
        
        if self.vista == "marina":
            tarifa += 25
        elif self.vista == "montaña":
            tarifa += 20
        
        if self.tipo_camas == "cama king":
            tarifa += 15
        
        impuestos = self._Habitacion__calcular_impuestos(tarifa)
        return tarifa + impuestos
    
    def capacidad_maxima(self) -> int:
        if "2 camas" in self.tipo_camas:
            return 3
        return 2
    
    def __str__(self):
        return (f"Doble #{self.numero} | Piso {self.piso} | {self.tipo_camas} | "
                f"Vista: {self.vista} | ${self.calcular_tarifa_noche():,.0f}/noche")


class Suite(Habitacion):
    """Suite (HERENCIA)"""
    
    def __init__(self, numero: int, piso: int, sala_estar: bool, cocina: bool, 
                 jacuzzi: bool, num_habitaciones: int):
        super().__init__(numero, piso, tarifa_base=200.0)
        self.sala_estar = sala_estar
        self.cocina = cocina
        self.jacuzzi = jacuzzi
        self.num_habitaciones = num_habitaciones
        self._servicios_incluidos = ["Wi-Fi VIP", "TV 55\"", "Minibar", "Jacuzzi"]
    
    def calcular_tarifa_noche(self) -> float:
        tarifa = self.tarifa_base
        
        if self.sala_estar:
            tarifa += 50
        if self.cocina:
            tarifa += 30
        if self.jacuzzi:
            tarifa += 80
        if self.num_habitaciones > 1:
            tarifa += (self.num_habitaciones - 1) * 40
        
        impuestos = self._Habitacion__calcular_impuestos(tarifa)
        return tarifa + impuestos
    
    def capacidad_maxima(self) -> int:
        return self.num_habitaciones * 2 + 2
    
    def __str__(self):
        amenities = []
        if self.sala_estar: amenities.append("Sala")
        if self.cocina: amenities.append("Cocina")
        if self.jacuzzi: amenities.append("Jacuzzi")
        
        return (f"Suite #{self.numero} | {self.num_habitaciones} habs | "
                f"Amenities: {', '.join(amenities)} | ${self.calcular_tarifa_noche():,.0f}/noche")


class Penthouse(Habitacion):
    """Penthouse (HERENCIA)"""
    
    def __init__(self, numero: int, piso: int, piso_completo: bool, 
                 terraza: bool, servicio_mayordomo: bool):
        super().__init__(numero, piso, tarifa_base=500.0)
        self.piso_completo = piso_completo
        self.terraza = terraza
        self.servicio_mayordomo = servicio_mayordomo
        self._servicios_incluidos = ["Wi-Fi empresarial", "TV 65\" 4K", 
                                     "Minibar premium", "Mayordomo"]
    
    def calcular_tarifa_noche(self) -> float:
        tarifa = self.tarifa_base
        
        if self.piso_completo:
            tarifa += 200
        if self.terraza:
            tarifa += 100
        if self.servicio_mayordomo:
            tarifa += 150
        
        impuestos = self._Habitacion__calcular_impuestos(tarifa)
        return tarifa + impuestos
    
    def capacidad_maxima(self) -> int:
        base = 8
        if self.piso_completo:
            base += 2
        if self.terraza:
            base += 2
        return base
    
    def __str__(self):
        features = []
        if self.piso_completo: features.append("Piso completo")
        if self.terraza: features.append("Terraza")
        if self.servicio_mayordomo: features.append("Mayordomo")
        
        return (f"Penthouse #{self.numero} | Piso {self.piso} | "
                f"Características: {', '.join(features)} | ${self.calcular_tarifa_noche():,.0f}/noche")