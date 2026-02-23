from django.db import models
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model

User = settings.AUTH_USER_MODEL

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    profile_pic = models.ImageField(upload_to='profile_pics/', default='default.png', blank=True)
    department = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return f"{self.user.username}'s Profile"

class ContributionType(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    base_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    def __str__(self):
        return self.name

class Payment(models.Model):
    STATUS_CHOICES = [
        ('Not Paid', 'Not Paid'),
        ('Pending', 'Pending'),
        ('Confirmed', 'Confirmed'),
        ('Rejected', 'Rejected'),
    ]
    
    serial_number = models.PositiveIntegerField(editable=False, null=True, blank=True)
    member = models.ForeignKey(User, on_delete=models.CASCADE, related_name='payments')
    contribution_type = models.ForeignKey(ContributionType, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    reference_number = models.CharField(max_length=50, blank=True, null=True)
    receipt_image = models.FileField(upload_to='receipts/', null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Not Paid')
    admin_comment = models.TextField(blank=True, null=True)
    date_paid = models.DateTimeField(auto_now_add=True)
    verified_by = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True, 
        related_name='verified_payments'
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['reference_number'], 
                name='unique_reference_number',
                condition=models.Q(reference_number__isnull=False)
            )
        ]
        ordering = ['-date_paid']

    def __str__(self):
        return f"#{self.serial_number} - {self.member.username} ({self.contribution_type.name})"

    def save(self, *args, **kwargs):
        if not self.serial_number:
            last_payment = Payment.objects.filter(member=self.member).order_by('serial_number').last()
            self.serial_number = (last_payment.serial_number + 1) if last_payment else 1
        super().save(*args, **kwargs)

# --- SIGNALS ---

@receiver(post_save, sender=get_user_model())
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.get_or_create(user=instance)

@receiver(post_save, sender=ContributionType)
def create_payments_for_all_users(sender, instance, created, **kwargs):
    if created:
        MemberModel = get_user_model()
        all_members = MemberModel.objects.all()
        for member in all_members:
            Payment.objects.get_or_create(
                member=member,
                contribution_type=instance,
                defaults={'amount': instance.base_amount, 'status': 'Not Paid'}
            )

@receiver(post_save, sender=get_user_model())
def create_payments_for_new_member(sender, instance, created, **kwargs):
    if created:
        all_contribution_types = ContributionType.objects.all()
        for cont_type in all_contribution_types:
                member=instance,
                contribution_type=cont_type,
                defaults={'amount': cont_type.base_amount, 'status': 'Not Paid'}
