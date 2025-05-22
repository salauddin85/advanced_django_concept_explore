from django.db import models
from django.db.models import Lookup, CharField
from django.contrib.auth.models import User

class Product(models.Model):
    name = models.CharField(max_length=100)

# Custom Lookup
@CharField.register_lookup
class IsUpper(Lookup):
    lookup_name = 'isupper'

    def as_sql(self, compiler, connection):
        lhs_sql, lhs_params = self.process_lhs(compiler, connection)
        if self.rhs:
            return f"UPPER({lhs_sql}) = {lhs_sql}", lhs_params * 2
        else:
            return f"UPPER({lhs_sql}) != {lhs_sql}", lhs_params * 2
        
        
from django.db import models

class Blog(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    author = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title



class Team(models.Model):
    name = models.CharField(max_length=50)
    team_member = models.ForeignKey('TeamMember',on_delete=models.CASCADE)
    management = models.ForeignKey('Management',on_delete=models.CASCADE)
    coach = models.ForeignKey('Coach',on_delete=models.CASCADE)
    staff = models.ManyToManyField('Staff')

class TeamMember(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    contact_number = models.CharField(max_length=12)
    email = models.EmailField()
    
class Management(models.Model):
    user = models.ManyToManyField(User)
    contact_number = models.CharField(max_length=12)
    email = models.EmailField()
    
    
class Coach(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    contact_number = models.CharField(max_length=12)
    email = models.EmailField()
    specialization = models.CharField(max_length=50)
    country = models.CharField(max_length=50,default='')
    
class Staff(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,null=True,blank=True)
    