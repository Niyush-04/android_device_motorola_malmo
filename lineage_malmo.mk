#
# SPDX-FileCopyrightText: The LineageOS Project
# SPDX-License-Identifier: Apache-2.0
#

# Inherit from those products. Most specific first.
$(call inherit-product, $(SRC_TARGET_DIR)/product/core_64_bit_only.mk)
$(call inherit-product, $(SRC_TARGET_DIR)/product/full_base_telephony.mk)

# Inherit some common Lineage stuff.
$(call inherit-product, vendor/lineage/config/common_full_phone.mk)

# Inherit from malmo device
$(call inherit-product, device/motorola/malmo/device.mk)

# Device identifiers
PRODUCT_DEVICE := malmo
PRODUCT_NAME := lineage_malmo
PRODUCT_BRAND := motorola
PRODUCT_MODEL := moto g85 5G
PRODUCT_MANUFACTURER := motorola

PRODUCT_BUILD_PROP_OVERRIDES += \
    BuildDesc="malmo_g-user 16 W1UOS36M-W1-ST31 bd8b26 release-keys" \
    BuildFingerprint=motorola/malmo_g/msi:16/W1UOS36M-W1-ST31/bd8b26:user/release-keys \
    DeviceName=malmo \
    DeviceProduct=malmo_g

# GMS
PRODUCT_GMS_CLIENTID_BASE := android-motorola
