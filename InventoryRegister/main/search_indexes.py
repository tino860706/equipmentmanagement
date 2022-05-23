import datetime
from haystack import indexes
from .models import EquipmentIssue

class EquipmentIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    #department = indexes.CharField(document=True, use_template=True)
    #equipment_category = indexes.CharField(document=True, use_template=True)
    #serial_number = indexes.CharField(document=True, use_template=True)
    #description = indexes.TextField(document=True, use_template=True)
    date_of_issue = indexes.DateTimeField(model_attr='date_of_issue')
    #status = indexes.CharField(document=True, use_template=True)
    content_auto = indexes.EdgeNgramField(model_attr='name')

    def get_model(self):
        return EquipmentIssue

    def index_queryset(self):
        return self.get_model().objects.all()



