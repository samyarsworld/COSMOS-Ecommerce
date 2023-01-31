from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),

    path('listings/<int:listing_id>', views.listing, name='listing'),
    path('remove_listing/<int:listing_id>', views.removeListing, name='remove_listing'),
    path('sell_listing/<int:listing_id>', views.sellListing, name='sell_listing'),
    path("category", views.category, name="category"),
    path('create_listing', views.createListing, name='create_listing'),
    
    path("add_watchlist", views.addWatchlist, name="add_watchlist"),
    path("remove_watchlist", views.removeWatchlist, name="remove_watchlist"),
    path("watchlist", views.watchlist, name="watchlist"),
    
    path("add_comment", views.addComment, name="add_comment"),

    path("add_bid", views.addBid, name="add_bid")
]
