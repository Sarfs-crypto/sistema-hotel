from abc import ABC, abstractmethod
from datetime import datetime
from typing import List


class ServicioHotel(ABC):
    """Clase abstracta base para todos los servicios (ABSTRACCION)"""
    
    def __init__(self, codigo_servicio: str, nombre: str, habitacion_solicitante: int):
        # Atributos privados (ENCAPSULAMIENTO)
        self.__codigo_servicio = codigo_servicio
        self.__nombre = nombre
        self.__habitacion_solicitante = habitacion_solicitante
        self.__fecha_solicitud = None
        
        # Atributo protegido
        self._horario_disponible = "07:00-22:00"  # Horario por defecto
    
    @abstractmethod
    def calcular_costo(self) -> float:
        """Calcula costo del servicio (POLIMORFISMO)"""
        pass
    
    @abstractmethod
    def tiempo_servicio(self) -> str:
        """Retorna tiempo estimado del servicio (POLIMORFISMO)"""
        pass
    
    def registrar_solicitud(self, fecha_hora: str = None):
        """Registra la fecha y hora de la solicitud"""
        if fecha_hora:
            self.__fecha_solicitud = fecha_hora
        else:
            self.__fecha_solicitud = datetime.now().strftime("%Y-%m-%d %H:%M")
    
    def __aplicar_recargo_nocturno(self, costo_base: float, hora: str) -> float:
        """Aplica recargo por servicio nocturno (ENCAPSULAMIENTO)"""
        try:
            hora_num = int(hora.split(':')[0])
            # Recargo del 30% entre 22:00 y 06:00
            if hora_num >= 22 or hora_num < 6:
                return costo_base * 1.30
        except:
            pass
        return costo_base
    
    @property
    def codigo_servicio(self) -> str:
        return self.__codigo_servicio
    
    @property
    def nombre(self) -> str:
        return self.__nombre
    
    @property
    def habitacion_solicitante(self) -> int:
        return self.__habitacion_solicitante
    
    @property
    def fecha_solicitud(self) -> str:
        return self.__fecha_solicitud or "No registrada"
    
    @property
    def horario_disponible(self) -> str:
        return self._horario_disponible
    
    def __str__(self):
        return f"Servicio {self.__codigo_servicio}: {self.__nombre} - Hab. {self.__habitacion_solicitante}"


class ServicioRestaurante(ServicioHotel):
    """Servicio de restaurante (HERENCIA)"""
    
    def __init__(self, codigo_servicio: str, nombre: str, habitacion_solicitante: int,
                 num_personas: int, tipo_menu: str, ubicacion_servir: str):
        super().__init__(codigo_servicio, nombre, habitacion_solicitante)
        self.num_personas = num_personas
        self.tipo_menu = tipo_menu  # "básico", "ejecutivo", "premium", "gourmet"
        self.ubicacion_servir = ubicacion_servir  # "restaurante", "habitacion", "terraza"
        self._horario_disponible = "06:00-23:00"
    
    def calcular_costo(self) -> float:
        """Calcula costo según tipo de menú y ubicación"""
        # Costos base por tipo de menú por persona
        costos_menu = {
            "básico": 35000,
            "ejecutivo": 55000,
            "premium": 85000,
            "gourmet": 120000
        }
        
        costo_base = costos_menu.get(self.tipo_menu.lower(), 35000) * self.num_personas
        
        # Recargo por servicio en habitación
        if self.ubicacion_servir == "habitacion":
            costo_base *= 1.15  # 15% recargo
        
        # Recargo por servicio en terraza
        elif self.ubicacion_servir == "terraza":
            costo_base *= 1.10  # 10% recargo
        
        # Aplicar recargo nocturno si aplica
        if self.fecha_solicitud != "No registrada":
            try:
                hora = self.fecha_solicitud.split(' ')[1][:5]
                costo_base = self._ServicioHotel__aplicar_recargo_nocturno(costo_base, hora)
            except:
                pass
        
        return costo_base
    
    def tiempo_servicio(self) -> str:
        """Tiempo estimado de servicio"""
        tiempos = {
            "básico": "45 minutos",
            "ejecutivo": "1 hora",
            "premium": "1.5 horas",
            "gourmet": "2 horas"
        }
        return tiempos.get(self.tipo_menu.lower(), "1 hora")
    
    def __str__(self):
        return (f"Restaurante: {self.nombre} | {self.num_personas} personas | "
                f"Menú: {self.tipo_menu} | Ubicación: {self.ubicacion_servir}")


class ServicioSpa(ServicioHotel):
    """Servicio de spa y bienestar (HERENCIA)"""
    
    def __init__(self, codigo_servicio: str, nombre: str, habitacion_solicitante: int,
                 tratamiento: str, duracion_minutos: int, terapeuta: str = ""):
        super().__init__(codigo_servicio, nombre, habitacion_solicitante)
        self.tratamiento = tratamiento
        self.duracion_minutos = duracion_minutos
        self.terapeuta = terapeuta
        self._horario_disponible = "08:00-21:00"
    
    def calcular_costo(self) -> float:
        """Calcula costo según tratamiento y duración"""
        # Costos base por tipo de tratamiento (por 60 minutos)
        costos_tratamiento = {
            "masaje relajante": 80000,
            "masaje terapéutico": 95000,
            "facial rejuvenecedor": 120000,
            "masaje sueco": 110000,
            "masaje con piedras": 150000,
            "tratamiento corporal": 180000,
            "day spa": 250000
        }
        
        costo_base = costos_tratamiento.get(self.tratamiento.lower(), 80000)
        
        # Ajustar por duración
        costo_base = (costo_base / 60) * self.duracion_minutos
        
        # Recargo por terapeuta especializado
        if self.terapeuta:
            costo_base *= 1.20  # 20% recargo
        
        return costo_base
    
    def tiempo_servicio(self) -> str:
        """Tiempo estimado del tratamiento"""
        return f"{self.duracion_minutos} minutos"
    
    def __str__(self):
        return (f"Spa: {self.nombre} | Tratamiento: {self.tratamiento} | "
                f"Duración: {self.duracion_minutos} min | "
                f"Terapeuta: {self.terapeuta if self.terapeuta else 'Por asignar'}")


class ServicioLavanderia(ServicioHotel):
    """Servicio de lavandería (HERENCIA)"""
    
    def __init__(self, codigo_servicio: str, nombre: str, habitacion_solicitante: int,
                 num_prendas: int, tipo_servicio: str, urgencia: bool = False):
        super().__init__(codigo_servicio, nombre, habitacion_solicitante)
        self.num_prendas = num_prendas
        self.tipo_servicio = tipo_servicio  # "lavado", "planchado", "lavado y planchado", "seco"
        self.urgencia = urgencia
        self._horario_disponible = "24 horas"
    
    def calcular_costo(self) -> float:
        """Calcula costo según tipo de servicio y urgencia"""
        # Costos por prenda según tipo de servicio
        costos_por_prenda = {
            "lavado": 5000,
            "planchado": 3000,
            "lavado y planchado": 7000,
            "seco": 12000
        }
        
        costo_por_prenda = costos_por_prenda.get(self.tipo_servicio.lower(), 5000)
        costo_base = costo_por_prenda * self.num_prendas
        
        # Recargo por servicio urgente (50%)
        if self.urgencia:
            costo_base *= 1.50
        
        return costo_base
    
    def tiempo_servicio(self) -> str:
        """Tiempo estimado del servicio"""
        if self.urgencia:
            return "4-6 horas"
        
        tiempos = {
            "lavado": "24 horas",
            "planchado": "12 horas",
            "lavado y planchado": "24 horas",
            "seco": "48 horas"
        }
        return tiempos.get(self.tipo_servicio.lower(), "24 horas")
    
    def __str__(self):
        urgencia_str = "EXPRESS" if self.urgencia else "Normal"
        return (f"Lavandería: {self.nombre} | {self.num_prendas} prendas | "
                f"Servicio: {self.tipo_servicio} | {urgencia_str}")


class RoomService(ServicioHotel):
    """Servicio de habitaciones (HERENCIA)"""
    
    def __init__(self, codigo_servicio: str, nombre: str, habitacion_solicitante: int,
                 items_pedido: List[str], hora_entrega: str, piso: int):
        super().__init__(codigo_servicio, nombre, habitacion_solicitante)
        self.items_pedido = items_pedido
        self.hora_entrega = hora_entrega
        self.piso = piso
        self._horario_disponible = "24 horas"
    
    def calcular_costo(self) -> float:
        """Calcula costo según items del pedido"""
        # Precios base por item
        precios_items = {
            "café": 8000,
            "té": 7000,
            "jugo": 9000,
            "sandwich": 15000,
            "ensalada": 18000,
            "sopa": 12000,
            "postre": 10000,
            "fruta": 8000,
            "pan": 5000,
            "agua": 5000,
            "refresco": 7000,
            "cerveza": 12000,
            "vino": 25000,
            "whisky": 35000
        }
        
        costo_base = 0
        for item in self.items_pedido:
            item_lower = item.lower().strip()
            costo_base += precios_items.get(item_lower, 10000)
        
        # Costo de delivery fijo
        costo_base += 5000
        
        # Recargo por piso alto (a partir del 5to piso)
        if self.piso >= 5:
            costo_base += 2000
        
        # Aplicar recargo nocturno
        try:
            hora = self.hora_entrega
            costo_base = self._ServicioHotel__aplicar_recargo_nocturno(costo_base, hora)
        except:
            pass
        
        return costo_base
    
    def tiempo_servicio(self) -> str:
        """Tiempo estimado de entrega"""
        return "15-30 minutos"
    
    def __str__(self):
        items_str = ", ".join(self.items_pedido[:3])
        if len(self.items_pedido) > 3:
            items_str += f" y {len(self.items_pedido) - 3} más"
        
        return (f"Room Service: {self.nombre} | Items: {items_str} | "
                f"Hora: {self.hora_entrega} | Piso: {self.piso}")
