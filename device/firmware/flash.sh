
export PORT=/dev/tty.wchusbserial1410

esptool.py --port $PORT erase_flash
esptool.py --port $PORT write_flash -fm dio 0x00000 nodemcu-master-13-modules-2017-09-24-07-24-59-float.bin
