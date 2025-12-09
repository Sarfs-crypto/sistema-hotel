from datetime import datetime


def validar_fecha(fecha_str: str) -> bool:
    """Valida que una cadena sea una fecha válida en formato YYYY-MM-DD"""
    try:
        datetime.strptime(fecha_str, "%Y-%m-%d")
        return True
    except ValueError:
        return False


def validar_email(email: str) -> bool:
    """Valida formato de email básico"""
    return '@' in email and '.' in email and len(email) > 5


def validar_telefono(telefono: str) -> bool:
    """Valida formato de teléfono (10 dígitos)"""
    return telefono.isdigit() and len(telefono) == 10


def calcular_edad(fecha_nacimiento: str) -> int:
    """Calcula edad a partir de fecha de nacimiento"""
    try:
        nacimiento = datetime.strptime(fecha_nacimiento, "%Y-%m-%d")
        hoy = datetime.now()
        edad = hoy.year - nacimiento.year
        
        # Ajustar si aún no ha cumplido años este año
        if (hoy.month, hoy.day) < (nacimiento.month, nacimiento.day):
            edad -= 1
        
        return edad
    except ValueError:
        return 0


def formatear_dinero(cantidad: float) -> str:
    """Formatea cantidad de dinero con separadores de miles"""
    return f"${cantidad:,.0f}"


def obtener_fecha_actual() -> str:
    """Retorna la fecha actual en formato YYYY-MM-DD"""
    return datetime.now().strftime("%Y-%m-%d")


def obtener_hora_actual() -> str:
    """Retorna la hora actual en formato HH:MM"""
    return datetime.now().strftime("%H:%M")


def calcular_dias_entre_fechas(fecha_inicio: str, fecha_fin: str) -> int:
    """Calcula días entre dos fechas"""
    try:
        inicio = datetime.strptime(fecha_inicio, "%Y-%m-%d")
        fin = datetime.strptime(fecha_fin, "%Y-%m-%d")
        
        if fin < inicio:
            return 0
        
        return (fin - inicio).days
    except ValueError:
        return 0


def es_fecha_futura(fecha_str: str) -> bool:
    """Verifica si una fecha es futura"""
    try:
        fecha = datetime.strptime(fecha_str, "%Y-%m-%d")
        return fecha > datetime.now()
    except ValueError:
        return False


def limpiar_texto(texto: str) -> str:
    """Limpia y normaliza texto"""
    return texto.strip().title()


def validar_rango(numero: float, minimo: float, maximo: float) -> bool:
    """Valida que un número esté dentro de un rango"""
    return minimo <= numero <= maximo


def convertir_a_boolean(valor: str) -> bool:
    """Convierte cadena a booleano"""
    valores_true = ['sí', 'si', 'yes', 'y', 'true', 'verdadero', '1']
    return valor.lower() in valores_true
