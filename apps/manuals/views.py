from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Brand, VehicleModel, Manual
from django.http import HttpResponseForbidden

class BrandListView(LoginRequiredMixin, ListView):
    model = Brand
    template_name = 'manuals/brand_list.html'
    context_object_name = 'brands'

class ModelListView(LoginRequiredMixin, ListView):
    model = VehicleModel
    template_name = 'manuals/model_list.html'
    context_object_name = 'models'

    def get_queryset(self):
        return VehicleModel.objects.filter(brand__slug=self.kwargs['brand_slug'])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['brand'] = get_object_or_404(Brand, slug=self.kwargs['brand_slug'])
        return context

class ManualListView(LoginRequiredMixin, ListView):
    model = Manual
    template_name = 'manuals/manual_list.html'
    context_object_name = 'manuals'

    def get_queryset(self):
        return Manual.objects.filter(
            vehicle_model__slug=self.kwargs['model_slug'],
            year=self.kwargs['year']
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['model'] = get_object_or_404(VehicleModel, slug=self.kwargs['model_slug'])
        context['year'] = self.kwargs['year']
        return context

def viewer_page(request, manual_id):
    if not request.user.is_authenticated:
        return redirect('accounts:login')
    
    manual = get_object_or_404(Manual, id=manual_id)
    
    # Check if user is active
    if request.user.status != 'active':
        return render(request, 'accounts/pending.html')

    return render(request, 'manuals/viewer.html', {'manual': manual})
