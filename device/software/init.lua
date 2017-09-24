local IDLE_AT_STARTUP_MS = 15000;

tmr.alarm(1,IDLE_AT_STARTUP_MS,0,function()
    dofile("meter.lua")
end)
