import asyncio
import aiohttp
from aiohttp import web
from cbpi.api.step import CBPiStep, StepResult
from cbpi.api.timer import Timer
from cbpi.api.dataclasses import Kettle, Props
from datetime import datetime
import time
from cbpi.api import *
import logging
from socket import timeout
from typing import KeysView
from cbpi.api.config import ConfigType
from cbpi.api.base import CBPiBase
from voluptuous.schema_builder import message
from cbpi.api.dataclasses import NotificationAction, NotificationType
import numpy as np
import requests
import warnings
from os import system, listdir, remove

@parameters([Property.Text(label="Notification", configurable=True, description="Text for notification"),
             Property.Select(label="AutoNext", options=["Yes", "No"], description="Automatically move to next step (Yes) or pause after Notification (No)")])
class ClearLogsStep(CBPiStep):

    async def NextStep(self, **kwargs):
        await self.next()

    async def on_timer_done(self, timer):
        self.summary = self.props.get("Notification", "")
        if self.AutoNext == True:
            self.cbpi.notify(self.name, self.props.get(
                "Notification", ""), NotificationType.INFO)
            await self.next()
        else:
            self.cbpi.notify(self.name, self.props.get("Notification", ""), NotificationType.INFO, action=[
                NotificationAction("Next Step", self.NextStep)])
            await self.push_update()

    async def on_start(self):
        # log_names = listdir('./logs/sensor_*.log*')
        log_names = glob.glob('./logs/sensor_*.log*')
        for f in log_names:
            os.remove(f)
        # for log_name in log_names:
            # remove(LOG_DIR+log_name)
        await self.push_update()

    async def run(self):
        self.cbpi.notify('ClearLogsStep', '...', NotificationType.INFO)
        return StepResult.DONE


def setup(cbpi):
    '''
    This method is called by the server during startup
    Here you need to register your plugins at the server
    :param cbpi: the cbpi core
    :return:
    '''

    cbpi.plugin.register("ClearLogsStep", ClearLogsStep)
