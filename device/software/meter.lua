--configuration: BEGIN

--wifi
wifiSSID = "astrohub";
wifiPassword = "1qazxsw23edc";

wifiDHCP = false;
wifiIP = "192.168.0.51";
wifiMask = "255.255.255.0"
wifiGateway = "192.168.0.1"

-- Pin definition 
local pin = 8
local duration = 5

--configuration:END


--init network:

wifi.setmode(wifi.STATION);
wifi.sta.config(wifiSSID, wifiPassword);

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

-- Create an interval
tmr.alarm(0, duration, 1, function ()
    local measure1
    local measure2
    gpio.write(pin, gpio.HIGH)
    measure1 = adc.read(0)
    gpio.write(pin, gpio.LOW)
    measure2 = adc.read(0)

    print(measure1, measure2)
end)
