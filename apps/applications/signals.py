from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Application, ApplicationTracking

@receiver(post_save, sender=Application)
def create_application_tracking(sender, instance, created, **kwargs):
    """
    Create a tracking log entry when an application is created or its status is updated.
    """
    if created:
        # For new applications, create the initial tracking entry
        ApplicationTracking.objects.create(
            application=instance,
            status=instance.status,
            remarks="Application submitted"
        )
    else:
        # Check if the status field was updated
        if instance.tracker.has_changed('status_id'):
            ApplicationTracking.objects.create(
                application=instance,
                status=instance.status,
                remarks=f"Status updated to {instance.status.name}",
                changed_by=instance.updated_by if hasattr(instance, 'updated_by') else None
            )