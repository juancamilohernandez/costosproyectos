from django.urls import path
from django.contrib.auth import views as auth_views
from . import views


urlpatterns = [
    # 1. Login inicial del ERP
    path('', auth_views.LoginView.as_view(template_name='costos_app/login.html'), name='login'),
    
    # 2. Registro de empleados (Nómina)
    path('empleados/nuevo/', views.registrar_empleado, name='registrar_empleado'),

    # 3. Cerrar sesión
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),

    # 4. Asignación de proyectos y Costo ABC (¡Corregido a una sola 's'!)
    path('proyectos/asignar/', views.asignar_proyecto, name='asignar_proyecto'), 

    # 5. Dashboard Financiero General
    path('dashboard/', views.dashboard_financiero, name='dashboard_financiero'),

    # 6. Registro de facturas fijas
    path('facturas/nueva/', views.registrar_factura, name='registrar_factura'),

    # 7. Registro de activos fijos (NIC 16 / NIIF 16)
    path('activos/nuevo/', views.registrar_activo, name='registrar_activo'),
]