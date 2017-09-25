local M = {}

local function strpad(input, pad_length, pad_string, pad_type)
  local output = input

  if not pad_string then pad_string = ' ' end
  if not pad_type   then pad_type   = 'STR_PAD_RIGHT' end

  if pad_type == 'STR_PAD_BOTH' then
    local j = 0
    while string.len(output) < pad_length do
      output = j % 2 == 0 and output .. pad_string or pad_string .. output
      j = j + 1
    end
  else
    while string.len(output) < pad_length do
      output = pad_type == 'STR_PAD_LEFT' and pad_string .. output or output .. pad_string
    end
  end

  return output
end

M.strpad = strpad;

return M
