from django.db import models
from django.contrib.auth.models import User

class Company(models.Model):
    name = models.CharField(max_length=125)
    location = models.CharField(max_length=125)

    class Meta:
        db_table = "company"

    def __str__(self):
        return self.name


class Members(models.Model):
    name = models.CharField(max_length=125, null=False)
    age = models.IntegerField()
    department = models.CharField(max_length=125, null=False)
    salary = models.DecimalField(max_digits=10, decimal_places=2, null=False)  # FIXED LINE
    email = models.EmailField(null=False)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "members"

    def __str__(self):
        if self.name:
            return f"{self.name}"
        elif self.age:
            return f"{self.age}"
        elif self.name:
            return f"{self.name}"
        elif self.department:
            return f"{self.department}"
        elif self.salary:
            return f"{self.salary}"
        elif self.email:
            return f"self.email"
        else:
            return "Unknown"
        
class UserSession(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    login_time = models.DateTimeField(null=True, blank=True)
    logout_time = models.DateTimeField(null=True, blank=True)
    duration = models.DurationField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = "user_sessions"
        
    def save(self, *args, **kwargs):
        if self.login_time and self.logout_time:
            self.duration = self.logout_time - self.login_time
        super().save(*args, **kwargs)
        
    def __str__(self):
        return f"{self.user.username} | Login: {self.login_time} | Logout: {self.logout_time}"
    
    
class api_data(models.Model):
    first_name = models.CharField(max_length=100, null=False)
    last_name = models.CharField(max_length=100, null=False)
    username = models.CharField(max_length=25, null=False)
    employee_id = models.BigIntegerField(null=False)
    department = models.CharField(max_length=225, null=False)
    log_in = models.DateTimeField()  
    log_out = models.DateTimeField()
    
    def __str__(self):
        return f"{self.first_name} {self.last_name}"
    
    class Meta:
        db_table = "api_data"