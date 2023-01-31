from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Category(models.Model):
    category_name = models.CharField(max_length=200)
    
    def __str__(self):
        return self.category_name


class Bid(models.Model):
    bid = models.FloatField()
    bid_owner = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name='user_bids')



class Listing(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name='user_listings')
    name = models.CharField(max_length=200)
    description = models.CharField(max_length=1000)
    date = models.DateTimeField(auto_now_add=True)
    price = models.ForeignKey(Bid, on_delete=models.CASCADE, null=True, blank=True, related_name='bid_listing')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True, blank=True, related_name='category_listings')
    image = models.CharField(max_length=400)
    is_active = models.BooleanField(default=True)
    watchlist = models.ManyToManyField(User, null=True, blank=True, related_name='user_watchlists')

    def __str__(self):
        return self.name


class Comment(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name='user_comments')
    content = models.CharField(max_length=400)
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, null=True, blank=True, related_name='listing_comments')

    def __str__(self):
        return f'Written by {self.author}'