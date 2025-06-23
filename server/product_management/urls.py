from django.urls import path
from .views import (
    ComplexProductListView,
    SimpleProductListView,
    ProductDetailView,
    ListShopsNumbers,
    FullfilProductListView,
    register_new_product_stock,
    customers_view,
    SimpleProductView,
    InvoicesView,
    BusinessContextView,
    InvoicesManagementView,
    SaleChannelView,
    PayingMethodsView,
)

urlpatterns = [
    # Customer related views
    path(
        "business-context/paying-methods",
        PayingMethodsView.as_view(),
        name="paying_methods",
    ),
    path("business-context/channels", SaleChannelView.as_view(), name="sale_channels"),
    path("business-invoices", InvoicesManagementView.as_view(), name="invoices"),
    path("business-context", BusinessContextView.as_view(), name="business"),
    path("invoices", InvoicesView.as_view(), name="invoices"),
    path(
        "retrieve-product",
        SimpleProductView.as_view(),
        name="retrieve_product_information",
    ),
    path("customers", customers_view.as_view(), name="manage_customers"),
    path(
        "complex-list-products",
        ComplexProductListView.as_view(),
        name="list-all-products",
    ),
    path("products/<str:search_term>", FullfilProductListView.as_view()),
    path(
        "simple-list-products",
        SimpleProductListView.as_view(),
        name="list-all-products",
    ),
    path(
        "retrieve-product-information/<str:product_id>",
        ProductDetailView.as_view(),
        name="get-product-information",
    ),
    path(
        "current-shop-number",
        ListShopsNumbers.as_view(),
        name="get-current-shop-number",
    ),
    path(
        "register-new-shop/<str:product_code>",
        register_new_product_stock,
        name="register-new-shop",
    ),
    # path('', include(router.urls)),
]
