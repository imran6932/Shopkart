from django.db import models
from django.contrib.auth.models import User

# States Name Choices For Customer Details
STATE_CHOICES = (
("Select", "-Select-"),
("Andaman and Nicobar Islands","Andaman and Nicobar Islands"),
("Andhra Pradesh","Andhra Pradesh"),
("Arunachal Pradesh","Arunachal Pradesh"),
("Assam","Assam"),
("Bihar","Bihar"),
("Chhattisgarh","Chhattisgarh"),
("Chandigarh","Chandigarh"),
("Dadra and Nagar Haveli","Dadra and Nagar Haveli"),
("Daman and Diu","Daman and Diu"),
("Delhi","Delhi"),
("Goa","Goa"),
("Gujarat","Gujarat"),
("Haryana","Haryana"),
("Himachal Pradesh","Himachal Pradesh"),
("Jammu and Kashmir","Jammu and Kashmir"),
("Jharkhand","Jharkhand"),
("Karnataka","Karnataka"),
("Kerala","Kerala"),
("Ladakh","Ladakh"),
("Lakshadweep","Lakshadweep"),
("Madhya Pradesh","Madhya Pradesh"),
("Maharashtra","Maharashtra"),
("Manipur","Manipur"),
("Meghalaya","Meghalaya"),
("Mizoram","Mizoram"),
("Nagaland","Nagaland"),
("Odisha","Odisha"),
("Punjab","Punjab"),
("Pondicherry","Pondicherry"),
("Rajasthan","Rajasthan"),
("Sikkim","Sikkim"),
("Tamil Nadu","Tamil Nadu"),
("Telangana","Telangana"),
("Tripura","Tripura"),
("Uttar Pradesh","Uttar Pradesh"),
("Uttarakhand","Uttarakhand"),
("West Bengal","West Bengal"),
)
# Customer Details Model Form
class Customer(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    locality = models.CharField(max_length=50)
    pin = models.PositiveIntegerField()
    city = models.CharField(max_length=50)
    state = models.CharField(choices=STATE_CHOICES,max_length=50, default='-Select-')

    def __str__(self):
        return str(self.id)


# Choices For Product Category
CATEGORY_CHOICES = (
    ('M','Mobile'),
    ('L','Laptop'),
    ('TW','Top Wear'),
    ('BW','Bottom Wear'),
    ('B','Books')
)
# Product Details Model Form
class Product(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    price = models.FloatField()
    discount_price = models.FloatField()
    brand = models.CharField(max_length=20)
    category = models.CharField(choices=CATEGORY_CHOICES, max_length=5)
    product_image = models.ImageField(upload_to ='productimg')

    def __str__(self):
        return str(self.id)

    @property
    def product_discount_percent(self):
        result = (self.price - self.discount_price) / self.price * 100
        return int(result)



# Cart Model Form
class Cart(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return str(self.id)

    # Property for Multiply of quantity and item price
    @property
    def product_cost(self):
        return self.quantity * self.product.discount_price

    


# Choices for Order Placed
STATUS_CHOICES = (
    ('Accepted','Accepted'),
    ('Packed','Packed'),
    ('Shipped','Shipped'),
    ('On The Way','On The Way'),
    ('Delivered','Delivered'),
    ('Cancelled','Cancelled')
    )

# Order Placed Model Form
class Order_placed(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer,on_delete=models.CASCADE)
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    order_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES,default='Pending')

    @property
    def product_cost(self):
        return self.quantity * self.product.discount_price

    

