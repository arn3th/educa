from django.db import models
from django.core.exceptions import ObjectDoesNotExist


class OrderField(models.PositiveIntegerField):

    def __init__(self, for_fields=None, *args, **kwargs):
        self.for_fields = for_fields
        super(OrderField, self).__init__(*args, **kwargs)

    def pre_save(self, model_instance, add):
        if getattr(model_instance, self.attname) is None:
            # Brak bieżącej wartości
            try:
                qs = self.model.objects.all() # dla np. modelu 'Module'
                if self.for_fields: # for_fields np. ['course']
                    # Filtrowanie, pobierz te modules, gdzie course jest taki sam jak w aktualnym model_instance
                    query = {field: getattr(model_instance, field) for field in self.for_fields}
                    qs = qs.filter(**query)
                # Pobranie ostatniego elementu i wartości jego pola OrderField
                last_item = qs.latest(self.attname)
                value = last_item.order + 1
            except ObjectDoesNotExist:
                value = 0
            setattr(model_instance, self.attname, value) # zapisanie i niżej zwrócenie
            return value
        else:
            return super(OrderField, self).pre_save(model_instance, add)