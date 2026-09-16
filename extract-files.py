#!/usr/bin/env -S PYTHONPATH=../../../tools/extract-utils python3
#
# SPDX-FileCopyrightText: The LineageOS Project
# SPDX-License-Identifier: Apache-2.0
#

from extract_utils.fixups_blob import (
    blob_fixup,
    blob_fixups_user_type,
)
from extract_utils.fixups_lib import (
    lib_fixups,
    lib_fixups_user_type,
)
from extract_utils.main import (
    ExtractUtils,
    ExtractUtilsModule,
)

namespace_imports = [
    'hardware/qcom-caf/sm6375-6.1',
    'hardware/qcom-caf/wlan',
    'hardware/motorola',
    'vendor/qcom/opensource/commonsys/display',
    'vendor/qcom/opensource/commonsys-intf/display',
    'vendor/qcom/opensource/dataservices',
]


def lib_fixup_vendor_suffix(lib: str, partition: str, *args, **kwargs):
    return f'{lib}_{partition}' if partition == 'vendor' else None


lib_fixups: lib_fixups_user_type = {
    **lib_fixups,
    (
        'vendor.qti.diaghal@1.0',
        'vendor.qti.hardware.wifidisplaysession@1.0',
        'vendor.qti.ImsRtpService-V1-ndk',
        'vendor.qti.imsrtpservice@3.0',
        'vendor.qti.imsrtpservice@3.1',
    ): lib_fixup_vendor_suffix,
}


blob_fixups: blob_fixups_user_type = {
    'system_ext/lib64/libwfdnative.so': blob_fixup()
        .add_needed('libinput_shim.so'),
    (
        'vendor/bin/hw/vendor.qti.camera.provider-service_64',
        'vendor/lib64/camx.provider-impl.so',
        'vendor/lib64/libdpps.so',
        'vendor/lib64/liblearningmodule.so',
        'vendor/lib64/libsnapdragoncolor-manager.so',
    ): blob_fixup()
        .replace_needed('libtinyxml2.so', 'libtinyxml2-v34.so'),
    (
        'vendor/bin/qcc-vendor',
        'vendor/bin/qms',
        'vendor/bin/xtra-daemon',
        'vendor/lib64/libcne.so',
        'vendor/lib64/libqcc_sdk.so',
        'vendor/lib64/libqms_client.so',
    ): blob_fixup()
        .add_needed('libbinder_shim.so'),
    'vendor/lib64/libqcodec2_core.so': blob_fixup()
        .add_needed('libcodec2_shim.so'),
    'vendor/lib64/vendor.libdpmframework.so': blob_fixup()
        .add_needed('libbinder_shim.so')
        .add_needed('libhidlbase_shim.so'),
    'vendor/etc/seccomp_policy/c2audio.vendor.ext-arm64.policy': blob_fixup()
        .add_line_if_missing('setsockopt: 1'),
    'vendor/lib64/libsensorndkbridge.so': blob_fixup()
        .replace_needed('android.hardware.sensors-V2-ndk.so', 'android.hardware.sensors-V3-ndk.so'),
    'system_ext/etc/permissions/moto-telephony.xml': blob_fixup()
        .regex_replace('/system/', '/system_ext/'),
}  # fmt: skip


module = ExtractUtilsModule(
    'malmo',
    'motorola',
    blob_fixups=blob_fixups,
    lib_fixups=lib_fixups,
    namespace_imports=namespace_imports,
    add_generated_carriersettings=True,
)

if __name__ == '__main__':
    utils = ExtractUtils.device(module)
    utils.run()
