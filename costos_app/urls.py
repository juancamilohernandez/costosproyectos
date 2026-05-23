from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    # 1. El camino vacío de la app ahora llama al LoginView de Django
    path('', auth_views.LoginView.as_view(template_name='costos_app/login.html'), name='login'),
    
    # 2. La ruta para registrar empleados
    path('empleados/nuevo/', views.registrar_empleado, name='registrar_empleado'),

    # 3. Cerrar sesión y redirigir de inmediato al Login
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),

    # 4. Asignación de proyectos
    path('proyectos/assignar/', views.asignar_proyecto, name='asignar_proyecto'), 

    # 5. Dashboard Financiero
    path('dashboard/', views.dashboard_financiero, name='dashboard_financiero'),

    # 6. Registro de facturas fijas
    path('facturas/nueva/', views.registrar_factura, name='registrar_factura'),

    # 7. Registro de activos fijos
    path('activos/nuevo/', views.registrar_activo, name='registrar_activo'),
]