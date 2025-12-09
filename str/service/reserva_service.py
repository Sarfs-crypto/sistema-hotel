"""
SERVICES: Lógica específica para gestión de reservas
"""

from models.reserva import *
from datetime import datetime


class ReservaService:
    """Servicio especializado en gestión de reservas"""
    
    def __init__(self, hotel_service):
        self.hotel_service = hotel_service
    
    def buscar_reserva_por_codigo(self, codigo: str):
        """Busca reserva por código"""
        for reserva in self.hotel_service.reservas:
            if reserva.codigo_reserva == codigo:
                return reserva
        return None
    
    def buscar_reservas_por_huesped(self, nombre_huesped: str):
        """Busca reservas por nombre de huésped"""
        resultados = []
        nombre_buscar = nombre_huesped.lower()
        
        for reserva in self.hotel_service.reservas:
            # Buscar en huéspedes de la reserva
            for huesped in reserva.huespedes:
                if nombre_buscar in huesped.lower():
                    resultados.append(reserva)
                    break
            
            # Buscar en atributos específicos
            if hasattr(reserva, 'huesped') and nombre_buscar in reserva.huesped.lower():
                if reserva not in resultados:
                    resultados.append(reserva)
            
            if hasattr(reserva, 'grupo_nombre') and nombre_buscar in reserva.grupo_nombre.lower():
                if reserva not in resultados:
                    resultados.append(reserva)
        
        return resultados
    
    def calcular_ocupacion_fecha(self, fecha: str):
        """Calcula ocupación para una fecha específica"""
        try:
            fecha_consulta = datetime.strptime(fecha, "%Y-%m-%d")
            ocupadas = 0
            
            for reserva in self.hotel_service.reservas:
                fecha_inicio = datetime.strptime(reserva.fecha_inicio, "%Y-%m-%d")
                fecha_fin = datetime.strptime(reserva.fecha_fin, "%Y-%m-%d")
                
                if fecha_inicio <= fecha_consulta <= fecha_fin:
                    ocupadas += 1
            
            total = len(self.hotel_service.habitaciones)
            if total > 0:
                porcentaje = (ocupadas / total) * 100
                return {
                    "fecha": fecha,
                    "habitaciones_ocupadas": ocupadas,
                    "habitaciones_totales": total,
                    "porcentaje_ocupacion": round(porcentaje, 2)
                }
            
        except ValueError:
            pass
        
        return None
    
    def cancelar_reserva(self, codigo_reserva: str) -> bool:
        """Cancela una reserva"""
        reserva = self.buscar_reserva_por_codigo(codigo_reserva)
        
        if not reserva:
            print(f"❌ No se encontró reserva con código: {codigo_reserva}")
            return False
        
        # Liberar habitación
        reserva.habitacion.cambiar_estado("disponible")
        
        # Remover reserva de la lista
        self.hotel_service.reservas.remove(reserva)
        
        print(f"✅ Reserva {codigo_reserva} cancelada exitosamente")
        print(f"💡 Política aplicada: {reserva.politica_cancelacion()}")
        
        return True
    
    def generar_reporte_mensual(self, mes: int, año: int):
        """Genera reporte mensual de reservas"""
        reservas_mes = []
        ingresos_mes = 0
        
        for reserva in self.hotel_service.reservas:
            try:
                fecha_reserva = datetime.strptime(reserva.fecha_inicio, "%Y-%m-%d")
                if fecha_reserva.month == mes and fecha_reserva.year == año:
                    reservas_mes.append(reserva)
                    ingresos_mes += reserva.calcular_costo_total()
            except ValueError:
                continue
        
        return {
            "mes": mes,
            "año": año,
            "total_reservas": len(reservas_mes),
            "ingresos_totales": ingresos_mes,
            "reservas": reservas_mes
        }
    
    def obtener_reservas_activas(self):
        """Retorna reservas que están activas (fecha actual dentro del rango)"""
        fecha_actual = datetime.now().strftime("%Y-%m-%d")
        reservas_activas = []
        
        for reserva in self.hotel_service.reservas:
            if reserva.fecha_inicio <= fecha_actual <= reserva.fecha_fin:
                reservas_activas.append(reserva)
        
        return reservas_activas