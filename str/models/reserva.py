"""
MODELO: Sistema de Reservas y Huéspedes
Implementa reservas individuales, grupales, corporativas y paquetes turísticos
"""

from abc import ABC, abstractmethod
from datetime import datetime, timedelta
from typing import List


class Reserva(ABC):
    """Clase abstracta base para todas las reservas (ABSTRACCION)"""
    
    def __init__(self, codigo_reserva: str, fecha_inicio: str, fecha_fin: str, habitacion):
        # Atributos privados (ENCAPSULAMIENTO)
        self.__codigo_reserva = codigo_reserva
        self.__fecha_inicio = fecha_inicio
        self.__fecha_fin = fecha_fin
        self.__habitacion = habitacion
        
        # Atributo protegido
        self._huespedes = []  # Lista de huéspedes
    
    # ========== METODOS ABSTRACTOS ==========
    @abstractmethod
    def calcular_costo_total(self) -> float:
        """Calcula costo total de la reserva (POLIMORFISMO)"""
        pass
    
    @abstractmethod
    def politica_cancelacion(self) -> str:
        """Retorna política de cancelación (POLIMORFISMO)"""
        pass
    
    # ========== METODOS CONCRETOS ==========
    def agregar_huesped(self, huesped: str):
        """Agrega un huésped a la reserva"""
        self._huespedes.append(huesped)
    
    # ========== METODOS PRIVADOS ==========
    def __calcular_noches(self) -> int:
        """Calcula número de noches de la reserva (ENCAPSULAMIENTO)"""
        try:
            fecha_inicio = datetime.strptime(self.__fecha_inicio, "%Y-%m-%d")
            fecha_fin = datetime.strptime(self.__fecha_fin, "%Y-%m-%d")
            return (fecha_fin - fecha_inicio).days
        except ValueError:
            return 1  # Valor por defecto si hay error en fechas
    
    # ========== GETTERS Y SETTERS ==========
    @property
    def codigo_reserva(self) -> str:
        return self.__codigo_reserva
    
    @property
    def fecha_inicio(self) -> str:
        return self.__fecha_inicio
    
    @property
    def fecha_fin(self) -> str:
        return self.__fecha_fin
    
    @property
    def habitacion(self):
        return self.__habitacion
    
    @property
    def huespedes(self) -> List[str]:
        return self._huespedes.copy()
    
    def __str__(self):
        noches = self.__calcular_noches()
        return (f"Reserva {self.__codigo_reserva} | Hab. {self.__habitacion.numero} | "
                f"{self.__fecha_inicio} al {self.__fecha_fin} ({noches} noches)")


class ReservaIndividual(Reserva):
    """Reserva para un solo huésped (HERENCIA)"""
    
    def __init__(self, codigo_reserva: str, fecha_inicio: str, fecha_fin: str, 
                 habitacion, huesped: str, proposito_visita: str, 
                 incluye_desayuno: bool = True):
        super().__init__(codigo_reserva, fecha_inicio, fecha_fin, habitacion)
        self.huesped = huesped
        self.proposito_visita = proposito_visita
        self.incluye_desayuno = incluye_desayuno
        self._huespedes.append(huesped)  # Agregar huésped principal
    
    def calcular_costo_total(self) -> float:
        """Calcula costo total con descuento 0% para individual"""
        noches = self._Reserva__calcular_noches()
        tarifa_noche = self.habitacion.calcular_tarifa_noche()
        costo_base = tarifa_noche * noches
        
        # Agregar costo de desayuno si está incluido
        if self.incluye_desayuno:
            costo_base += 25000 * noches  # $25,000 por desayuno por noche
        
        # Aplicar descuento según propósito
        if self.proposito_visita.lower() == "negocios":
            costo_base *= 0.95  # 5% descuento para negocios
        
        return costo_base
    
    def politica_cancelacion(self) -> str:
        """Política de cancelación: 48 horas"""
        return "Cancelación gratis hasta 48 horas antes. 50% de penalidad dentro de las 48 horas."
    
    def __str__(self):
        return (f"Individual: {self.codigo_reserva} | Huésped: {self.huesped} | "
                f"Propósito: {self.proposito_visita}")


class ReservaGrupal(Reserva):
    """Reserva para grupos (HERENCIA)"""
    
    def __init__(self, codigo_reserva: str, fecha_inicio: str, fecha_fin: str, 
                 habitaciones: List, grupo_nombre: str, num_personas: int, 
                 descuento_grupo: float = 15.0, coordinador: str = ""):
        # Para grupos, la habitación principal es la primera
        super().__init__(codigo_reserva, fecha_inicio, fecha_fin, habitaciones[0])
        self.habitaciones = habitaciones  # Lista de habitaciones
        self.grupo_nombre = grupo_nombre
        self.num_personas = num_personas
        self.descuento_grupo = descuento_grupo
        self.coordinador = coordinador
        self._huespedes.append(f"Grupo: {grupo_nombre}")
    
    def calcular_costo_total(self) -> float:
        """Calcula costo total con descuento de grupo (15% por defecto)"""
        noches = self._Reserva__calcular_noches()
        
        # Sumar costos de todas las habitaciones
        costo_total = 0
        for habitacion in self.habitaciones:
            costo_total += habitacion.calcular_tarifa_noche() * noches
        
        # Aplicar descuento de grupo
        costo_total *= (1 - self.descuento_grupo / 100)
        
        # Agregar servicio de coordinador si existe
        if self.coordinador:
            costo_total += 100000  # $100,000 por coordinador
        
        return costo_total
    
    def politica_cancelacion(self) -> str:
        """Política de cancelación: 1 semana"""
        return "Cancelación gratis hasta 1 semana antes. 30% de penalidad dentro de la semana."
    
    def agregar_habitacion(self, habitacion):
        """Agrega una habitación al grupo"""
        self.habitaciones.append(habitacion)
    
    def __str__(self):
        return (f"Grupal: {self.codigo_reserva} | Grupo: {self.grupo_nombre} | "
                f"{len(self.habitaciones)} habitaciones | {self.num_personas} personas")


class ReservaCorporativa(Reserva):
    """Reserva para empresas (HERENCIA)"""
    
    def __init__(self, codigo_reserva: str, fecha_inicio: str, fecha_fin: str, 
                 habitacion, huespedes: List[str], empresa: str, 
                 convenio: bool = True, facturacion_directa: bool = True):
        super().__init__(codigo_reserva, fecha_inicio, fecha_fin, habitacion)
        self.empresa = empresa
        self.convenio = convenio
        self.facturacion_directa = facturacion_directa
        
        # Agregar todos los huéspedes
        for huesped in huespedes:
            self.agregar_huesped(huesped)
    
    def calcular_costo_total(self) -> float:
        """Calcula costo total con descuento corporativo (20%)"""
        noches = self._Reserva__calcular_noches()
        tarifa_noche = self.habitacion.calcular_tarifa_noche()
        costo_base = tarifa_noche * noches
        
        # Aplicar descuento por convenio
        if self.convenio:
            costo_base *= 0.80  # 20% descuento
        
        return costo_base
    
    def politica_cancelacion(self) -> str:
        """Política de cancelación flexible"""
        return "Cancelación flexible según contrato. Generalmente sin penalidad con 3 días de anticipación."
    
    def __str__(self):
        return (f"Corporativa: {self.codigo_reserva} | Empresa: {self.empresa} | "
                f"Convenio: {'Sí' if self.convenio else 'No'} | "
                f"Facturación directa: {'Sí' if self.facturacion_directa else 'No'}")


class PaqueteTuristico(Reserva):
    """Paquete turístico todo incluido (HERENCIA)"""
    
    def __init__(self, codigo_reserva: str, fecha_inicio: str, fecha_fin: str, 
                 habitacion, huespedes: List[str], tour_incluido: str, 
                 transporte: bool = True, num_comidas: int = 3, guia_turistica: bool = True):
        super().__init__(codigo_reserva, fecha_inicio, fecha_fin, habitacion)
        self.tour_incluido = tour_incluido
        self.transporte = transporte
        self.num_comidas = num_comidas  # Comidas por día
        self.guia_turistica = guia_turistica
        
        # Agregar todos los huéspedes
        for huesped in huespedes:
            self.agregar_huesped(huesped)
    
    def calcular_costo_total(self) -> float:
        """Calcula costo total del paquete completo"""
        noches = self._Reserva__calcular_noches()
        tarifa_noche = self.habitacion.calcular_tarifa_noche()
        
        # Costo base de habitación
        costo_total = tarifa_noche * noches
        
        # Agregar costos del paquete
        # Tour incluido
        costo_total += 150000  # $150,000 por tour
        
        # Transporte
        if self.transporte:
            costo_total += 80000 * noches  # $80,000 por día de transporte
        
        # Comidas
        costo_total += 35000 * self.num_comidas * noches  # $35,000 por comida
        
        # Guía turística
        if self.guia_turistica:
            costo_total += 120000 * noches  # $120,000 por día de guía
        
        # Descuento por paquete completo (10%)
        costo_total *= 0.90
        
        return costo_total
    
    def politica_cancelacion(self) -> str:
        """Política de cancelación: no reembolsable"""
        return "No reembolsable después de la confirmación. Posible cambio de fechas con cargo del 25%."
    
    def __str__(self):
        servicios = []
        if self.transporte: servicios.append("Transporte")
        if self.guia_turistica: servicios.append("Guía")
        
        return (f"Paquete: {self.codigo_reserva} | Tour: {self.tour_incluido} | "
                f"Comidas/día: {self.num_comidas} | Servicios: {', '.join(servicios)}")