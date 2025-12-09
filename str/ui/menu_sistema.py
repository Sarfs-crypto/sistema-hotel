class SistemaHotelMenu:
    """Clase que maneja todos los menús del sistema"""
    
    def __init__(self, hotel_service):
        self.service = hotel_service
    
    def mostrar_menu_principal(self):
        """Muestra el menú principal"""
        print("\n" + "="*60)
        print("🏨 SISTEMA DE GESTIÓN HOTELERA - MENÚ PRINCIPAL")
        print("="*60)
        print("1️⃣  Gestión de Habitaciones")
        print("2️⃣  Gestión de Reservas")
        print("3️⃣  Gestión de Servicios")
        print("4️⃣  Gestión de Personal")
        print("5️⃣  Reportes Generales")
        print("6️⃣  Simulaciones del Sistema")
        print("7️⃣  Información del Sistema")
        print("0️⃣  Salir")
        print("-"*60)
    
    def mostrar_menu_habitaciones(self):
        """Muestra submenú de habitaciones"""
        print("\n" + "="*50)
        print("🏨 MÓDULO DE GESTIÓN DE HABITACIONES")
        print("="*50)
        print("1️⃣  Ver inventario completo")
        print("2️⃣  Ver habitaciones disponibles")
        print("3️⃣  Buscar habitación por número")
        print("4️⃣  Filtrar por tipo de habitación")
        print("5️⃣  Cambiar estado de habitación")
        print("6️⃣  Ver detalles de habitación")
        print("0️⃣  Volver al menú principal")
        print("-"*50)
    
    def mostrar_menu_reservas(self):
        """Muestra submenú de reservas"""
        print("\n" + "="*50)
        print("📅 MÓDULO DE GESTIÓN DE RESERVAS")
        print("="*50)
        print("1️⃣  Ver todas las reservas")
        print("2️⃣  Crear reserva individual")
        print("3️⃣  Crear reserva grupal")
        print("4️⃣  Crear reserva corporativa")
        print("5️⃣  Crear paquete turístico")
        print("6️⃣  Cancelar reserva")
        print("7️⃣  Ver política de cancelación")
        print("0️⃣  Volver al menú principal")
        print("-"*50)
    
    def ejecutar(self):
        """Ejecuta el sistema de menús"""
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
        """Ejecuta el módulo de habitaciones"""
        while True:
            self.mostrar_menu_habitaciones()
            opcion = input("\n🔍 Seleccione una opción: ").strip()
            
            if opcion == "0":
                break
            
            elif opcion == "1":
                self.mostrar_inventario_completo()
            
            elif opcion == "2":
                self.mostrar_habitaciones_disponibles()
            
            elif opcion == "3":
                self.buscar_habitacion_por_numero()
            
            elif opcion == "4":
                self.filtrar_habitaciones_por_tipo()
            
            elif opcion == "6":
                self.ver_detalles_habitacion()
            
            else:
                print("❌ Opción inválida.")
            
            if opcion != "0":
                input("\n⏎ Presione Enter para continuar...")
    
    def mostrar_inventario_completo(self):
        """Muestra todas las habitaciones"""
        print("\n" + "="*60)
        print("📋 INVENTARIO COMPLETO DE HABITACIONES")
        print("="*60)
        
        if not self.service.habitaciones:
            print("No hay habitaciones registradas.")
            return
        
        # Agrupar por tipo
        habitaciones_por_tipo = {}
        for habitacion in self.service.habitaciones:
            tipo = habitacion.__class__.__name__
            if tipo not in habitaciones_por_tipo:
                habitaciones_por_tipo[tipo] = []
            habitaciones_por_tipo[tipo].append(habitacion)
        
        # Mostrar por tipo
        for tipo, habitaciones in habitaciones_por_tipo.items():
            print(f"\n{tipo.upper()} ({len(habitaciones)}):")
            print("-"*40)
            for hab in habitaciones:
                print(f"  • {hab}")
        
        # Estadísticas
        print("\n📊 ESTADÍSTICAS:")
        print("-"*30)
        total = len(self.service.habitaciones)
        disponibles = len([h for h in self.service.habitaciones if h.estado == "disponible"])
        ocupadas = len([h for h in self.service.habitaciones if h.estado == "ocupada"])
        
        print(f"Total habitaciones: {total}")
        print(f"Disponibles: {disponibles}")
        print(f"Ocupadas: {ocupadas}")
        print(f"Ocupación: {(ocupadas/total*100):.1f}%")
    
    def mostrar_habitaciones_disponibles(self):
        """Muestra solo las habitaciones disponibles"""
        disponibles = self.service.obtener_habitaciones_disponibles()
        
        print("\n" + "="*50)
        print("✅ HABITACIONES DISPONIBLES")
        print("="*50)
        
        if not disponibles:
            print("No hay habitaciones disponibles en este momento.")
            return
        
        for habitacion in disponibles:
            print(f"• {habitacion}")
    
    def buscar_habitacion_por_numero(self):
        """Busca una habitación específica por número"""
        try:
            numero = int(input("\n🔍 Ingrese número de habitación: "))
            habitacion = self.service.obtener_habitacion_por_numero(numero)
            
            if habitacion:
                print(f"\n✅ HABITACIÓN ENCONTRADA:")
                print(f"   Número: {habitacion.numero}")
                print(f"   Piso: {habitacion.piso}")
                print(f"   Tipo: {habitacion.__class__.__name__}")
                print(f"   Estado: {habitacion.estado}")
                print(f"   Tarifa/noche: ${habitacion.calcular_tarifa_noche():,.0f}")
                print(f"   Capacidad: {habitacion.capacidad_maxima()} personas")
                print(f"   Servicios: {', '.join(habitacion.servicios_incluidos)}")
            else:
                print(f"❌ No se encontró habitación con número {numero}")
        except ValueError:
            print("❌ Por favor ingrese un número válido.")
    
    def filtrar_habitaciones_por_tipo(self):
        """Filtra habitaciones por tipo"""
        print("\n📋 TIPOS DE HABITACIONES:")
        print("1. Simple")
        print("2. Doble")
        print("3. Suite")
        print("4. Penthouse")
        
        try:
            opcion = int(input("\n🔍 Seleccione tipo (1-4): "))
            
            tipos = {
                1: "simple",
                2: "doble",
                3: "suite",
                4: "penthouse"
            }
            
            if opcion in tipos:
                habitaciones = self.service.obtener_habitaciones_por_tipo(tipos[opcion])
                
                print(f"\n🏨 HABITACIONES {tipos[opcion].upper()}:")
                print("-"*40)
                
                if habitaciones:
                    for hab in habitaciones:
                        print(f"• {hab}")
                    
                    # Calcular ingresos potenciales
                    ingresos = sum(h.calcular_tarifa_noche() for h in habitaciones)
                    print(f"\n💰 Ingresos potenciales/día: ${ingresos:,.0f}")
                    print(f"💰 Ingresos potenciales/mes: ${ingresos * 30:,.0f}")
                else:
                    print(f"No hay habitaciones de tipo {tipos[opcion]}.")
            else:
                print("❌ Opción inválida.")
        except ValueError:
            print("❌ Por favor ingrese un número válido.")
    
    def ver_detalles_habitacion(self):
        """Muestra detalles completos de una habitación"""
        try:
            numero = int(input("\n🔍 Ingrese número de habitación: "))
            habitacion = self.service.obtener_habitacion_por_numero(numero)
            
            if habitacion:
                print(f"\n" + "="*50)
                print(f"🏨 DETALLES COMPLETOS - HABITACIÓN {numero}")
                print("="*50)
                
                habitacion.mostrar_informacion()
                
                # Mostrar historial si existe
                if hasattr(habitacion, '_historial_huespedes') and habitacion._historial_huespedes:
                    print(f"\n📜 HISTORIAL DE HUÉSPEDES:")
                    print("-"*30)
                    for registro in habitacion._historial_huespedes[:5]:  # Mostrar últimos 5
                        print(f"• {registro['huesped']} - {registro['fecha']}")
            else:
                print(f"❌ No se encontró habitación con número {numero}")
        except ValueError:
            print("❌ Por favor ingrese un número válido.")
    
    def ejecutar_modulo_reservas(self):
        """Ejecuta el módulo de reservas"""
        while True:
            self.mostrar_menu_reservas()
            opcion = input("\n🔍 Seleccione una opción: ").strip()
            
            if opcion == "0":
                break
            
            elif opcion == "1":
                self.mostrar_todas_reservas()
            
            elif opcion == "2":
                self.crear_reserva_individual()
            
            elif opcion == "7":
                self.mostrar_politicas_cancelacion()
            
            else:
                print("❌ Opción en desarrollo. Próximamente disponible.")
            
            if opcion != "0":
                input("\n⏎ Presione Enter para continuar...")
    
    def mostrar_todas_reservas(self):
        """Muestra todas las reservas"""
        if not self.service.reservas:
            print("\n📭 No hay reservas registradas.")
            return
        
        print("\n" + "="*60)
        print("📋 RESERVAS REGISTRADAS")
        print("="*60)
        
        for i, reserva in enumerate(self.service.reservas, 1):
            print(f"\n{i}. {reserva}")
            print(f"   Huésped(es): {', '.join(reserva._huespedes)}")
            print(f"   Costo total: ${reserva.calcular_costo_total():,.0f}")
            print(f"   Política: {reserva.politica_cancelacion()}")
    
    def crear_reserva_individual(self):
        """Crea una nueva reserva individual"""
        print("\n" + "="*50)
        print("📝 CREAR RESERVA INDIVIDUAL")
        print("="*50)
        
        # Mostrar habitaciones disponibles
        disponibles = self.service.obtener_habitaciones_disponibles()
        if not disponibles:
            print("❌ No hay habitaciones disponibles.")
            return
        
        print("\n🏨 HABITACIONES DISPONIBLES:")
        for hab in disponibles:
            print(f"• Habitación {hab.numero} - {hab.__class__.__name__} - ${hab.calcular_tarifa_noche():,.0f}/noche")
        
        try:
            # Solicitar datos
            numero_hab = int(input("\n🔢 Número de habitación: "))
            codigo = input("🏷️  Código de reserva: ")
            fecha_inicio = input("📅 Fecha inicio (YYYY-MM-DD): ")
            fecha_fin = input("📅 Fecha fin (YYYY-MM-DD): ")
            huesped = input("👤 Nombre del huésped: ")
            proposito = input("🎯 Propósito de la visita: ")
            desayuno = input("🍳 ¿Incluye desayuno? (S/N): ").lower() == 's'
            
            # Crear reserva
            reserva = self.service.crear_reserva_individual(
                codigo, fecha_inicio, fecha_fin, numero_hab, 
                huesped, proposito, desayuno
            )
            
            if reserva:
                print(f"\n✅ RESERVA CREADA EXITOSAMENTE!")
                print(f"   Código: {reserva.codigo_reserva}")
                print(f"   Huésped: {reserva.huesped}")
                print(f"   Habitación: {reserva.habitacion.numero}")
                print(f"   Costo total: ${reserva.calcular_costo_total():,.0f}")
            else:
                print("❌ No se pudo crear la reserva.")
        except ValueError:
            print("❌ Error en los datos ingresados.")
    
    def mostrar_politicas_cancelacion(self):
        """Muestra políticas de cancelación"""
        print("\n" + "="*50)
        print("📜 POLÍTICAS DE CANCELACIÓN")
        print("="*50)
        print("\n1. Reserva Individual:")
        print("   • Cancelación gratis hasta 48 horas antes")
        print("   • Penalidad del 50% dentro de las 48 horas")
        print()
        print("2. Reserva Grupal:")
        print("   • Cancelación gratis hasta 1 semana antes")
        print("   • Penalidad del 30% dentro de la semana")
        print()
        print("3. Reserva Corporativa:")
        print("   • Política flexible según contrato")
        print("   • Generalmente sin penalidad con 3 días")
        print()
        print("4. Paquete Turístico:")
        print("   • No reembolsable después de confirmación")
        print("   • Posible cambio de fechas con cargo")
    
    def ejecutar_reportes_generales(self):
        """Muestra reportes generales"""
        print("\n" + "="*50)
        print("📊 REPORTES GENERALES DEL HOTEL")
        print("="*50)
        
        # Reporte de ocupación
        reporte_ocupacion = self.service.generar_reporte_ocupacion()
        
        print("\n🏨 OCUPACIÓN POR TIPO DE HABITACIÓN:")
        print("-"*45)
        
        for tipo, datos in reporte_ocupacion.items():
            print(f"\n{tipo}:")
            print(f"  Total: {datos['total']} habitaciones")
            print(f"  Disponibles: {datos['disponibles']}")
            print(f"  Ocupadas: {datos['ocupadas']}")
            print(f"  En limpieza: {datos['en_limpieza']}")
            print(f"  En mantenimiento: {datos['en_mantenimiento']}")
        
        # Ingresos potenciales
        ingresos = self.service.calcular_ingresos_potenciales()
        
        print("\n💰 INGRESOS POTENCIALES:")
        print("-"*30)
        
        total_ingresos = 0
        for tipo, ingreso in ingresos.items():
            print(f"{tipo}: ${ingreso:,.0f}/día")
            total_ingresos += ingreso
        
        print(f"\n💵 TOTAL POTENCIAL DIARIO: ${total_ingresos:,.0f}")
        print(f"💵 TOTAL POTENCIAL MENSUAL: ${total_ingresos * 30:,.0f}")
        
        # Nómina
        nomina = self.service.calcular_nomina_mensual()
        print(f"\n👥 NÓMINA MENSUAL: ${nomina:,.0f}")
        
        # Calcular margen
        margen_mensual = (total_ingresos * 30) - nomina
        print(f"📈 MARGEN ESTIMADO MENSUAL: ${margen_mensual:,.0f}")
    
    def ejecutar_simulaciones(self):
        """Ejecuta simulaciones del sistema"""
        print("\n" + "="*50)
        print("🔬 SIMULACIONES DEL SISTEMA HOTELERO")
        print("="*50)
        
        print("\n1. Simulación de Check-in:")
        print("-"*30)
        
        if self.service.habitaciones:
            # Tomar la primera habitación disponible
            disponibles = self.service.obtener_habitaciones_disponibles()
            if disponibles:
                habitacion = disponibles[0]
                print(f"Realizando check-in en Habitación {habitacion.numero}...")
                habitacion.cambiar_estado("ocupada")
                habitacion.agregar_huesped_al_historial("Cliente Simulación")
                print(f"✅ Check-in completado. Estado actual: {habitacion.estado}")
            else:
                print("❌ No hay habitaciones disponibles para simulación.")
        
        print("\n2. Simulación de Check-out:")
        print("-"*30)
        
        # Buscar una habitación ocupada
        ocupadas = [h for h in self.service.habitaciones if h.estado == "ocupada"]
        if ocupadas:
            habitacion = ocupadas[0]
            print(f"Realizando check-out de Habitación {habitacion.numero}...")
            habitacion.cambiar_estado("limpieza")
            print(f"✅ Check-out completado. Estado actual: {habitacion.estado}")
            print("La habitación ahora está en limpieza.")
        else:
            print("❌ No hay habitaciones ocupadas para simulación.")
        
        print("\n3. Simulación de Servicio:")
        print("-"*30)
        print("Solicitando servicio de Room Service...")
        print("✅ Pedido registrado. Costo estimado: $35,000")
        print("⏰ Tiempo estimado de entrega: 30 minutos")
    
    def mostrar_informacion_sistema(self):
        """Muestra información del sistema"""
        print("\n" + "="*50)
        print("🔧 INFORMACIÓN DEL SISTEMA")
        print("="*50)
        
        print(f"\n🏨 HOTEL: Luxury Palace")
        print(f"📍 DIRECCIÓN: Calle Principal #123, Ciudad Capital")
        print(f"📞 TELÉFONO: +57 1 234 5678")
        print(f"📧 EMAIL: reservas@luxurypalace.com")
        
        print(f"\n📊 ESTADÍSTICAS ACTUALES:")
        print(f"  • Habitaciones: {len(self.service.habitaciones)}")
        print(f"  • Empleados: {len(self.service.empleados)}")
        print(f"  • Reservas activas: {len(self.service.reservas)}")
        
        print(f"\n🛠️  MÓDULOS IMPLEMENTADOS:")
        print("  ✅ Gestión de Habitaciones")
        print("  ✅ Gestión de Reservas")
        print("  🔲 Gestión de Servicios (En desarrollo)")
        print("  ✅ Gestión de Personal")
        print("  ✅ Reportes y Estadísticas")
        
        print(f"\n👨‍💻 DESARROLLADO POR: [Tu Nombre]")
        print(f"📅 VERSIÓN: 2.0")
        print(f"🔒 LICENCIA: Uso educativo")
