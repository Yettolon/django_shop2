import keyword
from .forms import SearchForm


def kind_contexttt(request):
    context = {}
    forrrrrrm = SearchForm()
    context = {'forrrrrrm':forrrrrrm}
    return context