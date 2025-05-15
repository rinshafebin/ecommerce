from django.db import models

# Create your models here.

class Products(models.Model):
    CATEGORY_CHOICES=[
        ('TS','T-Shirts'),
        ('SH','Shirts'),
        ('PT','Pants'),
        ('JK','Jackets')
    ]
    

    name = models.CharField(max_length=100)
    description = models.TextField()
    category = models.CharField(max_length=2,choices=CATEGORY_CHOICES)
    price = models.IntegerField(max_length=10,decimel_places=2)
    stock = models.PositiveIntegerField()
    size = models.CharField(max_length=10)
    color = models.CharField(max_length=100)
    image = models.ImageField(upload_to='product-image/')
    date_added= models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        ordering = ['-date_added']

    
    def __str__(self):
        return self.name