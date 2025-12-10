from django.contrib.auth.models import User
from django.db.models.signals import (
    pre_init,   post_init,
    pre_save,   post_save,
    pre_delete, post_delete,
    m2m_changed
)

from django.dispatch import receiver
from django.contrib.auth.models import Group


# quando um objeto está prestes a ser instanciado
@receiver(pre_init, sender=User)
def pre_init_user(sender, *args, **kwargs):
    pass

# logo após a instanciação do objeto
@receiver(post_init, sender=User)
def post_init_user(sender, instance, **kwargs):
    pass

# antes de salvar o objeto
@receiver(pre_save, sender=User)
def pre_save_user(sender, instance, **kwargs):
    pass

# depois de salvar o objeto
@receiver(post_save, sender=User)
def post_save_user(sender, instance, created, **kwargs):
    if created:
        pass
    else:
        pass

# antes de deletar o objeto
@receiver(pre_delete, sender=User)
def pre_delete_user(sender, instance, **kwargs):
    pass

# depois de deletar o objeto
@receiver(post_delete, sender=User)
def post_delete_user(sender, instance, **kwargs):
    pass

# quando mudar uma relação many-to-many
@receiver(m2m_changed, sender=User.groups.through)
def m2m_changed_user(sender, instance, action, reverse, model, pk_set, **kwargs):
    pass