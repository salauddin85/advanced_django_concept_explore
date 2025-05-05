from django.db import models
from django.db.models import Lookup, CharField

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
