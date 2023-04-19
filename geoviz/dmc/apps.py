from django.apps import AppConfig
import os

class DmcConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'dmc'
    label= 'dmc'

        # enbable this code in prodcution
    def ready(self):
        run_once = os.environ.get('CMDLINERUNNER_RUN_ONCE')
        if run_once is not None:
            return
        os.environ['CMDLINERUNNER_RUN_ONCE'] = 'True'
        from jobs import updater
        updater.start()
