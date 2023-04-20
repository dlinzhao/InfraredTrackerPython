import numpy as np
import cv2

REGISTERED_TRACKER = {}


def register_tracker(cls, name=None):
    global REGISTERED_TRACKER
    if name is None:
        name = cls.__name__
    assert name not in REGISTERED_TRACKER, f"exist class: {REGISTERED_TRACKER}"
    REGISTERED_TRACKER[name] = cls
    return cls


def get_tracker(name):
    global REGISTERED_TRACKER
    assert name in REGISTERED_TRACKER, f"available class: {REGISTERED_TRACKER}"
    return REGISTERED_TRACKER[name]


class TrackerBase():
    def __init__(self):
        self.name = None
        self.tracker = None
        self.bbox = None

    def initTracker(self, frame, bbox):
        self.bbox = bbox
        return self.tracker.init(frame, bbox)

    def tracking(self, frame):
        ok, self.bbox = self.tracker.update(frame)
        return ok

    def getResults(self):
        return self.bbox

    def isWorking(self):
        return True
    
    def stopTracking(self):
        pass


@register_tracker
class TrackerKCF(TrackerBase):
    def __init__(self):
        super().__init__()
        self.name = 'TrackerKCF'
        self.tracker = cv2.TrackerKCF_create()


@register_tracker
class TrackerMIL(TrackerBase):
    def __init__(self):
        super().__init__()
        self.name = 'TrackerMIL'
        self.tracker = cv2.TrackerMIL_create()


@register_tracker
class TrackerTLD(TrackerBase):
    def __init__(self):
        super().__init__()
        self.name = 'TrackerTLD'
        self.tracker = cv2.TrackerTLD_create()


@register_tracker
class TrackerCSRT(TrackerBase):
    def __init__(self):
        super().__init__()
        self.name = 'TrackerCSRT'
        self.tracker = cv2.TrackerCSRT_create()


@register_tracker
class TrackerMOSSE(TrackerBase):
    def __init__(self):
        super().__init__()
        self.name = 'TrackerMOSSE'
        self.tracker = cv2.TrackerMOSSE_create()


@register_tracker
class TrackerGOTURN(TrackerBase):
    def __init__(self):
        super().__init__()
        self.name = 'TrackerGOTURN'
        self.tracker = cv2.TrackerGOTURN_create()


@register_tracker
class TrackerBoosting(TrackerBase):
    def __init__(self):
        super().__init__()
        self.name = 'TrackerBoosting'
        self.tracker = cv2.TrackerBoosting_create()


@register_tracker
class TrackerMedianFlow(TrackerBase):
    def __init__(self):
        super().__init__()
        self.name = 'TrackerMedianFlow'
        self.tracker = cv2.TrackerMedianFlow_create()
