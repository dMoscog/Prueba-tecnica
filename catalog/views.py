from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import Character
from .forms import CharacterForm

def is_admin(user):
    return user.is_authenticated and (user.is_superuser or user.groups.filter(name='Administrador').exists())

def character_list(request):
    search_query = request.GET.get('q', '')
    status_filter = request.GET.get('status', '')
    species_filter = request.GET.get('species', '')
    gender_filter = request.GET.get('gender', '')

    characters = Character.objects.select_related('location').prefetch_related('episodes').all()

    if search_query:
        characters = characters.filter(name__icontains=search_query)
    if status_filter:
        characters = characters.filter(status__iexact=status_filter)
    if species_filter:
        characters = characters.filter(species__iexact=species_filter)
    if gender_filter:
        characters = characters.filter(gender__iexact=gender_filter)

    characters = characters.order_by('id')

    paginator = Paginator(characters, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    statuses = Character.objects.values_list('status', flat=True).distinct().exclude(status='')
    species_list = Character.objects.values_list('species', flat=True).distinct().exclude(species='')
    genders = Character.objects.values_list('gender', flat=True).distinct().exclude(gender='')

    context = {
        'characters': page_obj,
        'search_query': search_query,
        'status_filter': status_filter,
        'species_filter': species_filter,
        'gender_filter': gender_filter,
        'statuses': statuses,
        'species_list': species_list,
        'genders': genders,
    }

    return render(request, 'catalog/character_list.html', context)

@login_required
@user_passes_test(is_admin)
def character_create(request):
    if request.method == 'POST':
        form = CharacterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('character_list')
    else:
        form = CharacterForm()
    return render(request, 'catalog/character_form.html', {'form': form, 'action': 'Crear'})

@login_required
@user_passes_test(is_admin)
def character_edit(request, pk):
    character = get_object_or_404(Character, pk=pk)
    if request.method == 'POST':
        form = CharacterForm(request.POST, instance=character)
        if form.is_valid():
            form.save()
            return redirect('character_list')
    else:
        form = CharacterForm(instance=character)
    return render(request, 'catalog/character_form.html', {'form': form, 'action': 'Editar'})

@login_required
@user_passes_test(is_admin)
def character_delete(request, pk):
    character = get_object_or_404(Character, pk=pk)
    if request.method == 'POST':
        character.delete()
        return redirect('character_list')
    return render(request, 'catalog/character_confirm_delete.html', {'character': character})