from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required

from .models import User, Comment, Listing, Bid, Category
from .forms import CreateListingForm


def index(request):
    listings = Listing.objects.filter(is_active=True)
    categories = Category.objects.all()
    return render(request, "auctions/index.html", {
        'listings': listings,
        'categories': categories
    })

@login_required
def createListing(request):
    if request.method == 'POST':
        form = CreateListingForm(request.POST)
        listing = form.save(commit=False)
        listing.owner = request.user
        
        bid = Bid(bid=1000.0, bid_owner=request.user)
        bid.save()
        listing.price = bid

        listing.save()

        return redirect(reverse('index'))
        
    form = CreateListingForm()
    return render(request, 'auctions/createListing.html', {
        'form': form
    })


def category(request):
    if request.method == 'POST':
        category = request.POST['category']
        category_object = Category.objects.get(category_name=category)
        categories = Category.objects.exclude(category_name=category)
        listings = Listing.objects.filter(is_active=True, category=category_object) 
        return render(request, 'auctions/category.html', {
            'listings': listings,
            'categories': categories,
            'category': category
        })

@login_required
def listing(request, listing_id):
    listing = Listing.objects.get(id=listing_id)
    comments = Comment.objects.filter(listing=listing)
    if listing in request.user.user_watchlists.all():
        watchlist = True
    else:
        watchlist = False

    return render(request, 'auctions/listing.html', {
        'listing': listing,
        'watchlist': watchlist,
        'comments': comments
    })


@login_required
def addWatchlist(request):
    if request.method == 'POST':
        listing = Listing.objects.get(id=request.POST['listing_id'])
        listing.watchlist.add(request.user)
        listing.save()
        return redirect(reverse('listing', args = (listing.id,)))

@login_required
def removeWatchlist(request):
    if request.method == 'POST':
        listing = Listing.objects.get(id=request.POST['listing_id'])
        listing.watchlist.remove(request.user)
        listing.save()
        return redirect(reverse('listing', args = (listing.id,)))


@login_required
def watchlist(request):
    watchlists = request.user.user_watchlists.all()

    return render(request, 'auctions/watchlist.html', {
        'watchlists': watchlists
    })

@login_required
def addComment(request):
    if request.method == 'POST':
        id = request.POST['listing_id']
        listing = Listing.objects.get(id=id)
        content = request.POST['comment']
        comment = Comment(content=content, listing=listing, author=request.user)
        comment.save()

        return redirect(reverse('listing', args = (listing.id,)))


@login_required
def addBid(request):
    if request.method == 'POST':
        id = request.POST['listing_id']
        listing = Listing.objects.get(id=id)
        bid = float(request.POST['bid'])
        current_bid = listing.price.bid
        comments = Comment.objects.filter(listing=listing)
        if listing in request.user.user_watchlists.all():
            watchlist = True
        else:
            watchlist = False

        if bid > current_bid:
            newBid = Bid(bid=bid, bid_owner=request.user)
            newBid.save()
            listing.price = newBid
            listing.save()
            
            return render(request, 'auctions/listing.html', {
                'listing': listing,
                'comments': comments,
                'update': True,
                'watchlist': watchlist
            })

        else:
            return render(request, 'auctions/listing.html', {
                'listing': listing,
                'comments': comments,
                'update': False,
                'watchlist': watchlist
            })

@login_required
def removeListing(request, listing_id):
    if request.method == 'POST':
        listing = Listing.objects.get(id=listing_id)
        listing.delete()
        return redirect(reverse('index'))

@login_required
def sellListing(request, listing_id):
    if request.method == 'POST':
        listing = Listing.objects.get(id=listing_id)
        listing.is_active = False
        listing.save()
        buyer = listing.price.bid_owner
        comments = Comment.objects.filter(listing=listing)


        return render(request, 'auctions/listing.html', {
            'listing': listing,
            'comments': comments,
            'message': f'Sold to {buyer} for ${listing.price.bid}'
        })



def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")

@login_required
def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")
