import json
import os
from datetime import datetime


class JSONStorage:
    """Maneja el almacenamiento de datos en archivos JSON"""
    
    def __init__(self, data_dir="data"):
        self.data_dir = data_dir
        self.archivo_habitaciones = os.path.join(data_dir, "habitaciones.json")
        self.archivo_reservas = os.path.join(data_dir, "reservas.json")
        self.archivo_empleados = os.path.join(data_dir, "empleados.json")
        
        # Crear directorio si no existe
        self._crear_directorio()
    
    def _crear_directorio(self):
        """Crea el directorio de datos si no existe"""
        if not os.path.exists(self.data_dir):
            os.makedirs(self.data_dir)
            print(f"📂 Directorio {self.data_dir} creado")
    
    def guardar_habitaciones(self, habitaciones):
        """Guarda lista de habitaciones en JSON"""
        try:
            datos = []
            for habitacion in habitaciones:
                # Convertir objeto a diccionario
                habitacion_dict = {
                    'tipo': habitacion.__class__.__name__,
                    'numero': habitacion.numero,
                    'piso': habitacion.piso,
                    'estado': habitacion.estado,
                    'tarifa_base': habitacion.tarifa_base,
                    'servicios_incluidos': habitacion.servicios_incluidos,
                    'historial_huespedes': getattr(habitacion, '_historial_huespedes', [])
                }
                
                # Agregar atributos específicos según tipo
                if hasattr(habitacion, 'vista'):
                    habitacion_dict['vista'] = habitacion.vista
                if hasattr(habitacion, 'baño_compartido'):
                    habitacion_dict['baño_compartido'] = habitacion.baño_compartido
                if hasattr(habitacion, 'tipo_camas'):
                    habitacion_dict['tipo_camas'] = habitacion.tipo_camas
                if hasattr(habitacion, 'sala_estar'):
                    habitacion_dict['sala_estar'] = habitacion.sala_estar
                if hasattr(habitacion, 'num_habitaciones'):
                    habitacion_dict['num_habitaciones'] = habitacion.num_habitaciones
                if hasattr(habitacion, 'piso_completo'):
                    habitacion_dict['piso_completo'] = habitacion.piso_completo
                
                datos.append(habitacion_dict)
            
            with open(self.archivo_habitaciones, 'w', encoding='utf-8') as f:
                json.dump(datos, f, indent=2, ensure_ascii=False)
            
            print(f"💾 {len(habitaciones)} habitaciones guardadas en {self.archivo_habitaciones}")
            return True
            
        except Exception as e:
            print(f"❌ Error al guardar habitaciones: {e}")
            return False
    
    def cargar_habitaciones(self):
        """Carga habitaciones desde JSON"""
        if not os.path.exists(self.archivo_habitaciones):
            print(f"📂 Archivo {self.archivo_habitaciones} no existe")
            return []
        
        try:
            with open(self.archivo_habitaciones, 'r', encoding='utf-8') as f:
                datos = json.load(f)
            
            print(f"📂 {len(datos)} habitaciones cargadas desde {self.archivo_habitaciones}")
            return datos
            
        except json.JSONDecodeError:
            print(f"❌ Error al leer {self.archivo_habitaciones}, archivo JSON corrupto")
            return []
        except Exception as e:
            print(f"❌ Error inesperado al cargar habitaciones: {e}")
            return []
    
    def guardar_reservas(self, reservas):
        """Guarda lista de reservas en JSON"""
        try:
            datos = []
            for reserva in reservas:
                # Convertir objeto a diccionario básico
                reserva_dict = {
                    'tipo': reserva.__class__.__name__,
                    'codigo_reserva': reserva.codigo_reserva,
                    'fecha_inicio': reserva.fecha_inicio,
                    'fecha_fin': reserva.fecha_fin,
                    'numero_habitacion': reserva.habitacion.numero if reserva.habitacion else None,
                    'huespedes': getattr(reserva, '_huespedes', [])
                }
                
                # Agregar atributos específicos según tipo
                if hasattr(reserva, 'huesped'):
                    reserva_dict['huesped'] = reserva.huesped
                if hasattr(reserva, 'proposito_visita'):
                    reserva_dict['proposito_visita'] = reserva.proposito_visita
                if hasattr(reserva, 'empresa'):
                    reserva_dict['empresa'] = reserva.empresa
                
                datos.append(reserva_dict)
            
            with open(self.archivo_reservas, 'w', encoding='utf-8') as f:
                json.dump(datos, f, indent=2, ensure_ascii=False)
            
            print(f"💾 {len(reservas)} reservas guardadas en {self.archivo_reservas}")
            return True
            
        except Exception as e:
            print(f"❌ Error al guardar reservas: {e}")
            return False
    
    def cargar_reservas(self):
        """Carga reservas desde JSON"""
        if not os.path.exists(self.archivo_reservas):
            print(f"📂 Archivo {self.archivo_reservas} no existe")
            return []
        
        try:
            with open(self.archivo_reservas, 'r', encoding='utf-8') as f:
                datos = json.load(f)
            
            print(f"📂 {len(datos)} reservas cargadas desde {self.archivo_reservas}")
            return datos
            
        except json.JSONDecodeError:
            print(f"❌ Error al leer {self.archivo_reservas}, archivo JSON corrupto")
            return []
        except Exception as e:
            print(f"❌ Error inesperado al cargar reservas: {e}")
            return []
    
    def obtener_info_archivos(self):
        """Retorna información sobre los archivos de datos"""
        info = {}
        
        archivos = {
            'habitaciones': self.archivo_habitaciones,
            'reservas': self.archivo_reservas,
            'empleados': self.archivo_empleados
        }
        
        for nombre, archivo in archivos.items():
            if os.path.exists(archivo):
                try:
                    stat = os.stat(archivo)
                    info[nombre] = {
                        'existe': True,
                        'tamaño': stat.st_size,
                        'modificado': datetime.fromtimestamp(stat.st_mtime).strftime('%Y-%m-%d %H:%M')
                    }
                except:
                    info[nombre] = {'existe': True, 'error': 'No se pudo leer'}
            else:
                info[nombre] = {'existe': False}
        
        return info
