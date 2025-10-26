from django.db import models


class Company(models.Model):
    name = models.CharField(max_length=125)
    location = models.CharField(max_length=125)

    class Meta:
        db_table = "company"

    def __str__(self):
        return self.name


class Jobs(models.Model):
    name = models.CharField(max_length=125, null=False)
    age = models.IntegerField()
    department = models.CharField(max_length=125, null=False)
    salary = models.DecimalField(max_digits=10, decimal_places=2, null=False)  # FIXED LINE
    email = models.EmailField(null=False)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "jobs"

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
        