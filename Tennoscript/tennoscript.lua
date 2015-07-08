--WIP
--vowel: shift up
--consonant: rotate
--symbol: nothing
--negative margin

local p = {}
 
local CharData = mw.loadData( 'Module:FactionScript/data' )

local function get_tenno ( word, para )
	if (para == nil or para == '') then para = 1 end
	return CharData["TennoChar"][word][para]
end

local function get_legit_size ( img_size, client_size )
	return math.ceil((img_size/20)*client_size)
end

function p.tenno( frame )
	local output_string = {}
	local humanwords = string.lower(frame.args[1])
	local size = frame.args[2]
	if (size == nil or size == '') then size='16' end
	local replacement = ""
	local char_type = ""
	local native_size = ""
	local i=1
	while i<=string.len(humanwords) do
		local first_char = humanwords:sub(i,i)
		local second_char = humanwords:sub(i+1,i+1)
		local third_char = humanwords:sub(i+2,i+2)
		if first_char == ("t" or "d" or "s" or "z" or "c" or "k" or "i" or "u") then
			if second_char == "h" then
				replacement = get_tenno(first_char.."h",1)
				char_type = get_tenno(first_char.."h",2)
				native_size = get_tenno(first_char.."h",3)
				i=i+2
			else
				replacement = get_tenno(first_char,1)
				char_type = get_tenno(first_char,2)
				native_size = get_tenno(first_char,3)
				i=i+1
			end
		elseif first_char == ("n") then
			char_type = "consonant"
			if second_char == "g" then
				replacement = get_tenno("ng",1)
				native_size = get_tenno("ng",3)
				i=i+2
			else
				replacement = get_tenno("n",1)
				native_size = get_tenno("n",3)
				i=i+1
			end
		elseif  first_char == ("e") then
			char_type = "vowel"
			if second_char == ("e" or "h") then
				replacement = get_tenno("e"..second_char)
				native_size = get_tenno("e"..second_char,3)
				i=i+2
			else 
				replacement = get_tenno("e")
				native_size = get_tenno("e",3)
				i=i+1
			end
		elseif first_char == ("a") then
			char_type = "vowel"
			if second_char == ("w" or "e") then
				replacement = get_tenno("a"..second_char)
				native_size = get_tenno("a"..second_char,3)
				i=i+2
			elseif second_char == ("y") then
				replacement = get_tenno("aye")
				native_size = get_tenno("aye",3)
				i=i+3
			else
				replacement = get_tenno("a")
				native_size = get_tenno("a",3)
				i=i+1
			end
		elseif first_char == ("o") then
			char_type = "vowel"
			if second_char == ("o" or "w") then
				replacement = get_tenno("o"..second_char)
				native_size = get_tenno("o"..second_char,3)
				i=i+2
			else 
				replacement = get_tenno("o")
				native_size = get_tenno("o",3)
				i=i+1
			end
		elseif CharData["TennoChar"][humanwords:sub(i,i)] ~= nil then
			replacement = get_tenno(humanwords:sub(i,i),1)
			char_type = get_tenno(humanwords:sub(i,i),2)
			native_size = get_tenno(humanwords:sub(i,i),3)
			i=i+1
		else
			replacement = '&nbsp;'
			i=i+1
		end
		if replacement ~= '&nbsp;' then
			if (char_type == "consonant" and native_size > 50) then
				replacement = '<div style="display:inline-block;transform:rotate(20deg);margin-right:-40px;">[[File:'..replacement..'|'..get_legit_size(native_size,size)..'px|link=]]</div>'
			elseif (char_type == "consonant" or char_type == "vowel") then
				replacement = '<div style="display:inline-block;transform:rotate(20deg) translateY(-12px);">[[File:'..replacement..'|'..get_legit_size(native_size,size)..'px|link=]]</div>'
			else
				replacement = '<div style="display:inline-block;">[[File:'..replacement..'|'..get_legit_size(native_size,size)..'px|link=]]</div>'
			end
		end
		table.insert(output_string,replacement)
	end
	return table.concat(output_string).."<br/>"
end

return p
