from django.views import generic
from .models import Project, Category, Technology
from django.shortcuts import get_object_or_404

class ProjectsListView(generic.ListView):
    model = Project
    template_name = "catalog/project_list.html"  
    context_object_name = "projects"

    def get_queryset(self):
        """
        Optimized query to fetch projects along with their categories
        using select_related (ForeignKey) and technologies using 
        prefetch_related (ManyToMany).
        """
        return Project.objects.select_related('category').prefetch_related('technologies')
           
    def get_context_data(self, **kwargs):
        """
        Add categories, technologies, and project filtering data to the context.
        """
        context = super().get_context_data(**kwargs)

        # Get projects
        projects = context['projects']

        # Get categories and technologies
        categories = Category.objects.filter(project__isnull=False).distinct()
        technologies = Technology.objects.filter(project__isnull=False).distinct()
               
        # Map categories to their projects
        category_projects = {category: [] for category in categories}
        for project in projects:
            if project.category:
                category_projects[project.category].append(project)

        # Map technologies to their projects
        technology_projects = {technology: [] for technology in technologies}
        for project in projects:
            for technology in project.technologies.all():
                technology_projects[technology].append(project)

        # Count projects per category        
        category_counts = [(category, len(projects)) 
                           for category, projects 
                           in category_projects.items()]

        # Add to context
        context['categories'] = categories
        context['technologies'] = technologies
        context['category_projects'] = category_projects  # pojects by category
        context['technology_projects'] = technology_projects  # projects by technology
        context['category_counts'] = category_counts  # project counts per category

        return context

class CategoryListView(generic.ListView):
    model = Project
    template_name = "catalog/project_in_category_list.html"  
    context_object_name = "projects_in_category"

    def get_queryset(self):
        """
        Optimized query to fetch projects belonging to a category along with 
        their technologies using prefetch_related (ManyToMany).
        """

        category_name = self.kwargs.get('category_name')
        category = get_object_or_404(Category, name=category_name)

        return Project.objects.filter(category=category).prefetch_related('technologies')
           
    def get_context_data(self, **kwargs):
        """
        Add selected category, categories and technologies to the context.
        """
        context = super().get_context_data(**kwargs)

        categories = Category.objects.filter(project__isnull=False).distinct()
        technologies = Technology.objects.filter(project__isnull=False).distinct()
        
        # Add to context
        context['categories'] = categories
        context['technologies'] = technologies
        context['selected_category'] = self.kwargs.get('category_name', None)

        return context

class TechnologyListView(generic.ListView):
    model = Project
    template_name = "catalog/project_with_technology_list.html"  
    context_object_name = "projects_with_technology"

    def get_queryset(self):
        """
        Optimized query to fetch projects implementing a technology along with 
        all their technologies using prefetch_related (ManyToMany).
        """

        technology_name = self.kwargs.get('technology_name')
        technology = get_object_or_404(Technology, name=technology_name)

        return Project.objects.filter(technologies__in=[technology]).prefetch_related('technologies')
           
    def get_context_data(self, **kwargs):
        """
        Add selected technology, categories and technologies to the context.
        """
        context = super().get_context_data(**kwargs)

        categories = Category.objects.filter(project__isnull=False).distinct()
        technologies = Technology.objects.filter(project__isnull=False).distinct()
        
        # Add to context
        context['categories'] = categories
        context['technologies'] = technologies
        context['selected_technology'] = self.kwargs.get('technology_name', None)

        return context
    
class ProjectDetailView(generic.DetailView):
    model = Project

    def get_context_data(self, **kwargs):
        """
        Add categories and technologies to the context.
        """
        context = super().get_context_data(**kwargs)

        categories = Category.objects.filter(project__isnull=False).distinct()
        technologies = Technology.objects.filter(project__isnull=False).distinct()
        
        # Add to context
        context['categories'] = categories
        context['technologies'] = technologies

        return context