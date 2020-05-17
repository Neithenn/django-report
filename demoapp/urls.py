from django.contrib import admin
from django.urls import path
from reports.views import start, createRecord, editRecord, deleteRecord, export_records_csv, delete_all_content, upload_content

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', start, name = 'index'),
    path('create/', createRecord, name = 'create'),
    path('edit/<int:id>', editRecord, name = 'edit'),
    path('delete/<int:id>', deleteRecord, name = 'delete'),
    path('export/csv/', export_records_csv, name='export_records_csv'),
    path('deleteall', delete_all_content, name='delete_all_content'),
    path('upload/csv', upload_content, name='upload_content'),
]
