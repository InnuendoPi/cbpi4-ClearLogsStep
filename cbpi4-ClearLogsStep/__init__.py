from cbpi.api.step import CBPiStep, StepResult
from cbpi.api import *
from voluptuous.schema_builder import message
from cbpi.api.dataclasses import NotificationType
import logging
import glob
import os


@parameters([Property.Text(label="Notification", configurable=True, description="Text for notification"),
             Property.Select(label="AutoNext", options=["Yes", "No"], description="Automatically move to next step (Yes) or pause after Notification (No)")])
class ClearLogsStep(CBPiStep):

    async def on_start(self):
        try:
            log_names = glob.glob('./logs/sensor_*.log*')
            for f in log_names:
                os.remove(f)
        except Exception as e:
            logging.error("Failed to delete sensor log files {} {}".format(id, e))

    async def NextStep(self, **kwargs):
        await self.next()

    async def on_stop(self):
        self.summary = ""
        await self.push_update()

    async def run(self):
        self.AutoNext = True
        self.cbpi.notify('ClearLogsStep', 'ClearLogsStep finished', NotificationType.INFO)
        await self.next()

        return StepResult.DONE


def setup(cbpi):
    '''
    This method is called by the server during startup
    Here you need to register your plugins at the server
    :param cbpi: the cbpi core
    :return:
    '''

    cbpi.plugin.register("ClearLogsStep", ClearLogsStep)
