from models.habitacion import *
from models.reserva import *
from models.servicio import *
from models.empleado import *


class HotelService:
    """Servicio principal del hotel - Coordina todas las operaciones"""
    
    def __init__(self):
        self.habitaciones = []
        self.reservas = []
        self.servicios = []
        self.empleados = []
        self._inicializar_datos()
    
    def _inicializar_datos(self):
        """Inicializa datos de ejemplo"""
        # Crear inventario de habitaciones
        self._crear_habitaciones_ejemplo()
        
        # Contratar personal
        self._contratar_personal_ejemplo()
        
        # Crear reservas de ejemplo
        self._crear_reservas_ejemplo()
    
    def _crear_habitaciones_ejemplo(self):
        """Crea 3 habitaciones de cada tipo"""
        # 3 Habitaciones Simples
        self.habitaciones.append(HabitacionSimple(101, 1, True, "jardin", True))
        self.habitaciones.append(HabitacionSimple(102, 1, True, "calle", False))
        self.habitaciones.append(HabitacionSimple(103, 1, True, "interior", True))
        
        # 3 Habitaciones Dobles
        self.habitaciones.append(HabitacionDoble(201, 2, "2 camas individuales", "calle", True))
        self.habitaciones.append(HabitacionDoble(202, 2, "cama queen", "marina", True))
        self.habitaciones.append(HabitacionDoble(203, 2, "cama king", "montaña", True))
        
        # 3 Suites
        self.habitaciones.append(Suite(301, 3, True, True, True, 2))
        self.habitaciones.append(Suite(302, 3, True, False, True, 1))
        self.habitaciones.append(Suite(303, 3, True, True, False, 3))
        
        # 3 Penthouse
        self.habitaciones.append(Penthouse(401, 4, True, True, True))
        self.habitaciones.append(Penthouse(402, 4, False, True, False))
        self.habitaciones.append(Penthouse(403, 4, True, False, True))
    
    def _contratar_personal_ejemplo(self):
        """Contrata personal de ejemplo"""
        # 2 Recepcionistas
        self.empleados.append(Recepcionista("Ana García", "REC-001", "matutino", 1500, ["español", "inglés"]))
        self.empleados.append(Recepcionista("Carlos López", "REC-002", "vespertino", 1500, ["español", "inglés", "francés"]))
        
        # 2 Housekeeping
        self.empleados.append(Housekeeping("María Rodríguez", "HK-001", "matutino", 1200, [101, 102, 103], 1))
        self.empleados.append(Housekeeping("Pedro Sánchez", "HK-002", "vespertino", 1200, [201, 202, 203], 2))
        
        # 2 Mantenimiento
        self.empleados.append(Mantenimiento("Juan Martínez", "MT-001", "nocturno", 1300, "electricidad", True))
        self.empleados.append(Mantenimiento("Laura Fernández", "MT-002", "diurno", 1300, "plomería", False))
        
        # 2 Gerentes
        self.empleados.append(Gerente("Roberto Vargas", "GER-001", "administrativo", 2500, "recepcion", 3))
        self.empleados.append(Gerente("Sofía Ramírez", "GER-002", "administrativo", 2500, "servicios", 5))
    
    def _crear_reservas_ejemplo(self):
        """Crea reservas de ejemplo"""
        if len(self.habitaciones) >= 7:
            # 2 Reservas Individuales
            self.reservas.append(ReservaIndividual(
                "RES-001", "2024-01-15", "2024-01-18", 
                self.habitaciones[0], "Sr. Alejandro Torres", "negocios", True
            ))
            self.reservas.append(ReservaIndividual(
                "RES-004", "2024-01-20", "2024-01-22", 
                self.habitaciones[1], "Sra. Laura Mendoza", "vacaciones", False
            ))
            
            # 2 Reservas Grupales
            self.reservas.append(ReservaGrupal(
                "RES-002", "2024-01-25", "2024-01-30", 
                [self.habitaciones[3], self.habitaciones[4]], 
                "Familia González", 3, 15.0, "Sra. González"
            ))
            
            # 2 Reservas Corporativas
            self.reservas.append(ReservaCorporativa(
                "RES-003", "2024-02-01", "2024-02-05", 
                self.habitaciones[6], ["Ejecutivo 1", "Ejecutivo 2"], 
                "Tech Solutions", True, True
            ))
            
            # 2 Paquetes Turísticos
            self.reservas.append(PaqueteTuristico(
                "RES-005", "2024-02-10", "2024-02-15", 
                self.habitaciones[9], ["Grupo Internacional"], 
                "Tour Ciudad", True, 3, True
            ))
    
    def obtener_habitaciones_disponibles(self):
        """Retorna lista de habitaciones disponibles"""
        return [h for h in self.habitaciones if h.estado == "disponible"]
    
    def obtener_habitacion_por_numero(self, numero: int):
        """Busca habitación por número"""
        for habitacion in self.habitaciones:
            if habitacion.numero == numero:
                return habitacion
        return None
    
    def obtener_habitaciones_por_tipo(self, tipo: str):
        """Filtra habitaciones por tipo"""
        tipo = tipo.lower()
        tipos_validos = {
            "simple": HabitacionSimple,
            "doble": HabitacionDoble,
            "suite": Suite,
            "penthouse": Penthouse
        }
        
        if tipo not in tipos_validos:
            return []
        
        return [h for h in self.habitaciones if isinstance(h, tipos_validos[tipo])]
    
    # ========== OPERACIONES RESERVAS ==========
    def crear_reserva_individual(self, codigo: str, fecha_inicio: str, fecha_fin: str,
                                numero_habitacion: int, huesped: str, proposito: str,
                                incluye_desayuno: bool):
        """Crea una nueva reserva individual"""
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
        """Genera reporte de ocupación por tipo"""
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
        """Calcula ingresos potenciales por tipo de habitación"""
        ingresos = {}
        
        for habitacion in self.habitaciones:
            tipo = habitacion.__class__.__name__
            if tipo not in ingresos:
                ingresos[tipo] = 0
            
            ingresos[tipo] += habitacion.calcular_tarifa_noche()
        
        return ingresos
    
    def calcular_nomina_mensual(self):
        """Calcula nómina mensual total"""
        total = 0
        for empleado in self.empleados:
            total += empleado.calcular_salario_mensual()
        return total
