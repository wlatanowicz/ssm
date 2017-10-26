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
local led = 4

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
gpio.mode(led, gpio.OUTPUT)

sntp.sync(ntpServerIp, nil, nil, 1)
--rtctime.set(1436430589, 0);

-- init WS client
local ws = websocket.createClient()
ws:connect('ws://ssm.tsdev.pl:8000')
local wsConneted = false

local i = 0
local n = 1000
local valueB = 0
local ivalueB = 0

local main = function ()
    
    local measure1
    local measure2
    local value
    local ivalue
    gpio.write(pin, gpio.LOW)
    measure1 = adc.read(0)
    gpio.write(pin, gpio.HIGH)
    measure2 = adc.read(0)
    
    value = (measure2 - 511.) * 2.5 / 511.
    valueB = valueB + math.pow(value, 2)
    
    ivalue = (measure1 - 511.) * 2.5 / 511.
    ivalueB = ivalueB + ivalue
    
    i = i + 1
    
    if ( i >= n ) then
      gpio.write(led, gpio.LOW)
    
      local s = ((4.46 * math.sqrt(valueB / i)) - 0.05) / ((ivalueB / i) + 0.0)
    
      local sec, usec, rate = rtctime.get()

      local json = sjson.encode({
            id = deviceID,
            ts = sec .. "." .. utils.strpad(usec, 6, "0", STR_PAD_LEFT),
            s = s
          })
      
      print(json)
      if (wsConneted) then
        ws:send(json)
        print("sent")
      else
        print("WS not connected")
      end
      
      i = 0
      valueB = 0
      ivalueB = 0
      
      gpio.write(led, gpio.HIGH)      
    end
    
    tmr.start(0)
end

ws:on("connection", function(ws)
  print('got ws connection')
  wsConneted = true
  tmr.alarm(0, 1, tmr.ALARM_SEMI, main)
end)

ws:on("close", function(_, status)
  print('connection closed', status)
  wsConneted = false
  ws = nil -- required to lua gc the websocket client
end)

