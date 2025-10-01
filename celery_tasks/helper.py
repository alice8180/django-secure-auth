

# create your background task helper function ad classes


class ManageInvalidObjects:
    def __init__(self, model):
        self.model = model
        self.queryset = None   # store filtered queryset
    
    def filter_objects(self, **kwargs):
        self.queryset = self.model.objects.filter(**kwargs)
        return self.queryset
    
    def clean_obj(self):
        if self.queryset is None:
            return 0
        count = self.queryset.count()
        self.queryset.delete()
        return count
