from django.views import generic
from .models import Project

class ProjectsListView(generic.ListView):
    model = Project
    template_name = "catalog/project_list.html"  
    context_object_name = "projects"

    def get_queryset(self):
        """
        Optimized query to fetch projects along with their categories
        using select_related (ForeignKey) and prefetch_related (ManyToMany).
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
        categories = {project.category for project in projects if project.category}
        technologies = {technology for project in projects 
                        for technology in project.technologies.all()}

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
