from django.db import models
from django.urls import reverse
from django.db.models import UniqueConstraint 
from django.db.models.functions import Lower 

class Category(models.Model):
    """Model representing a category."""
    name = models.CharField(
        max_length=200,
        unique=True,
        help_text="Enter a category name."
    )

    icon = models.CharField(
        max_length=100,
        default = '',
        help_text = 'Enter an icon name.'
    )

    def __str__(self):
        """String for representing the Model object."""
        return self.name

    def get_absolute_url(self):
        """Returns the url to access a particular category instance."""
        return reverse('category-detail', args=[str(self.id)])

    class Meta:
        constraints = [
            UniqueConstraint(
                Lower('name'),
                name='category_name_case_insensitive_unique',
                violation_error_message = "A category with this name already exists."
            ),
        ]

        verbose_name_plural = 'categories'

class Technology(models.Model):
    """Model representing a technology."""
    name = models.CharField(
        max_length=200,
        unique=True,
        help_text='Enter a technology name.'
    )

    icon = models.CharField(
        max_length=100,
        default = '',
        help_text = 'Enter an icon name.'
    )

    def __str__(self):
        """String for representing the Model object."""
        return self.name

    def get_absolute_url(self):
        """Returns the url to access a particular technology instance."""
        return reverse('technology-detail', args=[str(self.id)])

    class Meta:
        constraints = [
            UniqueConstraint(
                Lower('name'),
                name='technology_name_case_insensitive_unique',
                violation_error_message = 'A technology with this name already exists.'
            ),
        ]

        verbose_name_plural = 'technologies'

# The class inherits from models.Model
class Project(models.Model):
    """Model representing a project"""

    # name is a string with max length of 200 characters.
    name = models.CharField(max_length=200)

    # description is a text field with max length of 5000 characters.
    description = models.TextField(max_length=5000, 
                                   help_text='Enter a description of the project here.')
    
    # image is an image file field - the images will be uploaded to a specified directory.
    image = models.ImageField(upload_to='')
          
    # date_added is a DateField field.
    date_added = models.DateField(null=True, 
                                  blank=True,
                                  verbose_name='date of creation')

    # category is a ForeignKey field because a project can belong to only one category
    # and a category may contain multiple projects.
    category = models.ForeignKey(Category, 
                                 on_delete=models.RESTRICT, 
                                 null=True)
        
    # technologies is a ManyToManyField because a project may use multiple technologies
    # and a technology may be used in multiple projects.
    technologies = models.ManyToManyField(Technology, 
                                          help_text='Select technologies used in this project.')

    class Meta:
        ordering = ['-date_added']

    def __str__(self):
        """String for representing the Model object."""
        return self.name

    def get_absolute_url(self):
        """Returns the URL to access a detail record for this project."""
        return reverse('project-detail', args=[str(self.id)])
    
    def display_technologies(self):
        """Create a string for the technologies in the admin site."""
        return ', '.join(technology.name for technology in self.technologies.all())
    
    display_technologies.short_description = 'technologies'
   
class Link(models.Model):
    """Model representing a link."""

    # the name of the link like 'Github', 'Amazon', etc.
    name = models.CharField(max_length=100)

    # the logo icon for the link, like the Github logo
    icon = models.CharField(
        max_length=100,
        default = '',
        help_text = 'Enter an icon name.'
    )

    # the URL to the link target
    address = models.URLField()

    # the project the link belongs to
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='links')
        
    def __str__(self):
        """String for representing the Model object."""
        return self.name

    def display_link(self):
        """Create a string for the link in the admin site."""
        return f'{self.project} ({self.project.category}) - {self.name.upper()}'
    
    display_link.short_description = 'link'
