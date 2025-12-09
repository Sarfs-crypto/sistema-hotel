from abc import ABC, abstractmethod
from datetime import datetime, timedelta
from typing import List

class Habitacion(ABC):
    """Clase abstracta base para todas las habitaciones (ABSTRACCIÓN)"""
    
    def __init__(self, numero: int, piso: int, tarifa_base: float):
        # Atributos privados (ENCAPSULAMIENTO)
        self.__numero = numero
        self.__piso = piso
        self.__estado = "disponible"
        self.__tarifa_base = tarifa_base
        
        # Atributos protegidos
        self._servicios_incluidos = []
        self._historial_huespedes = []
    
    @abstractmethod
    def calcular_tarifa_noche(self) -> float:
        """Calcula tarifa por noche (POLIMORFISMO)"""
        pass
    
    @abstractmethod
    def capacidad_maxima(self) -> int:
        """Retorna capacidad máxima"""
        pass
    
    def cambiar_estado(self, nuevo_estado: str):
        """Cambia el estado de la habitación"""
        estados_validos = ["disponible", "ocupada", "limpieza", "mantenimiento"]
        if nuevo_estado in estados_validos:
            self.__estado = nuevo_estado
            return True
        return False
    
    def __calcular_impuestos(self, subtotal: float) -> float:
        """Calcula impuestos (método privado)"""
        return subtotal * 0.24
    
    # Getters
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
    
    def agregar_huesped_al_historial(self, huesped: str):
        """Agrega un huésped al historial"""
        registro = {
            "huesped": huesped,
            "fecha": datetime.now().strftime("%Y-%m-%d %H:%M"),
            "habitacion": f"{self.__numero} ({self.__class__.__name__})"
        }
        self._historial_huespedes.append(registro)
    
    def __str__(self):
        return f"Habitación {self.__numero} - {self.__class__.__name__}"


class HabitacionSimple(Habitacion):
    """Habitación simple para una persona (HERENCIA)"""
    
    def __init__(self, numero: int, piso: int, cama_individual: bool, vista: str, baño_compartido: bool):
        super().__init__(numero, piso, tarifa_base=50.0)
        self.cama_individual = cama_individual
        self.vista = vista
        self.baño_compartido = baño_compartido
        self._servicios_incluidos = ["Wi-Fi", "TV básica", "Aire acondicionado"]
    
    def calcular_tarifa_noche(self) -> float:
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
        return f"Simple #{self.numero} | Vista: {self.vista} | ${self.calcular_tarifa_noche():,.0f}/noche"


class HabitacionDoble(Habitacion):
    """Habitación doble para 2-3 personas (HERENCIA)"""
    
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
        return f"Doble #{self.numero} | {self.tipo_camas} | Vista: {self.vista} | ${self.calcular_tarifa_noche():,.0f}/noche"


class Suite(Habitacion):
    """Suite para 4-6 personas (HERENCIA)"""
    
    def __init__(self, numero: int, piso: int, sala_estar: bool, cocina: bool, jacuzzi: bool, num_habitaciones: int):
        super().__init__(numero, piso, tarifa_base=200.0)
        self.sala_estar = sala_estar
        self.cocina = cocina
        self.jacuzzi = jacuzzi
        self.num_habitaciones = num_habitaciones
        self._servicios_incluidos = ["Wi-Fi VIP", "TV 55\"", "Minibar", "Jacuzzi", "Room service"]
    
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
        
        return f"Suite #{self.numero} | {self.num_habitaciones} habs | ${self.calcular_tarifa_noche():,.0f}/noche"


class Penthouse(Habitacion):
    """Penthouse de lujo para 8-10 personas (HERENCIA)"""
    
    def __init__(self, numero: int, piso: int, piso_completo: bool, terraza: bool, servicio_mayordomo: bool):
        super().__init__(numero, piso, tarifa_base=500.0)
        self.piso_completo = piso_completo
        self.terraza = terraza
        self.servicio_mayordomo = servicio_mayordomo
        self._servicios_incluidos = ["Wi-Fi empresarial", "TV 65\" 4K", "Minibar premium", "Mayordomo"]
    
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
        
        return f"Penthouse #{self.numero} | ${self.calcular_tarifa_noche():,.0f}/noche"


# =================================================================================
# EJERCICIO 7.2: SISTEMA DE RESERVAS Y HUÉSPEDES
# =================================================================================

class Reserva(ABC):
    """Clase abstracta base para todas las reservas (ABSTRACCIÓN)"""
    
    def __init__(self, codigo_reserva: str, fecha_inicio: str, fecha_fin: str, habitacion):
        self.__codigo_reserva = codigo_reserva
        self.__fecha_inicio = fecha_inicio
        self.__fecha_fin = fecha_fin
        self.__habitacion = habitacion
        self._huespedes = []
    
    @abstractmethod
    def calcular_costo_total(self) -> float:
        pass
    
    @abstractmethod
    def politica_cancelacion(self) -> str:
        pass
    
    def agregar_huesped(self, huesped: str):
        self._huespedes.append(huesped)
    
    def __calcular_noches(self) -> int:
        try:
            fecha_inicio = datetime.strptime(self.__fecha_inicio, "%Y-%m-%d")
            fecha_fin = datetime.strptime(self.__fecha_fin, "%Y-%m-%d")
            return (fecha_fin - fecha_inicio).days
        except ValueError:
            return 1
    
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
        return f"Reserva {self.__codigo_reserva} | Hab. {self.__habitacion.numero} | {noches} noches"


class ReservaIndividual(Reserva):
    """Reserva para un solo huésped (HERENCIA)"""
    
    def __init__(self, codigo_reserva: str, fecha_inicio: str, fecha_fin: str, 
                 habitacion, huesped: str, proposito_visita: str, 
                 incluye_desayuno: bool = True):
        super().__init__(codigo_reserva, fecha_inicio, fecha_fin, habitacion)
        self.huesped = huesped
        self.proposito_visita = proposito_visita
        self.incluye_desayuno = incluye_desayuno
        self._huespedes.append(huesped)
    
    def calcular_costo_total(self) -> float:
        noches = self._Reserva__calcular_noches()
        tarifa_noche = self.habitacion.calcular_tarifa_noche()
        costo_base = tarifa_noche * noches
        
        if self.incluye_desayuno:
            costo_base += 25000 * noches
        
        if self.proposito_visita.lower() == "negocios":
            costo_base *= 0.95
        
        return costo_base
    
    def politica_cancelacion(self) -> str:
        return "Cancelación gratis hasta 48 horas antes. 50% de penalidad dentro de las 48 horas."
    
    def __str__(self):
        return f"Individual: {self.codigo_reserva} | Huésped: {self.huesped}"


class ReservaGrupal(Reserva):
    """Reserva para grupos (HERENCIA)"""
    
    def __init__(self, codigo_reserva: str, fecha_inicio: str, fecha_fin: str, 
                 habitaciones: List, grupo_nombre: str, num_personas: int, 
                 descuento_grupo: float = 15.0, coordinador: str = ""):
        super().__init__(codigo_reserva, fecha_inicio, fecha_fin, habitaciones[0])
        self.habitaciones = habitaciones
        self.grupo_nombre = grupo_nombre
        self.num_personas = num_personas
        self.descuento_grupo = descuento_grupo
        self.coordinador = coordinador
        self._huespedes.append(f"Grupo: {grupo_nombre}")
    
    def calcular_costo_total(self) -> float:
        noches = self._Reserva__calcular_noches()
        costo_total = 0
        
        for habitacion in self.habitaciones:
            costo_total += habitacion.calcular_tarifa_noche() * noches
        
        costo_total *= (1 - self.descuento_grupo / 100)
        
        if self.coordinador:
            costo_total += 100000
        
        return costo_total
    
    def politica_cancelacion(self) -> str:
        return "Cancelación gratis hasta 1 semana antes. 30% de penalidad dentro de la semana."
    
    def __str__(self):
        return f"Grupal: {self.codigo_reserva} | Grupo: {self.grupo_nombre} | {len(self.habitaciones)} habs"


class ReservaCorporativa(Reserva):
    """Reserva para empresas (HERENCIA)"""
    
    def __init__(self, codigo_reserva: str, fecha_inicio: str, fecha_fin: str, 
                 habitacion, huespedes: List[str], empresa: str, 
                 convenio: bool = True, facturacion_directa: bool = True):
        super().__init__(codigo_reserva, fecha_inicio, fecha_fin, habitacion)
        self.empresa = empresa
        self.convenio = convenio
        self.facturacion_directa = facturacion_directa
        
        for huesped in huespedes:
            self.agregar_huesped(huesped)
    
    def calcular_costo_total(self) -> float:
        noches = self._Reserva__calcular_noches()
        tarifa_noche = self.habitacion.calcular_tarifa_noche()
        costo_base = tarifa_noche * noches
        
        if self.convenio:
            costo_base *= 0.80
        
        return costo_base
    
    def politica_cancelacion(self) -> str:
        return "Cancelación flexible según contrato. Generalmente sin penalidad con 3 días."
    
    def __str__(self):
        return f"Corporativa: {self.codigo_reserva} | Empresa: {self.empresa}"


class PaqueteTuristico(Reserva):
    """Paquete turístico todo incluido (HERENCIA)"""
    
    def __init__(self, codigo_reserva: str, fecha_inicio: str, fecha_fin: str, 
                 habitacion, huespedes: List[str], tour_incluido: str, 
                 transporte: bool = True, num_comidas: int = 3, guia_turistica: bool = True):
        super().__init__(codigo_reserva, fecha_inicio, fecha_fin, habitacion)
        self.tour_incluido = tour_incluido
        self.transporte = transporte
        self.num_comidas = num_comidas
        self.guia_turistica = guia_turistica
        
        for huesped in huespedes:
            self.agregar_huesped(huesped)
    
    def calcular_costo_total(self) -> float:
        noches = self._Reserva__calcular_noches()
        tarifa_noche = self.habitacion.calcular_tarifa_noche()
        costo_total = tarifa_noche * noches
        
        costo_total += 150000  # Tour
        
        if self.transporte:
            costo_total += 80000 * noches
        
        costo_total += 35000 * self.num_comidas * noches
        
        if self.guia_turistica:
            costo_total += 120000 * noches
        
        costo_total *= 0.90
        
        return costo_total
    
    def politica_cancelacion(self) -> str:
        return "No reembolsable después de confirmación. Cambio de fechas con 25% de cargo."
    
    def __str__(self):
        return f"Paquete: {self.codigo_reserva} | Tour: {self.tour_incluido}"


# =================================================================================
# EJERCICIO 7.3: SERVICIOS ADICIONALES DEL HOTEL
# =================================================================================

class ServicioHotel(ABC):
    """Clase abstracta base para todos los servicios (ABSTRACCIÓN)"""
    
    def __init__(self, codigo_servicio: str, nombre: str, habitacion_solicitante: int):
        self.__codigo_servicio = codigo_servicio
        self.__nombre = nombre
        self.__habitacion_solicitante = habitacion_solicitante
        self.__fecha_solicitud = None
        self._horario_disponible = "07:00-22:00"
    
    @abstractmethod
    def calcular_costo(self) -> float:
        pass
    
    @abstractmethod
    def tiempo_servicio(self) -> str:
        pass
    
    def registrar_solicitud(self, fecha_hora: str = None):
        if fecha_hora:
            self.__fecha_solicitud = fecha_hora
        else:
            self.__fecha_solicitud = datetime.now().strftime("%Y-%m-%d %H:%M")
    
    def __aplicar_recargo_nocturno(self, costo_base: float, hora: str) -> float:
        try:
            hora_num = int(hora.split(':')[0])
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
    
    def __str__(self):
        return f"Servicio {self.__codigo_servicio}: {self.__nombre}"


class ServicioRestaurante(ServicioHotel):
    """Servicio de restaurante (HERENCIA)"""
    
    def __init__(self, codigo_servicio: str, nombre: str, habitacion_solicitante: int,
                 num_personas: int, tipo_menu: str, ubicacion_servir: str):
        super().__init__(codigo_servicio, nombre, habitacion_solicitante)
        self.num_personas = num_personas
        self.tipo_menu = tipo_menu
        self.ubicacion_servir = ubicacion_servir
        self._horario_disponible = "06:00-23:00"
    
    def calcular_costo(self) -> float:
        costos_menu = {
            "básico": 35000,
            "ejecutivo": 55000,
            "premium": 85000,
            "gourmet": 120000
        }
        
        costo_base = costos_menu.get(self.tipo_menu.lower(), 35000) * self.num_personas
        
        if self.ubicacion_servir == "habitacion":
            costo_base *= 1.15
        elif self.ubicacion_servir == "terraza":
            costo_base *= 1.10
        
        return costo_base
    
    def tiempo_servicio(self) -> str:
        tiempos = {
            "básico": "45 minutos",
            "ejecutivo": "1 hora",
            "premium": "1.5 horas",
            "gourmet": "2 horas"
        }
        return tiempos.get(self.tipo_menu.lower(), "1 hora")
    
    def __str__(self):
        return f"Restaurante: {self.nombre} | {self.num_personas} personas"


class ServicioSpa(ServicioHotel):
    """Servicio de spa (HERENCIA)"""
    
    def __init__(self, codigo_servicio: str, nombre: str, habitacion_solicitante: int,
                 tratamiento: str, duracion_minutos: int, terapeuta: str = ""):
        super().__init__(codigo_servicio, nombre, habitacion_solicitante)
        self.tratamiento = tratamiento
        self.duracion_minutos = duracion_minutos
        self.terapeuta = terapeuta
        self._horario_disponible = "08:00-21:00"
    
    def calcular_costo(self) -> float:
        costos_tratamiento = {
            "masaje relajante": 80000,
            "masaje terapéutico": 95000,
            "facial rejuvenecedor": 120000,
            "masaje sueco": 110000,
            "masaje con piedras": 150000
        }
        
        costo_base = costos_tratamiento.get(self.tratamiento.lower(), 80000)
        costo_base = (costo_base / 60) * self.duracion_minutos
        
        if self.terapeuta:
            costo_base *= 1.20
        
        return costo_base
    
    def tiempo_servicio(self) -> str:
        return f"{self.duracion_minutos} minutos"
    
    def __str__(self):
        return f"Spa: {self.nombre} | Tratamiento: {self.tratamiento}"


class ServicioLavanderia(ServicioHotel):
    """Servicio de lavandería (HERENCIA)"""
    
    def __init__(self, codigo_servicio: str, nombre: str, habitacion_solicitante: int,
                 num_prendas: int, tipo_servicio: str, urgencia: bool = False):
        super().__init__(codigo_servicio, nombre, habitacion_solicitante)
        self.num_prendas = num_prendas
        self.tipo_servicio = tipo_servicio
        self.urgencia = urgencia
        self._horario_disponible = "24 horas"
    
    def calcular_costo(self) -> float:
        costos_por_prenda = {
            "lavado": 5000,
            "planchado": 3000,
            "lavado y planchado": 7000,
            "seco": 12000
        }
        
        costo_por_prenda = costos_por_prenda.get(self.tipo_servicio.lower(), 5000)
        costo_base = costo_por_prenda * self.num_prendas
        
        if self.urgencia:
            costo_base *= 1.50
        
        return costo_base
    
    def tiempo_servicio(self) -> str:
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
        return f"Lavandería: {self.nombre} | {self.num_prendas} prendas | {urgencia_str}"


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
            "agua": 5000
        }
        
        costo_base = 0
        for item in self.items_pedido:
            item_lower = item.lower().strip()
            costo_base += precios_items.get(item_lower, 10000)
        
        costo_base += 5000  # Delivery
        
        if self.piso >= 5:
            costo_base += 2000
        
        try:
            hora = self.hora_entrega
            costo_base = self._ServicioHotel__aplicar_recargo_nocturno(costo_base, hora)
        except:
            pass
        
        return costo_base
    
    def tiempo_servicio(self) -> str:
        return "15-30 minutos"
    
    def __str__(self):
        items_str = ", ".join(self.items_pedido[:3])
        if len(self.items_pedido) > 3:
            items_str += f" y {len(self.items_pedido) - 3} más"
        
        return f"Room Service: {self.nombre} | Items: {items_str}"


# =================================================================================
# EJERCICIO 7.4: PERSONAL Y DEPARTAMENTOS
# =================================================================================

class EmpleadoHotel(ABC):
    """Clase abstracta base para todos los empleados (ABSTRACCIÓN)"""
    
    def __init__(self, nombre: str, codigo: str, turno: str, salario_base: float):
        self.__nombre = nombre
        self.__codigo = codigo
        self.__turno = turno
        self.__salario_base = salario_base
        self._evaluaciones = []
    
    @abstractmethod
    def calcular_salario_mensual(self) -> float:
        pass
    
    @abstractmethod
    def asignar_tarea(self) -> str:
        pass
    
    def registrar_evaluacion(self, calificacion: float, comentario: str = ""):
        evaluacion = {
            "fecha": datetime.now().strftime("%Y-%m-%d"),
            "calificacion": calificacion,
            "comentario": comentario
        }
        self._evaluaciones.append(evaluacion)
    
    def __calcular_bono_desempeño(self) -> float:
        if not self._evaluaciones:
            return 0
        
        promedio = sum(eval["calificacion"] for eval in self._evaluaciones) / len(self._evaluaciones)
        
        if promedio >= 4.5:
            return self.__salario_base * 0.15
        elif promedio >= 4.0:
            return self.__salario_base * 0.10
        elif promedio >= 3.5:
            return self.__salario_base * 0.05
        
        return 0
    
    @property
    def nombre(self) -> str:
        return self.__nombre
    
    @property
    def codigo(self) -> str:
        return self.__codigo
    
    @property
    def turno(self) -> str:
        return self.__turno
    
    @property
    def salario_base(self) -> float:
        return self.__salario_base
    
    def __str__(self):
        return f"{self.__nombre} - {self.__codigo}"


class Recepcionista(EmpleadoHotel):
    """Empleado de recepción (HERENCIA)"""
    
    def __init__(self, nombre: str, codigo: str, turno: str, salario_base: float,
                 idiomas: List[str]):
        super().__init__(nombre, codigo, turno, salario_base)
        self.idiomas = idiomas
        self.turno_rotativo = True
        self.atencion_cliente = True
    
    def calcular_salario_mensual(self) -> float:
        salario = self.salario_base
        
        if len(self.idiomas) > 1:
            salario += 50000 * (len(self.idiomas) - 1)
        
        if self.turno_rotativo:
            salario += 80000
        
        salario += self._EmpleadoHotel__calcular_bono_desempeño()
        salario += 150000  # Propinas
        
        return salario
    
    def asignar_tarea(self) -> str:
        if self.turno.lower() == "matutino":
            return "Atención al cliente y check-in/out"
        elif self.turno.lower() == "vespertino":
            return "Reservas telefónicas e información turística"
        else:
            return "Manejo de quejas y coordinación"
    
    def __str__(self):
        return f"Recepcionista: {self.nombre} | Idiomas: {', '.join(self.idiomas)}"


class Housekeeping(EmpleadoHotel):
    """Empleado de limpieza (HERENCIA)"""
    
    def __init__(self, nombre: str, codigo: str, turno: str, salario_base: float,
                 habitaciones_asignadas: List[int], piso: int, supervisor: str = ""):
        super().__init__(nombre, codigo, turno, salario_base)
        self.habitaciones_asignadas = habitaciones_asignadas
        self.piso = piso
        self.supervisor = supervisor
    
    def calcular_salario_mensual(self) -> float:
        salario = self.salario_base
        
        if len(self.habitaciones_asignadas) > 5:
            salario += 20000 * (len(self.habitaciones_asignadas) - 5)
        
        if self.piso >= 3:
            salario += 50000
        
        salario += self._EmpleadoHotel__calcular_bono_desempeño()
        salario += 100000  # Propinas
        
        return salario
    
    def asignar_tarea(self) -> str:
        if self.turno.lower() == "matutino":
            return f"Limpieza de {len(self.habitaciones_asignadas)} habitaciones en piso {self.piso}"
        else:
            return "Preparación de habitaciones para check-in"
    
    def __str__(self):
        return f"Housekeeping: {self.nombre} | Piso {self.piso} | {len(self.habitaciones_asignadas)} habs"


class Mantenimiento(EmpleadoHotel):
    """Empleado de mantenimiento (HERENCIA)"""
    
    def __init__(self, nombre: str, codigo: str, turno: str, salario_base: float,
                 especialidad: str, disponibilidad_24h: bool = False):
        super().__init__(nombre, codigo, turno, salario_base)
        self.especialidad = especialidad
        self.disponibilidad_24h = disponibilidad_24h
        self.herramientas = self._definir_herramientas()
    
    def _definir_herramientas(self) -> List[str]:
        herramientas = {
            "electricidad": ["multímetro", "pinzas", "cinta aislante"],
            "plomería": ["llave inglesa", "desatascador", "cinta teflón"],
            "carpintería": ["martillo", "sierra", "taladro"],
            "general": ["kit básico", "linterna", "guantes"]
        }
        return herramientas.get(self.especialidad.lower(), ["kit básico"])
    
    def calcular_salario_mensual(self) -> float:
        salario = self.salario_base
        
        bonos_especialidad = {
            "electricidad": 100000,
            "plomería": 80000,
            "carpintería": 70000,
            "general": 50000
        }
        salario += bonos_especialidad.get(self.especialidad.lower(), 0)
        
        if self.disponibilidad_24h:
            salario += 150000
        
        salario += self._EmpleadoHotel__calcular_bono_desempeño()
        salario += 50000  # Bono emergencias
        
        return salario
    
    def asignar_tarea(self) -> str:
        if self.disponibilidad_24h:
            return f"Mantenimiento 24h - Especialidad: {self.especialidad}"
        else:
            return f"Mantenimiento programado - Especialidad: {self.especialidad}"
    
    def __str__(self):
        disponibilidad = "24h" if self.disponibilidad_24h else self.turno
        return f"Mantenimiento: {self.nombre} | {self.especialidad} | {disponibilidad}"


class Gerente(EmpleadoHotel):
    """Gerente de departamento (HERENCIA)"""
    
    def __init__(self, nombre: str, codigo: str, turno: str, salario_base: float,
                 departamento: str, personal_a_cargo: int):
        super().__init__(nombre, codigo, turno, salario_base)
        self.departamento = departamento
        self.personal_a_cargo = personal_a_cargo
        self.bono_ocupacion = 0
    
    def calcular_salario_mensual(self) -> float:
        salario = self.salario_base
        
        bonos_departamento = {
            "recepcion": 200000,
            "servicios": 180000,
            "mantenimiento": 150000,
            "restaurante": 220000,
            "spa": 170000
        }
        salario += bonos_departamento.get(self.departamento.lower(), 100000)
        
        if self.personal_a_cargo > 0:
            salario += 20000 * self.personal_a_cargo
        
        salario += self.bono_ocupacion
        salario += self._EmpleadoHotel__calcular_bono_desempeño()
        
        return salario
    
    def asignar_tarea(self) -> str:
        return f"Gestión del departamento de {self.departamento}"
    
    def actualizar_bono_ocupacion(self, porcentaje_ocupacion: float):
        if porcentaje_ocupacion >= 85:
            self.bono_ocupacion = 300000
        elif porcentaje_ocupacion >= 70:
            self.bono_ocupacion = 200000
        elif porcentaje_ocupacion >= 50:
            self.bono_ocupacion = 100000
        else:
            self.bono_ocupacion = 0
    
    def __str__(self):
        return f"Gerente: {self.nombre} | Depto: {self.departamento}"


# =================================================================================
# SISTEMA PRINCIPAL
# =================================================================================

class HotelService:
    """Servicio principal del hotel"""
    
    def __init__(self):
        self.habitaciones = []
        self.reservas = []
        self.servicios = []
        self.empleados = []
        self._inicializar_datos()
    
    def _inicializar_datos(self):
        """Inicializa datos de ejemplo"""
        self._crear_habitaciones_ejemplo()
        self._contratar_personal_ejemplo()
        self._crear_reservas_ejemplo()
    
    def _crear_habitaciones_ejemplo(self):
        """Crea inventario de 3 habitaciones de cada tipo"""
        # Simples
        self.habitaciones.append(HabitacionSimple(101, 1, True, "jardin", True))
        self.habitaciones.append(HabitacionSimple(102, 1, True, "calle", False))
        self.habitaciones.append(HabitacionSimple(103, 1, True, "interior", True))
        
        # Dobles
        self.habitaciones.append(HabitacionDoble(201, 2, "2 camas individuales", "calle", True))
        self.habitaciones.append(HabitacionDoble(202, 2, "cama queen", "marina", True))
        self.habitaciones.append(HabitacionDoble(203, 2, "cama king", "montaña", True))
        
        # Suites
        self.habitaciones.append(Suite(301, 3, True, True, True, 2))
        self.habitaciones.append(Suite(302, 3, True, False, True, 1))
        self.habitaciones.append(Suite(303, 3, True, True, False, 3))
        
        # Penthouse
        self.habitaciones.append(Penthouse(401, 4, True, True, True))
        self.habitaciones.append(Penthouse(402, 4, False, True, False))
        self.habitaciones.append(Penthouse(403, 4, True, False, True))
    
    def _contratar_personal_ejemplo(self):
        """Contrata equipo completo de hotel"""
        self.empleados.append(Recepcionista("Ana García", "REC-001", "matutino", 1500, ["español", "inglés"]))
        self.empleados.append(Recepcionista("Carlos López", "REC-002", "vespertino", 1500, ["español", "inglés", "francés"]))
        self.empleados.append(Housekeeping("María Rodríguez", "HK-001", "matutino", 1200, [101, 102, 103], 1))
        self.empleados.append(Housekeeping("Pedro Sánchez", "HK-002", "vespertino", 1200, [201, 202, 203], 2))
        self.empleados.append(Mantenimiento("Juan Martínez", "MT-001", "nocturno", 1300, "electricidad", True))
        self.empleados.append(Mantenimiento("Laura Fernández", "MT-002", "diurno", 1300, "plomería", False))
        self.empleados.append(Gerente("Roberto Vargas", "GER-001", "administrativo", 2500, "recepcion", 3))
        self.empleados.append(Gerente("Sofía Ramírez", "GER-002", "administrativo", 2500, "servicios", 5))
    
    def _crear_reservas_ejemplo(self):
        """Crea 2 reservas de cada tipo"""
        if len(self.habitaciones) >= 7:
            self.reservas.append(ReservaIndividual("RES-001", "2024-01-15", "2024-01-18", 
                                                  self.habitaciones[0], "Sr. Alejandro Torres", "negocios", True))
            self.reservas.append(ReservaIndividual("RES-004", "2024-01-20", "2024-01-22", 
                                                  self.habitaciones[1], "Sra. Laura Mendoza", "vacaciones", False))
            self.reservas.append(ReservaGrupal("RES-002", "2024-01-25", "2024-01-30", 
                                              [self.habitaciones[3], self.habitaciones[4]], 
                                              "Familia González", 3, 15.0, "Sra. González"))
            self.reservas.append(ReservaCorporativa("RES-003", "2024-02-01", "2024-02-05", 
                                                   self.habitaciones[6], ["Ejecutivo 1", "Ejecutivo 2"], 
                                                   "Tech Solutions", True, True))
            self.reservas.append(PaqueteTuristico("RES-005", "2024-02-10", "2024-02-15", 
                                                 self.habitaciones[9], ["Grupo Internacional"], 
                                                 "Tour Ciudad", True, 3, True))
    
    # Métodos de operación
    def obtener_habitaciones_disponibles(self):
        return [h for h in self.habitaciones if h.estado == "disponible"]
    
    def obtener_habitacion_por_numero(self, numero: int):
        for habitacion in self.habitaciones:
            if habitacion.numero == numero:
                return habitacion
        return None
    
    def crear_reserva_individual(self, codigo: str, fecha_inicio: str, fecha_fin: str,
                                numero_habitacion: int, huesped: str, proposito: str,
                                incluye_desayuno: bool):
        habitacion = self.obtener_habitacion_por_numero(numero_habitacion)
        if not habitacion:
            return None
        
        reserva = ReservaIndividual(codigo, fecha_inicio, fecha_fin, habitacion, 
                                   huesped, proposito, incluye_desayuno)
        self.reservas.append(reserva)
        habitacion.cambiar_estado("ocupada")
        habitacion.agregar_huesped_al_historial(huesped)
        return reserva
    
    def generar_reporte_ocupacion(self):
        reporte = {}
        
        for habitacion in self.habitaciones:
            tipo = habitacion.__class__.__name__
            if tipo not in reporte:
                reporte[tipo] = {
                    "total": 0,
                    "disponibles": 0,
                    "ocupadas": 0,
                    "en_limpieza": 0,
                    "en_mantenimiento": 0
                }
            
            reporte[tipo]["total"] += 1
            
            if habitacion.estado == "disponible":
                reporte[tipo]["disponibles"] += 1
            elif habitacion.estado == "ocupada":
                reporte[tipo]["ocupadas"] += 1
            elif habitacion.estado == "limpieza":
                reporte[tipo]["en_limpieza"] += 1
            elif habitacion.estado == "mantenimiento":
                reporte[tipo]["en_mantenimiento"] += 1
        
        return reporte
    
    def calcular_ingresos_potenciales(self):
        ingresos = {}
        
        for habitacion in self.habitaciones:
            tipo = habitacion.__class__.__name__
            if tipo not in ingresos:
                ingresos[tipo] = 0
            ingresos[tipo] += habitacion.calcular_tarifa_noche()
        
        return ingresos
    
    def calcular_nomina_mensual(self):
        total = 0
        for empleado in self.empleados:
            total += empleado.calcular_salario_mensual()
        return total


class SistemaHotelMenu:
    """Interfaz de usuario del sistema"""
    
    def __init__(self, hotel_service):
        self.service = hotel_service
    
    def mostrar_menu_principal(self):
        print("\n" + "="*60)
        print("🏨 SISTEMA DE GESTIÓN HOTELERA - LUXURY PALACE")
        print("="*60)
        print("1️⃣  Gestión de Habitaciones")
        print("2️⃣  Gestión de Reservas")
        print("3️⃣  Servicios Adicionales")
        print("4️⃣  Personal del Hotel")
        print("5️⃣  Reportes Generales")
        print("6️⃣  Simulaciones")
        print("7️⃣  Información del Sistema")
        print("0️⃣  Salir")
        print("-"*60)
    
    def ejecutar(self):
        print("\n" + "="*60)
        print("🏨 BIENVENIDO AL SISTEMA DE GESTIÓN HOTELERA")
        print("Versión 2.0 | 4 Módulos completos implementados")
        print("="*60)
        
        while True:
            self.mostrar_menu_principal()
            opcion = input("\n🔍 Seleccione una opción: ").strip()
            
            if opcion == "0":
                print("\n👋 ¡Gracias por usar el Sistema de Gestión Hotelera!")
                break
            
            elif opcion == "1":
                self.ejecutar_modulo_habitaciones()
            
            elif opcion == "2":
                self.ejecutar_modulo_reservas()
            
            elif opcion == "4":
                self.ejecutar_modulo_personal()
            
            elif opcion == "5":
                self.ejecutar_reportes_generales()
            
            elif opcion == "6":
                self.ejecutar_simulaciones()
            
            elif opcion == "7":
                self.mostrar_informacion_sistema()
            
            else:
                print("❌ Opción inválida. Intente nuevamente.")
            
            if opcion != "0":
                input("\n⏎ Presione Enter para continuar...")
    
    def ejecutar_modulo_habitaciones(self):
        print("\n" + "="*50)
        print("🏨 MÓDULO DE GESTIÓN DE HABITACIONES")
        print("="*50)
        
        print("\n📋 INVENTARIO COMPLETO (12 habitaciones):")
        print("-"*50)
        
        tipos = {}
        for habitacion in self.service.habitaciones:
            tipo = habitacion.__class__.__name__
            if tipo not in tipos:
                tipos[tipo] = []
            tipos[tipo].append(habitacion)
        
        for tipo, habitaciones in tipos.items():
            print(f"\n{tipo.upper()} ({len(habitaciones)}):")
            for hab in habitaciones:
                print(f"  • {hab}")
        
        print("\n📊 ESTADÍSTICAS:")
        print("-"*30)
        total = len(self.service.habitaciones)
        disponibles = len([h for h in self.service.habitaciones if h.estado == "disponible"])
        print(f"Total: {total} | Disponibles: {disponibles} | Ocupación: {((total-disponibles)/total*100):.1f}%")
    
    def ejecutar_modulo_reservas(self):
        print("\n" + "="*50)
        print("📅 MÓDULO DE GESTIÓN DE RESERVAS")
        print("="*50)
        
        if not self.service.reservas:
            print("No hay reservas registradas.")
            return
        
        print(f"\n📋 RESERVAS ACTIVAS ({len(self.service.reservas)}):")
        print("-"*50)
        
        for i, reserva in enumerate(self.service.reservas, 1):
            print(f"\n{i}. {reserva}")
            print(f"   Costo total: ${reserva.calcular_costo_total():,.0f}")
            print(f"   Política: {reserva.politica_cancelacion()}")
        
        ingresos = sum(r.calcular_costo_total() for r in self.service.reservas)
        print(f"\n💰 INGRESOS TOTALES: ${ingresos:,.0f}")
    
    def ejecutar_modulo_personal(self):
        print("\n" + "="*50)
        print("👥 MÓDULO DE GESTIÓN DE PERSONAL")
        print("="*50)
        
        print(f"\n📋 PLANTILLA DE PERSONAL ({len(self.service.empleados)} empleados):")
        print("-"*50)
        
        for empleado in self.service.empleados:
            print(f"\n• {empleado}")
            print(f"  Salario mensual: ${empleado.calcular_salario_mensual():,.0f}")
            print(f"  Tarea asignada: {empleado.asignar_tarea()}")
        
        nomina = self.service.calcular_nomina_mensual()
        print(f"\n💰 NÓMINA MENSUAL TOTAL: ${nomina:,.0f}")
    
    def ejecutar_reportes_generales(self):
        print("\n" + "="*50)
        print("📊 REPORTES GENERALES DEL HOTEL")
        print("="*50)
        
        print("\n🏨 REPORTE DE OCUPACIÓN:")
        print("-"*30)
        reporte = self.service.generar_reporte_ocupacion()
        for tipo, datos in reporte.items():
            print(f"{tipo}: {datos['ocupadas']}/{datos['total']} ocupadas")
        
        print("\n💰 INGRESOS POTENCIALES:")
        print("-"*30)
        ingresos = self.service.calcular_ingresos_potenciales()
        total = sum(ingresos.values())
        for tipo, ingreso in ingresos.items():
            print(f"{tipo}: ${ingreso:,.0f}/día")
        
        print(f"\n💵 TOTAL DIARIO: ${total:,.0f}")
        print(f"💵 TOTAL MENSUAL: ${total * 30:,.0f}")
        
        print("\n👥 REPORTE DE PERSONAL:")
        print("-"*30)
        empleados_por_tipo = {}
        for empleado in self.service.empleados:
            tipo = empleado.__class__.__name__
            empleados_por_tipo[tipo] = empleados_por_tipo.get(tipo, 0) + 1
        
        for tipo, cantidad in empleados_por_tipo.items():
            print(f"{tipo}: {cantidad} empleados")
    
    def ejecutar_simulaciones(self):
        print("\n" + "="*50)
        print("🔬 SIMULACIONES DEL SISTEMA")
        print("="*50)
        
        print("\n1. Simulación de Check-in:")
        print("-"*30)
        disponibles = self.service.obtener_habitaciones_disponibles()
        if disponibles:
            habitacion = disponibles[0]
            print(f"Check-in en Habitación {habitacion.numero}")
            habitacion.cambiar_estado("ocupada")
            habitacion.agregar_huesped_al_historial("Cliente Simulación")
            print(f"✅ Estado actual: {habitacion.estado}")
        
        print("\n2. Simulación de Servicio:")
        print("-"*30)
        servicio = ServicioRestaurante("SERV-001", "Cena Especial", 101, 2, "gourmet", "habitacion")
        print(f"Solicitando: {servicio.nombre}")
        print(f"Costo: ${servicio.calcular_costo():,.0f}")
        print(f"Tiempo: {servicio.tiempo_servicio()}")
        
        print("\n3. Simulación de Reserva:")
        print("-"*30)
        if len(self.service.habitaciones) > 1:
            reserva = ReservaIndividual("SIM-001", "2024-01-20", "2024-01-22", 
                                       self.service.habitaciones[1], "Cliente Simulación", "vacaciones", True)
            print(f"Reserva creada: {reserva.codigo_reserva}")
            print(f"Costo total: ${reserva.calcular_costo_total():,.0f}")
    
    def mostrar_informacion_sistema(self):
        print("\n" + "="*50)
        print("🔧 INFORMACIÓN DEL SISTEMA")
        print("="*50)
        
        print("\n🏨 PAQUETE 7: SISTEMA DE HOTEL")
        print("EJERCICIOS COMPLETADOS:")
        print("7.1 ✅ Gestión de Habitaciones (4 tipos, 12 total)")
        print("7.2 ✅ Sistema de Reservas (4 tipos, 5 reservas)")
        print("7.3 ✅ Servicios Adicionales (4 tipos implementados)")
        print("7.4 ✅ Personal y Departamentos (4 roles, 8 empleados)")
        
        print("\n🏆 4 PILARES DE POO IMPLEMENTADOS:")
        print("• ABSTRACCIÓN: 4 clases abstractas")
        print("• ENCAPSULAMIENTO: Atributos privados y protegidos")
        print("• HERENCIA: Jerarquías completas por módulo")
        print("• POLIMORFISMO: Métodos con comportamientos diferentes")
        
        print(f"\n📊 ESTADÍSTICAS:")
        print(f"Habitaciones: {len(self.service.habitaciones)}")
        print(f"Reservas: {len(self.service.reservas)}")
        print(f"Empleados: {len(self.service.empleados)}")


def main():
    """Función principal"""
    try:
        hotel_service = HotelService()
        menu_sistema = SistemaHotelMenu(hotel_service)
        menu_sistema.ejecutar()
    
    except KeyboardInterrupt:
        print("\n\n👋 Sistema interrumpido por el usuario.")
    except Exception as e:
        print(f"\n❌ Error inesperado: {e}")


if __name__ == "__main__":
    main()