from abc import ABC, abstractmethod
from datetime import datetime
from typing import List


class EmpleadoHotel(ABC):
    """Clase abstracta base para todos los empleados (ABSTRACCION)"""
    
    def __init__(self, nombre: str, codigo: str, turno: str, salario_base: float):
        # Atributos privados (ENCAPSULAMIENTO)
        self.__nombre = nombre
        self.__codigo = codigo
        self.__turno = turno
        self.__salario_base = salario_base
        
        # Atributo protegido
        self._evaluaciones = []  # Historial de evaluaciones
    
  
    @abstractmethod
    def calcular_salario_mensual(self) -> float:
        """Calcula salario mensual con bonos (POLIMORFISMO)"""
        pass
    
    @abstractmethod
    def asignar_tarea(self) -> str:
        """Asigna tarea según rol (POLIMORFISMO)"""
        pass
    
    # ========== METODOS CONCRETOS ==========
    def registrar_evaluacion(self, calificacion: float, comentario: str = ""):
        """Registra una evaluación del empleado"""
        evaluacion = {
            "fecha": datetime.now().strftime("%Y-%m-%d"),
            "calificacion": calificacion,
            "comentario": comentario
        }
        self._evaluaciones.append(evaluacion)
    

    def __calcular_bono_desempeño(self) -> float:
        """Calcula bono por desempeño basado en evaluaciones (ENCAPSULAMIENTO)"""
        if not self._evaluaciones:
            return 0
        
        # Calcular promedio de evaluaciones
        promedio = sum(eval["calificacion"] for eval in self._evaluaciones) / len(self._evaluaciones)
        
        # Bono según calificación
        if promedio >= 4.5:
            return self.__salario_base * 0.15  # 15% bono
        elif promedio >= 4.0:
            return self.__salario_base * 0.10  # 10% bono
        elif promedio >= 3.5:
            return self.__salario_base * 0.05  # 5% bono
        
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
    
    @property
    def evaluaciones(self) -> List[dict]:
        return self._evaluaciones.copy()
    
    def __str__(self):
        return f"{self.__nombre} - {self.__codigo} - {self.__class__.__name__}"


class Recepcionista(EmpleadoHotel):
    """Empleado de recepción (HERENCIA)"""
    
    def __init__(self, nombre: str, codigo: str, turno: str, salario_base: float,
                 idiomas: List[str]):
        super().__init__(nombre, codigo, turno, salario_base)
        self.idiomas = idiomas
        self.turno_rotativo = True
        self.atencion_cliente = True
    
    def calcular_salario_mensual(self) -> float:
        """Calcula salario con bonos por idiomas y turno"""
        salario = self.salario_base
        
        # Bono por cada idioma adicional al español
        if len(self.idiomas) > 1:
            salario += 50000 * (len(self.idiomas) - 1)
        
        # Bono por turno rotativo
        if self.turno_rotativo:
            salario += 80000
        
        # Bono por desempeño (método privado)
        salario += self._EmpleadoHotel__calcular_bono_desempeño()
        
        # Propina promedio estimada
        salario += 150000  # $150,000 en propinas estimadas
        
        return salario
    
    def asignar_tarea(self) -> str:
        """Asigna tarea de recepcionista"""
        tareas = [
            "Atención al cliente en recepción",
            "Check-in y check-out de huéspedes",
            "Reservas telefónicas",
            "Información turística",
            "Manejo de quejas y reclamos",
            "Coordinación con otros departamentos"
        ]
        
        # Seleccionar tarea según turno
        if self.turno.lower() == "matutino":
            return tareas[0] + ", " + tareas[1]
        elif self.turno.lower() == "vespertino":
            return tareas[2] + ", " + tareas[3]
        else:
            return tareas[4] + ", " + tareas[5]
    
    def __str__(self):
        return (f"Recepcionista: {self.nombre} | Idiomas: {', '.join(self.idiomas)} | "
                f"Turno: {self.turno} | Salario: ${self.calcular_salario_mensual():,.0f}")


class Housekeeping(EmpleadoHotel):
    """Empleado de limpieza y mantenimiento de habitaciones (HERENCIA)"""
    
    def __init__(self, nombre: str, codigo: str, turno: str, salario_base: float,
                 habitaciones_asignadas: List[int], piso: int, supervisor: str = ""):
        super().__init__(nombre, codigo, turno, salario_base)
        self.habitaciones_asignadas = habitaciones_asignadas
        self.piso = piso
        self.supervisor = supervisor
    
    def calcular_salario_mensual(self) -> float:
        """Calcula salario con bonos por cantidad de habitaciones"""
        salario = self.salario_base
        
        # Bono por cantidad de habitaciones (por encima de 5)
        if len(self.habitaciones_asignadas) > 5:
            salario += 20000 * (len(self.habitaciones_asignadas) - 5)
        
        # Bono por piso alto (a partir del 3er piso)
        if self.piso >= 3:
            salario += 50000
        
        # Bono por desempeño
        salario += self._EmpleadoHotel__calcular_bono_desempeño()
        
        # Propinas de huéspedes
        salario += 100000  # $100,000 en propinas estimadas
        
        return salario
    
    def asignar_tarea(self) -> str:
        """Asigna tarea de housekeeping"""
        if self.turno.lower() == "matutino":
            return f"Limpieza de {len(self.habitaciones_asignadas)} habitaciones en piso {self.piso}"
        elif self.turno.lower() == "vespertino":
            return "Preparación de habitaciones para check-in y servicios adicionales"
        else:
            return "Limpieza general y preparación para el día siguiente"
    
    def agregar_habitacion(self, numero_habitacion: int):
        """Agrega una habitación a las asignadas"""
        if numero_habitacion not in self.habitaciones_asignadas:
            self.habitaciones_asignadas.append(numero_habitacion)
    
    def __str__(self):
        return (f"Housekeeping: {self.nombre} | Piso {self.piso} | "
                f"{len(self.habitaciones_asignadas)} habitaciones | "
                f"Salario: ${self.calcular_salario_mensual():,.0f}")


class Mantenimiento(EmpleadoHotel):
    """Empleado de mantenimiento técnico (HERENCIA)"""
    
    def __init__(self, nombre: str, codigo: str, turno: str, salario_base: float,
                 especialidad: str, disponibilidad_24h: bool = False):
        super().__init__(nombre, codigo, turno, salario_base)
        self.especialidad = especialidad  # "electricidad", "plomería", "carpintería", "general"
        self.disponibilidad_24h = disponibilidad_24h
        self.herramientas = self._definir_herramientas()
    
    def _definir_herramientas(self) -> List[str]:
        """Define herramientas según especialidad"""
        herramientas = {
            "electricidad": ["multímetro", "pinzas", "cinta aislante", "destornilladores"],
            "plomería": ["llave inglesa", "desatascador", "cinta teflón", "cortatubos"],
            "carpintería": ["martillo", "sierra", "taladro", "nivel", "metro"],
            "general": ["kit básico", "linterna", "guantes", "caja de herramientas"]
        }
        return herramientas.get(self.especialidad.lower(), ["kit básico"])
    
    def calcular_salario_mensual(self) -> float:
        """Calcula salario con bonos por especialidad y disponibilidad"""
        salario = self.salario_base
        
        # Bono por especialidad técnica
        bonos_especialidad = {
            "electricidad": 100000,
            "plomería": 80000,
            "carpintería": 70000,
            "general": 50000
        }
        salario += bonos_especialidad.get(self.especialidad.lower(), 0)
        
        # Bono por disponibilidad 24h
        if self.disponibilidad_24h:
            salario += 150000
        
        # Bono por desempeño
        salario += self._EmpleadoHotel__calcular_bono_desempeño()
        
        # Bono por emergencias atendidas
        salario += 50000  # Bono estimado
        
        return salario
    
    def asignar_tarea(self) -> str:
        """Asigna tarea de mantenimiento"""
        if self.disponibilidad_24h:
            return f"Mantenimiento preventivo y emergencias 24h - Especialidad: {self.especialidad}"
        else:
            return f"Mantenimiento programado - Especialidad: {self.especialidad}"
    
    def __str__(self):
        disponibilidad = "24h" if self.disponibilidad_24h else self.turno
        return (f"Mantenimiento: {self.nombre} | {self.especialidad} | "
                f"Disponibilidad: {disponibilidad} | "
                f"Salario: ${self.calcular_salario_mensual():,.0f}")


class Gerente(EmpleadoHotel):
    """Gerente de departamento (HERENCIA)"""
    
    def __init__(self, nombre: str, codigo: str, turno: str, salario_base: float,
                 departamento: str, personal_a_cargo: int):
        super().__init__(nombre, codigo, turno, salario_base)
        self.departamento = departamento
        self.personal_a_cargo = personal_a_cargo
        self.bono_ocupacion = 0
    
    def calcular_salario_mensual(self) -> float:
        """Calcula salario con bonos por departamento y personal a cargo"""
        salario = self.salario_base
        
        # Bono por departamento
        bonos_departamento = {
            "recepcion": 200000,
            "servicios": 180000,
            "mantenimiento": 150000,
            "restaurante": 220000,
            "spa": 170000
        }
        salario += bonos_departamento.get(self.departamento.lower(), 100000)
        
        # Bono por personal a cargo ($20,000 por persona)
        if self.personal_a_cargo > 0:
            salario += 20000 * self.personal_a_cargo
        
        # Bono por ocupación del hotel (calculado externamente)
        salario += self.bono_ocupacion
        
        # Bono por desempeño
        salario += self._EmpleadoHotel__calcular_bono_desempeño()
        
        return salario
    
    def asignar_tarea(self) -> str:
        """Asigna tarea gerencial"""
        return (f"Gestión del departamento de {self.departamento} | "
                f"Supervisión de {self.personal_a_cargo} empleados | "
                f"Reuniones de coordinación | Reportes a dirección")
    
    def actualizar_bono_ocupacion(self, porcentaje_ocupacion: float):
        """Actualiza bono según ocupación del hotel"""
        if porcentaje_ocupacion >= 85:
            self.bono_ocupacion = 300000
        elif porcentaje_ocupacion >= 70:
            self.bono_ocupacion = 200000
        elif porcentaje_ocupacion >= 50:
            self.bono_ocupacion = 100000
        else:
            self.bono_ocupacion = 0
    
    def __str__(self):
        return (f"Gerente: {self.nombre} | Depto: {self.departamento} | "
                f"Personal: {self.personal_a_cargo} | "
                f"Salario: ${self.calcular_salario_mensual():,.0f}")
