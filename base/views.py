from django.shortcuts import render,redirect
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView,UpdateView,DeleteView,FormView
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView,LogoutView
# Create your views here.
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from .models import Task

class CustomLogoutView(LogoutView):
    template_name='base/'



class RegisterPage(FormView):

    template_name='base/register.html'
    form_class= UserCreationForm
    redirect_authenticated_user=True

    success_url = reverse_lazy('tasks')


    def form_valid(self, form):

        user = form.save()
        if user is not None:
            login(self.request, user)
        return super().form_valid(form)
    
    def get(self,*args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('tasks')
        return super(RegisterPage,self).get(*args, **kwargs )

class CustomLoginView(LoginView):

    template_name="base/login.html"
    fields='__all__'
    redirect_authenticated_user=True
    def get_success_url(self) -> str:
        return reverse_lazy('tasks')
  
class TaskList(LoginRequiredMixin,ListView):

    model=Task
    context_object_name="tasks"

    def get_queryset(self):
        search_input = self.request.GET.get('search-area') or  ''
        if search_input:
            return Task.objects.filter(user=self.request.user).filter(title__startswith=search_input)
        return (
            Task.objects.filter(user=self.request.user)
            
        )
    def get_context_data(self, **kwargs) :
       
            context = super().get_context_data(**kwargs)
            search_input = self.request.GET.get('search-area') or  ''
            context["search_input"] = search_input
            return context
        
        

        
   
    


class TaskDetail(LoginRequiredMixin,DetailView):
    model=Task
    context_object_name="task"
    

class TaskCreate(LoginRequiredMixin,CreateView):
    model=Task
    #looks for template called task_form.html
    fields=['title','description','complete']
    success_url=reverse_lazy('tasks')

    def form_valid(self, form) :
        form.instance.user = self.request.user
        return super().form_valid(form)

class TaskDelete(LoginRequiredMixin,DeleteView):
    model=Task
    #looks for template called task_form.html
    success_url=reverse_lazy('tasks')

class TaskUpdate(LoginRequiredMixin,UpdateView):
    model=Task
    fields=['title','description','complete']
    #looks for template called task_form.html
    success_url=reverse_lazy('tasks')

    def form_valid(self, form) :
        form.instance.user = self.request.user
        return super().form_valid(form)

