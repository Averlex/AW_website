from django.db.models.signals import post_migrate
from django.dispatch import receiver
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from .models import User


@receiver(post_migrate)
def create_groups_and_permissions(sender, **kwargs):
    if sender.name == 'webapp':  # Ensure this only runs for your app
        # content_types = ContentType.objects.all()
        groups_permissions = {
            'Администратор': {
                'permissions': Permission.objects.all(),
                'is_superuser': True,
                'is_staff': True,
                'match': 0,
            },
            'Сотрудник мастерской': {
                'permissions': [
                    # 'view_user',
                    # More permissions here
                ],
                'is_superuser': False,
                'is_staff': True,
                'match': 1,
            },
            'Довольный клиент': {
                'permissions': [
                    # More permissions here
                ],
                'is_superuser': False,
                'is_staff': False,
                'match': 2,
            },
        }

        for group_name, config in groups_permissions.items():
            group, created = Group.objects.get_or_create(name=group_name)
            group.permissions.set(config['permissions'])

            users = User.objects.filter(user_group=groups_permissions[group_name]['match'])

            for user in users:
                user.is_superuser = config['is_superuser']
                user.is_staff = config['is_staff']
                user.groups.add(group)
                user.save()

                print(f'Successfully assigned permissions to {user.username}')
