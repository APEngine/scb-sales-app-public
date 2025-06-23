from django.http import JsonResponse
from django.views import View
from admin_management.models import (
    Inventory,
    InventoryRestock,
    Customers,
    Invoices,
    BusinessContext,
    SalesChannel,
    PayingMethods,
)
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from django.views.decorators.csrf import csrf_exempt, ensure_csrf_cookie
from django.views.decorators.http import require_http_methods
import json
from datetime import datetime
from http import HTTPStatus
from django.utils.decorators import method_decorator
from datetime import datetime


@method_decorator(csrf_exempt, name="dispatch")
class PayingMethodsView(View):
    def get(self, request):
        try:
            methods = PayingMethods.objects.all()
            paying_methods = [method.payingmethod for method in methods]

            return JsonResponse({"status": HTTPStatus.OK, "data": paying_methods})

        except PayingMethods.DoesNotExist as e:
            return JsonResponse({"status": HTTPStatus.NOT_FOUND, "data": e})

    def post(self, request):
        data = json.loads(request.body)
        new_paying_method = data.get("newPayingMethod")

        if not new_paying_method:
            return JsonResponse(
                {"error": "Se necesita un método de pago para continuar"},
                status=HTTPStatus.BAD_REQUEST,
            )

        try:
            paying_method = PayingMethods.objects.create(
                payingmethod=str(new_paying_method)
            )
            paying_method.save()
            return JsonResponse({"message": "Registro exitoso"}, status=HTTPStatus.OK)

        except Exception as e:
            return JsonResponse(e)

    def put(self, request):
        data = json.loads(request.body)
        paying_name = data.get("payingMethod")
        new_paying_name = data.get("newPayingMethod")

        if not paying_name:
            return JsonResponse(
                {"error": "Channel name is required"}, status=HTTPStatus.BAD_REQUEST
            )
        try:
            channel_to_modify = PayingMethods.objects.get(payingmethod=paying_name)
        except PayingMethods.DoesNotExist:
            return JsonResponse(
                {"error": "No match found"}, status=HTTPStatus.NOT_FOUND
            )

        channel_to_modify.payingmethod = new_paying_name
        channel_to_modify.save()

        return JsonResponse(
            {"message": "Cambio realizado con éxito"}, status=HTTPStatus.OK
        )


@method_decorator(csrf_exempt, name="dispatch")
class SaleChannelView(View):
    def get(self, request):
        try:
            channels = SalesChannel.objects.all()
            sale_channels = [channel.saleschannel for channel in channels]

            return JsonResponse({"status": HTTPStatus.OK, "data": sale_channels})

        except SalesChannel.DoesNotExist as e:
            return JsonResponse({"status": HTTPStatus.NOT_FOUND, "data": e})

    def post(self, request):
        data = json.loads(request.body)
        new_sales_channel = data.get("newSaleChannel")

        if not new_sales_channel:
            return JsonResponse(
                {"error": "Se necesita un canal para continuar"},
                status=HTTPStatus.BAD_REQUEST,
            )

        try:
            sale_channel = SalesChannel.objects.create(
                saleschannel=str(new_sales_channel)
            )
            sale_channel.save()
            return JsonResponse({"message": "Registro exitoso"}, status=HTTPStatus.OK)

        except Exception as e:
            return JsonResponse(e)

    def put(self, request):
        data = json.loads(request.body)
        channel_name = data.get("saleChannel")
        new_channel_name = data.get("newSaleChannel")

        if not channel_name:
            return JsonResponse(
                {"error": "Channel name is required"}, status=HTTPStatus.BAD_REQUEST
            )
        try:
            channel_to_modify = SalesChannel.objects.get(saleschannel=channel_name)
        except SalesChannel.DoesNotExist:
            return JsonResponse(
                {"error": "No match found"}, status=HTTPStatus.NOT_FOUND
            )

        channel_to_modify.saleschannel = new_channel_name
        channel_to_modify.save()

        return JsonResponse(
            {"message": "Cambio realizado con éxito"}, status=HTTPStatus.OK
        )

@method_decorator(csrf_exempt, name="dispatch")
class RestockManagementView(View):
    def get(self, request):
        print("A")
    
    def post(self, request):
        try:
            data = json.loads(request.body)
            # InventoryRestock
            product_code = data.get("productCode")
            product_name = data.get("productName")
            bill_date = data.get("billData")
            bill_number = data.get("billNumber")
            product_supplier = data.get("productSupplier")
            product_new_stock = data.get("newStock")
            bill_observations = data.get("d")
            defective_unities = data.get("a")
            
        except Exception as e:
            return JsonResponse(e)
        
@method_decorator(csrf_exempt, name="dispatch")
class InvoicesManagementView(View):
    def get(self, request):
        try:

            document_id = request.GET.get("documentId")
            # Check if document_id is not null
            if not document_id:
                return JsonResponse(
                    {"error": "Document ID is required"}, status=HTTPStatus.BAD_REQUEST
                )

            invoice_requested = Invoices.objects.filter(
                document_id=request.GET.get("documentId")
            )  # Retrieve document requested
            if not invoice_requested.exists():
                return JsonResponse(
                    {"error": "Invoice not found"}, status=HTTPStatus.NOT_FOUND
                )

            status = HTTPStatus.OK

            invoice = []
            invoice_information = invoice_requested[
                0
            ]  # Define first invoice for customer and invoice information

            # Loop through all products
            products = [
                {
                    "code": invoice.product_code,
                    "title": invoice.product_name,
                    "price": invoice.product_cost,
                    "quantity": invoice.product_quantity,
                    "total": invoice.unitary_sub_total,
                }
                for invoice in invoice_requested
            ]

            # Retrieve Information about customer
            try:
                customer_information = Customers.objects.get(
                    customer_id__endswith=invoice_information.customer_id
                )
                customer = {
                    "id": customer_information.customer_id,
                    "name": customer_information.name,
                    "address": customer_information.address,
                    "phone_number": customer_information.phone_number,
                    "email": customer_information.email,
                }
            except Customers.DoesNotExist:
                return JsonResponse(
                    {"error": "Customer not found"}, status=HTTPStatus.NOT_FOUND
                )

            invoice = {
                "id": document_id,
                "date": invoice_information.document_date,
                "type": invoice_information.document_type,
                "products": products,
                "customer": customer,
                "user": invoice_information.logged_user,
                "tax": invoice_information.product_tax,
            }
            # print(invoice_requested)
            print(invoice)

        except Invoices.DoesNotExist:
            invoice_requested = None
            status = HTTPStatus.NOT_FOUND

        # return JsonResponse({"status": status, "data": invoice_requested}, safe=False)

    def post(self, request):
        try:
            data = json.loads(request.body)
            print(data)
            document_id = data.get("documentId")
            document_date = data.get("documentDate")
            document_type = data.get("documentType")
            customer_id = data.get("customerId")
            products_sell = data.get("products")
            parsed_date = datetime.strptime(document_date, "%d-%m-%Y")
            formatted_date = parsed_date.strftime("%Y-%m-%d %H:%M:%S")
            sale_channel = data.get("salesChannel")
            paying_method = data.get("payingMethod")
            for product in products_sell:
                product = Invoices.objects.create(
                    document_id=str(document_id),
                    document_date=formatted_date,
                    document_type=str(document_type),
                    product_code=str(product["code"]),
                    product_name=product["title"],
                    product_quantity=product["quantity"],
                    product_cost=product["price"],
                    customer_id=customer_id[2:],
                    unitary_sub_total=product["totalPrice"],
                    sales_channel=str(sale_channel),
                    paying_method=str(paying_method)
                )
                product.save()
                
            for product in products_sell:    
                product_code = product.get("code")
                product_quantity = product.get("quantity")
                product = Inventory.objects.get(code=product_code)
                # product.to_shop = product.to_shop - product_quantity
                product.in_stock = product.in_stock - product_quantity
                product.save()
                
            status = HTTPStatus.OK
            return JsonResponse({"status": status})
        except Exception as e:
            return JsonResponse(e)


@method_decorator(csrf_exempt, name="dispatch")
class BusinessContextView(View):
    def get(self, request):
        try:
            business = BusinessContext.objects.get(id=1)
            business = {
                "name": business.name,
                "rif": business.rif,
                "direction": business.direction,
                "telephone": business.telephone,
                "iva": int(business.iva),
            }
            status = HTTPStatus.OK
        except Invoices.DoesNotExist:
            business = None
            status = HTTPStatus.NOT_FOUND

        return JsonResponse({"status": status, "data": business}, safe=False)

    def post(self, request):
        try:
            data = json.loads(request.body)
            business_name = data.get("businessName")
            business_rif = data.get("businessRif")
            business_telephone = data.get("businessTelephone")
            business_direction = data.get("businessDirection")
            business_iva = data.get("businessIva")

            business = BusinessContext.objects.create(
                name=business_name,
                rif=business_rif,
                telephone=business_telephone,
                direction=business_direction,
                iva=business_iva
            )

            return JsonResponse({"message": "Business created", "id": business.id}, status=201)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)
    
    def put(self, request):
        try:
            data = json.loads(request.body)
            business_name = data.get("businessName")
            business_rif = data.get("businessRif")
            business_telephone = data.get("businessTelephone")
            business_direction = data.get("businessDirection")
            business_iva = data.get("businessIva")

            business = BusinessContext.objects.get(id=1)
            business.name = business_name
            business.rif = business_rif
            business.telephone = business_telephone
            business.direction = business_direction
            business.iva = business_iva
            business.save()
        except Exception as e:
            return JsonResponse(e)


class InvoicesView(View):
    def get(self, request):
        try:
            # invoice_requested = (
            #     Invoices.objects.order_by("-document_id").first().document_id
            # )
            # invoice_requested = (
            #     int(Invoices.objects.order_by("-document_id").first().document_id)
            #     + 1
            # )
            latest_invoice = Invoices.objects.order_by("-document_id").first()

            if latest_invoice:
                doc_id = int(latest_invoice.document_id) + 1
            else:
                doc_id = 1
            status = HTTPStatus.OK

            print(doc_id)
        except Invoices.DoesNotExist:
            doc_id = None
            status = HTTPStatus.NOT_FOUND

        return JsonResponse({"status": status, "data": doc_id}, safe=False)


@method_decorator(csrf_exempt, name="dispatch")
class SimpleProductView(View):
    def get(self, request):
        try:
            product = Inventory.objects.get(code=request.GET.get("productId"))
            if product.in_stock >= 1:
                product = {
                    "productCode": product.code,
                    "productName": product.name,
                    "productDescription": product.description,
                    "productPrice": product.normal_price,
                    "productRetailPrice": product.retail_price,
                    "productWholesale": product.wholesale_price,
                    "minimumOrderQuantity": product.moq_whole_sale,
                    "existence": product.in_stock - product.to_shop,
                    "quantity": 1,
                }
                status = HTTPStatus.OK
                message = "Producto agregado con éxito"
            else:
                product = None
                status = HTTPStatus.NOT_ACCEPTABLE
                message = "No hay existencia del producto"

        except Inventory.DoesNotExist:
            product = None
            status = HTTPStatus.NOT_FOUND
            message = "No se encontró el producto"

        return JsonResponse(
            {"status": status, "message": message, "data": product}, safe=False
        )

    def post(self, request):
        try:
            data = json.loads(request.body)
            print()
            print("START")
            print(data)
            for product in data:
                try:
                    product_code = product.get("code")
                    product_quantity = product.get("quantity")
                    product = Inventory.objects.get(code=product_code)
                    print(product.to_shop, product_quantity)
                    product.to_shop = product.to_shop - product_quantity
                    product.save()
                except Inventory.DoesNotExist:
                    continue
            reset_codes = data.get("productsCodes")
        except json.JSONDecodeError:
            return JsonResponse(
                {"status": HTTPStatus.BAD_REQUEST, "message": "Invalid JSON format."},
                safe=False,
            )
        except Exception as e:
            # General error handler (optional)
            return JsonResponse(
                {"status": HTTPStatus.INTERNAL_SERVER_ERROR, "message": str(e)},
                safe=False,
            )

    def put(self, request):
        try:
            data = json.loads(request.body)

            # Validate input data
            product_code = data.get("productCode")
            unity_to_discount = data.get("unityToDiscount")

            if product_code is None or unity_to_discount is None:
                return JsonResponse(
                    {
                        "status": HTTPStatus.BAD_REQUEST,
                        "message": "Missing required fields.",
                    },
                    safe=False,
                )

            # Fetch product
            try:
                product_to_discount = Inventory.objects.get(code=product_code)
            except ObjectDoesNotExist:
                return JsonResponse(
                    {"status": HTTPStatus.NOT_FOUND, "message": "Product not found."},
                    safe=False,
                )

            # Validate `to_shop` value
            if product_to_discount.to_shop < 0:
                return JsonResponse(
                    {
                        "status": HTTPStatus.BAD_REQUEST,
                        "message": "Invalid `to_shop` value.",
                    },
                    safe=False,
                )

            # Check stock availability
            if (
                product_to_discount.in_stock
                >= product_to_discount.to_shop + unity_to_discount
            ):
                product_to_discount.to_shop = (
                    product_to_discount.to_shop + unity_to_discount
                )
                product_to_discount.save()
                return JsonResponse(
                    {
                        "status": HTTPStatus.ACCEPTED,
                        "message": "Producto agregado con éxito.",
                    },
                    safe=False,
                )
            else:
                return JsonResponse(
                    {
                        "status": HTTPStatus.BAD_REQUEST,
                        "message": "La cantidad a ingresar es mayor a la existente.",
                    },
                    safe=False,
                )

        except json.JSONDecodeError:
            return JsonResponse(
                {"status": HTTPStatus.BAD_REQUEST, "message": "Invalid JSON format."},
                safe=False,
            )
        except Exception as e:
            # General error handler (optional)
            return JsonResponse(
                {"status": HTTPStatus.INTERNAL_SERVER_ERROR, "message": str(e)},
                safe=False,
            )


@method_decorator(csrf_exempt, name="dispatch")
class customers_view(View):

    def get(self, request):
        # data = json.loads(request.body)
        try:
            customer = Customers.objects.get(customer_id=request.GET.get("customerId"))
            customer = {
                "id": customer.customer_id,
                "name": customer.name,
                "address": customer.address,
                "phone_number": customer.phone_number,
                "email": customer.email,
            }
            status = HTTPStatus.OK
        except Customers.DoesNotExist:
            customer = None
            status = HTTPStatus.NOT_FOUND

        return JsonResponse({"status": status, "data": customer}, safe=False)

    def post(self, request):
        try:
            data = json.loads(request.body)
            # Extract customer fields from the data
            customer_id = data.get("customerId")
            name = data.get("name")
            address = data.get("address")
            phone_number = data.get("phoneNumber")
            email = data.get("email")

            # Create a new customer in the database
            customer = Customers.objects.create(
                customer_id=customer_id,
                name=name,
                address=address,
                phone_number=phone_number,
                email=email,
            )
            customer.save()
            # Prepare the response data
            customer_data = {
                "id": customer.customer_id,
                "name": customer.name,
                "address": customer.address,
                "phoneNumber": customer.phone_number,
                "email": customer.email,
            }
            status = HTTPStatus.CREATED

        except KeyError as e:
            return JsonResponse(
                {"status": HTTPStatus.BAD_REQUEST, "error": f"Missing field: {e}"},
                status=HTTPStatus.BAD_REQUEST,
            )

        except Exception as e:
            return JsonResponse(
                {"status": HTTPStatus.INTERNAL_SERVER_ERROR, "error": str(e)},
                status=HTTPStatus.INTERNAL_SERVER_ERROR,
            )

        return JsonResponse({"status": status, "data": customer_data}, safe=False)


@method_decorator(csrf_exempt, name="dispatch")
class ComplexProductListView(View):
    def get(self, request):
        products = Inventory.objects.all()
        data = [
            {
                "id": product.id,
                "name": product.name,
                "code": product.code,
                "stockQuantity": product.in_stock,
                "price": product.normal_price,
                "retailPrice": product.retail_price,
                "wholesalePrice": product.wholesale_price,
                "inventoryPrice": product.item_inventory_price,
                "description": product.description,
                "defectiveUnits": product.defective_units,
            }
            for product in products
        ]
        return JsonResponse(data, safe=False)

    def post(self, request):
        try:
            data = json.loads(request.body)
            code = data.get("code")
            name = data.get("name")
            description = data.get("description")
            # in_stock = data.get("stock")
            to_shop = 0
            normal_price = data.get("normalPrice")
            retail_price = data.get("retailPrice")
            wholesale_price = data.get("wholesalePrice")
            moq_whole_sale = data.get("moq")
            # item_inventory_price = data.get("inventoryPrice")
            # defective_units = data.get("defectiveUnits")

            new_product = Inventory.objects.create(
                code=code,
                name=name,
                description=description,
                # in_stock=in_stock,
                in_stock=0,
                to_shop=to_shop,
                normal_price=normal_price,
                retail_price=retail_price,
                wholesale_price=wholesale_price,
                moq_whole_sale=moq_whole_sale,
                # item_inventory_price=item_inventory_price,
                item_inventory_price=0,
                # defective_units=defective_units,
                defective_units=0,
            )
            new_product.save()
            status = HTTPStatus.ACCEPTED
        except Exception as e:
            return JsonResponse(
                {"status": HTTPStatus.INTERNAL_SERVER_ERROR, "error": str(e)},
                status=HTTPStatus.INTERNAL_SERVER_ERROR,
            )
        return JsonResponse({"status": status}, safe=False)


class FullfilProductListView(View):
    def get(self, request, search_term=""):  # Added search_term argument
        search_term = search_term.lower()  # Ensure case-insensitive search
        products = Inventory.objects.filter(
            name__icontains=search_term
        )  # Filter by name
        data = [
            {
                "id": product.id,
                "name": product.name,
                "code": product.code,
            }
            for product in products
        ]
        return JsonResponse(data, safe=False)


class SimpleProductListView(View):
    def get(self, request):
        products = Inventory.objects.all()
        data = [
            {
                "id": product.id,
                "name": product.name,
                "code": product.code,
            }
            for product in products
        ]
        return JsonResponse(data, safe=False)


class ProductDetailView(View):
    def get(self, request, product_id):
        product = Inventory.objects.get(code=product_id)
        data = {
            "id": product.id,
            "name": product.name,
            "code": product.code,
            "stockQuantity": product.in_stock,
            "price": product.normal_price,
            "retailPrice": product.retail_price,
            "wholesalePrice": product.wholesale_price,
            "inventoryPrice": product.item_inventory_price,
            "description": product.description,
            "defectiveUnits": product.defective_units,
        }
        return JsonResponse(data)


class UpdateQuantityView(View):
    def post(self, request, product_id):
        product = Inventory.objects.get(product_id=product_id)
        new_quantity = request.POST.get("new_quantity")
        product.quantity = new_quantity
        product.save()
        data = {"message": "Quantity updated successfully"}
        return JsonResponse(data)


class CalculateTotalPriceView(View):
    def get(self, request, product_id):
        product = Inventory.objects.get(product_id=product_id)
        total_price = product.price * product.quantity
        data = {"product_id": product.product_id, "total_price": total_price}
        return JsonResponse(data)


class CreateProductView(View):
    def post(self, request):
        # Extract product data from the request body
        data = request.POST
        name = data.get("name")
        inner_code = data.get("inner_code")
        price = data.get("price")
        quantity = data.get("quantity")
        description = data.get("description")

        # Create a new product object
        product = Inventory.objects.create(
            name=name,
            inner_code=inner_code,
            price=price,
            quantity=quantity,
            description=description,
        )

        # Save the product to the database
        product.save()

        # Return a success response
        return JsonResponse({"message": "Product created successfully"}, safe=False)


class ListShopsNumbers(View):
    def get(self, request):
        shopNumber = InventoryRestock.objects.order_by("-id").first().id
        data = {
            "currentNumber": shopNumber + 1,
        }
        return JsonResponse(data)


from rest_framework.views import APIView


@csrf_exempt
def register_new_product_stock(request, product_code):
    # Extract product data from the request body
    data = json.loads(request.body)
    product_code = product_code
    bill_date = data.get("entryDateInput")
    bill_number = data.get("invoiceNumberInput")
    product_supplier = data.get("supplierInput")
    product_new_stock = int(data.get("newStockInput"))
    bill_observations = data.get("commentInput")
    user = data.get("user")

    try:
        # Create a new product object
        productRestock = InventoryRestock.objects.create(
            name=str(Inventory.objects.get(code=product_code).name),
            code=product_code,
            bill_date=datetime.strptime(bill_date, "%Y-%m-%d").date(),
            bill_number=bill_number,
            supplier=product_supplier,
            new_stock=product_new_stock,
            observations=bill_observations,
            user=user,
        )

        productRestock.save()

        product = Inventory.objects.get(code=product_code)
        product.in_stock += product_new_stock
        product.save()

        # Return a success response
        return JsonResponse({"message": "Product updated successfully"}, safe=False)

    except Inventory.DoesNotExist:
        return JsonResponse({"message": "Product not found"}, status=404)

    except Exception as e:
        # Handle any other unexpected errors
        return JsonResponse({"message": str(e)}, status=500)
