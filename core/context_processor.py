from ast import Add
from core.models import Product, Category, Vendor, CartOrder, ProductImages, ProductReview, wishlist_model, Address, CartOrderProducts
from django.db.models import Min, Max
from django.contrib import messages
from decimal import Decimal, InvalidOperation
from django.shortcuts import redirect

def default(request):
    categories = Category.objects.all()
    vendors = Vendor.objects.all()
    produits_populaires = Product.objects.filter(product_status="published", featured=True).order_by("-date")[:6]




    
    
    cart_total_amount = Decimal(0)  # Utiliser Decimal pour la précision
    
    if 'cart_data_obj' in request.session:
        for p_id, item in request.session['cart_data_obj'].items():
            # Vérifier ce que contient item['price']
            price_str = item['price'].replace(',', '.').strip()  # Remplacer la virgule et enlever les espaces
            
            # Afficher le prix avant conversion
            print(f"Price before conversion: {price_str}")
            
            try:
                # Convertir le prix en Decimal
                price_decimal = Decimal(price_str)
                cart_total_amount += Decimal(item['qty']) * price_decimal
            except InvalidOperation:
                # Afficher un message d'erreur si la conversion échoue
                print(f"Erreur de conversion pour le prix: {price_str}")
                messages.error(request, f"Le prix '{price_str}' est invalide. Veuillez vérifier.")

            
    min_max_price = Product.objects.aggregate(Min("price"), Max("price"))

    if request.user.is_authenticated:
        try:
            wishlist = wishlist_model.objects.filter(user=request.user)
        except:
            messages.warning(request, "Vous devez vous connecter.")
            wishlist = 0
    else:
        wishlist = 0



    try:
        address = Address.objects.get(user=request.user)
    except:
        address = None
    
    return {
        'categories':categories,
        'vendors': vendors,
        'wishlist': wishlist,
        'address':address,
        'min_max_price':min_max_price,
        'cart_total_amount':cart_total_amount,
        'produits_populaires ':produits_populaires 
    }