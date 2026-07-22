#!/bin/bash

set -e

DUMP_OUT=$1

function usage() {
	echo "Usage: ./extract-files.sh <dumprx-out-dir>"
	exit 1
}

if [[ -z $DUMP_OUT ]] || [[ ! -d $DUMP_OUT ]]; then
	usage
fi

# Clean and create needed directories
for dir in ./modules/vendor_dlkm ./modules/system_dlkm ./modules/vendor_boot ./images ./images/dtbs; do
    rm -rf $dir
    mkdir -p $dir
done

# BOOT
echo "Copying the kernel"
cp "$DUMP_OUT/boot/kernel" ./images/kernel
echo "Done"

# VENDOR_BOOT - ramdisk modules
echo "Copying vendor_boot ramdisk modules"
for module in $(find "$DUMP_OUT/vendor_boot/ramdisk" \( -name "*.ko" -o -name "modules.load*" -o -name "modules.blocklist" \)); do
	cp "$module" ./modules/vendor_boot/
done
echo "Done"

# VENDOR_DLKM modules
echo "Copying vendor_dlkm modules"
for module in $(find "$DUMP_OUT/vendor_dlkm/lib/modules" -maxdepth 1 \( -name "*.ko" -o -name "modules.load*" -o -name "modules.blocklist" \)); do
	cp "$module" ./modules/vendor_dlkm/
done
echo "Done"

# SYSTEM_DLKM modules
echo "Copying system_dlkm modules"
cp -r "$DUMP_OUT"/system_dlkm/lib/modules/6.1* ./modules/system_dlkm/
echo "Done"

# DTBO and vendor_boot DTBs (dumprx already split these out)
echo "Copying DTBs"
find "$DUMP_OUT/vendor_boot/dtb" -type f -name "*.dtb" \
    -exec cp {} ./images/dtbs/ \; \
    -exec printf "  - dtbs/" \; \
    -exec basename {} \;

echo "Copying dtbo.img"
cp -f "$DUMP_OUT/dtbo.img" ./images/dtbo.img
echo "Done"

echo "Extracted files successfully"
