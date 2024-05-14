from __future__ import annotations

import textwrap

from caproto.asyncio.client import Context
from caproto.server import run, template_arg_parser

from ..base import CaprotoSaveIOC, check_args
from ..utils import now

# def export_nano_zebra_data(zebra, filepath, fastaxis):
#     j = 0
#     while zebra.pc.data_in_progress.get() == 1:
#         print("Waiting for zebra...")
#         ttime.sleep(0.1)
#         j += 1
#         if j > 10:
#             print("THE ZEBRA IS BEHAVING BADLY CARRYING ON")
#             break

#     time_d = zebra.pc.data.time.get()
#     enc1_d = zebra.pc.data.enc1.get()
#     enc2_d = zebra.pc.data.enc2.get()
#     enc3_d = zebra.pc.data.enc3.get()

#     px = zebra.pc.pulse_step.get()
#     if fastaxis == 'NANOHOR':
#         # Add half pixelsize to correct encoder
#         enc1_d = enc1_d + (px / 2)
#     elif fastaxis == 'NANOVER':
#         # Add half pixelsize to correct encoder
#         enc2_d = enc2_d + (px / 2)
#     elif fastaxis == 'NANOZ':
#         # Add half pixelsize to correct encoder
#         enc3_d = enc3_d + (px / 2)

#     size = (len(time_d),)
#     with h5py.File(filepath, "w") as f:
#         dset0 = f.create_dataset("zebra_time", size, dtype="f")
#         dset0[...] = np.array(time_d)
#         dset1 = f.create_dataset("enc1", size, dtype="f")
#         dset1[...] = np.array(enc1_d)
#         dset2 = f.create_dataset("enc2", size, dtype="f")
#         dset2[...] = np.array(enc2_d)
#         dset3 = f.create_dataset("enc3", size, dtype="f")
#         dset3[...] = np.array(enc3_d)


# class ZebraPositionCaptureData(Device):
#     """
#     Data arrays for the Zebra position capture function and their metadata.
#     """
#     # Data arrays
#     ...
#     enc1 = Cpt(EpicsSignal, "PC_ENC1")  # XF:05IDD-ES:1{Dev:Zebra2}:PC_ENC1
#     enc2 = Cpt(EpicsSignal, "PC_ENC2")  # XF:05IDD-ES:1{Dev:Zebra2}:PC_ENC2
#     enc3 = Cpt(EpicsSignal, "PC_ENC3")  # XF:05IDD-ES:1{Dev:Zebra2}:PC_ENC3
#     time = Cpt(EpicsSignal, "PC_TIME")  # XF:05IDD-ES:1{Dev:Zebra2}:PC_TIME
#     ...

# class ZebraPositionCapture(Device):
#     """
#     Signals for the position capture function of the Zebra
#     """

#     # Configuration settings and status PVs
#     ...
#     pulse_step = Cpt(EpicsSignalWithRBV, "PC_PULSE_STEP")  # XF:05IDD-ES:1{Dev:Zebra2}:PC_PULSE_STEP
#     ...
#     data_in_progress = Cpt(EpicsSignalRO, "ARRAY_ACQ")  # XF:05IDD-ES:1{Dev:Zebra2}:ARRAY_ACQ
#     ...
#     data = Cpt(ZebraPositionCaptureData, "")

# nanoZebra = SRXZebra(
#    "XF:05IDD-ES:1{Dev:Zebra2}:", name="nanoZebra",
#    read_attrs=["pc.data.enc1", "pc.data.enc2", "pc.data.enc3", "pc.data.time"],
# )


class ZebraSaveIOC(CaprotoSaveIOC):
    """Zebra caproto save IOC."""

    #     enc1 = Cpt(EpicsSignal, "PC_ENC1")
    #     enc2 = Cpt(EpicsSignal, "PC_ENC2")
    #     enc3 = Cpt(EpicsSignal, "PC_ENC3")
    #     enc4 = Cpt(EpicsSignal, "PC_ENC4")

    # data_in_progress = pvproperty()  # +
    # time_d = pvproperty()
    # enc1_d = pvproperty()
    # enc2_d = pvproperty()
    # enc3_d = pvproperty()
    # pulse_step = pvproperty()

    def __init__(self, *args, external_pvs=None, **kwargs):
        """Init method.

        external_pvs : dict
            a dictionary of external PVs with keys as human-readable names.
        """
        super().__init__(*args, **kwargs)
        self._external_pvs = external_pvs

    # async def _stage(self, *args, **kwargs):
    #     ret = await super()._stage(*args, **kwargs)
    #     return ret

    async def _get_current_dataset(self, frame, external_pv="enc1"):
        client_context = Context()
        (pvobject,) = await client_context.get_pvs(self._external_pvs[external_pv])
        print(f"{pvobject = }")
        # pvobject = pvobjects[0]
        ret = await pvobject.read()

        dataset = ret.data

        print(f"{now()}:\n{dataset} {dataset.shape}")

        return dataset


if __name__ == "__main__":
    parser, split_args = template_arg_parser(
        default_prefix="", desc=textwrap.dedent(ZebraSaveIOC.__doc__)
    )
    ioc_options, run_options = check_args(parser, split_args)

    external_pvs = {
        "pulse_step": "XF:05IDD-ES:1{Dev:Zebra2}:PC_PULSE_STEP",
        "data_in_progress": "XF:05IDD-ES:1{Dev:Zebra2}:ARRAY_ACQ",
        "enc1": "XF:05IDD-ES:1{Dev:Zebra2}:PC_ENC1",
        "enc2": "XF:05IDD-ES:1{Dev:Zebra2}:PC_ENC2",
        "enc3": "XF:05IDD-ES:1{Dev:Zebra2}:PC_ENC3",
        "time": "XF:05IDD-ES:1{Dev:Zebra2}:PC_TIME",
    }

    ioc = ZebraSaveIOC(external_pvs=external_pvs, **ioc_options)
    run(ioc.pvdb, **run_options)
