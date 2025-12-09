"""
SERVICES: Generación de reportes y estadísticas
"""

from datetime import datetime
from utils.validaciones import formatear_dinero


class ReporteService:
    """Servicio para generación de reportes"""
    
    def __init__(self, hotel_service):
        self.hotel_service = hotel_service
    
    def generar_reporte_financiero(self):
        """Genera reporte financiero completo"""
        reporte = {}
        
        # Ingresos por habitaciones (potenciales)
        ingresos_potenciales = self.hotel_service.calcular_ingresos_potenciales()
        total_ingresos_potenciales = sum(ingresos_potenciales.values())
        
        # Ingresos por reservas activas
        ingresos_reservas = sum(r.calcular_costo_total() for r in self.hotel_service.reservas)
        
        # Costos (nómina)
        costos_nomina = self.hotel_service.calcular_nomina_mensual()
        
        # Margen estimado
        margen_mensual = (total_ingresos_potenciales * 30) - costos_nomina
        
        reporte["financiero"] = {
            "ingresos_potenciales_diarios": total_ingresos_potenciales,
            "ingresos_potenciales_mensuales": total_ingresos_potenciales * 30,
            "ingresos_reservas_activas": ingresos_reservas,
            "costos_nomina_mensual": costos_nomina,
            "margen_estimado_mensual": margen_mensual
        }
        
        return reporte
    
    def generar_reporte_ocupacion_detallado(self):
        """Genera reporte detallado de ocupación"""
        reporte = self.hotel_service.generar_reporte_ocupacion()
        
        # Calcular porcentajes
        for tipo, datos in reporte.items():
            total = datos["total"]
            if total > 0:
                datos["porcentaje_disponibles"] = (datos["disponibles"] / total) * 100
                datos["porcentaje_ocupadas"] = (datos["ocupadas"] / total) * 100
                datos["porcentaje_limpieza"] = (datos["en_limpieza"] / total) * 100
                datos["porcentaje_mantenimiento"] = (datos["en_mantenimiento"] / total) * 100
        
        return reporte
    
    def generar_reporte_personal(self):
        """Genera reporte detallado del personal"""
        reporte = {
            "total_empleados": len(self.hotel_service.empleados),
            "por_departamento": {},
            "salarios_totales": {},
            "empleados_por_turno": {}
        }
        
        # Agrupar empleados
        for empleado in self.hotel_service.empleados:
            tipo = empleado.__class__.__name__
            
            # Por departamento/tipo
            if tipo not in reporte["por_departamento"]:
                reporte["por_departamento"][tipo] = 0
            reporte["por_departamento"][tipo] += 1
            
            # Salarios por tipo
            if tipo not in reporte["salarios_totales"]:
                reporte["salarios_totales"][tipo] = 0
            reporte["salarios_totales"][tipo] += empleado.calcular_salario_mensual()
            
            # Por turno
            turno = empleado.turno
            if turno not in reporte["empleados_por_turno"]:
                reporte["empleados_por_turno"][turno] = 0
            reporte["empleados_por_turno"][turno] += 1
        
        return reporte
    
    def generar_reporte_servicios_mas_solicitados(self, servicios_ejemplo):
        """Genera reporte de servicios (usando datos de ejemplo)"""
        if not servicios_ejemplo:
            return {"mensaje": "No hay datos de servicios"}
        
        reporte = {
            "total_servicios": len(servicios_ejemplo),
            "por_tipo": {},
            "ingresos_por_tipo": {},
            "servicios_mas_costosos": []
        }
        
        for servicio in servicios_ejemplo:
            tipo = servicio.__class__.__name__
            costo = servicio.calcular_costo()
            
            # Contar por tipo
            if tipo not in reporte["por_tipo"]:
                reporte["por_tipo"][tipo] = 0
            reporte["por_tipo"][tipo] += 1
            
            # Sumar ingresos por tipo
            if tipo not in reporte["ingresos_por_tipo"]:
                reporte["ingresos_por_tipo"][tipo] = 0
            reporte["ingresos_por_tipo"][tipo] += costo
        
        # Ordenar servicios por costo
        reporte["servicios_mas_costosos"] = sorted(
            [(s.nombre, s.calcular_costo()) for s in servicios_ejemplo],
            key=lambda x: x[1],
            reverse=True
        )[:5]  # Top 5 más costosos
        
        return reporte
    
    def imprimir_reporte_consola(self, reporte, titulo=""):
        """Imprime un reporte formateado en consola"""
        if titulo:
            print(f"\n{'='*50}")
            print(f"📊 {titulo}")
            print("="*50)
        
        if isinstance(reporte, dict):
            for clave, valor in reporte.items():
                if isinstance(valor, dict):
                    print(f"\n{clave.upper().replace('_', ' ')}:")
                    for subclave, subvalor in valor.items():
                        if isinstance(subvalor, (int, float)):
                            if "porcentaje" in subclave or "margen" in subclave:
                                print(f"  {subclave}: {subvalor:.2f}%")
                            elif "ingreso" in subclave or "costo" in subclave or "salario" in subclave:
                                print(f"  {subclave}: {formatear_dinero(subvalor)}")
                            else:
                                print(f"  {subclave}: {subvalor}")
                        else:
                            print(f"  {subclave}: {subvalor}")
                else:
                    if isinstance(valor, (int, float)):
                        if "ingreso" in clave or "costo" in clave or "salario" in clave:
                            print(f"{clave}: {formatear_dinero(valor)}")
                        else:
                            print(f"{clave}: {valor}")
                    else:
                        print(f"{clave}: {valor}")
        else:
            print(reporte)