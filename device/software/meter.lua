local utils = require("utils")

--configuration: BEGIN

--wifi
wifiCfg = {}
wifiCfg.ssid = "flux2g";
wifiCfg.pwd = "1qazxsw23edc";

wifiDHCP = false;
wifiIP = "192.168.0.61";
wifiMask = "255.255.255.0"
wifiGateway = "192.168.0.1"

ntpServerIp = "17.253.38.253";

deviceID = node.chipid() .. "-" .. node.flashid();

-- Pin definition 
local pin = 8
local duration = 500

--configuration:END


--init network:

wifi.setmode(wifi.STATION);
wifi.sta.config(wifiCfg);

if (not wifiDHCP) then
    wifi.sta.setip({
        ip = wifiIP,
        netmask = wifiMask,
        gateway = wifiGateway
    });
end

if ( wifi.sta.getip() ~= nil ) then
    print("IP: " .. wifi.sta.getip())
else
    print("IP: not set yet")
end
-- Initialising pin
gpio.mode(pin, gpio.OUTPUT)

sntp.sync(ntpServerIp, nil, nil, 1)
--rtctime.set(1436430589, 0);

-- Create an interval
tmr.alarm(0, duration, 1, function ()
    local measure1
    local measure2
    gpio.write(pin, gpio.HIGH)
    measure1 = adc.read(0)
    gpio.write(pin, gpio.LOW)
    measure2 = adc.read(0)

    local sec, usec, rate = rtctime.get()

    print(sec .. "." .. utils.strpad(usec, 6, "0", STR_PAD_LEFT))
    print(measure1, measure2)
    
    local json = sjson.encode({
          id = deviceID,
          ts = sec .. "." .. utils.strpad(usec, 6, "0", STR_PAD_LEFT),
          m1 = measure1,
          m2 = measure2
        })
      
    print(123/2)
    print(json)
end)
