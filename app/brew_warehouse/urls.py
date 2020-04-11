from brew_warehouse import views
from rest_framework import routers

v1_router = routers.SimpleRouter()
v1_router.register('warehouse_item', views.WarehouseItemViewSet,
                   basename='warehouse_item')

urlpatterns = v1_router.urls
