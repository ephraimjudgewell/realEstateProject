from django.shortcuts import get_object_or_404, render
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from .choices import price_choices, bedroom_choices, state_choices

from .models import Listing
pageSize = 6

def getProperties(pg, **kwargs):
    listings = Listing.objects.order_by('-list_date').filter(is_published=True)
    if not kwargs:
        paginator = Paginator(listings, pageSize)
        return paginator.get_page(pg)
    else:
        for k,v in kwargs.items():
            ''' v here can either be -1 or 1 - 1000000; '''
            if not v:
                continue
            try:
                v = int(v)
                k = k + '__' + ('lte' if v.__ge__(0) else 'gte')
                if v.__eq__(-1):
                    v = 10 if k.__contains__('bedrooms') else 1000000
            except Exception as e:
                k = ('description' if k == 'keywords' else k) + '__i' + ('contains' if k.__contains__('keyword') else 'exact')
            finally:
                listings = listings.filter(**{k:v})
        paginator = Paginator(listings, pageSize)
        return paginator.get_page(pg)

# Create your views here.
def listings(request):
    context = {
        'listings': getProperties(request.GET.get('page'))
        }
    return render(request, 'listings/listings.html', context)

def listing(request,listing_id):
    listing = get_object_or_404(Listing, pk=listing_id)
    context = {
        'listing': listing
    }
    return render(request, 'listings/listing.html', context)

def search(request):
    page = request.GET.get('page')
    keywords = request.GET.get('keywords')
    city = request.GET.get('city')
    state = request.GET.get('state')
    bedrooms = request.GET.get('bedrooms')
    price = request.GET.get('price')
    queryset_list = None
    if not keywords and not city and not state and not bedrooms and not price:
        queryset_list = getProperties(page)
    else:
        queryset_list = getProperties(page, keywords=keywords, city = city, state = state, bedrooms = bedrooms, price = price)
    context = {
        'state_choices': state_choices,
        'bedroom_choices': bedroom_choices,
        'price_choices': price_choices,
        'listings': queryset_list,
        'values': request.GET
        }
    return render(request, "listings/search.html", context)
