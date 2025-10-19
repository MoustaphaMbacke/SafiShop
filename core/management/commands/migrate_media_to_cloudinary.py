from django.core.management.base import BaseCommand
from django.core.files import File
from django.conf import settings
from cloudinary_storage.storage import MediaCloudinaryStorage
import os

from core.models import Product, ProductImages, Vendor, Category
try:
    from userauths.models import Profile
except Exception:
    Profile = None


class Command(BaseCommand):
    help = 'Upload local media files to Cloudinary and update model fields.\nUse --commit to perform changes; by default runs a dry-run.'

    def add_arguments(self, parser):
        parser.add_argument('--commit', action='store_true', help='Actually upload and save changes (default: dry-run)')

    def handle(self, *args, **options):
        commit = options['commit']
        stor = MediaCloudinaryStorage()

        to_process = []

        # Map of queryset and field names to migrate
        to_process.append((Category.objects.all(), 'image'))
        to_process.append((Vendor.objects.all(), 'image'))
        to_process.append((Vendor.objects.all(), 'cover_image'))
        to_process.append((Product.objects.all(), 'image'))
        to_process.append((ProductImages.objects.all(), 'images'))
        if Profile is not None:
            to_process.append((Profile.objects.all(), 'image'))

        for qs, field_name in to_process:
            self.stdout.write(f'Processing {qs.model.__name__}.{field_name} ...')
            for obj in qs:
                field = getattr(obj, field_name, None)
                if not field:
                    continue
                # Skip if already points to Cloudinary (heuristic: URL starts with https://res.cloudinary)
                name = getattr(field, 'name', None)
                if not name:
                    continue
                if name.startswith('http') or 'res.cloudinary.com' in (getattr(field, 'url', '') or ''):
                    self.stdout.write(self.style.NOTICE(f'  SKIP {qs.model.__name__}#{obj.pk} - already remote: {name}'))
                    continue

                # Try to get local path
                try:
                    local_path = field.path
                except Exception:
                    self.stdout.write(self.style.WARNING(f'  SKIP {qs.model.__name__}#{obj.pk} - no local file path for {name}'))
                    continue

                if not os.path.exists(local_path):
                    self.stdout.write(self.style.WARNING(f'  SKIP {qs.model.__name__}#{obj.pk} - file missing: {local_path}'))
                    continue

                self.stdout.write(f'  WILL UPLOAD {qs.model.__name__}#{obj.pk} -> {local_path}')

                if commit:
                    with open(local_path, 'rb') as f:
                        saved_name = stor.save(name, File(f))
                    # Update field name to the stored name and save object
                    setattr(obj, field_name, saved_name)
                    obj.save(update_fields=[field_name])
                    self.stdout.write(self.style.SUCCESS(f'  UPLOADED and updated: {saved_name}'))

        self.stdout.write(self.style.SUCCESS('Done.'))
